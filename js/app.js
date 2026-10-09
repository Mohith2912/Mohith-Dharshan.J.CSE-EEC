(function () {
  "use strict";

  const data = window.PORTFOLIO_DATA;
  const featuredRoot = document.querySelector("#featured-projects");
  const repoRoot = document.querySelector("#repo-grid");
  const filtersRoot = document.querySelector("#repo-filters");
  const repoCount = document.querySelector("#repo-count");
  const search = document.querySelector("#repo-search");
  const dialog = document.querySelector("#project-dialog");
  const dialogContent = document.querySelector("#dialog-content");
  const menuButton = document.querySelector(".menu-button");
  const navigation = document.querySelector("#primary-navigation");
  let activeCategory = "all";

  const arrowIcon = `
    <svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8">
      <path d="M5 12h14M13 6l6 6-6 6"/>
    </svg>`;

  function featuredCard(project, position) {
    const liveLink = project.live
      ? `<a href="${project.live}" data-live-project="${project.id}" aria-label="View ${project.title} live project">Live site</a>`
      : `<span>Case study</span>`;

    return `
      <article class="project-card project-card-${project.tone} reveal" data-delay="${position % 3}">
        <div class="project-card-top"><span class="mono">${project.index}</span><span>${project.label}</span></div>
        <div class="project-card-body">
          <h3>${project.title}</h3>
          <p>${project.summary}</p>
          <ul class="tag-list" aria-label="Technologies">${project.tags.map((tag) => `<li>${tag}</li>`).join("")}</ul>
        </div>
        <div class="project-card-footer">
          ${liveLink}
          <button type="button" data-project="${project.id}" aria-label="Open ${project.title} case study">How it works ${arrowIcon}</button>
        </div>
      </article>`;
  }

  function renderFeatured() {
    featuredRoot.innerHTML = data.featured.map(featuredCard).join("");
  }

  function openProject(projectId) {
    const project = data.featured.find((item) => item.id === projectId);
    if (!project) return;
    dialogContent.innerHTML = `
      <p class="eyebrow">${project.index} · Case study</p>
      <h2 id="dialog-title">${project.title}</h2>
      <p class="dialog-lead">${project.summary}</p>
      <div class="dialog-grid">
        <div>
          <span class="dialog-label mono">SYSTEM VIEW</span>
          <p>${project.detail}</p>
          <ul class="tag-list">${project.tags.map((tag) => `<li>${tag}</li>`).join("")}</ul>
        </div>
        <div>
          <span class="dialog-label mono">HOW IT WORKS</span>
          <ol class="dialog-flow">${project.flow.map((step, index) => `<li><span>${String(index + 1).padStart(2, "0")}</span><p>${step}</p></li>`).join("")}</ol>
        </div>
      </div>
      <div class="dialog-actions">
        <a class="button button-primary" href="${project.source}" target="_blank" rel="noreferrer">View source</a>
        ${project.live ? `<a class="button button-secondary" href="${project.live}" data-live-project="${project.id}">Open live project</a>` : ""}
      </div>`;
    dialog.showModal();
    document.body.classList.add("dialog-open");
  }

  function closeDialog() {
    dialog.close();
    document.body.classList.remove("dialog-open");
  }

  function repoCard(repo) {
    const url = `https://github.com/Mohith2912/${encodeURIComponent(repo.name)}`;
    return `
      <article class="repo-card reveal">
        <div class="repo-card-meta"><span>${repo.category}</span><span class="mono">${repo.language}</span></div>
        <h3>${repo.name}</h3>
        <p>${repo.description}</p>
        <a href="${url}" target="_blank" rel="noreferrer" aria-label="View ${repo.name} on GitHub">View repository ${arrowIcon}</a>
      </article>`;
  }

  function renderFilters() {
    const categories = ["all", ...new Set(data.repositories.map((repo) => repo.category))];
    filtersRoot.innerHTML = categories.map((category) => `
      <button type="button" data-category="${category}" aria-pressed="${category === "all"}">${category}</button>
    `).join("");
  }

  function renderRepositories() {
    const term = search.value.trim().toLowerCase();
    const visible = data.repositories.filter((repo) => {
      const categoryMatch = activeCategory === "all" || repo.category === activeCategory;
      const termMatch = !term || `${repo.name} ${repo.language} ${repo.description} ${repo.category}`.toLowerCase().includes(term);
      return categoryMatch && termMatch;
    });
    repoRoot.innerHTML = visible.map(repoCard).join("");
    repoCount.textContent = `${visible.length} of ${data.repositories.length} repositories`;
    if (!visible.length) repoRoot.innerHTML = `<p class="empty-state">No repositories match that search. Try a technology, product area, or clear the filter.</p>`;
    observeReveals(repoRoot);
  }

  function observeReveals(scope = document) {
    const items = scope.querySelectorAll(".reveal:not(.is-observed)");
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      items.forEach((item) => item.classList.add("is-visible", "is-observed"));
      return;
    }
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        currentObserver.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8%", threshold: 0.08 });
    items.forEach((item) => {
      item.classList.add("is-observed");
      observer.observe(item);
    });
  }

  function updatePageProgress() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
    document.querySelector("#page-progress-bar").style.width = `${Math.min(progress, 100)}%`;
  }

  function updateActiveNavigation() {
    const sections = [...document.querySelectorAll("main section[id]")];
    let current = "";
    sections.forEach((section) => {
      if (window.scrollY >= section.offsetTop - 180) current = section.id;
    });
    navigation.querySelectorAll("a").forEach((link) => {
      if (link.getAttribute("href") === `#${current}`) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  renderFeatured();
  renderFilters();
  renderRepositories();
  observeReveals();
  document.querySelector("#year").textContent = new Date().getFullYear();

  featuredRoot.addEventListener("click", (event) => {
    const button = event.target.closest("[data-project]");
    if (button) openProject(button.dataset.project);
  });
  filtersRoot.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category]");
    if (!button) return;
    activeCategory = button.dataset.category;
    filtersRoot.querySelectorAll("button").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    renderRepositories();
  });
  search.addEventListener("input", renderRepositories);
  dialog.querySelector(".dialog-close").addEventListener("click", closeDialog);
  dialog.addEventListener("click", (event) => { if (event.target === dialog) closeDialog(); });
  dialog.addEventListener("close", () => document.body.classList.remove("dialog-open"));

  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    navigation.classList.toggle("is-open", !open);
  });
  navigation.addEventListener("click", () => {
    menuButton.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
  });

  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    requestAnimationFrame(() => {
      updatePageProgress();
      updateActiveNavigation();
      ticking = false;
    });
    ticking = true;
  }, { passive: true });
  updatePageProgress();
  updateActiveNavigation();
})();
