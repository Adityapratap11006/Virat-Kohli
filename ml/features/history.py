"""Incremental per-batter history for leakage-safe features.

A row dated D may only use completed rows with match_date strictly before D
(day-granular Cricsheet dates; same-day matches excluded conservatively).
Rows are (date, match_id, innings_id, row_id) ordered; history slices take
the most recent N strictly-earlier rows. Missing history yields None plus
explicit count features — never future data, never global fill.
"""
from bisect import bisect_left


class BatterHistory:
    def __init__(self) -> None:
        # each entry: (date, runs, balls, venue_key, opp, inn_no, is_chase)
        self._rows: list[tuple] = []
        self._dates: list[str] = []

    def add(self, date: str, runs: int, balls: int, venue_key: str,
            opp: str, inn_no: int, is_chase: bool) -> None:
        assert not self._dates or date >= self._dates[-1], "rows must be date-ordered"
        self._rows.append((date, runs, balls, venue_key, opp, inn_no, is_chase))
        self._dates.append(date)

    def _prior(self, date: str) -> list:
        return self._rows[:bisect_left(self._dates, date)]

    @staticmethod
    def _avg(rows: list) -> float | None:
        if not rows:
            return None
        return sum(r[1] for r in rows) / len(rows)

    @staticmethod
    def _sr(rows: list) -> float | None:
        balls = sum(r[2] for r in rows)
        if not rows or balls <= 0:
            return None
        return 100.0 * sum(r[1] for r in rows) / balls

    def snapshot(self, date: str, venue_key: str, opp: str) -> dict:
        prior = self._prior(date)
        # NOTE: windowed averages use available history even when shorter
        # than N (documented); count features expose the sample size.
        out = {
            "prior_innings": len(prior),
            "avg_5": self._avg(prior[-5:]) if prior else None,
            "avg_10": self._avg(prior[-10:]) if prior else None,
            "avg_20": self._avg(prior[-20:]) if prior else None,
            "sr_10": self._sr(prior[-10:]) if prior else None,
        }
        v = [r for r in prior if r[3] == venue_key]
        out.update({"venue_n": len(v), "venue_avg": self._avg(v),
                    "venue_sr": self._sr(v)})
        o = [r for r in prior if r[4] == opp]
        out.update({"opp_n": len(o), "opp_avg": self._avg(o),
                    "opp_sr": self._sr(o)})
        inn1 = [r for r in prior if r[5] == 1]
        inn2 = [r for r in prior if r[5] == 2]
        chase = [r for r in prior if r[6]]
        setting = [r for r in prior if not r[6]]
        out.update({"inn1_avg": self._avg(inn1), "inn2_avg": self._avg(inn2),
                    "chase_avg": self._avg(chase),
                    "setting_avg": self._avg(setting)})
        return out
