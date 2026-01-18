import pandas as pd
from data_loader import get_sport_columns

def analyze_countries_by_continent(df: pd.DataFrame) -> dict:
    """
    Analysiert die Verteilung der teilnehmenden Länder nach Kontinenten.
    
    Beantwortet: "Wie viele Länder nahmen an den Winterspielen teil 
    und wie verteilen sich diese auf die Kontinente?"
    
    Parameter:
        df: Bereinigter DataFrame mit Olympia-Daten
    
    Rückgabe:
        Dictionary mit Analyseergebnissen:
        - total_countries: Gesamtzahl teilnehmender Länder
        - by_continent: Dict mit Kontinent -> Anzahl Länder
        - details: DataFrame mit detaillierten Infos pro Kontinent
    """
    # Gesamtzahl der Länder
    total_countries = len(df)
    
    # Gruppierung nach Kontinent
    continent_counts = df.groupby('Continent').size().sort_values(ascending=False)
    
    # Detaillierte Statistik pro Kontinent
    continent_details = df.groupby('Continent').agg({
        'NOC': 'count',  # Anzahl Länder
        'Total Athletes': 'sum',  # Gesamte Athleten
        'Total Medals': 'sum'  # Gesamte Medaillen
    }).rename(columns={
        'NOC': 'Anzahl Länder',
        'Total Athletes': 'Athleten gesamt',
        'Total Medals': 'Medaillen gesamt'
    }).sort_values('Anzahl Länder', ascending=False)
    
    return {
        'total_countries': total_countries,
        'by_continent': continent_counts.to_dict(),
        'details': continent_details
    }


def analyze_sports_dominance(df: pd.DataFrame) -> dict:
    """
    Analysiert welche Sportarten von einzelnen Ländern dominiert werden.
    
    Beantwortet: "Welche Sportarten dominieren einzelne Länder?"
    
    Ein Land "dominiert" eine Sportart, wenn es die meisten Medaillen
    in dieser Sportart gewonnen hat.
    
    Parameter:
        df: Bereinigter DataFrame mit Olympia-Daten
    
    Rückgabe:
        Dictionary mit:
        - dominance: Dict mit Sportart -> (Land, Anzahl Medaillen)
        - top_countries: Liste der Länder mit den meisten dominierten Sportarten
    """
    sport_columns = get_sport_columns(df)
    
    dominance = {}
    
    for sport in sport_columns:
        # Finde das Land mit den meisten Medaillen in dieser Sportart
        if df[sport].max() > 0:  # Nur wenn überhaupt Medaillen vergeben wurden
            max_idx = df[sport].idxmax()
            max_medals = df.loc[max_idx, sport]
            country = df.loc[max_idx, 'NOC']
            dominance[sport] = {
                'land': country,
                'medaillen': int(max_medals)
            }
    
    # Zähle wie oft jedes Land eine Sportart dominiert
    country_dominance_count = {}
    for sport, info in dominance.items():
        country = info['land']
        if country not in country_dominance_count:
            country_dominance_count[country] = []
        country_dominance_count[country].append(sport)
    
    # Sortiere nach Anzahl dominierter Sportarten
    top_countries = sorted(
        country_dominance_count.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    return {
        'dominance': dominance,
        'top_countries': top_countries
    }


def format_countries_report(analysis: dict) -> str:
    """
    Formatiert die Länderanalyse als lesbaren Text.
    
    Parameter:
        analysis: Ergebnis von analyze_countries_by_continent()
    
    Rückgabe:
        Formatierter Textbericht
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ANALYSE: TEILNEHMENDE LÄNDER NACH KONTINENTEN")
    lines.append("Olympische Winterspiele 2022 - Peking")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Gesamtzahl teilnehmender Länder: {analysis['total_countries']}")
    lines.append("")
    lines.append("Verteilung nach Kontinenten:")
    lines.append("-" * 40)
    
    for continent, count in analysis['by_continent'].items():
        percentage = (count / analysis['total_countries']) * 100
        lines.append(f"  {continent:20} {count:3} Länder ({percentage:5.1f}%)")
    
    lines.append("")
    lines.append("Detaillierte Übersicht:")
    lines.append("-" * 40)
    lines.append(analysis['details'].to_string())
    lines.append("")
    
    return "\n".join(lines)


def format_dominance_report(analysis: dict) -> str:
    """
    Formatiert die Dominanz-Analyse als lesbaren Text.
    
    Parameter:
        analysis: Ergebnis von analyze_sports_dominance()
    
    Rückgabe:
        Formatierter Textbericht
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ANALYSE: SPORTARTEN-DOMINANZ")
    lines.append("Welches Land führt in welcher Sportart?")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("Dominanz nach Sportart (meiste Medaillen):")
    lines.append("-" * 40)
    
    for sport, info in analysis['dominance'].items():
        lines.append(f"  {sport:30} {info['land']:30} ({info['medaillen']} Medaillen)")
    
    lines.append("")
    lines.append("Top-Länder nach Anzahl dominierter Sportarten:")
    lines.append("-" * 40)
    
    for country, sports in analysis['top_countries'][:10]:  # Top 10
        lines.append(f"  {country:30} dominiert {len(sports)} Sportart(en):")
        for sport in sports:
            lines.append(f"    - {sport}")
    
    lines.append("")
    
    return "\n".join(lines)
