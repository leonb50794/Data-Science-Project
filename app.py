import streamlit as st

st.set_page_config(
    page_title="Fuel Consumption App",
    page_icon="🚗",
    layout="wide"
)

st.title("Willkommen zur Fuel Consumption App 🚗")

st.markdown("""
### Über dieses Projekt
Diese App analysiert den CO2-Verbrauch von Fahrzeugen aus dem Jahr 2023.

**Die App ist in drei Bereiche unterteilt:**

1.  **📊 Daten Exploration:**
    - Filtern Sie die Rohdaten nach Marken, Hubraum und Kraftstoff.
    - Sehen Sie sich die wichtigsten Kennzahlen (KPIs) an.
    - Top & Flop Listen der saubersten und schmutzigsten Autos.

2.  **📈 Visualisierung:**
    - Detaillierte Grafiken und Analysen.
    - Zusammenhänge zwischen Motorgröße und CO2.

3.  **🤖 ML Vorhersage:**
    - Ein Machine Learning Modell sagt den CO2-Ausstoß für Ihr Traumauto vorher.
    - Geben Sie einfach Hubraum, Zylinder und Getriebe ein!

""")