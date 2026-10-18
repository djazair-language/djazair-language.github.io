/**
 * Djazair WebAssembly Playground
 * Browser-side driver that wires the Emscripten module to the UI.
 *
 * Standards followed:
 *  - Each run creates a fresh VM (reproducible, no state leakage)
 *  - Execution is synchronous inside the WASM module (no async races)
 *  - Source capped at 64 KiB to keep the browser responsive
 *  - Keyboard accessibility: Ctrl/⌘+Enter to run, Tab inserts 4 spaces
 *  - ARIA live-regions update on every state change
 *  - Execution time is shown in the status bar
 *  - Share button copies a permalink with source encoded in the URL hash
 *  - Ctrl+L clears the output
 *  - Font-size adjustment buttons (A- / A+)
 */
(() => {
  "use strict";

  /* ── Samples ─────────────────────────────────────────────────────────── */
  const SAMPLES = {
    hello: [
      "# Djazair runs directly in your browser",
      'let name = "Djazair"',
      "let version = 1.0",
      'print("Hello from ${name} v${version}!")',
      "",
      "# String formatting & methods",
      'let msg = "Welcome to the modern era of scripting."',
      'print("Uppercase: ${msg.upper()}")',
      'print("Length:    ${msg.length()} chars")',
    ].join("\n"),

    match: [
      "# Pattern Matching with match-case",
      "fn handleResponse(status)",
      "    match status",
      "        case 200, 201, 204",
      '            print("✓ [2xx] Success: Request processed (${status})")',
      "        case 301, 302",
      '            print("➔ [3xx] Redirect: Moved permanently (${status})")',
      "        case 400, 401, 403, 404",
      '            print("✗ [4xx] Client Error: Resource unavailable (${status})")',
      "        case 500, 502, 503",
      '            print("⚠ [5xx] Server Error: Internal failure (${status})")',
      "        default",
      '            print("? Unknown status code: ${status}")',
      "    end",
      "end",
      "",
      "let codes = [200, 301, 404, 500]",
      "for code in codes",
      "    handleResponse(code)",
      "end",
    ].join("\n"),

    closures: [
      "# First-class functions and lexical closures",
      "fn makeCounter(initial, step = 1)",
      "    let count = initial",
      "    fn increment()",
      "        let current = count",
      "        count += step",
      "        return current",
      "    end",
      "    return increment",
      "end",
      "",
      "let counterA = makeCounter(10, 5)",
      "let counterB = makeCounter(100, 10)",
      "",
      'print("Counter A (start 10, step 5):  ${counterA()} -> ${counterA()} -> ${counterA()}")',
      'print("Counter B (start 100, step 10): ${counterB()} -> ${counterB()} -> ${counterB()}")',
    ].join("\n"),

    classes: [
      "# Object-Oriented Programming with Inheritance",
      "class Shape",
      "    init(name, color)",
      "        self.name = name",
      "        self.color = color",
      "    end",
      "",
      "    describe()",
      '        print("[Shape] ${self.color} ${self.name}")',
      "    end",
      "end",
      "",
      "class Circle is Shape",
      "    init(color, radius)",
      '        super.init("Circle", color)',
      "        self.radius = radius",
      "    end",
      "",
      "    area()",
      "        return 3.14159 * self.radius * self.radius",
      "    end",
      "",
      "    describe()",
      "        super.describe()",
      '        print("  Radius: ${self.radius}, Area: ${self.area()}")',
      "    end",
      "end",
      "",
      'let c = new Circle("Emerald Green", 7)',
      "c.describe()",
    ].join("\n"),

    arrays: [
      "# Functional transformations on arrays",
      "let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
      "",
      "let evens = numbers.filter(fn(n) => n % 2 == 0)",
      "let squares = evens.map(fn(n) => n * n)",
      "let sum = squares.reduce(fn(acc, n) => acc + n, 0)",
      "",
      'print("Original:         ${numbers}")',
      'print("Even numbers:     ${evens}")',
      'print("Squares of evens: ${squares}")',
      'print("Sum of squares:   ${sum}")',
    ].join("\n"),

    arabic: [
      "# لغة جزائر تدعم المعرفات والنصوص العربية كعناصر من الدرجة الأولى",
      'let رسالة_ترحيب = "مرحباً بكم في لغة جزائر البرمجية! 🇩🇿 🌍"',
      "let عدد_الطلاب = 45",
      "",
      "fn مضاعفة_العدد(س)",
      "    return س * 2",
      "end",
      "",
      "print(رسالة_ترحيب)",
      'print("العدد الأصلي:       ${عدد_الطلاب}")',
      'print("العدد بعد المضاعفة: ${مضاعفة_العدد(عدد_الطلاب)}")',
      'print("طول النص العربي:    ${رسالة_ترحيب.length()} محرفاً")',
    ].join("\n"),

    exceptions: [
      "# Exception handling with try / catch / finally",
      "fn divide(a, b)",
      "    if b == 0",
      '        throw "Division by zero is undefined!"',
      "    end",
      "    return a / b",
      "end",
      "",
      "let testCases = [",
      "    [10, 2],",
      "    [8, 0],",
      "    [15, 3]",
      "]",
      "",
      "for pair in testCases",
      "    try",
      "        let res = divide(pair[0], pair[1])",
      '        print("✓ ${pair[0]} / ${pair[1]} = ${res}")',
      "    catch e",
      '        print("✗ Caught Exception: ${e}")',
      "    finally",
      '        print("  Finished evaluating pair: ${pair}")',
      "    end",
      "end",
    ].join("\n"),

    fibonacci: [
      "# Fibonacci Sequence (Iterative & Fast)",
      "fn fib(n)",
      "    if n <= 1 return n end",
      "    let a = 0",
      "    let b = 1",
      "    for i in range(2, n + 1)",
      "        let tmp = a + b",
      "        a = b",
      "        b = tmp",
      "    end",
      "    return b",
      "end",
      "",
      'print("Computing first 15 Fibonacci numbers:")',
      "for i in range(0, 15)",
      '    print("  F(${i}) = ${fib(i)}")',
      "end",
    ].join("\n"),

    algorithms: [
      "# Classic Sorting Algorithm: Bubble Sort in Djazair",
      "fn bubbleSort(arr)",
      "    let n = arr.length()",
      "    for i in 0..n - 1",
      "        for j in 0..n - i - 2",
      "            if arr[j] > arr[j + 1]",
      "                let tmp = arr[j]",
      "                arr[j] = arr[j + 1]",
      "                arr[j + 1] = tmp",
      "            end",
      "        end",
      "    end",
      "    return arr",
      "end",
      "",
      "let sample = [64, 34, 25, 12, 22, 11, 90, 5]",
      'print("Unsorted list: ${sample}")',
      "let result = bubbleSort(sample)",
      'print("Sorted list:   ${result}")',
    ].join("\n"),
  };

  /* ── Source size limit (bytes) ────────────────────────────────────────── */
  const MAX_SOURCE_BYTES = 65536; // 64 KiB

  /* ── DOM refs ─────────────────────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", () => {
    const editor     = document.getElementById("playground-editor");
    if (!editor) return; // playground not on this page

    const monacoHost = document.getElementById("playground-monaco");
    let monacoEditor = null;

    const output     = document.getElementById("playground-output");
    const statusEl   = document.getElementById("playground-status");
    const runBtn     = document.getElementById("playground-run");
    const resetBtn   = document.getElementById("playground-reset");
    const copyBtn    = document.getElementById("playground-copy");
    const shareBtn   = document.getElementById("playground-share");
    const clearBtn   = document.getElementById("playground-clear");
    const fontDecBtn = document.getElementById("playground-font-dec");
    const fontIncBtn = document.getElementById("playground-font-inc");

    let wasmModule   = null;
    let fontSize      = 14; // px

    const getSource = () => (monacoEditor ? monacoEditor.getValue() : editor.value);
    const setSource = (code) => {
      if (monacoEditor) {
        monacoEditor.setValue(code);
      } else {
        editor.value = code;
      }
    };

    /* ── Mount Monaco Editor if available ───────────────────────────────── */
    if (typeof window.require === "function" && monacoHost) {
      try {
        window.require.config({ paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs" } });
        window.require(["vs/editor/editor.main"], (monaco) => {
          if (window.MonacoDjazair && typeof window.MonacoDjazair.setup === "function") {
            window.MonacoDjazair.setup(monaco);
          } else {
            monaco.languages.register({ id: 'djazair', extensions: ['.dz', '.djazair'] });
            monaco.editor.defineTheme('djazair-theme', {
              base: 'vs-dark',
              inherit: true,
              rules: [
                { token: 'keyword', foreground: '00e5ff', fontStyle: 'bold' },
                { token: 'string', foreground: 'c3e88d' },
                { token: 'number', foreground: 'f78c6c' },
                { token: 'comment', foreground: '546e7a', fontStyle: 'italic' },
                { token: 'function', foreground: '82aaff', fontStyle: 'bold' }
              ],
              colors: {
                'editor.background': '#0b101e',
                'editor.foreground': '#e2e2e6',
                'editorLineNumber.foreground': '#546e7a',
                'editorLineNumber.activeForeground': '#00e5ff'
              }
            });
          }
          monaco.editor.setTheme("djazair-theme");

          editor.style.display = "none";
          monacoHost.style.display = "block";

          monacoEditor = monaco.editor.create(monacoHost, {
            value: editor.value,
            language: "djazair",
            theme: "djazair-theme",
            fontSize: fontSize,
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace",
            fontLigatures: true,
            automaticLayout: true,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: "on",
            lineNumbersMinChars: 3,
            glyphMargin: false,
            folding: false,
            lineDecorationsWidth: 8,
            renderLineHighlight: "line",
            renderLineHighlightOnlyWhenFocus: false,
            cursorBlinking: "smooth",
            cursorSmoothCaretAnimation: "on",
            smoothScrolling: true,
            tabSize: 4,
            insertSpaces: true,
            padding: { top: 12, bottom: 12 },
            scrollbar: {
              vertical: "visible",
              horizontal: "auto",
              verticalScrollbarSize: 8,
              horizontalScrollbarSize: 8,
              useShadows: false
            },
            overviewRulerBorder: false,
            overviewRulerLanes: 0,
            hideCursorInOverviewRuler: true
          });

          setTimeout(() => {
            if (monacoEditor) monacoEditor.layout();
          }, 50);

          // Ctrl/Cmd + Enter → run
          monacoEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
            run();
          });
        });
      } catch (e) {
        console.warn("Monaco initialization fallback to textarea:", e);
      }
    }

    /* ── Output helpers ─────────────────────────────────────────────────── */
    const write = (text, isError = false) => {
      const span = document.createElement("span");
      span.className = isError ? "playground-output-error" : "playground-output-text";
      span.textContent = text;
      output.appendChild(span);
      output.scrollTop = output.scrollHeight;
    };

    const clearOutput = () => output.replaceChildren();

    /* ── Status helpers ─────────────────────────────────────────────────── */
    const setStatus = (message, state) => {
      statusEl.textContent = message;
      statusEl.dataset.state = state;
    };

    const setControls = (enabled) => {
      runBtn.disabled   = !enabled;
      resetBtn.disabled = !enabled;
      if (shareBtn)  shareBtn.disabled  = !enabled;
      if (clearBtn)  clearBtn.disabled  = false; // always allow clear
    };

    /* ── Host object consumed by WASM ──────────────────────────────────── */
    globalThis.DjazairWasmHost = {
      write,
      input: (promptText) => {
        const val = window.prompt(promptText || "Input:");
        return val !== null ? val : "";
      },
    };

    /* ── Load WASM ──────────────────────────────────────────────────────── */
    setControls(false);
    setStatus("Loading WebAssembly…", "loading");

    const factory = globalThis.DjazairWasm;
    if (typeof factory !== "function") {
      setStatus("WebAssembly bundle unavailable", "error");
      write(
        "The Djazair WebAssembly bundle could not be loaded.\n" +
        "Please refresh the page or check your network connection.\n",
        true
      );
      return;
    }

    factory({ locateFile: (file) => `assets/wasm/${file}` })
      .then((mod) => {
        wasmModule = mod;
        setControls(true);
        setStatus("Ready", "ready");
        write("Djazair WebAssembly is ready. Press Run or Ctrl/⌘ + Enter.\n");
        loadFromHash(); // restore state from URL hash if any
      })
      .catch((err) => {
        setStatus("Failed to initialize WebAssembly", "error");
        write(`Startup error: ${err.message}\n`, true);
      });

    /* ── Run ────────────────────────────────────────────────────────────── */
    const run = () => {
      if (!wasmModule) return;

      const source = getSource();
      const byteLen = new TextEncoder().encode(source).length;

      if (byteLen > MAX_SOURCE_BYTES) {
        clearOutput();
        write(
          `Source is too large (${byteLen} bytes). ` +
          `The playground limit is ${MAX_SOURCE_BYTES / 1024} KiB.\n`,
          true
        );
        return;
      }

      clearOutput();
      setControls(false);
      setStatus("Running…", "running");

      const t0 = performance.now();
      let exitCode;

      try {
        exitCode = wasmModule.ccall(
          "djazair_wasm_run",
          "number",
          ["string"],
          [source]
        );
      } catch (err) {
        write(`Internal runtime error: ${err.message}\n`, true);
        setStatus("Execution crashed", "error");
        setControls(true);
        editor.focus();
        return;
      }

      const elapsed = (performance.now() - t0).toFixed(1);

      if (exitCode === 0 && output.textContent.length === 0) {
        write("Program finished with no output.\n");
      }

      setStatus(
        exitCode === 0
          ? `Completed in ${elapsed} ms`
          : `Completed with errors in ${elapsed} ms`,
        exitCode === 0 ? "ready" : "error"
      );
      setControls(true);
      if (monacoEditor) monacoEditor.focus(); else editor.focus();
    };

    /* ── Reset ──────────────────────────────────────────────────────────── */
    const resetPlayground = () => {
      if (wasmModule) {
        wasmModule.ccall("djazair_wasm_reset", "number", [], []);
      }
      setSource(SAMPLES.hello);
      document.querySelectorAll("[data-playground-sample]").forEach((b) => {
        b.classList.toggle("active", b.dataset.playgroundSample === "hello");
      });
      clearOutput();
      setStatus("Ready", "ready");
      write("Editor and VM reset to initial state. Press Run or Ctrl/⌘ + Enter.\n");
      if (monacoEditor) {
        monacoEditor.focus();
        monacoEditor.setPosition({ lineNumber: 1, column: 1 });
      } else {
        editor.focus();
      }
      // Clear hash
      history.replaceState(null, "", location.pathname + location.search);
    };

    /* ── Share (permalink) ──────────────────────────────────────────────── */
    const share = async () => {
      try {
        const encoded = btoa(unescape(encodeURIComponent(getSource())));
        const url = `${location.origin}${location.pathname}#src=${encoded}`;
        await navigator.clipboard.writeText(url);
        if (shareBtn) {
          const original = shareBtn.innerHTML;
          shareBtn.innerHTML = '<i class="fa-solid fa-check"></i> Link copied!';
          setTimeout(() => { shareBtn.innerHTML = original; }, 2000);
        }
      } catch (_) {
        setStatus("Share is not available in this browser", "error");
      }
    };

    /* ── Load from URL hash ─────────────────────────────────────── */
    const loadFromHash = () => {
      try {
        const hash = location.hash;
        if (!hash.startsWith("#src=")) return;

        let srcPart = hash.slice(5);
        let autoRun = false;
        if (srcPart.includes("&autorun=1")) {
          autoRun = true;
          srcPart = srcPart.replace("&autorun=1", "");
        } else if (srcPart.includes("&autorun=true")) {
          autoRun = true;
          srcPart = srcPart.replace("&autorun=true", "");
        }

        const source = decodeURIComponent(escape(atob(srcPart)));
        setSource(source);
        clearOutput();
        write("// Code snippet loaded into playground.\n");

        document.querySelectorAll("[data-playground-sample]").forEach((b) => b.classList.remove("active"));

        const pg = document.getElementById("playground");
        if (pg) {
          setTimeout(() => {
            pg.scrollIntoView({ behavior: "smooth" });
          }, 120);
        }

        if (autoRun) {
          write("// Executing snippet in WebAssembly VM…\n\n");
          let attempts = 0;
          const tryRun = () => {
            attempts++;
            if (wasmModule) {
              run();
            } else if (attempts < 30) {
              setTimeout(tryRun, 150);
            }
          };
          setTimeout(tryRun, 350);
        } else {
          write("// Press Run or Ctrl/⌘ + Enter to execute.\n");
        }
      } catch (err) {
        console.warn("Could not load source from URL hash:", err);
      }
    };

    window.setPlaygroundSource = (code) => {
      setSource(code);
      document.querySelectorAll("[data-playground-sample]").forEach((b) => b.classList.remove("active"));
      clearOutput();
      write("// Code snippet loaded into playground.\n");
    };

    window.runPlayground = () => {
      run();
    };

    window.addEventListener("hashchange", loadFromHash);

    /* ── Font size ──────────────────────────────────────────────────────── */
    const updateFontIndicator = () => {
      const ind = document.getElementById("playground-font-indicator");
      if (ind) ind.textContent = `${fontSize}px`;
    };

    const applyFontSize = (size) => {
      fontSize = Math.min(22, Math.max(10, size));
      editor.style.fontSize  = `${fontSize}px`;
      output.style.fontSize  = `${fontSize}px`;
      if (monacoEditor) {
        monacoEditor.updateOptions({ fontSize: fontSize });
      }
      updateFontIndicator();
    };

    /* ── Copy output ────────────────────────────────────────────────────── */
    const copyOutput = async () => {
      try {
        await navigator.clipboard.writeText(output.textContent);
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied';
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i> Copy output';
        }, 1800);
      } catch (_) {
        setStatus("Clipboard access denied", "error");
      }
    };

    /* ── Event listeners ────────────────────────────────────────────────── */
    runBtn.addEventListener("click", run);
    resetBtn.addEventListener("click", resetPlayground);
    copyBtn.addEventListener("click", copyOutput);

    if (shareBtn) shareBtn.addEventListener("click", share);
    if (clearBtn) clearBtn.addEventListener("click", () => {
      clearOutput();
      write("// Console cleared. Ready for execution.\n");
      if (monacoEditor) monacoEditor.focus(); else editor.focus();
    });
    if (fontDecBtn) fontDecBtn.addEventListener("click", () => applyFontSize(fontSize - 2));
    if (fontIncBtn) fontIncBtn.addEventListener("click", () => applyFontSize(fontSize + 2));

    /* Sample buttons (data-playground-sample attribute) */
    document.querySelectorAll("[data-playground-sample]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.dataset.playgroundSample;
        if (SAMPLES[key]) {
          document.querySelectorAll("[data-playground-sample]").forEach((b) => b.classList.remove("active"));
          btn.classList.add("active");
          setSource(SAMPLES[key]);
          clearOutput();
          write(`// Loaded sample: ${btn.textContent.trim()}\n// Press Run or Ctrl/⌘ + Enter to execute.\n`);
          if (monacoEditor) {
            monacoEditor.focus();
            monacoEditor.setPosition({ lineNumber: 1, column: 1 });
          } else {
            editor.focus();
          }
        }
      });
    });

    /* Keyboard shortcuts in the editor */
    editor.addEventListener("keydown", (e) => {
      // Ctrl/⌘ + Enter → run
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        run();
        return;
      }
      // Ctrl/⌘ + L → clear output
      if ((e.ctrlKey || e.metaKey) && e.key === "l") {
        e.preventDefault();
        clearOutput();
        return;
      }
      // Tab → insert 4 spaces (instead of moving focus)
      if (e.key === "Tab") {
        e.preventDefault();
        const start = editor.selectionStart;
        const end   = editor.selectionEnd;
        editor.setRangeText("    ", start, end, "end");
      }
    });

    /* Auto-resize editor on input (optional UX improvement) */
    editor.addEventListener("input", () => {
      // Keep at least 290 px; grow with content up to 600 px
      editor.style.height = "auto";
      editor.style.height = Math.min(600, Math.max(290, editor.scrollHeight)) + "px";
    });
  });
})();
