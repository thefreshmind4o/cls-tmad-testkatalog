#!/usr/bin/env python3
"""
L1-L2-L3 Communicator v1.0
==========================

Bidirektionales Kommunikationsmodul für CLS-Dynamikmodell.

- L1 → L2: Aktualisierte L1-Positionen generieren neue L2-Relationen
- L2 → L3: Aktualisierte L2-Relationen generieren neue L3-Bilanzen
- L3 → L2: Neue L3-Bilanzen zeigen fehlende L2-Relationen auf
- L2 → L1: Neue L2-Relationen zeigen fehlende L1-Positionen auf

Verwendung:
    python l1_l2_l3_communicator.py --input cls_tmad_testkatalog_gruppen_sewkl_v5.json --output l1_l2_l3_vorschlaege.json

Autor: CLS-DB
Datum: 10. September 2026
Status: Arbeits- und Staging-Kandidat
"""

import json
import argparse
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
from itertools import combinations


def testkatalog_laden(filepath: str) -> Dict:
    """Laedt gesamten Testkatalog mit L1, L2, L3."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def extrahiere_l1_l2_l3(testkatalog: Dict) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Extrahiert L1, L2, L3 aus Testkatalog."""
    l1_positionen = []
    l2_relationen = []
    l3_bilanzen = []
    
    for testfall in testkatalog.get("tmad_testkatalog", []):
        beispieldaten = testfall.get("beispieldaten", {})
        
        if "l1_position" in beispieldaten:
            l1_positionen.append(beispieldaten["l1_position"])
        if "l2_relation" in beispieldaten:
            l2_relationen.append(beispieldaten["l2_relation"])
        if "l3_bilanz" in beispieldaten:
            l3_bilanzen.append(beispieldaten["l3_bilanz"])
    
    return l1_positionen, l2_relationen, l3_bilanzen


