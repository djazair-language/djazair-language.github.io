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
    ].join("\n"),

    closures: [
      "# Closures capture their enclosing scope",
      "fn makeCounter()",
      "    let count = 0",
      "    fn increment()",
      "        count++",
      "        return count",
      "    end",
      "    return increment",
      "end",
      "",
      "let c = makeCounter()",
      'print("${c()} ${c()} ${c()}")',
    ].join("\n"),

    arabic: [
      "# Arabic and emoji are first-class identifiers",
      'let 🚀_متغير = "مرحبا بالعالم 🌍"',
      "print(🚀_متغير)",
      'print("عدد المحارف: ${🚀_متغير.length()}")',
    ].join("\n"),

    classes: [
      "# Object-oriented programming with inheritance",
      "class Shape",
      "    init(color)",
      "    self.color = color",
      "    end",
      "    describe()",
      '    print("A ${self.color} shape")',
      "    end",
      "end",
      "",
      "class Circle is Shape",
      "    init(color, radius)",
      "    super.init(color)",
      "    self.radius = radius",
      "    end",
      "    describe()",
      '    print("A ${self.color} circle with radius ${self.radius}")',
      "    end",
      "    area()",
      "    return 3.14159 * self.radius * self.radius",
      "    end",
      "end",
      "",
      'let c = new Circle("red", 5)',
      "c.describe()",
      'print("Area: ${c.area()}")',
    ].join("\n"),

    arrays: [
      "# Higher-order array methods",
      "let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]",
      "",
      "let result = numbers",
      "    .filter(fn(n) => n % 2 == 0)",
      "    .map(fn(n) => n * n)",
      "    .reduce(fn(acc, n) => acc + n, 0)",
      "",
      'print("Sum of squares of evens: ${result}")',
      "",
      "# Chained string operations",
      'let words = ["Djazair", "is", "fast", "and", "elegant"]',
      'print(words.filter(fn(w) => w.length() > 3).join(", "))',
    ].join("\n"),

    fibonacci: [
      "# Fibonacci — recursive and iterative",
      "",
      "# Simple recursive",
      "fn fib(n)",
      "    if n <= 1",
      "        return n",
      "    end",
      "    return fib(n - 1) + fib(n - 2)",
      "end",
      "",
      "for i in range(0, 11)",
      '    print("fib(${i}) = ${fib(i)}")',
      "end",
      "",
      "# Iterative (fast for large n)",
      "fn fibIter(n)",
      "    if n <= 1",
      "        return n",
      "    end",
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
      'print("fibIter(30) = ${fibIter(30)}")',
    ].join("\n"),

    exceptions: [
      "# Exception handling with try / catch / finally",
      "fn divide(a, b)",
      "    if b == 0",
      '        throw "Division by zero!"',
      "    end",
      "    return a / b",
      "end",
      "",
      "try",
      "    let result = divide(10, 2)",
      '    print("10 / 2 = ${result}")',
      "    divide(5, 0)  # This will throw",
      "catch e",
      '    print("Caught: ${e}")',
      "finally",
      '    print("Cleanup always runs")',
      "end",
    ].join("\n"),

    interactive: [
      "# Interactive user input using input()",
      'let name = input("Enter your name: ")',
      'let age = input("Enter your age: ")',
      "",
      'print("Welcome, ${name}!")',
      'print("In 5 years, you will be ${num(age) + 5} years old.")',
    ].join("\n"),
  };

  /* ── Source size limit (bytes) ────────────────────────────────────────── */
  const MAX_SOURCE_BYTES = 65536; // 64 KiB

  /* ── DOM refs ─────────────────────────────────────────────────────────── */
  document.addEventListener("DOMContentLoaded", () => {
    const editor     = document.getElementById("playground-editor");
    if (!editor) return; // playground not on this page

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

      const source = editor.value;
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
      editor.focus();
    };

    /* ── Reset ──────────────────────────────────────────────────────────── */
    const resetPlayground = () => {
      if (wasmModule) {
        wasmModule.ccall("djazair_wasm_reset", "number", [], []);
      }
      editor.value = SAMPLES.hello;
      clearOutput();
      setStatus("Ready", "ready");
      write("Editor and VM reset to initial state.\n");
      editor.focus();
      // Clear hash
      history.replaceState(null, "", location.pathname + location.search);
    };

    /* ── Share (permalink) ──────────────────────────────────────────────── */
    const share = async () => {
      try {
        const encoded = btoa(unescape(encodeURIComponent(editor.value)));
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

    /* ── Load from URL hash ─────────────────────────────────────────────── */
    const loadFromHash = () => {
      try {
        const hash = location.hash;
        if (!hash.startsWith("#src=")) return;
        const encoded = hash.slice(5);
        const source = decodeURIComponent(escape(atob(encoded)));
        editor.value = source;
        clearOutput();
        write("Source loaded from shared link. Press Run to execute.\n");
      } catch (_) {
        // Ignore malformed hashes silently
      }
    };

    /* ── Font size ──────────────────────────────────────────────────────── */
    const applyFontSize = (size) => {
      fontSize = Math.min(22, Math.max(10, size));
      editor.style.fontSize  = `${fontSize}px`;
      output.style.fontSize  = `${fontSize}px`;
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
      editor.focus();
    });
    if (fontDecBtn) fontDecBtn.addEventListener("click", () => applyFontSize(fontSize - 2));
    if (fontIncBtn) fontIncBtn.addEventListener("click", () => applyFontSize(fontSize + 2));

    /* Sample buttons (data-playground-sample attribute) */
    document.querySelectorAll("[data-playground-sample]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.dataset.playgroundSample;
        if (SAMPLES[key]) {
          editor.value = SAMPLES[key];
          clearOutput();
          editor.focus();
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
