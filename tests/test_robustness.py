import unittest

from tracebook.cli import extract, sanitize


class RobustnessTests(unittest.TestCase):
    def test_arbitrary_text_does_not_invent_commands(self):
        record = extract("plain text\nwith no shell prompt\n")
        self.assertEqual(record["entries"], [])
        self.assertEqual(record["summary"]["commands"], 0)

    def test_empty_transcript_is_valid(self):
        record = extract("")
        self.assertEqual(record["entries"], [])
        self.assertEqual(record["unassigned_lines"], 0)

    def test_ansi_and_secret_redaction_can_coexist(self):
        raw = "\x1b[31m$ echo x\x1b[0m\ntoken=secret-value"
        text, summary = sanitize(raw)
        self.assertNotIn("\x1b", text)
        self.assertNotIn("secret-value", text)
        self.assertGreaterEqual(summary["ansi_sequences_removed"], 1)
        self.assertEqual(summary["secret_values_redacted"], 1)


if __name__ == "__main__":
    unittest.main()