def l1_to_l2_vorschlaege(l1_positionen: List[Dict], bestehende_l2: List[Dict]) -> List[Dict]:
    """Generiert L2-Vorschlaege aus L1-Positionen, die noch nicht existieren."""
    # Bestehende L2-Relationen als Set von (relatum_a_id, relatum_b_id)
    bestehende_l2_pairs = set()
    for l2 in bestehende_l2:
        if l2.get("relatum_a") and l2.get("relatum_b"):
            pair = tuple(sorted([l2["relatum_a"]["id"], l2["relatum_b"]["id"]]))
            bestehende_l2_pairs.add(pair)
    
    # Typische Relationsmuster
    RELATIONSMUSTER = {
        ("brauchen", "wollen"): "Brauchen (Bedarf) vs. Wollen (Wunsch)",
        ("brauchen", "sollen"): "Brauchen (Bedarf) vs. Sollen (Erwartung)",
        ("brauchen", "muessen"): "Brauchen (Bedarf) vs. Muessen (Druck)",
        ("wollen", "sollen"): "Wollen (Wunsch) vs. Sollen (Norm)",
        ("wollen", "muessen"): "Wollen (Wunsch) vs. Muessen (Druck)",
        ("sollen", "muessen"): "Sollen (Norm) vs. Muessen (Druck)",
        ("sollen", "koennen"): "Sollen (Erwartung) vs. Koennen (Faelhigkeit)",
        ("muessen", "koennen"): "Muessen (Druck) vs. Koennen (Faelhigkeit)",
        ("duerfen", "koennen"): "Duermen (Erlaubnis) vs. Koennen (Faelhigkeit)",
        ("brauchen", "brauchen"): "Brauchen (Bedarf A) vs. Brauchen (Bedarf B)",
        ("wollen", "wollen"): "Wollen (Wunsch A) vs. Wollen (Wunsch B)",
        ("sollen", "sollen"): "Sollen (Norm A) vs. Sollen (Norm B)",
        ("muessen", "muessen"): "Muessen (Druck A) vs. Muessen (Druck B)",
        ("duerfen", "duerfen"): "Duermen (Erlaubnis A) vs. Duermen (Erlaubnis B)",
        ("koennen", "koennen"): "Koennen (Faelhigkeit A) vs. Koennen (Faelhigkeit B)",
    }
    
    vorschlaege = []
    
    # Alle Kombinationen von 2 L1-Positionen
    for l1_a, l1_b in combinations(l1_positionen, 2):
        # Nur im selben Wir-Feld und derselben Runde
        if l1_a.get("wir_feld_typ") != l1_b.get("wir_feld_typ"):
            continue
        if l1_a.get("sewkl_runde") != l1_b.get("sewkl_runde"):
            continue
        
        # Pruefe, ob L2 bereits existiert
        pair = tuple(sorted([l1_a["id"], l1_b["id"]]))
        if pair in bestehende_l2_pairs:
            continue  # L2 existiert bereits
        
        # Generiere L2-Vorschlag
        modalitaet_a = l1_a.get("modalitaet")
        modalitaet_b = l1_b.get("modalitaet")
        modalitaeten_sortiert = tuple(sorted([modalitaet_a, modalitaet_b]))
        relationstyp = RELATIONSMUSTER.get(modalitaeten_sortiert, f"{modalitaet_a} vs. {modalitaet_b}")
        
        runde = l1_a.get("sewkl_runde", "kindheit")
        schutzbedarfe = {
            "kindheit": "Hohe Abhaengigkeit, begrenzte Artikulationsmacht.",
            "pubertaet": "Abweichung kann soziale Sanktion ausloesen.",
            "adoleszenz": "Gegenseitigkeit, Zustimmung, Grenze, Ausstieg.",
        }
        
        l2_vorschlag = {
            "id": f"l2_auto_{l1_a['id']}_{l1_b['id']}",
            "relatum_a": {"id": l1_a["id"], "typ": "l1_position"},
            "relatum_b": {"id": l1_b["id"], "typ": "l1_position"},
            "relationstyp": relationstyp,
            "gegenstand": l1_a.get("inhalt", "")[:50] + "..." if l1_a.get("inhalt") else "Unbekannt",
            "wir_feld_ref": l1_a.get("wir_feld_ref", "wir_feld_unbekannt"),
            "wir_feld_typ": l1_a.get("wir_feld_typ", "familie"),
            "zeitfenster": l1_a.get("zeitfenster", {"von": "2026-09-10T00:00:00Z", "bis": None}),
            "befund": "spannung",
            "schutzbedarf_runde": {"sewkl_runde": runde, "beschreibung": schutzbedarfe.get(runde, schutzbedarfe["kindheit"])},
            "was_befund_nicht_bedeutet": ["keine automatische Interpretation", "manuelle Pruefung erforderlich"],
            "evidenz_refs": l1_a.get("evidenz_refs", []) + l1_b.get("evidenz_refs", []),
            "l1_to_l2_transfer": f"Aus {l1_a['id']} und {l1_b['id']} abgeleitet.",
        }
        
        vorschlaege.append(l2_vorschlag)
    
    return vorschlaege


