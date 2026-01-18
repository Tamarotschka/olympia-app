"""
Hauptprogramm für die Olympia-Datenanalyse.

Dieses Programm analysiert die Daten der Olympischen Winterspiele 2022
und beantwortet folgende Fragen:

1. Wie viele Länder nahmen an den Winterspielen teil und wie verteilen 
   sich diese auf die Kontinente?
2. Welche Sportarten dominieren einzelne Länder?

Verwendung:
    python main.py
"""

from data_loader import load_olympics_data, clean_data
from analysis import (
    analyze_countries_by_continent,
    analyze_sports_dominance,
    format_countries_report,
    format_dominance_report
)


def main():
    """
    Hauptfunktion führt alle Analysen aus und gibt die Ergebnisse aus.
    """
    # Pfad zur Datendatei
    data_path = "../assets/Olympics2022.csv"
    
    print("Lade Olympia-Daten...")
    print("-" * 60)
    
    # Daten laden und bereinigen
    df = load_olympics_data(data_path)
    df = clean_data(df)
    
    print(f"Daten geladen: {len(df)} Länder, {len(df.columns)} Spalten")
    print("")
    
    # ===== ANALYSE 1: Länder nach Kontinenten =====
    print("Führe Analyse 1 aus: Länder nach Kontinenten...")
    countries_analysis = analyze_countries_by_continent(df)
    countries_report = format_countries_report(countries_analysis)
    print(countries_report)
    
    # ===== ANALYSE 2: Sportarten-Dominanz =====
    print("Führe Analyse 2 aus: Sportarten-Dominanz...")
    dominance_analysis = analyze_sports_dominance(df)
    dominance_report = format_dominance_report(dominance_analysis)
    print(dominance_report)
    
    print("=" * 60)
    print("Analyse abgeschlossen!")
    print("=" * 60)


if __name__ == "__main__":
    main()
