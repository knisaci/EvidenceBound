# Steward response: claim binding in v0.3

The review correctly identified two related defects in v0.2: the stored
free-form statement was not evaluated, and `expected_facts_json` accepted
subsets. A caller could therefore omit consequential assertions and obtain
`VERIFIED` for the supplied subset.

Version 0.3 removes the caller-supplied statement and replaces optional expected
facts with a canonical structured claim. Submission now requires exactly all
six consequential facts, rejects inconsistent totals, and generates the stored
statement deterministically from that object. Resolution compares all six claim
facts against the consensus-established evidence facts.

The direct test suite specifically proves that incomplete and internally
inconsistent claims revert, that the generated statement represents all six
facts, and that material validator disagreement is rejected.

The v0.2 Bradbury address is retained only as historical evidence. The current
submission will use a fresh v0.3 deployment whose source matches the repository.

## Finalized Bradbury evidence

- Contract: `0x490817c879b019a5099F937EaF5672bCA887DfA3`
- Deployment transaction: `0x7b3f1f3f3305c0a39cc3ffded38a54fc7c74b6c858abedaa51446616898358a7`
- Resolution transaction: `0x42779183162d31586d24eea48658295023524797a9f6045a262686d85a084e38`
- Resolution finalized: 2026-09-28 17:59:59
- Result: `PARTIALLY_VERIFIED`, `HIGH`, with
  `CLAIMED_RECORDS_MISMATCH` and `LOCKED_RECORDS_MISMATCH`.
