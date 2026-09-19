# TaskFlow

Smart Daily Task Management and Productivity Tracking System

## Technology Stack

- **Frontend:** Next.js + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python
- **Database:** Cloudflare D1
- **Deployment:** Vercel + Render + Cloudflare

## Project Structure

- `frontend/` - Contains the Next.js web application.
- `backend/` - Contains the FastAPI Python application.
- `database/` - Contains database schema and migrations for Cloudflare D1.

## Local Development

### Frontend
1. Open terminal and enter frontend folder:
   ```powershell
   cd frontend
   ```
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Run the development server:
   ```powershell
   npm run dev
   ```
   (Expected to run on http://localhost:3000)

### Backend
1. Open terminal and enter backend folder:
   ```powershell
   cd backend
   ```
2. Create virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate virtual environment (Windows PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
4. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run FastAPI:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   (Expected to run on http://localhost:8000)
   - Health check: http://localhost:8000/api/health
   - Swagger docs: http://localhost:8000/docs

### Database (Cloudflare D1)
1. Install Wrangler globally (if not already installed):
   ```powershell
   npm install -g wrangler
   ```
2. Authenticate with Cloudflare:
   ```powershell
   wrangler login
   ```
3. Create the D1 database:
   ```powershell
   wrangler d1 create taskflow
   ```
4. Update `wrangler.toml` with your generated `database_id`.
5. Apply the schema:
   ```powershell
   wrangler d1 execute taskflow --file=database/schema.sql --remote
   ```
   (Or use `--local` for local development testing).
