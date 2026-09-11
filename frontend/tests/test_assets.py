"""Asset validity: licensed images exist, are real JPEGs, are all referenced
by oppositionImages.ts (or documented), and docs/assets.md covers them."""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
IMG = REPO / "frontend" / "public" / "images"
TS = REPO / "frontend" / "src" / "data" / "oppositionImages.ts"
REGISTER = REPO / "docs" / "assets.md"


def test_images_exist_and_are_jpeg():
    files = sorted(IMG.glob("*.jpg"))
    assert len(files) >= 2
    for p in files:
        assert p.stat().st_size > 10_000, p.name
        assert p.read_bytes()[:2] == b"\xff\xd8", p.name


def test_ts_paths_resolve_and_strict_model():
    src = TS.read_text(encoding="utf-8")
    paths = set(re.findall(r"'(/images/[^']+)'", src))
    for path in paths:
        assert (REPO / "frontend" / "public" / path.lstrip("/")).exists(), path
    # strict model: provenance fields mandatory, no generic fallback export
    for field in ("sourceUrl", "sourceName", "creator", "license",
                  "matchAssociation", "matchDate", "exactMatch"):
        assert field in src
    assert "FALLBACK_IMAGE" not in src
    assert "Representative image" not in src


def test_register_covers_images():
    reg = REGISTER.read_text(encoding="utf-8")
    for p in IMG.glob("*.jpg"):
        assert p.name in reg, p.name
    assert "CC BY" in reg or "GODL" in reg


def test_every_image_used_or_documented():
    src = TS.read_text(encoding="utf-8")
    app = (REPO / "frontend" / "src" / "App.tsx").read_text(encoding="utf-8")
    comps = "".join(
        p.read_text(encoding="utf-8")
        for p in (REPO / "frontend" / "src" / "components").rglob("*.tsx"))
    used = src + app + comps
    for p in IMG.glob("*.jpg"):
        assert p.name in used, p.name
