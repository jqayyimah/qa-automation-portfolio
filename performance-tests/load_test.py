
from locust import HttpUser, task, between
import os

BASE_PATH = os.getenv("BASE_PATH", "/api/v1")
EMAIL = os.getenv("EMAIL", "user@example.com")
PASSWORD = os.getenv("PASSWORD", "Passw0rd!")

class AuthUser(HttpUser):
    wait_time = between(0.5, 1.5)  # seconds
    token = None

    def on_start(self):
        # Login once per user to get a token
        with self.client.post(
            f"{BASE_PATH}/auth/login",
            json={"email": EMAIL, "password": PASSWORD},
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    self.token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
                    if not self.token:
                        resp.failure("No token in response")
                except Exception as e:
                    resp.failure(f"JSON parse error: {e}")
            else:
                resp.failure(f"Login failed: {resp.status_code} {resp.text[:200]}")

    @task(3)
    def ping_public(self):
        self.client.get(f"{BASE_PATH}/health", name="GET /health")

    @task(5)
    def get_profile(self):
        # Example protected endpoint; change to your API path
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.client.get(f"{BASE_PATH}/users/me", headers=headers, name="GET /users/me")