def l2_to_l3_vorschlaege(l2_relationen: List[Dict], bestehende_l3: List[Dict]) -> List[Dict]:
    """Generiert L3-Vorschlaege aus L2-Relationen, die noch nicht existieren."""
    # Gruppiere L2 nach System (wir_feld_typ + sewkl_runde)
    l2_nach_system = defaultdict(list)
    for l2 in l2_relationen:
        system_key = (l2.get("wir_feld_typ"), l2.get("schutzbedarf_runde", {}).get("sewkl_runde"))
        l2_nach_system[system_key].append(l2)
    
    vorschlaege = []
    
    # Fuer jedes System mit >= 2 L2-Relationen
    for (wir_feld_typ, runde), l2_liste in l2_nach_system.items():
        if len(l2_liste) < 2:
            continue  # Mindestens 2 L2-Relationen fuer L3 noetig
        
        # Pruefe, ob L3 bereits existiert
        bestehende_l3_systeme = set()
        for l3 in bestehende_l3:
            system_key = (l3.get("wir_feld_typ"), l3.get("sewkl_runde"))
            bestehende_l3_systeme.add(system_key)
        
        if (wir_feld_typ, runde) in bestehende_l3_systeme:
            continue  # L3 existiert bereits
        
        # Generiere L3-Vorschlag
        system_typ_map = {
            "familie": "familie",
            "partnerschaft": "paar",
            "freundschaft_peers": "gruppe",
            "arbeit_organisation": "organisation",
            "institution": "institution",
            "gesellschaft_oeffentlichkeit": "gesellschaft",
        }
        
        bilanzfragen = {
            "familie": "Wie verteilen sich Schutz, Zeit, Aufmerksamkeit, Regeln und Beteiligung?",
            "partnerschaft": "Wie verteilen sich Naehe, Abstand, Sorgearbeit, Zeit, Entscheidung, Grenze und Ausstiegsmacht?",
            "freundschaft_peers": "Wie verteilen sich Zugehoerigkeit, Sichtbarkeit, Status, Ausschlussrisiko?",
            "arbeit_organisation": "Wie verteilen sich Arbeit, Risiko, Verantwortung, Ressourcen, Anerkennung und Entscheidungsmacht?",
            "institution": "Wie verteilen sich Zugang, Gehoer, Beschwerdeweg, Information und Schutz?",
            "gesellschaft_oeffentlichkeit": "Wie verteilen sich Sichtbarkeit, Zugang, strukturelle Verteilung, Definitionsmacht?",
        }
        
        # Sammle alle beteiligten L1-Positionen aus L2
        beteiligte_l1 = set()
        for l2 in l2_liste:
            if l2.get("relatum_a"):
                beteiligte_l1.add(l2["relatum_a"]["id"])
            if l2.get("relatum_b"):
                beteiligte_l1.add(l2["relatum_b"]["id"])
        
        l3_vorschlag = {
            "id": f"l3_auto_{wir_feld_typ}_{runde}",
            "system_ref": f"system_{wir_feld_typ}_{runde}",
            "system_typ": system_typ_map.get(wir_feld_typ, wir_feld_typ),
            "teilnehmer_refs": [{"id": l1_id, "typ": "person"} for l1_id in beteiligte_l1],
            "betroffenen_refs": [],
            "nicht_vertretene_perspektiven": [],
            "berechtigte_l1_refs": [{"id": l1_id, "typ": "l1_position"} for l1_id in beteiligte_l1],
            "berechtigte_l2_refs": [{"id": l2["id"], "typ": "l2_relation"} for l2 in l2_liste],
            "bilanzfrage": bilanzfragen.get(wir_feld_typ, "Wie verteilen sich Ressourcen und Entscheidungsmacht?"),
            "wir_feld_ref": f"wir_feld_{wir_feld_typ}_{runde}",
            "wir_feld_typ": wir_feld_typ,
            "sewkl_runde": runde,
            "zeitfenster": {"von": "2026-09-10T00:00:00Z", "bis": None},
            "perspektivlage": "Bilanz erstellt auf Basis von L2-Relationen; manuelle Pruefung erforderlich.",
            "vtl_felder": [
                {"feld": "Positives", "pruefstatus": "offen", "beschreibung": "Manuell zu pruefen."},
                {"feld": "Negatives", "pruefstatus": "offen", "beschreibung": "Manuell zu pruefen."},
                {"feld": "Willensgeltung", "pruefstatus": "offen", "beschreibung": "Manuell zu pruefen."},
            ],
            "bilanztyp": ["offen"],
            "geltungs_und_unsicherheitsgrenzen": ["Automatisch generiert; manuelle Pruefung erforderlich."],
            "zweck_zugriff_weitergabe": {"zweck": "Automatische Vorschlagsgenerierung.", "zugriff": ["system"], "weitergabe": []},
            "schutzgrenze": "Keine automatische Fairnessbewertung; keine Intervention ohne Entscheidung.",
            "l2_to_l3_transfer": f"Aus {len(l2_liste)} L2-Relationen abgeleitet.",
        }
        
        vorschlaege.append(l3_vorschlag)
    
    return vorschlaege


def l3_to_l2_luecken(l3_bilanzen: List[Dict], bestehende_l2: List[Dict]) -> List[str]:
    """Zeigt fehlende L2-Relationen basierend auf L3-Bilanzen."""
    fehlende = []
    
    for l3 in l3_bilanzen:
        berechtigte_l2 = l3.get("berechtigte_l2_refs", [])
        if len(berechtigte_l2) < 2:
            fehlende.append(f"L3 {l3['id']}: Weniger als 2 L2-Referenzen vorhanden.")
            continue
        
        # Pruefe, ob alle L2-Referenzen in bestehenden L2 existieren
        bestehende_l2_ids = {l2["id"] for l2 in bestehende_l2}
        for l2_ref in berechtigte_l2:
            if l2_ref["id"] not in bestehende_l2_ids:
                fehlende.append(f"L3 {l3['id']}: L2 {l2_ref['id']} fehlt.")
    
    return fehlende


