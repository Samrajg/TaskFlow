import httpx
from app.config import settings
import asyncio

_http_client = None

def get_http_client():
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=30.0, limits=httpx.Limits(max_connections=100, max_keepalive_connections=20))
    return _http_client

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
        payload = {"sql": query, "params": params}
        client = get_http_client()
        response = await client.post(self.base_url, headers=self.headers, json=payload)
        if not response.is_success:
            raise Exception(f"DB Error: {response.status_code} {response.text}")
        data = response.json()
        if data["success"]:
            return data["result"][0]["results"]
        else:
            raise Exception(f"DB Error: {data['errors']}")

    async def execute_write(self, query: str, params: list = None):
        if params is None:
            params = []
        payload = {"sql": query, "params": params}
        client = get_http_client()
        response = await client.post(self.base_url, headers=self.headers, json=payload)
        if not response.is_success:
            raise Exception(f"DB Error: {response.status_code} {response.text}")
        data = response.json()
        if data["success"]:
            return True
        else:
            raise Exception(f"DB Error: {data['errors']}")

def get_db():
    return Database()
