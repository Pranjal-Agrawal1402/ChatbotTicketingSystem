document.addEventListener("DOMContentLoaded", () => {
  /* ---------------- occupancy chart ---------------- */
  const chartEl = document.getElementById("occupancyChart");
  if (chartEl && window.Chart) {
    const labels = JSON.parse(chartEl.dataset.labels || "[]");
    const occ = JSON.parse(chartEl.dataset.occ || "[]");
    const cap = JSON.parse(chartEl.dataset.cap || "[]");
    new Chart(chartEl, {
      type: "bar",
      data: {
        labels,
        datasets: [
          { label: "Current Visitors", data: occ, backgroundColor: "rgba(10,38,71,0.85)", borderRadius: 6 },
          { label: "Max Capacity", data: cap, backgroundColor: "rgba(184,137,43,0.35)", borderRadius: 6 },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: "#1c1c24" } } },
        scales: {
          x: { ticks: { color: "#55586b", maxRotation: 60, minRotation: 40 }, grid: { display: false } },
          y: { ticks: { color: "#55586b" }, grid: { color: "rgba(10,38,71,0.06)" } },
        },
      },
    });
  }

  /* ---------------- quick occupancy +/- ---------------- */
  document.querySelectorAll("[data-occ-delta]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-gallery-id");
      const delta = parseInt(btn.getAttribute("data-occ-delta"), 10);
      const res = await fetch(`/admin/galleries/${id}/occupancy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ delta }),
      });
      if (res.ok) {
        const data = await res.json();
        const label = document.querySelector(`[data-occ-label="${id}"]`);
        if (label) label.textContent = `${data.current_occupancy} / ${data.max_occupancy}`;
        const bar = document.querySelector(`[data-occ-bar="${id}"]`);
        if (bar) bar.style.width = data.occupancy_percent + "%";
      }
    });
  });

  /* ---------------- delete / destructive action confirm ---------------- */
  document.querySelectorAll("[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!confirm(form.getAttribute("data-confirm"))) e.preventDefault();
    });
  });
});
