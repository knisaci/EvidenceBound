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

- Contract: `0x7126602956E61E7aBF191C4d44f0DAd6ac248A09`
- Deployment transaction: `0x570f5ffa76996828eb794a5813d6a63b51eb0e764a9804814c9bf9e6a291e71d`
- Finalized: 2026-09-23 13:02:38

## Still required before submission

- multi-validator execution of v0.2 in hosted GenLayer Studio;
- adversarial prompt-injection fixture;
- stable consensus on verified, partially verified, and insufficient-evidence
  cases.
