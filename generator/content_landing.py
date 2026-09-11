"""
Content generator for the modern landing page (index.html).
"""
from .highlighter import process_code_blocks

def render_landing_page() -> str:
    hero_code = '''# Experience the elegance of Djazair
use http
use json
use math

# Class with inheritance and custom methods
class Rocket
    init(name, fuel = 100)
        self.name = name
        self.fuel = fuel
    end

    launch()
        print("🚀 ${self.name} launched with ${self.fuel}% fuel!")
    end
end

let apollo = new Rocket("Djazair-1")
apollo.launch() # => 🚀 Djazair-1 launched with 100% fuel!

# First-class UTF-8 & Arabic identifiers
let 🇩🇿_البلد = "الجزائر"
print("مرحباً من ${🇩🇿_البلد}!")

# Modern higher-order array methods
let numbers = [1, 2, 3, 4, 5]
let doubledEvens = numbers
    .filter(fn(n) => n % 2 == 0)
    .map(fn(n) => n * 2)

print("Doubled evens: ${doubledEvens}") # => [4, 8]
'''

    highlighted_hero_code = process_code_blocks(f'<pre><code class="language-dz">{hero_code}</code></pre>')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Djazair Programming Language — Fast, Expressive & Modern</title>
  <meta name="description" content="A modern, expressive scripting language inspired by the soul of North Africa. Fast C bytecode VM, actor concurrency, Arabic UTF-8, and 20 built-in standard modules.">
  <link rel="icon" href="assets/images/logo.svg" type="image/svg+xml">
  
  <!-- FontAwesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Stylesheets -->
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/syntax.css">
  
  <script src="assets/js/theme.js"></script>
