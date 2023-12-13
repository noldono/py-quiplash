import logging

from gamecomm.server import GameConnection

from quip_model.game_master import GameMaster
from .server_controller import GameController
from .server_publisher import GamePublisher
from .server_ui.server_gui import ServerGUI

logger = logging.getLogger(__name__)


class GameServer:

    def __init__(self, game_id: str, ui: ServerGUI):
        self._game_id = game_id
        self._publisher = GamePublisher(ui)
        self._game = GameMaster(observer=self._publisher.publish)
        self.ui = ui

    def handle_connection(self, connection: GameConnection):
        if len(self._game.players) >= 8 or self._game.is_playing:
            message = { "event": "GameFullEvent", "game-id": self._game_id }
            connection.send(message)
            return
        
        player_num = self._game.add_connection()
        controller = GameController(connection, player_num, self._game, self.ui)
        self._publisher.add_subscriber(player_num, connection)
        controller.run()
