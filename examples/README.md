# Example transcripts

These are synthetic local transcripts used to demonstrate parsing and writeup structure.

- `session.txt` — minimal shell example.
- `debug-session.txt` — inspection + debugger + script categories.
- `powershell-session.txt` — PowerShell prompt parsing and an error-like script output.

Try:

```bash
ctf-tracebook examples/debug-session.txt --title "Local reversing notes"
ctf-tracebook examples/powershell-session.txt --format json
```

The tool only parses text already present in the transcript. It does not execute any command from these files.
