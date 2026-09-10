from etl.resolution.players import build_player_map, collect_registry, normalize_name
from etl.resolution.teams import canonical_team
from etl.resolution.venues import VenueMap


def test_registry_id_wins():
    pm = build_player_map({"V Kohli": {"abc123"}})
    assert pm.resolve("V Kohli", "abc123") == ("REG:abc123", False, True)


def test_name_fallback_deterministic():
    pm = build_player_map({"V Kohli": {"abc123"}})
    assert pm.resolve("V Kohli", None) == ("REG:abc123", False, False)


def test_ambiguous_name_flagged_not_merged():
    pm = build_player_map({"A Smith": {"id1", "id2"}})
    pid, ambiguous, has_reg = pm.resolve("A Smith", None)
    assert ambiguous and pid == "REG:id1"  # deterministic: sorted first


def test_ambiguous_flag_on_registry_path_too():
    pm = build_player_map({"A Smith": {"id1", "id2"}})
    assert pm.resolve("A Smith", "id2") == ("REG:id2", True, True)
    assert "REG:id2" in pm.meta and "REG:id1" in pm.meta


def test_parenthetical_disambiguator_preserved():
    assert normalize_name("Mohammad Nawaz (3)") != normalize_name("Mohammad Nawaz")
    pm = build_player_map({"Mohammad Nawaz (3)": {"x"}, "Mohammad Nawaz": {"y"}})
    assert pm.resolve("Mohammad Nawaz (3)", None)[0] != \
        pm.resolve("Mohammad Nawaz", None)[0]


def test_collect_registry():
    data = {"info": {"registry": {"people": {"A": "1", "B": "2"}}}}
    n2i, i2n = collect_registry([("m", data)])
    assert n2i == {"A": {"1"}, "B": {"2"}} and i2n == {"1": {"A"}, "2": {"B"}}


def test_team_aliases():
    assert canonical_team("Royal Challengers Bangalore") == \
        ("Royal Challengers Bengaluru", True)
    assert canonical_team("Kings XI Punjab") == ("Punjab Kings", True)
    assert canonical_team("Delhi Daredevils") == ("Delhi Capitals", True)
    assert canonical_team("Rising Pune Supergiants") == \
        ("Rising Pune Supergiant", True)


def test_team_non_merges():
    assert canonical_team("Deccan Chargers") == ("Deccan Chargers", False)
    assert canonical_team("Sunrisers Hyderabad") == ("Sunrisers Hyderabad", False)


def test_venue_variants_grouped_city_preserved():
    v = VenueMap()
    v.observe("Eden Gardens", "Kolkata")
    v.observe("eden gardens ", "Kolkata")
    v.observe("Eden Gardens", None)
    v.finalize()
    assert v.resolve("EDEN GARDENS") == ("Eden Gardens", True)
    assert v.report()["Eden Gardens"]["cities"] == ["Kolkata"]
