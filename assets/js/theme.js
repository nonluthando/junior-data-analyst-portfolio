// Light/dark toggle. Preference is stored locally and falls back to the OS setting.
(() => {
  const root = document.documentElement;
  const read = () => { try { return localStorage.getItem("theme"); } catch { return null; } };
  const write = (v) => { try { localStorage.setItem("theme", v); } catch { /* storage unavailable */ } };

  const preferred = read() || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  root.dataset.theme = preferred;

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      const paint = () => { btn.textContent = root.dataset.theme === "dark" ? "☀️" : "🌙"; };
      paint();
      btn.addEventListener("click", () => {
        root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
        write(root.dataset.theme);
        paint();
      });
    });

    // "/" jumps to the table of contents, like a Notion slash command.
    document.addEventListener("keydown", (e) => {
      if (e.key !== "/" || /input|textarea/i.test(e.target.tagName)) return;
      const toc = document.getElementById("toc");
      if (toc) { e.preventDefault(); toc.scrollIntoView({ behavior: "smooth" }); toc.querySelector("a")?.focus(); }
    });
  });
})();
