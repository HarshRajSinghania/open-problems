// Open Problems catalogue: vanilla JS, no build step.
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const STATUS = ["suggested", "researching", "ready-to-build", "being-built",
    "solved", "handed-over", "paused"];
  let data = null;

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => {
      if (k === "text") node.textContent = v;
      else if (k === "style") node.style.cssText = v;
      else node.setAttribute(k, v);
    });
    (children || []).forEach((c) => node.appendChild(c));
    return node;
  }

  function option(select, value, label) {
    select.appendChild(el("option", { value: value, text: label }));
  }

  function readHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    $("q").value = p.get("q") || "";
    $("f-goal").value = p.get("goal") || "";
    $("f-progress").value = p.get("progress") || "";
    $("f-priority").value = p.get("priority") || "";
    $("f-status").value = p.get("status") || "";
  }

  function writeHash() {
    const p = new URLSearchParams();
    [["q", "q"], ["goal", "f-goal"], ["progress", "f-progress"],
     ["priority", "f-priority"], ["status", "f-status"]].forEach(([k, id]) => {
      if ($(id).value) p.set(k, $(id).value);
    });
    const h = p.toString();
    history.replaceState(null, "", h ? "#" + h : location.pathname);
  }

  function render() {
    const q = $("q").value.trim().toLowerCase();
    const goal = $("f-goal").value;
    const progress = $("f-progress").value;
    const priority = $("f-priority").value;
    const status = $("f-status").value;
    const shown = data.problems.filter((p) => {
      if (goal && String(p.goal) !== goal) return false;
      if (progress && p.progress !== progress) return false;
      if (priority && p.priority !== priority) return false;
      if (status && p.status !== status) return false;
      if (!q) return true;
      const hay = [p.target, p.title, p.un_target_text, p.plain,
        data.goals[p.goal].short, p.tags.join(" ")].join(" ").toLowerCase();
      return q.split(/\s+/).every((w) => hay.includes(w));
    });
    document.querySelectorAll("#goal-strip button").forEach((b) => {
      b.setAttribute("aria-pressed", String(b.dataset.goal === goal));
    });
    const cards = $("cards");
    cards.textContent = "";
    shown.forEach((p) => cards.appendChild(card(p)));
    if (!shown.length) {
      cards.appendChild(el("p", { class: "empty",
        text: "No targets match. Try fewer filters." }));
    }
    $("count").textContent = shown.length + " of " + data.problems.length +
      " targets";
    writeHash();
  }

  function card(p) {
    const g = data.goals[p.goal];
    const pr = data.progress[p.progress] || { emoji: "", label: p.progress };
    const badges = [
      el("span", { class: "badge", title: "UN progress assessment, 2026",
        text: pr.emoji + " " + pr.label.split(",")[0] }),
      el("span", { class: "badge" + (p.priority === "high" ? " high" : ""),
        text: "priority: " + p.priority }),
      el("span", { class: "badge", text: "status: " + p.status }),
    ];
    return el("article", { class: "card", style: "--goal:#" + g.colour }, [
      el("div", { class: "goal", text: "Goal " + p.goal + " · " + g.short }),
      el("h2", {}, [el("a", { href: p.url, text: p.target + " · " + p.title })]),
      el("p", { text: p.plain || p.un_target_text }),
      el("div", { class: "badges" }, badges),
      el("div", { class: "links" }, [
        el("a", { href: p.url, text: "Read the problem" }),
        el("a", { href: p.tasks_url, text: "Open tasks" }),
      ]),
    ]);
  }

  function setup() {
    const goalSel = $("f-goal");
    const strip = $("goal-strip");
    Object.entries(data.goals).forEach(([n, g]) => {
      option(goalSel, n, n + ". " + g.short);
      const b = el("button", { type: "button", "data-goal": n,
        title: "Goal " + n + ": " + g.short, "aria-label": "Goal " + n +
        ": " + g.short, style: "background:#" + g.colour, text: n });
      b.addEventListener("click", () => {
        goalSel.value = goalSel.value === n ? "" : n;
        render();
      });
      strip.appendChild(b);
    });
    Object.entries(data.progress).forEach(([k, v]) => {
      option($("f-progress"), k, v.emoji + " " + v.label.split(",")[0]);
    });
    STATUS.forEach((s) => option($("f-status"), s, s));
    ["q", "f-goal", "f-progress", "f-priority", "f-status"].forEach((id) => {
      $(id).addEventListener("input", render);
    });
    $("reset").addEventListener("click", () => {
      ["q", "f-goal", "f-progress", "f-priority", "f-status"]
        .forEach((id) => { $(id).value = ""; });
      render();
    });
    if (data.un_numbers_retrieved) {
      $("retrieved").textContent = "UN World numbers retrieved " +
        data.un_numbers_retrieved + ".";
    }
    readHash();
    render();
  }

  fetch("data/problems.json")
    .then((r) => r.json())
    .then((d) => { data = d; setup(); })
    .catch(() => {
      $("count").textContent = "Could not load the catalogue data.";
    });
})();
