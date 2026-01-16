# BoxMachiBox Deployment Guide

This repository contains three applications that can be deployed independently:

1. **Next.js Frontend** - Main F1 analysis platform
2. **FastAPI Backend** - Prediction API service
3. **Streamlit App** - Data science dashboard

---

## 🚀 Quick Deployment Options

### Option 1: Deploy Frontend to Vercel (Recommended)
### Option 2: Deploy Frontend to GitHub Pages (Already Configured)
### Option 3: Deploy Backend to Render/Railway
### Option 4: Docker Deployment (All Services)

---

## 📦 1. Next.js Frontend Deployment

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Local Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### A. Deploy to Vercel (Recommended for Frontend)

**Steps:**

1. **Install Vercel CLI** (optional, for CLI deployment)
   ```bash
   npm i -g vercel
   ```

2. **Deploy via Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository: `Prabakaransr19/BoxMachiBox-`
   - Configure:
     - Framework Preset: `Next.js`
     - Root Directory: `./`
     - Build Command: `npm run build`
     - Output Directory: `.next`
   - Click "Deploy"

3. **Deploy via CLI**
   ```bash
   vercel
   ```

4. **Environment Variables** (if needed)
   - Add any required environment variables in Vercel dashboard
   - For API integration: `NEXT_PUBLIC_API_URL`

**Configuration:**
The repository includes `next.config.mjs` with export configuration. For Vercel deployment, you may want to modify it:

```javascript
// For Vercel (remove export and basePath)
const nextConfig = {
  images: {
    unoptimized: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};
```

### B. Deploy to GitHub Pages (Already Configured)

**Current Setup:**
- Workflow: `.github/workflows/deploy.yml`
- Configured for static export with basePath: `/BoxMachiBox-/`
- Triggers on push to `main` branch

**Steps:**

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: GitHub Actions
   - The workflow will automatically deploy on push to main

2. **Access your site**
   - URL: `https://prabakaransr19.github.io/BoxMachiBox-/`

**Note:** The current configuration is set for GitHub Pages with static export. This works but has limitations (no SSR, no API routes).

### C. Deploy to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub and select repository
4. Configure:
   - Build command: `npm run build`
   - Publish directory: `out` (for static export) or `.next` (for SSR)
5. Click "Deploy"

---

## 🔧 2. FastAPI Backend Deployment

### Prerequisites
- Python 3.8+
- pip package manager

### Local Development
```bash
cd BoxMachiBox-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
# or
uvicorn main:app --reload

# Access API docs
# http://localhost:8000/docs
```

### A. Deploy to Render

**Steps:**

1. **Prepare Repository**
   - Rename `Procfile.txt` to `Procfile`
   - Ensure `requirements.txt` is in BoxMachiBox-API directory

2. **Deploy via Render Dashboard**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - Name: `boxmachibox-api`
     - Environment: `Python 3`
     - Region: Choose closest to users
     - Branch: `main`
     - Root Directory: `BoxMachiBox-API`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Add Environment Variables** (if needed)
   - Add any required environment variables in Render dashboard

### B. Deploy to Railway

**Steps:**

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select repository
4. Configure:
   - Root Directory: `BoxMachiBox-API`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Railway will auto-detect Python and install dependencies

### C. Deploy to Heroku

**Steps:**

1. Install Heroku CLI
   ```bash
   npm install -g heroku
   ```

2. Login and create app
   ```bash
   heroku login
   heroku create boxmachibox-api
   ```

3. Set up for subdirectory deployment
   ```bash
   git subtree push --prefix BoxMachiBox-API heroku main
   ```

4. Verify deployment
   ```bash
   heroku open
   heroku logs --tail
   ```

---

## 📊 3. Streamlit App Deployment

