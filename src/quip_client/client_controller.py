from .client import GameClient
from quip_model.events import *


class GameController:

    def __init__(self, ui):
        self._ui = ui

    def handle_event(self, event):
        event_type = event["event"]
        self._ui.event_queue.put(event)
        if event_type == "PlayerJoinEvent":
            self._ui.id = event["player_num"]
            print(f"You are player {self._ui.id}")
        elif event_type == "PlayerLeaveEvent":
            pass
        elif event_type == "PlayerNicknameEvent":
            pass
        elif event_type == "PlayerChatEvent":
            pass
        elif event_type == "PlayerVIPEvent":
            print("You are the VIP!")
        elif event_type == "RoundStartedEvent":
            print("The Round is Starting!")
        elif event_type == "DistributePromptEvent":
            print(event["prompt_0"])
            print(event["prompt_1"])
            self._ui.prompt_0_id = event["prompt_0_id"]
            self._ui.prompt_1_id = event["prompt_1_id"]
        elif event_type == "BeginPromptVotingEvent":
            print("Voting has begun!")
            print(event)
            self._ui.prompt_vote_id = event["prompt_id"]

    def run(self, client: GameClient):
        client.start()
