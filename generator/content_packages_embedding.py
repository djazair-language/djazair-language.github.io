"""
Content generators for Packages, Embedding, Cookbook, and Reference sections.
"""

def get_packages_embedding_pages():
    pages = {}

    # =========================================================================
    # C/C++ EMBEDDING
    # =========================================================================

    pages["docs/embedding/index.html"] = '''
<h1 id="embedding-djazair">Embedding Djazair in C / C++</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair was engineered from day one to be easily embedded inside any host C or C++ application. A single header, <code>#include "djazair.h"</code>, gives your application full scripting superpowers.
</p>

<h2 id="minimal-c-example">Minimal Embed Example (main.c)</h2>
<pre><code class="language-c">#include "djazair.h"
#include <stdio.h>

static void customPrint(const char *text) {
    printf("[Host App] %s", text);
}

int main(int argc, char **argv) {
    /* 1. Configure the VM */
    DjazairConfiguration config;
    djazair_init_configuration(&config);
    config.writeFn = customPrint;

    /* 2. Instantiate isolated VM */
    DjazairVM *vm = djazair_newVM(&config);

    /* 3. Execute Djazair script string */
    djazair_interpret(vm, "print('Hello from embedded Djazair!')");

    /* 4. Execute script file */
    djazair_interpret_file(vm, "game_logic.dz");

    /* 5. Clean up memory */
    djazair_freeVM(vm);
    return 0;
}
</code></pre>

<h2 id="compiling-linking">Compiling & Linking</h2>
<p>Link your C application against the Djazair static library or compiled object files:</p>

<pre><code class="language-bash"># Linux / macOS
gcc -Isrc/include -Isrc/core main.c build/bin/libdjazair.a -lm -lpthread -ldl -o my_app

# Windows (MinGW)
gcc -Isrc/include -Isrc/core main.c build/bin/libdjazair.a -lm -lws2_32 -lregex -o my_app.exe
</code></pre>
'''

    pages["docs/embedding/vm-lifecycle.html"] = '''
<h1 id="vm-lifecycle">VM Lifecycle & Memory Configuration</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Learn how to customize callbacks, manage garbage collection, pass CLI arguments, and isolate multiple concurrent VM instances.
</p>

<h2 id="c-api-table">Core C API Functions</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>C Function</th><th>Return Type</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>djazair_newVM(config)</code></td><td><code>DjazairVM*</code></td><td>Creates a new isolated virtual machine instance.</td></tr>
      <tr><td><code>djazair_freeVM(vm)</code></td><td><code>void</code></td><td>Destroys VM and frees all heap allocations.</td></tr>
      <tr><td><code>djazair_interpret(vm, code)</code></td><td><code>DjazairResult</code></td><td>Executes source code string.</td></tr>
      <tr><td><code>djazair_interpret_file(vm, path)</code></td><td><code>DjazairResult</code></td><td>Executes a <code>.dz</code> script file from disk.</td></tr>
      <tr><td><code>djazair_gc(vm)</code></td><td><code>void</code></td><td>Forces an immediate garbage collection sweep.</td></tr>
      <tr><td><code>djazair_memory_allocated(vm)</code></td><td><code>size_t</code></td><td>Returns current allocated heap size in bytes.</td></tr>
    </tbody>
  </table>
</div>
'''

    pages["docs/embedding/c-extensions.html"] = '''
<h1 id="writing-c-extensions">Writing Native C Extensions</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Extend Djazair with high-performance C libraries using <code>djazair_api.h</code>.
</p>

<h2 id="sample-c-module">Writing a Native C Module</h2>
<pre><code class="language-c">#include "djazair_api.h"

// Define native function: adds two numbers in C
DJAZAIR_FUNC(native_fast_add) {
    djazair_check_args(2);
    double a = djazair_get_num(args, 0);
    double b = djazair_get_num(args, 1);
    return djazair_num(a + b);
}

// Register module exports
DJAZAIR_EXTENSION(fastmath, {
    {"fastAdd", native_fast_add, 2},
    {NULL, NULL, 0}
});
</code></pre>

<p>You can then compile this file to a shared library (<code>fastmath.dll</code> or <code>fastmath.so</code>) and load it seamlessly in Djazair!</p>
'''

    # =========================================================================
    # COOKBOOK
    # =========================================================================

    pages["docs/cookbook/rest-api.html"] = '''
<h1 id="recipe-rest-api">Cookbook: Building a REST API</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  In this practical recipe, we build a complete in-memory CRUD REST API service using Djazair's <code>http</code> and <code>json</code> standard library modules.
</p>

<h2 id="complete-api-code">Complete Server Code</h2>
<pre><code class="language-dz">use http
use json

# In-memory database
let products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mechanical Keyboard", "price": 150}
]
let nextId = 3

let server = new http.Server()

server.handle(fn(req, res)
    res.setHeader("Content-Type", "application/json")

    # GET /api/products
    if req.method == "GET" and req.path == "/api/products"
        res.send(json.encode(products))
        return
    end

    # POST /api/products
    if req.method == "POST" and req.path == "/api/products"
        let payload = json.decode(req.body)
        payload["id"] = nextId
        nextId++
        products.append(payload)
        res.status(201).send(json.encode(payload))
        return
    end

    # 404 Fallback
    res.status(404).send(json.encode({"error": "Route not found"}))
end)

print("Product REST API live at http://localhost:3000")
server.listen(3000)
</code></pre>
'''

    pages["docs/cookbook/cli-tool.html"] = '''
<h1 id="recipe-cli-tool">Cookbook: Building a CLI File Tool</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Build a command-line utility that inspects files, counts lines of code, and outputs a formatted statistics report.
</p>

<h2 id="cli-tool-code">Source Code (loc.dz)</h2>
<pre><code class="language-dz">use dir
use file
use path
use process

let args = process.args()
let targetFolder = if args.length() > 0 ? args[0] else "."

let files = dir.glob(path.join(targetFolder, "**/*.dz"))
let totalLines = 0
let fileCount = files.length()

print("Analyzing ${fileCount} files in ${targetFolder}...\n")

for f in files
    let lines = file.readLines(f)
    let count = lines.length()
    totalLines += count
    print("  ${path.basename(f)}: ${count} lines")
end

print("\n===================================")
print("Total Files: ${fileCount}")
print("Total Lines: ${totalLines}")
print("===================================")
</code></pre>
'''

    pages["docs/cookbook/parallel-workers.html"] = '''
<h1 id="recipe-parallel-workers">Cookbook: Parallel Worker Pool</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Distribute heavy computations across multiple CPU cores using actor worker threads and asynchronous JSON messaging.
</p>

<h2 id="worker-pool-code">Worker Pool Implementation</h2>
<pre><code class="language-dz">use thread
use os

let numWorkers = os.cpuCount()
print("Starting ${numWorkers} parallel workers...")

let workers = []
for i in 0..numWorkers - 1
    let w = thread.spawnCode(`
        use thread
        use math
        
        while True
            let task = thread.receiveJson()
            if task == Null or task["cmd"] == "stop" break end
            
            # Heavy calculation (e.g. factorial)
            let result = math.factorial(int(task["n"]))
            thread.replyJson({"id": task["id"], "result": result})
        end
    `)
    workers.append(w)
end

# Distribute tasks
for i in 1..numWorkers
    let target = workers[i - 1]
    target.sendJson({"id": i, "n": i * 5, "cmd": "work"})
end

# Collect answers
for w in workers
    let reply = w.receiveJson(5.0)
    print("Task #${reply["id"]} calculated: ${reply["result"]}")
    w.sendJson({"cmd": "stop"})
    w.close()
end
</code></pre>
'''

    # =========================================================================
    # REFERENCE
    # =========================================================================

    pages["docs/reference/builtins.html"] = '''
<h1 id="builtins-reference">Built-in Functions Reference</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Complete reference of all globally accessible built-in functions in the Djazair runtime.
</p>

<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Signature</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>print</code></td><td><code>print(...args)</code></td><td>Prints values to console output with spaces between items.</td></tr>
      <tr><td><code>input</code></td><td><code>input(prompt?)</code></td><td>Prompts user for text input in the terminal.</td></tr>
      <tr><td><code>type</code></td><td><code>type(val)</code></td><td>Returns type name string (Int, Float, String, Array, etc.).</td></tr>
      <tr><td><code>str</code></td><td><code>str(val)</code></td><td>Converts value to String representation.</td></tr>
      <tr><td><code>int</code></td><td><code>int(val)</code></td><td>Converts value to signed 32-bit integer.</td></tr>
      <tr><td><code>float</code></td><td><code>float(val)</code></td><td>Converts value to 64-bit float.</td></tr>
      <tr><td><code>bool</code></td><td><code>bool(val)</code></td><td>Evaluates truthiness, returning True or False.</td></tr>
      <tr><td><code>num</code></td><td><code>num(val)</code></td><td>Parses string into Int or Float automatically.</td></tr>
      <tr><td><code>abs</code></td><td><code>abs(number)</code></td><td>Returns absolute value.</td></tr>
      <tr><td><code>round</code></td><td><code>round(num, digits?)</code></td><td>Rounds number to optional decimal places.</td></tr>
      <tr><td><code>range</code></td><td><code>range(start, stop?, step?)</code></td><td>Generates an array containing integer sequence.</td></tr>
      <tr><td><code>enumerate</code></td><td><code>enumerate(arr, start?)</code></td><td>Returns array of [index, item] pairs.</td></tr>
      <tr><td><code>zip</code></td><td><code>zip(...arrays)</code></td><td>Aggregates elements from multiple arrays.</td></tr>
      <tr><td><code>chr</code></td><td><code>chr(codePoint)</code></td><td>Returns character string from Unicode code point.</td></tr>
      <tr><td><code>ord</code></td><td><code>ord(char)</code></td><td>Returns integer Unicode code point of character.</td></tr>
      <tr><td><code>isNull</code></td><td><code>isNull(val)</code></td><td>Returns True if value is Null.</td></tr>
      <tr><td><code>isString</code></td><td><code>isString(val)</code></td><td>Returns True if value is String.</td></tr>
      <tr><td><code>isNumber</code></td><td><code>isNumber(val)</code></td><td>Returns True if value is Int or Float.</td></tr>
      <tr><td><code>isInt</code></td><td><code>isInt(val)</code></td><td>Returns True if value is Int.</td></tr>
      <tr><td><code>isFloat</code></td><td><code>isFloat(val)</code></td><td>Returns True if value is Float.</td></tr>
      <tr><td><code>isBool</code></td><td><code>isBool(val)</code></td><td>Returns True if value is Bool.</td></tr>
      <tr><td><code>isArray</code></td><td><code>isArray(val)</code></td><td>Returns True if value is Array.</td></tr>
      <tr><td><code>isMap</code></td><td><code>isMap(val)</code></td><td>Returns True if value is Map.</td></tr>
      <tr><td><code>isFunction</code></td><td><code>isFunction(val)</code></td><td>Returns True if value is Function.</td></tr>
      <tr><td><code>isClass</code></td><td><code>isClass(val)</code></td><td>Returns True if value is Class.</td></tr>
      <tr><td><code>exit</code></td><td><code>exit(code = 0)</code></td><td>Terminates the current process with exit status code.</td></tr>
      <tr><td><code>getFile</code></td><td><code>getFile()</code></td><td>Returns current script file path.</td></tr>
      <tr><td><code>getDir</code></td><td><code>getDir()</code></td><td>Returns current script directory path.</td></tr>
      <tr><td><code>getLine</code></td><td><code>getLine()</code></td><td>Returns current executing line number.</td></tr>
    </tbody>
  </table>
</div>
'''

    pages["docs/reference/keywords.html"] = '''
<h1 id="keywords-grammar">Keywords & Grammar Reference</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  List of reserved keywords and formal grammar structure in the Djazair language specification.
</p>

<h2 id="reserved-keywords">Reserved Keywords</h2>
<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:2rem;">
  <code>let</code> <code>fn</code> <code>return</code> <code>class</code> <code>init</code> <code>super</code> <code>self</code>
  <code>is</code> <code>instanceof</code> <code>try</code> <code>catch</code> <code>finally</code> <code>throw</code>
  <code>if</code> <code>elif</code> <code>else</code> <code>match</code> <code>case</code> <code>default</code>
  <code>while</code> <code>do</code> <code>for</code> <code>in</code> <code>to</code> <code>break</code> <code>continue</code>
  <code>and</code> <code>or</code> <code>not</code> <code>Null</code> <code>True</code> <code>False</code>
  <code>use</code> <code>import</code> <code>as</code> <code>end</code> <code>new</code> <code>async</code> <code>await</code>
</div>
'''

    pages["docs/reference/cheat-sheet.html"] = '''
<h1 id="cheat-sheet">Djazair Syntax Cheat Sheet</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  A quick-reference guide summarizing syntax, control flow, functions, OOP, and common idioms.
</p>

<h2 id="basics">Basics & Variables</h2>
<pre><code class="language-dz">let x = 10                  # Integer
let pi = 3.14               # Float
let str = "Hello ${x}"      # String interpolation
let multiline = `row 1\nrow 2`
let arr = [1, 2, 3]         # Array
let map = {"key": "val"}    # Map
let isOk = True             # Bool
let empty = Null            # Null
</code></pre>

<h2 id="functions-closures">Functions</h2>
<pre><code class="language-dz"># Standard
fn add(a, b = 1)
    return a + b
end

# Arrow expression
let square = fn(x) => x * x

# Rest params
fn logAll(...items)
    print(items)
end
</code></pre>

<h2 id="control-structures">Control Structures</h2>
<pre><code class="language-dz">let x = 10

# If / Elif / Else
if x > 10
    print("Greater")
elif x == 10
    print("Equal")
else
    print("Smaller")
end

# Match-case
match x
    case 1, 2 print("Few")
    case 10   print("Ten")
    default   print("Other")
end

# For-in loop
for item in [1, 2, 3] print(item) end
for k, v in {"a": 1} print("${k}: ${v}") end
for i in 0..5 print(i) end
</code></pre>

<h2 id="classes-oop">Classes & OOP</h2>
<pre><code class="language-dz">class Animal
    init(name) self.name = name end
    speak() return "Roar" end
end

class Cat is Animal
    init(name, breed)
        super.init(name)
        self.breed = breed
    end
    speak() return "Meow" end
end

let c = new Cat("Luna", "Siamese")
print(c.speak()) # => Meow
print(c instanceof Animal) # => True
</code></pre>
'''

    return pages
