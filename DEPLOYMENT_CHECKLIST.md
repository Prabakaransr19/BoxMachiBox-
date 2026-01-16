# Pre-Deployment Checklist

Use this checklist before deploying BoxMachiBox to production.

## 📋 General Prerequisites

- [ ] All code is committed and pushed to the repository
- [ ] Latest changes are merged to the `main` branch
- [ ] `.env` files are configured (never commit these!)
- [ ] All dependencies are up to date
- [ ] Build succeeds locally without errors

## 🌐 Frontend Deployment (Next.js)

### For Vercel Deployment
- [ ] Vercel account is set up
- [ ] Repository is connected to Vercel
- [ ] Build command: `npm run build`
- [ ] Output directory: `.next`
- [ ] Node.js version: 20.x
- [ ] Environment variables configured (if any):
  - [ ] `NEXT_PUBLIC_API_URL` (if connecting to backend)
- [ ] Test deployment on preview URL
- [ ] Check all routes work correctly
- [ ] Verify mobile responsiveness

### For GitHub Pages Deployment
- [ ] GitHub Pages is enabled in repository settings
- [ ] `next.config.gh-pages.mjs` is used for build
- [ ] GitHub Actions workflow is active
- [ ] Permissions set: `contents: read`, `pages: write`, `id-token: write`
- [ ] Deployment succeeds without errors
- [ ] Site is accessible at: `https://prabakaransr19.github.io/BoxMachiBox-/`
- [ ] **Note:** Some dynamic features won't work in static export

### For Netlify Deployment
- [ ] Netlify account is set up
- [ ] Repository is connected to Netlify
- [ ] Build command: `npm run build`
- [ ] Publish directory: `.next`
- [ ] Node.js version: 20.x
- [ ] Environment variables configured

## 🔧 Backend Deployment (FastAPI)

### For Render Deployment
- [ ] Render account is set up
- [ ] Repository is connected to Render
- [ ] Service type: Web Service
- [ ] Environment: Python 3.11
- [ ] Root directory: `BoxMachiBox-API`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Health check path: `/`
- [ ] Environment variables configured (if any)
- [ ] Test API endpoints at `/docs`
- [ ] Verify CORS is configured for frontend domain

### For Railway Deployment
- [ ] Railway account is set up
- [ ] Repository is connected to Railway
- [ ] Root directory: `BoxMachiBox-API`
- [ ] Start command configured
- [ ] Environment variables set
- [ ] Health checks passing

### For Heroku Deployment
- [ ] Heroku CLI installed
- [ ] Heroku account is set up
- [ ] `Procfile` exists in `BoxMachiBox-API/`
- [ ] `runtime.txt` specifies Python version (if needed)
- [ ] App is created: `heroku create boxmachibox-api`
- [ ] Code is pushed: `git subtree push --prefix BoxMachiBox-API heroku main`

## 📊 Streamlit Dashboard Deployment

### For Streamlit Cloud
- [ ] Streamlit Cloud account is set up
- [ ] Repository is connected
- [ ] Main file path: `app_production.py`
- [ ] Required files are present:
  - [ ] `requirements.txt`
  - [ ] `f1_PRODUCTION_READY.pkl`
  - [ ] `2025_final_standings.csv`
  - [ ] `2026_driver_momentum.csv`
- [ ] Python version: 3.11
- [ ] App deploys without errors
- [ ] All tabs and features work

## 🐳 Docker Deployment

### Local Docker
- [ ] Docker and Docker Compose installed
- [ ] `docker-compose.yml` is configured
- [ ] All Dockerfiles are present:
  - [ ] `Dockerfile.frontend`
  - [ ] `BoxMachiBox-API/Dockerfile`
  - [ ] `Dockerfile.streamlit`
- [ ] Run: `./deploy-docker.sh` or `docker-compose up --build`
- [ ] Services start without errors
- [ ] All ports are accessible:
  - [ ] Frontend: http://localhost:3000
  - [ ] Backend: http://localhost:8000
  - [ ] Streamlit: http://localhost:8501

### Cloud Docker (AWS ECS, Google Cloud Run, etc.)
- [ ] Container registry is set up
- [ ] Images are built and pushed
- [ ] Services are configured with correct ports
- [ ] Environment variables are set
- [ ] Health checks are configured
- [ ] Load balancer is set up (if needed)
- [ ] SSL/TLS certificates are configured

## 🔒 Security Checklist

- [ ] No secrets in source code
- [ ] Environment variables are used for sensitive data
- [ ] `.env` files are in `.gitignore`
- [ ] CORS is properly configured (not `allow_origins=["*"]` in production)
- [ ] HTTPS is enabled
- [ ] API rate limiting is configured (if needed)
- [ ] Security headers are set
- [ ] Dependencies are up to date
- [ ] No known vulnerabilities (run `npm audit` and `pip check`)

## 🧪 Testing Checklist

### Frontend
- [ ] Homepage loads correctly
- [ ] All navigation links work
- [ ] Standings page displays data
- [ ] Driver info pages load
- [ ] Analyze page is functional
- [ ] Insights page works
- [ ] Responsive on mobile devices
- [ ] No console errors

### Backend
- [ ] API root endpoint (`/`) returns status
- [ ] Swagger docs (`/docs`) are accessible
- [ ] `/api/drivers` returns driver list
- [ ] `/api/circuits` returns circuit list
- [ ] `/api/predict` endpoint works
- [ ] `/api/model/info` returns model data
- [ ] CORS headers are present
- [ ] Error handling works correctly

### Streamlit
- [ ] App loads without errors
- [ ] All four tabs work:
  - [ ] Predict Race
  - [ ] Driver Analysis
  - [ ] 2026 Outlook
  - [ ] Model Info
- [ ] Predictions generate results
- [ ] Charts render correctly
- [ ] Data is displayed properly

## 📈 Monitoring & Maintenance

- [ ] Set up error tracking (Sentry, LogRocket, etc.)
- [ ] Configure uptime monitoring
- [ ] Set up analytics (Google Analytics, Plausible, etc.)
- [ ] Create backup plan for data
- [ ] Document rollback procedure
- [ ] Set up automated alerts
- [ ] Plan for regular updates

## 🚀 Go-Live Checklist

- [ ] All tests pass
- [ ] Performance is acceptable
- [ ] Load testing completed (if expecting high traffic)
- [ ] Documentation is up to date
- [ ] Deployment guide is accurate
- [ ] Team is informed of go-live
- [ ] Rollback plan is ready
- [ ] Monitoring is active
- [ ] Support plan is in place

## ✅ Post-Deployment

- [ ] Verify all services are running
- [ ] Test all critical user flows
- [ ] Check error rates in logs
- [ ] Monitor performance metrics
- [ ] Update DNS if needed
- [ ] Announce launch
- [ ] Monitor user feedback
- [ ] Schedule first maintenance window

---

**Last Updated:** January 2026

**Need Help?** See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.
