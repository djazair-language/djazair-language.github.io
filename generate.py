import os
import re
import json

# Helper to compute root prefix relative path
def get_root_prefix(file_path):
    parts = file_path.split('/')
    if len(parts) > 1:
        return '../' * (len(parts) - 1)
    return ''

# Custom syntax highlighter for code snippets
def highlight_djazair(code):
    token_spec = [
        ('COMMENT_MULTI', r'#![\s\S]*?!#'),
        ('COMMENT_SINGLE', r'#[^\n]*'),
        ('STRING_DOUBLE', r'"(?:\\.|[^"\\])*"'),
        ('STRING_BACKTICK', r'`(?:\\.|[^`\\])*`'),
        ('NUMBER', r'\b\d+(?:_\d+)*(?:\.\d+)?\b'),
        ('KEYWORD', r'\b(?:let|fn|return|class|init|super|self|is|instanceof|try|catch|finally|throw|if|elif|else|match|case|default|while|do|for|in|to|break|continue|and|or|not|Null|True|False|use|import|as|end|async|await|new)\b'),
        ('BUILTIN', r'\b(?:print|input|type|str|num|bool|int|float|chr|ord|range|enumerate|zip|abs|round|exit|isNull|isString|isNumber|isBool|isArray|isMap|isFunction|isClass|isInstance|__native|hasNative|getFile|getDir|getLine)\b'),
        ('FN_NAME', r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OP', r'[+\-*/%&|^~<>!=.?:@#]+'),
        ('SPACE', r'\s+'),
        ('OTHER', r'.')
    ]
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    def esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    highlighted = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        escaped = esc(value)
        if kind in ('COMMENT_MULTI', 'COMMENT_SINGLE'):
            highlighted.append(f'<span class="comment">{escaped}</span>')
        elif kind in ('STRING_DOUBLE', 'STRING_BACKTICK'):
            highlighted.append(f'<span class="str">{escaped}</span>')
        elif kind == 'KEYWORD':
            highlighted.append(f'<span class="kw">{escaped}</span>')
        elif kind == 'BUILTIN':
            highlighted.append(f'<span class="nd">{escaped}</span>')
        elif kind == 'NUMBER':
            highlighted.append(f'<span class="num">{escaped}</span>')
        elif kind == 'FN_NAME':
            highlighted.append(f'<span class="fn">{escaped}</span>')
        elif kind == 'OP':
            highlighted.append(f'<span class="op">{escaped}</span>')
        else:
            highlighted.append(escaped)
            
    return ''.join(highlighted)

# Parse custom markdown-like code block triggers in page content
def process_code_blocks(content):
    def replacer(match):
        code = match.group(1).strip('\n')
        return f'<pre><code>{highlight_djazair(code)}</code></pre>'
    
    pattern = r'<pre class="dz"><code>(.*?)</code></pre>'
    return re.sub(pattern, replacer, content, flags=re.DOTALL)

# Main page template
LAYOUT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} | Djazair Documentation</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%2310b981%22/><text x=%2250%22 y=%2268%22 font-size=%2250%22 font-weight=%22800%22 fill=%22white%22 text-anchor=%22middle%22 font-family=%22system-ui%22>Dz</text></svg>">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="{root_prefix}assets/style.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fuse.js/7.0.0/fuse.min.js"></script>
    <script id="search-index-data" type="application/json">{search_index_json}</script>
    <style>
        .feature-icon {{
            width: 48px; height: 48px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 12px;
            background: rgba(16, 185, 129, 0.1);
            color: var(--color-primary);
            font-size: 1.25rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }}
        .feature-card:hover .feature-icon {{
            background: var(--color-primary);
            color: #fff;
            transform: scale(1.05) translateY(-1px);
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        }}
        .feature-card {{
            opacity: 0;
            transform: translateY(24px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }}
        .feature-card.reveal {{
            opacity: 1;
            transform: translateY(0);
        }}
        .hero-section {{
            animation: fadeInDown 0.6s ease;
        }}
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        .search-container {{ position: relative; }}
        #search-results {{
            position: absolute; top: calc(100% + 8px); right: 0; width: 380px;
            max-height: 400px; overflow-y: auto;
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            display: none; z-index: 200;
        }}
        #search-results.show {{ display: block; }}
        #search-results .result-item {{
            display: block; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-color);
            color: var(--text-primary); text-decoration: none; transition: background 0.15s;
        }}
        #search-results .result-item:last-child {{ border-bottom: none; }}
        #search-results .result-item:hover {{ background: rgba(16,185,129,0.08); }}
        #search-results .result-item .result-title {{ font-weight: 600; font-size: 0.9rem; }}
        #search-results .result-item .result-desc {{ color: var(--text-muted); font-size: 0.8rem; margin-top: 2px; }}
        #search-results .result-empty {{ padding: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.9rem; }}
        .pre-wrapper {{ position: relative; }}
        .copy-btn {{
            position: absolute; top: 8px; right: 8px;
            background: rgba(255,255,255,0.06); border: 1px solid var(--border-color);
            color: var(--text-secondary); border-radius: 6px; padding: 4px 10px;
            font-size: 0.75rem; cursor: pointer; opacity: 0;
            transition: opacity 0.2s, background 0.2s;
        }}
        .pre-wrapper:hover .copy-btn {{ opacity: 1; }}
        .copy-btn:hover {{ background: var(--color-primary); color: #fff; border-color: var(--color-primary); }}
        .copy-btn.copied {{ background: var(--color-primary); color: #fff; border-color: var(--color-primary); }}
        .toc-links li.active a {{ color: var(--color-primary); font-weight: 600; }}
    </style>
</head>
<body>
    <header>
        <div class="logo-container">
            <div class="logo-icon">Dz</div>
            <div class="logo-text">Djazair</div>
            <div class="logo-version">v1.0.5</div>
        </div>
        <nav class="top-nav">
            <a href="{root_prefix}index.html" {active_home}>Home</a>
            <a href="{root_prefix}getting-started/installation.html" {active_getting}>Getting Started</a>
            <a href="{root_prefix}language-guide/comments.html" {active_guide}>Language Guide</a>
            <a href="{root_prefix}examples/hello-world.html" {active_examples}>Examples</a>
            <a href="{root_prefix}reference/keywords.html" {active_ref}>Reference</a>
            <a href="{root_prefix}faq.html" {active_faq}>FAQ</a>
        </nav>
        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" id="search-input" class="search-input" placeholder="Search docs...  (Ctrl+K)">
            <div id="search-results"></div>
        </div>
    </header>

    <div class="app-container">
        <aside class="sidebar">
            {sidebar}
        </aside>

        <main class="content-wrapper">
            <div class="content-body">
                <div class="breadcrumbs">
                    {breadcrumbs}
                </div>
                
                <article>
                    {content}
                </article>

                <div class="page-navigation">
                    {page_nav}
                </div>

                <footer>
                    <div>&copy; 2026 Harizi Riyadh. Released under the MIT License.</div>
                    <div>Official Documentation Website for Djazair.</div>
                </footer>
            </div>
        </main>

        <aside class="toc-wrapper">
            <div class="toc-title">On this page</div>
            <ul class="toc-links">
                {toc_items}
            </ul>
        </aside>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            // --- Scroll-reveal for feature cards ---
            (function() {{
                var observer = new IntersectionObserver(function(entries) {{
                    entries.forEach(function(entry) {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add("reveal");
                            observer.unobserve(entry.target);
                        }}
                    }});
                }}, {{ threshold: 0.1 }});
                var cards = document.querySelectorAll(".feature-card");
                for (var i = 0; i < cards.length; i++) observer.observe(cards[i]);
            }})();

            // --- Submenu arrow state ---
            (function() {{
                document.querySelectorAll(".has-submenu > a").forEach(function(el) {{
                    var li = el.closest("li");
                    var sm = li.querySelector(".submenu");
                    if (sm && sm.getAttribute("data-expanded") === "true") {{
                        el.querySelector(".arrow").textContent = "v";
                    }}
                }});
            }})();

            // --- Code copy buttons ---
            (function() {{
                document.querySelectorAll("pre > code").forEach(function(code) {{
                    var pre = code.parentElement;
                    if (pre.classList.contains("pre-wrapper")) return;
                    pre.classList.add("pre-wrapper");
                    var btn = document.createElement("button");
                    btn.className = "copy-btn";
                    btn.textContent = "Copy";
                    btn.setAttribute("aria-label", "Copy code to clipboard");
                    btn.addEventListener("click", function() {{
                        var text = code.textContent;
                        navigator.clipboard.writeText(text).then(function() {{
                            btn.textContent = "Copied!";
                            btn.classList.add("copied");
                            setTimeout(function() {{ btn.textContent = "Copy"; btn.classList.remove("copied"); }}, 2000);
                        }});
                    }});
                    pre.appendChild(btn);
                }});
            }})();

            // --- Full-text search via Fuse.js (inline index, no fetch) ---
            (function() {{
                var input = document.getElementById("search-input");
                var resultsEl = document.getElementById("search-results");
                var indexScript = document.getElementById("search-index-data");
                if (!input || !resultsEl || !indexScript || typeof Fuse === "undefined") return;

                var data;
                try {{ data = JSON.parse(indexScript.textContent); }} catch(e) {{ return; }}
                var fuse = new Fuse(data, {{
                    keys: ["title", "description", "text"],
                    threshold: 0.4,
                    includeScore: true,
                    minMatchCharLength: 2
                }});

                input.addEventListener("input", function() {{
                    var query = input.value.trim();
                    if (query.length < 2) {{ resultsEl.classList.remove("show"); return; }}
                    var results = fuse.search(query);
                    var html = "";
                    if (results.length === 0) {{
                        html = '<div class="result-empty">No results found</div>';
                    }} else {{
                        for (var i = 0; i < Math.min(results.length, 10); i++) {{
                            var r = results[i].item;
                            html += '<a href="' + r.path + '" class="result-item">' +
                                '<div class="result-title">' + r.title + '</div>' +
                                '<div class="result-desc">' + r.description + '</div>' +
                                '</a>';
                        }}
                    }}
                    resultsEl.innerHTML = html;
                    resultsEl.classList.add("show");
                }});

                input.addEventListener("blur", function() {{
                    setTimeout(function() {{ resultsEl.classList.remove("show"); }}, 200);
                }});
                input.addEventListener("focus", function() {{
                    if (input.value.trim().length >= 2) resultsEl.classList.add("show");
                }});

                // Ctrl+K / Cmd+K focus
                document.addEventListener("keydown", function(e) {{
                    if ((e.ctrlKey || e.metaKey) && e.key === "k") {{
                        e.preventDefault();
                        input.focus();
                        input.select();
                    }}
                }});
            }})();

            // --- Scroll-spy TOC ---
            (function() {{
                var tocLinks = document.querySelectorAll(".toc-links a");
                if (tocLinks.length === 0) return;
                var headings = [];
                tocLinks.forEach(function(a) {{
                    var id = a.getAttribute("href").slice(1);
                    var el = document.getElementById(id);
                    if (el) headings.push({{ el: el, link: a.parentElement }});
                }});
                if (headings.length === 0) return;
                var observer = new IntersectionObserver(function(entries) {{
                    entries.forEach(function(entry) {{
                        if (entry.isIntersecting) {{
                            headings.forEach(function(h) {{ h.link.classList.remove("active"); }});
                            var found = headings.find(function(h) {{ return h.el === entry.target; }});
                            if (found) found.link.classList.add("active");
                        }}
                    }});
                }}, {{ rootMargin: "-80px 0px -60% 0px" }});
                headings.forEach(function(h) {{ observer.observe(h.el); }});
            }})();
        }});
    </script>
