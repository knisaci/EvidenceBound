# EvidenceBound

EvidenceBound is a standalone GenLayer Intelligent Contract for adjudicating a
precisely scoped claim against declared public evidence.

It is not a general-purpose fact checker. Version 0.2 deliberately supports one
bounded evaluation profile: `RECORD_SET_CLAIM_V1`, for claims about operational
record sets such as audits, service reports, grant outputs, or agent work logs.

## Why GenLayer consensus is required

Ordinary code can hash a file or count records. It cannot reliably determine
whether the wording of a claim is supported, overstates a status, omits a
material contradiction, or lacks sufficient evidence. EvidenceBound combines:

- deterministic input validation and state transitions;
- independent web retrieval by leader and validators;
- structured LLM extraction into seven fixed fact fields;
- strict equality consensus over one canonical fact object; and
- deterministic derivation of the verdict, confidence, reason codes, and
  explanation after consensus.

Validators re-run the evidence evaluation. They do not merely validate the
leader's JSON format.

## Contract lifecycle

1. A builder calls `submit_claim(...)` with a statement, evidence URLs,
   expected facts, time period, and evidence-manifest digest.
2. The contract stores the claim as `PENDING`.
3. Anyone may call `resolve_claim(claim_id)`.
4. The leader retrieves the evidence and extracts the fixed fact schema.
5. Validators independently retrieve the evidence and extract the same schema.
6. `strict_eq` requires exact equality of the canonical extracted facts.
7. Deterministic code compares those facts with the submitted expected facts.
8. The accepted adjudication is immutable in v0.2.

## Verdicts

- `VERIFIED`
- `PARTIALLY_VERIFIED`
- `REFUTED`
- `INSUFFICIENT_EVIDENCE`

## Local setup

Requirements: Python 3.12+, Git, and internet access.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Lint and test:

```bash
genvm-lint check contracts/evidence_bound.py
pytest tests/direct -v
```

Docker is not required for the direct tests.

## Hosted Studio route

For a first manual deployment without local infrastructure:

1. Open <https://studio.genlayer.com>.
2. Create a new contract.
3. Paste the contents of `contracts/evidence_bound.py`.
4. Compile and deploy it.
5. Call `submit_claim` using a small immutable HTTPS evidence file.
6. Call `resolve_claim` and inspect the validator results.

Do not submit the contribution until the contract has reached consensus on at
least one supported, one partially supported, and one insufficient-evidence
fixture.

## Important v0.2 limits

- Maximum five HTTPS evidence sources.
- Only `RECORD_SET_CLAIM_V1` is accepted.
- Web evidence can change. The supplied manifest digest is a commitment, but
  this version does not yet recompute the digest inside GenVM.
- The contract stores an immutable adjudication; revision chains are not yet
  supported.
- Private or authenticated evidence is not supported.

## Reference demonstration

A claim states that twenty deals were all `claimed`. The evidence shows twenty
verified funding records but includes both `claimed` and `locked` states. A
responsible result is `PARTIALLY_VERIFIED` with reason code
`CLAIMED_RECORDS_MISMATCH`: the funding count is supported, but the claimed
record count is not.

The repository includes this scenario as an explicitly synthetic fixture at
`evidence/fixtures/evidencebound-partial-v1.json`.

## Bradbury v0.1 test — retired

- Contract: `0xE3C2d8B982380ca2034b41d3F9D4d2eD8dE65a1E`
- Deployment transaction: `0x973e76e1150714a70009bebd27a6561af0fbbaecb44b417c9352c254c30128df`
- Resolution transaction: `0x3d6e13e6aaf8e59f9be86ab0def6b217b4737b77999dddde28ba2fb537a01842`
- Network: GenLayer Testnet Bradbury (Phase 1)

The v0.1 resolution ended `undetermined` after an appeal overturned an accepted
result. Validators agreed on `PARTIALLY_VERIFIED` but produced different
confidence labels and reason-code wording. That exposed an overly broad and
brittle equivalence rule. This address is retained as a test record only and
must not be used as the contribution deployment.

Version 0.2 fixes the failure by asking consensus only for a canonical fixed
fact object.

## Bradbury v0.2 deployment

- Contract: `0x4A387168c90C9C700D31FB3F3Fb6c3621Af59e60`
- Deployment transaction: `0xaaf8b3969e31a24bff68ad3d000782f68c7fea8baae5b074fa6c6d2dca2e4ecb`
- GenLayer chain transaction: `0x4841846bac35f87bba730c10f8f8de94952bdb9cf7b2fb75f6e4980237efd61d`
- Network: GenLayer Testnet Bradbury (Phase 1)
- Deployment finalized: 2026-09-23 16:11:54
- Claim submission transaction: `0x33002df7f390a785e705d2b8a4641ebc19f168232edd2dcbf2f110c28d48652b`
- Resolution transaction: `0x6005cc5ca82999fad0f0a5b66088daaac633270d3d81d816387e542cf4f6966b`
- Resolution finalized: 2026-09-23 19:17:08
- Final verdict: `PARTIALLY_VERIFIED` (`HIGH` confidence)
- Reason code: `CLAIMED_RECORDS_MISMATCH`

## v0.2 Bradbury test vector

Use the fixture at immutable commit
`e1db917dfae002b191d1f9ce9ce44b149cb02040`:

- Evidence URL: `https://raw.githubusercontent.com/knisaci/EvidenceBound/e1db917dfae002b191d1f9ce9ce44b149cb02040/evidence/fixtures/evidencebound-partial-v1.json`
- SHA-256: `6969d8fd6ac2a46f650fb5c04c24c8b44c8e241cc2df396f376e2506792b43a3`
- Expected consensus facts: 20 total, 17 claimed, 3 locked, 0 other,
  20 funding records verified, and 0 funding mismatches.
- Expected deterministic result: `PARTIALLY_VERIFIED`, `HIGH`, with reason
  `CLAIMED_RECORDS_MISMATCH`.

## Repository layout

```text
contracts/evidence_bound.py       Contract and validator logic
tests/direct/test_evidence_bound.py
docs/SPECIFICATION.md             State, consensus, threat model, roadmap
docs/USER_RUNBOOK.md              Beginner-friendly next steps
evidence/fixtures/                Synthetic public consensus fixtures
```

## Status

Version 0.2 passes local direct tests, the GenVM linter, SDK semantic
validation, and a finalized Bradbury multi-validator resolution. The on-chain
facts and deterministic adjudication match the documented test vector.
