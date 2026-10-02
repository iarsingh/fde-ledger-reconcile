from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    event_id: str
    payment_id: str
    amount_cents: int
    currency: str


@dataclass(frozen=True)
class Settlement:
    settlement_id: str
    payment_id: str
    amount_cents: int
    status: str


@dataclass(frozen=True)
class Outcome:
    event_id: str
    payment_id: str
    status: str
    detail: str


@dataclass(frozen=True)
class Reconciliation:
    outcomes: tuple[Outcome, ...]
    matched_cents: int

    def render(self) -> str:
        lines = [f"Matched total: {self.matched_cents} cents. Nothing was auto-posted."]
        for outcome in self.outcomes:
            lines.append(f"{outcome.event_id} {outcome.payment_id} {outcome.status}: {outcome.detail}")
        return "\n".join(lines) + "\n"


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
            outcomes.append(
                Outcome(
                    event.event_id,
                    event.payment_id,
                    "amount_exception",
                    f"Webhook {event.amount_cents} vs settlement {settlement.amount_cents}. Not auto-resolved.",
                )
            )
            continue
        matched_payments.add(event.payment_id)
        matched_cents += event.amount_cents
        outcomes.append(
            Outcome(
                event.event_id,
                event.payment_id,
                "matched",
                f"Cited data/settlements.csv#{settlement.settlement_id}.",
            )
        )
    return Reconciliation(outcomes=tuple(outcomes), matched_cents=matched_cents)
