import unittest
from tracebook.cli import extract, render


class TranscriptTests(unittest.TestCase):
    def test_commands_and_line_numbers(self):
        record = extract("header\n$ file x\nELF\n$ python solve.py\nflag{demo}")
        self.assertEqual([e["line"] for e in record["entries"]], [2, 4])
        self.assertIn("[REDACTED FLAG]", render("Demo", record))

    def test_ansi_and_secret_redaction(self):
        record = extract("\x1b[32m$ echo ok\x1b[0m\nAuthorization: Bearer secret-value")
        self.assertEqual(record["entries"][0]["command"], "echo ok")
        self.assertNotIn("secret-value", str(record))

    def test_no_invented_commands(self):
        self.assertEqual(extract("plain output without a shell prompt")["entries"], [])


if __name__ == "__main__":
    unittest.main()
