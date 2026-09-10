# Session Handoff — 2026-09-10 (v0.14.0 Western Extension)

> Stand: master `cf487d7` | Nächster Meilenstein: Plattform-Eintragung (bis 9/13) → Tag `v1.0-bwki-submission` → Puffer bis 20.09.

## Was diese Session geliefert hat

v0.14.0: 51 → **55 vollständige Messungen** (50 Identitäten, 5 Dual-Host-Paare),
ZH-DE **55/55 signifikant**, Marge +0.03…+0.42, 8 EN-n.s. unverändert,
Richtung ≥10: 218 vs 147±4, ≥20: 61 vs 12±2. CN ~94%→~87%, West-Layer 2→7
(alle sig, Mittel 0.182). Youden-Optimum 0.13 (CI 0.13–0.14).

## Neue westliche Modelle (alle P1-identisch, je 10/10/10)

| Modell | Host | ZH-DE-Marge | Status |
|---|---|---|---|
| gpt-oss-20b | NVIDIA NIM | +0.132, p=0.0 | ✅ committed |
| command-a-03-2025 | Cohere (CA) | +0.424, p=0.0 | ✅ committed |
| laguna-s-2.1 | Kilo (2. Host) | +0.072, p=0.0 | ✅ committed |
| nemotron-3-super-120b | Kilo (US) | +0.172, p=0.0 | ✅ committed |
| gpt-5.6-luna | opencode-go (Herkunft ungeklärt) | +0.222, p=0.0 | ✅ committed (in Aggregation) |

## Neue Sammeltreiber (committed)

- `scripts/lds_c_opencode_run_subject.py` — P1 via `opencode run` (exe-Pfad, JSON-Events, Kosten-Tracking)
- `scripts/lds_c_gemini_subject.py` — P1 via Gemini Interactions REST (Pacing + 429-Backoff)
- `scripts/lds_c_cf_subject.py` — P1 via Cloudflare Workers AI (max_tokens-Fix, parse_lenient)
- `scripts/sw_fix_analyses.py` — liest jetzt `multi_model_replication_20260910.json`, Western-Stratum

## Geparkt (Dateien lokal, NICHT committed — resume-fähig)

- OR nemotron-3-ultra `:free` 8/30 (50/Tag-Limit, abgebrochen per User-Entscheid)
- grok-4.6 18/30 (opencode, kostenpflichtig — gestoppt, $ ~2 verbraucht)
- gpt-5.6-luna/muse-spark-1.3 partielle Terminal-Dateien (in Aggregation: luna vollständig!)
- gemini-3.8-flash ~2 (429), mistral medium/small (429), CF-Smokes sind committed
- NIM-Fehlversuche: mistral-large (404), gpt-oss-120b (410 EOL), gemma (hängt)

## Tote Kanäle (nicht erneut versuchen ohne neue Keys)

- Groq: 2 Keys 403 (Account-Problem) · Google OAuth-Token (401, ~1h TTL — AIza-Key fehlt)
- zen-Key (OPENAI_API_KEY): 403 auf beiden Endpunkten (seit 08-10-Arrears tot)
- Cloudflare-Token: aktiv, aber 0 Accounts (Scope unzureichend) — Account-ID bekannt
- OR `:free` Shared Pools (gemma, inkling): Tages-Caps

## Keys in .env (gitignored, Backup Temp/opencode/env.bak)

OPENROUTER (+2), DASHSCOPE, NVIDIA, GROQ (tot), GEMINI (OAuth, tot),
MISTRAL (429-limitiert), COHERE ✅, KILO ✅, CLOUDFLARE (Scope-los),
OPENAI_API_KEY (zen, tot).

## Zählungs-SSOT (verifiziert 09-10)

- 55 = 42 DashScope + 7 zen + D1-Baseline + 2 Kilo + 1 Cohere + 1 NIM + 1 opencode-go
- Alt "43 DashScope": 42 + qwen-max-partial; "51" = 50 komplett + qwen-max
- Dual-Host: deepseek-v4-flash, deepseek-v4-pro, glm-5.2, kimi-k2.6, laguna (neu)
- West: nemotron-ultra-free, laguna-free (zen), gpt-oss-20b, command-a, laguna (Kilo), nemotron-super, luna = 7 Messungen / 6 Identitäten

## Offen für 9/13–9/20

1. Plattform-Eintragung (`submission/final/feld_mapping.md` ist aktuell)
2. Video (separater Workflow, Assets fehlen)
3. Tag `v1.0-bwki-submission` nach Eintragung
4. Optional: Mistral-Retry (429-Cooldown), OR-nemotron-Resume (User hat abgelehnt — nur bei Meinungsänderung)
