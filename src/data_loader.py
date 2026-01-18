import pandas as pd


def load_olympics_data(pfad: str) -> pd.DataFrame:
    """
    Lädt die Olympia-Daten aus einer CSV-Datei.
    
    pfad - Pfad zur CSV-Datei
    
    Rückgabe: DataFrame mit den Olympia-Daten
    """
    # CSV mit Semikolon als Trennzeichen einlesen
    df = pd.read_csv(pfad, sep=';')
    return df


def get_sport_columns(df: pd.DataFrame) -> list:
    """
    Gibt eine Liste aller Sportarten-Spalten zurück.
    
    Die Sportarten beginnen ab Spalte 12 in der CSV Datei (Index 12).
    
    df - DataFrame mit Olympia-Daten (pandas)
    
    Rückgabe - Liste der Sportarten-Spaltennamen
    """
    # Sportarten sind ab Spalte 12 (nach den Medaillen-Spalten)
    sport_columns = df.columns[12:].tolist()
    return sport_columns


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bereinigt die Daten für die Analyse.
    
    - Füllt fehlende Werte in numerischen Spalten mit 0
    - Entfernt führende/nachfolgende Leerzeichen in Textspalten
    
    df - DataFrame mit Rohdaten (pandas)
    
    Rückgabe - Bereinigter oandas DataFrame
    """
    # Kopie erstellen, um Original nicht zu verändern
    df_clean = df.copy()
    
    # Sportarten-Spalten mit 0 füllen (leere bedeutet keine Medaillen)
    sport_columns = get_sport_columns(df_clean)
    for col in sport_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0).astype(int)
    
    # Medaillen-Spalten ebenfalls bereinigen
    medal_columns = ['Gold', 'Silver', 'Bronze', 'Total Medals']
    for col in medal_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0).astype(int)
    
    # Text-Spalten bereinigen
    text_columns = ['NOC', 'NOC CODE', 'Continent']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
    
    return df_clean
