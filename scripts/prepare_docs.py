"""Stage existing tutorials for MkDocs without modifying their source."""
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".docs"
SOURCES = [*ROOT.glob("*.md"), *ROOT.glob("experiments/**/*.md")]
PAGES = {}
for source in SOURCES:
    relative = source.relative_to(ROOT)
    if relative == Path("README_EN.md"):
        target = Path("en/index.md")
    elif source.stem.lower() == "readme":
        target = relative.with_name("index.md")
    else:
        target = relative
    PAGES[relative.as_posix()] = target.as_posix()

def rewrite(url, source, target):
    url = url.replace("https://datawhalechina.github.io/agentic-rl-lab/", "https://zhibinf.github.io/agentic-rl-lab/")
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path or url.startswith("/"):
        return url
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parsed.path)))
    suffix = ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
    if resolved in PAGES:
        destination = PAGES[resolved]
        # Raw HTML links bypass MkDocs' Markdown URL rewriting.
        if destination.endswith("/index.md"):
            destination = destination[:-8]
        elif destination == "index.md":
            destination = ""
        else:
            destination = destination[:-3] + "/"
        page_dir = posixpath.dirname(target) if target.endswith("index.md") else target[:-3]
        return posixpath.relpath(destination or ".", page_dir or ".") + "/" + suffix
    path = ROOT / resolved
    if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".pdf"}:
        output = DEST / resolved
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, output)
        page_dir = posixpath.dirname(target) if target.endswith("index.md") else target[:-3]
        return posixpath.relpath(resolved, page_dir or ".") + suffix
    return "https://github.com/zhibinF/agentic-rl-lab/blob/main/" + resolved + suffix

if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir()
shutil.copytree(ROOT / "docs-assets", DEST, dirs_exist_ok=True)
for source in SOURCES:
    relative = source.relative_to(ROOT).as_posix()
    target = PAGES[relative]
    content = source.read_text()
    content = re.sub(r'(!?\[[^\]\n]*\]\()([^\n]*?)(\))',
                     lambda m: m[1] + rewrite(m[2], relative, target) + m[3], content)
    content = re.sub(r'((?:href|src)=["\'])([^"\']+)(["\'])',
                     lambda m: m[1] + rewrite(m[2], relative, target) + m[3], content)
    output = DEST / target
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
print(f"Prepared {len(PAGES)} documentation pages")
