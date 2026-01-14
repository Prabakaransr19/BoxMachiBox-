# 🏎️ BoxMachiBox

AI-powered Formula 1 race predictions with **93.89% accuracy**.

*BoxMachiBox - Where AI meets the podium*

## 🎯 What It Does
Predicts which drivers will finish on the podium (top 3) in Formula 1 races using advanced machine learning.

## 🚀 Live Demo
[Try BoxMachiBox](https://boxmachibox.streamlit.app)

## 📊 Performance
- **Accuracy:** 93.89%
- **Model:** Multi-seed XGBoost Ensemble
- **Features:** 47 advanced engineered features
- **Training Data:** 2022-2025 F1 seasons (1,558 races)
- **Test Data:** 2025 R11-R19 (180 races)

## ✨ Features
- Real-time podium predictions
- Driver performance analysis
- Constructor comparison
- 2026 season outlook
- Interactive visualizations

## 🛠️ Tech Stack
- Python 3.10+
- XGBoost (Multi-seed Ensemble)
- Streamlit (Web Interface)
- Plotly (Visualizations)
- scikit-learn (ML Pipeline)

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/sarva-20/BoxMachiBox!.git
cd boxmachibox

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_production.py
```

## 🏆 Model Details

**Architecture:**
- Multi-seed XGBoost ensemble (5 models)
- 47 engineered features including:
  - Qualifying performance metrics
  - Driver momentum indicators
  - Constructor strength scores
  - Circuit-specific historical data

**Training Strategy:**
- Time-based split for realistic validation
- Regularization to prevent overfitting
- Hyperparameter optimization

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Test Accuracy | 93.89% |
| Precision (No Podium) | 94% |
| Recall (Podium) | 67% |
| F1-Score | 0.75 |

## 🎨 Screenshots
*(To be added after deployment)*

## 📂 Project Structure
```
boxmachibox/
├── app_production.py          # Main Streamlit application
├── f1_PRODUCTION_READY.pkl    # Trained model (93.89% accuracy)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── data/                      # Training data (not included)
```

## 🚀 Deployment
Deployed on Streamlit Cloud for free hosting and instant updates.

## 👨‍💻 Author
[Your Name] - Machine Learning Engineer

## 📄 License
MIT

## 🙏 Acknowledgments
- Data: 2022-2025 F1 seasons
- Inspired by the unpredictability of Formula 1 racing

---

**BoxMachiBox** - Predicting podiums, one race at a time! 🏁