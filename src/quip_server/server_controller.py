import threading
from logging import getLogger

from gamecomm.server import GameConnection, ConnectionClosed

from quip_model.events import *
from quip_model.exceptions import *
from quip_model.game_master import GameMaster
from quip_model.response import PromptResponse, VoteResponse
from .server_ui.server_gui import ServerGUI

logger = getLogger(__name__)

RECV_TIMEOUT = 1


class GameController:

    def __init__(self, connection: GameConnection, player_num: int, game: GameMaster, ui: ServerGUI):
        self._connection = connection
        self._player_num = player_num
        self._game = game
        self.ui = ui

    def _handle_start_message(self, message):
        num_players = len(self._game.players.players)
        if num_players < 3:
            raise NotEnoughPlayers(f"Need at least 3 players to start the game, only have {num_players}.")
        game_thread = threading.Thread(target=self._game.play_round)
        game_thread.start()
        self.ui.event_queue.put(RoundStartedEvent(1))

    def _handle_nickname_message(self, message):
        nickname = message["content"]
        self._game.accept_new_player(self._player_num, nickname)
        self.ui.event_queue.put(PlayerNicknameEvent(self._player_num, nickname))

    def _handle_responses_message(self, message):
        player_num = message["player_num"]
        self._game.observer(PlayerResponseEvent(player_num))

        # Set the responses inside the player objects
        prompt_0_id = message["prompt_0_id"]
        prompt_1_id = message["prompt_1_id"]
        response_0 = message["response_0"]
        response_1 = message["response_1"]
        player = self._game.players.get_player_by_id(player_num)
        prompt_0 = self._game.prompts.get_prompt_by_id(prompt_0_id)
        prompt_1 = self._game.prompts.get_prompt_by_id(prompt_1_id)
        prompt_0.receive_response(PromptResponse(prompt_0_id, player_num, response_0))
        prompt_1.receive_response(PromptResponse(prompt_1_id, player_num, response_1))
        player.current_prompts = [prompt_0, prompt_1]

        with self._game.responses_received_lock:
            self._game.responses_received += 1

        self.ui.event_queue.put(PlayerResponseEvent(player_num))

    def _handle_vote_message(self, message):
        # Extract player number, prompt id, and player vote from message
        player_num = message["player_num"]
        prompt_id = message["prompt_id"]
        player_vote = message["vote"]

        # Get player and prompt objects
        player = self._game.players.get_player_by_id(player_num)
        prompt = self._game.prompts.get_prompt_by_id(prompt_id)

        # Publish vote event with player name and vote
        self._game.observer(PlayerVoteEvent(player.name, player_vote))

        # Receive vote
        vote = VoteResponse(prompt_id, player_num, player_vote)
        prompt.receive_vote(vote)

        # Update votes received in game model:
        with self._game.votes_received_lock:
            self._game.votes_received += 1

    def _handle_leave_message(self, message):
        player_num = message["player_num"]
        self._game.remove_player(player_num)
        self._game.observer(PlayerLeaveEvent(player_num))

    def _log_and_send_error_message(self, error, message):
        logger.error(error)

    def _handle_request(self, message):
        """
        Handles the incoming request's JSON message. 'message' is a JSON formatted message.
        """
        print(message)
        try:
            match message["type"]:
                case "start":
                    self._handle_start_message(message)
                case "nickname":
                    self._handle_nickname_message(message)
                case "responses":
                    self._handle_responses_message(message)
                case "vote":
                    self._handle_vote_message(message)
                case "leave":
                    self._handle_leave_message(message)
                case _:
                    pass

        except (PlayerNameAlreadyInUse, PlayerResponseError, PlayerNicknameError, NotEnoughPlayers) as error:
            self._log_and_send_error_message(error, message)
            return

        # If no errors occurred, send an OK message
        self._connection.send({"status": "ok"})

    def run(self):
        while True:
            try:
                message = self._connection.recv(RECV_TIMEOUT)
                self._handle_request(message)
            except ConnectionClosed:
                break
            except TimeoutError:
                pass