</body>
</html>
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STRUCTURE = [
    {
        "category": "Getting Started",
        "pages": [
            {"title": "Installation", "path": "getting-started/installation.html", "description": "Install and build Djazair from source code on Windows, Linux, and macOS."},
            {"title": "First Program", "path": "getting-started/first-program.html", "description": "Write and run your very first hello world program in Djazair."},
            {"title": "Running Programs", "path": "getting-started/running-programs.html", "description": "Learn the various CLI commands to execute your scripts inline or via files."},
        ]
    },
    {
        "category": "Language Guide",
        "pages": [
            {"title": "Comments", "path": "language-guide/comments.html", "description": "Learn how to document your Djazair code with single and multi-line comments."},
            {"title": "Variables", "path": "language-guide/variables.html", "description": "Declare variables with let and understand lexical block scoping."},
            {"title": "Data Types", "path": "language-guide/data-types.html", "description": "Understand primitive and object types, dynamic typing, and memory model."},
            {"title": "Input & Output", "path": "language-guide/input-output.html", "description": "Console output, user input, and string formatting in Djazair."},
            {"title": "Operators", "path": "language-guide/operators.html", "description": "Examine mathematical, comparison, logical, assignment, and membership operators."},
            {"title": "Conditions", "path": "language-guide/conditions.html", "description": "Control execution flow using if-elif-else statements and ternary expressions."},
            {"title": "Loops", "path": "language-guide/loops.html", "description": "Write loops using while, do-while, and for-in iterators over collections and ranges."},
            {"title": "Arrays", "path": "language-guide/arrays.html", "description": "Create dynamic lists and manipulate them using standard array methods."},
            {"title": "Strings", "path": "language-guide/strings.html", "description": "Learn string interpolation, multi-line blocks, and comprehensive string methods."},
            {"title": "Maps", "path": "language-guide/maps.html", "description": "Create and manipulate key-value hash maps with built-in methods."},
            {"title": "Functions", "path": "language-guide/functions.html", "description": "Write reusable code blocks, closures, arrow functions, and default arguments."},
            {"title": "Modules", "path": "language-guide/modules.html", "description": "Import files and use native modules to organize codebases cleanly."},
            {"title": "Classes", "path": "language-guide/classes.html", "description": "Develop using Object-Oriented paradigms: classes, inheritance, super, and self."},
            {"title": "Error Handling", "path": "language-guide/error-handling.html", "description": "Handle runtime issues gracefully using try-catch-finally blocks and throw statements."},
            {"title": "Async / Await", "path": "language-guide/async-await.html", "description": "Concurrent programming with coroutines using async and await."},
        ]
    },
    {
        "category": "Standard Library",
        "pages": [
            {"title": "Overview", "path": "standard-library/index.html", "description": "A comprehensive index of all standard library modules."},
            {"title": "assert Module", "path": "standard-library/assert.html", "description": "Debugging and unit-testing assertion functions for validating values.", "subs": [
                {"title": "Truthiness Assertions", "anchor": "truthiness-assertions"},
                {"title": "Value Assertions", "anchor": "value-assertions"},
                {"title": "Type Assertions", "anchor": "type-assertions"}
            ]},
            {"title": "bytes Module", "path": "standard-library/bytes.html", "description": "Binary data manipulation and conversion utilities.", "subs": [
                {"title": "Creation & Conversion", "anchor": "creation--conversion"},
                {"title": "Manipulation", "anchor": "manipulation"}
            ]},
            {"title": "collections Module", "path": "standard-library/collections.html", "description": "Specialized container data types beyond built-in Array and Map."},
            {"title": "crypto Module", "path": "standard-library/crypto.html", "description": "Cryptographic hashing algorithms (SHA-256, etc.) and HMAC operations."},
            {"title": "datetime Module", "path": "standard-library/datetime.html", "description": "Date, time, and timezone manipulation functions and the Date class.", "subs": [
                {"title": "Time Functions", "anchor": "time-functions"},
                {"title": "Date Class", "anchor": "date-class"}
            ]},
            {"title": "dir Module", "path": "standard-library/dir.html", "description": "Directory traversal, creation, removal, and listing operations."},
            {"title": "env Module", "path": "standard-library/env.html", "description": "Access and manipulate environment variables at runtime."},
            {"title": "file Module", "path": "standard-library/file.html", "description": "File reading, writing, manipulation, and status query operations.", "subs": [
                {"title": "Read & Write", "anchor": "read--write-operations"},
                {"title": "File Manipulation", "anchor": "file-manipulation"},
                {"title": "Status Query", "anchor": "status-query"}
            ]},
            {"title": "http Module", "path": "standard-library/http.html", "description": "HTTP client and server implementations for web communication.", "subs": [
                {"title": "HTTP Client", "anchor": "http-client"},
                {"title": "HTTP Server", "anchor": "http-server"},
                {"title": "Classes & Helpers", "anchor": "classes--helpers"}
            ]},
            {"title": "json Module", "path": "standard-library/json.html", "description": "JSON parsing and stringification for data interchange."},
            {"title": "lang Module", "path": "standard-library/lang.html", "description": "Runtime introspection, control, and library path management.", "subs": [
                {"title": "Runtime Info", "anchor": "runtime-info"},
                {"title": "Control", "anchor": "control"},
                {"title": "Introspection", "anchor": "introspection"},
                {"title": "Library Paths", "anchor": "library-paths--queries"}
            ]},
            {"title": "math Module", "path": "standard-library/math.html", "description": "Mathematical constants, trigonometry, exponentiation, and statistics.", "subs": [
                {"title": "Constants", "anchor": "constants"},
                {"title": "Trigonometry", "anchor": "trigonometry"},
                {"title": "Exponentiation & Logs", "anchor": "exponentiation--logs"},
                {"title": "Rounding", "anchor": "rounding--absolute"},
                {"title": "Statistics", "anchor": "comparison--statistics"}
            ]},
            {"title": "net Module", "path": "standard-library/net.html", "description": "TCP networking: server and client classes for socket communication.", "subs": [
                {"title": "Classes & Exports", "anchor": "classes--exports"},
                {"title": "TCP Server", "anchor": "tcp-server-example"},
                {"title": "TCP Client", "anchor": "tcp-client-example"}
            ]},
            {"title": "os Module", "path": "standard-library/os.html", "description": "Platform detection, system information, and user/temp file paths.", "subs": [
                {"title": "Platform Detection", "anchor": "platform-detection"},
                {"title": "System Information", "anchor": "system-information"},
                {"title": "User & Temp Files", "anchor": "user--temporary-files"}
            ]},
            {"title": "path Module", "path": "standard-library/path.html", "description": "Cross-platform path joining, resolution, decomposition, and security checks.", "subs": [
                {"title": "Constants", "anchor": "constants"},
                {"title": "Join & Resolve", "anchor": "join--resolve"},
                {"title": "Decomposition", "anchor": "decomposition"},
                {"title": "Query & Security", "anchor": "query--security"}
            ]},
            {"title": "process Module", "path": "standard-library/process.html", "description": "Process identification, control, working directory, CLI args, and command execution.", "subs": [
                {"title": "Identification", "anchor": "process-identification"},
                {"title": "Process Control", "anchor": "process-control"},
                {"title": "Working Directory", "anchor": "working-directory"},
                {"title": "Command Execution", "anchor": "command-execution"},
                {"title": "CLI & Script", "anchor": "cli-arguments--script-location"},
                {"title": "Async Spawning", "anchor": "asynchronous-spawning"}
            ]},
            {"title": "random Module", "path": "standard-library/random.html", "description": "Random number generation and sampling utilities."},
            {"title": "regex Module", "path": "standard-library/regex.html", "description": "Regular expression pattern matching, search, and replace operations.", "subs": [
                {"title": "Flags", "anchor": "flags"},
                {"title": "Pattern Class", "anchor": "pattern-class"},
                {"title": "Match Class", "anchor": "match-class"},
                {"title": "Convenience Functions", "anchor": "convenience-functions"}
            ]},
            {"title": "thread Module", "path": "standard-library/thread.html", "description": "Parallel execution via threads, workers, and synchronization.", "subs": [
                {"title": "Thread Class", "anchor": "thread-class"},
                {"title": "Worker Functions", "anchor": "worker-side-functions"},
                {"title": "Convenience", "anchor": "convenience-functions"}
            ]},
            {"title": "uuid Module", "path": "standard-library/uuid.html", "description": "Generate universally unique identifiers (UUID v4)."},
        ]
    },
    {
        "category": "Examples",
        "pages": [
            {"title": "Hello World", "path": "examples/hello-world.html", "description": "Standard hello world code snippet and explanation."},
            {"title": "Calculator", "path": "examples/calculator.html", "description": "Implement a fully featured command-line calculator in Djazair."},
            {"title": "Todo App", "path": "examples/todo-app.html", "description": "A console Todo tracker demonstrating list manipulation and file persistence."},
            {"title": "File Processing", "path": "examples/file-processing.html", "description": "Read files line-by-line, parse data structures, and output logs."},
        ]
    },
    {
        "category": "Reference",
        "pages": [
            {"title": "Keywords", "path": "reference/keywords.html", "description": "Complete list of reserved keywords in the Djazair language."},
            {"title": "Operators", "path": "reference/operators.html", "description": "Arithmetic, comparison, logical, bitwise, and other operators."},
            {"title": "Built-in Functions", "path": "reference/builtins.html", "description": "Globally available functions for type conversion, I/O, and utilities."},
            {"title": "Methods", "path": "reference/methods.html", "description": "Built-in methods on Strings, Arrays, and Maps."},
            {"title": "Syntax Reference", "path": "reference/syntax-reference.html", "description": "Formal grammar and syntax rules of the Djazair language."},
            {"title": "Embedding API", "path": "reference/embedding.html", "description": "C/C++ API for embedding Djazair in applications."},
        ]
    }
]

