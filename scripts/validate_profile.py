#!/usr/bin/env python3
"""Validate the RAM GitHub profile repository.

Checks: required files, README local references, SVG validity, workflow YAML,
username/identity consistency and unverified-claim wording.
Exit code 1 if any error is found. Warnings never fail the run.
"""
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
USER = "raa-mm"
EMAIL = "ramm205061@gmail.com"
SITE = "https://sprkk.in/"
INSTA = "https://instagram.com/_raamm1"
# Files created by GitHub Actions after the first run; absent locally by design.
GENERATED_PREFIXES = ("profile-3d-contrib/",)
GENERATED_REMOTE = f"raw.githubusercontent.com/{USER}/{USER}/output/"
ALLOWED_HOSTS = {
    "github.com", "raw.githubusercontent.com", "sprkk.in", "instagram.com",
    "github-readme-stats.vercel.app", "streak-stats.demolab.com",
    "www.w3.org",
}
REQUIRED = [
    "README.md", "README-REVIEW.md", "SETUP.md", "CHANGELOG.md", "LICENSE-ASSETS.txt", ".gitignore",
    "assets/README.md", "assets/ram-hero.svg", "assets/ram-footer.svg",
    "assets/project-aprs.svg", "assets/project-skilllens.svg", "assets/project-sprkk.svg", "assets/project-lab.svg",
    ".github/workflows/snake.yml", ".github/workflows/profile-3d.yml", ".github/workflows/validate-profile.yml",
    "scripts/validate_profile.py", "scripts/check_external_links.py",
    "docs/PROFILE-CONTENT.md", "docs/DESIGN-SYSTEM.md", "docs/WORKFLOWS.md",
    "docs/MAINTENANCE.md", "docs/DEPLOY-CHECKLIST.md", "docs/PROJECT-CARD-TEMPLATE.md",
]
FORBIDDEN = ["udaysharmadev", "gravitas", "uday sharma"]
CLAIM_WORDS = re.compile(r"\b(winner|finalist|awarded|award-winning|certified|revenue|customers|orders)\b", re.I)

errors, warnings = [], []
def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

# 1. required files
for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        err(f"missing required file: {rel}")

# 2. README
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
refs = set()
for m in re.finditer(r'(?:src|srcset|href)="([^"]+)"', readme):
    refs.add(html.unescape(m.group(1)))
for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)", readme):
    refs.add(m.group(1))
for ref in sorted(refs):
    if ref.startswith(("http://", "https://", "mailto:", "#")):
        continue
    path = ref.split("#")[0].split("?")[0]
    if path.startswith(GENERATED_PREFIXES):
        warn(f"README references generated file (created by workflow): {path}")
    elif not (ROOT / path).exists():
        err(f"README references missing local file: {path}")
for img in re.finditer(r"<img\b[^>]*>", readme):
    if not re.search(r'\balt="[^"]+"', img.group(0)):
        err(f"README <img> without alt text: {img.group(0)[:80]}")
if re.search(r"\bon(click|load|error)=|<script|<style|<iframe", readme, re.I):
    err("README contains HTML that GitHub strips or blocks (script/style/iframe/event handlers)")
for needle, label in [(EMAIL, "email"), (SITE, "website"), (INSTA, "instagram"), (f"github.com/{USER}", "github profile")]:
    if needle not in readme:
        err(f"README is missing {label}: {needle}")

# 3. identity / usernames / claims
text_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md", ".yml", ".svg", ".py", ".txt"} and ".git" not in p.parts]
for p in text_files:
    if p.name == "validate_profile.py":
        continue
    body = p.read_text(encoding="utf-8", errors="ignore")
    rel = p.relative_to(ROOT)
    for word in FORBIDDEN:
        if word in body.lower():
            err(f"{rel}: contains reference-profile text '{word}'")
    for m in re.finditer(r"(?:github\.com|raw\.githubusercontent\.com)/([A-Za-z0-9_-]+)", body):
        if m.group(1).lower() != USER and m.group(1).lower() not in {"actions", "platane", "yoshi389111"}:
            err(f"{rel}: link to another GitHub account: {m.group(0)}")
    for m in re.finditer(r"[?&;](?:username|user)=([A-Za-z0-9_-]+)", body):
        if m.group(1) != USER:
            err(f"{rel}: wrong username parameter: {m.group(0)}")
    if p.name in {"README.md"} and CLAIM_WORDS.search(body):
        err(f"{rel}: contains wording that may state an unverified achievement or business metric: {CLAIM_WORDS.search(body).group(0)}")
for m in re.finditer(r"https?://([^/?#\s\"')]+)", readme):
    if m.group(1) not in ALLOWED_HOSTS:
        err(f"README uses a non-allowlisted host: {m.group(1)}")

# 4. SVG
SVG_NS = "http://www.w3.org/2000/svg"
for p in sorted((ROOT / "assets").rglob("*.svg")):
    rel = p.relative_to(ROOT)
    try:
        root = ET.parse(p).getroot()
    except ET.ParseError as ex:
        err(f"{rel}: invalid XML: {ex}")
        continue
    if root.tag != f"{{{SVG_NS}}}svg":
        err(f"{rel}: root is not an SVG element in the SVG namespace")
    if not root.get("viewBox"):
        err(f"{rel}: missing viewBox")
    if root.find(f"{{{SVG_NS}}}title") is None:
        err(f"{rel}: missing <title>")
    if "/icons/" not in str(rel) and root.find(f"{{{SVG_NS}}}desc") is None:
        err(f"{rel}: missing <desc>")
    raw = p.read_text(encoding="utf-8")
    if re.search(r"<script|<foreignObject|href=\"https?:|url\(https?:", raw):
        err(f"{rel}: contains script/foreignObject/external resource")
    if p.stat().st_size > 20_000:
        warn(f"{rel}: larger than 20 KB ({p.stat().st_size} bytes)")

# 5. workflows
CRON = re.compile(r"^\S+ \S+ \S+ \S+ \S+$")
for p in sorted((ROOT / ".github/workflows").glob("*.yml")):
    rel = p.relative_to(ROOT)
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as ex:
        err(f"{rel}: invalid YAML: {ex}")
        continue
    triggers = doc.get("on", doc.get(True))
    if not triggers:
        err(f"{rel}: no triggers")
    if "permissions" not in doc:
        err(f"{rel}: no top-level permissions block")
    if "concurrency" not in doc:
        err(f"{rel}: no concurrency group")
    for s in (triggers or {}).get("schedule", []) if isinstance(triggers, dict) else []:
        if not CRON.match(s.get("cron", "")):
            err(f"{rel}: bad cron expression: {s}")
    body = p.read_text(encoding="utf-8")
    if re.search(r"ghp_[A-Za-z0-9]{20,}|github_pat_|secrets\.(?!GITHUB_TOKEN)", body):
        err(f"{rel}: hard-coded token or non-default secret")
    for u in re.findall(r"uses:\s*(\S+)", body):
        if "@" not in u:
            err(f"{rel}: action without version: {u}")

# 6. duplicates
seen = {}
for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.suffix == ".svg":
        seen.setdefault(p.read_bytes(), []).append(p.relative_to(ROOT))
for group in seen.values():
    if len(group) > 1:
        warn(f"duplicate files: {', '.join(map(str, group))}")

for w in warnings: print(f"WARN  {w}")
for e in errors: print(f"ERROR {e}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
