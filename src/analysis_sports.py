import pandas as pd
from data_loader import get_sport_columns


def analyze_sports_dominance(df: pd.DataFrame) -> dict:
    """
    Analysiert welche Sportarten von einzelnen Ländern dominiert werden.
    """
    sport_columns = get_sport_columns(df)
    
    dominance = {}
    
    for sport in sport_columns:
        # Finde das Land mit den meisten Medaillen in dieser Sportart
        if df[sport].max() > 0:
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


def format_dominance_report(analysis: dict) -> str:
    """
    Formatiert die Dominanz-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Sportarten-Dominanz")
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
    
    for country, sports in analysis['top_countries'][:10]:
        lines.append(f"  {country:30} dominiert {len(sports)} Sportart(en):")
        for sport in sports:
            lines.append(f"    - {sport}")
    
    lines.append("")
    
    return "\n".join(lines)
