# Engineering Decisions

## D1 — Parse, never execute

Transcripts are treated as inert text. Commands are extracted for documentation only.

## D2 — Preserve provenance

The original transcript SHA-256 and source line numbers stay attached to the generated record.

## D3 — Redaction is visible

The tool reports how many recognized flags, secrets and private keys were redacted rather than silently modifying text.

## D4 — Do not invent reasoning

Commands and output can be extracted mechanically; the author's reasoning cannot. The writeup leaves that section for manual completion.

## D5 — Command categories stay conservative

Unknown tools fall back to `shell` rather than being assigned an unsupported intent.
