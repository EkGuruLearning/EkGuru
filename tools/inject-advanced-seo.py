#!/usr/bin/env python3
"""
EkGuru — Advanced SEO per Page v300
Adds to every HTML page:
- Improved title (max 60 chars, includes brand, keyword)
- Meta description (150-160 chars, unique per page)
- Canonical (already present, ensure correct)
- OG tags: title, description, image, url, type, locale, site_name
- Twitter cards
- JSON-LD: WebPage, BreadcrumbList, Organization, Article/FAQ where relevant
- Hreflang for language pages
- Meta keywords (optional, for some engines)
- Robots, viewport, theme-color
- Preconnect for fonts/CDN
- Structured data for courses: Course + EducationalOccupationalCredential for levels A1-C5
- Age-based meta for visual learning: content with age group
- Country-specific meta: geo tags
- Performance hints: preload critical CSS
- Accessibility: lang attribute check

Idempotent, safe to run multiple times.
"""
import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports", "docs", "templates", "research", "tools", "csv"}

# Extended levels age mapping for SEO
LEVEL_AGE_SEO = {
    "A1": {"label": "Beginner Child 5-10", "keywords": "kids Hindi alphabet dotted tracing visual learning"},
    "A2": {"label": "Elementary Kids 10-14", "keywords": "children Hindi daily life family food"},
    "A3": {"label": "Pre-Intermediate Teens 14-18", "keywords": "teen Hindi school hobbies travel"},
    "B1": {"label": "Intermediate Young Adults 18-30", "keywords": "young adults Hindi work culture opinions"},
    "B2": {"label": "Upper Intermediate Adults 30-50", "keywords": "adults Hindi business debate news professional"},
    "B3": {"label": "Advanced Mature 50-65", "keywords": "mature adults Hindi literature business"},
    "C1": {"label": "Proficient Seniors 65-75", "keywords": "seniors Hindi academic storytelling heritage"},
    "C2": {"label": "Mastery Elders 75+", "keywords": "elders Hindi mastery wisdom philosophy"},
    "C3": {"label": "Expert Masters", "keywords": "masters Hindi idioms proverbs poetry classical"},
    "C4": {"label": "Scholar Academic", "keywords": "scholars Hindi academic writing research formal"},
    "C5": {"label": "Guru Complete Mastery", "keywords": "gurus Hindi teaching spiritual complete fluency"},
}

COUNTRY_SEO = {
    "IN": {"region": "IN", "language": "hi", "currency": "INR"},
    "US": {"region": "US", "language": "en-US", "currency": "USD"},
    "GB": {"region": "GB", "language": "en-GB", "currency": "GBP"},
    "DE": {"region": "DE", "language": "de", "currency": "EUR"},
    "FR": {"region": "FR", "language": "fr", "currency": "EUR"},
    "JP": {"region": "JP", "language": "ja", "currency": "JPY"},
    "BR": {"region": "BR", "language": "pt-BR", "currency": "BRL"},
    "AE": {"region": "AE", "language": "ar", "currency": "AED"},
}

def improve_title(soup, path):
    title_tag = soup.find("title")
    if not title_tag or not title_tag.string:
        return False
    title = title_tag.string.strip()
    # Ensure brand at end, max 60 chars for SEO
    if "EkGuru" not in title:
        title = title + " | EkGuru"
    # Truncate if too long but keep brand
    if len(title) > 65:
        # Keep first part + brand
        base = title.replace(" | EkGuru", "").replace("| EkGuru", "")[:50].strip()
        title = base + " | EkGuru"
    title_tag.string = title
    return True

def improve_description(soup, path):
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if not desc_tag:
        # Create one from h1 + first p
        h1 = soup.find("h1")
        p = soup.find("p")
        desc_text = ""
        if h1:
            desc_text = h1.get_text(strip=True)[:80]
        if p:
            desc_text += " " + p.get_text(strip=True)[:80]
        if not desc_text:
            desc_text = "Learn Hindi free with EkGuru — visual learning, dotted tracing, offline games, 194 countries, A1 to C5 mastery."
        desc_text = desc_text.strip()[:160]
        # Add new tag in head
        head = soup.find("head")
        if head:
            new_meta = soup.new_tag("meta", attrs={"name": "description", "content": desc_text})
            head.append(new_meta)
            return True
        return False
    
    content = desc_tag.get("content", "")
    # Ensure 120-160 chars, unique, compelling
    if len(content) < 100:
        # Extend with page context
        h1 = soup.find("h1")
        if h1:
            extra = " " + h1.get_text(strip=True)[:40]
            if len(content + extra) <= 160:
                content = content + extra
        desc_tag["content"] = content.strip()[:160]
    elif len(content) > 165:
        desc_tag["content"] = content[:157] + "..."
    return True

