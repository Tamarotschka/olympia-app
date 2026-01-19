import pandas as pd


def analyze_gold_correlation(df: pd.DataFrame) -> dict:
    """
    Analysiert, wie stark hängen Goldmedaillen mit der Gesamtmedaillenzahl zusammen
    """
    # Nur Länder mit Medaillen
    df_with_medals = df[df['Total Medals'] > 0].copy()
    
    # Korrelation zwischen Gold und Gesamtmedaillen
    correlation = df_with_medals['Gold'].corr(df_with_medals['Total Medals'])
    
    # Goldanteil berechnen
    df_with_medals['Goldanteil (%)'] = (
        df_with_medals['Gold'] / df_with_medals['Total Medals'] * 100
    ).round(1)
    
    # Durchschnittlicher Goldanteil
    avg_gold_percentage = df_with_medals['Goldanteil (%)'].mean()
    
    # Ranking nach Goldanteil
    ranking_by_gold_pct = df_with_medals[['NOC', 'Gold', 'Silver', 'Bronze', 
                                          'Total Medals', 'Goldanteil (%)']].sort_values(
        'Goldanteil (%)', ascending=False
    )
    
    # Ranking nach absoluten Goldmedaillen
    ranking_by_gold_abs = df_with_medals[['NOC', 'Gold', 'Total Medals', 
                                           'Goldanteil (%)']].sort_values(
        'Gold', ascending=False
    ).head(15)
    
    # Gesamtstatistik
    total_gold = df_with_medals['Gold'].sum()
    total_silver = df_with_medals['Silver'].sum()
    total_bronze = df_with_medals['Bronze'].sum()
    total_medals = df_with_medals['Total Medals'].sum()
    
    return {
        'correlation': round(correlation, 3),
        'avg_gold_percentage': round(avg_gold_percentage, 1),
        'ranking_by_gold_pct': ranking_by_gold_pct,
        'ranking_by_gold_abs': ranking_by_gold_abs,
        'stats': {
            'total_gold': int(total_gold),
            'total_silver': int(total_silver),
            'total_bronze': int(total_bronze),
            'total_medals': int(total_medals)
        }
    }


def format_gold_report(analysis: dict) -> str:
    """
    Formatiert die Gold-Korrelations-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Goldmedaillen und Gesamterfolg")
    lines.append("Wie stark hängen Goldmedaillen mit der Gesamtzahl zusammen?")
    lines.append("=" * 60)
    lines.append("")
    
    stats = analysis['stats']
    lines.append("Gesamtstatistik aller Medaillen:")
    lines.append("-" * 40)
    lines.append(f"  Gold:                     {stats['total_gold']:3} ({stats['total_gold']/stats['total_medals']*100:.1f}%)")
    lines.append(f"  Silber:                   {stats['total_silver']:3} ({stats['total_silver']/stats['total_medals']*100:.1f}%)")
    lines.append(f"  Bronze:                   {stats['total_bronze']:3} ({stats['total_bronze']/stats['total_medals']*100:.1f}%)")
    lines.append(f"  Gesamt:                   {stats['total_medals']:3}")
    lines.append("")
    
    lines.append("Korrelationsanalyse:")
    lines.append("-" * 40)
    lines.append(f"  Pearson-Korrelation:      {analysis['correlation']}")
    lines.append("")
    
    # Interpretation
    corr = analysis['correlation']
    if corr >= 0.9:
        interpretation = "Sehr stark - Goldmedaillen korrelieren stark mit Gesamterfolg"
    elif corr >= 0.7:
        interpretation = "Stark - Wer viel Gold holt, holt meist auch viele Medaillen"
    elif corr >= 0.4:
        interpretation = "Moderat - Ein Zusammenhang besteht"
    else:
        interpretation = "Schwach - Kein starker Zusammenhang"
    
    lines.append(f"  Interpretation:           {interpretation}")
    lines.append("")
    
    lines.append(f"  Durchschn. Goldanteil:    {analysis['avg_gold_percentage']:.1f}%")
    lines.append("")
    
    lines.append("Top 15 Länder nach Goldmedaillen:")
    lines.append("-" * 40)
    for _, row in analysis['ranking_by_gold_abs'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Gold']):2} Gold / {int(row['Total Medals']):2} Gesamt "
            f"({row['Goldanteil (%)']:5.1f}%)"
        )
    
    lines.append("")
    lines.append("Länder nach Goldanteil (nur mit Medaillen):")
    lines.append("-" * 40)
    
    for _, row in analysis['ranking_by_gold_pct'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{row['Goldanteil (%)']:5.1f}% "
            f"({int(row['Gold'])}G / {int(row['Silver'])}S / {int(row['Bronze'])}B)"
        )
    
    lines.append("")
    
    return "\n".join(lines)
