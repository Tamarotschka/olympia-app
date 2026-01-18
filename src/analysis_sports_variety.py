import pandas as pd
from data_loader import get_sport_columns


def analyze_sports_variety(df: pd.DataFrame) -> dict:
    """
    Welche Länder haben in vielen verschiedenen Sportarten Medaillen
    """
    sport_columns = get_sport_columns(df)
    
    # Nur Länder mit Medaillen
    df_with_medals = df[df['Total Medals'] > 0].copy()
    
    # Zähle für jedes Land die Anzahl der Sportarten mit Medaillen
    df_with_medals['Sportarten mit Medaillen'] = df_with_medals[sport_columns].apply(
        lambda row: (row > 0).sum(), axis=1
    )
    
    # Ranking nach Anzahl verschiedener Sportarten
    ranking = df_with_medals[['NOC', 'Sportarten mit Medaillen', 'Total Medals']].sort_values(
        'Sportarten mit Medaillen', ascending=False
    )
    
    # Detaillierte Ansicht: Welche Sportarten pro Land
    details = {}
    for _, row in df_with_medals.iterrows():
        country = row['NOC']
        sports_with_medals = []
        for sport in sport_columns:
            if row[sport] > 0:
                sports_with_medals.append((sport, int(row[sport])))
        if sports_with_medals:
            details[country] = sorted(sports_with_medals, key=lambda x: x[1], reverse=True)
    
    # Statistiken
    total_sports = len(sport_columns)
    avg_sports_per_country = df_with_medals['Sportarten mit Medaillen'].mean()
    max_sports = df_with_medals['Sportarten mit Medaillen'].max()
    
    return {
        'ranking': ranking,
        'details': details,
        'stats': {
            'total_sports': total_sports,
            'avg_sports_per_country': round(avg_sports_per_country, 1),
            'max_sports': int(max_sports),
            'countries_with_medals': len(df_with_medals)
        }
    }


def format_sports_variety_report(analysis: dict) -> str:
    """
    Formatiert die Sportarten-Vielfalt-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ANALYSE: MEDAILLEN-VIELFALT NACH SPORTARTEN")
    lines.append("Welche Länder haben in vielen Sportarten Medaillen?")
    lines.append("=" * 60)
    lines.append("")
    
    stats = analysis['stats']
    lines.append("Statistik:")
    lines.append("-" * 40)
    lines.append(f"  Sportarten gesamt:                {stats['total_sports']}")
    lines.append(f"  Länder mit Medaillen:             {stats['countries_with_medals']}")
    lines.append(f"  Durchschn. Sportarten pro Land:   {stats['avg_sports_per_country']}")
    lines.append(f"  Maximum Sportarten (ein Land):    {stats['max_sports']}")
    lines.append("")
    
    lines.append("Ranking nach Anzahl Sportarten mit Medaillen:")
    lines.append("-" * 40)
    
    for _, row in analysis['ranking'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Sportarten mit Medaillen']):2} Sportarten -> "
            f"{int(row['Total Medals']):3} Medaillen gesamt"
        )
    
    lines.append("")
    lines.append("Top 10 - Detaillierte Aufschlüsselung:")
    lines.append("-" * 40)
    
    # Top 10 Länder mit Details
    top_countries = analysis['ranking'].head(10)['NOC'].tolist()
    
    for country in top_countries:
        sports = analysis['details'].get(country, [])
        lines.append(f"  {country}:")
        for sport, medals in sports:
            lines.append(f"    - {sport}: {medals} Medaille(n)")
        lines.append("")
    
    return "\n".join(lines)
