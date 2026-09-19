# Session Handoff — 2026-09-14 (v26-nobridges)

> Stand: 10 STEAM-Bridges retiriert (839 intra-only), Portal-Zahlen 1143/238-of-525 ehrlich gestellt, Steam-Panel `(hidden)`-Tag | Nächster Meilenstein: 72er-Blindaudit fertig → `--import`-Verdict → Plattform-Eintragung → Tag `v1.0-bwki-submission`.

## Entscheidung (Evidenz vor Wunsch)

1. **Bridges gelöscht, nicht aufgewertet.** Die 10 frozen Paare waren eine hand-picked Allowlist (shared en-labels, Typ `analogy`), kein systematisches Cross-Discipline-Mining. Behalten hätte eine entdeckte Struktur impliziert, die es nicht gibt. Archiv mit Begründung: `research/steam_bridges_retired_2026-09-14.json`. STEAM = Side-by-Side-Vergleichsansicht (1143 nodes / 839 intra-discipline links / 0 bridges, `steam-v2`). Viewer: Bridge-Zeile/Legende/`legend.bridge`/`steam.bridges`-Keys entfernt, `about.body_steam` EN/DE/ZH mit Retirement-Hinweis, tote `cross_discipline`-Branches bereinigt (`steamVisible`, `linkColorCB`, `linkWidthCB`).
2. **Chemie-0/0 war kein Datenbug.** Verifiziert: `refreshSteamPanel` zählt `steamVisible()`-gefiltert; bei abgewählter Chemie zeigt die Zeile 0/0 und Bridges fallen von 10 auf 5 (genau die 5 math-phys-Paare). Repo + `_deploy` hatten immer chem 220/215. Fix: `(hidden)`-Tag pro abgeblendeter Zeile (`steam.hidden`: EN `(hidden)` / DE `(ausgeblendet)` / ZH `（已隐藏）`), headless verifiziert, 0 JS-Errors.
3. **Portal-Wording vereinheitlicht.** Mathematik überall "556 nodes · 238 rendered links (of 525 aligned relations) · 219 groups"; Totals exakt **1,143** (statt 1,140+); Scope-Note EN/DE/ZH nennt STEAM-Vergleichsansicht (839 intra, no cross-links). Paper-Quoten (Mermaid/Abstract/Finding-Freeze/MIMO-Pipeline) unangetastet — das ist Math-Pipeline-Wahrheit.

Zahlen: 556/238of525/219 · 367/386/0.0057 · 220/215/0.0089 · STEAM 1143/839/0 · **59/54/177** · F1 0.881 · pytest 84/84 · Shots 7 neu (steam_overview×3, portal_hero×3, portal_full; DE/ZH bildverifiziert).

## Offen

1. **72er-Blindaudit (User läuft)**: `research/gold_review_v2/workbench.html` öffnen → Export → `python scripts/gold_blind_audit.py --import review_72_filled.json`. Pass iff F1≥0.85 UND Agreement≥0.8 UND jede Sprache≥0.7 (reject = F1 0, im Code enforced). Pass → C9b→Mature + Fußnoten; maintain → Developing bleibt, Report archivieren.
2. Gloss-30 (`research/wiki_gloss_audit_30.json`) wartet auf BAILIAN-Key für qwen-Kreuzhälfte.
3. Plattform-Upload (User): §6 = 1087, danach Tag `v1.0-bwki-submission`.
4. Uncommitted (bleibt so): 9× `data/lds_c/llm_subject/*_20260913.json` (§2.3/§3-Re-Runs, Compute ausstehend); `linguaGraph.db` ignoriert.
5. C4-Mono-Bug frozen; Video/SRT baked-freeze; `sync_readmes.py` verboten; keine AI-Annotierung (PROTOCOL §4).

## Zähl-SSOT (aktuell)

- 556/525/219 · 367/386 · 220/215 · STEAM 1143/839/0 · 204 = 32+83+89 · **59/54/177** (file-truth 62/57/186) · F1 0,881 (sozial DB 0,939† Developing, machine-seeded; Harness ~0,65) · N=15 Δ≈0 · Freeze 0,9336/0,9382/0,5188 · T1 0,52→0,99 · Commits 09-14: ba25b33 / 03ce125 / 716c262 / 7397d47 / 9874971 / 8fc81ef+d5cea60
