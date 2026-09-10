"""Delivery normalization + batter-innings construction on fixtures."""
from etl.derived.batter_innings import build_batter_innings
from etl.normalization.normalize import normalize_match
from etl.resolution.players import PlayerMap
from etl.resolution.venues import VenueMap
from etl.tests.conftest import dl, innings, match, over


def _norm(inn_list, info_over=None):
    if len(inn_list) == 1:  # keep first innings 'normal' for builder tests
        inn_list = inn_list + [innings("B", [over(0, [dl("B1")])],
                                       target={"runs": 10, "overs": 50})]
    m = match(info_over=info_over, innings=inn_list)
    venues = VenueMap()
    venues.observe(m["info"]["venue"], m["info"].get("city"))
    venues.finalize()
    return normalize_match("m1", "m1.json", "ODI", m, PlayerMap(), venues)


def _first(norm_ds):
    return [d for d in norm_ds if d.innings_no == 1]


def test_seq_disambiguates_duplicate_delivery_numbers():
    _, _, ds = _norm([innings("A", [over(0, [
        dl("A1", num="0.5", ex=1, extras={"wides": 1}), dl("A1", num="0.5")])])])
    ds = _first(ds)
    assert [(d.over, d.seq_in_over, d.actual_delivery) for d in ds] == \
        [(0, 0, "0.5"), (0, 1, "0.5")]
    assert ds[0].is_legal_ball is False and ds[1].is_legal_ball is True


def test_non_striker_run_out_keeps_batter_innings():
    ds = [dl("A1", br=1),
          dl("A1", wickets=[{"player_out": "N1", "kind": "run out"}])]
    _, _, norm_ds = _norm([innings("A", [over(0, ds)])])
    norm_ds = _first(norm_ds)
    assert norm_ds[1].batter_id == "REG:id-a1"
    assert norm_ds[1].wickets[0]["player_out_id"] == "NAME:n1"


def test_super_over_deliveries_excluded():
    inn = [innings("A", [over(0, [dl("A1")])]),
           innings("B", [over(0, [dl("B1")])], target={"runs": 10, "overs": 50}),
           {"team": "A", "overs": [over(0, [dl("A1", br=6)])]}]
    _, inns, ds = _norm(inn)
    assert [i.classification for i in inns] == ["normal", "normal", "super_over"]
    assert len(ds) == 2  # super-over ball not normalized


def test_entry_context_and_aggregates():
    ds = [dl("A1", br=4), dl("A1", br=1),
          dl("A1", wickets=[{"player_out": "A1", "kind": "bowled"}]),
          dl("A2", br=6)]
    m_xx, inns, norm_ds = _norm([innings("A", [over(0, ds)])])
    rows = build_batter_innings(m_xx, inns[0], _first(norm_ds))
    a1 = next(r for r in rows if r.batter_id == "REG:id-a1")
    a2 = next(r for r in rows if r.batter_id == "REG:id-a2")
    assert (a1.runs, a1.balls_faced, a1.is_dismissed, a1.dismissal_kind) == \
        (5, 3, True, "bowled")
    assert (a1.entry_team_runs, a1.entry_wickets_lost, a1.entry_balls_bowled) == (0, 0, 0)
    assert (a2.entry_team_runs, a2.entry_wickets_lost) == (5, 1)
    assert a2.entry_balls_remaining == 300 - 3
    assert [r.batting_position for r in rows] == [1, 3]  # N1 appeared at no. 2
    assert all(r.batting_position_reliable for r in rows)


def test_retired_hurt_not_dismissed_unreliable_position():
    ds = [dl("A1", br=10),
          dl("A1", wickets=[{"player_out": "A1", "kind": "retired hurt"}]),
          dl("A2", br=1)]
    m_xx, inns, norm_ds = _norm([innings("A", [over(0, ds)])])
    rows = build_batter_innings(m_xx, inns[0], _first(norm_ds))
    a1 = next(r for r in rows if r.batter_id == "REG:id-a1")
    assert a1.is_dismissed is False and a1.dismissal_kind == "retired hurt"
    assert all(r.batting_position_reliable is False for r in rows)


def test_retired_out_ends_innings():
    ds = [dl("A1", wickets=[{"player_out": "A1", "kind": "retired out"}])]
    m_xx, inns, norm_ds = _norm([innings("A", [over(0, ds)])])
    rows = build_batter_innings(m_xx, inns[0], _first(norm_ds))
    assert rows[0].is_dismissed is True


def test_chase_target_carried():
    ds = [dl("B1", br=2)]
    m_xx, inns, norm_ds = _norm(
        [innings("A", [over(0, [dl("A1")])]),
         innings("B", [over(0, ds)], target={"runs": 200, "overs": 50})])
    rows = build_batter_innings(
        m_xx, inns[1], [d for d in norm_ds if d.innings_no == 2])
    assert rows[0].chase_target == 200 and rows[0].entry_balls_remaining == 300


def test_incomplete_innings_skipped():
    m_xx, inns, norm_ds = _norm([innings("A", [over(0, [dl("A1")])])])
    inns[0].classification = "incomplete"
    assert build_batter_innings(m_xx, inns[0], norm_ds) == []
