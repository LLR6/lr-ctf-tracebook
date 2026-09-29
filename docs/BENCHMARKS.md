# Benchmarks

Fixture index: `benchmarks/transcripts.json`

Synthetic transcripts currently cover:

- shell inspection;
- debugger use;
- Python analysis;
- PowerShell parsing;
- error-like output.

Run:

```bash
python scripts/evaluate_transcripts.py benchmarks/transcripts.json --fail-on-regression
```

The gate checks command count, category distribution and error-like step count.

Separately, unit tests verify secret / flag / private-key redaction summaries.

The benchmark validates parser behavior only. It does not validate or execute CTF techniques.