### Prerequisites
- Python 3.8+
- Required data files: `f1_PRODUCTION_READY.pkl`, CSV files

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app_production.py
```

### A. Deploy to Streamlit Cloud (Recommended)

**Steps:**

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: `Prabakaransr19/BoxMachiBox-`
   - Branch: `main`
   - Main file path: `app_production.py`
5. Click "Deploy"

**Note:** Ensure all required files are in the repository:
- `app_production.py`
- `requirements.txt`
- `f1_PRODUCTION_READY.pkl`
- `2025_final_standings.csv`
- `2026_driver_momentum.csv`

### B. Deploy to Heroku

```bash
# Create Procfile for Streamlit
echo "web: streamlit run app_production.py --server.port $PORT" > Procfile

# Deploy
heroku create boxmachibox-streamlit
git push heroku main
```

---

## 🐳 4. Docker Deployment (All Services)

### Create Docker Configurations

**Frontend Dockerfile** (`Dockerfile.frontend`):
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "start"]
```

**Backend Dockerfile** (`BoxMachiBox-API/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Streamlit Dockerfile** (`Dockerfile.streamlit`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app_production.py .
COPY *.pkl *.csv ./

EXPOSE 8501
CMD ["streamlit", "run", "app_production.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

**Docker Compose** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  backend:
    build:
      context: ./BoxMachiBox-API
      dockerfile: Dockerfile
    ports:
      - "8000:8000"

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
```

**Run with Docker Compose:**
```bash
docker-compose up --build
```

---

## 🌐 5. Production Considerations

### Frontend
- [ ] Update `NEXT_PUBLIC_API_URL` environment variable
- [ ] Configure proper domain/subdomain
- [ ] Enable analytics if needed
- [ ] Set up CDN for static assets
- [ ] Configure caching headers

### Backend
- [ ] Add proper CORS origins (update `allow_origins` in `main.py`)
- [ ] Set up database if needed
- [ ] Configure logging and monitoring
- [ ] Add rate limiting
- [ ] Set up SSL/TLS
- [ ] Create health check endpoints

### Streamlit
- [ ] Ensure all data files are available
- [ ] Configure secrets if needed
- [ ] Set up caching properly
- [ ] Monitor memory usage

### Security
- [ ] Never commit `.env` files
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Implement authentication if needed
- [ ] Regular dependency updates
- [ ] Enable security headers

---

## 🔍 6. Verification Checklist

After deployment, verify:

### Frontend
- [ ] Homepage loads correctly
- [ ] All routes are accessible
- [ ] API calls work (if integrated)
- [ ] Images and assets load
- [ ] Mobile responsiveness
- [ ] Console has no errors

### Backend
- [ ] API is accessible
- [ ] Swagger docs work (`/docs`)
- [ ] All endpoints respond correctly
- [ ] CORS is configured properly
- [ ] Error handling works

### Streamlit
- [ ] App loads without errors
- [ ] All tabs are functional
- [ ] Charts render correctly
- [ ] Predictions work
- [ ] Data files are loaded

---

## 📝 7. Common Issues & Solutions

### Frontend Build Fails
**Issue:** Google Fonts not loading
**Solution:** Already fixed by removing Google Fonts import

**Issue:** Build errors with TypeScript
**Solution:** Already configured to ignore TypeScript errors

### Backend Won't Start
**Issue:** Port already in use
**Solution:** Use different port or kill existing process

**Issue:** Model file not found
**Solution:** Ensure `f1_model.pkl` exists in `BoxMachiBox-API/models/`

### Streamlit Issues
**Issue:** Missing data files
**Solution:** Ensure CSV and PKL files are in root directory

---

## 🔄 8. CI/CD Pipeline

### Current Setup
- GitHub Actions workflow for Next.js deployment
- Auto-deploys to GitHub Pages on push to `main`

### Recommended Additions
- Add tests before deployment
- Add linting checks
- Add backend deployment workflow
- Add Streamlit deployment workflow

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify all environment variables
3. Ensure all dependencies are installed
4. Check port availability
5. Review CORS settings (for API)

---

## 📚 Additional Resources

- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated:** January 2026
