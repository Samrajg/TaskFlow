# TaskFlow Backend

## Setup

1. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run FastAPI:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
