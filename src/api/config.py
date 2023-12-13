import os

LOCAL_IP = os.environ.get("LOCAL_IP", "127.0.0.1")
API_PORT = os.environ.get("API_PORT", "10021")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/game-db")

TOKEN_ISSUER_URI = os.environ.get("TOKEN_ISSUER_URI", "urn:ece4564:token-issuer")
PRIVATE_KEY_FILE = os.environ.get("PRIVATE_KEY_FILE", "private_key.pem")
PRIVATE_KEY_PASSPHRASE = os.environ.get("PRIVATE_KEY_PASSPHRASE", "secret")

GAME_SERVER_HOST = os.environ.get("GAME_SERVER_HOST", "localhost")
GAME_SERVER_WS_SCHEME = os.environ.get("GAME_SERVER_WS_SCHEME", "ws")
GAME_SERVER_WS_PORT = os.environ.get("GAME_SERVER_WS_PORT", "10020")
