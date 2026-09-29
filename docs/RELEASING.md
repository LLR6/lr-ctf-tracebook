# Releasing CTF Tracebook

## Checklist

1. CI green.
2. Transcript benchmark passes.
3. Redaction tests pass for flags, secrets and private keys.
4. New parser support includes synthetic fixtures.
5. Tool still does not execute transcript commands.
6. Update `CHANGELOG.md`, `pyproject.toml` and `CITATION.cff`.
7. Review `docs/TRACE_MODEL.md`, `docs/BENCHMARKS.md` and `docs/ROADMAP.md`.

Never publish an unreviewed generated writeup as if the tool had reconstructed the user's reasoning.
