# LinguaGraph — Data Protection & Privacy Documentation

> DSGVO/GDPR-compliant documents for the LinguaGraph human subjects study
> Part of the BWKI 2026 Ethics Package

---

## Document 4: GDPR Data Protection Notice

### Datenschutzerklärung (DE)

**Verantwortliche Stelle**:
Projektleitung LinguaGraph
Erreichbar über den Schulbetreuer des Projekts

**Zweck der Datenverarbeitung**:
Wissenschaftliche Untersuchung zum Einfluss von Sprache auf kognitive Strukturen im Rahmen des Bundeswettbewerbs Künstliche Intelligenz 2026.

**Art der verarbeiteten Daten**:
- Anonymisierte Textantworten auf offene Fragen (Themen: Freiheit, Gerechtigkeit, Erfolg, Verantwortung, Heimat)
- Keine personenbezogenen Daten (kein Name, keine Adresse, keine IP-Adresse, kein Geburtsdatum)

**Rechtsgrundlage**:
Art. 6 Abs. 1 lit. a DSGVO (Einwilligung)

**Speicherdauer**:
Die Daten werden maximal 12 Monate nach Abschluss des Projekts gespeichert und dann endgültig gelöscht.

**Ihre Rechte**:
- Art. 15 DSGVO: Auskunftsrecht
- Art. 16 DSGVO: Recht auf Berichtigung
- Art. 17 DSGVO: Recht auf Löschung ("Recht auf Vergessenwerden")
- Art. 7 Abs. 3 DSGVO: Recht auf Widerruf der Einwilligung
- Art. 77 DSGVO: Beschwerderecht bei einer Aufsichtsbehörde

**Zuständige Aufsichtsbehörde**:
Der Landesbeauftragte für den Datenschutz (LfDI) des jeweiligen Bundeslandes.

---

### Data Protection Notice (EN)

**Data Controller**:
LinguaGraph Project Lead
Reachable via the school project supervisor

**Purpose of Processing**:
Scientific investigation of language effects on cognitive structures, conducted as part of the Bundeswettbewerb Künstliche Intelligenz 2026.

**Categories of Data**:
- Anonymized text responses to open-ended questions (topics: freedom, justice, success, responsibility, home)
- No personal data (no name, address, IP address, or date of birth)

**Legal Basis**:
GDPR Art. 6(1)(a) — Consent

**Retention Period**:
Data is retained for a maximum of 12 months after project completion, then permanently deleted.

**Your Rights**:
- Art. 15 GDPR: Right of access
- Art. 16 GDPR: Right to rectification
- Art. 17 GDPR: Right to erasure
- Art. 7(3) GDPR: Right to withdraw consent
- Art. 77 GDPR: Right to lodge a complaint

---

## Document 5: Data Deletion Request Template

### Antrag auf Löschung meiner Daten (DE)

```
Betreff: Antrag auf Datenlöschung — LinguaGraph Studie

An:
Projektleitung LinguaGraph (über den Schulbetreuer)

Sehr geehrte Damen und Herren,

hiermit beantrage ich die Löschung meiner im Rahmen der LinguaGraph-Studie
erhobenen Daten gemäß Art. 17 DSGVO.

Meine Teilnehmer-ID: ________________

Ich bin darüber informiert, dass nach der Löschung keine Wiederherstellung
meiner Daten möglich ist.

Datum: ________________
Unterschrift: ________________
```

### Data Deletion Request (EN)

```
Subject: Data Deletion Request — LinguaGraph Study

To:
LinguaGraph Project Lead (via school project supervisor)

Dear Sir or Madam,

I hereby request the deletion of my data collected as part of the
LinguaGraph study, in accordance with GDPR Art. 17.

My Participant ID: ________________

I understand that after deletion, my data cannot be recovered.

Date: ________________
Signature: ________________
```

---

## Document 6: Data Retention & Deletion Policy

### Policy Statement

**LinguaGraph Data Management Policy**

1. **Data Collection**: All participant responses are collected via Google Forms (or equivalent) and stored in a local SQLite database (`linguaGraph.db`). No data is stored on commercial cloud services.

2. **Anonymization**: Upon collection, each participant is assigned a random ID (e.g., `S001`). The mapping between real names and IDs is stored separately in a password-protected file. This mapping is deleted upon project completion.

3. **Retention Schedule**:

| Data Type | Retention Period | Deletion Method |
|-----------|-----------------|-----------------|
| Anonymized responses | 12 months post-project | Permanent DB deletion |
| Name-ID mapping | Until project completion | Secure file shredding |
| Consent forms (paper) | 12 months post-project | Physical shredding |
| Consent forms (digital) | 12 months post-project | Permanent deletion |
| Analysis results | Indefinite (aggregated, no PII) | Not applicable |

4. **Deletion Procedure**: When a deletion request is received:
   - Locate participant by ID in the mapping file
   - Delete all responses by that ID from linguaGraph.db
   - Confirm deletion to participant within 30 days (GDPR Art. 12(3))

5. **Data Breach Procedure**: In case of data breach, affected participants will be notified within 72 hours (GDPR Art. 33, 34).

---

## Document 7: Minor Participation Statement

### Einwilligung der Erziehungsberechtigten (DE)

**Für Teilnehmer unter 16 Jahren**:

Gemäß Art. 8 DSGVO und § 4 DDG ist für die Verarbeitung personenbezogener Daten von Kindern unter 16 Jahren die Einwilligung der Erziehungsberechtigten erforderlich.

**Einwilligungserklärung**:

Ich, ________________ (Name des/der Erziehungsberechtigten),

erkläre hiermit, dass ich über die LinguaGraph-Studie informiert wurde und
der Teilnahme meines Kindes ________________ (Name des Kindes)

an dieser Studie zustimme.

Mir ist bekannt, dass:
- Die Teilnahme freiwillig ist und jederzeit beendet werden kann
- Die Daten meines Kindes anonymisiert werden
- Ich die Löschung der Daten jederzeit verlangen kann
- Bei Fragen steht die Projektleitung (über den Schulbetreuer) zur Verfügung

Datum: ________________
Unterschrift des/der Erziehungsberechtigten: ________________

---

### Parental/Guardian Consent (EN)

**For participants under 16**:

In accordance with GDPR Art. 8, parental/guardian consent is required for the processing of personal data of children under 16.

**Consent Statement**:

I, ________________ (Parent/Guardian Name),

hereby confirm that I have been informed about the LinguaGraph study and
consent to the participation of my child ________________ (Child's Name).

I understand that:
- Participation is voluntary and can be terminated at any time
- My child's data will be anonymized
- I can request deletion of data at any time
- The research team (via school project supervisor) is available for questions

Date: ________________
Signature of Parent/Guardian: ________________
