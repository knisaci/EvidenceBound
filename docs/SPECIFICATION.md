# EvidenceBound v0.1 Specification

## Purpose

EvidenceBound converts a precisely scoped public claim and a bounded evidence
set into a consensus-governed, structured adjudication.

## Non-goals

- Deciding unrestricted questions about the world.
- Browsing for evidence not declared by the submitter.
- Accepting private or authenticated sources.
- Producing legal, financial, or investment advice.
- Treating LLM confidence as a mathematical probability.

## Evaluation profile: RECORD_SET_CLAIM_V1

This profile evaluates assertions about a bounded collection of records. Its
material dimensions are:

- record count;
- record identity;
- status distribution;
- defined measurement period;
- claimed versus observed values;
- missing and contradictory records.

## Consensus invariant

An adjudication is accepted only when the leader and validators independently
agree on:

1. the exact verdict;
2. the exact confidence bucket;
3. the exact normalized reason-code set; and
4. the exact canonical claim-critical facts.

Explanatory prose and non-critical findings may differ.

## Stored state

Each claim stores its submitter, subject, statement, profile, evidence URLs,
manifest commitment, expected facts, period, adjudication fields, and resolution
status. Version 0.1 permits only the transition `PENDING -> resolved verdict`.

## Threat model

### Prompt injection

Evidence is explicitly delimited and described as untrusted data. The model is
instructed never to follow instructions embedded inside the evidence. Tests with
adversarial evidence should be added before submission.

### Source drift

Leader and validators retrieve sources separately. Rapidly changing evidence can
cause disagreement and leave the transaction undetermined, which is safer than
writing a disputed result. Production use should prefer content-addressed or
immutable evidence.

### Malicious leader

Validators independently rerun retrieval and evaluation, then compare material
fields. A schema-valid but substantively false leader result is rejected.

### Consensus brittleness

Exact comparison is intentionally limited to stable decision fields. If reason
codes or critical-fact naming prove unstable in multi-validator tests, the
normalization rules must be tightened rather than weakening validation.

### Oversized evidence

The source count is capped at five. A byte-size limit should be introduced when
the currently supported GenVM response-size behaviour has been measured.

## Acceptance criteria for v0.1

- Linter passes.
- Direct-mode tests pass.
- Hosted or local Studio reaches consensus for three fixed fixtures.
- A malicious prompt embedded in evidence does not change the output schema or
  cause the evaluator to follow evidence instructions.
- Validator disagreement prevents state mutation.
- README explains why consensus is substantive.

## Planned v0.2

- Content digest recomputation inside the contract.
- Revision and supersession chains.
- Registered evaluation profiles.
- Evidence-source type policy.
- More robust canonical fact vocabulary.
