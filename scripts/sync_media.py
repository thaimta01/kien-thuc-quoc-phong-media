#!/usr/bin/env python3
"""Synchronize public image files into the gallery manifest without losing metadata."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = PUBLIC / "media-manifest.json"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
EXCLUDE = {"favicon.png"}
data = json.loads(MANIFEST.read_text(encoding="utf-8"))
existing = {entry["path"]: entry for entry in data.get("images", []) if "path" in entry}
images = []
for file in sorted(PUBLIC.rglob("*")):
    if not file.is_file() or file.suffix.lower() not in EXTENSIONS or file.name.lower() in EXCLUDE:
        continue
    relative = file.relative_to(PUBLIC).as_posix()
    path = "/" + relative
    entry = existing.get(path)
    if entry is None:
        label = file.stem.replace("_", " ").replace("-", " ").strip()
        entry = {
            "id": relative.rsplit(".", 1)[0].replace("/", "-"),
            "path": path,
            "title": label,
            "type": "unreviewed",
            "credit": "Cần xác minh nguồn và quyền sử dụng trước khi đăng"
        }
    images.append(entry)
data["images"] = images
new_content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
if not MANIFEST.exists() or MANIFEST.read_text(encoding="utf-8") != new_content:
    MANIFEST.write_text(new_content, encoding="utf-8")
    print(f"Updated catalog: {len(images)} images")
else:
    print(f"Catalog already current: {len(images)} images")
