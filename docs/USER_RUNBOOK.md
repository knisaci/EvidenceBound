# EvidenceBound v0.2: Step-by-Step Runbook

The v0.1 contract is retired. Do not call it again and do not appeal its
undetermined transaction. The next deployment must use v0.2 source.

## Step 1 — Open hosted GenLayer Studio

Go to <https://studio.genlayer.com>. No Homebrew, local Python, Node, Docker, or
Terminal setup is required for this route.

## Step 2 — Create the replacement contract

Create a new contract, paste the complete v0.2 source from
`contracts/evidence_bound.py`, compile it, and deploy it to Testnet Bradbury.
The old contract cannot be upgraded in place.

## Step 3 — Record the deployment

Copy the new contract address and deployment transaction ID. Confirm that the
source begins with `EvidenceBound v0.2` before proceeding.

## Step 4 — Run the partial-evidence scenario

Submit one claim using the immutable raw GitHub URL and values recorded in the
repository after the v0.2 commit. Then call `resolve_claim("claim-1")` once.
Wait for the full appeal and finalization process; an intermediate `accepted`
status is not the final result.

## Step 5 — Submission preparation

Only after v0.2 multi-validator tests pass will we:

1. record the v0.2 contract address and transaction links;
2. test verified and insufficient-evidence fixtures;
3. add an adversarial prompt-injection fixture;
4. write the BuilderValidatorCommunity submission; and
5. perform a final claim-by-claim accuracy check.

Do not submit v0.1 or cite its address as a successful deployment.
