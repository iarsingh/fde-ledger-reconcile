from __future__ import annotations

import csv
import json
from pathlib import Path

from ledger.policy import Event, Settlement

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EVALS_PATH = ROOT / "evals" / "questions.jsonl"


def load_events(path: Path | None = None) -> list[Event]:
    events = []
    for line in (path or DATA_DIR / "webhooks.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        events.append(
            Event(
                event_id=row["event_id"],
                payment_id=row["payment_id"],
                amount_cents=int(row["amount_cents"]),
                currency=row["currency"],
            )
        )
    return events


def load_settlements(path: Path | None = None) -> list[Settlement]:
    with (path or DATA_DIR / "settlements.csv").open(newline="") as handle:
        return [
            Settlement(
                settlement_id=row["settlement_id"],
                payment_id=row["payment_id"],
                amount_cents=int(row["amount_cents"]),
                status=row["status"],
            )
            for row in csv.DictReader(handle)
        ]
