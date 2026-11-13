# Agent build log and recording plan

The spec was written before implementation. The first implementation uses one file-search tool, with no web lookup or file writes. The tool caps the amount of text returned and skips symlinks. Tests cover the successful retrieval loop, empty results, a rejected unsupported tool and a symlink pointing outside the notes folder. The live model stage was not exercised because no local Ollama runtime was available during preparation.

## FL-07 raw run

Record one continuous capture of about two minutes after the local model is installed. Start with the terminal in the agent folder. Run the example coverage question and show the cited Markdown lines next to the answer. Keep the entire run, including any delay or failure, in the raw capture.


## Verification update

All seven Python tests passed. The retrieval tests used real local Markdown with controlled model responses. Ollama was unavailable in this workspace and requests for the runtime/model timed out. The live model loop and raw recording are still pending.

## Website iteration — 2026-11-13

The user verified a live run with Ollama `qwen3:4b`, including a GA4 answer and retrieved source line references, and completed a browser recording. The original CLI had no browser interface. Added a localhost-only Python standard-library HTTP server (`web_app.py`) and responsive static web UI (`web/index.html`). The `/api/ask` endpoint calls the existing `run_agent` function, preserving the live Ollama + read-only note-search workflow. Added input length checks and basic error handling. Kept the scope narrow: no login, upload, note editing, or internet browsing. The raw demo recording is submitted separately and is intentionally excluded from this repository.
