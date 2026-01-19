import pandas as pd
import numpy as np


def analyze_athletes_medals_correlation(df: pd.DataFrame) -> dict:
    """
    Gibt es einen Zusammenhang zwischen der Anzahl der Athlet:innen und der Anzahl der gewonnenen Medaillen
    """
    # Nur Länder mit Athleten
    df_with_athletes = df[df['Total Athletes'] > 0].copy()
    
    # Korrelation berechnen (Pearson)
    correlation = df_with_athletes['Total Athletes'].corr(df_with_athletes['Total Medals'])
    
    # Medaillen pro Athlet berechnen
    df_with_athletes['Medaillen pro Athlet'] = (
        df_with_athletes['Total Medals'] / df_with_athletes['Total Athletes']
    ).round(3)
    
    # Effizienz-Ranking: Länder mit mindestens 1 Medaille
    df_with_medals = df_with_athletes[df_with_athletes['Total Medals'] > 0].copy()
    efficiency_ranking = df_with_medals[['NOC', 'Total Athletes', 'Total Medals', 
                                          'Medaillen pro Athlet']].sort_values(
        'Medaillen pro Athlet', ascending=False
    )
    
    # Top 10 nach Athletenzahl
    top_by_athletes = df_with_athletes[['NOC', 'Total Athletes', 'Total Medals']].sort_values(
        'Total Athletes', ascending=False
    ).head(10)
    
    # Statistiken
    total_athletes = df_with_athletes['Total Athletes'].sum()
    total_medals = df_with_athletes['Total Medals'].sum()
    countries_with_medals = len(df_with_medals)
    countries_without_medals = len(df_with_athletes) - countries_with_medals
    
    return {
        'correlation': round(correlation, 3),
        'efficiency_ranking': efficiency_ranking,
        'top_by_athletes': top_by_athletes,
        'stats': {
            'total_athletes': int(total_athletes),
            'total_medals': int(total_medals),
            'countries_with_medals': countries_with_medals,
            'countries_without_medals': countries_without_medals
        }
    }


def format_correlation_report(analysis: dict) -> str:
    """
    Formatiert die Korrelations-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Zusammenhang Athleten und Medaillen")
    lines.append("Gibt es eine Korrelation zwischen Teamgröße und Erfolg?")
    lines.append("=" * 60)
    lines.append("")
    
    stats = analysis['stats']
    corr = analysis['correlation']
    
    lines.append("Gesamtstatistik:")
    lines.append("-" * 40)
    lines.append(f"  Athleten gesamt:          {stats['total_athletes']:5}")
    lines.append(f"  Medaillen gesamt:         {stats['total_medals']:5}")
    lines.append(f"  Länder mit Medaillen:     {stats['countries_with_medals']:5}")
    lines.append(f"  Länder ohne Medaillen:    {stats['countries_without_medals']:5}")
    lines.append("")
    
    lines.append("Korrelationsanalyse:")
    lines.append("-" * 40)
    lines.append(f"  Pearson-Korrelation:      {corr}")
    lines.append("")
    
    # Interpretation der Korrelation
    if corr >= 0.7:
        interpretation = "Stark positiv - Mehr Athleten = tendenziell mehr Medaillen"
    elif corr >= 0.4:
        interpretation = "Moderat positiv - Ein gewisser Zusammenhang besteht"
    elif corr >= 0.2:
        interpretation = "Schwach positiv - Geringer Zusammenhang"
    else:
        interpretation = "Kein/kaum Zusammenhang erkennbar"
    
    lines.append(f"  Interpretation:           {interpretation}")
    lines.append("")
    
    lines.append("Top 10 Länder nach Athletenzahl:")
    lines.append("-" * 40)
    for _, row in analysis['top_by_athletes'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{int(row['Total Athletes']):4} Athleten -> "
            f"{int(row['Total Medals']):3} Medaillen"
        )
    
    lines.append("")
    lines.append("Effizienz-Ranking (Medaillen pro Athlet):")
    lines.append("-" * 40)
    lines.append("  Nur Länder mit mindestens 1 Medaille")
    lines.append("")
    
    for _, row in analysis['efficiency_ranking'].head(15).iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{row['Medaillen pro Athlet']:.3f} "
            f"({int(row['Total Medals'])} Medaillen / {int(row['Total Athletes'])} Athleten)"
        )
    
    lines.append("")
    
    return "\n".join(lines)
