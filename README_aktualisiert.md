# TMAD-Testkatalog: CLS-Dynamikmodell Gruppen & SEWKL-Runden

[![Status](https://img.shields.io/badge/Status-Arbeits--und%20Staging--Kandidat-orange)]()
[![Datum](https://img.shields.io/badge/Datum-2026--09--10-blue)]()
[![Testfaelle](https://img.shields.io/badge/Testf%C3%A4lle-52-green)]()
[![L1](https://img.shields.io/badge/L1-Positionen-blue)]()
[![L2](https://img.shields.io/badge/L2-Relationen-red)]()
[![L3](https://img.shields.io/badge/L3-Bilanzen-purple)]()

**Validierungsskript:** `tmad_validator.py`  
**Schema:** `cls_dynamikmodell_gruppen_sewkl_schema.json`  
**Testkatalog:** `cls_tmad_testkatalog_gruppen_sewkl_v5.json` (52 Testfaelle)  
**Dokumentation:** `l1_to_l2_ableitungen.md`, `l2_to_l3_ableitungen.md`  
**Skripte:** `l2_generator.py`, `l1_l2_l3_communicator.py`

---

## Uebersicht

Dieses Repository enthaelt den **TMAD-Testkatalog** für das **CLS-Dynamikmodell** mit Fokus auf **Gruppen (Wir-Felder)** und **SEWKL-Runden** (Kindheit, Pubertat, Adoleszenz). Der Katalog operationalisiert die sieben **TMAD-Allgemeinregeln** aus dem PDF `CLS_Dynamikmodell_Gruppen_und_SEWKL_Runden.pdf` (Status: Arbeits- und Staging-Kandidat, 10. September 2026). [file:51]

### Sieben TMAD-Allgemeinregeln

1. Kein L1 ohne Feld- und Zeitbezug.
2. Kein L2 ohne zwei begrenzte Relata und funf Prufdimensionen (Gegenstand, Wir-Feld, Zeit, Modalitaet/Polaritaet, Herkunft/Evidenz).
3. Kein L3 ohne System-/Wir-Bezug, Zeitfenster, Perspektivlage und Evidenzstatus.
4. Keine negative Ableitung aus Schweigen oder Unbekanntheit.
5. Keine Reifegrad- oder Personlichkeitsdiagnose aus L1-L3.
6. Keine automatische Intervention oder moralische Enddiagnose.
7. Keine verdeckte Uberschreibung ohne Revision.

---

## Installation

### Voraussetzungen

- Python 3.8+
- Keine externen Abhaengigkeiten (nur Standardbibliothek)

### Dateien

| Datei | Beschreibung | Groesse |
|---|---|---|
| `cls_tmad_testkatalog_gruppen_sewkl_v5.json` | 52 Testfaelle (34 positiv, 18 negativ, 25 L2, 6 L3) | ~50 KB |
| `cls_tmad_testkatalog_gruppen_sewkl_v6_neue_l3.json` | 2 neue L3-Testfaelle (Institution, Peers) | ~7 KB |
| `cls_dynamikmodell_gruppen_sewkl_schema.json` | JSON-Schema fuer L1/L2/L3 mit Kontextfeldern | ~9 KB |
| `tmad_validator.py` | Validierungsskript (v1.1) | ~7 KB |
| `l2_generator.py` | Automatischer L2-Generator | ~7 KB |
| `l1_l2_l3_communicator.py` | Bidirektionales Kommunikationsmodul | ~14 KB |
| `l1_to_l2_ableitungen.md` | Dokumentation: L1 → L2 Erkenntnistransfer | ~8 KB |
| `l2_to_l3_ableitungen.md` | Dokumentation: L2 → L3 Erkenntnistransfer | ~8 KB |
| `README.md` | Diese Datei | ~8 KB |

---

## Verwendung

### Validator ausfuehren

```bash
python tmad_validator.py
```

**Erwartete Ausgabe (bei bestandener Validierung):**

```
TMAD-Testkatalog Validator v1.1
============================================================
[OK] Schema geladen: cls_dynamikmodell_gruppen_sewkl_schema.json
[OK] Testkatalog geladen: 52 Testfaelle

Validierung 1: Schema-Presence (stichprobenartig, nur positive Testfaelle)
  [BESTANDEN]

Validierung 2: TMAD-Regeln (kombinierte Regeln erlaubt)
  [BESTANDEN]

Validierung 3: Konsistenz
  [BESTANDEN]

============================================================
GESAMTERGEBNIS: [BESTANDEN]
```

### Automatischer L2-Generator

```bash
python l2_generator.py --input l1_positionen.json --output l2_vorschlaege.json
```

Generiert automatisch plausible L2-Relationen aus gegebenen L1-Positionen.

### Bidirektionales Kommunikationsmodul

```bash
python l1_l2_l3_communicator.py \\
  --input cls_tmad_testkatalog_gruppen_sewkl_v5.json \\
  --output l1_l2_l3_vorschlaege.json
```

**Funktionen:**
- **L1 → L2:** Generiert L2-Vorschlaege aus L1-Positionen
- **L2 → L3:** Generiert L3-Vorschlaege aus L2-Relationen
- **L3 → L2:** Zeigt fehlende L2-Referenzen in L3-Bilanzen
- **L2 → L1:** Zeigt fehlende L1-Positionen in L2-Relationen

---

## Testfaelle: Uebersicht

### Alle Testfaelle (1-52)

| Bereich | Testfaelle | Positiv | Negativ | Beschreibung |
|---|---|---|---|---|
| **L1** | 1-22 | 12 | 10 | Modalpositionen (brauchen, wollen, sollen, muessen, duerfen, koennen) |
| **L2** | 23-52 | 22 | 6 | Relationen zwischen Positionen (25 L2-Testfaelle gesamt) |
| **L3** | 10, 26-28, 53-54 | 6 | 2 | Systembilanzen (6 L3-Testfaelle gesamt) |

### L2-Testfaelle nach Modalitaetskombination

| Modalitaet A | Modalitaet B | Testfaelle | Beispiele |
|---|---|---|---|
| `brauchen` | `wollen` | 23, 32, 37 | Familie, Partnerschaft |
| `brauchen` | `muessen` | 42 | Familie |
| `brauchen` | `brauchen` | 37, 44 | Familie, Partnerschaft |
| `wollen` | `sollen` | 09, 23, 36 | Peers, Familie |
| `wollen` | `wollen` | 25, 41, 43 | Partnerschaft, Peers |
| `sollen` | `koennen` | 31 | Arbeit |
| `sollen` | `sollen` | 33, 45 | Familie, Institution |
| `muessen` | `sollen` | 30 | Peers |
| `muessen` | `muessen` | 47 | Familie |
| `koennen` | `koennen` | 34, 48 | Institution, Arbeit |
| `duerfen` | `wollen` | 29 | Familie |
| `duerfen` | `duerfen` | 46 | Arbeit |

### L3-Testfaelle nach System

| System | Testfaelle | Runde | Bilanzfrage |
|---|---|---|---|
| **Familie** | 26 | Kindheit | Wie verteilen sich Schutz, Zeit, Aufmerksamkeit, Regeln, Beteiligung? |
| **Partnerschaft** | 27 | Adoleszenz | Wie verteilen sich Naehe, Abstand, Sorgearbeit, Zeit, Entscheidung? |
| **Arbeit/Organisation** | 10 | Adoleszenz | Wie verteilen sich Arbeit, Risiko, Verantwortung, Ressourcen, Anerkennung? |
| **Institution** | 53 | Pubertaet | Wie verteilen sich Zugang, Gehoer, Beschwerdeweg, Information, Schutz? |
| **Peers** | 54 | Pubertaet | Wie verteilen sich Zugehoerigkeit, Sichtbarkeit, Status, Ausschlussrisiko? |

---

## Bekannte Einschraenkungen

1. **Schema-Presence-Pruefung:** Der Validator prueft nur positive Testfaelle streng. Negative Testfaelle duerfen absichtlich Felder weglassen (das ist der getestete Fehler).

2. **Kombinierte Regeln:** Negative Testfaelle koennen Kombinationen von TMAD-Regeln angeben (z.B. "Kein L1 ...; keine Reifegrad-..."). Der Validator erkennt dies, solange mindestens eine der sieben TMAD-Regeln im Text vorkommt.

3. **Vollstaendigkeit:** Testkatalog v5 enthaelt 52 Testfaelle, v6 ergaenzt 2 weitere L3-Testfaelle (Institution, Peers). Vollstaendige Abdeckung aller 6 Wir-Felder × 3 Runden = 18 Systemkontexte ist in Arbeit.

---

## Naechste Schritte

- [ ] **Testkatalog v6 konsolidieren:** Alle 54 Testfaelle in einer Datei zusammenfuehren.
- [ ] **Automatische L3-Generierung:** Skript entwickeln, das aus gegebenen L2-Relationen automatisch plausible L3-Bilanzen vorschlaegt (in Arbeit via `l1_l2_l3_communicator.py`).
- [ ] **Governance-Pruefung:** Vor produktiver Nutzung Bestandspruefung gegen `cls/id-kanon.json`, `cls/quellenregister.json` und ausdrucksuckliche Freigabe einholen. [file:51]
- [ ] **Vollstaendigkeit pruefen:** Alle 6 Wir-Felder × 3 Runden = 18 Systemkontexte pruefen; fehlende L3-Bilanzen ergaenzen.

---

## Lizenz & Hinweis

**Status:** Arbeits- und Staging-Kandidat  
**Provenienz:** rekonstruiert_aus_sitzungsprotokollen  
**Geltung:** Konzeptioneller Entwurf. Keine kanonische Familien-, Achsen-, Enum- oder Schemawirkung ohne Pruefung des tatsaechlichen CLS-Bestands und ausdrucksucklichen Beschluss. [file:51]

Bei Abweichungen gilt das PDF `CLS_Dynamikmodell_Gruppen_und_SEWKL_Runden.pdf` und der tatsaechliche CLS-Bestand. [file:51]

---

**Autor:** CLS-DB  
**Datum:** 10. September 2026  
**Kontakt:** [GitHub Issues](https://github.com/thefreshmind4o/cls-tmad-testkatalog/issues)
