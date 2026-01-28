import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import os

st.set_page_config(page_title="ML Vorhersage", page_icon="🤖")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'data','Fuel Consumption Ratings 2023_cleaned.csv')
    return pd.read_csv(file_path)

df = load_data()

st.title("🤖 CO2 Vorhersage Modell")

st.write("Hier trainieren wir ein ML-Modell live und machen Vorhersagen!")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Modell Training")
    st.write("Klicke, um ein Random Forest Modell zu trainieren.")
    
    if st.button("Modell trainieren"):
        with st.spinner("Trainiere Modell..."):
            
            X = df[['Engine Size (L)', 'Cylinders', 'Fuel Type']]
            y = df['CO2 Emissions (g/km)']
            
            X = pd.get_dummies(X, columns=['Fuel Type'], drop_first=False) # drop_first=False damit wir alle Spalten haben
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            score = model.score(X_test, y_test)
            
            st.session_state['model'] = model
            st.session_state['X_columns'] = X.columns.tolist()
            
            st.success(f"Modell trainiert! R² Score: {score:.2f}")

with col2:
    st.header("2. Neue Vorhersage")
    
    if 'model' not in st.session_state:
        st.info("Bitte trainiere zuerst das Modell links!")
    else:
        st.write("Gib Fahrzeugdaten ein:")
        
        input_engine = st.number_input("Hubraum (Liter)", 1.0, 8.4, 2.0, step=0.1)
        input_cyl = st.slider("Zylinder", 3, 16, 4)
        
        fuel_types = sorted(df['Fuel Type'].unique())
        input_fuel = st.selectbox("Kraftstoffart", fuel_types)
        
        if st.button("CO2 berechnen"):
            input_data = pd.DataFrame({
                'Engine Size (L)': [input_engine],
                'Cylinders': [input_cyl],
                'Fuel Type': [input_fuel]
            })
            
            input_data_encoded = pd.get_dummies(input_data, columns=['Fuel Type'])
            
            for col in st.session_state['X_columns']:
                if col not in input_data_encoded.columns:
                    input_data_encoded[col] = 0
            
            input_data_encoded = input_data_encoded[st.session_state['X_columns']]
            
            prediction = st.session_state['model'].predict(input_data_encoded)[0]
            
            st.metric("Geschätzter CO2 Ausstoß", f"{prediction:.1f} g/km")
            
            if prediction < 200:
                st.balloons()
                st.success("Das ist ein umweltfreundliches Auto!")
            else:
                st.error("Das Auto ist eher schlecht für die Umwelt!.")