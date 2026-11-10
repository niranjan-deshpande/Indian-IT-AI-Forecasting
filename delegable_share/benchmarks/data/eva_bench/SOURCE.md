# eva_bench (ServiceNow EVA-Bench)
Accessed 2026-11-09. Licence: MIT (code and data in repo); HF mirror ServiceNow-AI/eva-bench not used.
- Items: https://github.com/ServiceNow/eva `data/{airline,itsm,medical_hr}_dataset.json`, repo HEAD 8e10190 (2026-11-06).
- Scores: leaderboard data embedded in `docs/assets/index-BNJMtYsi.js` (site https://servicenow.github.io/eva/#results); parsed to raw/leaderboard_models.json.
- Paper: arXiv 2605.13841 (May 2026).

## Population and sampling
Population = all 213 scenarios (airline 50 + ITSM 80 + medical HR 83), the same set the leaderboard pools over.
Ids are `<domain>/<native id>`, sorted; `random.Random(2026).sample(ids, 24)` (13 medical_hr, 7 itsm, 4 airline).
Items hold the caller goal, situation, must-have outcomes and the gold tool-call names from `ground_truth.expected_trace`.
Placeholders replaced by the English culture names. Simulator persona and behaviour rules left out. Build script: eva_bench/scripts/build_eva.py.

## Grading method: `state`
Hidden-DB-state hash comparison (task_completion) plus LLM-judge faithfulness and audio speech-fidelity; headline "EVA-A pass" needs all three.
(Mixed: deterministic state check plus LLM judges.)

## One-line description for time estimators
A phone call from a caller with a goal (airline customer service, HR service delivery for a healthcare employer, or an enterprise IT service desk); the worker verifies the caller, queries and updates the records and tells the caller the right information; done when the right records are changed and nothing false or disallowed was said or done.

## Published human times
None.

## Problems
- Score used: `EVA-A_pass` pooled over 213 scenarios, clean audio (about 3 trials per scenario). Also in notes: task_completion alone (state only), which is higher.
- Each leaderboard row is a whole voice system (STT+LLM+TTS cascade or speech-to-speech model), not a single LLM; scaffolds differ. 22 systems have clean results; 5 listed systems have no clean scores and were skipped.
- Leaderboard has no dates. eval_date is a proxy from git commits that added the results (blank or "2026-05" where in the initial release or unpinned). release_date is blank for several newer models (could not verify); for cascades it is the LLM's release date.
- Some leaderboard names (e.g. "Gemini 3.8 Live", "GPT Realtime 2.1") are as shown on the site; I could not verify them externally.
- Series spans only about May-Oct 2026. Public set; no private set known. Different runs used different settings (LLM streaming, pre-tool speech) per the README.
- Scenario texts are synthetic. Gold tool-call list is from the reference trace and includes lookup calls.
