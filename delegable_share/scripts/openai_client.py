"""Minimal OpenAI client with a project-wide spend ledger and hard cap.

Every call is logged to coding/openai_ledger.jsonl with token counts and estimated cost.
A call is refused if the ledger total already exceeds PROJECT_CAP_USD. The key is read from
the repo-root .env (OPENAI_API_KEY) and is never printed.
"""
import datetime
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = ROOT.parent / ".env"
LEDGER = ROOT / "coding" / "openai_ledger.jsonl"
PROJECT_CAP_USD = 80.0  # user's budget for the whole project (2026-11-09)

# USD per million tokens (input, output). Third-party listings, 2026-11; check OpenAI's page.
PRICES = {"gpt-6.1-terra": (1.0, 5.0)}
DEFAULT_MODEL = "gpt-6.1-terra"


def _key():
    for line in ENV.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("OPENAI_API_KEY not found in .env")


def spent():
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l)["usd"] for l in LEDGER.read_text().splitlines() if l.strip())


def chat_json(messages, purpose, model=DEFAULT_MODEL, timeout=600):
    """Send a chat completion that must return a JSON object. Returns (parsed, usage)."""
    if spent() >= PROJECT_CAP_USD:
        raise RuntimeError(f"OpenAI project cap ${PROJECT_CAP_USD} reached ({spent():.2f} spent)")
    body = json.dumps({"model": model, "messages": messages,
                       "response_format": {"type": "json_object"}}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read())
    u = resp.get("usage", {})
    pin, pout = PRICES.get(model, (5.0, 25.0))  # unknown model: assume expensive
    usd = (u.get("prompt_tokens", 0) * pin + u.get("completion_tokens", 0) * pout) / 1e6
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps({"time": datetime.datetime.now().isoformat(timespec="seconds"),
                            "model": resp.get("model", model), "purpose": purpose,
                            "prompt_tokens": u.get("prompt_tokens"),
                            "completion_tokens": u.get("completion_tokens"),
                            "usd": round(usd, 4)}) + "\n")
    return json.loads(resp["choices"][0]["message"]["content"]), u
