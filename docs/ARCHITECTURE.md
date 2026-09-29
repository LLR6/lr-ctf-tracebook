# CTF Tracebook Architecture

```text
local transcript
      ↓
ANSI cleanup
      ↓
secret / key / flag redaction
      ↓
prompt + command extraction
      ↓
command taxonomy
      ↓
outcome heuristic
      ↓
JSON record
 ├─ source SHA-256
 ├─ summary
 ├─ redaction_summary
 └─ entries[]
      ↓
Markdown writeup draft
```

## Invariants

- Input text is never executed.
- Source SHA-256 is retained.
- Default output redacts recognized secrets and flags.
- The tool does not invent analyst reasoning.
- Benchmarks validate full-session parsing behavior.

## Non-goals

- running exploit scripts;
- connecting to targets;
- generating offensive commands;
- replacing the author's own writeup reasoning.
