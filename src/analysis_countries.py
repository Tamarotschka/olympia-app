import pandas as pd


def analyze_countries_by_medals(df: pd.DataFrame) -> dict:
    """
    Welche Länder haben jeweils die meisten Gold-/Silber-/Bronzemedaillen gewonnen.
    """
    # Nur Länder mit Medaillen
    df_with_medals = df[df['Total Medals'] > 0].copy()
    
    # Top 10 nach Gold
    top_gold = df_with_medals[['NOC', 'Gold', 'Silver', 'Bronze', 'Total Medals']].sort_values(
        'Gold', ascending=False
    ).head(10)
    
    # Top 10 nach Silber
    top_silver = df_with_medals[['NOC', 'Gold', 'Silver', 'Bronze', 'Total Medals']].sort_values(
        'Silver', ascending=False
    ).head(10)
    
    # Top 10 nach Bronze
    top_bronze = df_with_medals[['NOC', 'Gold', 'Silver', 'Bronze', 'Total Medals']].sort_values(
        'Bronze', ascending=False
    ).head(10)
    
    # Top 10 nach Gesamt
    top_total = df_with_medals[['NOC', 'Gold', 'Silver', 'Bronze', 'Total Medals']].sort_values(
        'Total Medals', ascending=False
    ).head(10)
    
    # Gesamtstatistik
    total_gold = df_with_medals['Gold'].sum()
    total_silver = df_with_medals['Silver'].sum()
    total_bronze = df_with_medals['Bronze'].sum()
    total_medals = df_with_medals['Total Medals'].sum()
    
    return {
        'top_gold': top_gold,
        'top_silver': top_silver,
        'top_bronze': top_bronze,
        'top_total': top_total,
        'stats': {
            'total_gold': int(total_gold),
            'total_silver': int(total_silver),
            'total_bronze': int(total_bronze),
            'total_medals': int(total_medals),
            'countries_with_medals': len(df_with_medals)
        }
    }


def format_countries_report(analysis: dict) -> str:
    """
    Formatiert die Medaillen-Länder-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Medaillen-Ranking nach Ländern")
    lines.append("Olympische Winterspiele 2022 - Peking")
    lines.append("=" * 60)
    lines.append("")
    
    stats = analysis['stats']
    lines.append("Gesamtstatistik:")
    lines.append("-" * 40)
    lines.append(f"  Länder mit Medaillen:     {stats['countries_with_medals']}")
    lines.append(f"  Goldmedaillen gesamt:     {stats['total_gold']}")
    lines.append(f"  Silbermedaillen gesamt:   {stats['total_silver']}")
    lines.append(f"  Bronzemedaillen gesamt:   {stats['total_bronze']}")
    lines.append(f"  Medaillen gesamt:         {stats['total_medals']}")
    lines.append("")
    
    lines.append("Top 10 nach Goldmedaillen:")
    lines.append("-" * 40)
    for _, row in analysis['top_gold'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Gold']):2}G  {int(row['Silver']):2}S  {int(row['Bronze']):2}B  "
            f"= {int(row['Total Medals']):2} gesamt"
        )
    
    lines.append("")
    lines.append("Top 10 nach Silbermedaillen:")
    lines.append("-" * 40)
    for _, row in analysis['top_silver'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Gold']):2}G  {int(row['Silver']):2}S  {int(row['Bronze']):2}B  "
            f"= {int(row['Total Medals']):2} gesamt"
        )
    
    lines.append("")
    lines.append("Top 10 nach Bronzemedaillen:")
    lines.append("-" * 40)
    for _, row in analysis['top_bronze'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Gold']):2}G  {int(row['Silver']):2}S  {int(row['Bronze']):2}B  "
            f"= {int(row['Total Medals']):2} gesamt"
        )
    
    lines.append("")
    lines.append("Top 10 nach Gesamtmedaillen:")
    lines.append("-" * 40)
    for _, row in analysis['top_total'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Gold']):2}G  {int(row['Silver']):2}S  {int(row['Bronze']):2}B  "
            f"= {int(row['Total Medals']):2} gesamt"
        )
    
    lines.append("")
    
    return "\n".join(lines)
