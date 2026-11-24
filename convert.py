#!/usr/bin/env python3
"""
Build the whole site from content/posts/*.md:
  index.html, blog/index.html, blog/posts/*.html, cooking/index.html, 404.html, feed.xml
Usage: source venv/bin/activate && python convert.py
"""

import os
import re
from datetime import datetime
from email.utils import format_datetime
from html import escape
from itertools import groupby

import frontmatter
import markdown

POSTS_DIR = "content/posts"
OUTPUT_DIR = "blog/posts"
SITE = "https://bizzaretor.com"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light dark" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="alternate" type="application/rss+xml" title="Krishnanunni R" href="/feed.xml" />
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="site-name" href="/">Krishnanunni R</a>
    <nav aria-label="Site">
      <a href="/blog/">Writing</a>
      <a href="/#projects">Projects</a>
    </nav>
  </header>

  <main id="main">
"""

FOOT = """  </main>

  <footer class="site-footer">
    <a href="mailto:hello@bizzaretor.com">hello@bizzaretor.com</a>
    <a href="https://github.com/krishnanunnir">GitHub</a>
    <a href="https://twitter.com/bizzaretor">Twitter</a>
    <a href="https://www.linkedin.com/in/krishnanunnir">LinkedIn</a>
    <a href="/feed.xml">RSS</a>
  </footer>

  <!-- A pencil figure who walks to the flag as you scroll. Pure CSS; hidden where unsupported. -->
  <div class="walker" aria-hidden="true">
    <svg class="flag" viewBox="0 0 20 40"><path d="M4 40V3"/><path d="M4 4l13 5-13 6"/></svg>
    <svg class="person" viewBox="0 0 40 60">
      <filter id="pencil"><feTurbulence baseFrequency=".9" numOctaves="2" seed="2"/><feDisplacementMap in="SourceGraphic" scale="1.6"/></filter>
      <g filter="url(#pencil)">
        <path class="arm back" d="M20 22v13"/>
        <path class="leg back" d="M20 36v20h4"/>
        <path d="M20 17v19"/>
        <circle cx="20" cy="10" r="7"/>
        <path class="leg front" d="M20 36v20h4"/>
        <path class="arm front" d="M20 22v13"/>
      </g>
    </svg>
  </div>
