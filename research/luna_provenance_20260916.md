# luna-Provenienz (2026-09-16, P0 geschlossen als dokumentiert-undisclosed)

## Befund

- Modell: `opencode-go:gpt-5.6-luna` — Messung 2026-09-10T08:04:04Z via `scripts/lds_c_opencode_run_subject.py`,
  Design d1_mechanism, seed 20260808, temperature 0.3, n=30 Einheiten vollständig.
- Daten: `data/lds_c/llm_subject/llm_subject_opencode-go_opencode-go_gpt-5.6-luna_20260910.json`,
  aggregiert in `multi_model_replication_2026091*.json`; Marge +0.222, p=0.0.
- Router: `api_url = https://opencode.ai/zen/go/v1` — der Modell-Alias wird vom opencode-go-Router
  aufgelöst; **kein Hersteller / keine Gewichtsquelle aus der API zuordenbar**.
  Kein öffentlicher Modell-Steckbrief für `gpt-5.6-luna` auffindbar (Stand 2026-09-16).

## Entscheidung (Option B aus ARCHIVE_POLICY: schriftlich undisclosed + Konsequenzen tragen)

- Herkunft bleibt **ungeklärt (Modell-Alias des opencode-go-Routers, kein Hersteller zuordenbar)**.
- Messung ist protokoll-identisch (P1: 3 Sprachen × k=10) und bleibt im Datensatz;
  Sensitivität ohne luna ist berichtet (West 10/10, Marge 0,148 vs. 0,155 mit luna; §8.15 Robustheit (c)).
- Alle bestehenden `Herkunft ungeklärt`-Labels (Paper §8, declaration, README, SSOT-web) sind damit
  korrekt und referenzieren diese Notiz; keine Label-Änderung nötig.
- Folgearbeit: Modell-Matrix mit Hersteller-Attribution ersetzt den Alias, sobald verfügbar.
