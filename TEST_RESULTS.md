# EvidenceBound v0.2 Test Record

Tested on 2026-09-23 with:

- Python 3.12.14
- `genlayer-py` 0.18.0
- `genlayer-test` 0.29.2
- `genvm-linter` 0.11.1rc2

## Direct tests

Command:

```bash
pytest tests/direct -v
```

Result: **5 passed**.

Covered behaviours:

1. valid submissions enter `PENDING` state;
2. non-HTTPS evidence is rejected;
3. a partial-verification result is stored correctly;
4. a resolved claim cannot be resolved again; and
5. `strict_eq` rejects a materially different extracted fact object.

## Linter

Command:

```bash
genvm-lint check contracts/evidence_bound.py
```

Result: **lint passed (3 checks); SDK validation passed**.

## Bradbury v0.1 failure that motivated v0.2

The v0.1 resolution transaction
`0x3d6e13e6aaf8e59f9be86ab0def6b217b4737b77999dddde28ba2fb537a01842`
ended `undetermined` after an appeal overturned the accepted result. Different
rounds agreed on `PARTIALLY_VERIFIED` and on the material counts, but varied the
confidence bucket and reason-code wording.

Version 0.2 therefore limits consensus to a fixed seven-field fact object and
derives all decision labels deterministically.

## Bradbury v0.2 deployment

The replacement contract deployment finalized successfully:

- Contract: `0x4A387168c90C9C700D31FB3F3Fb6c3621Af59e60`
- Deployment transaction: `0xaaf8b3969e31a24bff68ad3d000782f68c7fea8baae5b074fa6c6d2dca2e4ecb`
- Deployment finalized: 2026-09-23 16:11:54
- Claim submission transaction: `0x33002df7f390a785e705d2b8a4641ebc19f168232edd2dcbf2f110c28d48652b`
- Resolution transaction: `0x6005cc5ca82999fad0f0a5b66088daaac633270d3d81d816387e542cf4f6966b`
- Resolution finalized: 2026-09-23 19:17:08
- Stored result: `PARTIALLY_VERIFIED`, `HIGH`,
  `CLAIMED_RECORDS_MISMATCH`
- Consensus facts: 20 total, 17 claimed, 3 locked, 0 other, 20 funding
  records verified, and 0 funding mismatches.

## Still required before submission

- adversarial prompt-injection fixture;
- additional Bradbury fixtures for verified and insufficient-evidence cases.
