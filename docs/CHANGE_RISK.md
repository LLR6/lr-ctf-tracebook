# Change Risk Policy

Low risk: docs and examples.

Medium risk: new prompt parsers, new command categories.

High risk: redaction logic, source-line mapping, category redefinition, output schema changes.

Any redaction change must include explicit tests for secrets, flags and private keys. Parser changes must never execute transcript content.
