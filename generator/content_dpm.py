"""
=============================================================================
Djazair Static Documentation — DPM Package Manager (content_dpm.py)
Dedicated standalone section for Djazair Package Manager (DPM).
=============================================================================
"""

def get_dpm_pages() -> dict:
    pages = {}

    pages["docs/dpm/index.html"] = r'''
<h1 id="dpm">Djazair Package Manager (DPM)</h1>
<p class="lead" style="font-size:1.15rem; color:var(--text-secondary); margin-bottom:1.75rem;">
  <strong>DPM</strong> is the official, self-hosted package manager and build orchestrator for the Djazair Programming Language. Written natively in Djazair, DPM provides project scaffolding, Semantic Versioning (SemVer) dependency resolution, multi-source downloading (GitHub monorepos, Git repositories, HTTP ZIPs, and local archives), isolated per-project dependency trees, global tool installations, and automated native compilation for hybrid C/C++ packages.
</p>

<div class="callout callout-info" style="margin-bottom:2rem;">
  <div style="font-weight:700; margin-bottom:0.35rem;"><i class="fa-solid fa-circle-info"></i> Native Architecture</div>
  <p style="margin:0;">DPM is implemented as a core Djazair application (<code>dpm/init.dz</code>) and can be executed either directly via the standalone <code>dpm</code> wrapper script (<code>dpm.bat</code> on Windows, <code>dpm</code> on POSIX) or through the language driver: <code>djazair dpm &lt;command&gt;</code>.</p>
</div>

<h2 id="architecture-concepts">Architecture & Core Concepts</h2>
<p>DPM is architected around deterministic dependency management, clean isolation, and cross-platform portability. Understanding these foundations is essential for developing production-grade applications and reusable packages in Djazair.</p>

<h3 id="local-vs-global">Local Isolation vs Global Scope</h3>
<p>DPM operates in two distinct execution modes:</p>
<ul>
  <li><strong>Local Project Scope (Default):</strong> Dependencies are installed strictly within the project directory inside the isolated <code>djazair_packages/</code> folder. Modifications are recorded directly in the project's root <code>dpm.json</code> manifest. This ensures completely reproducible builds and guarantees that two projects on the same machine can safely depend on different versions of the same library without conflict.</li>
  <li><strong>Global System Scope (<code>-g</code>, <code>--global</code>):</strong> Installs packages system-wide in the language runtime directory (or <code>~/.djazair/packages</code>). This mode is ideal for developer command-line tools, language extensions, and global utilities that need to be accessible from any working directory.</li>
</ul>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Scope</th>
        <th>Default Installation Directory</th>
        <th>Manifest Impact</th>
        <th>Primary Use Case</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Local</strong> (Default)</td>
        <td><code>&lt;project_root&gt;/djazair_packages/</code></td>
        <td>Pinned to root <code>dpm.json</code> (<code>require</code>)</td>
        <td>Application libraries, database drivers, framework plugins</td>
      </tr>
      <tr>
        <td><strong>Global</strong> (<code>-g</code>)</td>
        <td><code>&lt;djazair_root&gt;/packages/</code> or <code>~/.djazair/packages/</code></td>
        <td>None (standalone installation)</td>
        <td>CLI utilities, linters, system-wide code generators</td>
      </tr>
    </tbody>
  </table>
</div>

<h3 id="package-types">Package Classification: Pure vs Hybrid</h3>
<p>DPM explicitly recognizes two primary categories of packages:</p>
<ol>
  <li><strong>Pure Packages (<code>"type": "pure"</code>):</strong> Built entirely in Djazair source code (<code>.dz</code> files). They require no external compiler toolchain, install instantaneously across all operating systems (Windows, Linux, macOS), and have zero native binary dependencies.</li>
  <li><strong>Hybrid Packages (<code>"type": "hybrid"</code>):</strong> Contain both Djazair wrapper code and low-level C or C++ extensions (e.g., SQLite, WebSockets, image processing). They declare platform-specific build scripts (<code>build.bat</code> on Windows, <code>build.sh</code> on POSIX) and link against the Djazair C runtime header files (<code>djazair_api.h</code>) and static library (<code>libdjazair.a</code>).</li>
</ol>

<h3 id="resolution-hierarchy">Runtime Module Resolution Hierarchy</h3>
<p>When your Djazair script issues an <code>import</code> or <code>use</code> statement, the interpreter resolves packages in the following strictly defined order:</p>
<ol>
  <li><strong>Project-Local Directory Package:</strong> <code>&lt;project_root&gt;/djazair_packages/&lt;name&gt;/init.dz</code></li>
  <li><strong>Project-Local Single-File Package:</strong> <code>&lt;project_root&gt;/djazair_packages/&lt;name&gt;.dz</code></li>
  <li><strong>Global System Package:</strong> <code>&lt;djazair_root&gt;/packages/&lt;name&gt;/init.dz</code></li>
  <li><strong>Built-In Standard Library:</strong> Embedded C/Djazair standard modules (e.g., <code>math</code>, <code>json</code>, <code>http</code>, <code>file</code>).</li>
</ol>

---

<h2 id="semver-engine">Semantic Versioning (SemVer 2.0.0 Engine)</h2>
<p>DPM embeds an internal, full-featured SemVer parsing and evaluation engine (<code>dpm/core/semver.dz</code>). When declaring dependencies or updating packages, DPM evaluates version constraints to ensure breaking changes are never introduced unintentionally.</p>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Constraint Pattern</th>
        <th>Example</th>
        <th>Matching Versions</th>
        <th>Behavior & Rationale</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Caret (<code>^</code>)</strong> (Default)</td>
        <td><code>^1.2.0</code></td>
        <td><code>1.2.0</code>, <code>1.2.3</code>, <code>1.9.9</code> (Rejects <code>2.0.0</code>)</td>
        <td>Allows backwards-compatible minor and patch updates. For zero-major versions (<code>^0.2.0</code>), minor increments are treated as breaking (matches <code>0.2.x</code>, rejects <code>0.3.0</code>).</td>
      </tr>
      <tr>
        <td><strong>Tilde (<code>~</code>)</strong></td>
        <td><code>~1.2.0</code></td>
        <td><code>1.2.0</code>, <code>1.2.9</code> (Rejects <code>1.3.0</code>)</td>
        <td>Restricts updates strictly to patch releases. Useful when minor versions might alter API behavior.</td>
      </tr>
      <tr>
        <td><strong>Exact</strong></td>
        <td><code>1.2.3</code></td>
        <td>Only <code>1.2.3</code></td>
        <td>Locks dependency to an exact release. Essential for ultra-deterministic critical deployments.</td>
      </tr>
      <tr>
        <td><strong>Wildcard / Latest</strong></td>
        <td><code>*</code> or <code>latest</code></td>
        <td>Any version</td>
        <td>Matches the absolute latest release found upstream.</td>
      </tr>
      <tr>
        <td><strong>Comparison Operators</strong></td>
        <td><code>&gt;=1.0.0 &lt;2.0.0</code></td>
        <td>Any version in range</td>
        <td>Supports standard relational bounds (<code>&gt;=</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&lt;</code>).</td>
      </tr>
      <tr>
        <td><strong>Pre-Release Identifiers</strong></td>
        <td><code>1.0.0-rc.1</code></td>
        <td>SemVer pre-release</td>
        <td>Parsed cleanly via <code>semver.parse()</code>, allowing development candidate tracking.</td>
      </tr>
    </tbody>
  </table>
</div>

---

<h2 id="cli-reference">Complete CLI Reference & Workflows</h2>
<p>DPM commands share a consistent interface, intuitive aliases, and standardized flag behavior:</p>

<pre><code class="language-bash">dpm &lt;command&gt; [options] [arguments]
# or
djazair dpm &lt;command&gt; [options] [arguments]
</code></pre>

<h3 id="global-options">Global Command-Line Flags</h3>
<ul>
  <li><code>-g</code>, <code>--global</code>: Target the global language packages directory instead of the project-local workspace.</li>
  <li><code>-q</code>, <code>--quiet</code>: Run quietly, suppressing all non-error informational logs.</li>
  <li><code>--verbose</code>: Enable verbose diagnostic traces, showing git command outputs and path resolution steps.</li>
  <li><code>-v</code>, <code>--version</code>: Print DPM version, Djazair engine version, host OS platform, and author info.</li>
  <li><code>-h</code>, <code>--help</code>: Display interactive help screen.</li>
</ul>

<h3 id="cmd-init">1. Project Scaffolding: <code>dpm init</code></h3>
<p>Initializes a new Djazair project or library package. It launches an interactive wizard that prompts for project metadata and automatically generates a standard <code>dpm.json</code> manifest, starter entrypoint, <code>.gitignore</code>, and <code>README.md</code>.</p>

<pre><code class="language-bash"># Interactive scaffolding wizard
dpm init

# Non-interactive mode (accepts all sensible defaults immediately)
dpm init --yes
# or
dpm init -y
</code></pre>

<p>When run, <code>dpm init</code> scaffolds the following standard directory structure:</p>
<pre><code class="language-bash">my_project/
├── dpm.json         # Package manifest & dependency declarations
├── init.dz          # Primary entrypoint with starter function
├── .gitignore       # Pre-configured to ignore djazair_packages/ and build binaries
└── README.md        # Formatted markdown documentation with install/usage examples
</code></pre>

<div class="callout callout-tip">
  <div style="font-weight:700; margin-bottom:0.35rem;"><i class="fa-solid fa-lightbulb"></i> Automatic Git Safety</div>
  <p style="margin:0;">The generated <code>.gitignore</code> automatically excludes <code>djazair_packages/</code>, native build artifacts (<code>*.dll</code>, <code>*.so</code>, <code>*.dylib</code>, <code>*.o</code>, <code>*.a</code>), build flags (<code>.built</code>), and the DPM temporary cache (<code>.dpm_cache/</code>). This ensures you never accidentally commit downloaded dependencies or compiled binaries to source control.</p>
</div>

<h3 id="cmd-install">2. Package Installation: <code>dpm install</code></h3>
<p>The <code>install</code> command (aliases: <code>i</code>, <code>add</code>) handles both batch dependency synchronization and single package retrieval.</p>

<h4 id="batch-install">Batch Manifest Installation</h4>
<p>Running <code>dpm install</code> without arguments reads the local <code>dpm.json</code>, parses the <code>require</code> block, and recursively downloads, verifies, and installs every listed dependency:</p>
<pre><code class="language-bash">dpm install
</code></pre>

<h4 id="multi-source-formats">Supported Package Specifiers & Source Formats</h4>
<p>DPM supports an exceptionally versatile range of source identifiers:</p>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Source Format</th>
        <th>Syntax Example</th>
        <th>Resolution Mechanism</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Shorthand Name</strong></td>
        <td><code>dpm install sqlite</code><br><code>dpm install qalam</code></td>
        <td>Checks local offline packages (<code>&lt;djazair_root&gt;/packages/</code>) first; if not found, fetches from the official extensions monorepo (<code>github:djazair-language/djazair-extensions/&lt;name&gt;</code>).</td>
      </tr>
      <tr>
        <td><strong>GitHub Monorepo Subdirectory</strong></td>
        <td><code>dpm install github:org/repo/subfolder</code></td>
        <td>Clones/caches the repository and extracts the specified subdirectory as a standalone package.</td>
      </tr>
      <tr>
        <td><strong>GitHub Repository Shorthand</strong></td>
        <td><code>dpm install github:user/repo</code></td>
        <td>Clones directly from <code>https://github.com/user/repo.git</code>.</td>
      </tr>
      <tr>
        <td><strong>Direct Git URL</strong></td>
        <td><code>dpm install https://github.com/team/auth.git</code></td>
        <td>Executes shallow clone (<code>--depth 1</code>), cleans up <code>.git</code> metadata, and places package in <code>djazair_packages/auth</code>.</td>
      </tr>
      <tr>
        <td><strong>Direct HTTP/HTTPS ZIP Archive</strong></td>
        <td><code>dpm install https://cdn.example.com/matrix.zip</code></td>
        <td>Downloads archive to DPM cache and extracts cleanly into project packages.</td>
      </tr>
      <tr>
        <td><strong>Local Directory or Archive</strong></td>
        <td><code>dpm install ./libs/my-custom-pkg</code><br><code>dpm install ../archives/pkg.zip</code></td>
        <td>Copies local filesystem directory or extracts local archive directly into <code>djazair_packages/</code>.</td>
      </tr>
    </tbody>
  </table>
</div>

<h4 id="install-flags">Installation Modifiers</h4>
<pre><code class="language-bash"># Install globally into language packages directory
dpm install -g qalam

# Install without updating the root dpm.json manifest
dpm install sqlite --no-save

# Force re-download and re-install even if package directory exists
dpm install sqlite --force
</code></pre>

<h3 id="cmd-update">3. Package Upgrades: <code>dpm update</code></h3>
<p>The <code>update</code> command (alias: <code>up</code>) inspects installed packages against their remote origin. For Git-backed packages, DPM queries remote tags (<code>git ls-remote --tags</code>), compares available versions using its SemVer engine, and upgrades the package when a newer compatible version is detected.</p>

<pre><code class="language-bash"># Update a specific package locally
dpm update sqlite

# Update all installed packages in the current project
dpm update *
# or
dpm update

# Update a globally installed package
dpm update -g qalam

# Force re-installation of the latest version
dpm update sqlite --force
</code></pre>

<h3 id="cmd-remove">4. Package Uninstallation: <code>dpm remove</code></h3>
<p>The <code>remove</code> command (aliases: <code>rm</code>, <code>uninstall</code>) safely deletes a package from <code>djazair_packages/</code> and automatically removes its dependency constraint from <code>dpm.json</code>:</p>

<pre><code class="language-bash"># Remove package locally and update dpm.json
dpm remove sqlite

# Remove a globally installed package
dpm remove -g qalam
</code></pre>

<h3 id="cmd-list">5. Inventory Inspection: <code>dpm list</code></h3>
<p>The <code>list</code> command (alias: <code>ls</code>) scans the packages directory and outputs a cleanly formatted table of all installed packages, their detected versions, and package types:</p>

<pre><code class="language-bash"># List project-local packages
dpm list

# List globally installed packages
dpm list -g
</code></pre>

<h3 id="cmd-info">6. Deep Metadata Inspection: <code>dpm info</code></h3>
<p>The <code>info</code> command (alias: <code>show</code>) prints an exhaustive diagnostic report for any package, including its scope, installation location, entrypoint, author, dependency map, update availability, and file inventory:</p>

<pre><code class="language-bash">dpm info sqlite
</code></pre>

<pre><code class="language-text">Package Information: sqlite
----------------------------------------------------
  Name:        sqlite
  Scope:       Local
  Location:    D:\Projects\app\djazair_packages\sqlite
  Version:     1.0.0
  Type:        hybrid
  Description: SQLite native embedded database engine for Djazair
  Source:      github:djazair-language/djazair-extensions/sqlite
  Entrypoint:  init.dz
  Developer:   Harizi Riyadh &lt;hariziriyadh@gmail.com&gt;
  Dependencies: None
  Files (6):   dpm.json, init.dz, build.bat, build.sh, sqlite3.c, sqlite3.h
</code></pre>

<h3 id="cmd-pack">7. Distributable Bundling: <code>dpm pack</code></h3>
<p>Packages the current project or library into a clean, distributable ZIP archive named <code>&lt;name&gt;-&lt;version&gt;.zip</code>. It automatically excludes local dependencies (<code>djazair_packages/</code>), compiled binaries, and temporary files, producing a production-ready distribution artifact ready to be published or shared.</p>

<pre><code class="language-bash">dpm pack
# Output: Package archive created: 'D:\Projects\my_lib\my_lib-1.0.0.zip'
</code></pre>

---

<h2 id="manifest-specification">Package Manifest (<code>dpm.json</code>) Specification</h2>
<p>The <code>dpm.json</code> file is the single source of truth for any Djazair project or distributable library. Below is the complete annotated specification:</p>

<pre><code class="language-json">{
  "name": "super_cache",
  "version": "1.2.0",
  "description": "High-performance LRU cache and memory storage for Djazair",
  "type": "pure",
  "entry": "init.dz",
  "source": "github:developer/super_cache",
  "developer": {
    "name": "Harizi Riyadh",
    "email": "hariziriyadh@gmail.com"
  },
  "require": {
    "qalam": "^0.2.0",
    "sqlite": "~1.0.0"
  },
  "build": {
    "windows": "build.bat",
    "linux": "./build.sh"
  }
}
</code></pre>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Required</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>name</code></td>
        <td>String</td>
        <td><strong>Yes</strong></td>
        <td>The unique identifier of the package. Must use lowercase alphanumeric characters, dashes, or underscores (e.g. <code>"json_validator"</code>).</td>
      </tr>
      <tr>
        <td><code>version</code></td>
        <td>String</td>
        <td><strong>Yes</strong></td>
        <td>Valid SemVer 2.0.0 string (<code>MAJOR.MINOR.PATCH[-PRERELEASE]</code>).</td>
      </tr>
      <tr>
        <td><code>description</code></td>
        <td>String</td>
        <td>No</td>
        <td>Concise overview of the package's purpose and functionality.</td>
      </tr>
      <tr>
        <td><code>type</code></td>
        <td>String</td>
        <td><strong>Yes</strong></td>
        <td>Either <code>"pure"</code> (Djazair code only) or <code>"hybrid"</code> (contains native C/C++ build steps).</td>
      </tr>
      <tr>
        <td><code>entry</code></td>
        <td>String</td>
        <td>No</td>
        <td>Main entrypoint file executed when the package is imported. Defaults to <code>"init.dz"</code>.</td>
      </tr>
      <tr>
        <td><code>source</code></td>
        <td>String</td>
        <td>No</td>
        <td>Upstream repository specifier (e.g. <code>"github:org/repo"</code> or Git URL) used for automated updates.</td>
      </tr>
      <tr>
        <td><code>developer</code></td>
        <td>Object</td>
        <td>No</td>
        <td>Metadata map containing author <code>"name"</code> and <code>"email"</code>.</td>
      </tr>
      <tr>
        <td><code>require</code></td>
        <td>Object</td>
        <td>No</td>
        <td>Dictionary of package dependencies mapped to SemVer constraints (e.g., <code>{"qalam": "^0.2.0"}</code>).</td>
      </tr>
      <tr>
        <td><code>build</code></td>
        <td>Object</td>
        <td>No (Hybrid only)</td>
        <td>Cross-platform build scripts for hybrid packages (e.g., <code>"windows": "build.bat"</code>, <code>"linux": "./build.sh"</code>).</td>
      </tr>
    </tbody>
  </table>
</div>

---

<h2 id="step-by-step-tutorial">Professional Tutorial: Creating & Publishing a Package</h2>
<p>Follow this end-to-end walkthrough to create, structure, test, bundle, and distribute a professional Djazair package.</p>

<h3 id="step-1-scaffold">Step 1: Scaffolding the Package</h3>
<p>Create a dedicated directory for your library and initialize it with DPM:</p>
<pre><code class="language-bash">mkdir string_utils
cd string_utils
dpm init
</code></pre>
<p>Fill in the interactive prompts:</p>
<pre><code class="language-text">Package name (string_utils): string_utils
Version (0.1.0): 1.0.0
Description: Advanced string transformation algorithms for Djazair
Type (pure/hybrid) [pure]: pure
Author Name: Harizi Riyadh
Author Email: hariziriyadh@gmail.com
</code></pre>

<h3 id="step-2-architecture">Step 2: Designing the Package Architecture</h3>
<p>A professional package organizes its internal logic under a <code>src/</code> directory and exports a clean public API through <code>init.dz</code>:</p>

<pre><code class="language-bash">string_utils/
├── dpm.json
├── init.dz
├── src/
│   ├── case.dz
│   └── slugify.dz
├── tests/
│   └── test_string_utils.dz
└── README.md
</code></pre>

<p>Write your internal modules inside <code>src/</code>:</p>
<pre><code class="language-ruby"># src/slugify.dz
fn toSlug(text)
    let clean = text.lower().strip()
    let result = ""
    for ch in clean
        if (ch &gt;= "a" and ch &lt;= "z") or (ch &gt;= "0" and ch &lt;= "9")
            result = result + ch
        elif ch == " " or ch == "_" or ch == "-"
            if !result.endsWith("-") and result.length() &gt; 0
                result = result + "-"
            end
        end
    end
    return result
end
</code></pre>

<p>Expose your public functions in the package entrypoint (<code>init.dz</code>):</p>
<pre><code class="language-ruby"># init.dz — Public API Gateway
import "src/slugify.dz" as slug

# Re-export clean functions
fn slugify(text)
    return slug.toSlug(text)
end

fn version()
    return "1.0.0"
end
</code></pre>

<h3 id="step-3-dependencies">Step 3: Managing Dependencies</h3>
<p>If your package requires helper libraries (e.g. <code>qalam</code> for colored output or logging), install them directly:</p>
<pre><code class="language-bash">dpm install qalam
</code></pre>
<p>DPM installs <code>qalam</code> into <code>djazair_packages/qalam</code> and automatically records <code>"qalam": "^0.2.0"</code> in your <code>dpm.json</code>.</p>

<h3 id="step-4-testing">Step 4: Writing Unit Tests</h3>
<p>Create a test runner under <code>tests/test_string_utils.dz</code> utilizing the standard <code>assert</code> library:</p>
<pre><code class="language-ruby"># tests/test_string_utils.dz
use assert
import "../init.dz" as string_utils

print("==&gt; Testing string_utils...")

assert.equal(string_utils.slugify("Hello World! 2026"), "hello-world-2026", "Slugification failed")
assert.equal(string_utils.slugify("Djazair   Programming"), "djazair-programming", "Multiple spaces failed")

print("==&gt; All tests passed successfully!")
</code></pre>
<p>Execute your tests:</p>
<pre><code class="language-bash">djazair tests/test_string_utils.dz
</code></pre>

<h3 id="step-5-bundling">Step 5: Packaging & Publishing</h3>
<p>When ready for release, bundle your package using <code>dpm pack</code>:</p>
<pre><code class="language-bash">dpm pack
# Produces: string_utils-1.0.0.zip
</code></pre>

<p>To publish via Git, push your code to GitHub with a SemVer release tag:</p>
<pre><code class="language-bash">git init
git add .
git commit -m "Release v1.0.0"
git tag v1.0.0
git remote add origin https://github.com/myusername/string_utils.git
git push -u origin main --tags
</code></pre>

<h3 id="step-6-consuming">Step 6: Consuming the Published Package</h3>
<p>Other developers can now install and consume your package directly:</p>
<pre><code class="language-bash"># Install via GitHub shorthand
dpm install github:myusername/string_utils

# Or install from direct ZIP release
dpm install https://github.com/myusername/string_utils/releases/download/v1.0.0/string_utils-1.0.0.zip
</code></pre>

<p>In consumer code:</p>
<pre><code class="language-ruby">use string_utils

let slug = string_utils.slugify("Building with Djazair and DPM")
print("Generated Slug: " + slug)
# Output: Generated Slug: building-with-djazair-and-dpm
</code></pre>

---

<h2 id="hybrid-packages">Authoring Hybrid Packages (C/C++ Extensions)</h2>
<p>Hybrid packages bridge high-performance C or C++ shared libraries into the Djazair runtime. DPM automates native builds by orchestrating cross-platform build scripts.</p>

<h3 id="hybrid-structure">Hybrid Package Layout</h3>
<pre><code class="language-bash">fast_hash/
├── dpm.json         # Declares "type": "hybrid" and "build" scripts
├── init.dz          # Djazair bindings loading the native library
├── build.bat        # Windows compilation script (MinGW / MSVC)
├── build.sh         # Linux & macOS compilation script (GCC / Clang)
└── src/
    ├── native.c     # C implementation using Djazair C API
    └── native.h
</code></pre>

<h3 id="hybrid-manifest">Hybrid <code>dpm.json</code></h3>
<pre><code class="language-json">{
  "name": "fast_hash",
  "version": "1.0.0",
  "description": "Native high-speed hashing module for Djazair",
  "type": "hybrid",
  "entry": "init.dz",
  "build": {
    "windows": "build.bat",
    "linux": "./build.sh"
  }
}
</code></pre>

<h3 id="cross-platform-build-scripts">Standard Build Scripts</h3>
<p>DPM sets the <code>DJAZAIR_ROOT</code> environment variable before executing your build scripts. Your scripts should reference the Djazair header files in <code>$DJAZAIR_ROOT/src/include</code> and link against <code>libdjazair</code>:</p>

<div class="tabs-container">
  <div class="tabs-header">
    <button class="tab-btn active" onclick="switchTab(event, 'tab-win')">build.bat (Windows)</button>
    <button class="tab-btn" onclick="switchTab(event, 'tab-posix')">build.sh (Linux/macOS)</button>
  </div>

  <div id="tab-win" class="tab-content active">
<pre><code class="language-bash">@echo off
setlocal

:: Set include and library directories
if "%DJAZAIR_ROOT%"=="" set DJAZAIR_ROOT=..\..

gcc -O3 -shared -fPIC ^
    -I"%DJAZAIR_ROOT%\src\include" ^
    -o fast_hash.dll ^
    src\native.c ^
    -L"%DJAZAIR_ROOT%\build\lib" -ldjazair

if %ERRORLEVEL% equ 0 (
    echo [OK] fast_hash.dll compiled successfully.
    exit /b 0
) else (
    echo [ERROR] Compilation failed.
    exit /b 1
)
</code></pre>
  </div>

  <div id="tab-posix" class="tab-content">
<pre><code class="language-bash">#!/usr/bin/env bash
set -e

: "${DJAZAIR_ROOT:=../..}"

gcc -O3 -shared -fPIC \
    -I"${DJAZAIR_ROOT}/src/include" \
    -o fast_hash.so \
    src/native.c \
    -L"${DJAZAIR_ROOT}/build/lib" -ldjazair

echo "[OK] fast_hash.so compiled successfully."
</code></pre>
  </div>
</div>

---

<h2 id="programmatic-api">Programmatic Package Inspection via <code>lang</code></h2>
<p>Djazair's standard library <code>lang</code> module provides native functions to inspect packages and query update states directly from your running scripts:</p>

<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Function</th>
        <th>Return Type</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>lang.packagesDir()</code></td>
        <td><code>String</code></td>
        <td>Returns the absolute path to the active global packages directory.</td>
      </tr>
      <tr>
        <td><code>lang.packageExist(name, [isGlobal])</code></td>
        <td><code>Boolean</code></td>
        <td>Checks if a package exists locally or globally. Alias: <code>lang.packageExists()</code>.</td>
      </tr>
      <tr>
        <td><code>lang.checkPackageUpdate(name, [isGlobal])</code></td>
        <td><code>Map</code></td>
        <td>Returns a dictionary with <code>isInstalled</code>, <code>hasUpdate</code>, <code>currentVersion</code>, <code>latestVersion</code>, <code>path</code>, and <code>scope</code>.</td>
      </tr>
      <tr>
        <td><code>lang.hasUpdate(name, [isGlobal])</code></td>
        <td><code>Boolean</code></td>
        <td>Convenience predicate checking if a newer version is available upstream.</td>
      </tr>
    </tbody>
  </table>
</div>

<h3 id="runtime-check-example">Real-World Dynamic Inspection Example</h3>
<pre><code class="language-ruby">use lang

# Check if SQLite package is available
if lang.packageExist("sqlite")
    let info = lang.checkPackageUpdate("sqlite")
    print("SQLite Version: " + info["currentVersion"])
    print("Installed Path: " + info["path"])

    if info["hasUpdate"]
        print("Notice: A newer SQLite release (v" + info["latestVersion"] + ") is available!")
        print("Run 'dpm update sqlite' to upgrade.")
    end
else
    print("SQLite is not installed. Please run: dpm install sqlite")
end
</code></pre>

---

<h2 id="best-practices">Production & CI/CD Best Practices</h2>

<h3 id="git-repository-hygiene">1. Git Repository Hygiene</h3>
<ul>
  <li><strong>Always commit <code>dpm.json</code>:</strong> The manifest defines exact version bounds and is critical for team collaboration.</li>
  <li><strong>Never commit <code>djazair_packages/</code>:</strong> Always ignore dependencies in <code>.gitignore</code>. Team members and CI servers will reconstitute them deterministically using <code>dpm install</code>.</li>
  <li><strong>Never commit binary artifacts:</strong> Ensure <code>*.dll</code>, <code>*.so</code>, <code>*.dylib</code>, and <code>.dpm_cache/</code> are gitignored.</li>
</ul>

<h3 id="ci-cd-pipelines">2. Continuous Integration (CI/CD) Configuration</h3>
<p>In automated GitHub Actions or GitLab CI environments, incorporate DPM dependency synchronization into your build matrix:</p>

<pre><code class="language-yaml"># .github/workflows/ci.yml
name: Test Suite

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source
        uses: actions/checkout@v4

      - name: Setup Djazair & DPM
        run: |
          sudo apt-get update && sudo apt-get install -y gcc make
          # Build or install Djazair binaries
          make install

      - name: Install Project Dependencies
        run: dpm install

      - name: Run Test Suite
        run: djazair tests/run_all.dz
</code></pre>

<h3 id="troubleshooting">3. Troubleshooting Common Issues</h3>
<ul>
  <li><strong>Git is not recognized:</strong> DPM relies on the system <code>git</code> command to fetch repositories. Ensure Git is installed and added to your system <code>PATH</code>.</li>
  <li><strong>Compiler toolchain missing for hybrid packages:</strong> On Windows, ensure MinGW GCC (e.g. MSYS2 or WinLibs) is in your <code>PATH</code>. On Linux, install <code>build-essential</code> (GCC/Clang and Make).</li>
  <li><strong>Cleaning Cache:</strong> DPM caches monorepos and downloaded archives in your OS temporary directory under <code>dpm_cache/</code>. To clear stale caches, delete the directory:
    <pre><code class="language-bash"># Windows PowerShell
Remove-Item -Recurse -Force "$env:TEMP\dpm_cache"

# Linux / macOS
rm -rf /tmp/dpm_cache
</code></pre>
  </li>
</ul>
'''

    return pages
