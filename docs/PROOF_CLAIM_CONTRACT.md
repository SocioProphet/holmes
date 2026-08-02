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
- `methodFamily` (see "CHRONOS carrier alignment" below)
- `nonAuthorityDeclaration` (see "CHRONOS carrier alignment" below)

## CHRONOS carrier alignment

`sociosphere/docs/integration/neurosymbolic-chronos-alignment.md` defines a "CHRONOS
carrier" shape: any object crossing a governance boundary should carry a source
evidence reference, method family, method output type, grounding status, validation
status, explanation trace reference, owning authority plane, non-authority
declaration, replay reference, and a governance decision (or pending decision).

This section is an **additive superset**: it extends the existing
`TruthBounds`/`ReasoningTrace`/`ExplanationTrace` chain above with CHRONOS-carrier
fields, without removing or changing any existing field or behavior. The base
proof-claim shape documented earlier in this file (`ReasoningTrace`,
`ExplanationTrace`, `ProofCertificate`, `ContradictionReport`, `policyReadyClaim`)
is unchanged and remains backward compatible. However, the validator now *requires*
the CHRONOS-carrier fields introduced in this section —
`reasoningTrace[].methodFamily`, `reasoningTrace[].nonAuthorityDeclaration`, and each
worked example's `chronosCarrier` block — in order to pass. Artifacts produced
before this alignment was added are not automatically CHRONOS-carrier-valid; they
need those fields added before they will validate.

Holmes's `TruthBounds`/`ReasoningTrace` mechanism is admissible under that doctrine's
**"LNN-style truth-bound propagation"** method-family row:

- **admissible use**: report lower/upper truth bounds, formula-local inconsistency,
  and interpretable formula structure.
- **forbidden use**: claim global consistency, arbitrary entailment correctness, or
  learned rule structure.

Two new fields on each `ReasoningTrace` step carry that discipline as data:

- `methodFamily` — a constant identifying the method family. Currently only
  `"LNN-style truth-bound propagation"` is used, matching the doctrine's row name
  exactly (`ALLOWED_METHOD_FAMILIES` in `tools/validate_holmes.py`).
- `nonAuthorityDeclaration` — an object stating what this bounded result does
  **not** authorize:
  - `consistencyScope` — must be `"formula_local"`. A value of `"global"` is
    rejected by the validator: this is the forbidden-use case made mechanically
    checkable, not just documented in prose.
  - `doesNotAuthorize` — must include at least `["global_consistency",
    "arbitrary_entailment_correctness"]`.
  - `statement` — human-readable non-authority statement.

A package-level `chronosCarrier` object is attached to each worked example (the
policy-ready claim package that actually crosses the Holmes -> Policy Fabric
governance boundary). It fills the remaining carrier fields the doctrine requires,
reusing Holmes's existing vocabulary wherever it already covers the same ground
instead of duplicating it:

| CHRONOS carrier field | Carried by |
|---|---|
| source evidence reference | `chronosCarrier.sourceEvidenceRef` (also `evidenceRefs` on the trace/explanation/proof artifacts) |
| method family | `reasoningTrace[].methodFamily` |
| method output type | `chronosCarrier.methodOutputType` |
| grounding status | `chronosCarrier.groundingStatus` (`evidence_grounded` \| `ungrounded`) |
| validation status | `chronosCarrier.validationStatus` (reuses `proofCertificate.verificationStatus` / `verificationPath.result`) |
| explanation trace reference | `chronosCarrier.explanationTraceRef` (reuses `explanationTrace.traceId`; may be `null` where no explanation trace was produced, e.g. a candidate rejected before policy) |
| owning authority plane | `chronosCarrier.owningAuthorityPlane` — always `"SocioProphet/policy-fabric"`; Holmes never declares itself the owning authority plane |
| non-authority declaration | `reasoningTrace[].nonAuthorityDeclaration` |
| replay reference | `chronosCarrier.replayRef` (new: `replay://holmes/<claimId>/v1` convention) |
| governance decision (or pending) | `chronosCarrier.governanceDecision` (reuses `policyReadyClaim.admissionStatus` / `verificationPath.result`) |

This does not change who holds authority: Holmes still does not admit claims into
policy-approved truth, and no canonical-schema authority moves into `sociosphere`.
It only makes the existing prose-level ownership and non-authority statements above
carriable as data on the artifact itself.

## Worked examples

Deterministic worked examples are captured in:

- `examples/holmes-proof-claim-contract.json`

They cover:

1. Technical document span -> proposed platform claim -> explanation trace -> contradiction report -> policy-ready claim package, tagged with the `LNN-style truth-bound propagation` method family, a `nonAuthorityDeclaration`, and a `chronosCarrier` block.
2. Vector candidate -> candidate claim -> verification/rejection path, also carrying a `chronosCarrier` block (`groundingStatus: ungrounded`, since it is rejected before proof/evidence verification).

`fixtures/invalid/proof-claim-forbidden-global-consistency-claim.json` is a negative
fixture demonstrating the forbidden use: a `TruthBounds` result whose
`nonAuthorityDeclaration.consistencyScope` is set to `"global"`, as if the bounded
local result proved the whole system is globally consistent. The validator rejects
it.

## Repo boundaries

- Holmes: propose/explain/verify artifacts and traces for claims.
- Sherlock: retrieval/discovery and source evidence acquisition.
- Slash Topics: topic-pack semantics and membranes trained from Holmes evidence artifacts.
- GAIA: graph and world-model grounding inputs used by Holmes reasoners.
- Agentplane: governed runtime execution after policy admission.
- Policy Fabric: admission decisioning (`allow | deny | require_review | provisional`).
