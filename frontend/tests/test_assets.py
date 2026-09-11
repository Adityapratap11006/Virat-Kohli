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


def _records():
    src = TS.read_text(encoding="utf-8")
    blocks = re.findall(r"\{([^{}]*opposition:[^{}]*)\}", src, re.S)
    recs = []
    for b in blocks:
        if "imagePath: '" not in b:
            continue
        rec = dict(re.findall(r"(\w+):\s*'([^']*)'", b))
        for k, v in re.findall(r"(\w+):\s*(true|false)", b):
            rec[k] = v
        recs.append(rec)
    return src, recs


def test_ts_paths_resolve_and_strict_model():
    src, recs = _records()
    assert recs, "no image records parsed"
    paths = set(re.findall(r"'(/images/[^']+)'", src))
    for path in paths:
        assert (REPO / "frontend" / "public" / path.lstrip("/")).exists(), path
    for field in ("sourceUrl", "sourceName", "creator", "license",
                  "licenseStatus", "matchAssociation", "matchDate",
                  "matchDescription", "exactMatch", "sameOpposition",
                  "rightsVerified"):
        assert field in src
    # no generic portrait substitution on opposition cards
    assert "FALLBACK_IMAGE" not in src
    assert "virat-kohli-portrait" not in src


def test_exact_match_requires_metadata():
    _, recs = _records()
    for r in recs:
        if r.get("exactMatch") == "true":
            assert r.get("matchAssociation") and r.get("matchDate")


def test_same_opposition_requires_association():
    _, recs = _records()
    for r in recs:
        if r.get("sameOpposition") == "true":
            assert r.get("opposition") and r.get("matchAssociation")


def test_rights_verified_requires_license():
    _, recs = _records()
    for r in recs:
        if r.get("rightsVerified") == "true":
            assert r.get("license") not in ("", "unverified")
            assert r.get("sourceUrl")
        assert r.get("licenseStatus") in ("verified", "unverified")


def test_unverified_allowed_but_labelled():
    src, _ = _records()
    assert "LicenseStatus" in src or "licenseStatus" in src


def test_no_silent_generic_substitution():
    comp = (REPO / "frontend" / "src" / "components" / "AnalysisSection.tsx"
            ).read_text(encoding="utf-8")
    assert "portrait" not in comp.lower()


def test_fallback_branch_exists():
    comp = (REPO / "frontend" / "src" / "components" / "AnalysisSection.tsx"
            ).read_text(encoding="utf-8")
    assert "Image unavailable" in comp


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