# Flat list for navigation
FLAT_PAGES = []
FLAT_PAGES.append({"title": "Home", "path": "index.html", "description": "The Djazair Programming Language official documentation home page."})
for cat in STRUCTURE:
    for page in cat["pages"]:
        FLAT_PAGES.append(page)
FLAT_PAGES.append({"title": "FAQ", "path": "faq.html", "description": "Frequently Asked Questions about Djazair syntax, internals, and performance."})

# Page contents dictionary
PAGES_CONTENT = {}

PAGES_CONTENT["index.html"] = """
<div class="hero-section">
    <h1 class="hero-title">The Djazair Programming Language</h1>
    <p class="hero-subtitle">A modern, embeddable scripting language — written in pure C, featuring async coroutines, pattern matching, OOP, and a rich standard library. Designed for automation, tooling, game development, and seamless C/C++ embedding.</p>
    <div class="hero-buttons">
        <a href="getting-started/installation.html" class="btn btn-primary">Get Started</a>
        <a href="language-guide/comments.html" class="btn btn-secondary">Learn the Language</a>
    </div>
</div>

<h2>Why Djazair?</h2>
<p>Djazair is a lightweight, zero-dependency scripting engine written in pure C, designed from the ground up for <strong>embeddability and expressiveness</strong>. Whether you are adding scripting to a C/C++ application, writing automation scripts, building game logic, or prototyping ideas, Djazair gives you a modern, familiar syntax with first-class <strong>async/await coroutines</strong>, <strong>pattern matching</strong>, <strong>full OOP</strong>, and automatic memory management — all in a single portable library.</p>

<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-bolt"></i></div>
        <div class="feature-title">Dynamic Typing & Inference</div>
        <div class="feature-desc">Write less boilerplate with <code>let</code> declarations, native Arrays and Maps, first-class functions, and closures — productive from the first line.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-rocket"></i></div>
        <div class="feature-title">Async/Await Coroutines</div>
        <div class="feature-desc">First-class coroutines for non-blocking I/O, concurrent workflows, and efficient async scripting — no callback spaghetti, no external event loop.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-landmark"></i></div>
        <div class="feature-title">Object-Oriented Programming</div>
        <div class="feature-desc">Full OOP with <code>class</code>, single inheritance, constructors (<code>init</code>), <code>super</code>, and polymorphism — build organised, maintainable code at any scale.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-bullseye"></i></div>
        <div class="feature-title">Pattern Matching</div>
        <div class="feature-desc">Expressive <code>match</code>/<code>case</code>/<code>default</code> constructs for clean, declarative branching — more readable than chains of <code>elif</code>.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-plug"></i></div>
        <div class="feature-title">Embedding-First C API</div>
        <div class="feature-desc">Pure C with zero external dependencies. Embed into any C/C++ project via a minimal, documented API — ideal for extending applications with scripting.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-battery-full"></i></div>
        <div class="feature-title">Batteries Included</div>
        <div class="feature-desc">Comprehensive standard library: regex, TCP/UDP networking, JSON, crypto (SHA-256), threads, file I/O, date/time, math, UUID, and more — ready out of the box.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-shield-halved"></i></div>
        <div class="feature-title">Robust Error Handling</div>
        <div class="feature-desc">Structured <code>try</code>/<code>catch</code>/<code>finally</code> with <code>throw</code> for reliable error recovery — write production-ready scripts with confidence.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon"><i class="fa-solid fa-puzzle-piece"></i></div>
        <div class="feature-title">Automatic Memory Management</div>
        <div class="feature-desc">Precise tracing garbage collector — no reference counting, no manual <code>free()</code>. Focus on your logic, not memory.</div>
    </div>
</div>

<h2>Quick Snippet Preview</h2>
<p>Here is a taste of Djazair showing functions, dynamic string interpolation, and standard library modules:</p>
<pre class="dz"><code>use math

fn computeArea(radius)
    return math.PI * math.pow(radius, 2)
end

let r = 5
print("The area of a circle with radius ${r} is ${computeArea(r)}")
# Output => The area of a circle with radius 5 is 78.5398
</code></pre>
"""

PAGES_CONTENT["getting-started/installation.html"] = """
<h1>Installing Djazair</h1>
<p>Djazair is built to compile cleanly on Linux, macOS, and Windows. It relies on standard compiler environments and has minimal external dependencies.</p>

<h2>Linux & macOS Compilation</h2>
<p>Ensure you have GCC or Clang and <code>make</code> installed. Open a terminal and run the following commands:</p>
<pre class="bash"><code># Clone the repository
git clone https://github.com/djazair-language/djazair.git
cd djazair

# Build the interpreter using Makefile (very fast!)
make

# Optionally install it system-wide (requires root/sudo)
sudo make install
</code></pre>
<p>The build outputs will be placed under <code>build/bin/djazair</code>.</p>

<h2>Windows Compilation</h2>
<p>To compile on Windows, you must have a MinGW-w64 compiler environment installed, along with <code>libregex</code> (specifically <code>mingw-w64-x86_64-libgnurx</code>) for pattern matching capabilities. Run the automated build script in PowerShell:</p>
<pre class="powershell"><code># Navigate to workspace directory
cd djazair-language

# Run build script
tools\\build.ps1
</code></pre>
<p>The compiler will output <code>build\\bin\\djazair.exe</code>.</p>

<div class="alert alert-note">
    <p><strong>MinGW Dependency Tip:</strong> If you receive linker errors regarding regular expressions on Windows, ensure that <code>libgnurx</code> or a compatible regex library is installed in your MSYS2 / MinGW installation.</p>
</div>
"""

PAGES_CONTENT["getting-started/first-program.html"] = """
<h1>Your First Djazair Program</h1>
<p>In this guide, we will write, structure, and run our very first program in Djazair.</p>

<h2>Writing the Script</h2>
<p>Create a file named <code>hello.dz</code> in your preferred editor. Paste the following line of code into it:</p>
<pre class="dz"><code># Hello world in Djazair
print("Hello from Djazair!")
</code></pre>

<h2>Running the Script</h2>
<p>Invoke the Djazair interpreter pointing to the script file:</p>
<pre class="bash"><code># Executing hello.dz
./build/bin/djazair hello.dz
</code></pre>
<p>You should see the output printed to the terminal console:</p>
<pre class="text"><code>Hello from Djazair!</code></pre>

<h2>Interactive Expression Testing</h2>
<p>Djazair also supports running inline code snippets without a file by utilizing the <code>-c</code> CLI command option:</p>
<pre class="bash"><code>djazair -c 'print("Inline: " + str(10 + 20))'
# Output => Inline: 30
</code></pre>
"""

