"""Smoke test: real files through the full pipeline into a temp processed dir."""
import json

import etl.pipeline.run as run


def test_pipeline_limit5(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "PROCESSED_DIR", tmp_path)
    monkeypatch.setattr(run.sys, "argv", ["run", "--limit", "5"])
    run.main()
    for f in ("matches.jsonl", "innings.jsonl", "deliveries.jsonl",
              "batter_innings.jsonl", "etl_report.json", "manifest.json",
              "players.json", "teams.json", "venues.json"):
        assert (tmp_path / f).exists(), f
    rep = json.load(open(tmp_path / "etl_report.json", encoding="utf-8"))
    assert rep["records"]["matches"] >= 1
