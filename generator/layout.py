"""
HTML Page Layout & Component Generators for Djazair Documentation.
"""
import re
import html
from .highlighter import process_code_blocks

# Complete Page & Category Structure
SITE_STRUCTURE = [
    {
        "category": "Getting Started",
        "icon": "fa-rocket",
        "pages": [
            {
                "id": "intro",
                "title": "Introduction",
                "path": "docs/getting-started/index.html",
                "desc": "Overview of Djazair, architectural design, C engine, and modern features.",
                "keywords": "intro philosophy architecture features bytecode vm c engine"
            },
            {
                "id": "install",
                "title": "Installation",
                "path": "docs/getting-started/installation.html",
                "desc": "Build and install Djazair on Windows, Linux, and macOS with make or PowerShell.",
                "keywords": "install build windows linux mac make gcc clang mingw libregex"
            },
            {
                "id": "first-program",
                "title": "First Program",
                "path": "docs/getting-started/first-program.html",
                "desc": "Write your first script, string output, and interactive experimentation.",
                "keywords": "hello world print first script interactive quickstart"
            },
            {
                "id": "cli",
                "title": "Command-Line (CLI)",
                "path": "docs/getting-started/cli.html",
                "desc": "CLI flags, inline code evaluation, passing script arguments, and debug options.",
                "keywords": "cli flags arguments inline eval -c -d -v args"
            }
        ]
    },
    {
        "category": "Language Guide",
        "icon": "fa-book-open",
        "pages": [
            {
                "id": "variables",
                "title": "Variables & Scope",
                "path": "docs/language-guide/variables.html",
                "desc": "Variable declaration with let, lexical block scoping, and identifier rules.",
                "keywords": "variables let scoping block scope mutation identifiers"
            },
            {
                "id": "data-types",
                "title": "Data Types & Casting",
                "path": "docs/language-guide/data-types.html",
                "desc": "Primitive and compound types, type casting with int, float, str, bool, num.",
                "keywords": "types int float string bool null array map function range casting"
            },
            {
                "id": "operators",
                "title": "Operators",
                "path": "docs/language-guide/operators.html",
                "desc": "Arithmetic, logical, bitwise, assignment, deep equality, and identity operators.",
                "keywords": "operators arithmetic bitwise logic comparison equality is in"
            },
            {
                "id": "strings",
                "title": "Strings & Methods",
                "path": "docs/language-guide/strings.html",
                "desc": "String interpolation, multiline backticks, and 30+ string methods.",
                "keywords": "strings interpolation backticks slice split replace join upper lower"
            },
            {
                "id": "unicode",
                "title": "Unicode & UTF-8",
                "path": "docs/language-guide/unicode.html",
                "desc": "First-class UTF-8, Arabic identifiers, emojis, and code-point accurate operations.",
                "keywords": "unicode utf8 arabic identifiers emoji charCodeAt slicing"
            },
            {
                "id": "arrays",
                "title": "Arrays & Methods",
                "path": "docs/language-guide/arrays.html",
                "desc": "Dynamic lists, higher-order functions: map, filter, reduce, find, sort, unique.",
                "keywords": "arrays list append pop map filter reduce find every some sort"
            },
            {
                "id": "maps",
                "title": "Maps & Hashes",
                "path": "docs/language-guide/maps.html",
                "desc": "Hash maps, key-value storage, iteration, update, setDefault, and keys/values.",
                "keywords": "map hash dictionary keys values items has update setDefault"
            },
            {
                "id": "control-flow",
                "title": "Control Flow",
                "path": "docs/language-guide/control-flow.html",
                "desc": "Branching with if-elif-else, ternary expressions, and pattern matching match-case.",
                "keywords": "if elif else ternary match case default pattern matching"
            },
            {
                "id": "loops",
                "title": "Loops & Iteration",
                "path": "docs/language-guide/loops.html",
                "desc": "while, do-while, for-in on arrays, maps (key, value), ranges, and strings.",
                "keywords": "loops while do-while for in range iterators break continue"
            },
            {
                "id": "functions",
                "title": "Functions & Closures",
                "path": "docs/language-guide/functions.html",
                "desc": "First-class functions, arrow syntax =>, default arguments, rest parameters, closures.",
                "keywords": "functions fn arrow lambda closures default args rest params"
            },
            {
                "id": "oop",
                "title": "Classes & OOP",
                "path": "docs/language-guide/oop.html",
                "desc": "Object-oriented programming, class, init, self, inheritance with is, super, instanceof.",
                "keywords": "oop class init self super inheritance instanceof polymorphism new"
            },
            {
                "id": "error-handling",
                "title": "Error Handling",
                "path": "docs/language-guide/error-handling.html",
                "desc": "Exception management with try, catch, finally, throw, and nested error propagation.",
                "keywords": "exceptions try catch finally throw error handling"
            },
            {
                "id": "modules",
                "title": "Modules & Imports",
                "path": "docs/language-guide/modules.html",
                "desc": "Code organization with import for files, use for stdlib, aliases, and wildcard *.",
                "keywords": "modules import use as wildcard alias exports packages"
            }
        ]
    },
    {
        "category": "Package Manager (DPM)",
        "icon": "fa-box-open",
        "pages": [
            {
                "id": "dpm",
                "title": "DPM Guide & Reference",
                "path": "docs/dpm/index.html",
                "desc": "Official package manager, CLI reference, SemVer dependency engine, manifest specification, and package authoring.",
                "keywords": "dpm package manager install init update remove pack list info semver pure hybrid manifest dpm.json"
            }
        ]
    },
    {
        "category": "Standard Library",
        "icon": "fa-cubes",
        "pages": [
            {
                "id": "stdlib-overview",
                "title": "Overview",
                "path": "docs/standard-library/index.html",
                "desc": "Directory of all 20 built-in standard modules in Djazair.",
                "keywords": "standard library modules stdlib built-in overview"
            },
            {
                "id": "mod-assert",
                "title": "assert",
                "path": "docs/standard-library/assert.html",
                "desc": "Unit testing assertions: isTrue, equal, notEqual, approxEqual, isNull, throws.",
                "keywords": "assert testing test isTrue equal approxEqual throws"
            },
            {
                "id": "mod-bytes",
                "title": "bytes",
                "path": "docs/standard-library/bytes.html",
                "desc": "Binary byte arrays, buffer allocation, hex encoding/decoding, transformations.",
                "keywords": "bytes binary buffer hex alloc fromString toString"
            },
            {
                "id": "mod-collections",
                "title": "collections",
                "path": "docs/standard-library/collections.html",
                "desc": "Stack, Queue, Deque, Set (union, diff, intersect), LinkedList, PriorityQueue.",
                "keywords": "collections stack queue deque set linkedlist priorityqueue"
            },
            {
                "id": "mod-crypto",
                "title": "crypto",
                "path": "docs/standard-library/crypto.html",
                "desc": "SHA-256 cryptographic hashing, Base64 encode/decode, AES-CBC encryption.",
                "keywords": "crypto sha256 base64 aes encryption decryption hash"
            },
            {
                "id": "mod-datetime",
                "title": "datetime",
                "path": "docs/standard-library/datetime.html",
                "desc": "Current time, timestamps, date arithmetic, custom formatting, and Date class.",
                "keywords": "datetime date time timestamp format parse addDays diff"
            },
            {
                "id": "mod-dir",
                "title": "dir",
                "path": "docs/standard-library/dir.html",
                "desc": "Directory listing, recursive traversal, creation, and glob pattern matching (**).",
                "keywords": "dir directory folder glob traverse create list"
            },
            {
                "id": "mod-env",
                "title": "env",
                "path": "docs/standard-library/env.html",
                "desc": "Reading, setting, and querying environment variables at runtime.",
                "keywords": "env environment variables get set has"
            },
            {
                "id": "mod-file",
                "title": "file",
                "path": "docs/standard-library/file.html",
                "desc": "Reading, writing, appending text and binary, file stats, chmod, FileHandle, symlinks.",
                "keywords": "file io read write append stat chmod symlink lines"
            },
            {
                "id": "mod-http",
                "title": "http",
                "path": "docs/standard-library/http.html",
                "desc": "Full HTTP client (get, post, put, etc.) and multithreaded HTTP Server with streaming.",
                "keywords": "http client server request response get post headers keepalive"
            },
            {
                "id": "mod-json",
                "title": "json",
                "path": "docs/standard-library/json.html",
                "desc": "JSON serialization and deserialization with pretty printing and safe error handling.",
                "keywords": "json encode decode parse stringify serializer"
            },
            {
                "id": "mod-lang",
                "title": "lang",
                "path": "docs/standard-library/lang.html",
                "desc": "Runtime engine control, manual GC cycle triggering, and heap memory statistics.",
                "keywords": "lang runtime gc garbage collection memory stats"
            },
            {
                "id": "mod-math",
                "title": "math",
                "path": "docs/standard-library/math.html",
                "desc": "Mathematical constants, trigonometry, logs, power, rounding, gcd, lcm, factorial.",
                "keywords": "math sqrt sin cos tan log pow gcd lcm factorial clamp"
            },
            {
                "id": "mod-net",
                "title": "net",
                "path": "docs/standard-library/net.html",
                "desc": "TCP & UDP sockets, URL parsing, URLSearchParams, DNS lookups, TLS client.",
                "keywords": "net network tcp udp socket client server url dns tls"
            },
            {
                "id": "mod-os",
                "title": "os",
                "path": "docs/standard-library/os.html",
                "desc": "OS detection, CPU count, memory info, user and temp directory resolution, which.",
                "keywords": "os platform cpu memory username tempdir which"
            },
            {
                "id": "mod-path",
                "title": "path",
                "path": "docs/standard-library/path.html",
                "desc": "Cross-platform path manipulation, join, resolve, dirname, basename, extname.",
                "keywords": "path join resolve dirname basename extname normalize"
            },
            {
                "id": "mod-process",
                "title": "process",
                "path": "docs/standard-library/process.html",
                "desc": "Process control, PID, cwd, synchronous exec, and asynchronous spawn with pipes.",
                "keywords": "process exec spawn pid cwd args sleep wait"
            },
            {
                "id": "mod-random",
                "title": "random",
                "path": "docs/standard-library/random.html",
                "desc": "Pseudorandom number generator, float, int range, string, choice, shuffle, seed.",
                "keywords": "random rand int float choice shuffle seed bytes"
            },
            {
                "id": "mod-regex",
                "title": "regex",
                "path": "docs/standard-library/regex.html",
                "desc": "Regular expressions: compile, search, fullMatch, findAll, sub, and group captures.",
                "keywords": "regex pattern match search findall replace sub split"
            },
            {
                "id": "mod-thread",
                "title": "thread",
                "path": "docs/standard-library/thread.html",
                "desc": "Actor concurrency model, worker spawning, message passing, JSON messaging, pools.",
                "keywords": "thread actor concurrency spawn worker send receive pool"
            },
            {
                "id": "mod-uuid",
                "title": "uuid",
                "path": "docs/standard-library/uuid.html",
                "desc": "Universally Unique Identifier (UUID v4) generation and RFC-4122 validation.",
                "keywords": "uuid v4 unique identifier guid validate"
            }
        ]
    },
    {
        "category": "C / C++ Embedding",
        "icon": "fa-microchip",
        "pages": [
            {
                "id": "embedding-overview",
                "title": "Embedding Overview",
                "path": "docs/embedding/index.html",
                "desc": "Integrate Djazair into C and C++ applications using djazair.h.",
                "keywords": "embedding c cpp djazair.h api integrate link"
            },
            {
                "id": "vm-lifecycle",
                "title": "VM Lifecycle & Config",
                "path": "docs/embedding/vm-lifecycle.html",
                "desc": "DjazairVM creation, configuration callbacks, GC, and memory management.",
                "keywords": "vm lifecycle djazair_newVM callbacks writeFn errorFn memory"
            },
            {
                "id": "c-extensions",
                "title": "Writing C Extensions",
                "path": "docs/embedding/c-extensions.html",
                "desc": "Create native extensions using djazair_api.h and export them to Djazair.",
                "keywords": "c extensions djazair_api.h native functions dll so"
            }
        ]
    },
    {
        "category": "Cookbook & Practical",
        "icon": "fa-utensils",
        "pages": [
            {
                "id": "recipe-rest-api",
                "title": "Building a REST API",
                "path": "docs/cookbook/rest-api.html",
                "desc": "Step-by-step tutorial building a production-ready REST API with http and json.",
                "keywords": "rest api tutorial server http json routes backend"
            },
            {
                "id": "recipe-cli-tool",
                "title": "CLI Automation Tool",
                "path": "docs/cookbook/cli-tool.html",
                "desc": "Build a command-line file analyzer using path, file, and process modules.",
                "keywords": "cli tool automation flags arguments file processing"
            },
            {
                "id": "recipe-parallel-workers",
                "title": "Parallel Worker Pool",
                "path": "docs/cookbook/parallel-workers.html",
                "desc": "Distribute heavy tasks across CPU cores using actor threads and JSON messaging.",
                "keywords": "parallel workers actor threads background processing"
            }
        ]
    },
    {
        "category": "Reference",
        "icon": "fa-bookmark",
        "pages": [
            {
                "id": "ref-builtins",
                "title": "Built-in Functions",
                "path": "docs/reference/builtins.html",
                "desc": "Complete alphabetical reference of all 26+ built-in global functions.",
                "keywords": "builtins functions global print input type str int float range"
            },
            {
                "id": "ref-keywords",
                "title": "Keywords & Grammar",
                "path": "docs/reference/keywords.html",
                "desc": "Reserved keywords and formal grammar rules of the Djazair language.",
                "keywords": "keywords grammar syntax reserved words specification"
            },
            {
                "id": "ref-cheat-sheet",
                "title": "Cheat Sheet",
                "path": "docs/reference/cheat-sheet.html",
                "desc": "Quick-reference cheat sheet covering syntax, methods, and idioms.",
                "keywords": "cheat sheet reference quick syntax methods snippets"
            }
        ]
    }
]

