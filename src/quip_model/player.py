from .exceptions import *
from .prompt import Prompt
from .response import PromptResponse


class Player:
    def __init__(self, id: int):
        self.id = id
        self.name: str = None
        self.points = 0
        self.ready = False
        self.current_prompts = list[Prompt]()
        self.is_vip = False

    def get_responses(self) -> list[PromptResponse]:
        responses = ["", ""]
        print(f"{self.name}, please answer these prompts:")
        print(f"Prompt 0: {self.current_prompts[0].prompt}")
        print(f"Prompt 1: {self.current_prompts[1].prompt}")
        responses[0] = input("Response 0: ")
        responses[1] = input("Response 1: ")
        results = [PromptResponse(self.current_prompts[0].id, self.name, responses[0]),
                   PromptResponse(self.current_prompts[1].id, self.name, responses[1])]
        return results

    def vote(self, prompt: str, responses: tuple[str, str]) -> int:
        """
        Returns:
            int: 0 if the first option, 1 if the second
        """
        print(f"Prompt: {prompt}")
        print(f"Response 0: {responses[0]}")
        print(f"Response 1: {responses[1]}")
        return int(input("Your vote (0 or 1): "))


class PlayerList:
    """
    Custom list class to provide extra methods for referencing Players.
    """

    def __init__(self) -> None:
        """ Creates a new PlayerList initialized with a blank list. """
        self.players: list[Player] = list()

    def get_player_by_id(self, player_id: int) -> Player:
        """
        Gets a player from a PlayerList by the player's ID.

        Parameters:
            player_id (int): The id of the player to get.

        Returns:
            The specified player.
            If the player is not in the list, an exception is thrown.
        """
        if len(self.players) == 0:
            raise PlayerListEmpty()

        for player in self.players:
            if player.id == player_id:
                return player

        raise PlayerNotFound(f"Player {player_id} does not exist!")

    def get_player_by_name(self, nickname: str) -> Player:
        """
        Gets a player from a PlayerList by the player's nickname.

        Parameters:
            nickname (str): The name of the player to get.

        Returns:
            The specified player.
            If the player is not in the list, an exception is thrown.
        """
        if len(self.players) == 0:
            raise PlayerListEmpty()

        for player in self.players:
            if player.name == nickname:
                return player

        raise PlayerNotFound(f"Player {nickname} does not exist!")

    def __len__(self) -> int:
        return len(self.players)

    def append(self, player: Player) -> None:
        self.players.append(player)

    def __contains__(self, player: Player) -> bool:
        return player in self.players

    def __iter__(self):
        return iter(self.players)

    def __getitem__(self, index: int) -> Player:
        if isinstance(index, slice):
            return [self.players[i] for i in range(*index.indices(len(self.players)))]
        else:
            return self.players[index]

    def pop(self, index: int) -> Player:
        return self.players.pop(index)

    def has_player_by_name(self, name: str) -> bool:
        try:
            self.get_player_by_name(name)
            return True
        except PlayerListException:
            return False

    def has_player_by_id(self, player_id: int) -> bool:
        try:
            self.get_player_by_id(player_id)
            return True
        except PlayerListException:
            return False

    def get_index_by_id(self, player_id: int) -> int:
        for index in range(len(self.players)):
            if self.players[index].id == player_id:
                return index

        raise PlayerNotFound(f"Player {player_id} not found!")

    def remove_player_by_id(self, player_id: int) -> Player:
        index = self.get_index_by_id(player_id)
        return self.pop(index)

    def sort(self):
        """ Sorts by score. """
        self.players.sort(key=lambda player: player.points, reverse=True)
