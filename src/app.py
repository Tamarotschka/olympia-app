from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_olympics_data, clean_data, get_sport_columns

# Daten laden - Pfad relativ zum Skript-Verzeichnis
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "assets", "Olympics2022.csv")

df = load_olympics_data(data_path)
df = clean_data(df)
sport_columns = get_sport_columns(df)

# Dash App erstellen
app = Dash(__name__)

# Farben und Styling
colors = {
    'background': '#f8fafc',
    'card': '#ffffff',
    'primary': '#1e40af',
    'secondary': '#3b82f6',
    'accent': '#fbbf24',
    'text': '#1e293b',
    'text_light': '#64748b'
}

# CSS Styles
styles = {
    'container': {
        'fontFamily': '"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'backgroundColor': colors['background'],
        'minHeight': '100vh',
        'padding': '0'
    },
    'header': {
        'background': f'linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%)',
        'color': 'white',
        'padding': '2rem',
        'textAlign': 'center',
        'marginBottom': '2rem'
    },
    'title': {
        'fontSize': '2.5rem',
        'fontWeight': '700',
        'margin': '0',
        'letterSpacing': '-0.025em'
    },
    'subtitle': {
        'fontSize': '1.1rem',
        'opacity': '0.9',
        'marginTop': '0.5rem'
    },
    'tabs_container': {
        'maxWidth': '1400px',
        'margin': '0 auto',
        'padding': '0 2rem'
    },
    'card': {
        'backgroundColor': colors['card'],
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'padding': '1.5rem',
        'marginBottom': '1.5rem'
    },
    'stat_card': {
        'backgroundColor': colors['card'],
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'padding': '1.5rem',
        'textAlign': 'center',
        'flex': '1',
        'minWidth': '200px'
    },
    'stat_number': {
        'fontSize': '2.5rem',
        'fontWeight': '700',
        'color': colors['primary'],
        'margin': '0'
    },
    'stat_label': {
        'fontSize': '0.9rem',
        'color': colors['text_light'],
        'marginTop': '0.5rem'
    },
    'stats_row': {
        'display': 'flex',
        'gap': '1rem',
        'flexWrap': 'wrap',
        'marginBottom': '2rem'
    }
}


def create_medals_chart():
    df_with_medals = df[df['Total Medals'] > 0].copy()
    top_10 = df_with_medals.nlargest(10, 'Total Medals')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Gold', x=top_10['NOC'], y=top_10['Gold'], marker_color='#fbbf24'))
    fig.add_trace(go.Bar(name='Silber', x=top_10['NOC'], y=top_10['Silver'], marker_color='#94a3b8'))
    fig.add_trace(go.Bar(name='Bronze', x=top_10['NOC'], y=top_10['Bronze'], marker_color='#cd7f32'))
    
    fig.update_layout(
        title='Top 10 Länder nach Medaillen',
        xaxis_title='Land',
        yaxis_title='Anzahl Medaillen',
        barmode='stack',
        template='plotly_white',
        height=500
    )
    return fig


def create_scatter_chart():
    df_with_athletes = df[df['Total Athletes'] > 0].copy()
    
    fig = px.scatter(
        df_with_athletes,
        x='Total Athletes',
        y='Total Medals',
        text='NOC',
        size='Total Medals',
        color='Total Medals',
        color_continuous_scale='Blues',
        title='Zusammenhang: Athletenzahl und Medaillen'
    )
    fig.update_traces(textposition='top center', textfont_size=8)
    fig.update_layout(template='plotly_white', height=500)
    return fig


def create_gender_chart():
    df_top = df[df['Total Medals'] > 0].nlargest(15, 'Total Medals').copy()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Männer', x=df_top['NOC'], y=df_top['Men Athletes'], marker_color='#3b82f6'))
    fig.add_trace(go.Bar(name='Frauen', x=df_top['NOC'], y=df_top['Women Athletes'], marker_color='#ec4899'))
    
    fig.update_layout(
        title='Geschlechterverhältnis der Top 15',
        xaxis_title='Land',
        yaxis_title='Anzahl Athleten',
        barmode='group',
        template='plotly_white',
        height=500
    )
    return fig


def create_heatmap():
    df_top = df[df['Total Medals'] > 0].nlargest(15, 'Total Medals').copy()
    heatmap_data = df_top[['NOC'] + sport_columns].set_index('NOC')
    
    fig = px.imshow(
        heatmap_data.values,
        labels=dict(x='Sportart', y='Land', color='Medaillen'),
        x=sport_columns,
        y=heatmap_data.index.tolist(),
        color_continuous_scale='YlOrRd',
        title='Medaillen pro Sportart und Land'
    )
    fig.update_layout(xaxis_tickangle=-45, template='plotly_white', height=600)
    return fig


def create_pie_chart():
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
    fig.update_layout(template='plotly_white', height=500)
    return fig


def create_gold_chart():
    df_with_medals = df[df['Total Medals'] > 0].copy()
    df_with_medals['Goldanteil'] = (df_with_medals['Gold'] / df_with_medals['Total Medals'] * 100).round(1)
    df_sorted = df_with_medals.sort_values('Goldanteil', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted['Goldanteil'],
        y=df_sorted['NOC'],
        orientation='h',
        marker_color='#fbbf24',
        text=df_sorted['Goldanteil'].apply(lambda x: f'{x}%'),
        textposition='outside'
    ))
    fig.update_layout(
        title='Goldanteil an Gesamtmedaillen',
        xaxis_title='Goldanteil (%)',
        yaxis_title='Land',
        template='plotly_white',
        height=700
    )
    return fig


