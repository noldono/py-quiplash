from threading import Lock

from gamecomm.server import GameConnection, WsGameListener

from .server import GameServer
from .server_ui.server_gui import *

LOCAL_IP = "0.0.0.0"
LOCAL_PORT = 10020

logger = logging.getLogger(__name__)


class GameListener:

    def __init__(self, ui):
        self._lock = Lock()
        self._game_servers: dict[str, GameServer] = {}
        self._ui = ui

    def _find_or_create_game_server(self, game_id: str) -> GameServer:
        with self._lock:
            if game_id not in self._game_servers:
                self._game_servers[game_id] = GameServer(game_id, self._ui)
            return self._game_servers[game_id]

    def handle_connection(self, connection: GameConnection):
        self._find_or_create_game_server(connection.gid).handle_connection(connection)

    def run(self):
        ws_listener = WsGameListener(LOCAL_IP, LOCAL_PORT, on_connection=self.handle_connection)
        ws_listener.run()
