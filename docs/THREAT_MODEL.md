# Threat Model

CTF Tracebook converts terminal transcript text into a structured, redacted draft. It never executes commands from the transcript.

## Assets

- unpublished flags;
- tokens/passwords copied into terminal output;
- private keys accidentally pasted into sessions;
- challenge/infrastructure details;
- integrity of the original transcript hash.

## Trust boundary

```text
terminal transcript (untrusted text)
       │
       ▼
 sanitizer
       │
       ▼
 prompt/parser
       │
       ├── command taxonomy
       ├── outcome heuristic
       └── redacted Markdown / JSON
```

## Main risks

### Secret leakage

Regex redaction can miss formats it does not know.

Mitigations:

- redact common flag/token/password/private-key forms by default;
- emit redaction counters;
- preserve `--keep-flags` as an explicit opt-in;
- require manual review before publication.

Redaction coverage is a best-effort guard, not a DLP guarantee.

### Transcript-triggered execution

A transcript may contain dangerous shell commands.

Invariant: transcript content is parsed as text only. It must never be passed to a shell or subprocess.

### False reasoning

Command output shows what happened, not why the operator chose it.

The generated draft intentionally leaves reasoning/decision fields for the human author.

### Parser confusion

Prompt-like output may look like a shell prompt.

Synthetic Bash, debugger and PowerShell fixtures are kept as regression tests, but arbitrary terminal formats can still be ambiguous.

## Non-goals

CTF Tracebook does not:

- connect to challenge infrastructure;
- execute exploit scripts;
- validate flags against a server;
- infer authorization;
- guarantee all secrets are removed.

## Publication checklist

Before publishing a generated writeup:

- inspect the redaction summary;
- search manually for IPs, domains, usernames and tokens;
- confirm the event permits writeups;
- remove unpublished challenge material;
- add human reasoning rather than treating the draft as final.
