"""Cross-check: run Stage 1 briefs through an OpenAI model (default gpt-6.1-terra).

Uses the same brief body as the Claude subagents (everything from "=== INSTRUCTIONS ==="),
with the file-writing wrapper replaced by a return-JSON instruction. Writes
coding/stage1/<tag>_terra/<onetsoc>.json in the same format, so validate_stage1.py works on it.

Usage: python3 scripts/openai_stage1.py <tag>
"""
import json
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from openai_client import DEFAULT_MODEL, ROOT, chat_json, spent  # noqa: E402

SYSTEM = ("You are a coder in a research pipeline. Follow the instructions exactly. "
          "Code each TARGET independently, in the order given.")
RETURN = ('Return a JSON object {"items": [...]} with one element per target, in the order '
          'given. Each element is the output object described in the instructions, with '
          '"task_id" added as its first key. Return nothing else.')


def run(batch, outdir):
    body = (ROOT / batch["brief"]).read_text()
    body = body[body.index("=== INSTRUCTIONS ==="):]
    parsed, u = chat_json([{"role": "system", "content": SYSTEM},
                           {"role": "user", "content": body + "\n\n" + RETURN}],
                          purpose=f"stage1 {outdir.name} {batch['onetsoc']}")
    items = parsed.get("items", parsed if isinstance(parsed, list) else [])
    (outdir / f"{batch['onetsoc']}.json").write_text(json.dumps(items, indent=1))
    return batch["onetsoc"], len(items), u


def main():
    tag = sys.argv[1]
    manifest = json.loads((ROOT / "coding" / "stage1" / tag / "manifest.json").read_text())
    outdir = ROOT / "coding" / "stage1" / f"{tag}_terra"
    outdir.mkdir(parents=True, exist_ok=True)
    before = spent()
    with ThreadPoolExecutor(3) as ex:
        for code, n, u in ex.map(lambda b: run(b, outdir), manifest["batches"]):
            print(code, n, "items", u)
    (outdir / "RUN.json").write_text(json.dumps({"model": DEFAULT_MODEL, "tag": tag}, indent=1))
    print(f"this run ${spent() - before:.3f}; project total ${spent():.3f}")


if __name__ == "__main__":
    main()
