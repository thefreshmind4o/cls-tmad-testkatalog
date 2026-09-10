#!/usr/bin/env python3
"""
L2-Generator v1.0
=================

Generiert automatisch plausible L2-Relationen aus gegebenen L1-Positionen.

Verwendung:
    python l2_generator.py --input l1_positionen.json --output l2_vorschlaege.json

Autor: CLS-DB
Datum: 10. September 2026
Status: Arbeits- und Staging-Kandidat
"""

import json
import argparse
from typing import List, Dict, Any
from itertools import combinations


# Typische Relationsmuster nach Modalitaeten
RELATIONSMUSTER = {
    ("brauchen", "wollen"): "Brauchen (Bedarf) vs. Wollen (Wunsch)",
    ("brauchen", "sollen"): "Brauchen (Bedarf) vs. Sollen (Erwartung)",
    ("brauchen", "muessen"): "Brauchen (Bedarf) vs. Muessen (Druck)",
    ("brauchen", "duerfen"): "Brauchen (Bedarf) vs. Duermen (Erlaubnis)",
    ("brauchen", "koennen"): "Brauchen (Bedarf) vs. Koennen (Faelhigkeit)",
    ("wollen", "sollen"): "Wollen (Wunsch) vs. Sollen (Norm)",
    ("wollen", "muessen"): "Wollen (Wunsch) vs. Muessen (Druck)",
    ("wollen", "duerfen"): "Wollen (Wunsch) vs. Duermen (Erlaubnis)",
    ("wollen", "koennen"): "Wollen (Wunsch) vs. Koennen (Faelhigkeit)",
    ("sollen", "muessen"): "Sollen (Norm) vs. Muessen (Druck)",
    ("sollen", "duerfen"): "Sollen (Erwartung) vs. Duermen (Erlaubnis)",
    ("sollen", "koennen"): "Sollen (Erwartung) vs. Koennen (Faelhigkeit)",
    ("muessen", "duerfen"): "Muessen (Druck) vs. Duermen (Erlaubnis)",
    ("muessen", "koennen"): "Muessen (Druck) vs. Koennen (Faelhigkeit)",
    ("duerfen", "koennen"): "Duermen (Erlaubnis) vs. Koennen (Faelhigkeit)",
    # Gleiche Modalitaet
    ("brauchen", "brauchen"): "Brauchen (Bedarf A) vs. Brauchen (Bedarf B)",
    ("wollen", "wollen"): "Wollen (Wunsch A) vs. Wollen (Wunsch B)",
    ("sollen", "sollen"): "Sollen (Norm A) vs. Sollen (Norm B)",
    ("muessen", "muessen"): "Muessen (Druck A) vs. Muessen (Druck B)",
    ("duerfen", "duerfen"): "Duermen (Erlaubnis A) vs. Duermen (Erlaubnis B)",
    ("koennen", "koennen"): "Koennen (Faelhigkeit A) vs. Koennen (Faelhigkeit B)",
}

# Typische Befunde nach Relationsmustern
BEFUNDE = {
    "Brauchen": "spannung",
    "Wollen": "spannung",
    "Sollen": "widerspruch",
    "Muessen": "asymmetrie",
    "Duermen": "asymmetrie",
    "Koennen": "deckung",
}

# Typische Schutzbedarfe nach Runden
SCHUTZBEDARFE = {
    "kindheit": {"stufe": "hoch", "beschreibung": "Hohe Abhaengigkeit, begrenzte Artikulationsmacht."},
    "pubertaet": {"stufe": "erhoeht", "beschreibung": "Abweichung kann soziale Sanktion ausloesen; Duerfen-Fenster pruefen."},
    "adoleszenz": {"stufe": "weiterhin_vorhanden", "beschreibung": "Gegenseitigkeit, Zustimmung, Grenze, Ausstieg."},
}

# Was-Befund-nicht-bedeutet nach Runden
WAS_NICHT = {
    "kindheit": ["keine Ueberforderung durch erwachsene Konfliktlogik", "kein fehlender Bedarf bei Nicht-Artikulation"],
    "pubertaet": ["keine Pathologisierung", "keine Rebellion-Diagnose", "keine Unreife-Zuschreibung"],
    "adoleszenz": ["keine automatische Fairnessbewertung", "keine Intervention ohne Entscheidung"],
}


