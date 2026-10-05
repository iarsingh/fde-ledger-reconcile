# fde-ledger-reconcile — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-ledger-reconcile address, and what can you demonstrate?

Simulated forward deployed engagement for Brightpath, a payments ops team. Webhooks and the settlement file do not arrive once, and they do not always agree. The controller will not let software mark a payment settled when the cents differ.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/ledger/policy.py`](src/ledger/policy.py): Implementation or supporting configuration.
- [`src/ledger/eval.py`](src/ledger/eval.py): Implementation or supporting configuration.
- [`src/ledger/ingest.py`](src/ledger/ingest.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/ledger/__init__.py`](src/ledger/__init__.py): Implementation or supporting configuration.
- [`src/ledger/__main__.py`](src/ledger/__main__.py): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.
- [`tests/test_policy.py`](tests/test_policy.py): Executable checks and regression examples.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `reconcile` and explain the decision it makes?

The main walkthrough here is `reconcile(events: list[Event], settlements: list[Settlement])` in [`src/ledger/policy.py`](src/ledger/policy.py#L42). Match each webhook once. Never treat an amount mismatch as paid.

```python
def reconcile(events: list[Event], settlements: list[Settlement]) -> Reconciliation:
    """Match each webhook once. Never treat an amount mismatch as paid."""
    by_payment = {item.payment_id: item for item in settlements}
    seen_events: set[str] = set()
    matched_payments: set[str] = set()
    outcomes: list[Outcome] = []
    matched_cents = 0
    for event in events:
        if event.event_id in seen_events:
            outcomes.append(Outcome(event.event_id, event.payment_id, "duplicate_event", "Ignored replay of the same event id."))
            continue
        seen_events.add(event.event_id)
        if event.payment_id in matched_payments:
            outcomes.append(Outcome(event.event_id, event.payment_id, "duplicate_payment", "This payment is already matched. Not counted again."))
            continue
        settlement = by_payment.get(event.payment_id)
        if settlement is None or settlement.status != "posted":
            outcomes.append(Outcome(event.event_id, event.payment_id, "pending_settlement", "No posted settlement. Left in the exception queue."))
            continue
        if settlement.amount_cents != event.amount_cents:
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `Outcome`, `Reconciliation`, `by_payment.get`, `matched_payments.add`, `outcomes.append`, `seen_events.add`, `set`, `tuple`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `run` have?

`run(path: Path | None=None)` is defined in [`src/ledger/eval.py`](src/ledger/eval.py#L12).

Its return expressions include:

- `0`
- `1`

It uses `(path or EVALS_PATH).read_text`, `(path or EVALS_PATH).read_text().splitlines`, `by_event.get`, `by_event.setdefault`, `by_event.setdefault(outcome.event_id, []).append`, `cases.append`, `failures.append`, `json.loads`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `SystemExit(main())` in [`src/ledger/__main__.py`](src/ledger/__main__.py#L18).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_policy.py`](tests/test_policy.py#L6) contains `test_eval_file_passes`:

```python
def test_eval_file_passes():
    assert run(EVALS_PATH) == 0
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. How do you separate the current design from a future production design?

The current design is the source/component map in [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md). A future deployment needs explicit input contracts, persistence decisions, authentication, monitoring, and rollback. I would present these as proposed work until the corresponding implementation and verification exist.

## 8. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `reconcile`?

In [`src/ledger/policy.py`](src/ledger/policy.py#L42), `reconcile(events: list[Event], settlements: list[Settlement])` receives the inputs. The function computes these intermediate values:

- `by_payment = {item.payment_id: item for item in settlements}`
- `seen_events: set[str] = set()`
- `matched_payments: set[str] = set()`
- `outcomes: list[Outcome] = []`
- `matched_cents = 0`

Its result is defined by:

- `Reconciliation(outcomes=tuple(outcomes), matched_cents=matched_cents)`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/ledger/policy.py`](src/ledger/policy.py#L42) branches on:

- `event.event_id in seen_events`
- `event.payment_id in matched_payments`
- `settlement is None or settlement.status != 'posted'`
- `settlement.amount_cents != event.amount_cents`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
