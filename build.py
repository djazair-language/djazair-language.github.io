#!/usr/bin/env python3
"""
=============================================================================
Djazair Static Documentation Site Generator (build.py)
Builds all HTML pages, search indexes, and assets for GitHub Pages deployment.
=============================================================================
"""

import os
import sys
import json
import time

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from generator.layout import SITE_STRUCTURE, ALL_PAGES, render_docs_page
from generator.content_getting_started import get_getting_started_pages
from generator.content_language_guide import get_language_guide_pages
from generator.content_stdlib_1 import get_stdlib_part1_pages
from generator.content_stdlib_2 import get_stdlib_part2_pages
from generator.content_packages_embedding import get_packages_embedding_pages
from generator.content_dpm import get_dpm_pages
from generator.content_landing import render_landing_page

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build_site():
    start_time = time.time()
    print("=" * 70)
    print("  🚀 Building Djazair Documentation Website...")
    print("=" * 70)

    # 1. Collect all pages content
    content_map = {}
    content_map.update(get_getting_started_pages())
    content_map.update(get_language_guide_pages())
    content_map.update(get_dpm_pages())
    content_map.update(get_stdlib_part1_pages())
    content_map.update(get_stdlib_part2_pages())
    content_map.update(get_packages_embedding_pages())

    print(f"\n[1/5] Collected content for {len(content_map)} doc pages.")

    # 2. Render and write documentation pages
    generated_count = 0
    for page in ALL_PAGES:
        rel_path = page["path"]
        if rel_path not in content_map:
            print(f"  ⚠️ Warning: missing content for {rel_path}")
            continue

        raw_content = content_map[rel_path]
        full_html = render_docs_page(page, raw_content)

        target_file = os.path.join(BASE_DIR, rel_path.replace('/', os.sep))
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        generated_count += 1

    # Legacy redirect for docs/language-guide/dpm.html -> ../dpm/index.html
    legacy_dpm_file = os.path.join(BASE_DIR, "docs", "language-guide", "dpm.html")
    with open(legacy_dpm_file, 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=../dpm/index.html">
  <link rel="canonical" href="https://djazair-language.github.io/docs/dpm/index.html">
  <title>Redirecting to DPM Documentation...</title>
  <script>window.location.replace("../dpm/index.html");</script>
</head>
<body>
  <p>Redirecting to <a href="../dpm/index.html">DPM Documentation</a>...</p>
</body>
</html>''')

    print(f"[2/5] Generated {generated_count} documentation pages.")

    # 3. Render and write landing page (index.html)
    landing_html = render_landing_page()
    landing_path = os.path.join(BASE_DIR, "index.html")
    with open(landing_path, 'w', encoding='utf-8') as f:
        f.write(landing_html)
    print(f"[3/5] Generated landing page: index.html")

    # 4. Generate search index (assets/js/search-index.js)
    search_data = []
    for page in ALL_PAGES:
        search_data.append({
            "title": page["title"],
            "category": page["category"],
            "path": page["path"],
            "desc": page["desc"],
            "keywords": page.get("keywords", "")
        })

    search_js_path = os.path.join(BASE_DIR, "assets", "js", "search-index.js")
    os.makedirs(os.path.dirname(search_js_path), exist_ok=True)
    with open(search_js_path, 'w', encoding='utf-8') as f:
        f.write("/* Auto-generated search index for Djazair Documentation */\n")
        f.write("window.DJAZAIR_SEARCH_INDEX = ")
        json.dump(search_data, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"[4/5] Generated search index: assets/js/search-index.js ({len(search_data)} entries)")

    # 5. Generate sitemap.xml & robots.txt
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        '    <loc>https://djazair-language.github.io/</loc>',
        '    <priority>1.0</priority>',
        '  </url>'
    ]
    for page in ALL_PAGES:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>https://djazair-language.github.io/{page["path"]}</loc>')
        sitemap_lines.append('    <priority>0.8</priority>')
        sitemap_lines.append('  </url>')
    sitemap_lines.append('</urlset>')

    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_lines) + '\n')

    robots_path = os.path.join(BASE_DIR, "robots.txt")
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://djazair-language.github.io/sitemap.xml\n")

    print("[5/5] Generated sitemap.xml and robots.txt")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"  ✨ Documentation build completed successfully in {elapsed:.2f}s!")
    print(f"  📄 Total pages: {generated_count + 1} (including index.html)")
    print(f"  🔍 Search index size: {len(search_data)} entries")
    print("=" * 70)

if __name__ == "__main__":
    build_site()
