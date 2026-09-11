/**
 * Djazair Documentation — Code Tools (code-tools.js)
 * Copy-to-clipboard functionality with responsive feedback for all code snippets.
 */
document.addEventListener('DOMContentLoaded', () => {
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
});
