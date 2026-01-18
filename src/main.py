from data_loader import load_olympics_data, clean_data
from analysis_countries import analyze_countries_by_continent, format_countries_report
from analysis_sports import analyze_sports_dominance, format_dominance_report
from analysis_gender import analyze_gender_ratio, format_gender_report
from analysis_correlation import analyze_athletes_medals_correlation, format_correlation_report
from analysis_gender_medals import analyze_gender_medals_correlation, format_gender_medals_report


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
    
    # ===== ANALYSE 3: Geschlechterverhältnis =====
    print("Führe Analyse 3 aus: Geschlechterverhältnis...")
    gender_analysis = analyze_gender_ratio(df)
    gender_report = format_gender_report(gender_analysis)
    print(gender_report)
    
    # ===== ANALYSE 4: Korrelation Athleten/Medaillen =====
    print("Führe Analyse 4 aus: Korrelation Athleten/Medaillen...")
    correlation_analysis = analyze_athletes_medals_correlation(df)
    correlation_report = format_correlation_report(correlation_analysis)
    print(correlation_report)
    
    # ===== ANALYSE 5: Frauenanteil und Medaillenerfolg =====
    print("Führe Analyse 5 aus: Frauenanteil und Medaillenerfolg...")
    gender_medals_analysis = analyze_gender_medals_correlation(df)
    gender_medals_report = format_gender_medals_report(gender_medals_analysis)
    print(gender_medals_report)
    
    print("=" * 60)
    print("Analyse abgeschlossen!")
    print("=" * 60)


if __name__ == "__main__":
    main()