def l1_positionen_laden(filepath: str) -> List[Dict]:
    """Laedt L1-Positionen aus JSON-Datei."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Falls es ein Testkatalog ist, extrahiere nur L1-Positionen
    if "tmad_testkatalog" in data:
        l1_positionen = []
        for testfall in data["tmad_testkatalog"]:
            if "l1_position" in testfall.get("beispieldaten", {}):
                l1_positionen.append(testfall["beispieldaten"]["l1_position"])
        return l1_positionen
    # Falls es direkt eine Liste von L1-Positionen ist
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Ungueltiges Format: Erwartet Testkatalog oder Liste von L1-Positionen.")


def l2_vorschlag_generieren(l1_a: Dict, l1_b: Dict) -> Dict:
    """Generiert einen L2-Vorschlag aus zwei L1-Positionen."""
    # Pruefe, ob beide L1-Positionen im selben Wir-Feld und derselben Runde sind
    if l1_a.get("wir_feld_typ") != l1_b.get("wir_feld_typ"):
        return None  # Unterschiedliche Wir-Felder -> keine L2-Relation generieren
    
    if l1_a.get("sewkl_runde") != l1_b.get("sewkl_runde"):
        return None  # Unterschiedliche Runden -> keine L2-Relation generieren
    
    # Bestimme Relationstyp
    modalitaet_a = l1_a.get("modalitaet")
    modalitaet_b = l1_b.get("modalitaet")
    
    # Sortiere Modalitaeten fuer konsistenten Key
    modalitaeten_sortiert = tuple(sorted([modalitaet_a, modalitaet_b]))
    relationstyp = RELATIONSMUSTER.get(modalitaeten_sortiert, f"{modalitaet_a} vs. {modalitaet_b}")
    
    # Bestimme Befund
    befund = BEFUNDE.get(relationstyp.split(" ")[0], "spannung")
    
    # Bestimme Schutzbedarf
    runde = l1_a.get("sewkl_runde", "kindheit")
    schutzbedarf = SCHUTZBEDARFE.get(runde, SCHUTZBEDARFE["kindheit"])
    was_nicht = WAS_NICHT.get(runde, WAS_NICHT["kindheit"])
    
    # Generiere L2-Relation
    l2_vorschlag = {
        "id": f"l2_auto_{l1_a['id']}_{l1_b['id']}",
        "relatum_a": {"id": l1_a["id"], "typ": "l1_position"},
        "relatum_b": {"id": l1_b["id"], "typ": "l1_position"},
        "relationstyp": relationstyp,
        "gegenstand": l1_a.get("inhalt", "")[:50] + "..." if l1_a.get("inhalt") else "Unbekannt",
        "wir_feld_ref": l1_a.get("wir_feld_ref", "wir_feld_unbekannt"),
        "wir_feld_typ": l1_a.get("wir_feld_typ", "familie"),
        "zeitfenster": l1_a.get("zeitfenster", {"von": "2026-09-10T00:00:00Z", "bis": None}),
        "befund": befund,
        "schutzbedarf_runde": {"sewkl_runde": runde, "beschreibung": schutzbedarf["beschreibung"]},
        "was_befund_nicht_bedeutet": was_nicht,
        "evidenz_refs": l1_a.get("evidenz_refs", []) + l1_b.get("evidenz_refs", []),
    }
    
    return l2_vorschlag


def alle_l2_vorschlaege_generieren(l1_positionen: List[Dict]) -> List[Dict]:
    """Generiert alle moeglichen L2-Vorschlaege aus einer Liste von L1-Positionen."""
    l2_vorschlaege = []
    
    # Alle Kombinationen von 2 L1-Positionen
    for l1_a, l1_b in combinations(l1_positionen, 2):
        l2 = l2_vorschlag_generieren(l1_a, l1_b)
        if l2:
            l2_vorschlaege.append(l2)
    
    return l2_vorschlaege


def main():
    parser = argparse.ArgumentParser(description="Generiert L2-Relationen aus L1-Positionen.")
    parser.add_argument("--input", required=True, help="Pfad zur JSON-Datei mit L1-Positionen.")
    parser.add_argument("--output", required=True, help="Pfad zur Ausgabe-JSON-Datei.")
    args = parser.parse_args()
    
    print(f"Lade L1-Positionen aus {args.input}...")
    l1_positionen = l1_positionen_laden(args.input)
    print(f"  Gefunden: {len(l1_positionen)} L1-Positionen.")
    
    print(f"Generiere L2-Vorschlaege...")
    l2_vorschlaege = alle_l2_vorschlaege_generieren(l1_positionen)
    print(f"  Generiert: {len(l2_vorschlaege)} L2-Vorschlaege.")
    
    print(f"Speichere L2-Vorschlaege in {args.output}...")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(l2_vorschlaege, f, indent=2, ensure_ascii=False)
    
    print("Fertig!")
    print(f"\nHinweis: Diese Vorschlaege sind automatisch generiert und muessen manuell geprueft werden.")
    print(f"Insbesondere: Gegenstand, Wir-Feld, Zeitfenster, Evidenz und Schutzbedarf.")


if __name__ == "__main__":
    main()
