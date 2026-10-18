/**
 * Djazair Documentation — Code Tools (code-tools.js)
 * Robust copy-to-clipboard and "Run in Playground" functionality for code snippets.
 * Uses event delegation on document so it executes reliably under all browser timings.
 */
(function () {
  'use strict';

  // Helper for safe UTF-8 Base64 encoding compatible with Arabic, emojis & special chars
  function safeBase64Encode(str) {
    return encodeURIComponent(btoa(unescape(encodeURIComponent(str))));
  }

  // Global event delegation for clicks on .copy-btn and .run-code-btn
  document.addEventListener('click', function (e) {
    // ── 1. Copy code button ──────────────────────────────────────────────
    const copyBtn = e.target.closest('.copy-btn');
    if (copyBtn) {
      e.preventDefault();
      const codeWrapper = copyBtn.closest('.code-wrapper');
      if (!codeWrapper) return;

      const codeElement = codeWrapper.querySelector('pre code');
      if (!codeElement) return;

      const text = codeElement.innerText || codeElement.textContent || '';
      if (!text) return;

      navigator.clipboard.writeText(text).then(function () {
        const originalHtml = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Copied!</span>';
        copyBtn.classList.add('copied');

        setTimeout(function () {
          copyBtn.innerHTML = originalHtml;
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(function (err) {
        console.error('Failed to copy code: ', err);
      });
      return;
    }

    // ── 2. Run in Playground button ───────────────────────────────────────
    const runBtn = e.target.closest('.run-code-btn');
    if (runBtn) {
      e.preventDefault();
      const codeWrapper = runBtn.closest('.code-wrapper');
      if (!codeWrapper) return;

      const codeElement = codeWrapper.querySelector('pre code');
      if (!codeElement) return;

      const rawCode = (codeElement.innerText || codeElement.textContent || '').trim();
      if (!rawCode) return;

      // Visual feedback on the button
      const originalHtml = runBtn.innerHTML;
      runBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Opening…</span>';
      runBtn.disabled = true;

      const restoreBtn = function () {
        runBtn.innerHTML = originalHtml;
        runBtn.disabled = false;
      };

      const encoded = safeBase64Encode(rawCode);
      const rootPrefix = codeWrapper.dataset.rootPrefix || '';

      // Check if the playground element is on the current page (landing page index.html)
      const playgroundEl = document.getElementById('playground');
      if (playgroundEl && typeof window.setPlaygroundSource === 'function') {
        window.setPlaygroundSource(rawCode);
        playgroundEl.scrollIntoView({ behavior: 'smooth' });
        if (typeof window.runPlayground === 'function') {
          setTimeout(function () {
            window.runPlayground();
            restoreBtn();
          }, 350);
        } else {
          restoreBtn();
        }
      } else {
        // We are on a documentation page: open in new tab so user keeps their reading position
        const targetUrl = `${rootPrefix}index.html#src=${encoded}&autorun=1`;
        
        try {
          const newTab = window.open(targetUrl, '_blank');
          if (!newTab || newTab.closed || typeof newTab.closed === 'undefined') {
            // Popup blocked: fallback to same-window navigation
            window.location.href = targetUrl;
          } else {
            setTimeout(restoreBtn, 1200);
          }
        } catch (_) {
          window.location.href = targetUrl;
        }
      }
    }
  });
})();