# Flattened list of pages for navigation
ALL_PAGES = []
for cat in SITE_STRUCTURE:
    for p in cat["pages"]:
        ALL_PAGES.append({
            **p,
            "category": cat["category"]
        })

def get_root_prefix(file_path: str) -> str:
    """Compute relative prefix (e.g. '../../') based on file path."""
    depth = file_path.count('/')
    return '../' * depth if depth > 0 else ''

def extract_toc(article_html: str):
    """Extract h2 and h3 elements for table of contents."""
    pattern = r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h[23]>'
    items = []
    for match in re.finditer(pattern, article_html, re.DOTALL):
        level = int(match.group(1))
        anchor_id = match.group(2)
        raw_text = match.group(3)
        clean_text = re.sub(r'<[^>]+>', '', raw_text).strip()
        items.append({
            "level": level,
            "id": anchor_id,
            "text": clean_text
        })
    return items

def render_navbar(root_prefix: str, active_tab: str = "docs") -> str:
    return f'''<header class="site-header">
  <div class="header-left">
    <button class="mobile-toggle-btn" id="mobile-toggle" aria-label="Toggle navigation drawer">
      <i class="fa-solid fa-bars"></i>
    </button>
    <a href="{root_prefix}index.html" class="brand-link">
      <img src="{root_prefix}assets/images/logo.svg" alt="Djazair Logo" class="brand-logo">
      <span>Djazair</span>
      <span class="version-tag">v1.1.0</span>
    </a>
  </div>

  <nav class="header-nav">
    <a href="{root_prefix}docs/getting-started/index.html" class="nav-link {'active' if active_tab == 'docs' else ''}">Documentation</a>
    <a href="{root_prefix}docs/standard-library/index.html" class="nav-link {'active' if active_tab == 'stdlib' else ''}">Standard Library</a>
    <a href="{root_prefix}docs/dpm/index.html" class="nav-link {'active' if active_tab == 'dpm' else ''}">DPM</a>
    <a href="{root_prefix}docs/cookbook/rest-api.html" class="nav-link {'active' if active_tab == 'cookbook' else ''}">Cookbook</a>
    <a href="{root_prefix}docs/reference/cheat-sheet.html" class="nav-link {'active' if active_tab == 'reference' else ''}">Cheat Sheet</a>
  </nav>

  <div class="header-right">
    <button class="search-btn" aria-label="Search documentation">
      <i class="fa-solid fa-magnifying-glass"></i>
      <span>Search...</span>
      <span class="search-shortcut">Ctrl K</span>
    </button>
    <button class="theme-btn" id="theme-toggle" aria-label="Toggle dark mode">
      <i class="fa-solid fa-moon"></i>
    </button>
    <a href="https://github.com/djazair-language/djazair" target="_blank" rel="noopener noreferrer" class="icon-btn" aria-label="GitHub repository">
      <i class="fa-brands fa-github"></i>
    </a>
  </div>
</header>'''

