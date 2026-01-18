import pandas as pd


def analyze_gender_medals_correlation(df: pd.DataFrame) -> dict:
    """
    Analysiert wie ist der Zusammenhang zwischen dem Frauenanteil eines Landes und der Gesamtanzahl der gewonnenen Medaillen
    """
    # Nur Länder mit Athleten
    df_with_athletes = df[df['Total Athletes'] > 0].copy()
    
    # Frauenanteil berechnen
    df_with_athletes['Frauenanteil (%)'] = (
        df_with_athletes['Women Athletes'] / df_with_athletes['Total Athletes'] * 100
    ).round(1)
    
    # Korrelation zwischen Frauenanteil und Medaillen
    correlation = df_with_athletes['Frauenanteil (%)'].corr(df_with_athletes['Total Medals'])
    
    # Länder mit Medaillen für detaillierte Analyse
    df_with_medals = df_with_athletes[df_with_athletes['Total Medals'] > 0].copy()
    
    # Durchschnittlicher Frauenanteil bei Ländern mit/ohne Medaillen
    avg_women_with_medals = df_with_medals['Frauenanteil (%)'].mean()
    df_without_medals = df_with_athletes[df_with_athletes['Total Medals'] == 0]
    avg_women_without_medals = df_without_medals['Frauenanteil (%)'].mean()
    
    # Ranking nach Frauenanteil (nur Länder mit Medaillen)
    ranking = df_with_medals[['NOC', 'Frauenanteil (%)', 'Women Athletes', 
                               'Total Athletes', 'Total Medals']].sort_values(
        'Frauenanteil (%)', ascending=False
    )
    
    return {
        'correlation': round(correlation, 3),
        'avg_women_with_medals': round(avg_women_with_medals, 1),
        'avg_women_without_medals': round(avg_women_without_medals, 1),
        'ranking': ranking,
        'countries_with_medals': len(df_with_medals),
        'countries_without_medals': len(df_without_medals)
    }


def format_gender_medals_report(analysis: dict) -> str:
    """
    Formatiert die Frauenanteil-Medaillen-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("ANALYSE: FRAUENANTEIL UND MEDAILLENERFOLG")
    lines.append("Gibt es einen Zusammenhang?")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("Korrelationsanalyse:")
    lines.append("-" * 40)
    lines.append(f"  Pearson-Korrelation:              {analysis['correlation']}")
    lines.append("")
    
    # Interpretation
    corr = analysis['correlation']
    if corr >= 0.3:
        interpretation = "POSITIV - Höherer Frauenanteil korreliert mit mehr Medaillen"
    elif corr <= -0.3:
        interpretation = "NEGATIV - Höherer Frauenanteil korreliert mit weniger Medaillen"
    else:
        interpretation = "KEIN klarer Zusammenhang erkennbar"
    
    lines.append(f"  Interpretation:                   {interpretation}")
    lines.append("")
    
    lines.append("Durchschnittlicher Frauenanteil:")
    lines.append("-" * 40)
    lines.append(f"  Länder MIT Medaillen ({analysis['countries_with_medals']:2}):       {analysis['avg_women_with_medals']:.1f}%")
    lines.append(f"  Länder OHNE Medaillen ({analysis['countries_without_medals']:2}):      {analysis['avg_women_without_medals']:.1f}%")
    lines.append("")
    
    lines.append("Medaillengewinner nach Frauenanteil:")
    lines.append("-" * 40)
    
    for _, row in analysis['ranking'].iterrows():
        lines.append(
            f"  {row['NOC']:30} "
            f"{row['Frauenanteil (%)']:5.1f}% Frauen -> "
            f"{int(row['Total Medals']):3} Medaillen"
        )
    
    lines.append("")
    
    return "\n".join(lines)
