import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Visualisierung", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data','Fuel Consumption Ratings 2023_cleaned.csv')
    return pd.read_csv(file_path)

df = load_data()

st.title("📈 Visualisierung")

vis_option = st.selectbox(
    'Wähle eine Analyse:',
    [
        'Scatterplot: Hubraum vs. CO2 (Interaktiv)', 
        'Boxplot: CO2 nach Fahrzeugklasse', 
        'Balkendiagramm: CO2 nach Kraftstoffart'
    ]
)

if vis_option == 'Scatterplot: Hubraum vs. CO2 (Interaktiv)':
    st.subheader("Interaktiver Zusammenhang: Hubraum & CO2")
    fig = px.scatter(
        df, 
        x='Engine Size (L)', 
        y='CO2 Emissions (g/km)',
        color='Vehicle Class',
        hover_data=['Make', 'Model'],
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

elif vis_option == 'Boxplot: CO2 nach Fahrzeugklasse':
    st.subheader("Verteilung CO2 nach Fahrzeugklasse")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='Vehicle Class', y='CO2 Emissions (g/km)', ax=ax, palette="Set2")
    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    st.pyplot(fig)

elif vis_option == 'Balkendiagramm: CO2 nach Kraftstoffart':
    st.subheader("Durchschnitt CO2 nach Kraftstoff")
    grouped_data = df.groupby('Fuel Type')['CO2 Emissions (g/km)'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_data.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    st.pyplot(fig)