# Holmes Proof-Claim Contract

## Scope and ownership

Holmes owns the reasoning-layer contract segment of the canonical loop:

`Observe -> Anchor -> Normalize -> Propose -> Explain -> Verify -> Govern -> Act -> Receipt -> Learn`

Holmes ownership is bounded to: `Propose -> Explain -> Verify`.

Holmes does **not** admit claims into policy-approved truth. Policy Fabric evaluates Holmes outputs and decides:

`allow | deny | require_review | provisional`

## Contract invariant

`VectorCandidate | ModelOutput | GraphCandidate -> ProposedClaim -> ExplanationTrace + ProofCertificate? + ContradictionReport`

Vector and model outputs remain `candidate_only` unless sufficient evidence/proof exists and policy admits them.

## Canonical contract mapping (Ontogenesis)

Holmes maps to Ontogenesis canonical contracts without divergence:

- `Claim` -> `ontogenesis.socioprophet.dev/v1/Claim`
- `ProofCertificate` -> `ontogenesis.socioprophet.dev/v1/ProofCertificate`
- `ExplanationTrace` -> `ontogenesis.socioprophet.dev/v1/ExplanationTrace`
- `ContradictionReport` -> `ontogenesis.socioprophet.dev/v1/ContradictionReport`
- `TruthBounds` -> `ontogenesis.socioprophet.dev/v1/TruthBounds`
- `ReasoningTrace` -> `holmes.socioprophet.dev/v1/ReasoningTrace` (Holmes-local minimal trace payload embedded in explanation/proof artifacts; not a separate Ontogenesis canonical object)
- `VectorCandidate` is candidate input only
- `PolicyDecision` is downstream admission status (owned by Policy Fabric, not Holmes)

## Minimal `ReasoningTrace` format

Each reasoning step should include:

- `ruleName`
- `premises` (list)
- `conclusion`
- `evidenceRefs` (list of evidence IDs/URIs)
- `confidence` (0..1)
- `truthBounds` (`lower`, `upper`, `method`)

## Worked examples

Deterministic worked examples are captured in:

- `examples/holmes-proof-claim-contract.json`

They cover:

1. Technical document span -> proposed platform claim -> explanation trace -> contradiction report -> policy-ready claim package.
2. Vector candidate -> candidate claim -> verification/rejection path.

## Repo boundaries

- Holmes: propose/explain/verify artifacts and traces for claims.
- Sherlock: retrieval/discovery and source evidence acquisition.
- Slash Topics: topic-pack semantics and membranes trained from Holmes evidence artifacts.
- GAIA: graph and world-model grounding inputs used by Holmes reasoners.
- Agentplane: governed runtime execution after policy admission.
- Policy Fabric: admission decisioning (`allow | deny | require_review | provisional`).
