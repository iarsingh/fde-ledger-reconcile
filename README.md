# Brightpath payment reconciliation

Simulated forward deployed engagement for Brightpath, a payments ops team. Webhooks and the settlement file do not arrive once, and they do not always agree. The controller will not let software mark a payment settled when the cents differ.

## What the file shows

| Event | What happens |
| --- | --- |
| evt-1 pay-9 1500 | matched to set-1 |
| evt-1 again | duplicate_event, ignored |
| evt-2 same payment | duplicate_payment, not counted twice |
| evt-3 pay-4 8000 vs settlement 7900 | amount_exception, not auto-resolved |
| evt-4 pay-7 | pending_settlement, no posted row |

Matched total on this sample is 1500 cents.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest
python -m ledger eval
python -m ledger
```

## Docs

- [Discovery](docs/01-discovery.md)
- [Security](docs/02-security.md)
- [Readout](docs/03-readout.md)

The pilot does not claim recovered revenue. It claims that a replay does not double-count and a mismatch stays in the exception file.
