#!/usr/bin/env python3
"""
Convert content/posts/*.md → blog/posts/*.html and regenerate blog/index.html.
Usage: source venv/bin/activate && python convert.py
"""

import os
import re
from datetime import datetime

import frontmatter
import markdown

POSTS_DIR = "content/posts"
OUTPUT_DIR = "blog/posts"
BLOG_INDEX = "blog/index.html"

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} – Krishnanunni R</title>
  <meta name="description" content="{description}" />
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
  <div class="container">
    <header class="site-header">
      <div class="nav-inner">
        <div class="site-name"><a href="/">Krishnanunni R</a></div>
        <nav>
          <a href="/blog/">Blog</a>
          <a href="https://cooking.bizzaretor.com">Cooking</a>
        </nav>
      </div>
    </header>

    <main>"""

FOOTER = """    </main>

    <footer class="site-footer">
      <div class="footer-links">
        <a href="https://github.com/krishnanunnir" title="GitHub"><span class="svg-icon github"></span></a>
        <a href="https://twitter.com/bizzaretor" title="Twitter"><span class="svg-icon twitter"></span></a>
        <a href="https://www.linkedin.com/in/krishnanunnir" title="LinkedIn"><span class="svg-icon linkedin"></span></a>
        <a href="mailto:hello@bizzaretor.com" title="Email"><span class="svg-icon email"></span></a>
      </div>
      <div>&copy; Krishnanunni R</div>
    </footer>
  </div>
</body>
</html>"""


def slugify(filename):
    """Extract slug from filename: '2020-7-1-Hello-World.md' → 'Hello-World'"""
    name = os.path.splitext(filename)[0]
    m = re.match(r"^\d{4}-\d{1,2}-\d{1,2}-(.+)", name)
    return m.group(1) if m else name


def format_date(d):
    """Format a date to 'Month Day, Year'."""
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d")
    return d.strftime("%B %d, %Y").replace(" 0", " ")


def get_date(filename, frontmatter_date):
    """Get date from frontmatter or filename."""
    if frontmatter_date:
        if isinstance(frontmatter_date, str):
            return frontmatter_date
        return frontmatter_date.strftime("%Y-%m-%d")
    m = re.match(r"^(\d{4}-\d{1,2}-\d{1,2})-", filename)
    return m.group(1) if m else ""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    posts = []

    for filename in sorted(os.listdir(POSTS_DIR)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(POSTS_DIR, filename)

        try:
            post = frontmatter.load(filepath)
        except Exception as e:
            print(f"  ⚠ skipping {filename}: {e}")
            continue

        slug = post.get("slug") or slugify(filename)
        title = post.get("title") or slug.replace("-", " ")
        description = post.get("description", "")
        date_str = get_date(filename, post.get("date"))

        html_content = markdown.markdown(post.content, extensions=["extra", "codehilite"])

        page = HEADER.format(title=title, description=description) + "\n"
        page += f'      <article class="post">\n'
        page += f"        <h1>{title}</h1>\n"
        page += f'        <div class="date">{format_date(date_str)}</div>\n'
        page += f'        <div class="entry">\n'
        page += f"          {html_content}\n"
        page += f"        </div>\n"
        page += f"      </article>\n"
        page += FOOTER

        out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(out_path, "w") as f:
            f.write(page)

        print(f"  ✓ blog/posts/{slug}.html")

        posts.append({
            "title": title,
            "slug": slug,
            "description": description,
            "date": date_str,
        })

    # Sort posts newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    # Generate blog/index.html
    post_items = []
    for p in posts:
        date_fmt = format_date(p["date"])
        desc_html = f"<p>{p['description']}</p>" if p["description"] else ""
        post_items.append(
            f"""        <li class="post-item">
          <h2><a href="/blog/posts/{p['slug']}.html">{p['title']}</a></h2>
          <div class="post-meta">{date_fmt}</div>
          {desc_html}
        </li>"""
        )

    blog_page = HEADER.format(title="Blog", description="Articles and thoughts") + "\n"
    blog_page += '      <h1>Blog</h1>\n'
    blog_page += '      <ul class="post-list">\n'
    blog_page += "\n".join(post_items) + "\n"
    blog_page += "      </ul>\n"
    blog_page += FOOTER

    with open(BLOG_INDEX, "w") as f:
        f.write(blog_page)

    print(f"  ✓ {BLOG_INDEX} ({len(posts)} posts)")


if __name__ == "__main__":
    print(f"\n🔨 Converting posts from {POSTS_DIR}/\n")
    main()
    print(f"\n✅ Done!\n")
