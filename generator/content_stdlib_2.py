"""
Content generators for Standard Library part 2 (lang, math, net, os, path, process, random, regex, thread, uuid).
"""

def get_stdlib_part2_pages():
    pages = {}

    # 1. lang
    pages["docs/standard-library/lang.html"] = '''
<h1 id="lang-module">lang Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>lang</code> module exposes runtime introspection, manual garbage collection triggers, and heap memory statistics directly from the C engine.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use lang</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>lang.gc()</code></td><td>Triggers an immediate garbage collection mark-and-sweep cycle.</td></tr>
      <tr><td><code>lang.memoryUsed()</code></td><td>Returns current heap memory usage in bytes.</td></tr>
      <tr><td><code>lang.version()</code></td><td>Returns the Djazair interpreter version string (e.g. <code>"1.1.0"</code>).</td></tr>
      <tr><td><code>lang.platform()</code></td><td>Returns the target runtime build architecture (e.g. <code>"x86_64"</code>).</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use lang

print("Engine Version: ${lang.version()}")
print("Heap before GC: ${lang.memoryUsed()} bytes")

# Force garbage collection cycle
lang.gc()

print("Heap after GC:  ${lang.memoryUsed()} bytes")
</code></pre>
'''

    # 2. math
    pages["docs/standard-library/math.html"] = '''
<h1 id="math-module">math Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>math</code> module provides mathematical constants, trigonometric operations, logarithms, power functions, statistical aggregations, and number theory utilities.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use math</code></pre>

<h2 id="constants">Mathematical Constants</h2>
<ul>
  <li><code>math.PI</code>: Ratio of circle circumference to diameter (~3.141592653589793).</li>
  <li><code>math.E</code>: Base of natural logarithms (~2.718281828459045).</li>
  <li><code>math.TAU</code>: 2 * PI (~6.283185307179586).</li>
</ul>

<h2 id="functions-catalog">Functions Catalog</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th><th>Example</th></tr>
    </thead>
    <tbody>
      <tr><td><code>math.sqrt(x)</code></td><td>Square root</td><td><code>math.sqrt(16) # => 4.0</code></td></tr>
      <tr><td><code>math.cbrt(x)</code></td><td>Cube root</td><td><code>math.cbrt(27) # => 3.0</code></td></tr>
      <tr><td><code>math.pow(x, y)</code></td><td>x raised to power y</td><td><code>math.pow(2, 10) # => 1024.0</code></td></tr>
      <tr><td><code>math.sin(x)</code> / <code>cos(x)</code> / <code>tan(x)</code></td><td>Trigonometric functions (radians)</td><td><code>math.sin(math.PI / 2) # => 1.0</code></td></tr>
      <tr><td><code>math.log(x)</code> / <code>log10(x)</code> / <code>log2(x)</code></td><td>Logarithms (natural, base-10, base-2)</td><td><code>math.log10(1000) # => 3.0</code></td></tr>
      <tr><td><code>math.ceil(x)</code> / <code>floor(x)</code> / <code>round(x)</code></td><td>Rounding functions</td><td><code>math.ceil(2.1) # => 3</code></td></tr>
      <tr><td><code>math.gcd(a, b)</code></td><td>Greatest Common Divisor</td><td><code>math.gcd(12, 8) # => 4</code></td></tr>
      <tr><td><code>math.lcm(a, b)</code></td><td>Least Common Multiple</td><td><code>math.lcm(4, 6) # => 12</code></td></tr>
      <tr><td><code>math.factorial(n)</code></td><td>Factorial n!</td><td><code>math.factorial(5) # => 120</code></td></tr>
      <tr><td><code>math.clamp(x, min, max)</code></td><td>Restricts x between min and max</td><td><code>math.clamp(15, 0, 10) # => 10</code></td></tr>
      <tr><td><code>math.deg(rad)</code> / <code>rad(deg)</code></td><td>Angle conversions</td><td><code>math.deg(math.PI) # => 180.0</code></td></tr>
    </tbody>
  </table>
</div>
'''

    # 3. net
    pages["docs/standard-library/net.html"] = '''
<h1 id="net-module">net Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>net</code> module offers network communication primitives: TCP clients and servers, UDP sockets, raw sockets, URL parsing, URLSearchParams, DNS resolution, and TLS client connections.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use net</code></pre>

<h2 id="tcp-client-server">TCP Client and Server</h2>
<pre><code class="language-dz">use net

# 1. High-Performance TCP Server (asynchronous Poller)
let server = new net.tcpServer(fn(client, ip, port)
    print("New connection from ${ip}:${port}")
    client.send("Welcome to Djazair TCP Server!\n")
    client.close()
end)

# Start listening on port 9000
server.listen(9000)

# 2. TCP Client
let client = new net.tcpClient()
client.connect("127.0.0.1", 9000)
client.send("Hello Server")
let reply = client.receive()
print("Received: " + reply)
client.close()
</code></pre>

<h2 id="url-parsing">URL Parsing & Query Strings</h2>
<pre><code class="language-dz">use net

let u = net.parseURL("https://api.example.com:8080/v1/users?role=admin&active=true")
print("Host: ${u.hostname}") # => api.example.com
print("Port: ${u.port}")     # => 8080
print("Path: ${u.pathname}") # => /v1/users

# Query Parameters
let params = u.searchParams
print("Role: ${params.get("role")}")       # => admin
print("Active? ${params.has("active")}")   # => True
</code></pre>
'''

    # 4. os
    pages["docs/standard-library/os.html"] = '''
<h1 id="os-module">os Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>os</code> module provides system diagnostics, platform detection, hardware resources (CPU/RAM), and user environment paths.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use os</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>os.platform()</code></td><td>Returns platform name (<code>"windows"</code>, <code>"linux"</code>, <code>"macos"</code>).</td></tr>
      <tr><td><code>os.isWindows()</code> / <code>isLinux()</code> / <code>isMac()</code></td><td>Boolean platform checks.</td></tr>
      <tr><td><code>os.cpuCount()</code></td><td>Number of logical CPU cores available.</td></tr>
      <tr><td><code>os.totalMemory()</code> / <code>freeMemory()</code></td><td>Total and available physical system RAM in bytes.</td></tr>
      <tr><td><code>os.hostname()</code></td><td>Returns network machine hostname.</td></tr>
      <tr><td><code>os.username()</code></td><td>Current logged-in system user.</td></tr>
      <tr><td><code>os.homeDir()</code></td><td>User home directory path.</td></tr>
      <tr><td><code>os.tmpDir()</code></td><td>System temporary directory path.</td></tr>
      <tr><td><code>os.which(binaryName)</code></td><td>Resolves executable path in system PATH (or Null).</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use os

print("OS Platform:  ${os.platform()}")
print("CPU Cores:    ${os.cpuCount()}")
print("Total Memory: ${os.totalMemory() / (1024 * 1024 * 1024)} GB")
print("Temp Dir:     ${os.tmpDir()}")
</code></pre>
'''

    # 5. path
    pages["docs/standard-library/path.html"] = '''
<h1 id="path-module">path Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>path</code> module provides cross-platform filesystem path manipulation, ensuring seamless behavior across Windows (backslashes) and Unix/macOS (forward slashes).
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use path</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function / Constant</th><th>Description</th><th>Example</th></tr>
    </thead>
    <tbody>
      <tr><td><code>path.sep</code></td><td>System path separator (<code>"\\"</code> or <code>"/"</code>).</td><td><code>path.sep</code></td></tr>
      <tr><td><code>path.join(...parts)</code></td><td>Joins path segments with platform separator.</td><td><code>path.join("src", "core", "main.dz")</code></td></tr>
      <tr><td><code>path.dirname(filePath)</code></td><td>Returns parent directory path.</td><td><code>path.dirname("/a/b/c.txt") # => "/a/b"</code></td></tr>
      <tr><td><code>path.basename(filePath, ext?)</code></td><td>Returns file name, optionally stripping extension.</td><td><code>path.basename("/a/b/file.dz", ".dz") # => "file"</code></td></tr>
      <tr><td><code>path.extname(filePath)</code></td><td>Returns file extension including dot.</td><td><code>path.extname("archive.tar.gz") # => ".gz"</code></td></tr>
      <tr><td><code>path.isAbsolute(filePath)</code></td><td>Returns True if path is absolute.</td><td><code>path.isAbsolute("/var/log") # => True</code></td></tr>
      <tr><td><code>path.normalize(filePath)</code></td><td>Resolves <code>.</code> and <code>..</code> segments.</td><td><code>path.normalize("a/b/../c") # => "a/c"</code></td></tr>
    </tbody>
  </table>
</div>
'''

    # 6. process
    pages["docs/standard-library/process.html"] = '''
<h1 id="process-module">process Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>process</code> module enables executing child processes, piping data through standard I/O streams, changing working directories, and inspecting process metadata.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use process</code></pre>

<h2 id="synchronous-exec">Synchronous Execution (<code>process.exec</code>)</h2>
<p>Executes a command synchronously and captures its exit code, stdout, and stderr:</p>

<pre><code class="language-dz">use process

let res = process.exec("git --version")
if res["exit_code"] == 0
    print("Git output: ${res["stdout"].strip()}")
else
    print("Error: ${res["stderr"]}")
end
</code></pre>

<h2 id="asynchronous-spawn">Asynchronous Spawning & Pipes</h2>
<p>For long-running tasks or streaming stdin/stdout:</p>

<pre><code class="language-dz">use process

# Spawn process with pipes
let p = process.spawn("sort")

# Write data into child process stdin
process.write(p["write"], "zebra\napple\nbanana\n")
process.close(p["write"]) # Close stdin to signal EOF

# Wait for completion and read sorted stdout
process.wait(p["pid"])
let sortedOutput = process.read(p["read"])
print("Sorted output:\n${sortedOutput}")
# apple
# banana
# zebra
</code></pre>
'''

    # 7. random
    pages["docs/standard-library/random.html"] = '''
<h1 id="random-module">random Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>random</code> module generates pseudorandom numbers, integers within bounds, random booleans, alphanumeric strings, and performs array shuffling and element selection.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use random</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th><th>Example</th></tr>
    </thead>
    <tbody>
      <tr><td><code>random.float()</code></td><td>Uniform random float in [0.0, 1.0).</td><td><code>random.float()</code></td></tr>
      <tr><td><code>random.int(min, max)</code></td><td>Random integer between min and max (inclusive).</td><td><code>random.int(1, 100)</code></td></tr>
      <tr><td><code>random.bool()</code></td><td>Random boolean (True or False).</td><td><code>random.bool()</code></td></tr>
      <tr><td><code>random.string(length)</code></td><td>Random alphanumeric string of given length.</td><td><code>random.string(16)</code></td></tr>
      <tr><td><code>random.choice(array)</code></td><td>Selects a random element from an array.</td><td><code>random.choice(["A", "B", "C"])</code></td></tr>
      <tr><td><code>random.shuffle(array)</code></td><td>Shuffles array elements in-place.</td><td><code>random.shuffle(cards)</code></td></tr>
      <tr><td><code>random.seed(number)</code></td><td>Initializes PRNG seed for reproducible results.</td><td><code>random.seed(12345)</code></td></tr>
    </tbody>
  </table>
</div>
'''

    # 8. regex
    pages["docs/standard-library/regex.html"] = '''
<h1 id="regex-module">regex Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>regex</code> module provides powerful regular expression pattern matching, substring search, global match collection, replacements, and capture group extraction.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use regex</code></pre>

<h2 id="convenience-functions">Convenience Functions</h2>
<pre><code class="language-dz">use regex

# 1. fullMatch — exact match against full string
let isValidEmail = regex.fullMatch("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", "user@example.com")
print("Valid email? ${isValidEmail != Null}") # => True

# 2. search — finds first substring match
let matched = regex.search("\\d+", "Order #12894 approved")
if matched != Null
    print("Found order ID: ${matched.group(0)}") # => 12894
end

# 3. findAll — collects all occurrences
let words = regex.findAll("[A-Z][a-z]+", "Algiers Oran Constantine Annaba")
print("Cities: ${words}") # => ["Algiers", "Oran", "Constantine", "Annaba"]

# 4. sub — replaces matched patterns
let cleaned = regex.sub("\\s+", " ", "Too   many    spaces")
print(cleaned) # => "Too many spaces"
</code></pre>

<h2 id="compiled-patterns">Compiled Pattern Objects</h2>
<p>For high performance inside loops, pre-compile patterns using <code>regex.compile(pattern, flags?)</code>:</p>

<pre><code class="language-dz">use regex

let phonePattern = regex.compile("(\\+\\d{1,3})\\s+(\\d{9})")
let m = phonePattern.search("Contact: +213 555123456")

if m != Null
    print("Country code: ${m.group(1)}") # => +213
    print("Local number: ${m.group(2)}") # => 555123456
    print("Match span:   ${m.start()} to ${m.endPos()}")
end
</code></pre>
'''

    # 9. thread
    pages["docs/standard-library/thread.html"] = '''
<h1 id="thread-module">thread Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>thread</code> module implements an <strong>Actor-Model concurrency architecture</strong>. Worker threads run isolated bytecode VM instances in parallel OS threads, communicating via message passing.
</p>

<div class="callout callout-tip">
  <div class="callout-title"><i class="fa-solid fa-bolt"></i> Safe, Lock-Free Parallelism</div>
  <p>Because each worker thread operates inside its own isolated VM heap, you never have to worry about data races, mutex deadlocks, or manual memory synchronizations. Communication is handled purely through message passing.</p>
</div>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use thread</code></pre>

<h2 id="worker-lifecycle">Spawning Workers & Message Passing</h2>
<pre><code class="language-dz">use thread

# Spawn a worker executing inline Djazair code
let worker = thread.spawnCode(`
    use thread
    
    # Receive message from parent thread
    let message = thread.receive()
    print("Worker received: " + message)
    
    # Reply back to parent
    thread.reply("Processed: " + message.upper())
`)

# Send message to worker
worker.send("djazair concurrency")

# Receive reply with a 2-second timeout
let response = worker.receive(2.0)
print("Parent received: ${response}")
# => Parent received: Processed: DJAZAIR CONCURRENCY

worker.join()
worker.close()
</code></pre>

<h2 id="json-messaging">Structured JSON Messaging</h2>
<p>Workers can exchange structured dictionaries using <code>sendJson()</code> and <code>receiveJson()</code>:</p>

<pre><code class="language-dz">use thread

let mathWorker = thread.spawnCode(`
    use thread
    let data = thread.receiveJson()
    let result = data["x"] * data["y"]
    thread.replyJson({"answer": result, "status": "ok"})
`)

mathWorker.sendJson({"x": 12, "y": 8})
let res = mathWorker.receiveJson(3.0)
print("Computed answer: ${res["answer"]}") # => 96
mathWorker.close()
</code></pre>
'''

    # 10. uuid
    pages["docs/standard-library/uuid.html"] = '''
<h1 id="uuid-module">uuid Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>uuid</code> module generates cryptographically strong, RFC-4122 compliant Universally Unique Identifiers (UUID Version 4).
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use uuid</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>uuid.v4()</code></td><td>Generates a random UUID v4 string (e.g. <code>"f47ac10b-58cc-4372-a567-0e02b2c3d479"</code>).</td></tr>
      <tr><td><code>uuid.validate(uuidStr)</code></td><td>Validates whether a string matches the standard 36-character UUID format.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use uuid

let newId = uuid.v4()
print("Generated UUID: ${newId}")

print("Is valid? ${uuid.validate(newId)}")   # => True
print("Is valid? ${uuid.validate("invalid")}") # => False
</code></pre>
'''

    return pages
