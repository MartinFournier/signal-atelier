document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[role='main'] table").forEach((table) => {
    if (table.parentElement?.classList.contains("table-scroll")) {
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "table-scroll";
    table.before(wrapper);
    wrapper.append(table);
  });

  if (!window.location.pathname.endsWith("/reference/mods/")) {
    return;
  }

  const table = document.querySelector("[role='main'] table");
  if (!table || !table.tHead || !table.tBodies.length) {
    return;
  }

  const body = table.tBodies[0];
  const collator = new Intl.Collator(undefined, {
    numeric: true,
    sensitivity: "base",
  });

  table.classList.add("sortable-table");
  table.querySelectorAll("thead th").forEach((heading, column) => {
    const label = heading.textContent.trim();
    const button = document.createElement("button");
    button.type = "button";
    button.className = "sort-button";
    button.textContent = label;
    button.setAttribute("aria-label", `Sort by ${label}`);
    heading.textContent = "";
    heading.append(button);

    button.addEventListener("click", () => {
      const direction = heading.getAttribute("aria-sort") === "ascending"
        ? "descending"
        : "ascending";
      const multiplier = direction === "ascending" ? 1 : -1;
      const rows = Array.from(body.rows);

      table.querySelectorAll("thead th").forEach((item) => {
        item.removeAttribute("aria-sort");
      });
      heading.setAttribute("aria-sort", direction);

      rows.sort((left, right) => {
        const leftValue = left.cells[column]?.textContent.trim() ?? "";
        const rightValue = right.cells[column]?.textContent.trim() ?? "";
        return collator.compare(leftValue, rightValue) * multiplier;
      });
      rows.forEach((row) => body.append(row));
    });
  });
});
