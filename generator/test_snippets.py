#!/usr/bin/env python3
"""
Test harness for Djazair documentation code snippets.
Extracts code blocks from HTML pages and executes them against `djazair`.
"""

import os
import sys
import re
import html
import tempfile
import subprocess

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from generator.content_getting_started import get_getting_started_pages
from generator.content_language_guide import get_language_guide_pages
from generator.content_dpm import get_dpm_pages
from generator.content_stdlib_1 import get_stdlib_part1_pages
from generator.content_stdlib_2 import get_stdlib_part2_pages
from generator.content_packages_embedding import get_packages_embedding_pages

def extract_snippets():
    content_map = {}
    content_map.update(get_getting_started_pages())
    content_map.update(get_language_guide_pages())
    content_map.update(get_dpm_pages())
    content_map.update(get_stdlib_part1_pages())
    content_map.update(get_stdlib_part2_pages())
    content_map.update(get_packages_embedding_pages())

    snippets = []
    pattern = r'<pre><code class="language-(?:dz|ruby|djazair)">(.*?)</code></pre>'

    for page_path, page_html in content_map.items():
        matches = re.finditer(pattern, page_html, re.DOTALL)
        for idx, m in enumerate(matches):
            raw_code = m.group(1)
            clean_code = html.unescape(raw_code).strip()
            snippets.append({
                "file": page_path,
                "index": idx + 1,
                "code": clean_code
            })

    return snippets

def is_runnable(code: str) -> tuple[bool, str]:
    # Check for conceptual ellipsis
    lines = code.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped == '...' or stripped.startswith('... #') or stripped == '# ...':
            return False, "Contains conceptual ellipsis '...'"

    # Check for infinite loops or long-running servers
    if 'server.listen' in code or 'listen(8080)' in code or 'listen(3000)' in code:
        return False, "Long-running server/listen call"
    if 'while True' in code and 'break' not in code and 'return' not in code:
        return False, "Infinite loop while True"

    # Check for pseudo paths that cannot exist
    if '"path/to/' in code or '"/path/to/' in code or 'your_project' in code:
        return False, "Contains placeholder path"

    # Check for single-line fragments that don't do anything or import missing files
    if 'import "../init.dz"' in code or 'import "src/' in code or 'import "my_module.dz"' in code or 'import "math_utils.dz"' in code:
        return False, "Relative import of tutorial-only local file"

    # Check for tutorial fictional package
    if 'use string_utils' in code:
        return False, "Tutorial fictional package"

    return True, "OK"

def main():
    snippets = extract_snippets()
    print(f"==================================================")
    print(f" Found {len(snippets)} Djazair code snippets in documentation")
    print(f"==================================================\n")

    passed = 0
    failed = 0
    skipped = 0
    failures = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for s in snippets:
            file_name = s["file"]
            idx = s["index"]
            code = s["code"]

            runnable, reason = is_runnable(code)
            if not runnable:
                skipped += 1
                # print(f"  [SKIP] {file_name} #{idx} — {reason}")
                continue

            test_file = os.path.join(tmpdir, f"test_{abs(hash(file_name))}_{idx}.dz")
            with open(test_file, 'w', encoding='utf-8') as tf:
                tf.write(code)

            try:
                # Provide simulated input if input() is called
                simulated_stdin = b"test_input\n42\nyes\n"
                proc = subprocess.run(
                    ["djazair", test_file],
                    input=simulated_stdin,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=6,
                    cwd=tmpdir
                )

                if proc.returncode == 0:
                    passed += 1
                else:
                    failed += 1
                    err_msg = proc.stderr.decode('utf-8', errors='replace').strip()
                    if not err_msg:
                        err_msg = proc.stdout.decode('utf-8', errors='replace').strip()
                    failures.append({
                        "file": file_name,
                        "index": idx,
                        "code": code,
                        "error": err_msg
                    })
                    print(f"  ❌ [FAIL] {file_name} #{idx}")
                    print(f"     Error: {err_msg[:200]}")
            except subprocess.TimeoutExpired:
                failed += 1
                failures.append({
                    "file": file_name,
                    "index": idx,
                    "code": code,
                    "error": "Execution timed out (> 6s)"
                })
                print(f"  ⏱️ [TIMEOUT] {file_name} #{idx}")
            except Exception as e:
                failed += 1
                failures.append({
                    "file": file_name,
                    "index": idx,
                    "code": code,
                    "error": str(e)
                })
                print(f"  ❌ [ERR] {file_name} #{idx}: {e}")

    print("\n" + "=" * 50)
    print(f" SUMMARY:")
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print(f"  Skipped: {skipped}")
    print(f"==================================================")

    report_path = os.path.join(BASE_DIR, "generator", "test_report.txt")
    with open(report_path, 'w', encoding='utf-8') as rf:
        rf.write(f"TEST SUMMARY:\nPassed: {passed}\nFailed: {failed}\nSkipped: {skipped}\n\n")
        for idx, f in enumerate(failures, 1):
            rf.write(f"====================================================\n")
            rf.write(f"Failure #{idx}: {f['file']} (Block #{f['index']})\n")
            rf.write(f"----------------------------------------------------\n")
            rf.write(f"CODE:\n{f['code']}\n\n")
            rf.write(f"ERROR:\n{f['error']}\n\n")
    print(f"Detailed failures written to: {report_path}")

    sys.exit(1 if failed > 0 else 0)

if __name__ == "__main__":
    main()
