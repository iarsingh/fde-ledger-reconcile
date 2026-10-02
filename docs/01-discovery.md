# Discovery — Brightpath

The user is the payments controller's ops analyst. Every morning they paste webhook exports next to the settlement CSV and look for ghosts: the same payment twice, or a webhook that is ten dollars off the settlement.

Constraint: nothing in this tool posts to the ledger. A mismatch is an exception a person resolves. The analyst said they had already been burned by a script that "helpfully" wrote the webhook amount over the settlement.

Out of scope: charging a card again, issuing a refund, and guessing which side is right.
