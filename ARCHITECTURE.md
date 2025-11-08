# PromptCraft Architecture

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                           ↓                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER / CDN                       │
│                    (Railway / AWS ALB)                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴──────────────────┐
        ↓                                      ↓
┌──────────────────┐                 ┌──────────────────┐
│   FRONTEND       │                 │    BACKEND       │
│   Container      │    HTTP/JSON    │   Container      │
│                  │ ──────────────→ │                  │
│ - React SPA      │                 │ - FastAPI        │
│ - Tailwind CSS   │                 │ - spaCy NLP      │
│ - Nginx          │                 │ - Pydantic       │
│                  │                 │ - Uvicorn        │
│ Port: 80         │                 │ Port: 8000       │
└──────────────────┘                 └──────────────────┘
                                              ↓
                                     ┌──────────────────┐
                                     │  NLP Models      │
                                     │                  │
                                     │ - en_core_web_sm │
                                     │ - Custom rules   │
                                     └──────────────────┘
```

---

## 📦 Container Architecture

### **Frontend Container**
```
docker build → Node.js Builder → React Build → Nginx Server
     ↓              ↓                ↓              ↓
  Source      Compile JS/CSS    Static files    Serve HTTP
  (2GB)         (500MB)          (15MB)         (50MB final)
```

**Optimization**: Multi-stage build reduces image size by 97%!

### **Backend Container**
```
docker build → Python Base → Install Deps → Copy Code → Run Server
     ↓              ↓             ↓             ↓           ↓
  Base Image    System libs   Python pkgs    App code   Uvicorn
  (150MB)       (+50MB)       (+200MB)       (+10MB)    (Running)
```

---

## 🔄 Request Flow

### **Prompt Analysis Request**

```
1. User enters prompt in React UI
   └─→ Form submission event

2. Frontend sends POST request
   └─→ axios.post('/analyze', {prompt: '...'})
   └─→ http://backend:8000/analyze

3. Backend receives request
   ├─→ Pydantic validates JSON schema
   ├─→ Extracts prompt text
   └─→ Calls analyze_prompt()

4. Analysis Engine processes
   ├─→ Tokenizes text (spaCy)
   ├─→ Calculates scores (heuristics)
   ├─→ Detects issues (rules)
   └─→ Generates suggestions

5. Backend returns JSON response
   └─→ {analysis: {...}, optimized_prompt: '...'}

6. Frontend updates UI
   ├─→ Renders score badges
   ├─→ Displays issues list
   └─→ Shows suggestions
```

---

## 🗂️ Project Structure

```
promptcraft/
│
├── backend/                    # Python FastAPI service
│   ├── app/
│   │   ├── main.py            # API routes & CORS
│   │   ├── models.py          # Pydantic schemas
│   │   └── prompt_analysis.py # NLP logic
│   ├── Dockerfile             # Backend container config
│   ├── requirements.txt       # Python dependencies
│   └── .dockerignore
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   └── Navbar.js
│   │   ├── pages/
│   │   │   └── Home.js
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│   ├── public/
│   ├── Dockerfile             # Frontend container config
│   ├── nginx.conf             # Web server config
│   ├── package.json           # Node dependencies
│   └── .dockerignore
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
│
├── docker-compose.yml         # Multi-container orchestration
├── DEPLOYMENT.md              # Deployment guide
├── QUICKSTART.md              # Quick start guide
└── ARCHITECTURE.md            # This file
```

---

## 🔧 Technology Stack

### **Frontend**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **React 19** | UI framework | Component reusability, virtual DOM |
| **Tailwind CSS** | Styling | Utility-first, fast development |
| **Axios** | HTTP client | Promise-based, interceptors |
| **React Router** | Navigation | SPA routing |
| **Nginx** | Web server | Production-grade, efficient |

### **Backend**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **FastAPI** | API framework | Async, auto-docs, type safety |
| **Uvicorn** | ASGI server | High performance, async support |
| **Pydantic** | Data validation | Runtime validation, type hints |
| **spaCy** | NLP library | Fast, production-ready |
| **Python 3.11** | Language | Latest features, performance |

### **DevOps**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Docker** | Containerization | Consistent environments |
| **Docker Compose** | Orchestration | Local development |
| **GitHub Actions** | CI/CD | Free, GitHub integration |
| **Railway** | Deployment | Easy, free tier |

---

## 🔐 Security Model

### **1. API Security**
```python
# CORS Configuration
allow_origins = ["https://yourfrontend.com"]  # Whitelist
allow_methods = ["GET", "POST"]                # Limited methods
allow_headers = ["Content-Type"]               # Specific headers
```

### **2. Input Validation**
```python
class PromptRequest(BaseModel):
    prompt: str  # Type validation
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if len(v) > 10000:  # Length limit
            raise ValueError('Prompt too long')
        return v
