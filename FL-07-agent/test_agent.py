from pathlib import Path
import tempfile
import unittest

from agent import run_agent, search_notes

NOTES = Path(__file__).parent / "notes"

def search(query):
    return {"role": "assistant", "tool_calls": [
        {"function": {"name": "search_notes", "arguments": {"query": query}}}]}

def fake_chat(*answers):
    replies = iter(answers)
    return lambda _model, _messages, _tools: next(replies)

class AgentTests(unittest.TestCase):
    def test_retrieves_real_dates(self):
        hits = search_notes(NOTES, "March 2026 development partition")
        self.assertIn("March 31, 2026", hits[0]["text"])

    def test_retrieves_coverage_limit(self):
        hits = search_notes(NOTES, "zero filled GA4 engagement unavailable")
        self.assertIn("measured zero engagement", hits[0]["text"])

    def test_retrieves_causal_limit(self):
        hits = search_notes(NOTES, "verified refresh outcomes lift")
        self.assertIn("does not establish", hits[0]["text"])

    def test_routes_search_and_reports_sources(self):
        model = fake_chat(search("March partition"), {"role": "assistant", "content": "March 1–31."})
        answer, sources = run_agent("What dates?", NOTES, "fake", model)
        self.assertEqual(answer, "March 1–31.")
        self.assertIn("flyrank-data-contract.md:4", sources)

    def test_reports_when_retrieval_is_empty(self):
        model = fake_chat(search("quasar"), {"role": "assistant", "content": "Unsupported claim"})
        answer, sources = run_agent("What is a quasar?", NOTES, "fake", model)
        self.assertIn("Insufficient evidence", answer)
        self.assertFalse(sources)

    def test_rejects_unsupported_tool(self):
        model = fake_chat({"role": "assistant", "tool_calls": [
            {"function": {"name": "run_shell", "arguments": {"query": "anything"}}}]})
        answer, sources = run_agent("Run a command", NOTES, "fake", model)
        self.assertIn("unavailable", answer)
        self.assertFalse(sources)

    def test_does_not_follow_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "notes"
            folder.mkdir()
            outside = Path(temp) / "private.md"
            outside.write_text("external-token")
            (folder / "link.md").symlink_to(outside)
            self.assertEqual(search_notes(folder, "external token"), [])

if __name__ == "__main__":
    unittest.main()