PAGES_CONTENT["getting-started/running-programs.html"] = """
<h1>Running Djazair Scripts</h1>
<p>The Djazair interpreter offers a command-line interface (CLI) to execute code, check versions, and configure file paths.</p>

<h2>CLI Usage</h2>
<p>The general syntax of the interpreter CLI is:</p>
<pre class="bash"><code>djazair [options] [script_file.dz] [arguments...]</code></pre>

<h2>Available Options</h2>
<table>
    <thead>
        <tr>
            <th>Option</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>-c "code"</code></td>
            <td>Executes the given inline script string directly.</td>
        </tr>
        <tr>
            <td><code>-d</code> / <code>--debug</code></td>
            <td>Enable virtual machine debugger mode (traces bytecode execution and stack status).</td>
        </tr>
        <tr>
            <td><code>-v</code> / <code>--version</code></td>
            <td>Prints the interpreter build version and exits.</td>
        </tr>
        <tr>
            <td><code>--disasm</code></td>
            <td>Disassembles compiled code instructions to standard output.</td>
        </tr>
    </tbody>
</table>

<h2>Script Arguments</h2>
<p>Any arguments passed after the script file path are automatically collected and made available inside your code as a list named <code>args</code>:</p>
<pre class="dz"><code># script.dz
print("Supplied Arguments:")
for arg in args
    print(" - " + arg)
end
</code></pre>
<p>Run it like this:</p>
<pre class="bash"><code>djazair script.dz first second third</code></pre>
"""

PAGES_CONTENT["language-guide/comments.html"] = """
<h1>Comments</h1>
<p>Comments are text entries ignored by the compiler, used to document structures and write explanations.</p>

<h2>Single-line Comments</h2>
<p>Single-line comments start with a hash character (<code>#</code>). Everything following the <code>#</code> on that line is ignored:</p>
<pre class="dz"><code># Declare a score variable
let score = 100 # Inline comment about score
</code></pre>
"""

PAGES_CONTENT["language-guide/variables.html"] = """
<h1>Variables & Scope</h1>
<p>Variables store values. Djazair is dynamically typed, meaning variables can hold any type of value and change types over time.</p>

<h2>Declaration</h2>
<p>Declare variables using <code>let</code>:</p>
<pre class="dz"><code>let username = "Riyadh"
let age = 30
let balance = 200.50

# Reassignment
balance = 450.75
</code></pre>

<h2>Scoping Rules</h2>
<p>Djazair uses lexical block scoping. Variables declared inside a block (such as an <code>if</code> block, loop, or function body) are local to that block and cannot be accessed outside of it:</p>
<pre class="dz"><code>let x = 10
if x > 5
    let y = 20 # local to this if-block
    print(x + y) # => 30
end

# print(y) # Error: y is not defined!
</code></pre>


"""

PAGES_CONTENT["language-guide/data-types.html"] = """
<h1>Data Types</h1>
<p>Djazair features a rich set of built-in data types. It uses dynamic typing, but every value has a concrete runtime type.</p>

<h2>Summary of Types</h2>
<table>
    <thead>
        <tr>
            <th>Type</th>
            <th>Sample Literals</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Number</strong></td>
            <td><code>42</code>, <code>3.14</code>, <code>100_000</code></td>
            <td>64-bit floating point number (double-precision). Underscores as thousands separators.</td>
        </tr>
        <tr>
            <td><strong>String</strong></td>
            <td><code>"hello"</code>, <code>`multi`</code></td>
            <td>UTF-8 immutable text sequences. Supports multiline blocks and interpolation.</td>
        </tr>
        <tr>
            <td><strong>Bool</strong></td>
            <td><code>True</code>, <code>False</code></td>
            <td>Boolean truth values. Note the capitalization.</td>
        </tr>
        <tr>
            <td><strong>Null</strong></td>
            <td><code>Null</code></td>
            <td>Representing the absence of value.</td>
        </tr>
        <tr>
            <td><strong>Array</strong></td>
            <td><code>[1, "two", True]</code></td>
            <td>Dynamically sized ordered lists. Can hold mixed types.</td>
        </tr>
        <tr>
            <td><strong>Map</strong></td>
            <td><code>{"key": "value"}</code></td>
            <td>Hash tables associating keys with values. Keys can be any type.</td>
        </tr>
        <tr>
            <td><strong>Range</strong></td>
            <td><code>1..5</code>, <code>0 to 10</code></td>
            <td>Inclusive sequences of numeric values, ideal for iteration.</td>
        </tr>
        <tr>
            <td><strong>Function</strong></td>
            <td><code>fn() ... end</code></td>
            <td>First-class callable closures. Can be stored and passed around.</td>
        </tr>
    </tbody>
</table>

<h2>Type Casting</h2>
<p>Convert between types using built-in casting functions:</p>
<pre class="dz"><code>let n = int(3.14)       # => 3
let f = float("2.5")    # => 2.5
let s = str(42)         # => "42"
let b = bool(1)         # => True
let x = num("10.5")     # => 10.5 (generic number conversion)
</code></pre>
<p>Falsy values (convert to <code>False</code>): <code>Null</code>, <code>False</code>, <code>0</code>, <code>0.0</code>, empty string <code>""</code>, empty array <code>[]</code>, empty map <code>{}</code>.</p>

<h2>Querying Types</h2>
<p>Use the built-in <code>type()</code> function or type assertions to inspect variables at runtime:</p>
<pre class="dz"><code>let val = 123.45
print(type(val)) # => Number
print(isNumber(val)) # => True
print(isString(val)) # => False
</code></pre>
"""

PAGES_CONTENT["language-guide/input-output.html"] = """
<h1>Input & Output</h1>
<p>Djazair provides built-in functions for console output and user input.</p>

<h2>Console Output</h2>
<p>Use <code>print()</code> to output values to stdout. It accepts multiple arguments separated by spaces:</p>
<pre class="dz"><code>print("Hello World")
print("The answer is", 42)
print("Value:", True, Null, [1, 2])
</code></pre>

<h2>String Interpolation</h2>
<p>Embed expressions inside double-quoted strings using <code>${expr}</code>:</p>
<pre class="dz"><code>let name = "Riad"
let age = 30
print("${name} is ${age} years old")
# Output: Riad is 30 years old
</code></pre>

<h2>User Input</h2>
<p>Use <code>input(prompt?)</code> to read a line from stdin:</p>
<pre class="dz"><code>let name = input("Enter your name: ")
print("Hello, ${name}!")
</code></pre>
"""

PAGES_CONTENT["language-guide/operators.html"] = """
<h1>Operators Reference</h1>
<p>Djazair provides standard arithmetic, comparison, logical, bitwise, assignment, increment/decrement, and identity operators.</p>

<h2>Arithmetic Operators</h2>
<p>Basic mathematical calculations:</p>
<pre class="dz"><code>let sum = 10 + 5    # Addition => 15
let diff = 10 - 5   # Subtraction => 5
let prod = 10 * 5   # Multiplication => 50
let div = 10 / 4    # Division => 2.5
let fdiv = 10 // 4  # Floor division => 2
let power = 2 ** 3  # Exponentiation => 8
let rem = 10 % 3    # Modulo => 1
</code></pre>

<h2>Increment & Decrement</h2>
<p>Both prefix and postfix forms are supported:</p>
<pre class="dz"><code>let n = 5
print(n++)  # Postfix: prints 5, then increments to 6
print(++n)  # Prefix: increments to 7, prints 7
print(n--)  # Postfix: prints 7, then decrements to 6
print(--n)  # Prefix: decrements to 5, prints 5
</code></pre>

<h2>Logical Operators</h2>
<p>Logical chaining uses descriptive keywords: <code>and</code>, <code>or</code>, and <code>not</code>:</p>
<pre class="dz"><code>let condition1 = True
let condition2 = False

print(condition1 and condition2) # => False
print(condition1 or condition2)  # => True
print(not condition1)            # => False
</code></pre>

<h2>Identity Operators (is / is not)</h2>
<p>Check if two variables reference the same object in memory:</p>
<pre class="dz"><code>let a = [1, 2]
let b = a
let c = [1, 2]
print(a is b)      # => True  (same reference)
print(a is c)      # => False (different objects)
print(a is not c)  # => True
print(Null is Null) # => True
</code></pre>

<h2>Type Checking (instanceof)</h2>
<p>Check if a value is an instance of a given type (pass type name as a string):</p>
<pre class="dz"><code>print(42 instanceof "Number")    # => True
print("hi" instanceof "String")  # => True
print(True instanceof "Bool")    # => True
print(Null instanceof "Null")    # => True
print([1,2] instanceof "Array")  # => True
print({"a":1} instanceof "Map")  # => True

class Animal end
class Dog is Animal end
let d = Dog()
print(d instanceof Dog)     # => True
print(d instanceof Animal)  # => True (inheritance)
</code></pre>

<h2>Membership Operators (in / not in)</h2>
<p>Check if items exist in strings, arrays, or maps:</p>
<pre class="dz"><code>print(2 in [1, 2, 3])       # => True
print(5 not in [1, 2, 3])   # => True
print("name" in {"name": "A"}) # => True (key exists)
print("orld" in "Hello World") # => True (substring)
</code></pre>
"""

