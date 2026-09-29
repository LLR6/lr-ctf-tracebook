# Compatibility

## Runtime

- Python: **3.10+**
- CI target: **3.10 / 3.11 / 3.12**
- CLI: `ctf-tracebook`

## Input

Plain terminal transcripts. Synthetic fixtures currently cover Bash-like and PowerShell prompts.

## Output schemas

- trace record: `lr-ctf-tracebook/v2`

Command categories and redaction-summary keys are compatibility-sensitive.
Parser support may expand without changing prior category meaning.
