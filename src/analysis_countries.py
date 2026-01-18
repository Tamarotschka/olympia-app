import pandas as pd


def analyze_countries_by_continent(df: pd.DataFrame) -> dict:
    """
    Analysiert die Verteilung der teilnehmenden Länder nach Kontinenten.
    """
    # Gesamtzahl der Länder
    total_countries = len(df)
    
    # Gruppierung nach Kontinent
    continent_counts = df.groupby('Continent').size().sort_values(ascending=False)
    
    # Detaillierte Statistik pro Kontinent
    continent_details = df.groupby('Continent').agg({
        'NOC': 'count',
        'Total Athletes': 'sum',
        'Total Medals': 'sum'
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


def format_countries_report(analysis: dict) -> str:
    """
    Formatiert die Länderanalyse als lesbaren Text.
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