PAGES_CONTENT["language-guide/conditions.html"] = """
<h1>Conditions (If-Else & Match)</h1>
<p>Control flow structures let your script make decisions depending on boolean expressions or value patterns.</p>

<h2>If, Elif, Else</h2>
<p>The conditional syntax uses <code>if</code>, <code>elif</code>, <code>else</code>, and concludes with the <code>end</code> keyword:</p>
<pre class="dz"><code>let score = 85

if score >= 90
    print("Grade: A")
elif score >= 80
    print("Grade: B")
elif score >= 70
    print("Grade: C")
else
    print("Grade: F")
end
</code></pre>

<h2>Ternary Conditional Expression</h2>
<p>Djazair supports a ternary operator syntax that begins with an <code>if</code> statement inline:</p>
<pre class="dz"><code>let age = 19
let category = if age >= 18 ? "Adult" else "Minor"
print(category) # => Adult
</code></pre>



<h2>Match / Case / Default</h2>
<p>Pattern matching for multi-way branching. Case values are literal comparisons with no fall-through:</p>
<pre class="dz"><code>let day = 6
match day
case 6
    print("Saturday")
case 7
    print("Sunday")
default
    print("Weekday")
end
</code></pre>
"""

PAGES_CONTENT["language-guide/loops.html"] = """
<h1>Loops</h1>
<p>Perform repeated executions using <code>while</code>, <code>do-while</code>, and <code>for-in</code> constructs.</p>

<h2>While Loop</h2>
<p>Runs as long as a boolean expression evaluates to <code>True</code>:</p>
<pre class="dz"><code>let i = 1
while i <= 5
    print("Count: ${i}")
    i = i + 1
end
</code></pre>

<h2>Do-While Loop</h2>
<p>Executes the body block at least once, then continues while the condition matches:</p>
<pre class="dz"><code>let x = 10
do
    print("Runs at least once: ${x}")
    x--
while x > 5
</code></pre>

<h2>For-In Iteration</h2>
<p>Iterate over items in arrays, strings, ranges, or key-value entries in maps:</p>
<pre class="dz"><code># Array iteration
for fruit in ["apple", "banana"]
    print(fruit)
end

# String iteration (character by character)
for char in "Hi"
    print(char)
end

# Range iteration (.. syntax)
for idx in 1..4
    print("Index: ${idx}")
end

# Range iteration (to syntax)
for i in 0 to 3
    print("i: ${i}")
end

# Map iteration (unpacking key, value)
let scores = {"Riad": 95, "Sarah": 99}
for name, score in scores
    print("${name} scored ${score}")
end
</code></pre>

<h2>Break & Continue</h2>
<p>Standard loop directives are fully supported: <code>break</code> immediately terminates the loop, while <code>continue</code> skips to the next iteration:</p>
<pre class="dz"><code>for i in 0..5
    if i == 3
        break  # stops at 3
    end
    if i == 1
        continue  # skips printing 1
    end
    print(i)
end
# Output: 0 2
</code></pre>
"""

PAGES_CONTENT["language-guide/functions.html"] = """
<h1>Functions</h1>
<p>Functions are declared using the <code>fn</code> keyword and terminated with <code>end</code>. They are first-class citizen objects in Djazair.</p>

<h2>Standard Declaration</h2>
<pre class="dz"><code>fn calculateSum(a, b)
    return a + b
end

print(calculateSum(10, 20)) # => 30
</code></pre>

<h2>Default Arguments</h2>
<p>Djazair allows function parameters to have default values, which are evaluated if the argument is omitted:</p>
<pre class="dz"><code>fn greet(name = "Guest", prefix = "Hello")
    return "${prefix}, ${name}!"
end

print(greet())             # => Hello, Guest!
print(greet("Riad", "Hi")) # => Hi, Riad!
</code></pre>

<h2>Rest Parameters</h2>
<p>Collect variable amounts of arguments into a single array using the <code>...</code> syntax prefix:</p>
<pre class="dz"><code>fn printLog(level, ...messages)
    print("[${level}]", messages.join(" "))
end

printLog("INFO", "Server started on", "port", 8080)
# Output => [INFO] Server started on port 8080
</code></pre>

<h2>Arrow Functions & Expressions</h2>
<p>Write compact lambdas using the arrow symbol (<code>=></code>):</p>
<pre class="dz"><code>let square = fn(x) => x * x
print(square(4)) # => 16

# Named function with arrow syntax
fn double(x) => x * 2
print(double(5)) # => 10
</code></pre>

<h2>Closures</h2>
<p>Functions capture their surrounding lexical scope. Inner functions can access and modify outer variables:</p>
<pre class="dz"><code>fn makeCounter()
    let count = 0
    return fn()
        count += 1
        return count
    end
end
let c = makeCounter()
print(c())  # => 1
print(c())  # => 2
print(c())  # => 3
</code></pre>

<h2>Higher-Order Functions</h2>
<p>Pass functions to array methods for transformation, filtering, and reduction:</p>
<pre class="dz"><code>let nums = [1, 2, 3, 4, 5]
print(nums.map(fn(x) => x * 2))       # => [2, 4, 6, 8, 10]
print(nums.filter(fn(x) => x > 2))    # => [3, 4, 5]
print(nums.reduce(fn(a, x) => a + x, 0)) # => 15

# Method chaining
let result = [1, 2, 3, 4, 5]
    .filter(fn(x) => x % 2 == 0)
    .map(fn(x) => x * 10)
    .reduce(fn(acc, x) => acc + x, 0)
print(result) # => 60
</code></pre>

<h2>Async Functions</h2>
<p>Declare asynchronous functions using <code>async fn</code>. They return coroutines that can be awaited:</p>
<pre class="dz"><code>async fn fetchData()
    # Simulate async work
    return 42
end

let task = fetchData()
let result = await task
print(result) # => 42
</code></pre>
"""

PAGES_CONTENT["language-guide/async-await.html"] = """
<h1>Async / Await</h1>
<p>Djazair supports coroutine-based concurrency using <code>async fn</code> and <code>await</code>.</p>

<h2>Async Functions</h2>
<p>Declare with <code>async fn</code>. They return a coroutine instead of executing immediately:</p>
<pre class="dz"><code>async fn fetchData()
    # Simulate async work
    return 42
end

let task = fetchData()
print(task)  # Coroutine object
</code></pre>

<h2>Awaiting Results</h2>
<p>Use <code>await</code> to block until the coroutine completes and get its return value:</p>
<pre class="dz"><code>let result = await task
print(result)  # => 42
</code></pre>

<h2>Multiple Async Calls</h2>
<p>Launch several coroutines and await them:</p>
<pre class="dz"><code>async fn getValue(n)
    return n * 2
end

let t1 = getValue(10)
let t2 = getValue(20)
let r1 = await t1
let r2 = await t2
print(r1 + r2)  # => 60
</code></pre>

<h2>Async Methods in Classes</h2>
<p>Async methods in classes do not use the <code>fn</code> keyword — just <code>async</code> directly:</p>
<pre class="dz"><code>class Fetcher
    async load(id)
        return "data_" + str(id)
    end
end

let f = Fetcher()
let result = await f.load(42)
print(result)  # => "data_42"
</code></pre>

<div class="alert alert-note">
    <p><strong>Note:</strong> Exceptions inside async coroutines propagate when <code>await</code>ed in the parent context.</p>
</div>
"""

PAGES_CONTENT["language-guide/arrays.html"] = """
<h1>Arrays</h1>
<p>Arrays are dynamic, ordered lists. They can hold mixed data types, resize automatically, and feature an extensive collection of utility methods.</p>

<h2>Instantiation</h2>
<pre class="dz"><code>let list = [10, "apple", True, [3, 4]]
print(list[0])    # => 10
print(list[3][1]) # => 4
</code></pre>

<h2>Full Methods Catalog</h2>
<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>length()</code></td><td>Number of elements</td></tr>
        <tr><td><code>append(value)</code></td><td>Add value at end</td></tr>
        <tr><td><code>pop(index?)</code></td><td>Remove and return element (last or at index)</td></tr>
        <tr><td><code>insert(index, val)</code></td><td>Insert at position, shifting elements</td></tr>
        <tr><td><code>remove(value)</code></td><td>Remove first occurrence of value</td></tr>
        <tr><td><code>reverse()</code></td><td>Reverse array <b>in-place</b></td></tr>
        <tr><td><code>reversed()</code></td><td>Return new array in reverse order (original unchanged)</td></tr>
        <tr><td><code>index(value)</code></td><td>Index of value (-1 if not found)</td></tr>
        <tr><td><code>extend(array)</code></td><td>Append all elements from another array</td></tr>
        <tr><td><code>sort(descOrCmp?)</code></td><td>Sort array; accepts bool (descending) or comparator function</td></tr>
        <tr><td><code>sorted(desc?)</code></td><td>Return sorted copy (original unchanged)</td></tr>
        <tr><td><code>copy()</code></td><td>Return shallow copy of array</td></tr>
        <tr><td><code>clear()</code></td><td>Remove all elements</td></tr>
        <tr><td><code>contains(value)</code></td><td>Check if value exists in array</td></tr>
        <tr><td><code>count(value)</code></td><td>Count occurrences of value</td></tr>
        <tr><td><code>concat(other)</code></td><td>Return new array with elements from both</td></tr>
        <tr><td><code>slice(start, end?)</code></td><td>Extract sub-array</td></tr>
        <tr><td><code>join(sep)</code></td><td>Join elements into string with separator</td></tr>
        <tr><td><code>flatten()</code></td><td>Flatten nested arrays one level</td></tr>
        <tr><td><code>unique()</code></td><td>Return new array with duplicate values removed</td></tr>
        <tr><td><code>all()</code></td><td>All elements are truthy</td></tr>
        <tr><td><code>any()</code></td><td>Any element is truthy</td></tr>
        <tr><td><code>min()</code></td><td>Minimum value in array</td></tr>
        <tr><td><code>max()</code></td><td>Maximum value in array</td></tr>
        <tr><td><code>sum()</code></td><td>Sum of all numeric elements</td></tr>
        <tr><td><code>map(callback)</code></td><td>Transform each element, return new array</td></tr>
        <tr><td><code>filter(callback)</code></td><td>Keep elements where callback returns truthy</td></tr>
        <tr><td><code>reduce(callback, init)</code></td><td>Accumulate values into single result</td></tr>
                <tr><td><code>find(value)</code></td><td>Find first element matching value or callback (Null if not found)</td></tr>
        <tr><td><code>every(callback)</code></td><td>Check if all elements pass callback</td></tr>
        <tr><td><code>some(callback)</code></td><td>Check if any element passes callback</td></tr>
    </tbody>
</table>

<h2>Method Chaining Example</h2>
<pre class="dz"><code>let numbers = [1, 2, 3, 4, 5, 6]
let result = numbers
    .filter(fn(x) => x % 2 == 0)
    .map(fn(x) => x * 10)
    .sum()

print(result) # (2*10) + (4*10) + (6*10) => 120
</code></pre>

<h2>Sort Variants</h2>
<pre class="dz"><code>let arr = [5, 1, 9, 3]
arr.sort()                 # ascending: [1, 3, 5, 9]
arr.sort(True)             # descending: [9, 5, 3, 1]
arr.sort(fn(x, y) => y - x) # custom comparator: [9, 5, 3, 1]
</code></pre>
"""

