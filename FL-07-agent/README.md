# FL-07 Study Notes AI Assistant

A local question-answering agent built with Python, Ollama (Qwen3 4B), and a localhost web interface. It searches the bundled FlyRank study note, answers with source line references, and proposes a practice question.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running
- Qwen3 4B downloaded locally

## Run the web app

From this folder, pull the model once and start the server:

```bash
ollama pull qwen3:4b
python3 web_app.py
```

Open http://127.0.0.1:8765 in a browser. The server listens on localhost only. Stop it with Ctrl+C.

## Run the command-line agent

```bash
python3 agent.py "Why are zero-filled GA4 fields misleading?"
```

To search other UTF-8 Markdown notes, pass a notes directory with the CLI's `--notes` option. Do not put private or client data in notes used for public demonstrations.

## Tests

Run the seven offline unit tests with controlled model responses:

```bash
python3 -m unittest -v
```

These tests cover note retrieval, empty evidence, tool restrictions, symlink handling, and source reporting. They do not replace a live Ollama run. The successful live run is shown in the separately submitted raw demo recording; the large recording is intentionally excluded from this repository.

## How it works and limits

The model requests a single read-only note-search tool. Python validates the tool request, searches local Markdown, and returns a small set of matching lines. The model then drafts an answer and practice question; the UI displays the retrieved source references so the reader can check the evidence.

Search is word-based and may miss paraphrases. A source citation shows which lines were retrieved; it does not guarantee that every generated claim is correct. The app has no internet access, file-writing tool, or note-editing feature.
