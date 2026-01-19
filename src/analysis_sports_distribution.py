import pandas as pd
from data_loader import get_sport_columns


def analyze_sports_distribution(df: pd.DataFrame) -> dict:
    """
    In welchen Sportarten haben viele verschiedene Länder Medaillen gewonnen.
    """
    sport_columns = get_sport_columns(df)
    
    # Für jede Sportart: Wie viele Länder haben Medaillen?
    sport_stats = []
    
    for sport in sport_columns:
        countries_with_medals = (df[sport] > 0).sum()
        total_medals = df[sport].sum()
        
        # Liste der Länder mit Medaillen in dieser Sportart
        countries = df[df[sport] > 0][['NOC', sport]].sort_values(sport, ascending=False)
        country_list = [(row['NOC'], int(row[sport])) for _, row in countries.iterrows()]
        
        sport_stats.append({
            'sport': sport,
            'countries': countries_with_medals,
            'total_medals': int(total_medals),
            'country_list': country_list
        })
    
    # Sortieren nach Anzahl Länder (breiteste Verteilung zuerst)
    sport_stats_sorted = sorted(sport_stats, key=lambda x: x['countries'], reverse=True)
    
    # Statistiken
    avg_countries = sum(s['countries'] for s in sport_stats) / len(sport_stats)
    max_countries = max(s['countries'] for s in sport_stats)
    min_countries = min(s['countries'] for s in sport_stats)
    
    return {
        'sports': sport_stats_sorted,
        'stats': {
            'total_sports': len(sport_columns),
            'avg_countries_per_sport': round(avg_countries, 1),
            'max_countries': max_countries,
            'min_countries': min_countries
        }
    }


def format_sports_distribution_report(analysis: dict) -> str:
    """
    Formatiert die Sportarten-Verteilungs-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Medaillen-Verteilung pro Sportart")
    lines.append("In welchen Sportarten haben viele Länder Medaillen?")
    lines.append("=" * 60)
    lines.append("")
    
    stats = analysis['stats']
    lines.append("Statistik:")
    lines.append("-" * 40)
    lines.append(f"  Sportarten gesamt:                  {stats['total_sports']}")
    lines.append(f"  Durchschn. Länder pro Sportart:     {stats['avg_countries_per_sport']}")
    lines.append(f"  Breiteste Verteilung:               {stats['max_countries']} Länder")
    lines.append(f"  Engste Verteilung:                  {stats['min_countries']} Länder")
    lines.append("")
    
    lines.append("Ranking nach Anzahl teilnehmender Länder:")
    lines.append("-" * 40)
    
    for sport in analysis['sports']:
        lines.append(
            f"  {sport['sport']:30} "
            f"{sport['countries']:2} Länder "
            f"({sport['total_medals']:3} Medaillen gesamt)"
        )
    
    lines.append("")
    lines.append("Detaillierte Aufschlüsselung:")
    lines.append("-" * 40)
    
    for sport in analysis['sports']:
        lines.append(f"  {sport['sport']} ({sport['countries']} Länder):")
        for country, medals in sport['country_list']:
            lines.append(f"    - {country}: {medals}")
        lines.append("")
    
    return "\n".join(lines)
