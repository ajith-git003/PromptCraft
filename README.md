# PromptCraft – AI Prompt Analysis & Optimization Platform

PromptCraft is a full-stack web application that analyzes AI prompts and provides structured feedback to help users improve prompt clarity and effectiveness.

This project is built as a **production-style MVP**, focusing on clean architecture, explainable NLP logic, and real-world deployment.

---

## What This Project Does

- Analyzes user-written AI prompts using NLP techniques  
- Identifies unclear or weak parts of a prompt  
- Provides actionable suggestions for improvement  
- Generates a clearer, optimized version of the prompt  
- Delivers feedback in real time through a web interface  

---

## Key Features

- **Prompt Analysis**
  - Evaluates clarity, specificity, structure, and completeness
  - Detects ambiguous or missing information

- **Issue Detection**
  - Highlights weak areas in prompts
  - Explains why improvements are needed

- **Suggestions & Optimization**
  - Provides practical rewriting suggestions
  - Returns an improved version of the prompt

- **API-First Architecture**
  - REST APIs built with FastAPI
  - OpenAPI (Swagger) documentation included

- **Production Deployment**
  - Frontend deployed on Vercel
  - Backend deployed on Render
  - Dockerized services for consistency

---

## Tech Stack

**Backend**
- FastAPI  
- spaCy  
- Pydantic  
- Uvicorn  

**Frontend**
- React  
- Tailwind CSS  
- Nginx  

**DevOps**
- Docker & Docker Compose  
- GitHub Actions  
- Render & Vercel  

---

## Architecture Overview

Browser
↓
React Frontend (Vercel)
↓
FastAPI Backend (Render)
↓
spaCy NLP Pipeline


- Frontend and backend are deployed as independent services  
- Backend is stateless and API-driven  

---

## Project Structure

```text
PromptCraft/
├── backend/
│   ├── app/
│   │   ├── main.py                 # API routes
│   │   ├── models.py               # Pydantic schemas
│   │   └── prompt_analysis.py      # NLP analysis logic
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── docker-compose.yml
├── ARCHITECTURE.md
├── DEPLOYMENT.md
└── README.md
```

---

## Live Application

Frontend:
https://prompt-craft-z.vercel.app/

---

## Design Notes

- The current analysis engine uses **rule-based NLP techniques**
- This approach was chosen for **explainability and transparency**
- The architecture allows future integration of transformer-based models without breaking the API

---

## Future Improvements

- Add structured prompt scoring
- Store prompt history using a database
- Introduce user authentication
- Integrate transformer-based semantic analysis
- Add caching, monitoring, and rate limiting

---

## License

This project is intended for educational and portfolio purposes.

---