def render_sidebar(current_path: str, root_prefix: str) -> str:
    html_parts = ['<aside class="docs-sidebar" id="docs-sidebar">']
    for cat in SITE_STRUCTURE:
        html_parts.append(f'''<div class="sidebar-category">
  <div class="category-title">
    <span><i class="fa-solid {cat['icon']} fa-fw" style="margin-right:6px; opacity:0.7;"></i> {html.escape(cat['category'])}</span>
  </div>
  <ul class="sidebar-items">''')
        for p in cat["pages"]:
            is_active = (p["path"] == current_path)
            active_class = "active" if is_active else ""
            html_parts.append(f'''    <li class="sidebar-item">
      <a href="{root_prefix}{p['path']}" class="sidebar-link {active_class}">{html.escape(p['title'])}</a>
    </li>''')
        html_parts.append('  </ul>\n</div>')
    html_parts.append('</aside>')
    return '\n'.join(html_parts)

def render_breadcrumbs(current_page: dict, root_prefix: str) -> str:
    return f'''<nav class="breadcrumbs" aria-label="Breadcrumb">
  <a href="{root_prefix}index.html">Home</a>
  <span class="breadcrumb-separator"><i class="fa-solid fa-chevron-right fa-xs"></i></span>
  <span>{html.escape(current_page['category'])}</span>
  <span class="breadcrumb-separator"><i class="fa-solid fa-chevron-right fa-xs"></i></span>
  <span style="color:var(--text-primary); font-weight:600;">{html.escape(current_page['title'])}</span>
</nav>'''