PAGES_CONTENT["language-guide/strings.html"] = """
<h1>Strings</h1>
<p>Djazair Strings are immutable, UTF-8 encoded, and packed with formatting, trimming, and searching APIs.</p>

<h2>String Literals</h2>
<p>Use double quotes for standard strings. Strings support variable interpolation using <code>${expression}</code>:</p>
<pre class="dz"><code>let user = "Riyadh"
let greet = "Hello, ${user}! The time is ${getLine()}"
print(greet)
</code></pre>

<h2>Multiline Strings</h2>
<p>Use backticks (<code>`</code>) to construct multiline blocks. Interpolation operates inside backticks as well:</p>
<pre class="dz"><code>let val = 42
let query = `
    SELECT * 
    FROM users 
    WHERE id = ${val};
`
print(query)
</code></pre>

<h2>String Methods</h2>
<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>length()</code></td><td>Character count</td></tr>
        <tr><td><code>upper()</code></td><td>Uppercase conversion</td></tr>
        <tr><td><code>lower()</code></td><td>Lowercase conversion</td></tr>
        <tr><td><code>strip()</code></td><td>Trim whitespace from both ends</td></tr>
        <tr><td><code>lStrip()</code></td><td>Trim whitespace from left</td></tr>
        <tr><td><code>rStrip()</code></td><td>Trim whitespace from right</td></tr>
        <tr><td><code>contains(substr)</code></td><td>Check if substring exists</td></tr>
        <tr><td><code>count(substr)</code></td><td>Count occurrences of substring</td></tr>
        <tr><td><code>index(needle)</code></td><td>First index of needle (returns -1 if not found)</td></tr>
        <tr><td><code>split(sep?)</code></td><td>Split into array (default: whitespace)</td></tr>
        <tr><td><code>join(list)</code></td><td>Join array elements with this string as separator</td></tr>
        <tr><td><code>slice(start, end?)</code></td><td>Extract substring</td></tr>
        <tr><td><code>subStr(start, length?)</code></td><td>Extract by start and length</td></tr>
        <tr><td><code>replace(old, new)</code></td><td>Replace all occurrences</td></tr>
        <tr><td><code>reverse()</code></td><td>Return reversed string</td></tr>
        <tr><td><code>repeat(n)</code></td><td>Return string repeated n times</td></tr>
        <tr><td><code>zFill(width)</code></td><td>Zero-pad to given width</td></tr>
        <tr><td><code>center(width)</code></td><td>Center string in field of given width</td></tr>
        <tr><td><code>lJust(width)</code></td><td>Left-justify in field of given width</td></tr>
        <tr><td><code>rJust(width)</code></td><td>Right-justify in field of given width</td></tr>
        <tr><td><code>startsWith(prefix)</code></td><td>Check if starts with prefix</td></tr>
        <tr><td><code>endsWith(suffix)</code></td><td>Check if ends with suffix</td></tr>
        <tr><td><code>capitalize()</code></td><td>First character uppercase, rest lowercase</td></tr>
        <tr><td><code>title()</code></td><td>Title case</td></tr>
        <tr><td><code>swapCase()</code></td><td>Swap uppercase/lowercase</td></tr>
        <tr><td><code>charCodeAt(i)</code></td><td>Character code at index</td></tr>
        <tr><td><code>isAlpha()</code></td><td>Check if all alphabetic</td></tr>
        <tr><td><code>isAlnum()</code></td><td>Check if all alphanumeric</td></tr>
        <tr><td><code>isDigit()</code></td><td>Check if all digits</td></tr>
        <tr><td><code>isLower()</code></td><td>Check if all lowercase</td></tr>
        <tr><td><code>isUpper()</code></td><td>Check if all uppercase</td></tr>
        <tr><td><code>isSpace()</code></td><td>Check if all whitespace</td></tr>
        <tr><td><code>concat(...)</code></td><td>Concatenate multiple strings</td></tr>
    </tbody>
</table>

<h2>String Method Examples</h2>
<pre class="dz"><code>let s = "  Hello World  "
print(s.length())          # => 15
print(s.strip())           # => "Hello World"
print(s.upper())           # => "  HELLO WORLD  "
print(s.contains("World")) # => True
print(s.replace("World", "Djazair")) # => "  Hello Djazair  "
print("a,b,c".split(","))  # => ["a", "b", "c"]
print(", ".join(["a", "b", "c"])) # => "a, b, c"
print("hello".index("l"))  # => 2
print("hello".index("x"))  # => -1 (not found)
print("42".zFill(5))       # => "00042"
</code></pre>
"""

PAGES_CONTENT["language-guide/maps.html"] = """
<h1>Maps</h1>
<p>Maps (dictionaries) are unordered key-value hash tables. Keys can be any type.</p>

<h2>Creating Maps</h2>
<pre class="dz"><code>let empty = {}
let user = {"name": "Riad", "age": 30, "active": True}
print(user["name"])  # => Riad
</code></pre>

<h2>Map Methods</h2>
<table>
    <thead><tr><th>Method</th><th>Description</th></tr></thead>
    <tbody>
        <tr><td><code>length()</code></td><td>Number of entries</td></tr>
        <tr><td><code>keys()</code></td><td>Array of keys</td></tr>
        <tr><td><code>values()</code></td><td>Array of values</td></tr>
        <tr><td><code>items()</code></td><td>Array of [key, value] pairs</td></tr>
        <tr><td><code>has(key)</code></td><td>Check if key exists</td></tr>
        <tr><td><code>get(key)</code></td><td>Get value (Null if missing)</td></tr>
        <tr><td><code>copy()</code></td><td>Shallow copy of map</td></tr>
        <tr><td><code>clear()</code></td><td>Remove all entries</td></tr>
        <tr><td><code>pop(key)</code></td><td>Remove key and return value</td></tr>
        <tr><td><code>setDefault(k, v)</code></td><td>Set only if key missing</td></tr>
        <tr><td><code>update(other)</code></td><td>Merge entries from another map</td></tr>
    </tbody>
</table>

<h2>Examples</h2>
<pre class="dz"><code>let m = {"a": 1, "b": 2}
print(m.length())          # => 2
print(m.has("a"))          # => True
print(m.keys())            # => ["a", "b"]
print(m.values())          # => [1, 2]
print(m.get("a"))          # => 1
print(m.get("x"))          # => Null
m.setDefault("c", 3)       # adds {"c": 3}
print(m.pop("a"))          # => 1  (removes "a")
m.update({"d": 4})         # adds {"d": 4}
</code></pre>

<h2>Iteration</h2>
<pre class="dz"><code>for key, value in {"name": "John", "age": 30}
    print("${key}: ${value}")
end
</code></pre>
"""