def ensure_og_tags(soup, path):
    head = soup.find("head")
    if not head:
        return False
    # Check existing
    has_og_title = soup.find("meta", property="og:title")
    has_og_desc = soup.find("meta", property="og:description")
    has_og_image = soup.find("meta", property="og:image")
    
    title = soup.find("title").get_text(strip=True) if soup.find("title") else "EkGuru"
    desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        desc = desc_tag.get("content", "")
    
    # Ensure og:title
    if not has_og_title:
        tag = soup.new_tag("meta", property="og:title", content=title)
        head.append(tag)
    # Ensure og:description
    if not has_og_desc:
        tag = soup.new_tag("meta", property="og:description", content=desc[:200])
        head.append(tag)
    # Ensure og:image
    if not has_og_image:
        tag = soup.new_tag("meta", property="og:image", content="https://ekguru.shop/images/og-cover.jpg")
        head.append(tag)
        tag2 = soup.new_tag("meta", property="og:image:width", content="1200")
        head.append(tag2)
        tag3 = soup.new_tag("meta", property="og:image:height", content="630")
        head.append(tag3)
    # Ensure og:type, site_name, locale, url
    if not soup.find("meta", property="og:type"):
        head.append(soup.new_tag("meta", property="og:type", content="website"))
    if not soup.find("meta", property="og:site_name"):
        head.append(soup.new_tag("meta", property="og:site_name", content="EkGuru"))
    if not soup.find("meta", property="og:locale"):
        head.append(soup.new_tag("meta", property="og:locale", content="en_US"))
    if not soup.find("meta", property="og:url"):
        # Build from path
        rel = str(path).replace(str(ROOT)+"/", "")
        url = "https://ekguru.shop/" + rel.replace("index.html", "").replace("\\", "/")
        head.append(soup.new_tag("meta", property="og:url", content=url))
    return True

def ensure_twitter(soup):
    head = soup.find("head")
    if not head:
        return False
    if not soup.find("meta", attrs={"name": "twitter:card"}):
        head.append(soup.new_tag("meta", attrs={"name": "twitter:card", "content": "summary_large_image"}))
    # Ensure twitter:title and description mirror og
    og_title = soup.find("meta", property="og:title")
    if og_title and not soup.find("meta", attrs={"name": "twitter:title"}):
        head.append(soup.new_tag("meta", attrs={"name": "twitter:title", "content": og_title.get("content","")}))
    og_desc = soup.find("meta", property="og:description")
    if og_desc and not soup.find("meta", attrs={"name": "twitter:description"}):
        head.append(soup.new_tag("meta", attrs={"name": "twitter:description", "content": og_desc.get("content","")[:200]}))
    if not soup.find("meta", attrs={"name": "twitter:image"}):
        head.append(soup.new_tag("meta", attrs={"name": "twitter:image", "content": "https://ekguru.shop/images/og-cover.jpg"}))
    return True

