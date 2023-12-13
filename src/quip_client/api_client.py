import json
import logging

import requests
from requests.auth import HTTPBasicAuth
from requests.compat import urljoin

from .errors import AuthenticationRequiredError

logger = logging.getLogger(__name__)


class UsersApiClient:
    USERS_PATH = "/users"

    def __init__(self, base_url):
        self.base_url = base_url
        self._auth = None

    def auth(self, uid: str, password: str):
        self._auth = HTTPBasicAuth(uid, password)

    def create_user(self, data: dict) -> dict:
        url = urljoin(self.base_url, self.USERS_PATH)
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")

    def add_stats(self, attr: str, points: int, href: str, wins: int = 0) -> dict:
        url = urljoin(self.base_url, href)
        data = {
            "attribute": attr,
            "points": points,
            "wins": wins
        }
        response = requests.put(url, json=data)
        return response.json()

    def fetch_user(self, href) -> dict:
        url = urljoin(self.base_url, href)
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")

    def delete_user(self, href):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, href)
        response = requests.delete(url, auth=self._auth)
        response.raise_for_status()

    def update_user(self, href, data, etag):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, href)
        response = requests.put(url, json=data, headers={"If-Match": etag}, auth=self._auth)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")

    def change_password(self, href: str, password: str):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, href)
        response = requests.put(url, data=password, auth=self._auth)
        response.raise_for_status()

    def login_user(self, href: str):
        if not self._auth:
            raise AuthenticationRequiredError()
        url = urljoin(self.base_url, href)
        response = requests.get(url, auth=self._auth)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")

    def authenticated(self) -> bool:
        return self._auth is not None


class GamesApiClient:
    GAMES_PATH = "/games"

    def __init__(self, base_url):
        self.base_url = base_url
        self._auth = None

    def create_game(self, href, creator: str, creator_id: str):
        url = urljoin(self.base_url, href)
        data = {
            "creator": creator,
            "creator_id": creator_id,
            "game_id": "placeholder"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json(), response.headers.get("ETag")