PAGES_CONTENT["language-guide/modules.html"] = """
<h1>Modules & Imports</h1>
<p>Organize and scale your application by breaking it down into discrete script files or leveraging standard libraries.</p>

<h2>Local Files (import)</h2>
<p>Import local script files using the <code>import</code> keyword. You can assign a namespace or use wildcard imports:</p>
<pre class="dz"><code># main.dz
import "utils.dz" as utils    # Namespaced import
import "helpers.dz" as *       # Wildcard (all names in global scope)

print(utils.calculateTax(500))
print(squareVal(9)) # imported via wildcard
</code></pre>

<h2>Standard Libraries (use)</h2>
<p>Load built-in system standard libraries using the <code>use</code> keyword:</p>
<pre class="dz"><code>use math
use json

print(math.sqrt(64)) # => 8
print(json.stringify({"status": "active"}))
</code></pre>

<h2>Namespace Aliases</h2>
<p>Customize namespace aliases to prevent naming collisions. Wildcard (<code>*</code>) also works with <code>use</code>:</p>
<pre class="dz"><code>use net as connection
# Now access networking sockets via connection.*

use math as *   # Import math functions into global scope
print(sqrt(64)) # => 8  (no "math." prefix needed)
</code></pre>

<h2>Nested Module Paths</h2>
<p>Access sub-modules using the <code>::</code> separator:</p>
<pre class="dz"><code>use http
# Access nested modules
http::client::get(...)
http::server::createServer(...)
</code></pre>
"""

PAGES_CONTENT["language-guide/classes.html"] = """
<h1>Classes & OOP</h1>
<p>Djazair implements fully featured Object-Oriented programming including classes, constructors, methods, and single inheritance.</p>

<h2>Class Declaration</h2>
<p>Declare classes, instantiate objects, and refer to properties inside methods via the <code>self</code> prefix:</p>
<pre class="dz"><code>class User
    init(name, email)
        self.name = name
        self.email = email
    end

    describe()
        return "${self.name} &lt;${self.email}&gt;"
    end
end

let admin = User("Riad", "riad@djazair.org")
print(admin.describe())
</code></pre>

<h2>Inheritance</h2>
<p>Inherit classes using the <code>is</code> keyword. Override parent functions and trigger parent constructors using the <code>super</code> namespace keyword:</p>
<pre class="dz"><code>class Staff is User
    init(name, email, role)
        super.init(name, email)
        self.role = role
    end

    describe()
        return "${super.describe()} [Role: ${self.role}]"
    end
end

let mod = Staff("Sara", "sara@djazair.org", "Moderator")
print(mod.describe())
</code></pre>
"""

PAGES_CONTENT["language-guide/error-handling.html"] = """
<h1>Error Handling</h1>
<p>Runtime faults are caught and mitigated gracefully via structured exception blocks.</p>

<h2>Try-Catch-Finally Blocks</h2>
<p>The error handling block uses <code>try</code>, <code>catch [variable]</code>, <code>finally</code>, and finishes with <code>end</code>:</p>
<pre class="dz"><code>try
    let num = 1 / 0
catch error
    print("Caught an error: " + str(error))
finally
    print("Cleanup: This block always executes.")
end
</code></pre>

<h2>Try-Finally (No Catch)</h2>
<p>You can omit the <code>catch</code> block and just use <code>try/finally</code> for resource cleanup:</p>
<pre class="dz"><code>try
    let f = "file_handle"
    # use resource...
finally
    print("cleaned")
end
</code></pre>

<h2>Finally with Return</h2>
<p>The <code>finally</code> block runs even when a <code>return</code> statement is executed in the <code>try</code> block:</p>
<pre class="dz"><code>fn testReturn()
    try
        return 42
    finally
        print("cleanup runs before return")
    end
end
print(testReturn()) # prints "cleanup runs before return" then 42
</code></pre>

<h2>Nested Try-Catch Order</h2>
<p>When nesting try-catch blocks, the inner catch handles the error first. If it re-throws, the outer catch handles it:</p>
<pre class="dz"><code>try
    try
        throw "inner error"
    catch e
        print("Inner caught: ${e}")
        throw e  # re-throw to outer
    end
catch e
    print("Outer caught: ${e}")
end
</code></pre>

<h2>Throwing Exceptions</h2>
<p>Raise custom errors using the <code>throw</code> keyword. You can throw simple strings or complex payload Maps:</p>
<pre class="dz"><code>fn validateAge(age)
    if age < 0
        throw {"error": "InvalidAge", "message": "Age cannot be negative"}
    end
end

try
    validateAge(-1)
catch err
    print("Error Code: " + err["error"]) # => InvalidAge
end
</code></pre>


"""

# Standard Library Pages
# Examples pages
PAGES_CONTENT["examples/hello-world.html"] = """
<h1>Example: Hello World</h1>
<p>A simple printing execution showing standard Djazair outputs:</p>
<pre class="dz"><code># The hello world program
print("Hello World from Djazair!")
</code></pre>
<h2>How it Works</h2>
<p>The code uses the global built-in <code>print()</code> function to write text streams directly to the terminal stdout. Lines starting with <code>#</code> represent single-line comments.</p>
"""

PAGES_CONTENT["examples/calculator.html"] = """
<h1>Example: Calculator</h1>
<p>An interactive command line calculator script:</p>
<pre class="dz"><code>print("--- Djazair CLI Calculator ---")
print("Enter calculation mode or type 'exit' to quit.")

while True
    let inputStr = input("calc> ")
    if inputStr == "exit"
        break
    end
    
    # Simple evaluation split
    let parts = inputStr.split(" ")
    if parts.length() < 3
        print("Invalid syntax. Format: [number] [operator] [number]")
        continue
    end
    
    let a = num(parts[0])
    let op = parts[1]
    let b = num(parts[2])
    let result = 0
    
    if op == "+"
        result = a + b
    elif op == "-"
        result = a - b
    elif op == "*"
        result = a * b
    elif op == "/"
        if b == 0
            print("Error: division by zero!")
            continue
        end
        result = a / b
    else
        print("Unknown operator: " + op)
        continue
    end
    
    print("Result: ${result}")
end
</code></pre>
"""

PAGES_CONTENT["examples/todo-app.html"] = """
<h1>Example: Todo Application</h1>
<p>A terminal Todo list manager featuring file persistence:</p>
<pre class="dz"><code>use file
use json

let todoFile = "todos.json"
let todos = []

if file.exists(todoFile)
    todos = json.parse(file.read(todoFile))
end

fn saveTodos()
    file.write(todoFile, json.stringify(todos))
end

while True
    print("\\n1. View List")
    print("2. Add Todo")
    print("3. Delete Todo")
    print("4. Exit")
    
    let choice = input("Choose option: ")
    
    if choice == "1"
        print("\\n--- Current Todos ---")
        for idx, item in enumerate(todos)
            print("${idx + 1}. [ ] ${item}")
        end
    elif choice == "2"
        let entry = input("Enter Todo task: ")
        todos.append(entry)
        saveTodos()
        print("Task added!")
    elif choice == "3"
        let deleteIdx = num(input("Enter task number to delete: ")) - 1
        if deleteIdx >= 0 and deleteIdx < todos.length()
            todos.remove(todos[deleteIdx])
            saveTodos()
            print("Task deleted!")
        else
            print("Invalid index.")
        end
    elif choice == "4"
        break
    end
end
</code></pre>
"""

PAGES_CONTENT["examples/file-processing.html"] = """
<h1>Example: File Processing</h1>
<p>A script that parses a log file and extracts formatted records:</p>
<pre class="dz"><code>use file
use regex

let logFile = "app.log"
if not file.exists(logFile)
    # Seed dummy log
    file.write(logFile, "[INFO] Started\\n[ERROR] DB Connection failed\\n[INFO] Retrying\\n")
end

let pattern = regex.compile("\\\\[(INFO|ERROR)\\\\] (.*)")
let lines = file.readLines(logFile)

for idx, line in enumerate(lines)
    let match = pattern.search(line)
    if !isNull(match)
        let level = match.group(1)
        let msg = match.group(2)
        print("Line ${idx + 1}: [${level}] - Message: ${msg}")
    end
end
</code></pre>
"""

# Reference Pages
PAGES_CONTENT["reference/embedding.html"] = """
<h1>Embedding Djazair in C/C++</h1>
<p>Djazair is designed to be easily embedded into C/C++ applications via a single header <code>djazair.h</code>.</p>

<h2>Minimal Example</h2>
<pre class="c"><code>#include "djazair.h"
#include &lt;stdio.h&gt;

int main() {
    // Create a new VM instance
    djazair_vm* vm = djazair_new_vm();
    
    // Execute a script file
    djazair_execute_file(vm, "script.dz");
    
    // Execute inline code
    djazair_execute_string(vm, "print('Hello from C!')");
    
    // Cleanup
    djazair_free_vm(vm);
    return 0;
}
</code></pre>

<h2>Multiple VM Instances</h2>
<p>You can create multiple isolated VM instances concurrently:</p>
<pre class="c"><code>djazair_vm* vm1 = djazair_new_vm();
djazair_vm* vm2 = djazair_new_vm();

// Each VM has its own state
djazair_execute_string(vm1, "let x = 42");
djazair_execute_string(vm2, "let x = 100"); // independent
</code></pre>

<h2>Callback Registration</h2>
<p>Register C functions callable from Djazair:</p>
<pre class="c"><code>void my_log(djazair_vm* vm, djazair_args* args) {
    const char* msg = djazair_get_arg_string(args, 0);
    printf("[Djazair Log] %s\\n", msg);
}

// Register the callback
djazair_register_function(vm, "logMessage", my_log);
</code></pre>
<p>Then call from Djazair:</p>
<pre class="dz"><code>logMessage("Hello from Djazair!") # calls C callback
</code></pre>

<h2>API Functions</h2>
<ul>
    <li><code>djazair_new_vm()</code> - Create a new VM instance.</li>
    <li><code>djazair_free_vm(vm)</code> - Destroy VM and free resources.</li>
    <li><code>djazair_execute_file(vm, path)</code> - Execute a script file.</li>
    <li><code>djazair_execute_string(vm, code)</code> - Execute inline code.</li>
    <li><code>djazair_register_function(vm, name, callback)</code> - Register C callback.</li>
    <li><code>djazair_get_arg_string(args, index)</code> - Get string argument.</li>
    <li><code>djazair_get_arg_number(args, index)</code> - Get number argument.</li>
    <li><code>djazair_set_std_lib_path(vm, path)</code> - Set standard library path.</li>
</ul>
"""