</body>
</html>
"""


def write(path, title, description, body):
    full = title if title == "Krishnanunni R" else f"{title} – Krishnanunni R"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(HEAD.format(title=escape(full), description=escape(description)))
        f.write(body)
        f.write(FOOT)
    print(f"  ✓ {path}")


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


def post_list(posts, descriptions=False):
    """Posts grouped by year. The title carries a view-transition-name so it
    glides into the post's heading when you open it."""
    out = ""
    for year, group in groupby(posts, key=lambda p: p["date"].year):
        out += f'      <h3 class="year">{year}</h3>\n      <ol class="posts">\n'
        for p in group:
            desc = f'<span class="desc">{escape(p["description"])}</span>' if descriptions and p["description"] else ""
            out += (
                f'        <li><a href="/blog/posts/{p["slug"]}.html">'
                f'<span class="t" style="view-transition-name:p-{p["slug"]}">{escape(p["title"])}</span>{desc}</a>'
                f'<time datetime="{p["date"]:%Y-%m-%d}">{p["date"]:%b} {p["date"].day}</time></li>\n'
            )
        out += "      </ol>\n"
    return out


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    posts = []

    for filename in sorted(os.listdir(POSTS_DIR)):
        if not filename.endswith(".md"):
            continue
        try:
            post = frontmatter.load(os.path.join(POSTS_DIR, filename))
        except Exception as e:
            print(f"  ⚠ skipping {filename}: {e}")
            continue

        slug = post.get("slug") or slugify(filename)
        html = markdown.markdown(post.content, extensions=["extra", "codehilite"])
        # Old posts point at ../images/, which resolves to /blog/images/ and 404s.
        html = html.replace('src="../images/', 'src="/images/')
        posts.append({
            "title": post.get("title") or slug.replace("-", " "),
            "slug": slug,
            "description": post.get("description", ""),
            "date": datetime.strptime(get_date(filename, post.get("date")), "%Y-%m-%d"),
            "minutes": max(1, round(len(post.content.split()) / 200)),
            "html": html,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)  # newest first, by real date not string

    # ---- posts ----
    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = ""
        if older:
            nav += f'<a class="older" href="/blog/posts/{older["slug"]}.html"><span>Older</span>{escape(older["title"])}</a>'
        if newer:
            nav += f'<a class="newer" href="/blog/posts/{newer["slug"]}.html"><span>Newer</span>{escape(newer["title"])}</a>'
        body = f"""    <article class="post">
      <h1 style="view-transition-name:p-{p['slug']}">{escape(p['title'])}</h1>
      <p class="meta">{format_date(p['date'])} · {p['minutes']} min read</p>
      <div class="entry rise">
        {p['html']}
      </div>
      <nav class="post-nav" aria-label="More posts">{nav}</nav>
    </article>
"""
        write(f"{OUTPUT_DIR}/{p['slug']}.html", p["title"], p["description"], body)

    # ---- blog index ----
    write("blog/index.html", "Writing", "Articles and thoughts", f"""    <h1>Writing</h1>
    <section class="rise">
{post_list(posts, descriptions=True)}    </section>
""")

    # ---- home ----
    write("index.html", "Krishnanunni R", "Engineer, open source builder, and writer", f"""    <section class="intro rise">
      <h1>Hey, I'm Krishnanunni.</h1>
      <p class="tagline">I build open source tools and write about making things.</p>
      <p>
        I'm an engineer who loves building things that people use. I created
        <a href="https://ezhuth.in">Ezhuth.in</a> — a social platform for Malayalam speakers, and
        <a href="https://github.com/krishnanunnir/firstcontrib">First Contrib</a> — helping developers
        break into open source. When I'm not coding, I'm in the kitchen —
        <a href="https://cooking.bizzaretor.com">find my recipes here</a>.
      </p>
      <p>Say hi at <a href="mailto:hello@bizzaretor.com">hello@bizzaretor.com</a>.</p>
    </section>

    <section class="rise">
      <h2>Writing</h2>
{post_list(posts)}    </section>

    <section id="projects" class="rise">
      <h2>Projects</h2>
      <dl class="projects">
        <dt><a href="https://ezhuth.in">Ezhuth.in</a></dt>
        <dd>A social media platform built for Malayalam speakers — writing, sharing, community.</dd>
        <dt><a href="https://github.com/krishnanunnir/firstcontrib">First Contrib</a></dt>
        <dd>Helping developers make their first open source contribution with guided workflows.</dd>
        <dt>Reddit Compilation Maker</dt>
        <dd>A tool to create video compilations from Reddit threads automatically.</dd>
      </dl>
    </section>
""")

    # ---- small pages ----
    write("cooking/index.html", "Cooking", "Krishnanunni's kitchen experiments", """    <h1>Cooking</h1>
    <section class="rise">
      <p>I love experimenting in the kitchen. Cooking is where creativity meets precision — not unlike building software.</p>
      <p>Recipes and notes live at <a href="https://cooking.bizzaretor.com">cooking.bizzaretor.com</a>.</p>
    </section>
""")
    write("404.html", "Not found", "This page does not exist", """    <h1>Nothing here.</h1>
    <section class="rise">
      <p>This address doesn't lead anywhere. Try <a href="/blog/">the writing</a> or go <a href="/">home</a>.</p>
    </section>
""")

    # ---- feed ----
    items = "".join(
        f"<item><title>{escape(p['title'])}</title>"
        f"<link>{SITE}/blog/posts/{p['slug']}.html</link>"
        f"<guid>{SITE}/blog/posts/{p['slug']}.html</guid>"
        f"<pubDate>{format_datetime(p['date'])}</pubDate>"
        f"<description>{escape(p['description'])}</description></item>\n"
        for p in posts
    )
    with open("feed.xml", "w") as f:
        f.write(
            '<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel>\n'
            f"<title>Krishnanunni R</title><link>{SITE}/</link>"
            "<description>Writing by Krishnanunni R</description>\n"
            f"{items}</channel></rss>\n"
        )
    print(f"  ✓ feed.xml ({len(posts)} posts)")


if __name__ == "__main__":
    print(f"\n🔨 Building site from {POSTS_DIR}/\n")
    main()
    print("\n✅ Done!\n")
