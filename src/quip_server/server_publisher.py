from threading import Lock

from gamecomm.server import GameConnection

from quip_model.events import *
from .server_ui.server_gui import ServerGUI


class GamePublisher:

    def __init__(self, ui: ServerGUI):
        self._connections: dict[int, GameConnection] = {}
        self._lock = Lock()
        self.ui = ui

    def _handle_join_event(self, event: PlayerJoinEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        target_players = [event.player_num]
        return message, target_players

    def _handle_leave_event(self, event: PlayerLeaveEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        # Remove connection
        with self._lock:
            self._connections.pop(event.player_num)
        target_players = list(self._connections.keys())
        self.ui.event_queue.put(event)
        return message, target_players

    def _handle_nickname_event(self, event: PlayerNicknameEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        message["name"] = event.name
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_vip_event(self, event: PlayerVIPEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        target_players = [event.player_num]
        return message, target_players

    def _handle_vip_leave_event(self, event: VIPLeaveEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        target_players = list()
        return message, target_players

    def _handle_response_event(self, event: PlayerResponseEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_vote_event(self, event: PlayerVoteEvent, message: dict) -> tuple[dict, list[int]]:
        message["nickname"] = event.nickname
        message["vote"] = event.vote
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_round_start_event(self, event: RoundStartedEvent, message: dict) -> tuple[dict, list[int]]:
        message["round_num"] = event.round_num
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_distribute_prompt_event(self, event: DistributePromptEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_num"] = event.player_num
        message["prompt_0"] = event.prompt_0
        message["prompt_1"] = event.prompt_1
        message["prompt_0_id"] = event.prompt_0_id
        message["prompt_1_id"] = event.prompt_1_id
        target_players = [event.player_num]
        return message, target_players

    def _handle_begin_voting_event(self, event: BeginVotingEvent, message: dict) -> tuple[dict, list[int]]:
        message["round"] = event.round
        target_players = list(self._connections.keys())
        self.ui.event_queue.put(event)
        return message, target_players

    def _handle_prompt_vote_event(self, event: BeginPromptVotingEvent, message: dict) -> tuple[dict, list[int]]:
        message["prompt"] = event.prompt.prompt
        message["prompt_id"] = event.prompt.id

        player_0_id = event.prompt.player_ids[0]
        player_1_id = event.prompt.player_ids[1]

        message["response_0"] = event.prompt.responses[player_0_id]
        message["response_1"] = event.prompt.responses[player_1_id]

        target_players = list(self._connections.keys())
        if player_0_id in target_players:
            target_players.remove(player_0_id)

        if player_1_id in target_players:
            target_players.remove(player_1_id)

        self.ui.event_queue.put(event)

        return message, target_players

    def _handle_end_prompt_vote_event(self, event: EndPromptVotingEvent, message: dict) -> tuple[dict, list[int]]:
        message["player_0_name"] = event.player_0_name
        message["player_0_voter_names"] = event.player_0_voter_names
        message["player_0_points_awarded"] = event.player_0_points_awarded
        message["player_1_name"] = event.player_1_name
        message["player_1_voter_names"] = event.player_1_voter_names
        message["player_1_points_awarded"] = event.player_1_points_awarded
        message["tie"] = event.tie
        message["winner"] = event.winner
        message["quiplasher"] = event.quiplasher
        self.ui.event_queue.put(event)
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_scoreboard_event(self, event: ScoreboardEvent, message: dict) -> tuple[dict, list[int]]:
        message["names_in_order"] = event.names_in_order
        message["points_in_order"] = event.points_in_order
        target_players = list(self._connections.keys())
        self.ui.event_queue.put(event)
        return message, target_players

    def _handle_client_end_prompt_voting_event(self, event: ClientEndPromptVotingEvent, message: dict) -> tuple[
        dict, list[int]]:
        message["data"] = None
        target_players = list(self._connections.keys())
        return message, target_players

    def _handle_nickname_already_in_use_event(self, event, message):
        target_players = [event.player_num]
        message["data"] = None
        return message, target_players

    def _event_to_dict(self, event: GameEvent) -> tuple[dict, list[int]]:
        message = {"event": event.__class__.__name__}
        match event:
            case PlayerJoinEvent():
                return self._handle_join_event(event, message)
            case PlayerLeaveEvent():
                return self._handle_leave_event(event, message)
            case PlayerNicknameEvent():
                return self._handle_nickname_event(event, message)
            case PlayerVIPEvent():
                return self._handle_vip_event(event, message)
            case VIPLeaveEvent():
                return self._handle_vip_leave_event(event, message)
            case PlayerResponseEvent():
                return self._handle_response_event(event, message)
            case PlayerVoteEvent():
                return self._handle_vote_event(event, message)
            case RoundStartedEvent():
                return self._handle_round_start_event(event, message)
            case DistributePromptEvent():
                return self._handle_distribute_prompt_event(event, message)
            case BeginVotingEvent():
                return self._handle_begin_voting_event(event, message)
            case BeginPromptVotingEvent():
                return self._handle_prompt_vote_event(event, message)
            case EndPromptVotingEvent():
                return self._handle_end_prompt_vote_event(event, message)
            case ScoreboardEvent():
                return self._handle_scoreboard_event(event, message)
            case ClientEndPromptVotingEvent():
                return self._handle_client_end_prompt_voting_event(event, message)
            case NicknameAlreadyExistsEvent():
                return self._handle_nickname_already_in_use_event(event, message)

    def add_subscriber(self, player_num: int, connection: GameConnection):
        with self._lock:
            self._connections[player_num] = connection

    def publish(self, event: GameEvent):

        with self._lock:
            # make a "defensive" copy
            connections = list(self._connections.values())
            connections_with_keys = self._connections

        message, target_player_nums = self._event_to_dict(event)
        for player_num in target_player_nums:
            connections_with_keys[player_num].send(message)

