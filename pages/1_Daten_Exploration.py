import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Daten Exploration", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data','Fuel Consumption Ratings 2023_cleaned.csv')
    return pd.read_csv(file_path)

st.title("📊 Daten Exploration")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Fehler: CSV-Datei nicht gefunden. Bitte stelle sicher, dass sie im Hauptordner liegt.")
    st.stop()

st.sidebar.header("Filter Einstellungen")

all_makes = sorted(df['Make'].unique())
selected_makes = st.sidebar.multiselect("Marken (leer = alle):", all_makes)

min_engine, max_engine = float(df['Engine Size (L)'].min()), float(df['Engine Size (L)'].max())
engine_range = st.sidebar.slider("Hubraum (L):", min_engine, max_engine, (min_engine, max_engine))

fuel_options = ['Alle'] + sorted(list(df['Fuel Type'].unique()))
selected_fuel = st.sidebar.selectbox("Kraftstoffart:", fuel_options)

filtered_df = df.copy()
if selected_makes:
    filtered_df = filtered_df[filtered_df['Make'].isin(selected_makes)]
filtered_df = filtered_df[
    (filtered_df['Engine Size (L)'] >= engine_range[0]) & 
    (filtered_df['Engine Size (L)'] <= engine_range[1])
]
if selected_fuel != 'Alle':
    filtered_df = filtered_df[filtered_df['Fuel Type'] == selected_fuel]

st.write(f"Zeige **{len(filtered_df)}** von {len(df)} Fahrzeugen")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fahrzeuge", len(filtered_df))
c2.metric("Ø CO2", f"{filtered_df['CO2 Emissions (g/km)'].mean():.1f} g/km")
c3.metric("Ø Hubraum", f"{filtered_df['Engine Size (L)'].mean():.1f} L")
c4.metric("Ø Zylinder", f"{filtered_df['Cylinders'].mean():.1f}")

st.markdown("---")

c_top, c_flop =st.columns(2)
with c_top:
    st.subheader("🌱 Top 5 (Wenig CO2)")
    st.dataframe(filtered_df.nsmallest(5, 'CO2 Emissions (g/km)')[['Make', 'Model', 'CO2 Emissions (g/km)']], hide_index=True)

with c_flop:
    st.subheader("🏭 Flop 5 (Viel CO2)")
    st.dataframe(filtered_df.nlargest(5, 'CO2 Emissions (g/km)')[['Make', 'Model', 'CO2 Emissions (g/km)']], hide_index=True)

with st.expander("Gefilterte Rohdaten anzeigen"):
    st.dataframe(filtered_df)