def render_nav_footer(current_page_idx: int, root_prefix: str) -> str:
    prev_page = ALL_PAGES[current_page_idx - 1] if current_page_idx > 0 else None
    next_page = ALL_PAGES[current_page_idx + 1] if current_page_idx < len(ALL_PAGES) - 1 else None

    html_parts = ['<div class="docs-nav-footer">']
    if prev_page:
        html_parts.append(f'''  <a href="{root_prefix}{prev_page['path']}" class="nav-card prev">
    <div class="nav-card-label"><i class="fa-solid fa-arrow-left"></i> Previous</div>
    <div class="nav-card-title">{html.escape(prev_page['title'])}</div>
  </a>''')
    else:
        html_parts.append('  <div></div>')

    if next_page:
        html_parts.append(f'''  <a href="{root_prefix}{next_page['path']}" class="nav-card next">
    <div class="nav-card-label">Next <i class="fa-solid fa-arrow-right"></i></div>
    <div class="nav-card-title">{html.escape(next_page['title'])}</div>
  </a>''')
    else:
        html_parts.append('  <div></div>')

    html_parts.append('</div>')
    return '\n'.join(html_parts)

def render_toc(toc_items: list) -> str:
    if not toc_items:
        return ''
    links_html = []
    for item in toc_items:
        indent = 'style="padding-left:1.5rem;"' if item["level"] == 3 else ''
        links_html.append(f'''    <li>
      <a href="#{item['id']}" class="toc-link" {indent}>{html.escape(item['text'])}</a>
    </li>''')

    return f'''<aside class="docs-toc">
  <div class="toc-title">On this page</div>
  <ul class="toc-links">
{chr(10).join(links_html)}
  </ul>
</aside>'''