```

### **3. Container Security**
- Non-root user in production
- Minimal base images (Alpine/Slim)
- No secrets in images (use env vars)
- Regular security updates

### **4. Network Security**
```yaml
networks:
  promptcraft-network:
    driver: bridge  # Isolated network
```

---

## 📈 Scalability Considerations

### **Current Architecture**
- **Vertical Scaling**: Increase container resources
- **Horizontal Scaling**: Multiple container replicas
- **Stateless**: No session state in containers

### **Future Enhancements**

#### **Phase 1: Caching**
```
User → Frontend → Backend → Redis Cache → NLP Engine
                      ↑                        ↓
                      └────── Cache Hit ───────┘
```

#### **Phase 2: Load Balancing**
```
             Load Balancer
                  ↓
     ┌────────────┼────────────┐
     ↓            ↓            ↓
Backend-1    Backend-2    Backend-3
```

#### **Phase 3: Microservices**
```
API Gateway
    ↓
    ├─→ Analysis Service (spaCy)
    ├─→ Optimization Service (GPT-4)
    ├─→ Database Service (PostgreSQL)
    └─→ Cache Service (Redis)
```

---

## 🔍 Monitoring & Observability

### **Current**
- Health check endpoints
- Docker container logs
- Platform-native monitoring

### **Production Additions**
```
Application
    ↓
Logging → Centralized Logs (ELK Stack)
    ↓
Metrics → Prometheus → Grafana
    ↓
Tracing → Jaeger (distributed tracing)
    ↓
Errors → Sentry (error tracking)
```

---

## 🧪 Testing Strategy

### **Unit Tests**
```python
# Backend
def test_analyze_prompt():
    result = analyze_prompt("Test prompt")
    assert result.overall_score > 0
```

### **Integration Tests**
```python
# API tests
def test_analyze_endpoint():
    response = client.post("/analyze", json={"prompt": "..."})
    assert response.status_code == 200
```

### **E2E Tests**
```javascript
// Frontend with Cypress
cy.visit('/')
cy.get('textarea').type('Test prompt')
cy.get('button').click()
cy.contains('Analysis Results')
```

---

## 🚀 Deployment Flow

```
Developer
    ↓
git push origin main
    ↓
GitHub Actions Triggered
    ↓
    ├─→ Run Tests
    ├─→ Build Docker Images
    ├─→ Security Scan
    └─→ Deploy to Railway
         ↓
    Live Production
```

---

## 💡 Design Decisions

### **Why FastAPI over Flask?**
- **Performance**: 3x faster (async support)
- **Type Safety**: Automatic validation
- **Documentation**: Auto-generated OpenAPI
- **Modern**: Python 3.11+ features

### **Why Nginx over Node serve?**
- **Performance**: C-based, optimized for static files
- **Features**: Gzip, caching, security headers
- **Production**: Industry standard
- **Size**: Smaller image footprint

### **Why Docker over VMs?**
- **Speed**: Seconds to start vs minutes
- **Size**: MBs vs GBs
- **Portability**: Run anywhere
- **Efficiency**: Share host OS kernel

### **Why Railway over AWS?**
- **Simplicity**: Zero config deployment
- **Cost**: Free tier for MVPs
- **Time**: 5 minutes vs 2 hours
- **Learning**: Fewer concepts upfront

---

## 🎯 Performance Metrics

### **Target SLAs**
- **Latency**: < 200ms (95th percentile)
- **Availability**: > 99.9% uptime
- **Throughput**: 100 requests/second
- **Error Rate**: < 0.1%

### **Current Bottlenecks**
1. **spaCy model loading**: ~2s startup
2. **No caching**: Repeated analysis
3. **Single thread**: Limited concurrency

### **Optimizations Applied**
✅ Docker layer caching
✅ Multi-stage builds
✅ Gzip compression
✅ Static asset caching
✅ Async request handling

---

## 📚 Further Reading

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [React Production Build](https://reactjs.org/docs/optimizing-performance.html)
- [spaCy Production](https://spacy.io/usage/production)
- [12-Factor App](https://12factor.net)

---

**This architecture is designed to scale from prototype to production!** 🚀
