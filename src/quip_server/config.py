import os

LOCAL_IP = os.environ.get("LOCAL_IP", "127.0.0.1")
WS_LISTENER_PORT = os.environ.get("WS_LISTENER_PORT", "10020")

ENABLE_AUTH = os.environ.get("ENABLE_AUTH")
TOKEN_ISSUER_URI = os.environ.get("TOKEN_ISSUER_URI", "urn:ece4564:token-issuer")
PUBLIC_KEY_FILE = os.environ.get("PUBLIC_KEY_FILE", "public_key.pem")
