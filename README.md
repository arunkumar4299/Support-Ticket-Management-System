# Support Ticket Management System – Full Stack

Backend: FastAPI + SQLAlchemy + PostgreSQL + Alembic + JWT
Frontend: React + TypeScript + Vite

## Run backend
1. Create PostgreSQL database.
2. Copy `.env.example` to `.env` and update credentials.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run migrations:
   `alembic upgrade head`
5. Start:
   `uvicorn app.main:app --reload`

Swagger: http://127.0.0.1:8000/docs

## Run frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

Frontend: http://localhost:5173

The frontend is a clean starter UI wired to the REST API through Axios. Update `VITE_API_URL` if the backend uses another URL.

## Roles
ADMIN, SUPPORT_AGENT, CUSTOMER

## Notes
This repository is structured so business logic lives in services/repositories instead of route handlers. The backend includes authentication, RBAC, tickets, comments, attachments, categories, notifications, dashboard, SLA helpers, audit logging, migrations, tests, and API documentation scaffolding.
