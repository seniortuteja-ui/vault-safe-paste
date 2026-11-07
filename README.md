# Vault Safe Paste

Built for the Clocked Build Challenge (Oct 21 - Nov 10, 2026) by Shobhit Tuteja.

Screens CRM notes and scripts with three Clocked endpoints before they are shared, pasted into an AI tool, or run.

**Live demo:** https://vault-safe-paste.onrender.com

The demo runs on a free instance, so the first load can take about 50 seconds to wake up.

Shobhit Tuteja and CLOCKED BUILD CHALLENGE

| Step | Clocked endpoint | What it changes in the app |
|------|------------------|----------------------------|
| Guard | `injection` | A flagged note is blocked outright; nothing downstream runs (fails closed). |
| Protect | `pii` | A clean note is returned with personal data replaced; the app shows original vs. masked. |
| Inspect | `script` | The verdict is shown before anyone runs a pasted script. |

All demo data in `samples.json` is synthetic. Never paste real CRM data into a public demo.

## Run it

```bash
# Mac / Linux
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your Clocked API key
uvicorn app:app --reload
```

```powershell
# Windows
py -m pip install --user -r requirements.txt
copy .env.example .env      # add your Clocked API key
py -m uvicorn app:app --reload
```
Open http://127.0.0.1:8000. The API key stays on the server and is never sent to the browser.

## Notes
- Any verdict other than `benign` from Guard is treated as unsafe.
- The raw Clocked responses are available under each result for transparency.
