# Mod integration matrix

This matrix explains why every pinned artifact belongs in Signal Atelier and
how it connects to the rest of the pack. **Static** means repository policy or
configuration exists; it does not mean the behavior has passed an in-game
test. See the [test plan](../test-plan.md) for runtime acceptance checks.

## Factory and progression

| Project | Pack role and connection | Enforcement and guidance | Evidence still required |
| --- | --- | --- | --- |
| [Oritech](https://modrinth.com/project/4sYI62kA) | Anchor technology system for power, processing, transport, remote work, and endgame production. | The engineering notebook follows its factory arc; no competing broad technology mod is included. | Complete progression, persistence, and production-rate pass. |
| [Oracle Index](https://modrinth.com/project/J8MMsNrL) | Oritech's in-game technical manual. | The Orientation chapter directs players to it before factory construction. | Confirm the book opens and covers the pinned Oritech build. |
| [Just Enough Items](https://modrinth.com/project/u6dRKJwZ) | Shared recipe and machine-process reference. | Locked recipes are removed through the pack datapack and must disappear from ordinary discovery. | Inspect all Oritech processes and locked entries in-game. |
| [Jade](https://modrinth.com/project/nvQzSEkH) | Identifies machines, inventories, and graves at the point of use. | Kept informational; it must not expose unintended hidden machine state. | Inspect Oritech and GraveStone overlays. |
| [Simply Quests](https://modrinth.com/project/uwJu7Fi8) | Reward-free engineering notebook joining the pack's systems into one progression. | Seven generated chapters and 27 manual milestones; recipes never depend on quest state. | Confirm loading, layout, team sync, persistence, and update behavior. |

## Storage and distributed work

| Project | Pack role and connection | Enforcement and guidance | Evidence still required |
| --- | --- | --- | --- |
| [Refined Storage](https://modrinth.com/project/KDvYkUg3) | Central storage, requests, and autocrafting powered by Oritech. | Wireless access, world interaction, and remote-network devices are recipe-locked; quests preserve Oritech machine-side logistics. | Test recursive requests and the Oritech machine/interface return loop. |
| [Chunk Loaders](https://modrinth.com/project/t1VgucWo) | Optional physical persistence for one carefully chosen remote work site. | Larger loaders and the upgrade path are locked; shipped config limits use to four chunks per player with an offline timeout. | Verify recipe, ownership, limits, restart behavior, and offline shutdown. |
| [Universal Data Pack](https://modrinth.com/project/TPKaNwWP) | Loads the pack-owned recipe restrictions consistently. | Carries the Refined Storage, backpack, and chunk-loader locks under `overrides/`. | Confirm every lock is active and hidden from normal recipe discovery. |
| [Traveler's Backpack](https://modrinth.com/project/rlloIFEV) | Modest expedition storage that can travel through the death-recovery loop. | Capacity, nesting, tanks, utilities, loot, and higher tiers are restricted through config and recipes. | Test capacities, nesting, graves, placement, pickup, logout, and restart. |
| [GraveStone Mod](https://modrinth.com/project/RYtXKJPr) | Sole death-recovery system for player inventory and equipped backpack contents. | Owner restriction and no-expiry policy ship as server defaults; no competing grave mod is included. | Test hazards, ownership, backpack transfer, duplication, and persistence. |
| [Xaero's World Map](https://modrinth.com/project/NcUtCpym) | Explored-terrain navigation and waypoints for remote Oritech sites. | Minimap, entity radar, and teleportation are outside pack policy. Runtime-generated privacy settings still need capture. | Verify explored-only mapping, teleport/radar state, and player markers. |

## Player information and handling

| Project | Pack role and connection | Enforcement and guidance | Evidence still required |
| --- | --- | --- | --- |
| [AppleSkin](https://modrinth.com/project/EsAfCjCV) | Makes vanilla food decisions legible without changing food progression. | Client-only informational role. | Confirm it remains a presentation-only convenience. |
| [Mouse Tweaks](https://modrinth.com/project/aC3cM3Vq) | Reduces friction across machine, backpack, and storage inventories. | Client-only input role with no progression effect. | Review inventory interactions and control conflicts. |
| [Better Advancements](https://modrinth.com/project/Q2OqKxDG) | Improves the vanilla advancement screen alongside the separate engineering notebook. | Client-only presentation role; Simply Quests remains the pack guide. | Confirm both interfaces remain distinct and usable. |
| [XP Tome](https://modrinth.com/project/AnpW69o3) | Stores a bounded level-30-equivalent XP reserve for workshop use. | Default 1,395 XP capacity is accepted; it must work safely with graves and restarts. | Test capacity, death, logout, restart, and duplication paths. |
| [Tax Free Levels](https://modrinth.com/project/jCBrrLTs) | Makes anvil costs use consistent raw XP alongside the XP Tome. | Pack config retains the vanilla anvil ceiling and one-level renaming. | Compare raw-XP costs at different starting levels. |
| [Enchantment Descriptions](https://modrinth.com/project/UVtY3ZAC) | Documents otherwise vanilla enchantments in tooltips. | No extraction, selection, reroll, or extra-enchantment system is included. | Verify tooltip coverage and dedicated-server independence. |

## Building and presentation

| Project | Pack role and connection | Enforcement and guidance | Evidence still required |
| --- | --- | --- | --- |
| [Rechiseled](https://modrinth.com/project/B0g2vT6l) | Sole broad decorative block expansion for industrial builds. | Avoids overlapping furniture and building systems. | Test recipes, connected textures, variants, and persistence. |
| [Simple Menu](https://modrinth.com/project/6pdhya1q) | Applies the Signal Atelier title, icon, wordmark, and restrained menu policy. | Pack assets and config hide Realms while retaining standard play and settings controls. | Check scaling, required buttons, warning visibility, and absence of promotions. |

## Performance, graphics, and sound

| Project | Pack role and connection | Enforcement and guidance | Evidence still required |
| --- | --- | --- | --- |
| [Sodium](https://modrinth.com/project/AANobbMI) | Base client renderer and performance layer. | Other visual features must remain compatible with its renderer. | Establish graphical baseline around Oritech machinery and portals. |
| [Lithium](https://modrinth.com/project/gvQqBUqZ) | Conservative game-logic optimization on client and server. | Preferred over aggressive world-threading or ticking changes. | Profile the full pack and isolate only if a regression appears. |
| [FerriteCore](https://modrinth.com/project/uXXizFIs) | Reduces memory overhead for the 4–6 GiB target. | Part of the baseline performance stack. | Measure clean-client and dedicated-server memory. |
| [ModernFix](https://modrinth.com/project/nmDcB62a) | Broad compatibility and resource-usage fixes. | Part of the baseline performance stack. | Confirm startup, resource reload, and server behavior. |
| [ImmediatelyFast](https://modrinth.com/project/5ZwdcRci) | Accelerates client immediate-mode rendering. | Client-only and subordinate to correctness. | Inspect GUIs, particles, maps, and Oritech rendering. |
| [Dynamic FPS](https://modrinth.com/project/LQ3K71Q1) | Reduces background resource use. | Shipped config disables optional runtime battery-library downloads. | Test focus loss, recovery, audio, and absence of downloads. |
| [Iris Shaders](https://modrinth.com/project/YL57xq9U) | Optional shader loader layered on Sodium. | Shaders stay disabled by default and outside minimum requirements. | Test toggling and Oritech, map, portal, and transparency rendering. |
| [Complementary Shaders - Reimagined](https://modrinth.com/project/HVnmMxH1) | Curated optional visual preset for Iris. | Bundled but disabled by default. | Validate performance and rendering at representative factory scale. |
| [LambDynamicLights](https://modrinth.com/project/yBW8D80W) | Conservative held-item and block lighting. | Optional visual enhancement that must coexist with Sodium and backpacks. | Test Oritech items, backpack integration, and update quality. |
| [Sound Physics Remastered](https://modrinth.com/project/qyVF9oeo) | Optional spatial sound for workshops and tunnels. | Must be independently disableable without affecting worlds or servers. | Test factories, tunnels, disabling, and reconnection. |

## Support libraries

These artifacts support the selected features and do not define separate pack
progression. They remain pinned, hashed, licensed, and covered by the same
manifest and server smoke checks.

| Project | Required by or used with |
| --- | --- |
| [Architectury API](https://modrinth.com/project/lhGA9TYQ) | Oracle Index |
| [Athena](https://modrinth.com/project/b1ZV3DIJ) | Oritech rendering |
| [Cloth Config API](https://modrinth.com/project/9s6osm5g) | Dynamic FPS, Sound Physics Remastered, and Tax Free Levels |
| [Collective](https://modrinth.com/project/e0M1UDsY) | Simple Menu |
| [Fusion](https://modrinth.com/project/p19vrgc2) | Rechiseled connected textures |
| [Geckolib](https://modrinth.com/project/8BmcQJ2H) | Oritech animation and rendering |
| [Prickle](https://modrinth.com/project/aaRl8GiW) | Enchantment Descriptions on the client |
| [SuperMartijn642's Config Lib](https://modrinth.com/project/LN9BxssP) | Chunk Loaders and Rechiseled |
| [SuperMartijn642's Core Lib](https://modrinth.com/project/rOUBggPv) | Chunk Loaders and Rechiseled |

## Integration backlog

The matrix exposes the remaining work in dependency order:

1. Complete the clean graphical baseline before changing recipes or captured
   runtime configuration.
2. Exercise the Oritech–Refined Storage interface loop, then refine quest text
   using observed machine names and costs.
3. Test the backpack–grave and XP Tome–enchanting recovery loops for loss or
   duplication.
4. Capture and sanitize Xaero and backpack runtime settings, then implement
   first-install-only map, backpack, and notebook bindings.
5. Balance the single chunk-loader recipe and define the Signal Core bill of
   materials from measured Oritech production rates.
6. Validate the complete visual stack before enabling splash text or making
   further branding changes.