</head>
<body>

  <!-- Top Navbar -->
  <header class="site-header">
    <div class="header-left">
      <a href="index.html" class="brand-link">
        <img src="assets/images/logo.svg" alt="Djazair Logo" class="brand-logo">
        <span>Djazair</span>
        <span class="version-tag">v1.1.0</span>
      </a>
    </div>

    <nav class="header-nav">
      <a href="docs/getting-started/index.html" class="nav-link">Documentation</a>
      <a href="docs/standard-library/index.html" class="nav-link">Standard Library</a>
      <a href="docs/dpm/index.html" class="nav-link">DPM</a>
      <a href="docs/cookbook/rest-api.html" class="nav-link">Cookbook</a>
      <a href="docs/reference/cheat-sheet.html" class="nav-link">Cheat Sheet</a>
    </nav>

    <div class="header-right">
      <button class="search-btn" aria-label="Search documentation">
        <i class="fa-solid fa-magnifying-glass"></i>
        <span>Search docs...</span>
        <span class="search-shortcut">Ctrl K</span>
      </button>
      <button class="theme-btn" id="theme-toggle" aria-label="Toggle theme">
        <i class="fa-solid fa-moon"></i>
      </button>
      <a href="https://github.com/djazair-language/djazair" target="_blank" rel="noopener noreferrer" class="icon-btn" aria-label="GitHub repository">
        <i class="fa-brands fa-github"></i>
      </a>
    </div>
  </header>

  <!-- Hero Section -->
  <main>
    <section class="hero-section">
      <div class="hero-badge">
        <i class="fa-solid fa-sparkles"></i> Djazair v1.1.0 is now available
      </div>
      <h1 class="hero-title">
        The Expressive Scripting Language<br>
        <span class="hero-gradient-text">Inspired by North Africa</span>
      </h1>
      <p class="hero-subtitle">
        A lightweight, embeddable language written in ANSI C. Featuring a fast bytecode VM, automatic memory management, first-class functions, actor concurrency, deep Unicode UTF-8 support, and 20 built-in standard modules.
      </p>

      <div class="hero-actions">
        <a href="docs/getting-started/index.html" class="btn btn-primary">
          <i class="fa-solid fa-book"></i> Read Documentation
        </a>
        <a href="docs/getting-started/installation.html" class="btn btn-secondary">
          <i class="fa-solid fa-download"></i> Install Djazair
        </a>
        <a href="https://github.com/djazair-language/djazair" target="_blank" class="btn btn-secondary">
          <i class="fa-brands fa-github"></i> GitHub (Source)
        </a>
      </div>

      <!-- Hero Code Showcase -->
      <div class="showcase-container">
        {highlighted_hero_code}
      </div>
    </section>

    <!-- Core Features Grid -->
    <section class="features-section">
      <div class="section-header">
        <h2 class="section-title">Engineered for Elegance and Speed</h2>
        <p class="section-desc">Everything you need to write clean, maintainable, high-performance software without unnecessary complexity.</p>
      </div>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-bolt-lightning"></i></div>
          <h3 class="feature-title">Fast C Bytecode VM</h3>
          <p class="feature-desc">Single-pass compilation straight into bytecode, executed by an efficient stack-based virtual machine with automatic mark-and-sweep garbage collection.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-earth-africa"></i></div>
          <h3 class="feature-title">100% Deep Unicode & Arabic</h3>
          <p class="feature-desc">Arabic identifiers, multi-byte emojis, and accents treated as first-class code points. Strings, loops, and index operations never break character boundaries.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-cubes-stacked"></i></div>
          <h3 class="feature-title">20 Standard Library Modules</h3>
          <p class="feature-desc">Built-in HTTP client and server, TCP/UDP sockets, JSON, SHA-256/AES crypto, regex, datetime, path, dir globbing, process control, and collections.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-arrows-split-up-and-left"></i></div>
          <h3 class="feature-title">Actor-Model Concurrency</h3>
          <p class="feature-desc">True parallelism across CPU cores. Workers execute in isolated VM heaps, exchanging messages without data races, mutex locking, or memory corruption.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-microchip"></i></div>
          <h3 class="feature-title">Easily Embeddable</h3>
          <p class="feature-desc">Include <code>djazair.h</code> to embed the engine inside any C/C++ host application in under 20 lines of code. Zero external runtime dependencies.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon"><i class="fa-solid fa-code"></i></div>
          <h3 class="feature-title">Modern Functions & Closures</h3>
          <p class="feature-desc">First-class functions, lexical closures, arrow syntax (=>), default arguments, and functional collection pipelines (map, filter, reduce).</p>
        </div>
      </div>
    </section>

    <!-- Standard Library Quick Browse -->
    <section class="features-section" style="padding-top:1rem;">
      <div class="section-header">
        <h2 class="section-title">Explore the Standard Library</h2>
        <p class="section-desc">Explore 20 built-in modules ready out of the box with zero external packages needed.</p>
      </div>

      <div class="stdlib-grid">
        <a href="docs/standard-library/http.html" class="stdlib-card">
          <div class="stdlib-name">http</div>
          <div class="stdlib-desc">Client & multithreaded server with routing, streaming, and keep-alive.</div>
        </a>
        <a href="docs/standard-library/net.html" class="stdlib-card">
          <div class="stdlib-name">net</div>
          <div class="stdlib-desc">TCP/UDP socket servers, URL parsing, URLSearchParams, DNS, TLS.</div>
        </a>
        <a href="docs/standard-library/json.html" class="stdlib-card">
          <div class="stdlib-name">json</div>
          <div class="stdlib-desc">Fast JSON encoding and decoding with pretty formatting.</div>
        </a>
        <a href="docs/standard-library/crypto.html" class="stdlib-card">
          <div class="stdlib-name">crypto</div>
          <div class="stdlib-desc">SHA-256 digests, Base64 encoding/decoding, and AES encryption.</div>
        </a>
        <a href="docs/standard-library/file.html" class="stdlib-card">
          <div class="stdlib-name">file</div>
          <div class="stdlib-desc">Read/write text & binary files, permissions chmod, file stats.</div>
        </a>
        <a href="docs/standard-library/dir.html" class="stdlib-card">
          <div class="stdlib-name">dir</div>
          <div class="stdlib-desc">Create folders, list directories, and recursive glob matching (**).</div>
        </a>
        <a href="docs/standard-library/thread.html" class="stdlib-card">
          <div class="stdlib-name">thread</div>
          <div class="stdlib-desc">Actor concurrency, worker threads, and JSON message passing.</div>
        </a>
        <a href="docs/standard-library/regex.html" class="stdlib-card">
          <div class="stdlib-name">regex</div>
          <div class="stdlib-desc">Regular expressions, compile, search, replace, and capture groups.</div>
        </a>
      </div>
      
      <div style="text-align:center; margin-top:2.5rem;">
        <a href="docs/standard-library/index.html" class="btn btn-secondary">View All 20 Modules &rarr;</a>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-content">
      <div>
        <strong style="color:var(--text-primary); font-size:1.1rem;">Djazair Programming Language</strong>
        <p style="margin-top:0.4rem; color:var(--text-muted);">Released under the open-source MIT License. Designed & Developed by Harizi Riyadh.</p>
      </div>
      <div class="footer-links">
        <a href="docs/getting-started/index.html">Docs</a>
        <a href="docs/standard-library/index.html">Stdlib</a>
        <a href="docs/cookbook/rest-api.html">Cookbook</a>
        <a href="https://github.com/djazair-language/djazair" target="_blank">GitHub</a>
      </div>
    </div>
  </footer>

  <!-- Search Modal -->
  <div class="search-modal-backdrop" id="search-modal">
    <div class="search-modal">
      <div class="search-input-wrap">
        <i class="fa-solid fa-magnifying-glass"></i>
        <input type="text" id="search-input" class="search-input" placeholder="Search documentation, functions, keywords..." autocomplete="off">
      </div>
      <div class="search-results-list" id="search-results"></div>
      <div class="search-footer">
        <span>Navigate with <kbd>↑</kbd> <kbd>↓</kbd></span>
        <span>Open with <kbd>Enter</kbd></span>
        <span>Close with <kbd>Esc</kbd></span>
      </div>
    </div>
  </div>

  <!-- Scripts -->
  <script src="assets/js/search-index.js"></script>
  <script src="assets/js/search.js"></script>
  <script src="assets/js/code-tools.js"></script>
</body>
</html>'''
