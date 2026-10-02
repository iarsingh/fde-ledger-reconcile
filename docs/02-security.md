# Security

Reads `data/webhooks.jsonl` and `data/settlements.csv` from disk. No outbound call.

The output is a classification per event id. It does not contain a card number, because the sample never has one. A real drop should keep the same rule: match on payment id and amount, and do not copy the raw provider payload into the exception log.

Rollback is deleting the output file. The ledger is unchanged because this process does not write to it.
