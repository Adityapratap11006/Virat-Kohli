"""ETL quality report: machine-readable JSON + human-readable summary."""
import json
from collections import Counter
from pathlib import Path


class QualityReport:
    def __init__(self) -> None:
        self.files_seen = 0
        self.parse_failures: list[str] = []
        self.dispositions: Counter = Counter()
        self.fatal: Counter = Counter()
        self.warnings: Counter = Counter()
        self.unresolved_names: Counter = Counter()
        self.ambiguous_hits = 0
        self.team_variants: Counter = Counter()
        self.missing_city = 0
        self.quarantined: list[str] = []
        self.n_matches = 0
        self.n_innings = 0
        self.n_deliveries = 0
        self.n_batter_innings = 0

    def summary(self) -> dict:
        return {
            "files_seen": self.files_seen,
            "parse_failures": self.parse_failures,
            "dispositions": dict(self.dispositions),
            "fatal_messages": dict(self.fatal.most_common(20)),
            "warning_messages": dict(self.warnings.most_common(20)),
            "ambiguous_player_hits": self.ambiguous_hits,
            "unresolved_names": dict(self.unresolved_names.most_common(20)),
            "team_variants": dict(self.team_variants),
            "missing_city": self.missing_city,
            "quarantined": self.quarantined,
            "records": {
                "matches": self.n_matches,
                "innings": self.n_innings,
                "deliveries": self.n_deliveries,
                "batter_innings": self.n_batter_innings,
            },
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.summary(), indent=2), encoding="utf-8")

    def print_human(self) -> None:
        s = self.summary()
        print(f"files={s['files_seen']} dispositions={s['dispositions']}")
        print(f"records={s['records']}")
        print(f"missing_city={s['missing_city']} ambiguous_hits={s['ambiguous_player_hits']}")
        print(f"team_variants={s['team_variants']}")
        print(f"parse_failures={len(s['parse_failures'])} quarantined={len(s['quarantined'])}")
