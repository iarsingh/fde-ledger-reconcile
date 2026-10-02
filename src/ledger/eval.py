from __future__ import annotations

import json
from pathlib import Path

from ledger.ingest import EVALS_PATH, load_events, load_settlements
from ledger.policy import reconcile

ROOT = Path(__file__).resolve().parents[2]


def run(path: Path | None = None) -> int:
    result = reconcile(load_events(), load_settlements())
    by_event = {}
    for outcome in result.outcomes:
        by_event.setdefault(outcome.event_id, []).append(outcome)
    failures = []
    cases = []
    for line in (path or EVALS_PATH).read_text().splitlines():
        if line.strip():
            cases.append(json.loads(line))
    if result.matched_cents != 1500:
        failures.append(f"matched_cents {result.matched_cents}")
    for case in cases:
        statuses = [item.status for item in by_event.get(case["event_id"], [])]
        if case["expected_status"] not in statuses:
            failures.append(f"{case['event_id']}: {statuses}")
    if failures:
        print(f"{len(failures)} eval failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"{len(cases)} eval cases passed")
    return 0
