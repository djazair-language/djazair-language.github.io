"""
Content generators for Getting Started section.
"""

def get_getting_started_pages():
    pages = {}

    # 1. Introduction
    pages["docs/getting-started/index.html"] = '''
<h1 id="introduction">Introduction to Djazair</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  <strong>Djazair</strong> is a modern, expressive, lightweight scripting language inspired by the vibrant spirit of North Africa. Built from the ground up in ANSI C, it seamlessly combines the intuitive elegance of high-level dynamic languages with the raw performance and low memory footprint of a compact bytecode virtual machine.
</p>

<div class="callout callout-tip">
  <div class="callout-title"><i class="fa-solid fa-lightbulb"></i> Why Djazair?</div>
  <p>Djazair was engineered to solve a common dilemma: developers shouldn't have to choose between developer happiness and execution efficiency. It offers first-class functions, closures, class-based object-oriented programming, pattern matching, native Unicode support, and a complete 20-module standard library—all inside an engine that embeds into any C or C++ application in less than 20 lines of code.</p>
</div>

<h2 id="core-philosophy">Core Architectural Philosophy</h2>
<ul>
  <li><strong>Clean, Readable Syntax:</strong> No cryptic semicolons or braces cluttering your logic. Blocks use familiar, expressive keywords like <code>fn ... end</code>, <code>class ... end</code>, and <code>if ... end</code>.</li>
  <li><strong>Bytecode Virtual Machine (VM):</strong> Single-pass compilation from source code directly into optimized bytecode instructions, executed by an efficient stack-based C virtual machine.</li>
  <li><strong>Exact Garbage Collection:</strong> Automatic memory management with mark-and-sweep garbage collection, ensuring developers never have to worry about manual memory leaks.</li>
  <li><strong>Uncompromising Unicode UTF-8:</strong> Variables, function identifiers, strings, and looping constructs treat multi-byte UTF-8 sequences (including Arabic characters and emojis) as first-class citizens.</li>
  <li><strong>Actor-Model Concurrency:</strong> True parallel execution using native OS threads with actor-style message passing, isolating state and preventing race conditions without complex mutex locking.</li>
</ul>

<h2 id="quick-glance">Djazair at a Glance</h2>
<p>Here is a snippet showcasing variable declarations, first-class functions, string interpolation, and collection operations:</p>

<pre><code class="language-dz"># A quick taste of Djazair
fn createMultiplier(factor)
    return fn(number) => number * factor
end

let double = createMultiplier(2)
let numbers = [1, 2, 3, 4, 5]

# Functional transformation with map and filter
let doubledOdds = numbers
    .filter(fn(n) => n % 2 != 0)
    .map(double)

print("Doubled odd numbers: ${doubledOdds}")
# => Doubled odd numbers: [2, 6, 10]
</code></pre>

<h2 id="features-summary">Feature Summary</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Capability</th>
        <th>Specification</th>
        <th>Highlights</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Typing System</strong></td>
        <td>Dynamic with strong runtime contracts</td>
        <td>Int, Float, String, Bool, Null, Array, Map, Function, Range, Class</td>
      </tr>
      <tr>
        <td><strong>Unicode</strong></td>
        <td>First-Class 100% UTF-8</td>
        <td>Arabic identifiers (e.g. <code>let السرعة = 100</code>), logical code-point indexing</td>
      </tr>
      <tr>
        <td><strong>Functions</strong></td>
        <td>First-Class Citizens & Closures</td>
        <td>Default arguments, rest parameters (<code>...args</code>), arrow expressions (<code>=&gt;</code>)</td>
      </tr>
      <tr>
        <td><strong>Object-Oriented</strong></td>
        <td>Class-based with Single Inheritance</td>
        <td><code>class ... is ...</code>, <code>super</code>, <code>self</code>, <code>new</code>, <code>instanceof</code></td>
      </tr>
      <tr>
        <td><strong>Concurrency</strong></td>
        <td>Actor Model / Worker Threads</td>
        <td>Worker threads with <code>send()</code>, <code>receive()</code>, and structured JSON messaging</td>
      </tr>
      <tr>
        <td><strong>Standard Library</strong></td>
        <td>20 Built-in Standard Modules</td>
        <td>http, net, json, crypto, regex, datetime, file, dir, process, thread, etc.</td>
      </tr>
      <tr>
        <td><strong>Embeddable</strong></td>
        <td>Pure C Header (<code>djazair.h</code>)</td>
        <td>Zero external hard runtime dependencies; embeds anywhere in seconds</td>
      </tr>
    </tbody>
  </table>
</div>
'''

    # 2. Installation
    pages["docs/getting-started/installation.html"] = '''
<h1 id="installation">Installing & Building Djazair</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair is crafted to compile cleanly and rapidly on <strong>Linux</strong>, <strong>macOS</strong>, and <strong>Windows</strong> with virtually zero external build dependencies.
</p>

<h2 id="prerequisites">Prerequisites</h2>
<p>To compile the Djazair interpreter and its command-line tools, you need:</p>
<ul>
  <li>A standard C99 (or newer) compiler: <strong>GCC</strong> or <strong>Clang</strong>.</li>
  <li>GNU <strong>Make</strong> (or MinGW Make on Windows).</li>
  <li><strong>Windows only:</strong> <code>libregex</code> (provided via MSYS2 / MinGW-w64 as <code>mingw-w64-x86_64-libgnurx</code>).</li>
</ul>

<h2 id="linux-macos">Building on Linux & macOS</h2>
<p>Open your terminal and clone the repository, then run <code>make</code>:</p>

<pre><code class="language-bash"># 1. Clone the repository
git clone https://github.com/djazair-language/djazair.git
cd djazair

# 2. Build the interpreter (extremely fast, ~2-4 seconds)
make

# 3. Verify the executable
./build/bin/djazair -v
# Output: Djazair Programming Language v1.1.0
</code></pre>

<div class="callout callout-note">
  <div class="callout-title"><i class="fa-solid fa-circle-info"></i> System-wide Installation (Optional)</div>
  <p>To install the <code>djazair</code> executable into your standard binary path (<code>/usr/local/bin</code>), execute:</p>
  <pre><code class="language-bash">sudo make install</code></pre>
</div>

<h2 id="windows">Building on Windows</h2>
<p>Djazair includes an automated build script written in PowerShell that configures the build, links with MinGW, and automatically registers the binary directory in your system environment PATH.</p>

<pre><code class="language-powershell"># 1. Clone the repository
git clone https://github.com/djazair-language/djazair.git
cd djazair

# 2. Execute the automated PowerShell build script
powershell -ExecutionPolicy Bypass -File .\\tools\\build.ps1

# 3. Test the built executable
.\\build\\bin\\djazair.exe -v
</code></pre>

<div class="callout callout-warning">
  <div class="callout-title"><i class="fa-solid fa-triangle-exclamation"></i> MinGW-w64 Dependency Note</div>
  <p>If you encounter a linker error regarding missing regex symbols (<code>regcomp</code>, <code>regexec</code>) on Windows, ensure that <code>libgnurx</code> is installed in your MSYS2 / MinGW environment using:</p>
  <pre><code class="language-bash">pacman -S mingw-w64-x86_64-libgnurx</code></pre>
</div>

<h2 id="build-artifacts">Build Output Structure</h2>
<p>Once compilation completes, the build directory contains:</p>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Artifact Path</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>build/bin/djazair</code> (or <code>.exe</code>)</td>
        <td>The core Djazair standalone interpreter binary.</td>
      </tr>
      <tr>
        <td><code>build/bin/dpm</code> (or <code>.bat</code>)</td>
        <td>The Djazair Package Manager executable utility.</td>
      </tr>
      <tr>
        <td><code>build/bin/libdjazair.a</code></td>
        <td>Static import library for embedding Djazair into C/C++ applications.</td>
      </tr>
      <tr>
        <td><code>build/obj/</code></td>
        <td>Compiled C object files.</td>
      </tr>
    </tbody>
  </table>
</div>
'''

    # 3. First Program
    pages["docs/getting-started/first-program.html"] = '''
<h1 id="first-program">Your First Program</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Let's walk through creating, formatting, and running your very first Djazair application.
</p>

<h2 id="writing-hello-world">Writing "Hello World"</h2>
<p>Create a file named <code>hello.dz</code> in your project directory using any text editor:</p>

<pre><code class="language-dz"># hello.dz — My first script in Djazair
let greeting = "Hello from Djazair!"
print(greeting)
</code></pre>

<h2 id="executing-the-script">Executing the Script</h2>
<p>To run your script, pass the file path to the <code>djazair</code> interpreter:</p>

<pre><code class="language-bash">djazair hello.dz
# Output:
# Hello from Djazair!
</code></pre>

<h2 id="interactive-input">Prompting for User Input</h2>
<p>Djazair provides the built-in <code>input(prompt)</code> function to read text input from the console:</p>

<pre><code class="language-dz"># interactive.dz
let name = input("Enter your name: ")
let city = input("Where are you from? ")

print("Welcome, ${name}! Greetings to everyone in ${city}.")
</code></pre>

<p>When run, the program prompts you in the terminal:</p>
<pre><code class="language-bash">djazair interactive.dz
# Enter your name: Riad
# Where are you from? Algiers
# Welcome, Riad! Greetings to everyone in Algiers.
</code></pre>

<h2 id="comments-syntax">Comments in Djazair</h2>
<p>Documentation is a vital part of every codebase. Djazair supports both single-line and multi-line comments:</p>

<pre><code class="language-dz"># 1. Single-line comment starts with a hash character (#)
let x = 10 # This comment follows code

#*
   2. Multi-line comments are wrapped in #* ... *# blocks.
   They can span across multiple lines and are ideal
   for file headers or detailed algorithmic documentation.
*#
let y = 20
</code></pre>
'''

    # 4. CLI
    pages["docs/getting-started/cli.html"] = '''
<h1 id="cli">Command-Line Interface (CLI)</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>djazair</code> executable includes comprehensive command-line options for executing scripts, evaluating inline code strings, inspecting version info, and disassembling bytecode.
</p>

<h2 id="synopsis">CLI Synopsis</h2>
<pre><code class="language-bash">djazair [options] [script_file.dz] [arguments...]</code></pre>

<h2 id="available-options">Available Command-Line Flags</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Flag</th>
        <th>Description</th>
        <th>Example</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>-c &lt;code&gt;</code></td>
        <td>Executes an inline Djazair code string directly without saving a file.</td>
        <td><code>djazair -c 'print(10 * 4)'</code></td>
      </tr>
      <tr>
        <td><code>-v</code>, <code>--version</code></td>
        <td>Displays the interpreter version, build platform, and compiler information.</td>
        <td><code>djazair -v</code></td>
      </tr>
      <tr>
        <td><code>-h</code>, <code>--help</code></td>
        <td>Prints the help menu and command synopsis.</td>
        <td><code>djazair --help</code></td>
      </tr>
      <tr>
        <td><code>-d</code>, <code>--debug</code></td>
        <td>Enables runtime VM instruction tracing and stack state inspection per opcode.</td>
        <td><code>djazair -d script.dz</code></td>
      </tr>
      <tr>
        <td><code>--disassemble</code></td>
        <td>Disassembles the compiled bytecode chunk into human-readable opcode mnemonics.</td>
        <td><code>djazair --disassemble script.dz</code></td>
      </tr>
    </tbody>
  </table>
</div>

<h2 id="inline-execution">Inline Code Execution (<code>-c</code>)</h2>
<p>The <code>-c</code> option is handy for quick evaluations, shell one-liners, or piping data from command pipelines:</p>

<pre><code class="language-bash"># One-line arithmetic and JSON calculation
djazair -c 'use json; print(json.encode({"status": "healthy", "code": 200}))'
# => {"status":"healthy","code":200}
</code></pre>

<h2 id="script-arguments">Accessing Command-Line Arguments</h2>
<p>Any arguments passed after the script filename are accessible inside your Djazair script via the <code>process.args()</code> standard library function or the global <code>args</code> array:</p>

<pre><code class="language-dz"># args_demo.dz
use process

let cliArgs = process.args()
print("Received ${cliArgs.length()} arguments:")

for idx, arg in enumerate(cliArgs)
    print("  [${idx}]: ${arg}")
end
</code></pre>

<pre><code class="language-bash">djazair args_demo.dz apple banana cherry 42
# Received 4 arguments:
#   [0]: apple
#   [1]: banana
#   [2]: cherry
#   [3]: 42
</code></pre>
'''

    return pages
