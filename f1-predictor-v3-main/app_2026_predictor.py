import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="F1 2026 Podium Predictor",
    page_icon="🏎️",
    layout="wide"
)

# Title
st.title("🏎️ F1 2026 Race Podium Predictor")
st.markdown("### AI-Powered Formula 1 Predictions | 93.40% Accuracy")
st.markdown("---")

from pathlib import Path

# Load model (use absolute path relative to this script so Streamlit can be
# launched from any working directory)
ROOT = Path(__file__).parent

@st.cache_resource
def load_model():
    with open(ROOT / 'my_f1_model_FINAL_OPTIMIZED.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_2025_data():
    with open(ROOT / '2025_final_standings.pkl', 'rb') as f:
        return pickle.load(f)

model_package = load_model()
driver_data_2025 = load_2025_data()

# Sidebar - Model Info
with st.sidebar:
    st.header("📊 Model Performance")
    st.metric("Test Accuracy", f"{model_package['accuracy']*100:.2f}%")
    st.metric("Ensemble Models", len(model_package['models']))
    st.metric("Training Data", "2022-2024 Seasons")
    st.metric("Test Data", "2025 Season")
    
    st.markdown("---")
    st.markdown("### 🎯 Model Features")
    st.markdown("- Qualifying Performance")
    st.markdown("- Driver Form & Momentum")
    st.markdown("- Constructor Strength")
    st.markdown("- Circuit-Specific Stats")
    st.markdown("- Championship Pressure")

# Main content
tab1, tab2, tab3 = st.tabs(["🔮 Make Prediction", "📈 Driver Analysis", "ℹ️ About"])

with tab1:
    st.header("Predict 2026 Race Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Driver selection
        driver_names = driver_data_2025['givenName'] + ' ' + driver_data_2025['familyName']
        selected_driver = st.selectbox("Select Driver", driver_names.tolist())
        
        # Get driver data
        driver_idx = driver_names[driver_names == selected_driver].index[0]
        driver_info = driver_data_2025.iloc[driver_idx]
        
        st.markdown(f"**Team:** {driver_info['constructorName']}")
        st.markdown(f"**2025 Points:** {driver_info['driver_season_points']:.0f}")
        
        # Race parameters
        st.markdown("### Race Parameters")
        grid_position = st.slider("Qualifying Position", 1, 20, 5)
        circuit_type = st.selectbox("Circuit Type", 
                                    ["Street Circuit", "Permanent Circuit", "High Speed"])
        
    with col2:
        st.markdown("### Prediction")
        
        if st.button("🎯 Predict Podium Finish", type="primary"):
            # Prepare features for prediction
            # (You'll need to construct this properly based on your features)
            prediction_data = driver_info.to_dict()
            prediction_data['grid_position'] = grid_position

            try:
                # Construct feature dictionary from driver data
                feature_dict = {}

                for feature in model_package['features']:
                    if feature in prediction_data:
                        feature_dict[feature] = prediction_data[feature]
                    else:
                        # Set defaults for missing features
                        feature_dict[feature] = 0

                # Override with race-specific parameters
                feature_dict['grid_position'] = grid_position

                # Create DataFrame
                X_pred = pd.DataFrame([feature_dict])

                # Encode categorical columns
                for col in model_package.get('categorical_cols', []):
                    if col in X_pred.columns:
                        le = model_package['label_encoders'].get(col)
                        if le:
                            try:
                                X_pred[col] = le.transform(X_pred[col].astype(str))
                            except Exception:
                                X_pred[col] = -1

                # Ensure correct column order
                X_pred = X_pred.reindex(columns=model_package['features'], fill_value=0)

                # Get predictions from ensemble
                all_probas = []
                for name, model, weight in model_package['models']:
                    proba = model.predict_proba(X_pred)[:, 1][0]
                    all_probas.append(proba)

                # Weighted average
                weights = model_package.get('weights', [1/len(all_probas)]*len(all_probas))
                final_proba = np.average(all_probas, weights=weights)

                # Make prediction
                prediction = 1 if final_proba >= model_package.get('threshold', 0.5) else 0

                # Confidence calculation
                distance_from_threshold = abs(final_proba - model_package.get('threshold', 0.5))
                max_distance = max(model_package.get('threshold', 0.5), 1 - model_package.get('threshold', 0.5))
                confidence = min((distance_from_threshold / max_distance) * 100, 99)

                result = {
                    'podium_prediction': 'YES' if prediction == 1 else 'NO',
                    'probability': final_proba * 100,
                    'confidence': confidence
                }

                # Display result
                if result['podium_prediction'] == 'YES':
                    st.success("### 🏆 PODIUM LIKELY!")
                    st.metric("Probability", f"{result['probability']:.1f}%")
                    st.metric("Confidence", f"{result['confidence']:.1f}%")
                else:
                    st.info("### ❌ Podium Unlikely")
                    st.metric("Probability", f"{result['probability']:.1f}%")
                    st.metric("Confidence", f"{result['confidence']:.1f}%")

                # Probability gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = result['probability'],
                    title = {'text': "Podium Probability"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkred"},
                        'steps': [
                            {'range': [0, 33], 'color': "lightgray"},
                            {'range': [33, 66], 'color': "gray"},
                            {'range': [66, 100], 'color': "darkgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, width='stretch')

            except Exception as e:
                st.error(f"Prediction error: {e}")

with tab2:
    st.header("📈 Driver Performance Analysis")
    
    # Top performers
    top_10 = driver_data_2025.nlargest(10, 'driver_season_points')
    
    fig = px.bar(
        top_10,
        x='givenName',
        y='driver_season_points',
        color='constructorName',
        title="Top 10 Drivers - 2025 Season Points"
    )
    st.plotly_chart(fig, width='stretch')
    
    # Driver comparison
    st.subheader("Compare Drivers")
    col1, col2 = st.columns(2)
    
    with col1:
        driver1 = st.selectbox("Driver 1", driver_names.tolist(), key='d1')
    with col2:
        driver2 = st.selectbox("Driver 2", driver_names.tolist(), key='d2')
    
    # Show comparison metrics
    # (Add comparison logic here)

with tab3:
    st.header("ℹ️ About This Project")
    
    st.markdown("""
    ### 🏎️ F1 2026 Podium Predictor
    
    This AI-powered prediction system forecasts Formula 1 race outcomes with **93.40% accuracy**.
    
    #### 🎯 Model Architecture
    - **Ensemble of 5 ML Models**: XGBoost (x3), Random Forest, Gradient Boosting
    - **Training Data**: 2022-2024 F1 seasons (1,359 races)
    - **Test Performance**: 93.40% accuracy on 2025 season
    - **Features Used**: 69 engineered features including:
      - Qualifying performance
      - Recent race form
      - Constructor strength
      - Circuit-specific statistics
      - Championship pressure indicators
    
    #### 📊 Performance Metrics
    - **Precision (No Podium)**: 97% - Very reliable
    - **Recall (Podium)**: 81% - Catches most podiums
    - **Overall Accuracy**: 93.40%
    
    #### 🚀 Technology Stack
    - Python, scikit-learn, XGBoost
    - Streamlit for web interface
    - Plotly for visualizations
    
    #### 👨‍💻 Created by: [Sarvatarshan Sankar]
    Portfolio project demonstrating advanced machine learning and data science skills.
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for F1 fans | Data: 2022-2025 F1 Seasons")