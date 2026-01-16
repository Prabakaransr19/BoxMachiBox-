# BoxMachiBox 🏎️

An advanced Formula 1 analysis and prediction platform combining AI-powered predictions, real-time data analysis, and interactive visualizations.

## 🎯 Project Overview

This repository contains three integrated applications:

1. **Next.js Frontend** - Modern, responsive F1 analysis platform
2. **FastAPI Backend** - High-performance prediction API (93.89% accuracy)
3. **Streamlit Dashboard** - Interactive data science dashboard

## 🚀 Quick Start

### Frontend (Next.js)

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

### Backend API (FastAPI)

```bash
cd BoxMachiBox-API

# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn main:app --reload
```

API documentation available at [http://localhost:8000/docs](http://localhost:8000/docs)

### Streamlit Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app_production.py
```

Dashboard available at [http://localhost:8501](http://localhost:8501)

## 📦 Deployment

**For complete deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

Quick deployment options:
- ✅ **Vercel** - Recommended for Next.js frontend
- ✅ **GitHub Pages** - Already configured (auto-deploys on push to main)
- ✅ **Render/Railway** - Recommended for FastAPI backend
- ✅ **Streamlit Cloud** - Recommended for Streamlit dashboard
- ✅ **Docker** - For local or cloud deployment of all services

## 🛠️ Tech Stack

### Frontend
- Next.js 14
- React 18
- TypeScript
- TailwindCSS
- Framer Motion
- Lucide Icons

### Backend
- FastAPI
- Python 3.11
- XGBoost ML Model
- Pydantic
- Uvicorn

### Data Science
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn

## 📁 Project Structure

```
BoxMachiBox-/
├── src/                    # Next.js frontend source
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   └── types/             # TypeScript types
├── BoxMachiBox-API/       # FastAPI backend
│   ├── main.py           # API application
│   ├── models/           # ML models
│   └── requirements.txt  # Python dependencies
├── public/                # Static assets
├── app_production.py      # Streamlit dashboard
├── docker-compose.yml     # Docker orchestration
└── DEPLOYMENT.md          # Deployment guide
```

## 🎨 Features

### Frontend Features
- Interactive F1 race analysis
- Real-time predictions
- Driver comparisons
- Team standings
- Responsive design
- Dark mode optimized

### API Features
- Podium prediction endpoint
- Driver and circuit data
- Model performance metrics
- OpenAPI documentation
- CORS enabled

### Dashboard Features
- Interactive race predictions
- Driver analysis & comparisons
- 2026 season outlook
- Model performance stats
- Real-time visualizations

## 🔧 Development

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend/dashboard)
- npm or yarn
- pip

### Environment Variables

Create `.env.local` for frontend:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

See `.env.example` files for complete configuration options.

## 🧪 Testing

```bash
# Frontend
npm run lint

# Backend
cd BoxMachiBox-API
python -m pytest

# Type checking
npm run type-check
```

## 📊 Model Information

- **Model Type:** XGBoost Ensemble
- **Accuracy:** 93.89%
- **Training Data:** 1,838 samples (2022-2024 seasons)
- **Features:** Qualifying position, recent form, circuit mastery, weather conditions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is private and proprietary.

## 🔗 Links

- [Deployment Guide](./DEPLOYMENT.md)
- [FastAPI Documentation](http://localhost:8000/docs)
- [Next.js Documentation](https://nextjs.org/docs)

## 📞 Support

For issues and questions, please open an issue in the GitHub repository.

---

**Built with ❤️ for Formula 1 enthusiasts**
