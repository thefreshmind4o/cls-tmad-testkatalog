# L2 → L3 Ableitungen: Systematischer Erkenntnistransfer

**Dokument:** CLS_Dynamikmodell_Gruppen_und_SEWKL_Runden.pdf  
**Status:** Arbeits- und Staging-Kandidat  
**Datum:** 10. September 2026  
**Testkatalog-Version:** v5 (52 Testfaelle: 34 positiv, 18 negativ, 25 L2-Testfaelle, 4 L3-Testfaelle)

---

## Uebersicht

Dieses Dokument beschreibt den systematischen **Erkenntnistransfer von L2 (Relationen) zu L3 (Systembilanzen)** im CLS-Dynamikmodell. Wenn L2 aktualisiert wird (neue oder praesentere Relationen), ergeben sich daraus automatisch neue Erkenntnisse fuer L3 (Verteilungsbilanzen in Systemen). [file:51]

### Grundregel L3

L3 gehort dem Paar, der Gruppe oder dem klar begrenzten Wir – nicht einer Einzelperson. L3 addiert nicht Menschen und berechnet keine Personenwerte. Es macht Verteilungen sichtbar. [file:51]

L3 benoetigt:
- **System-Bezug** (Paar, Gruppe, Organisation)
- **Teilnehmer-Refs** (wer ist beteiligt?)
- **Betroffenen-Refs** (wer ist betroffen, aber nicht direkt teilnehmend?)
- **Berechtigte L1/L2-Refs** (welche Positionen/Relationen fliessen ein?)
- **VTL-Felder** (Bedarfsdeckung, Pflichtverteilung, Definitionsmacht, Folgekosten, Revisionsmacht, etc.)
- **Bilanztyp** (symmetrische/asymmetrische Ungedecktheit, gedeckte Verteilung, Kontrastfeld, Verteilungskollaps, Mehrfachlage)
- **Perspektivlage** (wer bilanziert aus welcher Position?)
- **Geltungs- und Unsicherheitsgrenzen**
- **Schutzgrenze** (was darf die Bilanz nicht?)

---

## Ableitungsregeln

### Regel 1: Mehrere L2-Relationen → Eine L3-Bilanz

Aus mehreren L2-Relationen (mit vollstaendigen Feldern) kann eine L3-Bilanz abgeleitet werden, wenn:

- Alle L2-Relationen dasselbe **System** betreffen (z.B. Familie, Paar, Team).
- Alle L2-Relationen im selben **Wir-Feld** und vergleichbarem **Zeitfenster** gelten.
- Die L2-Befunde zusammen eine **Verteilungsfrage** ergeben (z.B. "Wie verteilen sich Naehe, Abstand, Sorgearbeit?").

**Beispiel:**

- L2-25 (`wollen` vs. `wollen`, Partnerschaft): "Naehe vs. Abstand" → Befund: `spannung`
- L2-32 (`brauchen` vs. `wollen`, Partnerschaft): "Bedarf vs. Wunsch" → Befund: `spannung`
- L2-44 (`brauchen` vs. `brauchen`, Partnerschaft): "Naehe vs. Abstand" → Befund: `spannung`
- → L3-27 (Partnerschaftsverteilung): Bilanzfrage: "Wie verteilen sich Naehe, Abstand, Sorgearbeit, Zeit, Entscheidung?" [file:51]

### Regel 2: L2-Befunde → L3-VTL-Felder

Die **Befunde** aus L2-Relationen (`spannung`, `asymmetrie`, `widerspruch`, `kontrastfeld`, `blockade`, `deckung`) werden in L3 als **VTL-Pruefstatus** uebernommen und konkreten Verteilungsfeldern zugeordnet.

**Beispiel:**

- L2-25: Befund `spannung` (Naehe vs. Abstand) → L3: VTL-Feld "Willensgeltung", Pruefstatus: `asymmetrie`
- L2-32: Befund `spannung` (Bedarf vs. Wunsch) → L3: VTL-Feld "Positives/Negatives", Pruefstatus: `ungedeckt`
- L2-44: Befund `spannung` (Naehe vs. Abstand) → L3: VTL-Feld "Folgekosten", Pruefstatus: `asymmetrie` [file:51]

### Regel 3: L2-Schutzbedarf → L3-Schutzgrenze

Der **Schutzbedarf** aus L2-Relationen (z.B. "erhoeht" in Pubertaet, "hoch" in Kindheit) wird in L3 als **Schutzgrenze** uebernommen und kontextualisiert.

**Beispiel:**

- L2-24 (Familie, Kindheit): Schutzbedarf: "hoch" → L3-26: Schutzgrenze: "Keine formale Systembilanz als Ersatz fuer Schutzpflicht, Fuersorge oder kindgerechte Vertretung."
- L2-25 (Partnerschaft, Adoleszenz): Schutzbedarf: "weiterhin_vorhanden" → L3-27: Schutzgrenze: "Keine automatische Fairnessbewertung; keine Intervention ohne Entscheidung und Duerfen-Pruefung." [file:51]

### Regel 4: L2-Evidenz → L3-Perspektivlage

Die **Evidenz-Refs** aus L2-Relationen (Selbstartikulation, Beobachtung) werden in L3 als **Perspektivlage** uebernommen und explizit gemacht.

