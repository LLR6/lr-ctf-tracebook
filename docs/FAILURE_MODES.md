# Known Failure Modes

- Prompt parser misses an unfamiliar shell.
  - Commands remain unassigned; do not invent them.
- Output text contains the word "error" but command actually succeeded.
  - `error-like` is only a heuristic label.
- Sensitive text is not covered by current redaction patterns.
  - Manual review remains mandatory before publishing.
- Multiline command is split incorrectly.
  - Preserve source lines; extend parser with a fixture.
- Tool-generated draft is mistaken for the author's reasoning.
  - Reasoning fields remain explicitly manual.
