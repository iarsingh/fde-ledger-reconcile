from __future__ import annotations

import sys

from ledger.eval import run
from ledger.ingest import load_events, load_settlements
from ledger.policy import reconcile


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        return run()
    print(reconcile(load_events(), load_settlements()).render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
