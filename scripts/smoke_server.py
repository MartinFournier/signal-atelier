#!/usr/bin/env python3
"""Run a disposable, verified NeoForge dedicated-server smoke test."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import select
import signal
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "modrinth.index.json"
MODRINTH_HOST = "cdn.modrinth.com"
NEOFORGE_HOST = "maven.neoforged.net"


def safe_target(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes runtime directory: {relative}") from error
    return target


def require_url(url: str, host: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != host:
        raise ValueError(f"unapproved download URL: {url}")


def download(url: str, target: Path, host: str) -> None:
    require_url(url, host)
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "signal-atelier-smoke/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        require_url(response.geturl(), host)
        with target.open("wb") as output:
            shutil.copyfileobj(response, output)


def digest(path: Path, algorithm: str) -> str:
    checksum = hashlib.new(algorithm)
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def server_files(manifest: dict) -> list[dict]:
    return [
        entry
        for entry in manifest["files"]
        if entry.get("env", {}).get("server") != "unsupported"
    ]


def install_mods(runtime: Path, manifest: dict) -> int:
    entries = server_files(manifest)
    for entry in entries:
        target = safe_target(runtime, entry["path"])
        urls = entry.get("downloads", [])
        expected = entry.get("hashes", {}).get("sha512")
        if len(urls) != 1 or not expected:
            raise ValueError(f"manifest entry lacks one URL and SHA-512: {entry['path']}")
        download(urls[0], target, MODRINTH_HOST)
        if digest(target, "sha512") != expected:
            raise ValueError(f"SHA-512 mismatch: {entry['path']}")
    return len(entries)


def install_neoforge(runtime: Path, version: str, java: str) -> None:
    base = (
        f"https://{NEOFORGE_HOST}/releases/net/neoforged/neoforge/"
        f"{version}/neoforge-{version}-installer.jar"
    )
    installer = runtime / "neoforge-installer.jar"
    checksum_file = runtime / "neoforge-installer.jar.sha256"
    download(base, installer, NEOFORGE_HOST)
    download(f"{base}.sha256", checksum_file, NEOFORGE_HOST)
    expected = checksum_file.read_text(encoding="ascii").strip().split()[0]
    if len(expected) != 64 or digest(installer, "sha256") != expected:
        raise ValueError("NeoForge installer SHA-256 mismatch")

    with (runtime / "installer.log").open("wb") as log:
        result = subprocess.run(
            [java, "-jar", installer.name, "--installServer"],
            cwd=runtime,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=300,
            check=False,
        )
    if result.returncode != 0:
        raise RuntimeError("NeoForge server installation failed")


def free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def configure(runtime: Path) -> None:
    shutil.copytree(ROOT / "overrides", runtime, dirs_exist_ok=True)
    (runtime / "eula.txt").write_text("eula=true\n")
    (runtime / "server.properties").write_text(
        "online-mode=false\n"
        "server-ip=127.0.0.1\n"
        f"server-port={free_port()}\n"
        "motd=Signal Atelier smoke test\n"
        "max-players=1\n"
        "view-distance=4\n"
        "simulation-distance=4\n"
    )
    (runtime / "user_jvm_args.txt").write_text("-Xms1G\n-Xmx4G\n")


def stop_process(process: subprocess.Popen, force: bool = False) -> None:
    if process.poll() is not None:
        return
    os.killpg(process.pid, signal.SIGKILL if force else signal.SIGTERM)


def run_server(runtime: Path, timeout_seconds: int) -> None:
    log_path = runtime / "server-smoke.log"
    deadline = time.monotonic() + timeout_seconds
    started = False

    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            ["bash", "run.sh", "nogui"],
            cwd=runtime,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            start_new_session=True,
        )
        assert process.stdout is not None
        while time.monotonic() < deadline:
            readable, _, _ = select.select([process.stdout], [], [], 1)
            if not readable:
                if process.poll() is not None:
                    break
                continue
            line = process.stdout.readline()
            if line:
                log.write(line)
                log.flush()
                if "Done (" in line and 'For help, type "help"' in line:
                    started = True
                    break
            elif process.poll() is not None:
                break
            else:
                time.sleep(0.1)

        if started and process.stdin is not None:
            process.stdin.write("stop\n")
            process.stdin.flush()
        else:
            stop_process(process)

        try:
            return_code = process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            stop_process(process, force=True)
            process.wait(timeout=15)
            raise RuntimeError("server did not stop within 60 seconds")

    if not started:
        if time.monotonic() >= deadline:
            raise RuntimeError("server did not reach ready state before timeout")
        raise RuntimeError(f"server exited before ready state (code {return_code})")
    if return_code != 0:
        raise RuntimeError(f"server stopped with code {return_code}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--java", default="java", help="Java 25 executable")
    parser.add_argument("--timeout", type=int, default=600, help="startup timeout in seconds")
    parser.add_argument("--keep", action="store_true", help="retain the untrusted runtime")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(MANIFEST.read_text())
    version = manifest["dependencies"]["neoforge"]
    runtime = Path(tempfile.mkdtemp(prefix="signal-atelier-server-", dir="/tmp"))
    keep = args.keep

    print(f"Runtime: {runtime}")
    try:
        count = install_mods(runtime, manifest)
        print(f"Verified {count} server artifacts")
        install_neoforge(runtime, version, args.java)
        print(f"Verified and installed NeoForge {version}")
        configure(runtime)
        run_server(runtime, args.timeout)
        print("Dedicated server reached ready state and stopped cleanly")
        return 0
    except Exception as error:
        keep = True
        print(f"Smoke test failed: {error}", file=sys.stderr)
        print("Runtime retained for manual log review", file=sys.stderr)
        return 1
    finally:
        if not keep:
            shutil.rmtree(runtime)
        elif runtime.exists():
            print(f"Untrusted runtime retained at: {runtime}")


if __name__ == "__main__":
    sys.exit(main())
