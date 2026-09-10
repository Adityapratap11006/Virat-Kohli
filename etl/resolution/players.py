"""Player entity resolution.

Canonical identity: Cricsheet registry hex ID where available (ODI/IPL 100%,
T20 ~53%). Otherwise a deterministic normalized-name key. Names mapping to
multiple registry IDs are flagged ambiguous but still resolved deterministically
(name key); never silently merged into one registry identity.
Parenthetical disambiguators (e.g. 'Mohammad Nawaz (3)') are significant.
"""
import re
from dataclasses import dataclass, field

_WS = re.compile(r"\s+")


def normalize_name(name: str) -> str:
    return _WS.sub(" ", name.strip().casefold())


def collect_registry(parsed_files: list) -> tuple[dict, dict]:
    """parsed_files: [(match_id, data)]. Returns (name -> set(ids), id -> set(names))."""
    name_to_ids: dict[str, set] = {}
    id_to_names: dict[str, set] = {}
    for _, data in parsed_files:
        people = (data.get("info", {}).get("registry") or {}).get("people") or {}
        for name, pid in people.items():
            name_to_ids.setdefault(name, set()).add(pid)
            id_to_names.setdefault(pid, set()).add(name)
    return name_to_ids, id_to_names


@dataclass
class PlayerMap:
    # normalized name -> canonical player_id (first-sorted registry id, or NAME: key)
    canonical: dict = field(default_factory=dict)
    # normalized name -> all registry ids observed for it
    by_norm: dict = field(default_factory=dict)
    # canonical player_id -> {registry_ids, variants, ambiguous, has_registry_id}
    # NOTE: every observed registry id gets its own meta entry.
    meta: dict = field(default_factory=dict)

    def resolve(self, name: str, registry_id: str | None) -> tuple[str, bool, bool]:
        """Returns (player_id, ambiguous, has_registry_id).

        Ambiguous is True when this display name maps to multiple registry
        IDs anywhere in the corpus, whichever path resolved it.
        """
        norm = normalize_name(name)
        ids = self.by_norm.get(norm, set())
        ambiguous = len(ids) > 1
        if registry_id:
            return f"REG:{registry_id}", ambiguous, True
        pid = self.canonical.get(norm)
        if pid is None:  # name never observed; deterministic fallback
            return f"NAME:{norm}", False, False
        return pid, ambiguous, False


def build_player_map(name_to_ids: dict) -> PlayerMap:
    pm = PlayerMap()
    variants: dict[str, set] = {}
    for name, ids in name_to_ids.items():
        norm = normalize_name(name)
        pm.by_norm.setdefault(norm, set()).update(ids)
        variants.setdefault(norm, set()).add(name)
    for norm, ids in pm.by_norm.items():
        if ids:
            pm.canonical[norm] = f"REG:{sorted(ids)[0]}"
            for pid in sorted(ids):
                pm.meta[f"REG:{pid}"] = {
                    "registry_ids": sorted(ids),
                    "variants": sorted(variants[norm]),
                    "ambiguous": len(ids) > 1,
                    "has_registry_id": True,
                }
        else:
            pm.canonical[norm] = f"NAME:{norm}"
            pm.meta[f"NAME:{norm}"] = {
                "registry_ids": [],
                "variants": sorted(variants[norm]),
                "ambiguous": False,
                "has_registry_id": False,
            }
    return pm
