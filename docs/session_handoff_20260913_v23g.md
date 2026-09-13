# Session Handoff — 2026-09-13 abend (v23g-smallmodel)

> Stand: phi-4-mini promoviert (59/54/177), Kleinstmodell-Grenze dokumentiert | Nächster Meilenstein: Plattform-Eintragung → Tag `v1.0-bwki-submission` → Puffer bis 20.09.

## Entscheidung (Evidenz vor Wunsch)

User-Order war "4 alle → 62/57/186". Befund: nur **phi-4-mini** formal-fähig (ZH-DE +0.087, p<0.01, ~140 Konzepte/Sprache). qwen2.5-0.5b ZH-DE n.s. (p=0.168, floor NaN), hy-mt2-1.8b floor überall NaN (ZH-EN LDS=1.0 = retired Leermengen-Artefakt), gemma-3-270m Format-inkompatibel (crashte `lds_c_multi_model.py`, isoliert nach `Temp/opencode/quarantine/`). **Statt 62: 59/54/177 formal + 3 als Boundary-Sektion** (Portal-Panel mit 2 Vergleichscharts, Paper-§8.15-Absatz, §6-Zeile). User kann 62 überstimmen — dann braucht es Cross-Extraktion + Methoden-Disclosure.

Zahlen formal 59: ZH-DE 59/59; EN n.s. 9/177 (+phi ZH-EN); CN 48/48 (0.130) vs West 11/11 (0.155, ohne luna 10/10 0.148); dedup 54/54 (0.137); Youden 59: 0.12, CI 0.12–0.13; votes 62: ≥10 237/157, Heimat:safety 48 → "48 von 62"; file-truth 62/57/186; §6 1087 Zeichen (Puffer groß); PDF 231718B ×3; pytest 84/84; Wave-2 ALL OK.

## Offen
1. Plattform-Upload (User): §6 = 1087, unkritisch
2. Tag `v1.0-bwki-submission` nach Eintragung
3. gemma-Re-Run (reparierter Kollektor) + Kleinstmodell-Extraktionsschiene = registrierte Folgearbeit
4. C4-Mono-Bug frozen; Video/SRT baked-freeze; `sync_readmes.py` verboten
5. Uncommitted: 3 lokale n=30-Files (phi/qwen2.5/hy-mt2) + 8 Sammel-Files — Welle läuft ggf. weiter

## Zähl-SSOT (aktuell)
- 556/525/219 · 204 = 32+83+89 · **59/54/177** (file-truth 62/57/186) · qwen-max n=26/30 · phi +0.09 · F1 0,881/0,939 · N=15 Δ≈0 · Freeze 0,9336/0,9382/0,5188 · T1 0,52→0,99