def render_search_modal() -> str:
    return '''<div class="search-modal-backdrop" id="search-modal">
  <div class="search-modal">
    <div class="search-input-wrap">
      <i class="fa-solid fa-magnifying-glass"></i>
      <input type="text" id="search-input" class="search-input" placeholder="Search documentation, methods, keywords..." autocomplete="off">
    </div>
    <div class="search-results-list" id="search-results"></div>
    <div class="search-footer">
      <span>Navigate with <kbd>↑</kbd> <kbd>↓</kbd></span>
      <span>Open with <kbd>Enter</kbd></span>
      <span>Close with <kbd>Esc</kbd></span>
    </div>
  </div>
</div>'''

def render_docs_page(current_page: dict, content_html: str) -> str:
    """Assemble complete HTML page for documentation."""
    root_prefix = get_root_prefix(current_page["path"])
    
    # Highlight all code blocks in content
    highlighted_content = process_code_blocks(content_html)
    
    # Extract TOC from content
    toc_items = extract_toc(highlighted_content)
    
    # Find current index for prev/next
    current_idx = 0
    for idx, p in enumerate(ALL_PAGES):
        if p["path"] == current_page["path"]:
            current_idx = idx
            break

    active_tab = "docs"
    page_path = current_page["path"]
    if page_path.startswith("docs/dpm/"):
        active_tab = "dpm"
    elif page_path.startswith("docs/standard-library/"):
        active_tab = "stdlib"
    elif page_path.startswith("docs/cookbook/"):
        active_tab = "cookbook"
    elif page_path == "docs/reference/cheat-sheet.html":
        active_tab = "reference"

    navbar = render_navbar(root_prefix, active_tab=active_tab)
    sidebar = render_sidebar(current_page["path"], root_prefix)
    breadcrumbs = render_breadcrumbs(current_page, root_prefix)
    nav_footer = render_nav_footer(current_idx, root_prefix)
    toc = render_toc(toc_items)
    search_modal = render_search_modal()

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(current_page['title'])} | Djazair Documentation</title>
  <meta name="description" content="{html.escape(current_page['desc'])}">
  <link rel="icon" href="{root_prefix}assets/images/logo.svg" type="image/svg+xml">
  
  <!-- FontAwesome 6 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Google Fonts (Inter & JetBrains Mono) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Modern Docs Stylesheets -->
  <link rel="stylesheet" href="{root_prefix}assets/css/main.css">
  <link rel="stylesheet" href="{root_prefix}assets/css/syntax.css">
  
  <!-- Early theme application to avoid flash -->
  <script src="{root_prefix}assets/js/theme.js"></script>
</head>
<body>
  {navbar}

  <div class="docs-layout">
    <div class="sidebar-backdrop" id="sidebar-backdrop"></div>
    {sidebar}

    <main class="docs-content-wrapper">
      <article class="docs-article">
        {breadcrumbs}
        
        {highlighted_content}

        {nav_footer}
      </article>
    </main>

    {toc}
  </div>

  {search_modal}

  <!-- Scripts -->
  <script src="{root_prefix}assets/js/search-index.js"></script>
  <script src="{root_prefix}assets/js/search.js"></script>
  <script src="{root_prefix}assets/js/code-tools.js"></script>
  <script src="{root_prefix}assets/js/navigation.js"></script>
</body>
</html>'''
