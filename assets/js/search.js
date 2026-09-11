/**
 * Djazair Documentation — Instant Search (search.js)
 * Fast client-side fuzzy search with modal interface, keyboard navigation (Ctrl+K).
 */
(function () {
  let searchIndex = [];
  let selectedIndex = -1;
  let visibleResults = [];

  function initSearch() {
    searchIndex = window.DJAZAIR_SEARCH_INDEX || [];
    const searchModal = document.getElementById('search-modal');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchTriggers = document.querySelectorAll('.search-btn');

    if (!searchModal || !searchInput || !searchResults) return;

    function openModal() {
      searchModal.classList.add('open');
      searchInput.value = '';
      renderResults('');
      setTimeout(() => searchInput.focus(), 50);
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      searchModal.classList.remove('open');
      document.body.style.overflow = '';
      selectedIndex = -1;
    }

    searchTriggers.forEach(btn => btn.addEventListener('click', openModal));

    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) closeModal();
    });

    // Keyboard Shortcuts (Ctrl+K / Cmd+K, Escape, Arrows)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        if (searchModal.classList.contains('open')) {
          closeModal();
        } else {
          openModal();
        }
      } else if (e.key === 'Escape' && searchModal.classList.contains('open')) {
        closeModal();
      }
    });

    searchInput.addEventListener('input', (e) => {
      renderResults(e.target.value.trim());
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (visibleResults.length > 0) {
          selectedIndex = (selectedIndex + 1) % visibleResults.length;
          updateSelectedHighlight();
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (visibleResults.length > 0) {
          selectedIndex = (selectedIndex - 1 + visibleResults.length) % visibleResults.length;
          updateSelectedHighlight();
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < visibleResults.length) {
          window.location.href = visibleResults[selectedIndex].path;
          closeModal();
        }
      }
    });

    function updateSelectedHighlight() {
      const items = searchResults.querySelectorAll('.search-result-item');
      items.forEach((item, idx) => {
        if (idx === selectedIndex) {
          item.classList.add('selected');
          item.scrollIntoView({ block: 'nearest' });
        } else {
          item.classList.remove('selected');
        }
      });
    }

    function renderResults(query) {
      selectedIndex = -1;
      if (!query) {
        searchResults.innerHTML = '<div class="search-empty">Type keywords to search functions, modules, and guides...</div>';
        visibleResults = [];
        return;
      }

      const q = query.toLowerCase();
      const terms = q.split(/\s+/).filter(Boolean);

      const matched = searchIndex.filter(item => {
        const fullText = `${item.title} ${item.category} ${item.desc} ${item.keywords || ''}`.toLowerCase();
        return terms.every(t => fullText.includes(t));
      }).slice(0, 10);

      visibleResults = matched;

      if (matched.length === 0) {
        searchResults.innerHTML = `<div class="search-empty">No results found for "<strong>${escapeHtml(query)}</strong>"</div>`;
        return;
      }

      selectedIndex = 0;
      searchResults.innerHTML = matched.map((item, idx) => `
        <a href="${item.path}" class="search-result-item ${idx === 0 ? 'selected' : ''}">
          <div class="search-result-title">
            <span>${highlightMatch(item.title, terms)}</span>
            <span class="search-result-category">${escapeHtml(item.category)}</span>
          </div>
          <div class="search-result-desc">${highlightMatch(item.desc, terms)}</div>
        </a>
      `).join('');
    }

    function highlightMatch(text, terms) {
      let escaped = escapeHtml(text);
      terms.forEach(term => {
        if (!term) return;
        const re = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        escaped = escaped.replace(re, '<mark style="background:var(--color-primary-light); color:var(--color-primary-dark); padding:0 2px; border-radius:2px;">$1</mark>');
      });
      return escaped;
    }

    function escapeHtml(str) {
      if (!str) return '';
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  }

  document.addEventListener('DOMContentLoaded', initSearch);
})();
