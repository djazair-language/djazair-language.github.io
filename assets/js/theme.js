/**
 * Djazair Documentation — Permanent Dark Mode
 * Locks the documentation theme to dark mode permanently.
 */
(function () {
  document.documentElement.setAttribute('data-theme', 'dark');
  try {
    localStorage.setItem('dz-theme', 'dark');
  } catch (_) {}
})();
