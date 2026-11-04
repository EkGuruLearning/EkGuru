#!/usr/bin/env python3
"""Fix SEO metadata issues across all HTML pages:
1. Fix malformed og:image tag (missing closing >)
2. Add missing og:image tags (for pages with og:title but no og:image)
3. Add missing Twitter Card tags
4. Add missing JSON-LD structured data
"""
import re
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OG_COVER = "https://ekguru.shop/images/og-cover.jpg"
OG_ALT = "EkGuru — free, self-paced Hindi learning"

def fix_malformed_og_image(html):
    """Fix og:image tag missing closing > and og:image:alt with extra >"""
    # Fix og:image:alt double >>
    html = html.replace(
        'og:image:alt" content="EkGuru — free, self-paced Hindi learning">>',
        'og:image:alt" content="EkGuru — free, self-paced Hindi learning">'
    )
    # Fix og:image tag missing closing >
    lines = html.split('\n')
    fixed = []
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith('<meta') and
            'og:image"' in stripped and
            'og-cover.jpg"' in stripped and
            not stripped.endswith('>') and
            not stripped.endswith('/>')):
            fixed.append(line.rstrip() + '>')
        else:
            fixed.append(line)
    return '\n'.join(fixed)

def has_og_image(html):
    return 'og:image' in html

def has_twitter_card(html):
    return 'twitter:card' in html

def has_jsonld(html):
    return 'application/ld+json' in html

def has_og_title(html):
    return 'og:title' in html

def extract_og_title(html):
    m = re.search(r'og:title"\s*content="([^"]+)"', html)
    return m.group(1) if m else "EkGuru"

def extract_og_description(html):
    m = re.search(r'og:description"\s*content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'name="description"\s*content="([^"]+)"', html)
    return m.group(1) if m else "EkGuru — free, self-paced Hindi learning"

def extract_og_url(html):
    m = re.search(r'og:url"\s*content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'canonical"\s*href="([^"]+)"', html)
    return m.group(1) if m else "https://ekguru.shop/"

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return "EkGuru"

def add_og_image_set(html):
    """Add og:image meta tags after og:url or og:description"""
    og_tags = (
        f'<meta property="og:image" content="{OG_COVER}">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{OG_ALT}">'
    )
    # Try to insert after og:url line
    m = re.search(r'(<meta[^>]*og:url[^>]*>)', html)
    if m:
        html = html[:m.end()] + '\n' + og_tags + html[m.end():]
        return html
    # Try after og:description
    m = re.search(r'(<meta[^>]*og:description[^>]*>)', html)
    if m:
        html = html[:m.end()] + '\n' + og_tags + html[m.end():]
        return html
    # Try after og:title
    m = re.search(r'(<meta[^>]*og:title[^>]*>)', html)
    if m:
        html = html[:m.end()] + '\n' + og_tags + html[m.end():]
        return html
    # Fallback: before </head>
    html = html.replace('</head>', og_tags + '\n</head>', 1)
    return html

def add_twitter_cards(html, og_title, og_desc):
    """Add Twitter Card meta tags after og:image:alt"""
    twitter_tags = (
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{og_title}">\n'
        f'<meta name="twitter:description" content="{og_desc[:200]}">\n'
        f'<meta name="twitter:image" content="{OG_COVER}">\n'
        f'<meta name="twitter:image:alt" content="{OG_ALT}">'
    )
    # Try to insert after og:image:alt
    m = re.search(r'(<meta[^>]*og:image:alt[^>]*>)', html)
    if m:
        html = html[:m.end()] + '\n' + twitter_tags + html[m.end():]
        return html
    # Try after og:image
    m = re.search(r'(<meta[^>]*og:image"[^>]*>)', html)
    if m:
        html = html[:m.end()] + '\n' + twitter_tags + html[m.end():]
        return html
    # Fallback: before </head>
    html = html.replace('</head>', twitter_tags + '\n</head>', 1)
    return html

def build_breadcrumb(url):
    parts = [p for p in url.replace('https://ekguru.shop', '').strip('/').split('/') if p]
    crumbs = [{"@type":"ListItem","position":1,"name":"EkGuru","item":"https://ekguru.shop/"}]
    base = "https://ekguru.shop/"
    for i, part in enumerate(parts):
        pos = i + 2
        item_url = base + "/".join(parts[:i+1]) + "/"
        name = part.replace("-", " ").title()
        crumbs.append({"@type":"ListItem","position":pos,"name":name,"item":item_url})
    return {"@type":"BreadcrumbList","itemListElement":crumbs}

def add_jsonld(html, url, title, desc):
    name = title.replace(' | EkGuru', '').strip()
    if not name:
        name = "EkGuru"
    breadcrumb = build_breadcrumb(url)
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url + "#page",
                "url": url,
                "name": name,
                "description": desc[:200],
                "dateModified": "2026-11-04",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://ekguru.shop/#website",
                    "url": "https://ekguru.shop/",
                    "name": "EkGuru"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "EkGuru",
                    "url": "https://ekguru.shop/",
                    "email": "EkGuruLearning@gmail.com"
                }
            },
            breadcrumb
        ]
    }
    jsonld_str = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>'
    if '</body>' in html:
        html = html.replace('</body>', jsonld_str + '\n</body>', 1)
    else:
        html += '\n' + jsonld_str
    return html

def process_file(filepath):
    """Process a single HTML file and return (fixed_html, issues_found)"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix malformed og:image
    if re.search(r'<meta[^>]*og:image[^>]*[^>]$', html, re.MULTILINE):
        html = fix_malformed_og_image(html)
        issues.append('fixed_malformed_og_image')

    # 2. Add missing og:image tags
    if has_og_title(html) and not has_og_image(html):
        html = add_og_image_set(html)
        issues.append('added_og_image')

    # 3. Add Twitter Cards
    if has_og_title(html) and not has_twitter_card(html):
        og_title = extract_og_title(html)
        og_desc = extract_og_description(html)
        html = add_twitter_cards(html, og_title, og_desc)
        issues.append('added_twitter_cards')

    # 4. Add JSON-LD
    if has_og_title(html) and not has_jsonld(html):
        og_url = extract_og_url(html)
        title = extract_title(html)
        desc = extract_og_description(html)
        html = add_jsonld(html, og_url, title, desc)
        issues.append('added_jsonld')

    return html, issues

def main():
    files = []
    for root, dirs, files_ in os.walk(ROOT):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        for f in files_:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))

    print(f"Scanning {len(files)} HTML files...")

    total_fixed = 0
    stats = {'fixed_malformed_og_image': 0, 'added_og_image': 0,
             'added_twitter_cards': 0, 'added_jsonld': 0}

    for f in files:
        if '404.html' in f:
            continue
        html, issues = process_file(f)
        if issues:
            with open(f, 'w', encoding='utf-8') as out:
                out.write(html)
            total_fixed += 1
            for issue in issues:
                stats[issue] += 1

    print(f"\nResults:")
    print(f"  Files fixed: {total_fixed}")
    for key, count in sorted(stats.items()):
        print(f"  {key}: {count}")

if __name__ == '__main__':
    main()
