# Brightpath payment reconciliation

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/ledger/policy.py`](src/ledger/policy.py) | Functions: `reconcile`, `render` |
| [`src/ledger/eval.py`](src/ledger/eval.py) | Functions: `run` |
| [`src/ledger/ingest.py`](src/ledger/ingest.py) | Functions: `load_events`, `load_settlements` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/ledger/__init__.py`](src/ledger/__init__.py) | Implementation or supporting configuration |
| [`src/ledger/__main__.py`](src/ledger/__main__.py) | Functions: `main` |
| [`Dockerfile`](Dockerfile) | Container build/service configuration |
| [`tests/test_policy.py`](tests/test_policy.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |
| [`docs/01-discovery.md`](docs/01-discovery.md) | Project explanations or operating notes |
| [`docs/02-security.md`](docs/02-security.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

<!-- project-guide:end -->

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

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```
