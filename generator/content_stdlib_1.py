"""
Content generators for Standard Library part 1 (assert, bytes, collections, crypto, datetime, dir, env, file, http, json).
"""

def get_stdlib_part1_pages():
    pages = {}

    # 1. Stdlib Overview
    pages["docs/standard-library/index.html"] = '''
<h1 id="standard-library-overview">Standard Library Overview</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair includes a robust, zero-external-dependency standard library containing <strong>20 built-in modules</strong>. Every module is written in optimized C or pure Djazair, loaded with zero overhead using the <code>use &lt;module&gt;</code> syntax.
</p>

<div class="stdlib-grid">
  <a href="assert.html" class="stdlib-card">
    <div class="stdlib-name">assert</div>
    <div class="stdlib-desc">Test assertions, equality checks, truthiness, and exception testing.</div>
  </a>
  <a href="bytes.html" class="stdlib-card">
    <div class="stdlib-name">bytes</div>
    <div class="stdlib-desc">Binary buffer allocation, hex conversions, slicing, and byte operations.</div>
  </a>
  <a href="collections.html" class="stdlib-card">
    <div class="stdlib-name">collections</div>
    <div class="stdlib-desc">Stack, Queue, Deque, Set, LinkedList, and PriorityQueue data structures.</div>
  </a>
  <a href="crypto.html" class="stdlib-card">
    <div class="stdlib-name">crypto</div>
    <div class="stdlib-desc">SHA-256 hashing, Base64 encoding/decoding, and AES encryption.</div>
  </a>
  <a href="datetime.html" class="stdlib-card">
    <div class="stdlib-name">datetime</div>
    <div class="stdlib-desc">High-precision timestamps, formatting, calendar math, and Date class.</div>
  </a>
  <a href="dir.html" class="stdlib-card">
    <div class="stdlib-name">dir</div>
    <div class="stdlib-desc">Directory creation, recursive glob matching (**), and traversal.</div>
  </a>
  <a href="env.html" class="stdlib-card">
    <div class="stdlib-name">env</div>
    <div class="stdlib-desc">Access, query, and manipulate environment variables at runtime.</div>
  </a>
  <a href="file.html" class="stdlib-card">
    <div class="stdlib-name">file</div>
    <div class="stdlib-desc">File read/write, streams, binary bytes, stat, chmod, and symlinks.</div>
  </a>
  <a href="http.html" class="stdlib-card">
    <div class="stdlib-name">http</div>
    <div class="stdlib-desc">HTTP client (GET, POST, etc.) and multithreaded HTTP/1.1 web server.</div>
  </a>
  <a href="json.html" class="stdlib-card">
    <div class="stdlib-name">json</div>
    <div class="stdlib-desc">JSON serialization and deserialization with pretty-printing.</div>
  </a>
  <a href="lang.html" class="stdlib-card">
    <div class="stdlib-name">lang</div>
    <div class="stdlib-desc">Garbage collection control, heap memory statistics, and VM metadata.</div>
  </a>
  <a href="math.html" class="stdlib-card">
    <div class="stdlib-name">math</div>
    <div class="stdlib-desc">Constants, trigonometry, logs, powers, rounding, gcd, lcm, factorial.</div>
  </a>
  <a href="net.html" class="stdlib-card">
    <div class="stdlib-name">net</div>
    <div class="stdlib-desc">TCP/UDP client and server, URL parsing, URLSearchParams, DNS, TLS.</div>
  </a>
  <a href="os.html" class="stdlib-card">
    <div class="stdlib-name">os</div>
    <div class="stdlib-desc">Platform detection, CPU count, memory, username, temp directory.</div>
  </a>
  <a href="path.html" class="stdlib-card">
    <div class="stdlib-name">path</div>
    <div class="stdlib-desc">Cross-platform path manipulation, join, resolve, dirname, basename.</div>
  </a>
  <a href="process.html" class="stdlib-card">
    <div class="stdlib-name">process</div>
    <div class="stdlib-desc">Process identification, exec commands, and async spawn with pipes.</div>
  </a>
  <a href="random.html" class="stdlib-card">
    <div class="stdlib-name">random</div>
    <div class="stdlib-desc">Pseudorandom numbers, floats, integers, choice, shuffle, seed.</div>
  </a>
  <a href="regex.html" class="stdlib-card">
    <div class="stdlib-name">regex</div>
    <div class="stdlib-desc">Regular expressions, compile, search, fullMatch, findAll, sub, split.</div>
  </a>
  <a href="thread.html" class="stdlib-card">
    <div class="stdlib-name">thread</div>
    <div class="stdlib-desc">Actor model concurrency, worker threads, message passing, pools.</div>
  </a>
  <a href="uuid.html" class="stdlib-card">
    <div class="stdlib-name">uuid</div>
    <div class="stdlib-desc">Universally Unique Identifier (UUID v4) generation and validation.</div>
  </a>
</div>
'''

    # 2. assert
    pages["docs/standard-library/assert.html"] = '''
<h1 id="assert-module">assert Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>assert</code> module provides comprehensive testing assertions for validating conditions, types, exceptions, and collection equality in unit tests and development suites.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use assert</code></pre>

<h2 id="truthiness-equality">Truthiness & Equality Assertions</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>assert.isTrue(val, msg?)</code></td><td>Asserts that <code>val</code> evaluates to true.</td></tr>
      <tr><td><code>assert.isFalse(val, msg?)</code></td><td>Asserts that <code>val</code> evaluates to false.</td></tr>
      <tr><td><code>assert.equal(actual, expected, msg?)</code></td><td>Asserts that <code>actual == expected</code> (supports deep equality).</td></tr>
      <tr><td><code>assert.notEqual(actual, expected, msg?)</code></td><td>Asserts that <code>actual != expected</code>.</td></tr>
      <tr><td><code>assert.approxEqual(a, b, tolerance, message)</code></td><td>Asserts that two floats are equal within tolerance.</td></tr>
      <tr><td><code>assert.isNull(val, msg?)</code></td><td>Asserts that <code>val</code> is <code>Null</code>.</td></tr>
      <tr><td><code>assert.notNull(val, msg?)</code></td><td>Asserts that <code>val</code> is not <code>Null</code>.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="practical-example">Practical Unit Test Example</h2>
<pre><code class="language-dz">use assert

fn calculateDiscount(price, percentage)
    if percentage < 0 or percentage > 100
        throw "Invalid percentage"
    end
    return price * (1.0 - percentage / 100.0)
end

# 1. Equality check
assert.equal(calculateDiscount(100, 20), 80.0, "Discount calculation")

# 2. Approximate float comparison (value, expected, tolerance, message)
assert.approxEqual(calculateDiscount(99.99, 15), 84.9915, 0.001, "Discount approximate equality")

# 3. Exception testing
let threw = False
try
    calculateDiscount(100, 150)
catch e
    threw = True
end
assert.isTrue(threw, "Out-of-range percentage must throw error")

print("All assertions passed successfully!")
</code></pre>
'''

    # 3. bytes
    pages["docs/standard-library/bytes.html"] = '''
<h1 id="bytes-module">bytes Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>bytes</code> module provides manipulation and conversions for raw byte buffers, binary encodings, and hex representations.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use bytes</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>bytes.alloc(size)</code></td><td>Allocates a zeroed byte buffer of given size.</td></tr>
      <tr><td><code>bytes.fromString(str)</code></td><td>Converts a UTF-8 string into an array of byte integers (0-255).</td></tr>
      <tr><td><code>bytes.toString(buf)</code></td><td>Converts an array of byte integers back into a UTF-8 string.</td></tr>
      <tr><td><code>bytes.hexToBytes(hexStr)</code></td><td>Decodes a hexadecimal string (e.g. "48656c6c6f") into bytes.</td></tr>
      <tr><td><code>bytes.bytesToHex(buf)</code></td><td>Encodes a byte array into a hex string.</td></tr>
      <tr><td><code>bytes.slice(buf, start, end)</code></td><td>Slices a subarray of bytes.</td></tr>
      <tr><td><code>bytes.indexOf(buf, byteVal)</code></td><td>Finds index of first occurrence of byte (-1 if not found).</td></tr>
      <tr><td><code>bytes.contains(buf, byteVal)</code></td><td>Returns True if byte is present.</td></tr>
      <tr><td><code>bytes.concat(bufA, bufB)</code></td><td>Concatenates two byte arrays.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use bytes

# Allocate or decode a byte buffer from hex
let buf = bytes.hexToBytes("deadbeef")

# Convert to hex string
print(bytes.bytesToHex(buf)) # => "deadbeef"

# Roundtrip from string
let msg = "Hello Djazair"
let encoded = bytes.fromString(msg)
print("Bytes length: ${encoded.length()}") # => 13
print(bytes.toString(encoded))           # => "Hello Djazair"
</code></pre>
'''

    # 4. collections
    pages["docs/standard-library/collections.html"] = '''
<h1 id="collections-module">collections Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>collections</code> module introduces specialized data structures beyond built-in Arrays and Maps: <strong>Stack</strong>, <strong>Queue</strong>, <strong>Deque</strong>, <strong>Set</strong>, <strong>LinkedList</strong>, and <strong>PriorityQueue</strong>.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use collections</code></pre>

<h2 id="data-structures">Data Structures Catalog</h2>

<h3 id="stack">1. Stack (LIFO)</h3>
<pre><code class="language-dz">use collections

let s = new collections.Stack()
s.push(10)
s.push(20)
print(s.peek())     # => 20
print(s.pop())      # => 20
print(s.size())     # => 1
print(s.isEmpty())  # => False
</code></pre>

<h3 id="queue">2. Queue (FIFO) & Deque (Double-Ended)</h3>
<pre><code class="language-dz">use collections

# Queue
let q = new collections.Queue()
q.enqueue("Task 1")
q.enqueue("Task 2")
print(q.dequeue())  # => "Task 1"

# Deque (pushFront, pushBack, popFront, popBack)
let d = new collections.Deque()
d.pushBack(10)
d.pushFront(5)
print(d.popFront()) # => 5
print(d.popBack())  # => 10
</code></pre>

<h3 id="set">3. Set (Unique Elements & Math Operations)</h3>
<pre><code class="language-dz">use collections

let s1 = new collections.Set()
s1.add(1).add(2).add(3)

let s2 = new collections.Set()
s2.add(2).add(3).add(4)

# Set algebra
let unionSet = s1.union(s2)             # contains 1, 2, 3, 4
let intersectSet = s1.intersection(s2)  # contains 2, 3
let diffSet = s1.difference(s2)        # contains 1

print(s1.has(2))                        # => True
print(s1.has(99))                       # => False
</code></pre>

<h3 id="priority-queue">4. PriorityQueue (Min-Heap / Priority Ordering)</h3>
<pre><code class="language-dz">use collections

let pq = new collections.PriorityQueue()
pq.enqueue("Low priority task", 4)
pq.enqueue("Critical emergency", 1)
pq.enqueue("Medium priority task", 2)

# Dequeues in priority order (1 is highest priority):
print(pq.dequeue()) # => "Critical emergency"
print(pq.dequeue()) # => "Medium priority task"
</code></pre>
'''

    # 5. crypto
    pages["docs/standard-library/crypto.html"] = '''
<h1 id="crypto-module">crypto Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>crypto</code> module provides cryptographic primitives: SHA-256 secure hashing, Base64 encoding/decoding, and AES-CBC symmetric encryption.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use crypto</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>crypto.sha256(text)</code></td><td>Computes the SHA-256 digest of <code>text</code>, returning a 64-character lowercase hex string.</td></tr>
      <tr><td><code>crypto.base64Encode(text)</code></td><td>Encodes text into a standard RFC-4648 Base64 string.</td></tr>
      <tr><td><code>crypto.base64Decode(encoded)</code></td><td>Decodes a Base64 string back into original text.</td></tr>
      <tr><td><code>crypto.aesEncrypt(plain, key, iv)</code></td><td>Encrypts plaintext using AES-256-CBC with the provided 32-byte key and 16-byte IV.</td></tr>
      <tr><td><code>crypto.aesDecrypt(cipher, key, iv)</code></td><td>Decrypts ciphertext back to plaintext using AES-256-CBC.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use crypto

# 1. SHA-256 Hashing
let hash = crypto.sha256("password123")
print("SHA-256: ${hash}")
# => ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# 2. Base64 Roundtrip
let encoded = crypto.base64Encode("Djazair Language")
print("Base64: ${encoded}") # => "RGphemFpciBMYW5ndWFnZQ=="
print("Decoded: ${crypto.base64Decode(encoded)}")

# 3. AES-256 Symmetric Encryption
let key = "0123456789abcdef0123456789abcdef" # 32 bytes
let iv  = "0123456789abcdef"                 # 16 bytes

let secret = "Confidential payload data"
let encrypted = crypto.aesEncrypt(secret, key, iv)
let decrypted = crypto.aesDecrypt(encrypted, key, iv)

print("Decrypted successfully: ${decrypted == secret}") # => True
</code></pre>
'''

    # 6. datetime
    pages["docs/standard-library/datetime.html"] = '''
<h1 id="datetime-module">datetime Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>datetime</code> module handles dates, timestamps, calendar math, custom string formatting, and date comparison operations.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use datetime</code></pre>

<h2 id="api-reference">Key Functions & Date Methods</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function / Method</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>datetime.timestamp()</code></td><td>Returns current Unix epoch timestamp in seconds.</td></tr>
      <tr><td><code>datetime.ticks()</code></td><td>Returns high-resolution millisecond monotonic ticks for benchmarking.</td></tr>
      <tr><td><code>datetime.now()</code></td><td>Returns a <code>Date</code> instance representing current system time.</td></tr>
      <tr><td><code>datetime.fromParts(year, month, day, hour, min, sec)</code></td><td>Constructs a <code>Date</code> instance from specific calendar parts.</td></tr>
      <tr><td><code>datetime.isLeapYear(year)</code></td><td>Returns True if the specified year is a leap year.</td></tr>
      <tr><td><code>date.format(fmtString)</code></td><td>Formats date using strftime tokens (e.g. <code>"%Y-%m-%d %H:%M:%S"</code>).</td></tr>
      <tr><td><code>date.addDays(n)</code></td><td>Returns a new Date advanced by <code>n</code> days.</td></tr>
      <tr><td><code>date.diffInDays(otherDate)</code></td><td>Calculates difference in days between two dates.</td></tr>
      <tr><td><code>date.isBefore(otherDate)</code></td><td>Returns True if date occurs before otherDate.</td></tr>
      <tr><td><code>date.isAfter(otherDate)</code></td><td>Returns True if date occurs after otherDate.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use datetime

let now = datetime.now()
print("Current Year: ${now.year()}")
print("Formatted: ${now.format("%Y-%m-%d %H:%M:%S")}")

# Date arithmetic
let event = datetime.fromParts(2026, 11, 1, 9, 0, 0)
let reminder = event.addDays(-7)

print("Event Date: ${event.format("%d %B %Y")}")
print("Reminder: ${reminder.format("%d %B %Y")}")
print("Days until event: ${event.diffInDays(now)}")
</code></pre>
'''

    # 7. dir
    pages["docs/standard-library/dir.html"] = '''
<h1 id="dir-module">dir Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>dir</code> module provides filesystem directory operations: creating directories, listing directory contents, recursive globbing with <code>**</code>, and recursive removal.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use dir</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>dir.current()</code></td><td>Returns the absolute current working directory path.</td></tr>
      <tr><td><code>dir.create(path)</code></td><td>Creates a single directory.</td></tr>
      <tr><td><code>dir.createAll(path)</code></td><td>Recursively creates all parent directories in path (like <code>mkdir -p</code>).</td></tr>
      <tr><td><code>dir.list(path)</code></td><td>Returns an array of file and folder names inside directory.</td></tr>
      <tr><td><code>dir.glob(pattern)</code></td><td>Matches files using glob patterns (supports recursive <code>**/*.dz</code>).</td></tr>
      <tr><td><code>dir.traverse(path, callback)</code></td><td>Recursively walks through a directory hierarchy invoking callback.</td></tr>
      <tr><td><code>dir.delete(path)</code></td><td>Deletes an empty directory.</td></tr>
      <tr><td><code>dir.deleteAll(path)</code></td><td>Recursively deletes a directory and all its contents.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use dir

# Get working directory
let cwd = dir.current()
print("Working in: ${cwd}")

# Find all Djazair scripts recursively
let scripts = dir.glob("src/**/*.dz")
print("Found ${scripts.length()} scripts:")
for s in scripts
    print("  -> ${s}")
end
</code></pre>
'''

    # 8. env
    pages["docs/standard-library/env.html"] = '''
<h1 id="env-module">env Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>env</code> module allows you to read, set, and verify operating system environment variables at runtime.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use env</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>env.get(name)</code></td><td>Retrieves environment variable (or Null if undefined).</td></tr>
      <tr><td><code>env.set(name, value)</code></td><td>Sets or updates an environment variable for the current process.</td></tr>
      <tr><td><code>env.has(name)</code></td><td>Returns True if the environment variable is defined.</td></tr>
      <tr><td><code>env.all()</code></td><td>Returns a Map of all defined environment variables.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use env

# Reading with a fallback default
let port = env.get("PORT")
if isNull(port) port = "8080" end

let dbUrl = env.get("DATABASE_URL")
if isNull(dbUrl) dbUrl = "sqlite://app.db" end

print("Server configured on port: ${port}")

# Setting environment variables
env.set("APP_ENV", "production")
print("Running in: ${env.get("APP_ENV")}")
</code></pre>
'''

    # 9. file
    pages["docs/standard-library/file.html"] = '''
<h1 id="file-module">file Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>file</code> module handles filesystem operations: reading/writing text, reading/writing binary buffers, line-by-line streaming, querying file metadata, modifying permissions (chmod), and managing symlinks.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use file</code></pre>

<h2 id="convenience-functions">Convenience Functions</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>file.read(path)</code></td><td>Reads entire file content as a UTF-8 String.</td></tr>
      <tr><td><code>file.write(path, text)</code></td><td>Overwrites file with text string.</td></tr>
      <tr><td><code>file.append(path, text)</code></td><td>Appends text to the end of file.</td></tr>
      <tr><td><code>file.readLines(path)</code></td><td>Reads entire file and returns an Array of lines.</td></tr>
      <tr><td><code>file.writeLines(path, lines)</code></td><td>Writes an Array of strings to file, separated by newlines.</td></tr>
      <tr><td><code>file.exists(path)</code></td><td>Returns True if file or directory exists.</td></tr>
      <tr><td><code>file.isFile(path)</code></td><td>Returns True if path points to a regular file.</td></tr>
      <tr><td><code>file.isDir(path)</code></td><td>Returns True if path points to a directory.</td></tr>
      <tr><td><code>file.delete(path)</code></td><td>Deletes the file.</td></tr>
      <tr><td><code>file.copy(src, dest)</code></td><td>Copies file from src to dest.</td></tr>
      <tr><td><code>file.move(src, dest)</code></td><td>Moves or renames file from src to dest.</td></tr>
      <tr><td><code>file.stat(path)</code></td><td>Returns a Map of file metadata: size, modified timestamp, etc.</td></tr>
      <tr><td><code>file.chmod(path, mode)</code></td><td>Changes file permissions (e.g. 0644).</td></tr>
      <tr><td><code>file.writeBytes(path, bytes)</code></td><td>Writes raw byte buffer to binary file.</td></tr>
      <tr><td><code>file.readBytes(path)</code></td><td>Reads raw byte buffer from binary file.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="filehandle-class">Low-Level FileHandle Streaming</h2>
<p>For fine-grained control or streaming large files, open files using <code>file.open(path, mode)</code>:</p>

<pre><code class="language-dz">use file

# Open file for writing
let handle = file.open("log.txt", "w")
handle.write("Line 1: system started\n")
handle.write("Line 2: connected to database\n")
handle.flush()
handle.close()

# Open file for reading
let reader = file.open("log.txt", "r")
let firstLine = reader.readLine()
print("First line: ${firstLine}")
reader.close()
</code></pre>
'''

    # 10. http
    pages["docs/standard-library/http.html"] = '''
<h1 id="http-module">http Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>http</code> module offers a complete HTTP/1.1 networking toolkit: an easy-to-use HTTP client (GET, POST, PUT, DELETE, etc.) and a high-performance multithreaded HTTP Server with connection pooling, keep-alive, streaming, and custom routing.
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use http</code></pre>

<h2 id="http-client">HTTP Client Methods</h2>
<pre><code class="language-dz">use http
use json

# Simple GET request
let res = http.get("https://httpbin.org/get")
print("Status: ${res.statusCode}") # => 200
print("Body: ${res.body}")

# POST request with JSON payload
let payload = json.encode({"name": "Djazair", "version": "1.1.0"})
let headers = {"Content-Type": "application/json"}

let postRes = http.post("https://httpbin.org/post", payload, headers)
print("Response status: ${postRes.statusCode}")
</code></pre>

<h2 id="http-server">Building an HTTP Web Server (Kasbah)</h2>
<p>Create a high-performance, non-blocking HTTP server using <code>http.createServer()</code>:</p>

<pre><code class="language-dz">use http
use json

let server = http.createServer(fn(req, res)
    print("${req.method} ${req.path} from ${req.remoteAddr}")

    if req.pathname == "/"
        res.setHeader("Content-Type", "text/html")
        res.status(200).send("<h1>Hello from Djazair Kasbah Server!</h1>")
    elif req.pathname == "/api/status"
        res.setHeader("Content-Type", "application/json")
        res.status(200).send({"status": "running", "uptime": 120})
    else
        res.status(404).send("Page Not Found")
    end
end)

# Start listening on port 8080
print("Server listening on http://localhost:8080")
server.listen(8080)
</code></pre>
'''

    # 11. json
    pages["docs/standard-library/json.html"] = '''
<h1 id="json-module">json Module</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  The <code>json</code> module provides fast, safe JSON serialization and deserialization between JSON strings and native Djazair data types (Arrays, Maps, Booleans, Numbers, and Null).
</p>

<h2 id="importing">Importing</h2>
<pre><code class="language-dz">use json</code></pre>

<h2 id="api-reference">API Reference</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr><th>Function</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>json.decode(jsonString)</code></td><td>Parses a JSON string into corresponding Djazair types (Maps, Arrays, primitives). Alias: <code>json.parse()</code>.</td></tr>
      <tr><td><code>json.encode(value, indent?, sortKeys?)</code></td><td>Serializes a value into a JSON string with optional formatting indentation. Alias: <code>json.stringify()</code>.</td></tr>
    </tbody>
  </table>
</div>

<h2 id="code-example">Example Usage</h2>
<pre><code class="language-dz">use json

# Decoding JSON string to native Map
let raw = `{"project": "Djazair", "stars": 1500, "stable": true}`
let data = json.decode(raw)

print(data["project"]) # => Djazair
print(data["stars"])   # => 1500

# Modifying and Encoding back with 2-space indentation
data["stars"] += 50
data["tags"] = ["scripting", "compiler", "c"]

let jsonOutput = json.encode(data, 2)
print(jsonOutput)
</code></pre>
'''

    return pages
