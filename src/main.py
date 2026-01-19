from data_loader import load_olympics_data, clean_data
from analysis_countries import analyze_countries_by_medals, format_countries_report
from analysis_sports import analyze_sports_dominance, format_dominance_report
from analysis_gender import analyze_gender_ratio, format_gender_report
from analysis_correlation import analyze_athletes_medals_correlation, format_correlation_report
from analysis_gender_medals import analyze_gender_medals_correlation, format_gender_medals_report
from analysis_gold import analyze_gold_correlation, format_gold_report
from analysis_sports_variety import analyze_sports_variety, format_sports_variety_report
from analysis_sports_distribution import analyze_sports_distribution, format_sports_distribution_report


def main():
    """
    Hauptfunktion führt alle Analysen aus und gibt die Ergebnisse aus.
    """
    data_path = "../assets/Olympics2022.csv"
    
    print("Lade Olympia-Daten...")
    print("-" * 60)
    
    # Daten laden und bereinigen
    df = load_olympics_data(data_path)
    df = clean_data(df)
    
    print(f"Daten geladen: {len(df)} Länder, {len(df.columns)} Spalten")
    print("")
    
    # ===== ANALYSE 1: Medaillen-Ranking nach Ländern =====
    print("Führe Analyse 1 aus: Welche Länder haben die meisten Gold-/Silber-/Bronzemedaillen...")
    countries_analysis = analyze_countries_by_medals(df)
    countries_report = format_countries_report(countries_analysis)
    print(countries_report)
    
    # ===== ANALYSE 2: Sportarten-Dominanz =====
    print("Führe Analyse 2 aus: Welche Sportarten dominieren einzelne Länder")
    dominance_analysis = analyze_sports_dominance(df)
    dominance_report = format_dominance_report(dominance_analysis)
    print(dominance_report)
    
    # ===== ANALYSE 3: Geschlechterverhältnis =====
    print("Führe Analyse 3 aus: Wie ist das Verhältnis von Männern zu Frauen pro Land?...")
    gender_analysis = analyze_gender_ratio(df)
    gender_report = format_gender_report(gender_analysis)
    print(gender_report)
    
    # ===== ANALYSE 4: Korrelation Athleten/Medaillen =====
    print("Führe Analyse 4 aus: Gibt es einen Zusammenhang zwischen der Anzahl der Athlet:innen und der Anzahl der gewonnenen Medaillen...")
    correlation_analysis = analyze_athletes_medals_correlation(df)
    correlation_report = format_correlation_report(correlation_analysis)
    print(correlation_report)
    
    # ===== ANALYSE 5: Frauenanteil und Medaillenerfolg =====
    print("Führe Analyse 5 aus: Wie ist der Zusammenhang zwischen dem Frauenanteil eines Landes und der Gesamtanzahl der gewonnenen Medaillen...")
    gender_medals_analysis = analyze_gender_medals_correlation(df)
    gender_medals_report = format_gender_medals_report(gender_medals_analysis)
    print(gender_medals_report)
    
    # ===== ANALYSE 6: Gold und Gesamtmedaillen =====
    print("Führe Analyse 6 aus: Wie stark hängen Goldmedaillen mit der Gesamtmedaillenzahl zusammen")
    gold_analysis = analyze_gold_correlation(df)
    gold_report = format_gold_report(gold_analysis)
    print(gold_report)
    
    # ===== ANALYSE 7: Medaillen-Vielfalt nach Sportarten =====
    print("Führe Analyse 7 aus: Welche Länder haben in vielen verschiedenen Sportarten Medaillen")
    variety_analysis = analyze_sports_variety(df)
    variety_report = format_sports_variety_report(variety_analysis)
    print(variety_report)
    
    # ===== ANALYSE 8: Medaillen-Verteilung pro Sportart =====
    print("Führe Analyse 8 aus: In welchen Sportarten haben viele verschiedene Länder Medaillen gewonnen.")
    distribution_analysis = analyze_sports_distribution(df)
    distribution_report = format_sports_distribution_report(distribution_analysis)
    print(distribution_report)
    
    print("=" * 60)
    print("Analyse abgeschlossen!")
    print("=" * 60)


if __name__ == "__main__":
    main()
