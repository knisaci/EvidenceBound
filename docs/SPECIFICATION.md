# EvidenceBound v0.2 Specification

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
fixed extraction schema is:

- `total_records`;
- `claimed_records`;
- `locked_records`;
- `other_records`;
- `funding_records_verified`;
- `funding_mismatches`; and
- `source_sufficient`.

## Consensus invariant

The leader and validators independently fetch the declared evidence and extract
the seven fields above. Each execution serializes the result as canonical JSON.
GenLayer's `strict_eq` principle requires exact equality of that JSON.

Only after consensus does deterministic code derive the verdict, confidence
bucket, reason codes, contradiction details, and explanation. No validator is
asked to independently invent those labels or prose.

## Stored state

Each claim stores its submitter, subject, statement, profile, evidence URLs,
manifest commitment, expected facts, period, adjudication fields, and resolution
status. Version 0.2 permits only the transition `PENDING -> resolved verdict`.

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

Validators independently rerun retrieval and extraction, then strictly compare
the canonical fixed fact object. A materially different leader extraction is
rejected.

### Consensus brittleness

Version 0.1 incorrectly asked validators to agree on LLM-generated verdicts,
confidence labels, reason codes, and critical-fact naming. A Bradbury appeal
showed that semantically agreeing validators could vary those labels and leave
the transaction undetermined. Version 0.2 removes those outputs from the LLM
and derives them deterministically from the consensus facts.

### Oversized evidence

The source count is capped at five. A byte-size limit should be introduced when
the currently supported GenVM response-size behaviour has been measured.

## Acceptance criteria for v0.2

- Linter passes.
- Direct-mode tests pass.
- Hosted or local Studio reaches consensus for three fixed fixtures.
- A malicious prompt embedded in evidence does not change the output schema or
  cause the evaluator to follow evidence instructions.
- Validator disagreement prevents state mutation.
- README explains why consensus is substantive.

## Planned work

- Content digest recomputation inside the contract.
- Revision and supersession chains.
- Registered evaluation profiles.
- Evidence-source type policy.
- Additional fixed fact vocabularies for new profiles.
