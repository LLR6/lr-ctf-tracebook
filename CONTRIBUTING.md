# Contributing

Good contributions improve parsing, provenance, redaction, benchmarks, or documentation without turning the project into an execution framework.

## Rules

- Parser changes should include a synthetic transcript fixture.
- Redaction changes must include tests for both removal and reporting.
- New command categories should be conservative.
- Do not infer or invent reasoning that is not present in the transcript.
- Do not add automatic command execution.

## Checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/evaluate_transcripts.py benchmarks/transcripts.json --fail-on-regression
```
