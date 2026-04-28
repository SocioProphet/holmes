# Holmes CLI

`holmes` is the local command-line surface for the Holmes language intelligence fabric.

It is a releaseable skeleton for evidence-first language workflows. Runtime integrations with Sherlock Search, The Canon, Deduction Engine, Mycroft Router, Moriarty Bench, Irene Shield, and 221B are declared but intentionally reported as `not-yet-wired` until their backing services are integrated.

## Command contract

```bash
holmes --version
holmes doctor
holmes self-test
holmes emit-evidence
holmes analyze examples/sample.txt
holmes search "truth and evidence"
holmes graph examples/sample.txt
holmes govern examples/sample.txt
```

## Build and validation

```bash
make build
make test
make validate
make dist
make release-dry-run
```

`make validate` runs the contract validator and exercises the compiled CLI.

## Prophet CLI delegation

`prophet-cli` should delegate these command families to `holmes`:

```bash
prophet holmes analyze <path>
prophet holmes search <query>
prophet holmes graph <path>
prophet holmes govern <path>
```

## Integration boundaries

Holmes owns the language intelligence product surface.

Sherlock Search owns discovery and retrieval.

Prophet Core Query owns shared governed query contracts.

Agentplane owns governed execution and evidence replay.

Prophet Platform owns runtime deployment and platform records.

SourceOS Model Carry owns local carry refs and on-device service access.

## Current skeleton behavior

- `analyze` performs deterministic local file analysis: byte count, line count, word count, SHA-256, and evidence ref.
- `search`, `graph`, and `govern` return deterministic `not-yet-wired` records with stable evidence ids.
- `doctor` reports declared components as pending rather than pretending they are wired.
