document.addEventListener("DOMContentLoaded", () => {
  /* ---------------- mobile nav ---------------- */
  const navToggle = document.getElementById("nav-toggle");
  const navLinks = document.getElementById("nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => navLinks.classList.toggle("open"));
  }

  /* ---------------- accessibility toolbar ---------------- */
  const root = document.documentElement;
  let fontStep = parseInt(localStorage.getItem("heritage_font_step") || "0", 10);
  const applyFont = () => { root.style.fontSize = (100 + fontStep * 8) + "%"; };
  applyFont();

  const incBtn = document.getElementById("font-inc");
  const decBtn = document.getElementById("font-dec");
  const resetBtn = document.getElementById("font-reset");
  if (incBtn) incBtn.addEventListener("click", () => { fontStep = Math.min(fontStep + 1, 3); localStorage.setItem("heritage_font_step", fontStep); applyFont(); });
  if (decBtn) decBtn.addEventListener("click", () => { fontStep = Math.max(fontStep - 1, -2); localStorage.setItem("heritage_font_step", fontStep); applyFont(); });
  if (resetBtn) resetBtn.addEventListener("click", () => { fontStep = 0; localStorage.setItem("heritage_font_step", fontStep); applyFont(); });

  const contrastBtn = document.getElementById("contrast-toggle");
  if (localStorage.getItem("heritage_high_contrast") === "1") document.body.classList.add("high-contrast");
  if (contrastBtn) {
    contrastBtn.addEventListener("click", () => {
      document.body.classList.toggle("high-contrast");
      localStorage.setItem("heritage_high_contrast", document.body.classList.contains("high-contrast") ? "1" : "0");
    });
  }

  /* ---------------- scroll reveal ---------------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add("in-view"); io.unobserve(entry.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  /* ---------------- animated counters ---------------- */
  document.querySelectorAll("[data-counter]").forEach((el) => {
    const target = parseFloat(el.getAttribute("data-counter"));
    if (isNaN(target)) return;
    let current = 0;
    const step = target / 50;
    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        counterObserver.unobserve(el);
        const tick = () => {
          current += step;
          if (current >= target) { el.textContent = Math.round(target).toLocaleString(); return; }
          el.textContent = Math.round(current).toLocaleString();
          requestAnimationFrame(tick);
        };
        tick();
      });
    });
    counterObserver.observe(el);
  });

  /* ---------------- flash auto-dismiss ---------------- */
  document.querySelectorAll(".flash-msg").forEach((el) => {
    setTimeout(() => { el.style.opacity = "0"; setTimeout(() => el.remove(), 400); }, 6000);
  });

  /* ---------------- ticket price calculator ---------------- */
  const priceForm = document.getElementById("ticket-form");
  if (priceForm) {
    const rates = {
      indian: parseFloat(priceForm.dataset.priceIndian || 0),
      foreign: parseFloat(priceForm.dataset.priceForeign || 0),
      student: parseFloat(priceForm.dataset.priceStudent || 0),
      child: parseFloat(priceForm.dataset.priceChild || 0),
    };
    const totalEl = document.getElementById("ticket-total");
    const updateTotal = () => {
      let total = 0, count = 0;
      ["indian", "foreign", "student", "child"].forEach((k) => {
        const input = document.getElementById("qty_" + k);
        const n = Math.max(0, parseInt(input.value || "0", 10));
        total += n * rates[k];
        count += n;
      });
      totalEl.textContent = "₹" + total.toLocaleString();
      document.getElementById("ticket-count").textContent = count;
    };
    priceForm.querySelectorAll("input[type=number]").forEach((inp) => inp.addEventListener("input", updateTotal));
    updateTotal();
  }

  /* ---------------- chatbot widget ---------------- */
  initChatWidget();
});

function initChatWidget() {
  const toggle = document.getElementById("chat-toggle");
  const panel = document.getElementById("chat-panel");
  const closeBtn = document.getElementById("chat-close");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const messages = document.getElementById("chat-messages");
  if (!toggle || !panel || !form) return;

  const openPanel = () => {
    panel.classList.add("open");
    if (!messages.dataset.greeted) {
      addMessage("bot", "Namaste! 🙏 I'm Heritage AI. Ask me about gallery timings, ticket prices, history, or live visitor numbers for any era!");
      messages.dataset.greeted = "1";
    }
    input.focus();
  };
  toggle.addEventListener("click", () => { panel.classList.contains("open") ? panel.classList.remove("open") : openPanel(); });
  closeBtn && closeBtn.addEventListener("click", () => panel.classList.remove("open"));

  function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = "chat-msg " + role;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }
  function addTyping() {
    const div = document.createElement("div");
    div.className = "chat-msg bot flex gap-1 items-center";
    div.id = "typing-indicator";
    div.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }
  function removeTyping() { const el = document.getElementById("typing-indicator"); if (el) el.remove(); }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    addMessage("user", text);
    input.value = "";
    addTyping();
    try {
      const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: text }) });
      const data = await res.json();
      removeTyping();
      addMessage("bot", data.reply || "Sorry, I couldn't process that right now.");
    } catch (err) {
      removeTyping();
      addMessage("bot", "I'm having trouble connecting right now. Please try again shortly.");
    }
  });

  document.querySelectorAll("[data-quick-q]").forEach((btn) => {
    btn.addEventListener("click", () => {
      input.value = btn.getAttribute("data-quick-q");
      form.dispatchEvent(new Event("submit"));
      openPanel();
    });
  });
}
