"""
Content generators for Language Guide section.
"""

def get_language_guide_pages():
    pages = {}

    # 1. Variables & Scope
    pages["docs/language-guide/variables.html"] = '''
<h1 id="variables-scope">Variables & Lexical Scope</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  In Djazair, variables are declared using the <code>let</code> keyword. The language uses dynamic typing with lexical block scoping.
</p>

<h2 id="declaring-variables">Declaring Variables</h2>
<p>Variables are declared using <code>let</code> followed by an identifier and an optional initial value:</p>

<pre><code class="language-dz">let name = "Djazair"
let version = 1.1
let isReleased = True

# Numbers can include underscores for readability
let largeCount = 100_000_000
let hexNumber = 0xFF
</code></pre>

<h2 id="reassignment-mutation">Reassignment & Mutation</h2>
<p>Once declared with <code>let</code>, variables can be reassigned to values of any type, or mutated using shorthand assignment operators:</p>

<pre><code class="language-dz">let score = 10
score += 5       # score is now 15
score *= 2       # score is now 30
score++          # score is now 31

# Changing types dynamically
score = "Thirty-One" # Valid dynamic typing
</code></pre>

<h2 id="lexical-scoping">Lexical Block Scoping</h2>
<p>Djazair follows strict lexical block scoping. Any variable declared inside a block (such as an <code>if</code>, <code>while</code>, <code>for</code>, or <code>fn</code> block) is isolated to that block and shadows any identical outer identifier:</p>

<pre><code class="language-dz">let count = 100

if True
    let count = 50  # Shadows the outer count
    print("Inner count: ${count}") # => Inner count: 50
end

print("Outer count: ${count}")     # => Outer count: 100
</code></pre>

<h2 id="naming-conventions">Identifier Naming Rules</h2>
<ul>
  <li>Identifiers can start with any ASCII letter (<code>a-z</code>, <code>A-Z</code>), underscore (<code>_</code>), or any valid Unicode letter (including Arabic letters like <code>ع</code>, <code>س</code>).</li>
  <li>Subsequent characters may include digits (<code>0-9</code>) and emojis (e.g. <code>let 🚀_speed = 300</code>).</li>
  <li>Keywords such as <code>let</code>, <code>fn</code>, <code>class</code>, <code>if</code>, and <code>while</code> cannot be used as variable names.</li>
</ul>
'''

    # 2. Data Types & Casting
    pages["docs/language-guide/data-types.html"] = '''
<h1 id="data-types-casting">Data Types & Casting</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair features a clean set of primitive and compound data types. Every value carries its own type metadata at runtime, inspectable using <code>type(v)</code>.
</p>

<h2 id="primitive-types">Primitive Data Types</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example Literal</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>Int</code></td>
        <td>Signed 32-bit integer for counts, indexing, and arithmetic.</td>
        <td><code>42</code>, <code>-17</code>, <code>100_000</code></td>
      </tr>
      <tr>
        <td><code>Float</code></td>
        <td>IEEE 754 64-bit double precision floating-point number.</td>
        <td><code>3.14159</code>, <code>-0.5</code>, <code>1.0</code></td>
      </tr>
      <tr>
        <td><code>String</code></td>
        <td>Immutable, UTF-8 encoded text sequence.</td>
        <td><code>"hello"</code>, <code>`multiline`</code></td>
      </tr>
      <tr>
        <td><code>Bool</code></td>
        <td>Boolean truth values: <code>True</code> and <code>False</code>.</td>
        <td><code>True</code>, <code>False</code></td>
      </tr>
      <tr>
        <td><code>Null</code></td>
        <td>Represents the intentional absence of any value.</td>
        <td><code>Null</code></td>
      </tr>
    </tbody>
  </table>
</div>

<h2 id="compound-types">Compound & Object Types</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Type</th>
        <th>Description</th>
        <th>Example Literal</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>Array</code></td>
        <td>Ordered dynamic list supporting mixed types and nested structures.</td>
        <td><code>[1, "two", True, [3, 4]]</code></td>
      </tr>
      <tr>
        <td><code>Map</code></td>
        <td>Hash table storing key-value associations of any types.</td>
        <td><code>{"name": "Riad", "age": 30}</code></td>
      </tr>
      <tr>
        <td><code>Range</code></td>
        <td>Inclusive integer sequence for loops and slicing.</td>
        <td><code>0..5</code>, <code>10 to 20</code></td>
      </tr>
      <tr>
        <td><code>Function</code></td>
        <td>First-class callable closures or native function pointers.</td>
        <td><code>fn(x) => x * 2</code></td>
      </tr>
      <tr>
        <td><code>Class / Instance</code></td>
        <td>Object-oriented classes and instantiated objects.</td>
        <td><code>class User ... end</code></td>
      </tr>
    </tbody>
  </table>
</div>

<h2 id="type-casting">Explicit Type Casting</h2>
<p>Djazair provides five global conversion functions: <code>int()</code>, <code>float()</code>, <code>str()</code>, <code>bool()</code>, and <code>num()</code>:</p>

<pre><code class="language-dz"># Converting to Int
let a = int("42")       # 42
let b = int(3.99)       # 3 (truncation)
let c = int(True)       # 1

# Converting to Float
let d = float("3.14")   # 3.14
let e = float(10)       # 10.0

# Converting to String
let f = str(123)        # "123"
let g = str(True)       # "True"
let h = str(Null)       # "Null"

# Converting to Boolean (Truthy / Falsy semantics)
print(bool(1))          # True
print(bool(0))          # False
print(bool("hello"))    # True
print(bool(""))         # False
print(bool([]))         # False (empty collections are falsy)
print(bool(Null))       # False

# num() parses strings to either int or float automatically
print(num("100"))       # 100 (Int)
print(num("100.5"))     # 100.5 (Float)
</code></pre>

<h2 id="type-introspection">Type Introspection</h2>
<p>You can check a value's runtime type with <code>type(v)</code> or use dedicated type predicate functions:</p>

<pre><code class="language-dz">let val = [1, 2, 3]

print(type(val))        # => Array
print(isArray(val))     # => True
print(isString(val))    # => False
print(isNumber(42))     # => True
print(isNull(Null))     # => True
</code></pre>
'''

    # 3. Operators
    pages["docs/language-guide/operators.html"] = '''
<h1 id="operators">Operators</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair provides a rich set of operators for arithmetic, bitwise logic, deep equality comparisons, identity checks, and collection membership.
</p>

<h2 id="arithmetic-operators">Arithmetic Operators</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Operator</th>
        <th>Description</th>
        <th>Example</th>
        <th>Result</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>+</code></td><td>Addition / String Concatenation</td><td><code>10 + 5</code></td><td><code>15</code></td></tr>
      <tr><td><code>-</code></td><td>Subtraction / Negation</td><td><code>10 - 5</code></td><td><code>5</code></td></tr>
      <tr><td><code>*</code></td><td>Multiplication</td><td><code>4 * 3</code></td><td><code>12</code></td></tr>
      <tr><td><code>/</code></td><td>Division (returns Float)</td><td><code>7 / 2</code></td><td><code>3.5</code></td></tr>
      <tr><td><code>//</code></td><td>Floor Division (integer division)</td><td><code>7 // 2</code></td><td><code>3</code></td></tr>
      <tr><td><code>%</code></td><td>Modulo (remainder)</td><td><code>10 % 3</code></td><td><code>1</code></td></tr>
      <tr><td><code>**</code></td><td>Exponentiation (Power)</td><td><code>2 ** 8</code></td><td><code>256</code></td></tr>
      <tr><td><code>++</code>, <code>--</code></td><td>Increment / Decrement (prefix or postfix)</td><td><code>x++</code></td><td>Increments x by 1</td></tr>
    </tbody>
  </table>
</div>

<h2 id="comparison-deep-equality">Comparison & Deep Equality</h2>
<p>In Djazair, the equality operator <code>==</code> performs <strong>deep structural equality</strong> for collections and hash maps, not just reference comparison:</p>

<pre><code class="language-dz"># Primitive comparisons
print(10 == 10)         # => True
print(10 != 5)          # => True
print(10 > 5)           # => True
print(10 <= 10)         # => True

# Deep Equality on Arrays and Maps!
let listA = [1, [2, 3]]
let listB = [1, [2, 3]]
print(listA == listB)   # => True (structural match)

let mapA = {"user": "Riad", "role": "admin"}
let mapB = {"user": "Riad", "role": "admin"}
print(mapA == mapB)   # => True (deep equality)
</code></pre>

<h2 id="identity-membership">Identity (<code>is</code>) & Membership (<code>in</code>)</h2>
<p>Djazair separates value equality (<code>==</code>) from object identity (<code>is</code>), and provides the powerful <code>in</code> operator for testing membership across collections, strings, and classes:</p>

<pre><code class="language-dz"># Identity check: checks if both variables reference the EXACT same heap object
let x = [1, 2]
let y = x
let z = [1, 2]

print(x is y)           # => True (same reference)
print(x is z)           # => False (distinct objects)
print(x is not z)       # => True

# Membership check: in and not in
let fruits = ["apple", "banana", "orange"]
print("banana" in fruits)       # => True
print("grape" not in fruits)    # => True

# in on Maps (checks keys)
let user = {"id": 1, "name": "Sarah"}
print("name" in user)           # => True
print("email" not in user)      # => True

# in on Strings (checks substrings)
print("air" in "Djazair")       # => True
</code></pre>

<h2 id="bitwise-operators">Bitwise Operators</h2>
<pre><code class="language-dz">let a = 5   # binary 0101
let b = 3   # binary 0011

print(a & b)    # Bitwise AND  => 1  (0001)
print(a | b)    # Bitwise OR   => 7  (0111)
print(a ^ b)    # Bitwise XOR  => 6  (0110)
print(~a)       # Bitwise NOT  => -6
print(8 << 2)   # Shift Left   => 32
print(8 >> 2)   # Shift Right  => 2
</code></pre>
'''

    # 4. Strings & Methods
    pages["docs/language-guide/strings.html"] = '''
<h1 id="strings-methods">Strings & Methods</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Strings in Djazair are immutable sequences of UTF-8 encoded characters. They support string interpolation, raw multiline backtick blocks, and more than 30 built-in manipulation methods.
</p>

<h2 id="string-literals">String Literals & Interpolation</h2>
<p>Strings can be enclosed in double quotes <code>"..."</code> or backticks <code>`...`</code>. Any valid Djazair expression can be evaluated inside <code>${...}</code>:</p>

<pre><code class="language-dz">let name = "Riad"
let age = 25

# String interpolation
let message = "Hello, my name is ${name} and in 5 years I will be ${age + 5}."
print(message)
# => Hello, my name is Riad and in 5 years I will be 30.

# Multiline Strings with backticks
let htmlTemplate = `
  <div class="card">
    <h2>${name}</h2>
    <p>Age: ${age}</p>
  </div>
`
print(htmlTemplate)
</code></pre>

<h2 id="complete-methods-catalog">Complete String Methods Catalog</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Method</th>
        <th>Signature</th>
        <th>Description</th>
        <th>Example</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>length()</code></td><td><code>s.length()</code></td><td>Number of UTF-8 characters</td><td><code>"مرحبا".length() # => 5</code></td></tr>
      <tr><td><code>upper()</code></td><td><code>s.upper()</code></td><td>Converts to uppercase</td><td><code>"dz".upper() # => "DZ"</code></td></tr>
      <tr><td><code>lower()</code></td><td><code>s.lower()</code></td><td>Converts to lowercase</td><td><code>"HELLO".lower() # => "hello"</code></td></tr>
      <tr><td><code>strip()</code></td><td><code>s.strip()</code></td><td>Trims leading/trailing whitespace</td><td><code>"  hi  ".strip() # => "hi"</code></td></tr>
      <tr><td><code>lStrip()</code> / <code>rStrip()</code></td><td><code>s.lStrip()</code></td><td>Trims left or right whitespace</td><td><code>"  hi".lStrip() # => "hi"</code></td></tr>
      <tr><td><code>split(sep?)</code></td><td><code>s.split(sep?)</code></td><td>Splits string into an Array</td><td><code>"a,b,c".split(",") # => ["a","b","c"]</code></td></tr>
      <tr><td><code>join(array)</code></td><td><code>s.join(arr)</code></td><td>Joins array elements using separator</td><td><code>"-".join(["a","b"]) # => "a-b"</code></td></tr>
      <tr><td><code>replace(from, to)</code></td><td><code>s.replace(old, new)</code></td><td>Replaces occurrences of substring</td><td><code>"foo".replace("o","a") # => "faa"</code></td></tr>
      <tr><td><code>contains(sub)</code></td><td><code>s.contains(sub)</code></td><td>Returns True if substring exists</td><td><code>"djazair".contains("jaz") # => True</code></td></tr>
      <tr><td><code>startsWith(sub)</code></td><td><code>s.startsWith(sub)</code></td><td>Checks if string starts with prefix</td><td><code>"http://".startsWith("http") # => True</code></td></tr>
      <tr><td><code>endsWith(sub)</code></td><td><code>s.endsWith(sub)</code></td><td>Checks if string ends with suffix</td><td><code>"doc.pdf".endsWith(".pdf") # => True</code></td></tr>
      <tr><td><code>index(sub)</code></td><td><code>s.index(sub)</code></td><td>Index of substring (-1 if not found)</td><td><code>"hello".index("ll") # => 2</code></td></tr>
      <tr><td><code>slice(start, end?)</code></td><td><code>s.slice(start, end)</code></td><td>Slice between start and end index</td><td><code>"Djazair".slice(0, 4) # => "Djaz"</code></td></tr>
      <tr><td><code>subStr(start, len)</code></td><td><code>s.subStr(start, len)</code></td><td>Substring with given length</td><td><code>"Djazair".subStr(1, 3) # => "jaz"</code></td></tr>
      <tr><td><code>reverse()</code></td><td><code>s.reverse()</code></td><td>Returns reversed string</td><td><code>"abc".reverse() # => "cba"</code></td></tr>
      <tr><td><code>capitalize()</code></td><td><code>s.capitalize()</code></td><td>Capitalizes first character</td><td><code>"algiers".capitalize() # => "Algiers"</code></td></tr>
      <tr><td><code>title()</code></td><td><code>s.title()</code></td><td>Title-cases every word</td><td><code>"hello world".title() # => "Hello World"</code></td></tr>
      <tr><td><code>swapCase()</code></td><td><code>s.swapCase()</code></td><td>Inverts letter cases</td><td><code>"AbC".swapCase() # => "aBc"</code></td></tr>
      <tr><td><code>center(width, pad?)</code></td><td><code>s.center(w, pad)</code></td><td>Centers string in given width</td><td><code>"dz".center(6, "-") # => "--dz--"</code></td></tr>
      <tr><td><code>lJust()</code> / <code>rJust()</code></td><td><code>s.lJust(w, pad)</code></td><td>Pads string on right or left</td><td><code>"5".lJust(3, "0") # => "500"</code></td></tr>
      <tr><td><code>zFill(width)</code></td><td><code>s.zFill(width)</code></td><td>Pads with leading zeroes</td><td><code>"42".zFill(5) # => "00042"</code></td></tr>
      <tr><td><code>charCodeAt(index)</code></td><td><code>s.charCodeAt(idx)</code></td><td>Returns character Unicode code-point</td><td><code>"A".charCodeAt(0) # => 65</code></td></tr>
      <tr><td><code>isAlpha()</code></td><td><code>s.isAlpha()</code></td><td>Checks if purely alphabetic</td><td><code>"abc".isAlpha() # => True</code></td></tr>
      <tr><td><code>isDigit()</code></td><td><code>s.isDigit()</code></td><td>Checks if purely numeric digits</td><td><code>"123".isDigit() # => True</code></td></tr>
      <tr><td><code>isAlnum()</code></td><td><code>s.isAlnum()</code></td><td>Checks if alphanumeric</td><td><code>"a1".isAlnum() # => True</code></td></tr>
      <tr><td><code>isSpace()</code></td><td><code>s.isSpace()</code></td><td>Checks if whitespace-only</td><td><code>" \t\n".isSpace() # => True</code></td></tr>
    </tbody>
  </table>
</div>
'''

    # 5. Unicode
    pages["docs/language-guide/unicode.html"] = '''
<h1 id="unicode-utf8">Unicode & UTF-8</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair was engineered with first-class internationalization at its very core. Rather than treating strings as raw ASCII byte buffers, Djazair operates on true Unicode code points.
</p>

<div class="callout callout-tip">
  <div class="callout-title"><i class="fa-solid fa-earth-africa"></i> Native Arabic & Emoji Support</div>
  <p>In Djazair, Arabic identifiers, multi-byte emojis, Japanese Kanji, and accented letters are valid anywhere: in variable names, function declarations, class properties, and string operations.</p>
</div>

<h2 id="arabic-identifiers">Arabic Identifiers & Code Example</h2>
<p>You can write complete scripts using Arabic variable and function names:</p>

<pre><code class="language-dz"># Variables and functions with Arabic and emojis
let 🚀_السرعة = 100

fn 🧑‍💻_حساب_المجموع(أ, ب)
    return أ + ب
end

print("النتيجة: ${🧑‍💻_حساب_المجموع(25, 75)}")
# => النتيجة: 100
</code></pre>

<h2 id="code-point-accuracy">Code-Point Accurate Length & Indexing</h2>
<p>Consider a mixed string with 1-byte, 2-byte, 3-byte, and 4-byte characters:</p>

<pre><code class="language-dz"># A (1 byte), م (2 bytes), 漢 (3 bytes), 🚀 (4 bytes)
let complexStr = "Aم漢🚀"

# In many other languages, length returns 10 bytes.
# In Djazair, length() returns the true logical character count:
print(complexStr.length())          # => 4

# Accurate character iteration:
for char in complexStr
    print("${char} => code point: ${char.charCodeAt(0)}")
end
# A => code point: 65
# م => code point: 1605
# 漢 => code point: 28450
# 🚀 => code point: 128640

# Surgical slicing without breaking multi-byte boundaries:
print(complexStr.slice(1, 3))       # => م漢
</code></pre>

<h2 id="arabic-diacritics">Arabic Diacritics (التشكيل)</h2>
<p>Arabic vowels and diacritical marks (حركات التشكيل) are treated as distinct logical Unicode code points, allowing precise linguistic processing:</p>

<pre><code class="language-dz">let phrase = "بِسْمِ اللَّهِ"
print("Text: ${phrase}")
print("Character count with diacritics: ${phrase.length()}")
</code></pre>
'''

    # 6. Arrays
    pages["docs/language-guide/arrays.html"] = '''
<h1 id="arrays-methods">Arrays & Higher-Order Functions</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Arrays in Djazair are dynamic, resizable lists that can hold values of any type. They come packed with rich functional programming methods like <code>map</code>, <code>filter</code>, <code>reduce</code>, <code>find</code>, <code>every</code>, and <code>some</code>.
</p>

<h2 id="creating-arrays">Creating & Modifying Arrays</h2>
<pre><code class="language-dz"># Array initialization
let list = [10, 20, 30]

# Adding and removing elements
list.append(40)         # [10, 20, 30, 40]
list.insert(1, 15)      # [10, 15, 20, 30, 40]
let last = list.pop()   # last is 40, list is [10, 15, 20, 30]
list.remove(15)         # removes value 15 => [10, 20, 30]

# Element update & arithmetic
list[0] += 5            # list[0] is now 15
</code></pre>

<h2 id="higher-order-functions">Functional Transformations (HOFs)</h2>
<p>Djazair provides powerful higher-order functions that take callbacks or arrow functions:</p>

<pre><code class="language-dz">let numbers = [1, 2, 3, 4, 5, 6]

# 1. map — transform each element
let doubled = numbers.map(fn(x) => x * 2)
# => [2, 4, 6, 8, 10, 12]

# 2. filter — select matching elements
let evens = numbers.filter(fn(x) => x % 2 == 0)
# => [2, 4, 6]

# 3. reduce — aggregate array into a single accumulator
let sum = numbers.reduce(fn(acc, x) => acc + x, 0)
# => 21

# 4. Method Chaining
let chainedResult = numbers
    .filter(fn(x) => x > 2)
    .map(fn(x) => x * 10)
    .reduce(fn(acc, x) => acc + x, 0)

print("Chained result: ${chainedResult}") # => 180
</code></pre>

<h2 id="search-predicate-methods">Search & Predicate Methods</h2>
<pre><code class="language-dz">let users = [
    {"name": "Alice", "age": 22},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30}
]

# find — returns the first item matching predicate
let adult = users.find(fn(u) => u["age"] >= 18)
print("First adult: ${adult["name"]}") # => Alice

# every — checks if all items satisfy condition
let allAdults = users.every(fn(u) => u["age"] >= 18)
print("All adults? ${allAdults}") # => False

# some — checks if any item satisfies condition
let hasMinor = users.some(fn(u) => u["age"] < 18)
print("Has minor? ${hasMinor}") # => True
</code></pre>

<h2 id="statistical-utility-methods">Statistical & Utility Methods</h2>
<pre><code class="language-dz">let scores = [10, 5, 20, 15, 10]

print("sum: ${scores.sum()}")       # => 60
print("max: ${scores.max()}")       # => 20
print("min: ${scores.min()}")       # => 5
print("unique: ${scores.unique()}") # => [10, 5, 20, 15]

# In-place sorting and non-destructive sorted()
let letters = ["c", "a", "b"]
print(letters.sorted())             # => ["a", "b", "c"]
</code></pre>
'''

    # 7. Maps
    pages["docs/language-guide/maps.html"] = '''
<h1 id="maps-hashes">Maps & Hashes</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Maps (also known as Hashes or Dictionaries) store associative key-value pairs. They support fast lookups, arbitrary key types, nested structures, and convenient built-in methods.
</p>

<h2 id="creating-maps">Creating & Modifying Maps</h2>
<pre><code class="language-dz">let user = {
    "name": "Riyadh",
    "role": "Developer",
    "level": 5,
    "skills": ["C", "Djazair", "Web"]
}

# Accessing keys
print(user["name"])         # => Riyadh

# Updating & Adding keys
user["level"] += 1          # level is now 6
user["city"] = "Blida"      # new key added

# Checking key existence
print("role" in user)       # => True
print(user.has("salary"))   # => False
</code></pre>

<h2 id="map-methods">Map Methods Catalog</h2>
<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Method</th>
        <th>Description</th>
        <th>Example</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>length()</code></td><td>Number of key-value pairs</td><td><code>user.length()</code></td></tr>
      <tr><td><code>has(key)</code></td><td>Returns True if key is present</td><td><code>user.has("name")</code></td></tr>
      <tr><td><code>get(key)</code></td><td>Retrieves value of key (Null if missing)</td><td><code>user.get("missing")</code></td></tr>
      <tr><td><code>keys()</code></td><td>Returns an Array of all map keys</td><td><code>user.keys()</code></td></tr>
      <tr><td><code>values()</code></td><td>Returns an Array of all map values</td><td><code>user.values()</code></td></tr>
      <tr><td><code>items()</code></td><td>Returns array of [key, value] pairs</td><td><code>user.items()</code></td></tr>
      <tr><td><code>update(otherMap)</code></td><td>Merges another map into this map</td><td><code>user.update({"active": True})</code></td></tr>
      <tr><td><code>setDefault(k, v)</code></td><td>Sets key to default value if missing</td><td><code>user.setDefault("theme", "dark")</code></td></tr>
      <tr><td><code>pop(key)</code></td><td>Removes and returns value of key</td><td><code>user.pop("level")</code></td></tr>
      <tr><td><code>clear()</code></td><td>Removes all entries from map</td><td><code>user.clear()</code></td></tr>
      <tr><td><code>copy()</code></td><td>Creates a shallow copy of the map</td><td><code>let clone = user.copy()</code></td></tr>
    </tbody>
  </table>
</div>

<h2 id="iterating-maps">Iterating Over Maps</h2>
<p>The <code>for-in</code> loop directly supports key-value destructuring:</p>

<pre><code class="language-dz">let config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

for key, value in config
    print("${key} => ${value}")
end
# host => localhost
# port => 8080
# debug => True
</code></pre>
'''

    # 8. Control Flow
    pages["docs/language-guide/control-flow.html"] = '''
<h1 id="control-flow">Control Flow & Pattern Matching</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair provides clear branching constructs: <code>if-elif-else</code> statements, concise ternary expressions, and structural <code>match-case</code> pattern matching.
</p>

<h2 id="if-elif-else">If, Elif, Else</h2>
<pre><code class="language-dz">let score = 85

if score >= 90
    print("Grade: Excellent")
elif score >= 75
    print("Grade: Very Good")
elif score >= 50
    print("Grade: Pass")
else
    print("Grade: Retake")
end
</code></pre>

<h2 id="ternary-expression">Ternary Expression</h2>
<p>Djazair offers an inline ternary syntax for assigning values based on a condition:</p>

<pre><code class="language-dz">let age = 20
let status = if age >= 18 ? "Adult" else "Minor"

print("User status: ${status}") # => User status: Adult
</code></pre>

<h2 id="pattern-matching">Pattern Matching (<code>match-case</code>)</h2>
<p>The <code>match</code> construct provides structured multi-way branching, supporting multiple values per case and fallback defaults:</p>

<pre><code class="language-dz">let httpStatus = 404

match httpStatus
    case 200, 201, 204
        print("Success")
    case 301, 302
        print("Redirect")
    case 400, 401, 403, 404
        print("Client Error: ${httpStatus}")
    case 500, 502, 503
        print("Server Error")
    default
        print("Unknown Status Code")
end
# => Client Error: 404
</code></pre>
'''

    # 9. Loops
    pages["docs/language-guide/loops.html"] = '''
<h1 id="loops-iteration">Loops & Iteration</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair supports <code>while</code>, <code>do-while</code>, and rich <code>for-in</code> iterators across arrays, maps, strings, and ranges.
</p>

<h2 id="while-loops">While & Do-While</h2>
<pre><code class="language-dz"># While loop
let count = 0
while count < 3
    print("Count: ${count}")
    count++
end

# Do-While loop (guarantees at least one execution)
let n = 0
do
    print("Executed at least once, n = ${n}")
    n++
while (n < 2)
</code></pre>

<h2 id="for-in-collections">For-in on Collections & Ranges</h2>
<pre><code class="language-dz"># 1. Iterating over an Array
let items = ["Alpha", "Beta", "Gamma"]
for item in items
    print(item)
end

# 2. Iterating over an Integer Range (inclusive 0..4)
for i in 0..4
    print("Index: ${i}")
end

# 3. Iterating over a String (character by character)
for char in "Djazair"
    print(char)
end

# 4. Iterating over a Map with Key & Value
let capitals = {"Algeria": "Algiers", "Tunisia": "Tunis"}
for country, capital in capitals
    print("The capital of ${country} is ${capital}")
end
</code></pre>

<h2 id="break-continue">Break & Continue</h2>
<pre><code class="language-dz">for i in 1..10
    if i == 3
        continue # Skip 3
    end
    if i == 6
        break    # Terminate loop at 6
    end
    print(i) # Prints 1, 2, 4, 5
end
</code></pre>
'''

    # 10. Functions
    pages["docs/language-guide/functions.html"] = '''
<h1 id="functions-closures">Functions & Closures</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Functions in Djazair are first-class citizens. They can be stored in variables, passed as arguments, returned from other functions, and capture lexical closures.
</p>

<h2 id="defining-functions">Defining Functions</h2>
<pre><code class="language-dz"># Standard function declaration
fn add(a, b)
    return a + b
end

print(add(10, 20)) # => 30

# Concise Arrow Function expression
let multiply = fn(a, b) => a * b
print(multiply(4, 5)) # => 20
</code></pre>

<h2 id="default-arguments">Default Arguments</h2>
<p>Parameters can have default expressions, which can even reference previous parameters:</p>

<pre><code class="language-dz">fn greet(name = "World", greeting = "Hello")
    print("${greeting}, ${name}!")
end

greet()                 # => Hello, World!
greet("Riad")           # => Hello, Riad!
greet("Ali", "Welcome") # => Welcome, Ali!

# Referencing earlier parameters in default values:
fn calculateOffset(base, step = base * 2)
    return base + step
end
print(calculateOffset(5)) # => 15 (5 + 10)
</code></pre>

<h2 id="rest-parameters">Rest Parameters (<code>...args</code>)</h2>
<p>Variadic functions accept any number of trailing arguments packed into an Array:</p>

<pre><code class="language-dz">fn sumAll(initial, ...rest)
    let total = initial
    for val in rest
        total += val
    end
    return total
end

print(sumAll(10, 1, 2, 3, 4)) # => 20
</code></pre>

<h2 id="lexical-closures">Lexical Closures</h2>
<p>Functions maintain a reference to their enclosing scope even after the outer function has returned:</p>

<pre><code class="language-dz">fn createCounter(start = 0)
    let count = start
    return fn()
        count++
        return count
    end
end

let c1 = createCounter(10)
print(c1()) # => 11
print(c1()) # => 12

let c2 = createCounter(100)
print(c2()) # => 101 (independent closure environment)
</code></pre>
'''

    # 11. OOP
    pages["docs/language-guide/oop.html"] = '''
<h1 id="classes-oop">Classes & Object-Oriented Programming</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair provides an intuitive class-based OOP model with constructors (<code>init</code>), instance state (<code>self</code>), single inheritance (<code>is</code>), parent dispatch (<code>super</code>), and type verification (<code>instanceof</code>).
</p>

<h2 id="defining-classes">Declaring Classes & Instantiation</h2>
<pre><code class="language-dz">class Person
    init(name, age)
        self.name = name
        self.age = age
    end

    greet()
        print("Hi, I am ${self.name}, age ${self.age}.")
    end
end

# Instantiating with new
let p = new Person("Riad", 28)
p.greet() # => Hi, I am Riad, age 28.
</code></pre>

<h2 id="inheritance-super">Inheritance & <code>super</code></h2>
<p>Classes inherit using the <code>is</code> keyword. Child classes invoke parent constructors via <code>super.init(...)</code>:</p>

<pre><code class="language-dz">class Person
    init(name, age)
        self.name = name
        self.age = age
    end
end

class Employee is Person
    init(name, age, role)
        super.init(name, age)
        self.role = role
    end

    # Overriding method
    greet()
        print("Hello, I am ${self.name}, working as a ${self.role}.")
    end
end

let emp = new Employee("Sarah", 32, "Lead Architect")
emp.greet() # => Hello, I am Sarah, working as a Lead Architect.
</code></pre>

<h2 id="instanceof-checks">Type Verification with <code>instanceof</code></h2>
<p>The <code>instanceof</code> operator verifies whether an object is an instance of a class, its superclasses, or primitive type names:</p>

<pre><code class="language-dz">class Person
end

class Employee is Person
end

let emp = new Employee()

print(emp instanceof Employee)  # => True
print(emp instanceof Person)    # => True (inherited)
print(emp instanceof "String")  # => False

# Can also check primitive string types:
print("hello" instanceof "String") # => True
print(42 instanceof "Number")      # => True
</code></pre>
'''

    # 12. Error Handling
    pages["docs/language-guide/error-handling.html"] = '''
<h1 id="error-handling">Error Handling & Exceptions</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair uses structured exception handling with <code>try</code>, <code>catch</code>, <code>finally</code>, and <code>throw</code> to gracefully handle runtime errors and guarantee resource cleanup.
</p>

<h2 id="try-catch-finally">Try, Catch, Finally</h2>
<pre><code class="language-dz">try
    let divisor = 0
    if divisor == 0
        throw "Division by zero is not permitted"
    end
catch err
    print("Caught error: ${err}")
finally
    print("Cleanup logic executed unconditionally")
end
# => Caught error: Division by zero is not permitted
# => Cleanup logic executed unconditionally
</code></pre>

<h2 id="nested-exceptions">Nested Exceptions & Rethrowing</h2>
<p>Exceptions propagate up the call stack until caught. You can catch an error, perform logging, and rethrow:</p>

<pre><code class="language-dz">fn processFile(filename)
    try
        # Attempt operation
        throw "FileNotFound: ${filename}"
    catch e
        print("Log: failed to process ${filename}")
        throw e # Rethrow error to caller
    end
end

try
    processFile("config.json")
catch e
    print("Top-level handler received: ${e}")
end
</code></pre>
'''

    # 13. Modules & Imports
    pages["docs/language-guide/modules.html"] = '''
<h1 id="modules-imports">Modules & Code Organization</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  Djazair provides two distinct import mechanisms: <code>import</code> for user-defined script files, and <code>use</code> for built-in standard library modules.
</p>

<h2 id="import-local-files">Importing Local Files (<code>import</code>)</h2>
<p>Suppose you have a utility file named <code>math_utils.dz</code>:</p>

<pre><code class="language-dz"># math_utils.dz
fn square(x)
    return x * x
end

fn cube(x)
    return x * x * x
end
</code></pre>

<p>You can import it in your main script using three different styles:</p>

<pre><code class="language-dz"># 1. Standard import (module namespace matches filename)
import "math_utils.dz"
print(math_utils.square(5)) # => 25

# 2. Named alias import
import "math_utils.dz" as mu
print(mu.cube(3))           # => 27

# 3. Wildcard import (imports all top-level functions directly)
import "math_utils.dz" as *
print(square(4))            # => 16
</code></pre>

<h2 id="use-standard-library">Standard Library Imports (<code>use</code>)</h2>
<p>Standard library modules are loaded with the <code>use</code> keyword:</p>

<pre><code class="language-dz"># Standard import
use json
use math

let parsed = json.decode('{"val": 16}')
print(math.sqrt(parsed["val"])) # => 4.0

# With alias
use datetime as dt
print(dt.now().format("%Y-%m-%d"))

# Wildcard stdlib import
use math as *
print(ceil(3.14)) # Direct access to ceil()
</code></pre>
'''

    return pages
