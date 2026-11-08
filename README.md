# Vault Safe Paste

Built for the Clocked Build Challenge (Oct 21 – Nov 10, 2026) by Shobhit Tuteja, with AI assistance.

**Live demo:** https://vault-safe-paste.onrender.com
The demo runs on a free instance, so the first load can take about 50 seconds to wake up.

Vault Safe Paste checks CRM notes and scripts before they are shared, pasted into an AI tool, or run. People who work with CRM data copy notes into emails, chats and AI assistants all the time. Those notes can contain personal data, and they can contain hidden instructions aimed at whatever reads them next. This app puts three checkpoints in front of that step, using three Clocked endpoints.

All demo data in `samples.json` is synthetic. Never paste real CRM data into a public demo.

## How Clocked is used

| Checkpoint | Clocked endpoint | Request | What the app does with the result |
|---|---|---|---|
| Guard | `injection` | `source="content"`, `evidence=True` | Any verdict other than `benign` blocks the note. The app shows the category, confidence, severity, the quoted evidence, and marks the flagged passage inside the original note using the character offsets Clocked returns. |
| Protect | `pii` | `anonymize="replace"` | Runs only on notes that passed Guard. The app shows the original and the masked version side by side, counts what was masked, and the Copy button copies the masked text only. |
| Inspect | `script` | `threshold=0.3`, `evidence=True` | The verdict, confidence, category and severity are shown before anyone runs a pasted script, and the flagged lines are marked in the script. Scripts are analyzed, never executed. |

The result of each call decides what happens next, not just what is displayed:

- A blocked note stops the flow. Protect is skipped, and the checkpoint cards show "Blocked" and "Skipped: note not trusted".
- A clean note continues to Protect and ends with text that is safe to copy out.
- A malicious script turns the result into a "Do not run this script" warning with the offending lines marked.

I chained Guard and Protect in the app's own code (two SDK calls). Clocked's Pipeline can also run steps in one request. I kept separate calls so each checkpoint is visible in the interface.

## Handling uncertain results, missing information and failed requests

- **Uncertain results:** Guard is fail-closed. Anything other than a `benign` verdict is treated as unsafe. The Inspect threshold is set to 0.3 to lean cautious.
- **Missing information:** Empty input is rejected before any call is made. Input is capped at 20,000 characters on the server. If a response has no evidence offsets, the app falls back to a plain evidence list.
- **Failed requests:** If a Clocked call fails (for example a bad API key), the app shows the error on screen. A note is never passed on as "safe" because a check failed to run.
- **Secrets:** The Clocked API key stays on the server and is never sent to the browser.
- **Privacy:** The server does not store notes. The Copy button copies only the masked text, never the raw API response, which still contains the original values.

## Try it

Open the live demo and use the sample buttons:

1. **Note with hidden injection:** blocked, with the injected sentence marked in the note.
2. **Note with patient detail:** names, date of birth, phone and email masked.
3. **Routine call note:** name, email, phone and address masked.
4. **Clean note:** passes with "No hidden instructions, no personal data found."
5. **Check a script:** "Risky: download and run" comes back malicious with the flagged line marked. "Harmless" comes back benign.

Under every result, "Raw Clocked response" shows exactly what the API returned.

## Run it locally

You need Python 3.10+ and a Clocked API key.

Mac / Linux:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your Clocked API key
uvicorn app:app --reload
```

Windows:
```powershell
py -m pip install --user -r requirements.txt
copy .env.example .env      # add your Clocked API key
py -m uvicorn app:app --reload
```

Then open http://127.0.0.1:8000.

## Project layout

- `app.py`: FastAPI server with `/api/scan` (Guard, then Protect), `/api/inspect` (Inspect) and `/api/samples`.
- `static/index.html`: the whole interface (no build step).
- `samples.json`: synthetic notes and scripts for the demo.

## Limitations and next steps

- Allow or block only. A "needs review" state for borderline results would be a natural next step.
- Masking uses Clocked's default entity types. A per-team allow list (for example, colleagues' first names) could be added.
- It is a web page. A browser extension or an API wrapper would remove the extra copy-and-paste step.