**Beispiel:**

- L2-24: Evidenz: "beobachtung_erzieherin" → L3-26: Perspektivlage: "Bilanz erstellt durch externe Beratungsstelle auf Basis von Interviews."
- L2-25: Evidenz: "selbstartikulation_partner_A" → L3-27: Perspektivlage: "Bilanz erstellt im Rahmen von Paarberatung; beide Partner einverstanden." [file:51]

---

## Ableitungstabelle: L2-Testfaelle → L3-Testfaelle

| L3-Testfall | Abgeleitet aus L2-Testfaellen | Bilanzfrage | System | Runde | Bilanztyp |
|---|---|---|---|---|---|
| L3-26 | L2-24 (`brauchen` vs. `fuersorge`) + L2-37 (`brauchen` vs. `brauchen`) | Wie verteilen sich Schutz, Zeit, Aufmerksamkeit, Regeln und Beteiligung? | Familie | Kindheit | `asymmetrische_ungedecktheit` |
| L3-27 | L2-25 (`wollen` vs. `wollen`) + L2-32 (`brauchen` vs. `wollen`) + L2-44 (`brauchen` vs. `brauchen`) | Wie verteilen sich Naehe, Abstand, Sorgearbeit, Zeit, Entscheidung, Grenze und Ausstiegsmacht? | Partnerschaft | Adoleszenz | `asymmetrische_ungedecktheit` |
| L3-10 | L2-09 (`wollen` vs. `sollen`) + L2-31 (`sollen` vs. `koennen`) + L2-38 (`sollen` vs. `duerfen`) | Wie verteilen sich Arbeit, Risiko, Verantwortung, Ressourcen, Anerkennung und Entscheidungsmacht? | Arbeit/Organisation | Adoleszenz | `asymmetrische_ungedecktheit` |

---

## Negative L3-Testfaelle: Fehlende L3-Anforderungen

| L3-Testfall | Fehlerbeschreibung | Verletzte Regel |
|---|---|---|
| L3-05 | L3-Bilanz wird einer Einzelperson zugeschrieben. | Kein L3 ohne System-/Wir-Bezug, Zeitfenster, Perspektivlage und Evidenzstatus. [file:51] |
| L3-06 | L3-Bilanz ohne Perspektivlage und Geltungsgrenzen. | Kein L3 ohne System-/Wir-Bezug, Zeitfenster, Perspektivlage und Evidenzstatus. [file:51] |
| L3-28 | L3-Bilanz ohne berechtigte L1/L2-Referenzen. | Kein L3 ohne System-/Wir-Bezug, Zeitfenster, Perspektivlage und Evidenzstatus. [file:51] |

---

## Typische L3-Bilanzkonstellationen nach Systemen

| System | Typische Bilanzfrage | VTL-Felder | Bilanztyp | Beispiel aus Testkatalog |
|---|---|---|---|---|
| Familie | Wie verteilen sich Schutz, Zeit, Aufmerksamkeit, Regeln, Beteiligung? | Bedarfsdeckung, Definitionsmacht, Revisionsmacht | `asymmetrische_ungedecktheit` | L3-26 |
| Partnerschaft | Wie verteilen sich Naehe, Abstand, Sorgearbeit, Zeit, Entscheidung? | Positives, Negatives, Willensgeltung, Folgekosten | `asymmetrische_ungedecktheit` | L3-27 |
| Arbeit/Organisation | Wie verteilen sich Arbeit, Risiko, Verantwortung, Ressourcen, Anerkennung, Entscheidung? | Pflichtverteilung, Definitionsmacht, Revisionsmacht | `asymmetrische_ungedecktheit` | L3-10 |
| Institution | Wie verteilen sich Zugang, Gehoer, Beschwerdeweg, Information, Schutz? | Erlaubnisverteilung, Faehigkeitszugang, Revisionsmacht | `asymmetrische_ungedecktheit` | (neu zu ergaenzen) |
| Peers | Wie verteilen sich Zugehoerigkeit, Sichtbarkeit, Status, Ausschlussrisiko? | Positives, Negatives, Willensgeltung, Definitionsmacht | `asymmetrische_ungedecktheit` | (neu zu ergaenzen) |

---

## Nachste Schritte

1. **L3-Testfaelle ergaenzen:** Weitere L3-Bilanzen fuer Institution, Peers, Gesellschaft/Oeffentlichkeit.
2. **Automatische L3-Generierung:** Skript entwickeln, das aus gegebenen L2-Relationen automatisch plausible L3-Bilanzen vorschlaegt (mit manueller Pruefung).
3. **Vollstaendigkeit pruefen:** Alle 6 Wir-Felder × 3 Runden = 18 Systemkontexte pruefen; fehlende L3-Bilanzen ergaenzen.

---

**Hinweis:** Diese Dokumentation ist ein Arbeits- und Staging-Kandidat. Alle Aussagen sind ohne Gewahr; bei Abweichungen gilt das PDF `CLS_Dynamikmodell_Gruppen_und_SEWKL_Runden.pdf` und der tatsaechliche CLS-Bestand. [file:51]

---

**Autor:** CLS-DB  
**Datum:** 10. September 2026  
**GitHub:** https://github.com/thefreshmind4o/cls-tmad-testkatalog