PAGES_CONTENT["faq.html"] = """
<h1>Frequently Asked Questions</h1>

<h2>1. Is Djazair compiled or interpreted?</h2>
<p>Djazair features a hybrid design inspired by modern byte-oriented engines. The compiler parses your code, resolves scopes, compiles variables and functions into streamlined bytecode instruction chunks, and executes them on a fast virtual stack-based VM.</p>

<h2>2. How does the memory management work?</h2>
<p>Djazair features an automated Mark-and-Sweep garbage collector (GC). Local allocations, strings, dynamic array buffers, map nodes, closures, and object instances are tracked dynamically. The garbage collector triggers automatically once memory usage thresholds are crossed.</p>

<h2>3. Can I use Djazair within C applications?</h2>
<p>Absolutely! Djazair is designed to be easily embeddable. A single include header <code>djazair.h</code> provides all API bindings to instantiate multiple isolated VM stacks, pass command-line arguments, set search folders, register custom callback logs, and execute file routines.</p>

<h2>4. What concurrency paradigms does Djazair implement?</h2>
<p>Djazair utilizes coroutines. Asynchronous functions declared with <code>async fn</code> return coroutine pointers. Invoking <code>await [coroutine]</code> yields evaluation control back to the VM scheduler, allowing concurrent non-blocking execution streams.</p>

<h2>5. Does the ternary operator need an end keyword?</h2>
<p>No. The ternary <code>if condition ? value else value</code> does not use an <code>end</code> keyword. Only block-level constructs like <code>if/elif/else/end</code> require <code>end</code>.</p>

<h2>6. What does string.index() return on not found?</h2>
<p>The <code>index()</code> method returns <code>-1</code> when the substring is not found — not <code>Null</code>. Check the return value with <code>== -1</code>, not <code>isNull()</code>.</p>

<h2>7. What is the difference between split() and split("")?</h2>
<p><code>split()</code> without arguments splits on whitespace and removes empty tokens. <code>split("")</code> splits on every empty position, effectively returning an array of individual characters.</p>
"""


# Build search index once
def build_search_index():
    def strip_html(text):
        return re.sub(r'<[^>]+>', '', text).strip()
    index = []
    for page in FLAT_PAGES:
        raw = PAGES_CONTENT.get(page["path"], "")
        index.append({
            "title": page["title"],
            "path": page["path"],
            "description": page["description"],
            "text": strip_html(raw)[:300]
        })
    return json.dumps(index, ensure_ascii=False)

SEARCH_INDEX_JSON = build_search_index()

# Function to generate individual pages
def generate_all_pages():
    for page in FLAT_PAGES:
        file_path = page["path"]
        title = page["title"]
        desc = page["description"]
        
        # Only regenerate pages that have content in PAGES_CONTENT
        # (preserves manually crafted HTML for reference/ and standard-library/)
        if file_path not in PAGES_CONTENT:
            continue
        
        # Calculate relative prefix
        root_prefix = get_root_prefix(file_path)
        
        # Determine top navigation active classes
        active_home = 'class="active"' if file_path == 'index.html' else ''
        active_getting = 'class="active"' if file_path.startswith('getting-started/') else ''
        active_guide = 'class="active"' if file_path.startswith('language-guide/') else ''
        active_std = 'class="active"' if file_path.startswith('standard-library/') else ''
        active_examples = 'class="active"' if file_path.startswith('examples/') else ''
        active_ref = 'class="active"' if file_path.startswith('reference/') else ''
        active_faq = 'class="active"' if file_path == 'faq.html' else ''

        # Sidebar navigation compilation
        sidebar_html = []
        for section in STRUCTURE:
            sidebar_html.append(f'<div class="sidebar-section">')
            sidebar_html.append(f'  <div class="sidebar-title">{section["category"]}</div>')
            sidebar_html.append(f'  <ul class="sidebar-links">')
            for p in section["pages"]:
                active_page = 'class="active"' if p["path"] == file_path else ''
                link_href = f'{root_prefix}{p["path"]}'
                has_subs = "subs" in p and len(p["subs"]) > 0
                if has_subs:
                    expanded = 'true' if p["path"] == file_path else 'false'
                    link_class = 'submenu-toggle active' if active_page else 'submenu-toggle'
                    sidebar_html.append(f'    <li class="has-submenu"><a href="{link_href}" class="{link_class}" onclick="toggleSubmenu(event, this)">{p["title"]} <span class="arrow">{">" if p["path"] != file_path else "v"}</span></a>')
                    sidebar_html.append(f'      <ul class="submenu" data-expanded="{expanded}">')
                    for sub in p["subs"]:
                        sub_href = f'{root_prefix}{p["path"]}#{sub["anchor"]}'
                        sidebar_html.append(f'        <li><a href="{sub_href}" class="sub-link">{sub["title"]}</a></li>')
                    sidebar_html.append(f'      </ul>')
                    sidebar_html.append(f'    </li>')
                else:
                    sidebar_html.append(f'    <li><a href="{link_href}" {active_page}>{p["title"]}</a></li>')
            sidebar_html.append(f'  </ul>')
            sidebar_html.append(f'</div>')
        sidebar_nav = '\n'.join(sidebar_html)

        # Breadcrumbs construction
        breadcrumbs_list = []
        breadcrumbs_list.append(f'<a href="{root_prefix}index.html">Home</a>')
        if '/' in file_path:
            cat_folder = file_path.split('/')[0]
            # Match folder to clean category name
            cat_name = ""
            for s in STRUCTURE:
                if s["pages"][0]["path"].startswith(cat_folder + '/'):
                    cat_name = s["category"]
                    break
            if cat_name:
                breadcrumbs_list.append(f'<span class="separator">/</span>')
                breadcrumbs_list.append(f'<span>{cat_name}</span>')
        breadcrumbs_list.append(f'<span class="separator">/</span>')
        breadcrumbs_list.append(f'<span class="active">{title}</span>')
        breadcrumbs = '\n'.join(breadcrumbs_list)

        # Main content body
        raw_body = PAGES_CONTENT[file_path]
        processed_body = process_code_blocks(raw_body)

        # Compute Table of Contents (TOC) dynamically by parsing H2 and H3 tags
        h2_h3_pattern = r'<(h2|h3)>(.*?)</\1>'
        toc_items = []
        
        # We also need to inject id tags dynamically into the body headings
        headings_map = []
        def heading_replacer(match):
            tag = match.group(1)
            text = match.group(2)
            anchor = re.sub(r'[^a-zA-Z0-9]', '-', text.lower()).strip('-')
            headings_map.append((tag, text, anchor))
            return f'<{tag} id="{anchor}">{text}</{tag}>'
            
        modified_body = re.sub(h2_h3_pattern, heading_replacer, processed_body)
        
        for tag, text, anchor in headings_map:
            indent_class = 'indent-2' if tag == 'h3' else ''
            toc_items.append(f'<li class="{indent_class}"><a href="#{anchor}">{text}</a></li>')
            
        if not toc_items:
            toc_items.append('<li><a href="#">Back to top</a></li>')
            
        toc_html = '\n'.join(toc_items)

        # Page navigation calculation (Previous / Next)
        page_idx = -1
        for idx, item in enumerate(FLAT_PAGES):
            if item["path"] == file_path:
                page_idx = idx
                break
                
        prev_card = ""
        next_card = ""
        
        if page_idx > 0:
            prev_page = FLAT_PAGES[page_idx - 1]
            prev_card = f"""
            <a href="{root_prefix}{prev_page["path"]}" class="nav-card">
                <span class="nav-label">Previous</span>
                <span class="nav-title">{prev_page["title"]}</span>
            </a>
            """
        else:
            prev_card = "<div></div>" # empty spacer
            
        if page_idx < len(FLAT_PAGES) - 1:
            next_page = FLAT_PAGES[page_idx + 1]
            next_card = f"""
            <a href="{root_prefix}{next_page["path"]}" class="nav-card next">
                <span class="nav-label">Next</span>
                <span class="nav-title">{next_page["title"]}</span>
            </a>
            """
        else:
            next_card = "<div></div>"
            
        page_nav_html = prev_card + next_card

        # Render final layout string
        rendered_html = LAYOUT.format(
            description=desc,
            title=title,
            root_prefix=root_prefix,
            active_home=active_home,
            active_getting=active_getting,
            active_guide=active_guide,
            active_std=active_std,
            active_examples=active_examples,
            active_ref=active_ref,
            active_faq=active_faq,
            sidebar=sidebar_nav,
            breadcrumbs=breadcrumbs,
            content=modified_body,
            page_nav=page_nav_html,
            toc_items=toc_html,
            search_index_json=SEARCH_INDEX_JSON
        )

        # Create target directories
        target_file_path = os.path.join(BASE_DIR, file_path)
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
            
    print("Static website generated successfully!")

if __name__ == "__main__":
    generate_all_pages()
