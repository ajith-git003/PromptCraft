# PromptCraft Deployment Guide

## 🚀 Deployment Options

### Option 1: Docker Local Testing

#### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum

#### Steps
```bash
# Navigate to project root
cd promptcraft

# Build and run all services
docker-compose up --build

# Access:
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Stop services
```bash
docker-compose down
```

---

### Option 2: Railway (Recommended for Beginners)

#### Why Railway?
- Free tier available ($5 credit/month)
- Automatic HTTPS
- Easy GitHub integration
- No credit card required for trial

#### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial deployment"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy Backend**
- Go to [railway.app](https://railway.app)
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository
- Railway auto-detects Dockerfile
- Set root directory: `/backend`
- Add environment variable: `PORT=8000`
- Deploy!

3. **Deploy Frontend**
- Create new service in same project
- Set root directory: `/frontend`
- Update environment: `REACT_APP_API_URL=<backend-url>`
- Deploy!

**Cost**: Free tier (~500 hours/month)

---

### Option 3: Render

#### Why Render?
- Free tier (slower than Railway)
- Automatic SSL
- Good for prototypes

#### Steps

1. **Backend (Web Service)**
- Go to [render.com](https://render.com)
- New → Web Service
- Connect GitHub repo
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Instance Type: Free

2. **Frontend (Static Site)**
- New → Static Site
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `build`

**Cost**: Free (with spin-down on inactivity)

---

### Option 4: AWS (Production-Grade)

#### Services Used
- **ECS (Elastic Container Service)** - Run Docker containers
- **ECR (Elastic Container Registry)** - Store Docker images
- **ALB (Application Load Balancer)** - Route traffic
- **RDS** (Optional) - PostgreSQL database
- **CloudFront** - CDN for frontend

#### Cost Estimate
- ~$20-50/month for small traffic
- Scales with usage

#### Steps (High-Level)

1. **Build and push images**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t promptcraft-backend ./backend
docker tag promptcraft-backend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/promptcraft-backend:latest

# Push
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/promptcraft-backend:latest
```

2. **Create ECS Task Definitions**
3. **Configure Load Balancer**
4. **Set up Auto Scaling**

---

### Option 5: Google Cloud Platform (GCP) - Cloud Run

#### Why Cloud Run?
-   **Serverless**: Pay only when code runs
-   **Scalable**: Scales to zero automatically
-   **Free Tier**: Generous free tier (2M requests/month)

#### Steps

1.  **Install Google Cloud SDK**
    -   Download and install `gcloud` CLI.
    -   Run `gcloud init` to log in.

2.  **Deploy Backend**
    ```bash
    cd backend
    gcloud run deploy promptcraft-backend --source . --region us-central1 --allow-unauthenticated
    ```
    -   Note the URL provided (e.g., `https://promptcraft-backend-xyz.a.run.app`).

3.  **Deploy Frontend**
    -   Update `frontend/.env` with the backend URL.
    -   Deploy frontend to Cloud Run (requires Dockerfile) OR Firebase Hosting (recommended for static sites).
    
    **Using Firebase Hosting (Easier for React):**
    ```bash
    cd frontend
    npm install -g firebase-tools
    firebase login
    firebase init
    # Select "Hosting", "Create new project", "build" as public directory
    npm run build
    firebase deploy
    ```

---

## 📊 Deployment Comparison

| Platform | Cost | Setup Time | Best For |
|----------|------|------------|----------|
| **Railway** | Free-$20/mo | 10 min | MVPs, demos |
| **Render** | Free-$15/mo | 15 min | Side projects |
| **Heroku** | $7+/mo | 10 min | Quick deploys |
| **AWS ECS** | $20-100+/mo | 2-4 hours | Production apps |
| **DigitalOcean** | $5-50/mo | 1-2 hours | Cost-conscious |

---

## 🔐 Environment Variables

### Backend
```env
ENVIRONMENT=production
LOG_LEVEL=info
ALLOWED_ORIGINS=https://yourfrontend.com
```

### Frontend
```env
REACT_APP_API_URL=https://your-backend-api.com
```

---

## 🛠 Production Checklist

- [ ] Environment variables configured
- [ ] CORS origins restricted
- [ ] HTTPS enabled
- [ ] Health checks working
- [ ] Error logging configured
- [ ] Rate limiting added
- [ ] Database backups (if using DB)
- [ ] Monitoring setup (Sentry/LogRocket)
- [ ] Domain configured
- [ ] CDN enabled for frontend

---

## 🔍 Monitoring & Debugging

### Check logs
```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Railway
# View in dashboard under "Logs" tab
```

### Health checks
```bash
# Backend
curl http://localhost:8000/

# Frontend
curl http://localhost/health
```

---

## 📈 Next Steps for Scaling

1. **Add Redis** for caching
2. **Add PostgreSQL** for persistence
3. **Implement CDN** (CloudFlare/AWS CloudFront)
4. **Add monitoring** (Prometheus + Grafana)
5. **Set up CI/CD** (GitHub Actions)
6. **Horizontal scaling** (Multiple containers)
