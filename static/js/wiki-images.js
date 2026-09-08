/**
 * Loads real photographs from Wikipedia's public MediaWiki API (no key
 * required, CORS-enabled via origin=*) for any element carrying a
 * data-wiki-topic attribute. Falls back to a themed gradient placeholder
 * if the fetch fails (offline, blocked, or topic not found) so the site
 * never shows a broken image.
 *
 * Admin-uploaded images (via the Media Library) are supported too: set
 * data-wiki-topic to "media:filename.jpg" and it resolves directly to
 * /static/uploads/filename.jpg with no external API call.
 *
 * Usage:
 *   <img data-wiki-topic="Taj_Mahal" data-wiki-size="800" alt="...">
 *   <div class="wiki-bg" data-wiki-topic="media:my-photo-a1b2c3d4.jpg"></div>
 */
(function () {
  const cache = new Map();

  async function fetchThumb(topic, size) {
    if (cache.has(topic)) return cache.get(topic);
    const url =
      "https://en.wikipedia.org/w/api.php?action=query&titles=" +
      encodeURIComponent(topic) +
      "&prop=pageimages&pithumbsize=" + size +
      "&format=json&origin=*";
    const promise = fetch(url)
      .then((r) => r.json())
      .then((data) => {
        const pages = data.query && data.query.pages;
        if (!pages) return null;
        const page = Object.values(pages)[0];
        return (page && page.thumbnail && page.thumbnail.source) || null;
      })
      .catch(() => null);
    cache.set(topic, promise);
    return promise;
  }

  async function hydrate(el) {
    const topic = el.getAttribute("data-wiki-topic");
    if (!topic) return;

    // Admin-uploaded image via the Media Library: "media:filename.jpg"
    if (topic.startsWith("media:")) {
      const filename = topic.slice("media:".length);
      const src = "/static/uploads/" + filename;
      if (el.tagName === "IMG") {
        el.src = src;
      } else {
        el.style.backgroundImage = `linear-gradient(180deg, rgba(11,26,58,0.15), rgba(11,26,58,0.75)), url('${src}')`;
      }
      el.classList.add("wiki-loaded");
      return;
    }

    const size = el.getAttribute("data-wiki-size") || "800";
    el.classList.add("wiki-loading");
    const src = await fetchThumb(topic, size);
    el.classList.remove("wiki-loading");
    if (!src) {
      el.classList.add("wiki-fallback");
      return;
    }
    if (el.tagName === "IMG") {
      el.src = src;
      el.classList.add("wiki-loaded");
    } else {
      el.style.backgroundImage = `linear-gradient(180deg, rgba(11,26,58,0.15), rgba(11,26,58,0.75)), url('${src}')`;
      el.classList.add("wiki-loaded");
    }
  }

  function init() {
    document.querySelectorAll("[data-wiki-topic]").forEach((el) => {
      // Stagger slightly to avoid a burst of simultaneous requests
      hydrate(el);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Expose for dynamically-inserted content (e.g. after search/filter)
  window.HeritageWikiImages = { hydrate, init };
})();
