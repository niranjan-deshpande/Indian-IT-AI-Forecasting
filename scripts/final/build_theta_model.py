"""Build docs/theta-model.html from theta_model_text.md.

    python3 scripts/final/build_theta_model.py

Needs the `markdown` package (pip install markdown). Math is rendered in the browser with KaTeX.
The page reuses the stylesheet and contents script of docs/health-check.html, so the two stay in step.
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "theta_model_text.md"
OUT = ROOT / "docs" / "theta-model.html"
STYLE_FROM = ROOT / "docs" / "health-check.html"

CRUMBS = ('<a href="index.html">Pilot note</a> · <a href="two-questions.html">Two questions (working draft)</a> · '
          '<a href="health-check.html">Health check</a> · <b>Estimating θ (working draft)</b>')
UNNUMBERED = {"Sources"}
EXTRA_CSS = """
/* this page */
table.text th, table.text td { text-align: left; }
table.text td:last-child, table.text th:last-child { padding-right: 0; }
.imath { white-space: nowrap; }
.math .katex-display { margin: 0; }
"""
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, "missing front matter"
    front = dict(line.split(": ", 1) for line in m.group(1).splitlines())
    return front, text[m.end():]


def slug(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render(body):
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = body.replace("\\$", "XDOLLARX")
    maths = []

    def keep(tex, display):
        maths.append((tex.strip(), display))
        return f"XMATH{len(maths) - 1}X"

    body = re.sub(r"\$\$(.+?)\$\$", lambda m: keep(m.group(1), True), body)
    body = re.sub(r"\$(.+?)\$", lambda m: keep(m.group(1), False), body)
    out = markdown.markdown(body, extensions=["tables", "smarty"], output_format="html")

    def math_html(i):
        tex, display = maths[i]
        esc = html.escape(tex, quote=True)
        if display:
            return f'<div class="math" data-tex="{esc}"><span class="math-fallback">{html.escape(tex)}</span></div>'
        return f'<span class="imath" data-tex="{esc}">{html.escape(tex)}</span>'

    out = re.sub(r"<p>\s*XMATH(\d+)X\s*</p>", lambda m: math_html(int(m.group(1))), out)
    plain = {}  # heading text with math as TeX, for slugs

    def head(m):
        level, inner = m.group(1), m.group(2)
        plain_text = re.sub(r"XMATH(\d+)X", lambda n: maths[int(n.group(1))][0], inner)
        hid = base = slug(plain_text) or f"section-{len(plain)}"
        k = 2
        while hid in plain:
            hid, k = f"{base}-{k}", k + 1
        plain[hid] = plain_text
        return f'<h{level} id="{hid}">{inner}</h{level}>'

    out = re.sub(r"<h([23])>(.*?)</h\1>", head, out)
    out = re.sub(r"XMATH(\d+)X", lambda m: math_html(int(m.group(1))), out)
    out = out.replace("XDOLLARX", "$")
    out = out.replace("<table>", '<div class="table-wrap"><table class="text">').replace("</table>", "</table></div>")
    return out


def number_and_toc(main_html):
    items, n = [], 0

    def h2(m):
        nonlocal n
        hid, inner = m.group(1), m.group(2)
        label = re.sub(r"<[^>]+>", "", inner)
        if label in UNNUMBERED:
            items.append([hid, inner, []])
            return m.group(0)
        n += 1
        items.append([hid, f"{n}. {inner}", []])
        return f'<h2 id="{hid}"><span class="num">{n}</span>{inner}</h2>'

    def h3(m):
        items[-1][2].append((m.group(1), m.group(2)))
        return m.group(0)

    pieces = re.split(r"(<h[23] id=\"[^\"]+\">.*?</h[23]>)", main_html)
    out = []
    for piece in pieces:
        if piece.startswith("<h2"):
            piece = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', h2, piece)
        elif piece.startswith("<h3"):
            re.sub(r'<h3 id="([^"]+)">(.*?)</h3>', h3, piece)
        out.append(piece)
    toc = ['<nav class="toc" aria-label="Contents"><div class="toc-head">Contents</div><ul>']
    for hid, label, subs in items:
        sub = "".join(f'<li><a href="#{s}" data-target="{s}">{t}</a></li>' for s, t in subs)
        toc.append(f'<li><a href="#{hid}" data-target="{hid}">{label}</a>' + (f"<ul>{sub}</ul>" if sub else "") + "</li>")
    toc.append("</ul></nav>")
    return "".join(out), "".join(toc)


def main():
    front, body = front_matter(SRC.read_text(encoding="utf-8"))
    style_src = STYLE_FROM.read_text(encoding="utf-8")
    css = re.search(r"<style>\n(.*?)</style>", style_src, re.S).group(1)
    toc_js = style_src[style_src.index("/* table of contents: open collapsed"):style_src.rindex("</script>")]
    main_html, toc = number_and_toc(render(body))
    title_text = re.sub(r"<sub>(.*?)</sub>", r"_\1", front["title"])
    by = [p.strip() for p in front["byline"].split("·")]
    byline = " · ".join(html.escape(p) for p in by[:-1]) + f' · <span class="tag">{html.escape(by[-1])}</span>'
    header = (f'<header><p class="crumbs">{CRUMBS}</p><h1>{front["title"]}</h1>'
              f'<p class="byline">{byline}</p><p class="thanks">{html.escape(front["thanks"])}</p></header>'
              f'<details class="toc-mobile"><summary>Contents</summary>{toc}</details>')
    footer = ('<p class="footer">Built from <code>theta_model_text.md</code> by '
              '<code>scripts/final/build_theta_model.py</code>.</p>')
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title_text)}</title>
<meta name="description" content="A model of how much labor AI can save in Indian IT and BPO, by service line and task length, with the best evidence for each parameter.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}{EXTRA_CSS}</style>
</head>
<body>
<div class="page">
{toc}
<main>
{header}
{main_html}
{footer}
</main>
</div>
<script src="{KATEX}/katex.min.js"></script>
<script>
if (window.katex) {{
  document.querySelectorAll(".math[data-tex]").forEach(el =>
    katex.render(el.dataset.tex, el, {{ displayMode: true, throwOnError: false }}));
  document.querySelectorAll(".imath[data-tex]").forEach(el =>
    katex.render(el.dataset.tex, el, {{ displayMode: false, throwOnError: false }}));
}}
{toc_js}</script>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
