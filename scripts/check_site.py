#!/usr/bin/env python3
"""Check local routes, referenced assets and basic page metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse

ROOT = Path(__file__).resolve().parents[1] / "site"
PAGES = [ROOT / "index.html", ROOT / "pharma/index.html", ROOT / "medtech/index.html"]
EXPECTED_IMAGES = {"portrait.webp", "theatre.webp", "speaking.webp", "scientist.webp", "hemotech.webp", "mosfarma.webp"}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.title = False
        self.description = False
        self.h1 = 0
        self.images_missing_alt = 0

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "a" and "href" in attr:
            self.references.append((tag, attr["href"]))
        if tag in {"script", "img", "link"}:
            key = "href" if tag == "link" else "src"
            if key in attr:
                self.references.append((tag, attr[key]))
        if tag == "meta" and attr.get("name") == "description":
            self.description = bool(attr.get("content"))
        if tag == "title":
            self.title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and not attr.get("alt"):
            self.images_missing_alt += 1

parser = argparse.ArgumentParser()
parser.add_argument("--assets", action="store_true", help="Require vendored image files")
args = parser.parse_args()
issues = []
for page in PAGES:
    if not page.is_file():
        issues.append(f"Missing page: {page}")
        continue
    doc = Links()
    doc.feed(page.read_text(encoding="utf-8"))
    if not doc.title or not doc.description or doc.h1 != 1 or doc.images_missing_alt:
        issues.append(f"Metadata/semantics: {page}: title={doc.title}, description={doc.description}, h1={doc.h1}, images missing alt={doc.images_missing_alt}")
    for tag, href in doc.references:
        url = urlsplit(href)
        if url.scheme or href.startswith("//") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("#"):
            continue
        target = (page.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(ROOT.resolve()):
            issues.append(f"Path leaves site: {page}: {href}")
            continue
        if not target.exists() and not (not args.assets and target.suffix == ".webp" and target.name in EXPECTED_IMAGES):
            issues.append(f"Broken {tag} path: {page}: {href}")
        if url.fragment and target.is_file() and target.suffix == ".html":
            html = target.read_text(encoding="utf-8")
            if f'id="{url.fragment}"' not in html:
                issues.append(f"Broken anchor: {page}: {href}")
if args.assets:
    for image in EXPECTED_IMAGES:
        path = ROOT / "assets" / image
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"Missing image: {path}")
if issues:
    raise SystemExit("\n".join(issues))
print(f"Checked {len(PAGES)} pages, local links and metadata; images required: {args.assets}")
