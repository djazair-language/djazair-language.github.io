/**
 * Djazair Documentation — Code Tools (code-tools.js)
 * Copy-to-clipboard and "Run in Playground" functionality for code snippets.
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Copy button functionality
  const copyButtons = document.querySelectorAll('.copy-btn');
  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const codeWrapper = button.closest('.code-wrapper');
      if (!codeWrapper) return;

      const codeElement = codeWrapper.querySelector('pre code');
      if (!codeElement) return;

      const text = codeElement.innerText || codeElement.textContent;

      try {
        await navigator.clipboard.writeText(text);
        const originalHtml = button.innerHTML;
        button.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
        button.classList.add('copied');

        setTimeout(() => {
          button.innerHTML = originalHtml;
          button.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Failed to copy code: ', err);
      }
    });
  });

  // 2. Run in Playground functionality
  const runButtons = document.querySelectorAll('.run-code-btn');
  runButtons.forEach(button => {
    button.addEventListener('click', () => {
      const codeWrapper = button.closest('.code-wrapper');
      if (!codeWrapper) return;

      const codeElement = codeWrapper.querySelector('pre code');
      if (!codeElement) return;

      const rawCode = (codeElement.innerText || codeElement.textContent || '').trim();
      if (!rawCode) return;

      // Safe UTF-8 Base64 encoding
      const encoded = btoa(unescape(encodeURIComponent(rawCode)));
      const rootPrefix = codeWrapper.dataset.rootPrefix || '';

      // Check if the playground element is on the current page (e.g. landing page index.html)
      const playgroundEl = document.getElementById('playground');
      if (playgroundEl && typeof window.setPlaygroundSource === 'function') {
        window.setPlaygroundSource(rawCode);
        playgroundEl.scrollIntoView({ behavior: 'smooth' });
        if (typeof window.runPlayground === 'function') {
          setTimeout(() => window.runPlayground(), 350);
        }
      } else {
        // Redirect to landing page playground with hash and autorun parameter
        const targetUrl = `${rootPrefix}index.html#src=${encoded}&autorun=1`;
        window.location.href = targetUrl;
      }
    });
  });
});