def l2_to_l1_luecken(l2_relationen: List[Dict], bestehende_l1: List[Dict]) -> List[str]:
    """Zeigt fehlende L1-Positionen basierend auf L2-Relationen."""
    fehlende = []
    
    for l2 in l2_relationen:
        relatum_a = l2.get("relatum_a")
        relatum_b = l2.get("relatum_b")
        
        if not relatum_a or not relatum_b:
            fehlende.append(f"L2 {l2['id']}: Nur ein Relatum vorhanden.")
            continue
        
        # Pruefe, ob beide L1-Referenzen in bestehenden L1 existieren
        bestehende_l1_ids = {l1["id"] for l1 in bestehende_l1}
        if relatum_a["id"] not in bestehende_l1_ids:
            fehlende.append(f"L2 {l2['id']}: L1 {relatum_a['id']} fehlt.")
        if relatum_b["id"] not in bestehende_l1_ids:
            fehlende.append(f"L2 {l2['id']}: L1 {relatum_b['id']} fehlt.")
    
    return fehlende


def main():
    parser = argparse.ArgumentParser(description="Bidirektionales L1-L2-L3 Kommunikationsmodul.")
    parser.add_argument("--input", required=True, help="Pfad zum Testkatalog-JSON.")
    parser.add_argument("--output", required=True, help="Pfad zur Ausgabe-JSON.")
    args = parser.parse_args()
    
    print(f"Lade Testkatalog aus {args.input}...")
    testkatalog = testkatalog_laden(args.input)
    l1_positionen, l2_relationen, l3_bilanzen = extrahiere_l1_l2_l3(testkatalog)
    
    print(f"  L1-Positionen: {len(l1_positionen)}")
    print(f"  L2-Relationen: {len(l2_relationen)}")
    print(f"  L3-Bilanzen: {len(l3_bilanzen)}")
    print()
    
    # L1 → L2
    print("Generiere L1 → L2 Vorschlaege...")
    l2_vorschlaege = l1_to_l2_vorschlaege(l1_positionen, l2_relationen)
    print(f"  Generiert: {len(l2_vorschlaege)} L2-Vorschlaege.")
    
    # L2 → L3
    print("Generiere L2 → L3 Vorschlaege...")
    l3_vorschlaege = l2_to_l3_vorschlaege(l2_relationen, l3_bilanzen)
    print(f"  Generiert: {len(l3_vorschlaege)} L3-Vorschlaege.")
    
    # L3 → L2 (Luecken)
    print("Pruefe L3 → L2 Luecken...")
    l3_to_l2_fehlende = l3_to_l2_luecken(l3_bilanzen, l2_relationen)
    print(f"  Gefunden: {len(l3_to_l2_fehlende)} fehlende L2-Referenzen.")
    
    # L2 → L1 (Luecken)
    print("Pruefe L2 → L1 Luecken...")
    l2_to_l1_fehlende = l2_to_l1_luecken(l2_relationen, l1_positionen)
    print(f"  Gefunden: {len(l2_to_l1_fehlende)} fehlende L1-Referenzen.")
    
    # Ausgabe
    ausgabe = {
        "l1_to_l2_vorschlaege": l2_vorschlaege,
        "l2_to_l3_vorschlaege": l3_vorschlaege,
        "l3_to_l2_fehlende": l3_to_l2_fehlende,
        "l2_to_l1_fehlende": l2_to_l1_fehlende,
        "zusammenfassung": {
            "l1_positionen": len(l1_positionen),
            "l2_relationen": len(l2_relationen),
            "l3_bilanzen": len(l3_bilanzen),
            "l2_vorschlaege": len(l2_vorschlaege),
            "l3_vorschlaege": len(l3_vorschlaege),
            "l3_to_l2_fehlende": len(l3_to_l2_fehlende),
            "l2_to_l1_fehlende": len(l2_to_l1_fehlende),
        }
    }
    
    print(f"\nSpeichere Ergebnisse in {args.output}...")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(ausgabe, f, indent=2, ensure_ascii=False)
    
    print("Fertig!")
    print(f"\nHinweis: Diese Vorschlaege sind automatisch generiert und muessen manuell geprueft werden.")


if __name__ == "__main__":
    main()
