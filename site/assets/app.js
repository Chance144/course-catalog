const state = {
  catalog: null,
  pageDept: document.body.dataset.dept || "all",
};

const els = {
  search: document.querySelector("#search"),
  count: document.querySelector("#result-count"),
  list: document.querySelector("#course-list"),
  empty: document.querySelector("#empty-state"),
  deptRadios: document.querySelectorAll('input[name="dept"]'),
  levelRadios: document.querySelectorAll('input[name="level"]'),
  writingRadios: document.querySelectorAll('input[name="writing"]'),
};

function selected(name) {
  const checked = document.querySelector(`input[name="${name}"]:checked`);
  return checked ? checked.value : "all";
}

function setRadio(name, value) {
  const input = document.querySelector(`input[name="${name}"][value="${value}"]`);
  if (input) input.checked = true;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[char]));
}

function highlight(value, query) {
  const text = escapeHtml(value || "");
  const tokens = [...new Set(query.trim().toLowerCase().split(/\s+/).filter((token) => token.length > 1))];
  if (!text || !tokens.length) return text;
  const pattern = new RegExp(`(${tokens.map((token) => token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`, "gi");
  return text.replace(pattern, "<mark>$1</mark>");
}

function normalize(value) {
  return value.toLowerCase().replace(/[_-]/g, " ").replace(/\s+/g, " ").trim();
}

function matchesCourse(course, query) {
  if (!query) return true;
  const haystack = course.searchText;
  return normalize(query).split(" ").every((token) => {
    if (!token) return true;
    return haystack.includes(token) || haystack.replace(/\s+/g, "").includes(token.replace(/\s+/g, ""));
  });
}

function creditLabel(credits) {
  return /^v\s/i.test(credits) ? `${credits} credits` : `${credits} credit${credits === "1" ? "" : "s"}`;
}

function coursePath(course) {
  return `${course.dept === "I_BUS" ? "/ibus/" : "/mktg/"}#${course.id}`;
}

function renderCourse(course, query) {
  const badges = [
    course.writingM ? '<span class="badge badge-m">[M] Writing</span>' : "",
    `<span class="badge ${course.level === "graduate" ? "badge-grad" : ""}">${course.level}</span>`,
    `<span class="badge">${escapeHtml(creditLabel(course.credits))}</span>`,
    course.effectiveThrough ? `<span class="badge">Effective through ${escapeHtml(course.effectiveThrough)}</span>` : "",
  ].join("");

  const blocks = [];
  if (course.prerequisite) {
    blocks.push(`<p class="prereq"><span class="meta-label">Course Prerequisite</span>${highlight(course.prerequisite, query)}</p>`);
  }
  if (course.description) {
    blocks.push(`<p class="desc">${highlight(course.description, query)}</p>`);
  }
  if (course.recommended) {
    blocks.push(`<p class="recommended"><span class="meta-label">Recommended preparation</span>${highlight(course.recommended, query)}</p>`);
  }
  if (course.repeatable) {
    blocks.push(`<p class="repeatable">${highlight(course.repeatable, query)}</p>`);
  }
  if (course.crosslisted) {
    blocks.push(`<p class="crosslist">Crosslisted course offered as ${highlight(course.crosslisted, query)}.</p>`);
  }
  if (course.typicallyOffered) {
    blocks.push(`<p class="offered">Typically offered ${escapeHtml(course.typicallyOffered)}.</p>`);
  }
  if (course.grading) {
    blocks.push(`<p class="grading">${escapeHtml(course.grading)}.</p>`);
  }

  return `
    <article class="course" id="${escapeHtml(course.id)}" data-dept="${escapeHtml(course.dept)}">
      <div class="course-top">
        <a class="course-code" href="${coursePath(course)}">${escapeHtml(course.dept)} ${escapeHtml(course.numberDisplay)}</a>
        <div class="badges">${badges}</div>
      </div>
      <h2>${highlight(course.title, query)}</h2>
      ${blocks.join("")}
    </article>
  `;
}

function currentFilters() {
  return {
    q: els.search.value.trim(),
    dept: state.pageDept !== "all" ? state.pageDept : selected("dept"),
    level: selected("level"),
    writing: selected("writing"),
  };
}

function writeUrl(filters, replace = true) {
  const params = new URLSearchParams();
  if (filters.q) params.set("q", filters.q);
  if (state.pageDept === "all" && filters.dept !== "all") params.set("dept", filters.dept);
  if (filters.level !== "all") params.set("level", filters.level);
  if (filters.writing !== "all") params.set("writing", filters.writing);
  const query = params.toString();
  const url = `${location.pathname}${query ? `?${query}` : ""}${location.hash}`;
  history[replace ? "replaceState" : "pushState"](null, "", url);
}

function applyFilters() {
  if (!state.catalog) return;
  const filters = currentFilters();
  writeUrl(filters);

  const visible = state.catalog.courses.filter((course) => {
    if (filters.dept !== "all" && course.dept !== filters.dept) return false;
    if (filters.level !== "all" && course.level !== filters.level) return false;
    if (filters.writing === "m" && !course.writingM) return false;
    return matchesCourse(course, filters.q);
  });

  els.list.innerHTML = visible.map((course) => renderCourse(course, filters.q)).join("");
  els.empty.hidden = visible.length !== 0;
  const scope = filters.dept === "all" ? "courses" : `${filters.dept} courses`;
  els.count.textContent = `Showing ${visible.length} of ${
    filters.dept === "all" ? state.catalog.courses.length : state.catalog.courses.filter((course) => course.dept === filters.dept).length
  } ${scope}`;

  if (location.hash) {
    const target = document.getElementById(location.hash.slice(1));
    if (target) {
      target.classList.add("is-target");
      target.scrollIntoView({ block: "start" });
    }
  }
}

function hydrateFromUrl() {
  const params = new URLSearchParams(location.search);
  els.search.value = params.get("q") || "";
  setRadio("dept", params.get("dept") || "all");
  setRadio("level", params.get("level") || "all");
  setRadio("writing", params.get("writing") || "all");
}

function bindEvents() {
  els.search.addEventListener("input", applyFilters);
  document.querySelectorAll(".filters input").forEach((input) => {
    input.addEventListener("change", applyFilters);
  });
  window.addEventListener("popstate", () => {
    hydrateFromUrl();
    applyFilters();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && event.target !== els.search && !event.metaKey && !event.ctrlKey && !event.altKey) {
      event.preventDefault();
      els.search.focus();
    }
    if (event.key === "Escape" && event.target === els.search) {
      els.search.value = "";
      applyFilters();
      els.search.blur();
    }
  });
}

function updateDeptCounts() {
  const counts = { I_BUS: 0, MKTG: 0 };
  for (const course of state.catalog.courses) counts[course.dept] += 1;
  document.querySelectorAll("[data-dept-count]").forEach((node) => {
    const dept = node.getAttribute("data-dept-count");
    node.textContent = `${counts[dept]} courses`;
  });
}

async function init() {
  bindEvents();
  hydrateFromUrl();
  const response = await fetch("/assets/courses.json");
  if (!response.ok) {
    els.count.textContent = "Could not load the catalog.";
    return;
  }
  state.catalog = await response.json();
  updateDeptCounts();
  applyFilters();
}

init();
