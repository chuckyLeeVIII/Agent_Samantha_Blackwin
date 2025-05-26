import base64
import json
import urllib.request
from typing import List, Dict, Optional


class SurrealDBClient:
    """Minimal SurrealDB client using the HTTP API."""

    def __init__(self, host: str = "http://localhost:8000", namespace: str = "test", database: str = "test", user: str = "root", password: str = "root"):
        self.host = host.rstrip('/')
        self.namespace = namespace
        self.database = database
        self.user = user
        self.password = password

    def _request(self, sql: str) -> List[Dict]:
        data = sql.encode("utf-8")
        req = urllib.request.Request(f"{self.host}/sql", data=data)
        req.add_header("NS", self.namespace)
        req.add_header("DB", self.database)
        auth_bytes = f"{self.user}:{self.password}".encode("utf-8")
        auth_header = base64.b64encode(auth_bytes).decode("ascii")
        req.add_header("Authorization", f"Basic {auth_header}")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def log_conversation(self, question: str, answer: str) -> Optional[List[Dict]]:
        sql = f"CREATE conversation SET question = '{question}', answer = '{answer}'"
        try:
            return self._request(sql)
        except Exception:
            return None

    def fetch_conversations(self) -> Optional[List[Dict]]:
        sql = "SELECT * FROM conversation ORDER BY time DESC LIMIT 10"
        try:
            return self._request(sql)
        except Exception:
            return None
