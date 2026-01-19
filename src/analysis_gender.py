import pandas as pd


def analyze_gender_ratio(df: pd.DataFrame) -> dict:
    """
    Analysiert das Verhältnis von Männern zu Frauen pro Land.
    """
    # Nur Länder mit Athleten berücksichtigen
    df_with_athletes = df[df['Total Athletes'] > 0].copy()
    
    # Gesamtstatistik
    total_men = df_with_athletes['Men Athletes'].sum()
    total_women = df_with_athletes['Women Athletes'].sum()
    total_ratio = total_men / total_women if total_women > 0 else 0
    
    # Verhältnis pro Land berechnen
    df_with_athletes['Männeranteil (%)'] = (
        df_with_athletes['Men Athletes'] / df_with_athletes['Total Athletes'] * 100
    ).round(1)
    
    df_with_athletes['Frauenanteil (%)'] = (
        df_with_athletes['Women Athletes'] / df_with_athletes['Total Athletes'] * 100
    ).round(1)
    
    # Sortiert nach Frauenanteil (höchster zuerst)
    by_country = df_with_athletes[['NOC', 'Men Athletes', 'Women Athletes', 
                                    'Total Athletes', 'Männeranteil (%)', 
                                    'Frauenanteil (%)']].sort_values(
        'Frauenanteil (%)', ascending=False
    )
    
    return {
        'total': {
            'men': int(total_men),
            'women': int(total_women),
            'ratio': round(total_ratio, 2)
        },
        'by_country': by_country
    }


def format_gender_report(analysis: dict) -> str:
    """
    Formatiert die Geschlechterverhältnis-Analyse als lesbaren Text.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Analyse: Geschlechterverhältnis")
    lines.append("Verhältnis von Männern zu Frauen pro Land")
    lines.append("=" * 60)
    lines.append("")
    
    total = analysis['total']
    lines.append("Gesamtstatistik:")
    lines.append("-" * 40)
    lines.append(f"  Männliche Athleten:   {total['men']:5}")
    lines.append(f"  Weibliche Athleten:   {total['women']:5}")
    lines.append(f"  Verhältnis (M:F):     {total['ratio']}:1")
    lines.append("")
    
    lines.append("Top 15 Länder mit höchstem Frauenanteil:")
    lines.append("-" * 40)
    
    top_15 = analysis['by_country'].head(15)
    for _, row in top_15.iterrows():
        lines.append(
            f"  {row['NOC']:35} "
            f"{row['Frauenanteil (%)']:5.1f}% Frauen "
            f"({int(row['Women Athletes'])}/{int(row['Total Athletes'])} Athleten)"
        )
    
    lines.append("")
    lines.append("Top 15 Länder mit höchstem Männeranteil:")
    lines.append("-" * 40)
    
    bottom_15 = analysis['by_country'].tail(15).iloc[::-1]
    for _, row in bottom_15.iterrows():
        lines.append(
            f"  {row['NOC']:35} "
            f"{row['Männeranteil (%)']:5.1f}% Männer "
            f"({int(row['Men Athletes'])}/{int(row['Total Athletes'])} Athleten)"
        )
    
    lines.append("")
    
    return "\n".join(lines)
