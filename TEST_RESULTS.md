# EvidenceBound v0.1 Test Record

Tested on 2026-09-21 with:

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
5. a validator rejects a materially different verdict and reason-code set.

## Linter

The linter command was started, but its remote GenVM-version resolution did not
complete in the available environment. This is not recorded as a pass or a
contract failure. Re-run the following command in a normal network environment:

```bash
genvm-lint check contracts/evidence_bound.py
```

## Still required before submission

- successful linter completion;
- multi-validator execution in hosted or local GenLayer Studio;
- adversarial prompt-injection fixture;
- stable consensus on verified, partially verified, and insufficient-evidence
  cases.
