from ledger.eval import run
from ledger.ingest import EVALS_PATH, load_events, load_settlements
from ledger.policy import reconcile


def test_eval_file_passes():
    assert run(EVALS_PATH) == 0


def test_replay_does_not_double_the_matched_total():
    result = reconcile(load_events(), load_settlements())
    assert result.matched_cents == 1500
    statuses = [item.status for item in result.outcomes]
    assert statuses.count("matched") == 1
    assert "amount_exception" in statuses
    assert "auto-resolved" in result.render()