def create_variety_chart():
    df_with_medals = df[df['Total Medals'] > 0].copy()
    df_with_medals['Sportarten'] = df_with_medals[sport_columns].apply(lambda row: (row > 0).sum(), axis=1)
    df_sorted = df_with_medals.sort_values('Sportarten', ascending=False)
    
    fig = px.bar(
        df_sorted,
        x='NOC',
        y='Sportarten',
        color='Total Medals',
        color_continuous_scale='Blues',
        title='Anzahl Sportarten mit Medaillen pro Land'
    )
    fig.update_layout(template='plotly_white', height=500)
    return fig


# Statistiken berechnen
total_countries = len(df)
total_athletes = int(df['Total Athletes'].sum())
total_medals = int(df['Total Medals'].sum())
countries_with_medals = len(df[df['Total Medals'] > 0])

# App Layout
app.layout = html.Div(style=styles['container'], children=[
    # Header
    html.Div(style=styles['header'], children=[
        html.H1('Olympische Winterspiele 2022', style=styles['title']),
        html.P('Datenanalyse und Visualisierung - Peking', style=styles['subtitle'])
    ]),
    
    # Main Content
    html.Div(style=styles['tabs_container'], children=[
        # Statistik-Karten
        html.Div(style=styles['stats_row'], children=[
            html.Div(style=styles['stat_card'], children=[
                html.P(f'{total_countries}', style=styles['stat_number']),
                html.P('Teilnehmende Länder', style=styles['stat_label'])
            ]),
            html.Div(style=styles['stat_card'], children=[
                html.P(f'{total_athletes:,}', style=styles['stat_number']),
                html.P('Athleten gesamt', style=styles['stat_label'])
            ]),
            html.Div(style=styles['stat_card'], children=[
                html.P(f'{total_medals}', style=styles['stat_number']),
                html.P('Medaillen vergeben', style=styles['stat_label'])
            ]),
            html.Div(style=styles['stat_card'], children=[
                html.P(f'{countries_with_medals}', style=styles['stat_number']),
                html.P('Länder mit Medaillen', style=styles['stat_label'])
            ])
        ]),
        
        # Tabs
        dcc.Tabs(id='tabs', value='tab-medals', children=[
            dcc.Tab(label='Medaillen-Ranking', value='tab-medals', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
            dcc.Tab(label='Athleten & Erfolg', value='tab-athletes', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
            dcc.Tab(label='Geschlechter', value='tab-gender', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
            dcc.Tab(label='Sportarten', value='tab-sports', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
            dcc.Tab(label='Kontinente', value='tab-continents', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
            dcc.Tab(label='Gold-Effizienz', value='tab-gold', style={'padding': '12px'}, selected_style={'padding': '12px', 'borderTop': f'3px solid {colors["primary"]}'}),
        ], style={'marginBottom': '1.5rem'}),
        
        # Tab Content
        html.Div(id='tab-content', style=styles['card'])
    ]),
    
    # Footer
    html.Div(style={
        'textAlign': 'center',
        'padding': '2rem',
        'color': colors['text_light'],
        'fontSize': '0.9rem'
    }, children=[
        html.P('Olympia-Datenanalyse - Studentenprojekt 2022')
    ])
])


@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def update_tab(tab):
    if tab == 'tab-medals':
        return html.Div([
            html.H3('Medaillen-Ranking der Top 10 Länder', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Gestapeltes Balkendiagramm zeigt die Verteilung von Gold, Silber und Bronze.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_medals_chart())
        ])
    
    elif tab == 'tab-athletes':
        return html.Div([
            html.H3('Zusammenhang: Athletenzahl und Medaillen', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Korrelation zwischen der Größe des Teams und dem Erfolg bei den Spielen.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_scatter_chart())
        ])
    
    elif tab == 'tab-gender':
        return html.Div([
            html.H3('Geschlechterverhältnis der Teams', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Vergleich der Anzahl männlicher und weiblicher Athleten pro Land.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_gender_chart())
        ])
    
    elif tab == 'tab-sports':
        return html.Div([
            html.H3('Sportarten-Analyse', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Heatmap der Medaillenverteilung und Sportarten-Vielfalt pro Land.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_heatmap()),
            html.Hr(style={'margin': '2rem 0', 'border': 'none', 'borderTop': '1px solid #e2e8f0'}),
            dcc.Graph(figure=create_variety_chart())
        ])
    
    elif tab == 'tab-continents':
        return html.Div([
            html.H3('Medaillenverteilung nach Kontinent', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Tortendiagramm zeigt den Anteil jedes Kontinents am Gesamterfolg.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_pie_chart())
        ])
    
    elif tab == 'tab-gold':
        return html.Div([
            html.H3('Gold-Effizienz der Länder', style={'color': colors['text'], 'marginBottom': '1rem'}),
            html.P('Anteil der Goldmedaillen an den Gesamtmedaillen pro Land.', 
                   style={'color': colors['text_light'], 'marginBottom': '1rem'}),
            dcc.Graph(figure=create_gold_chart())
        ])


server = app.server  # Für Deployment (Gunicorn)

if __name__ == '__main__':
    print("Starte Dash-App auf http://127.0.0.1:8050")
    app.run(debug=True)
