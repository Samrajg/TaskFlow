import os
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
