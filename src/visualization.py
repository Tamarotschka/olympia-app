import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_medals_bar_chart(df: pd.DataFrame, output_path: str):
    """
    Erstellt ein Balkendiagramm der Top 10 Länder nach Medaillen.
    """
    df_with_medals = df[df['Total Medals'] > 0].copy()
    top_10 = df_with_medals.nlargest(10, 'Total Medals')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Gold',
        x=top_10['NOC'],
        y=top_10['Gold'],
        marker_color='gold'
    ))
    
    fig.add_trace(go.Bar(
        name='Silber',
        x=top_10['NOC'],
        y=top_10['Silver'],
        marker_color='silver'
    ))
    
    fig.add_trace(go.Bar(
        name='Bronze',
        x=top_10['NOC'],
        y=top_10['Bronze'],
        marker_color='#CD7F32'
    ))
    
    fig.update_layout(
        title='Top 10 Länder nach Medaillen - Olympische Winterspiele 2022',
        xaxis_title='Land',
        yaxis_title='Anzahl Medaillen',
        barmode='stack',
        template='plotly_white'
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_athletes_medals_scatter(df: pd.DataFrame, output_path: str):
    """
    Erstellt ein Streudiagramm: Athletenzahl vs. Medaillen.
    """
    df_with_athletes = df[df['Total Athletes'] > 0].copy()
    
    fig = px.scatter(
        df_with_athletes,
        x='Total Athletes',
        y='Total Medals',
        text='NOC',
        size='Total Medals',
        color='Total Medals',
        color_continuous_scale='Viridis',
        title='Zusammenhang: Anzahl Athleten und Medaillen'
    )
    
    fig.update_traces(textposition='top center', textfont_size=8)
    fig.update_layout(
        xaxis_title='Anzahl Athleten',
        yaxis_title='Anzahl Medaillen',
        template='plotly_white'
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_gender_ratio_chart(df: pd.DataFrame, output_path: str):
    """
    Erstellt ein Diagramm zum Geschlechterverhältnis der Top-Länder.
    """
    df_top = df[df['Total Medals'] > 0].nlargest(15, 'Total Medals').copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Männer',
        x=df_top['NOC'],
        y=df_top['Men Athletes'],
        marker_color='steelblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Frauen',
        x=df_top['NOC'],
        y=df_top['Women Athletes'],
        marker_color='coral'
    ))
    
    fig.update_layout(
        title='Geschlechterverhältnis der Top 15 Medaillengewinner',
        xaxis_title='Land',
        yaxis_title='Anzahl Athleten',
        barmode='group',
        template='plotly_white'
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_sports_dominance_heatmap(df: pd.DataFrame, sport_columns: list, output_path: str):
    """
    Erstellt eine Heatmap der Sportarten-Dominanz.
    """
    df_top = df[df['Total Medals'] > 0].nlargest(15, 'Total Medals').copy()
    
    heatmap_data = df_top[['NOC'] + sport_columns].set_index('NOC')
    
    fig = px.imshow(
        heatmap_data.values,
        labels=dict(x='Sportart', y='Land', color='Medaillen'),
        x=sport_columns,
        y=heatmap_data.index.tolist(),
        color_continuous_scale='YlOrRd',
        title='Medaillen pro Sportart und Land (Top 15)'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        template='plotly_white'
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_continent_pie_chart(df: pd.DataFrame, output_path: str):
    """
    Erstellt ein Tortendiagramm der Medaillenverteilung nach Kontinent.
    """
    continent_medals = df.groupby('Continent')['Total Medals'].sum().reset_index()
    continent_medals = continent_medals[continent_medals['Total Medals'] > 0]
    
    fig = px.pie(
        continent_medals,
        values='Total Medals',
        names='Continent',
        title='Medaillenverteilung nach Kontinent',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_gold_efficiency_chart(df: pd.DataFrame, output_path: str):
    """
    Erstellt ein Diagramm zum Gold-Anteil (Goldanteil an Gesamtmedaillen).
    """
    df_with_medals = df[df['Total Medals'] > 0].copy()
    df_with_medals['Goldanteil'] = (df_with_medals['Gold'] / df_with_medals['Total Medals'] * 100).round(1)
    df_sorted = df_with_medals.sort_values('Goldanteil', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_sorted['Goldanteil'],
        y=df_sorted['NOC'],
        orientation='h',
        marker_color='gold',
        text=df_sorted['Goldanteil'].apply(lambda x: f'{x}%'),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Goldanteil an Gesamtmedaillen pro Land',
        xaxis_title='Goldanteil (%)',
        yaxis_title='Land',
        template='plotly_white',
        height=800
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_sports_variety_chart(df: pd.DataFrame, sport_columns: list, output_path: str):
    """
    Erstellt ein Diagramm zur Sportarten-Vielfalt pro Land.
    """
    df_with_medals = df[df['Total Medals'] > 0].copy()
    df_with_medals['Sportarten'] = df_with_medals[sport_columns].apply(
        lambda row: (row > 0).sum(), axis=1
    )
    df_sorted = df_with_medals.sort_values('Sportarten', ascending=False)
    
    fig = px.bar(
        df_sorted,
        x='NOC',
        y='Sportarten',
        color='Total Medals',
        color_continuous_scale='Blues',
        title='Anzahl Sportarten mit Medaillen pro Land'
    )
    
    fig.update_layout(
        xaxis_title='Land',
        yaxis_title='Anzahl Sportarten',
        template='plotly_white'
    )
    
    fig.write_image(output_path)
    fig.write_html(output_path.replace('.png', '.html'))
    return fig


def create_all_visualizations(df: pd.DataFrame, sport_columns: list, output_dir: str):
    """
    Erstellt alle Visualisierungen und speichert sie im angegebenen Verzeichnis.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("  - Erstelle Medaillen-Balkendiagramm...")
    create_medals_bar_chart(df, f"{output_dir}/medaillen_ranking.png")
    
    print("  - Erstelle Athleten-Medaillen-Streudiagramm...")
    create_athletes_medals_scatter(df, f"{output_dir}/athleten_medaillen.png")
    
    print("  - Erstelle Geschlechterverhältnis-Diagramm...")
    create_gender_ratio_chart(df, f"{output_dir}/geschlechterverhaeltnis.png")
    
    print("  - Erstelle Sportarten-Heatmap...")
    create_sports_dominance_heatmap(df, sport_columns, f"{output_dir}/sportarten_heatmap.png")
    
    print("  - Erstelle Kontinent-Tortendiagramm...")
    create_continent_pie_chart(df, f"{output_dir}/kontinente_medaillen.png")
    
    print("  - Erstelle Gold-Anteil-Diagramm...")
    create_gold_efficiency_chart(df, f"{output_dir}/gold_effizienz.png")
    
    print("  - Erstelle Sportarten-Vielfalt-Diagramm...")
    create_sports_variety_chart(df, sport_columns, f"{output_dir}/sportarten_vielfalt.png")
    
    print(f"  Alle Grafiken wurden in '{output_dir}/' gespeichert.")
