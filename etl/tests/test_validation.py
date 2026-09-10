from etl.tests.conftest import dl, innings, match, over
from etl.validation.validate import validate_match


def _two():
    return [innings("A", [over(0, [dl("A1")])]),
            innings("B", [over(0, [dl("B1")])], target={"runs": 10, "overs": 50})]


def _m(**kw):
    return match(innings=_two(), **kw)


def test_odi_male_ok():
    assert validate_match("x", "odis", _m()).disposition == "ok"


def test_women_excluded():
    assert validate_match("x", "odis", _m(info_over={"gender": "female"})) \
        .disposition == "excluded_non_v1"


def test_t20i_filter_uses_team_type_not_match_type():
    m = _m(info_over={"match_type": "T20", "team_type": "international",
                      "overs": 20})
    assert validate_match("x", "t20s", m).disposition == "ok"
    club = _m(info_over={"match_type": "T20", "team_type": "club",
                         "overs": 20})
    assert validate_match("x", "t20s", club).disposition == "excluded_non_v1"


def test_t20i_nonexistent_label_excluded():
    m = _m(info_over={"match_type": "T20I"})
    assert validate_match("x", "t20s", m).disposition == "excluded_non_v1"


def test_runs_total_mismatch_fatal():
    bad = dl("A1", br=4, ex=0)
    bad["runs"]["total"] = 5
    inn = _two()
    inn[0]["overs"] = [over(0, [bad])]
    m = match(innings=inn)
    r = validate_match("x", "odis", m)
    assert r.disposition == "invalid" and r.fatal


def test_unknown_extras_fatal():
    inn = _two()
    inn[0]["overs"] = [over(0, [dl("A1", ex=1, extras={"mystery": 1})])]
    m = match(innings=inn)
    assert validate_match("x", "odis", m).disposition == "invalid"


def test_seven_batter_runs_allowed():
    inn = _two()
    inn[0]["overs"] = [over(0, [dl("A1", br=7)])]
    m = match(innings=inn)
    r = validate_match("x", "odis", m)
    assert r.disposition == "ok" and not r.fatal and r.warnings


def test_duplicate_actual_delivery_ok():
    ds = [dl("A1", num="0.5", ex=1, extras={"wides": 1}),
          dl("A1", num="0.5", br=2)]
    inn = _two()
    inn[0]["overs"] = [over(0, ds)]
    m = match(innings=inn)
    assert validate_match("x", "odis", m).disposition == "ok"


def test_single_innings_excluded_incomplete():
    m = match(info_over={"outcome": {"result": "no result"}},
              innings=[innings("A", [over(0, [dl("A1")])])])
    assert validate_match("x", "odis", m).disposition == "excluded_incomplete"


def test_t20s_50_over_quarantine():
    m = _m(info_over={"match_type": "T20", "team_type": "international",
                      "overs": 50})
    assert validate_match("x", "t20s", m).disposition == "excluded_anomaly"


def test_missing_toss_invalid():
    info = {"dates": ["2024-01-01"], "teams": ["A", "B"], "gender": "male",
            "match_type": "ODI", "team_type": "international"}
    assert validate_match("x", "odis", match(info_over=info, innings=[])) \
        .disposition == "invalid"


def test_wicket_without_player_out_fatal():
    inn = _two()
    inn[0]["overs"] = [over(0, [dl("A1", wickets=[{"kind": "bowled"}])])]
    m = match(innings=inn)
    assert validate_match("x", "odis", m).disposition == "invalid"
