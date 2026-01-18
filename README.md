# Olympia-Datenanalyse 2022

Das ist eine Python-Anwendung zur Analyse der Olympischen Winterspiele 2022 in Peking.

## Voraussetzungen

Für die lokale Entwicklung benötigen wir:
- Python 3.13+
- pip

## Installation & Ausführung

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren (Linux/Mac)
source venv/bin/activate

# Aktivieren (Windows)
venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Ausführen
cd src
python main.py
```

## Analysen

Die Anwendung beantwortet folgende Fragen:

1. **Länderverteilung**: Wie viele Länder nahmen teil und wie verteilen sich diese auf die Kontinente?
2. **Sportarten-Dominanz**: Welche Sportarten dominieren einzelne Länder?

## Erweiterung

Schritte, um eine neue Analyse hinzuzufügen:

1. Neue Funktion in `analysis.py` erstellen
2. Formatierungsfunktion für die Ausgabe erstellen
3. In `main.py` aufrufen

## Datenquelle

Die Daten stammen aus den offiziellen Ergebnissen der Olympischen Winterspiele 2022 in Peking. Die Datei liegt in /assets/
