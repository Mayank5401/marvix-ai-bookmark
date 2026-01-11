# Marvix AI – Article Bookmark Tool

A FastAPI-based backend application that allows users to:
- Search Wikipedia articles
- Save favorite articles
- Auto-tag articles
- Edit tags
- Authenticate users

## Tech Stack
- Backend: FastAPI, SQLAlchemy
- Database: CockroachDB (Postgres-compatible)
- Frontend: HTML, CSS, JavaScript
- Auth: JWT
- Deployment-ready with Docker

## How to Run Locally

### Backend
```bash
uvicorn app.main:app --reload
