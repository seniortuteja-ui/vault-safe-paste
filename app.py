"""Vault Safe Paste: screen CRM text and scripts with Clocked before they travel."""
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

load_dotenv()
from clocked_sdk import Clocked, ClockedError  # noqa: E402  (after load_dotenv)

BASE = Path(__file__).parent
app = FastAPI(title="Vault Safe Paste")
_client = None


def client() -> Clocked:
    global _client
    if _client is None:
        _client = Clocked()  # reads CLOCKED_API_KEY
    return _client


class Note(BaseModel):
    text: str = Field(min_length=1, max_length=20000)


class Script(BaseModel):
    script: str = Field(min_length=1, max_length=20000)


def fail(e: Exception):
    status = getattr(e, "status", None) or 502
    raise HTTPException(status_code=status if 400 <= status < 600 else 502,
                        detail=str(getattr(e, "error", e)))


@app.post("/api/scan")
def scan(n: Note):
    """Guard first (fail closed), then Protect."""
    try:
        guard = client().injection(text=n.text, source="user", evidence=True)
        # Anything other than a benign verdict is treated as unsafe.
        if guard.get("verdict") != "benign":
            return {"blocked": True, "guard": dict(guard)}
        pii = client().pii(text=n.text, anonymize="replace")
        return {"blocked": False, "guard": dict(guard),
                "masked": pii.get("anonymized_text"), "pii": dict(pii)}
    except ClockedError as e:
        fail(e)


@app.post("/api/inspect")
def inspect(s: Script):
    """Inspect: classify what a script would do before anyone runs it."""
    try:
        return dict(client().script(script=s.script, threshold=0.3, evidence=True))
    except ClockedError as e:
        fail(e)


@app.get("/api/samples")
def samples():
    return json.loads((BASE / "samples.json").read_text())


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")
