/**
 * Djazair Documentation — Navigation & ScrollSpy (navigation.js)
 * Controls mobile sidebar drawer, scroll-spy table of contents, and active link states.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Mobile drawer controls
  const mobileToggle = document.getElementById('mobile-toggle');
  const sidebar = document.getElementById('docs-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (backdrop) backdrop.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('show');
    document.body.style.overflow = '';
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      if (sidebar && sidebar.classList.contains('open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }

  // Close sidebar on link click (mobile)
  if (sidebar) {
    sidebar.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 900) {
          closeSidebar();
        }
      });
    });
  }

  // ScrollSpy for On-This-Page Table of Contents
  const tocLinks = document.querySelectorAll('.docs-toc .toc-link');
  if (tocLinks.length > 0) {
    const headings = [];
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const id = href.slice(1);
        const target = document.getElementById(id);
        if (target) {
          headings.push({ el: target, link: link });
        }
      }
    });

    if (headings.length > 0) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            tocLinks.forEach(l => l.classList.remove('active'));
            const match = headings.find(h => h.el === entry.target);
            if (match) {
              match.link.classList.add('active');
            }
          }
        });
      }, {
        rootMargin: '-80px 0px -70% 0px',
        threshold: 0
      });

      headings.forEach(h => observer.observe(h.el));
    }
  }
});
