"""Venue normalization: group case/whitespace variants, keep the most frequent
original spelling as canonical, preserve city (never invented)."""
import re
from collections import Counter

_WS = re.compile(r"\s+")


def normalize_venue(name: str) -> str:
    return _WS.sub(" ", name.strip().casefold())


class VenueMap:
    def __init__(self) -> None:
        self._spellings: dict[str, Counter] = {}
        self._cities: dict[str, set] = {}
        self.canonical: dict[str, str] = {}

    def observe(self, venue: str, city: str | None) -> None:
        key = normalize_venue(venue)
        self._spellings.setdefault(key, Counter())[venue] += 1
        if city:
            self._cities.setdefault(key, set()).add(city)

    def finalize(self) -> None:
        for key, spellings in self._spellings.items():
            self.canonical[key] = spellings.most_common(1)[0][0]

    def resolve(self, venue: str) -> tuple[str, bool]:
        key = normalize_venue(venue)
        canon = self.canonical.get(key, venue)
        return canon, canon != venue

    def report(self) -> dict:
        out = {}
        for key, spellings in self._spellings.items():
            out[self.canonical[key]] = {
                "variants": sorted(spellings),
                "cities": sorted(self._cities.get(key, set())),
            }
        return out
