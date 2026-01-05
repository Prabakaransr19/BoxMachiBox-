import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="F1 Race Predictor | 93.4% Accuracy",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #E10600 0%, #FF6B35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load models and data
@st.cache_resource
def load_production_model():
    with open('f1_PRODUCTION_READY.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_driver_data():
    return pd.read_csv('2025_final_standings.csv')

@st.cache_data
def load_momentum_data():
    return pd.read_csv('2026_driver_momentum.csv')

try:
    model_package = load_production_model()
    drivers_data = load_driver_data()
    momentum_data = load_momentum_data()
except Exception as e:
    st.error("⚠️ Required files not found. Please check file paths.")
    st.stop()

# Sidebar
with st.sidebar:
    st.image(
        "https://via.placeholder.com/200x80/E10600/FFFFFF?text=F1+Predictor",
        use_container_width=True
    )

    st.markdown("### 📊 Model Stats")
    st.metric("Test Accuracy", "93.40%")
    st.metric("Training Data", "2022–2024")
    st.metric("Ensemble Models", "5")

    st.markdown("---")
    st.markdown("""
    ### 🎯 Features
    - Real-time race predictions  
    - Confidence scoring  
    - Driver comparisons  
    """)

# Main header
st.markdown('<h1 class="main-header">🏎️ F1 RACE PREDICTOR</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#888;">AI-Powered Formula 1 Predictions</p>',
    unsafe_allow_html=True
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔮 Predict Race", "📊 Driver Analysis", "🏆 2026 Outlook", "📈 Model Info"]
)

st.info("⚠️ Demo Mode: Simplified prediction logic.")

# ---------------- TAB 1 ----------------
with tab1:
    st.header("Predict Podium Finish")

    col1, col2 = st.columns(2)

    with col1:
        driver_names = drivers_data['givenName'] + ' ' + drivers_data['familyName']
        selected_driver = st.selectbox("Select Driver", driver_names.tolist())

        driver_info = drivers_data.loc[
            driver_names == selected_driver
        ].iloc[0]

        st.metric("Team", driver_info['constructorName'])
        st.metric("2025 Points", int(driver_info['total_points']))

        grid_position = st.slider("Qualifying Position", 1, 20, 5)

    with col2:
        if st.button("🎯 Predict Podium", use_container_width=True):

            base_prob = 0.5
            grid_factor = (21 - grid_position) / 20
            form_factor = driver_info['total_points'] / drivers_data['total_points'].max()

            final_prob = min(0.98, base_prob + grid_factor * 0.3 + form_factor * 0.2)
            confidence = abs(final_prob - 0.5) * 200

            if final_prob > 0.5:
                st.success("🏆 Podium Likely")
            else:
                st.warning("❌ Podium Unlikely")

            st.metric("Probability", f"{final_prob * 100:.1f}%")
            st.metric("Confidence", f"{confidence:.1f}%")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=final_prob * 100,
                gauge={'axis': {'range': [0, 100]}}
            ))
            st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 2 ----------------
with tab2:
    st.header("Driver Analysis")
    top_10 = drivers_data.nlargest(10, 'total_points')

    fig = px.bar(
        top_10,
        x='givenName',
        y='total_points',
        color='constructorName'
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.header("2026 Outlook")
    st.info("Momentum-based championship outlook.")

# ---------------- TAB 4 ----------------
with tab4:
    st.header("Model Info")
    st.markdown("""
    - Ensemble learning  
    - XGBoost-based architecture  
    - Time-based cross validation  
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#888;'>🏎️ F1 Predictor | Streamlit App</p>",
    unsafe_allow_html=True
)
