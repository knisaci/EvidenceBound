# EvidenceBound v0.3: Step-by-Step Runbook

The v0.1 and v0.2 contracts are retired. The next deployment must use v0.3
source. Confirm the source header before deployment.

## Step 1 — Open hosted GenLayer Studio

Go to <https://studio.genlayer.com>. No Homebrew, local Python, Node, Docker, or
Terminal setup is required for this route.

## Step 2 — Create the replacement contract

Create a new contract, paste the complete v0.3 source from
`contracts/evidence_bound.py`, compile it, and deploy it to Testnet Bradbury.
The old contract cannot be upgraded in place.

## Step 3 — Record the deployment

Copy the new contract address and deployment transaction ID. Confirm that the
source begins with `EvidenceBound v0.3` before proceeding.

## Step 4 — Run the partial-evidence scenario

Submit one claim using the immutable raw GitHub URL below. Then call
`resolve_claim("claim-1")` once.
Wait for the full appeal and finalization process; an intermediate `accepted`
status is not the final result.

Use these exact `submit_claim` values:

- `subject`: `Synthetic funding-record audit`
- `evaluation_profile`: `RECORD_SET_CLAIM_V1`
- `evidence_urls_json`: `["https://raw.githubusercontent.com/knisaci/EvidenceBound/e1db917dfae002b191d1f9ce9ce44b149cb02040/evidence/fixtures/evidencebound-partial-v1.json"]`
- `manifest_digest`: `sha256:6969d8fd6ac2a46f650fb5c04c24c8b44c8e241cc2df396f376e2506792b43a3`
- `claim_facts_json`: `{"total_records":20,"claimed_records":20,"locked_records":0,"other_records":0,"funding_records_verified":20,"funding_mismatches":0}`
- `period_start`: `1785542400`
- `period_end`: `1788220799`

The expected final claim result is `PARTIALLY_VERIFIED` with `HIGH` confidence
and reason codes `CLAIMED_RECORDS_MISMATCH` and
`LOCKED_RECORDS_MISMATCH`.

## Step 5 — Submission preparation

After the v0.3 resolution is finalized:

1. record the v0.3 contract address and transaction links;
2. test verified and insufficient-evidence fixtures;
3. add an adversarial prompt-injection fixture;
4. write the BuilderValidatorCommunity submission; and
5. perform a final claim-by-claim accuracy check.

Update the existing Portal submission rather than creating a new contribution.
Do not cite the v0.1 or v0.2 address as the current deployment.
