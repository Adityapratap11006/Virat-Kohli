# KohliIQ — Entity Resolution (Phase 2)

## Players

- Canonical identity = Cricsheet registry hex ID (`REG:<id>`) when the file
  provides one; else deterministic `NAME:<casefolded name>`.
- Parenthetical disambiguators (`Mohammad Nawaz (3)`) are significant.
- 119 identities are **ambiguous**: one display name → 2+ registry IDs
  (mostly shared names across associate sides, e.g. `Junaid Khan`,
  `Muhammad Usman`; also `Shahid Afridi` with two IDs). They are kept as
  separate `REG:` entities and flagged (`batter_ambiguous`, report count
  28,976 delivery-hits). Never merged — per spec, no aggressive merging.
- `V Kohli` resolves to exactly one entity (`REG:ba607b88`); `Pawan Kohli`
  and `T Kohli` are separate entities.
- Zero `NAME:`-only entities in V1: every normalized name was observed with
  a registry ID at least once (T20 registry gaps are covered by recurrence).

## Teams

Verified same-franchise renames merged (source value preserved alongside):

| Source | Canonical |
|---|---|
| Royal Challengers Bangalore | Royal Challengers Bengaluru |
| Kings XI Punjab | Punjab Kings |
| Delhi Daredevils | Delhi Capitals |
| Rising Pune Supergiants | Rising Pune Supergiant |

NOT merged: Deccan Chargers vs Sunrisers Hyderabad (different franchises);
defunct sides (Kochi Tuskers Kerala, Pune Warriors, Gujarat Lions) stay
separate. Hit counts: RCB 240, KXIP 190, DD 161, RPS 14 match rows.

## Venues

Case/whitespace variants grouped; canonical = most frequent spelling;
city preserved, never invented; 454 V1 matches lack `city`.