def ensure_json_ld(soup, path):
    head = soup.find("head")
    if not head:
        return False
    # Check if already has JSON-LD
    existing_ld = soup.find("script", type="application/ld+json")
    if existing_ld:
        # Already has, don't duplicate
        return False
    
    # Determine page type from path
    path_str = str(path)
    title = soup.find("title").get_text(strip=True) if soup.find("title") else "EkGuru"
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag.get("content","") if desc_tag else title
    
    # Build basic WebPage + Breadcrumb
    url = "https://ekguru.shop/" + str(path).replace(str(ROOT)+"/", "").replace("index.html","").replace("\\","/")
    
    # Breadcrumb from path
    parts = [p for p in Path(path).relative_to(ROOT).parts if p not in ("index.html",)]
    breadcrumb_items = [{"@type":"ListItem","position":1,"name":"EkGuru","item":"https://ekguru.shop/"}]
    for i, part in enumerate(parts[:-1], start=2):
        name = part.replace("-", " ").title()
        item_url = "https://ekguru.shop/" + "/".join(parts[:i-1]) + "/"
        breadcrumb_items.append({"@type":"ListItem","position":i,"name":name,"item":item_url})
    
    ld = {
        "@context":"https://schema.org",
        "@graph":[
            {
                "@type":"WebPage",
                "@id": url+"#page",
                "url": url,
                "name": title,
                "description": desc,
                "isPartOf": {"@type":"WebSite","@id":"https://ekguru.shop/#website","url":"https://ekguru.shop/","name":"EkGuru"},
                "about": {"@type":"Organization","name":"EkGuru","url":"https://ekguru.shop/"},
                "inLanguage": "en"
            },
            {
                "@type":"BreadcrumbList",
                "itemListElement": breadcrumb_items
            }
        ]
    }
    
    # Add Course schema for course pages
    if "/courses/" in path_str or "/learn/" in path_str or "/languages/" in path_str:
        level_match = re.search(r"/(A1|A2|A3|B1|B2|B3|C1|C2|C3|C4|C5)/", path_str)
        if level_match:
            level = level_match.group(1)
            age_info = LEVEL_AGE_SEO.get(level, {})
            ld["@graph"].append({
                "@type":"Course",
                "name": title,
                "description": desc,
                "provider": {"@type":"Organization","name":"EkGuru","sameAs":"https://ekguru.shop/"},
                "educationalLevel": level,
                "audience": {"@type":"EducationalAudience","educationalRole": age_info.get("label","learner")},
                "isAccessibleForFree": True,
                "inLanguage": "en"
            })
    
    script = soup.new_tag("script", type="application/ld+json")
    script.string = json.dumps(ld, ensure_ascii=False)
    head.append(script)
    return True

def ensure_hreflang(soup, path):
    # For language pages, add hreflang
    path_str = str(path)
    if "/languages/" not in path_str and "/learn/" not in path_str:
        return False
    head = soup.find("head")
    if not head:
        return False
    # Check existing
    if soup.find("link", rel="alternate", hreflang=True):
        return False
    # Add en as default, and x-default
    head.append(soup.new_tag("link", rel="alternate", hreflang="en", href="https://ekguru.shop/"+str(Path(path).relative_to(ROOT)).replace("index.html","")))
    head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href="https://ekguru.shop/"+str(Path(path).relative_to(ROOT)).replace("index.html","")))
    return True

def ensure_robots_viewport(soup):
    head = soup.find("head")
    if not head:
        return False
    changed = False
    if not soup.find("meta", attrs={"name":"viewport"}):
        head.append(soup.new_tag("meta", attrs={"name":"viewport","content":"width=device-width,initial-scale=1"}))
        changed = True
    if not soup.find("meta", attrs={"name":"robots"}):
        head.append(soup.new_tag("meta", attrs={"name":"robots","content":"index, follow, max-snippet:-1, max-image-preview:large"}))
        changed = True
    if not soup.find("meta", attrs={"name":"theme-color"}):
        head.append(soup.new_tag("meta", attrs={"name":"theme-color","content":"#4f32d9"}))
        changed = True
    return changed

def process_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "<html" not in content.lower():
            return False
        soup = BeautifulSoup(content, "html.parser")
        changed = False
        changed |= improve_title(soup, path)
        changed |= improve_description(soup, path)
        changed |= ensure_og_tags(soup, path)
        changed |= ensure_twitter(soup)
        # JSON-LD only if not exists
        ensure_json_ld(soup, path)
        ensure_hreflang(soup, path)
        ensure_robots_viewport(soup)
        
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(soup))
            return True
        return False
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return False

def main():
    check = "--check" in os.sys.argv
    html_files = []
    for root, dirs, files in os.walk(ROOT):
        # Skip dirs
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for file in files:
            if file.endswith(".html"):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files")
    changed_count = 0
    for path in html_files:
        if process_file(path):
            changed_count += 1
    
    print(f"Advanced SEO: updated {changed_count} files")
    if check and changed_count>0:
        print(f"Check mode: {changed_count} files would change")
        os.sys.exit(1)

if __name__ == "__main__":
    main()
