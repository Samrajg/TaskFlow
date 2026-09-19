import os

backend_requirements_append = """passlib[bcrypt]
httpx
pyjwt
python-multipart
"""
with open("backend/requirements.txt", "a") as f:
    f.write(backend_requirements_append)

config_py_content = """import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "TaskFlow API")
    app_env: str = os.getenv("APP_ENV", "development")
    database_name: str = os.getenv("DATABASE_NAME", "taskflow")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    
    # Cloudflare Config for DB
    cloudflare_account_id: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    cloudflare_database_id: str = os.getenv("CLOUDFLARE_DATABASE_ID", "")
    cloudflare_api_token: str = os.getenv("CLOUDFLARE_API_TOKEN", "")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-key-for-dev")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"

settings = Settings()
"""
with open("backend/app/config.py", "w") as f:
    f.write(config_py_content)


database_py_content = """import httpx
from app.config import settings
import json

class Database:
    def __init__(self):
        self.account_id = settings.cloudflare_account_id
        self.db_id = settings.cloudflare_database_id
        self.api_token = settings.cloudflare_api_token
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.db_id}/query"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    async def execute(self, query: str, params: list = None):
        if params is None:
            params = []
        async with httpx.AsyncClient() as client:
            payload = {"sql": query, "params": params}
            response = await client.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data["success"]:
                return data["result"][0]["results"]
            else:
                raise Exception(f"DB Error: {data['errors']}")

    async def execute_write(self, query: str, params: list = None):
        if params is None:
            params = []
        async with httpx.AsyncClient() as client:
            payload = {"sql": query, "params": params}
            response = await client.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data["success"]:
                return True
            else:
                raise Exception(f"DB Error: {data['errors']}")

def get_db():
    return Database()
"""
with open("backend/app/database.py", "w") as f:
    f.write(database_py_content)


main_py_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.health import router as health_router
from app.api.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the TaskFlow daily task management system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
"""
with open("backend/app/main.py", "w") as f:
    f.write(main_py_content)

print("Backend initial files written")
