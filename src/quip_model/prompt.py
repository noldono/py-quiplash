"""
File: prompt.py
Author: Jason Dech (jasonmdech@vt.edu)
Created: 4 November 2023
"""
from .exceptions import *
from .response import *


class Prompt:
    """
    The Prompt class holds data such as the actual prompt sent to players as
    well as the players involved in the prompt and their involvement.
    """

    def __init__(self, id: int, prompt: str, player_ids: list[int]):
        """
        Creates a new Prompt. A freshly created prompt should only have the
        prompt itself as well as the players involved in it. All other
        variables are initialized to be empty strings or ints of zero.

        Args:
            id (int): The prompt's unique ID for the game.
            prompt (str): The prompt that the players will answer.
            player_ids (list[int]): The list of players assigned to the prompt.
        """
        self.id: int = id
        """ The prompt's unique ID for the game. """

        self.prompt: str = prompt
        """ The prompt that the players will answer. """

        self.player_ids: list[int] = player_ids
        """ The list of player ids assigned to the prompt. """

        self.responses = dict[int, str]()  # Player ID: Response
        """ Dictionary that holds the responses of each player """

        self.votes = dict[
            int, list[int]]()  # Player ID that submitted the response : List of player IDs that voted on the response
        """ Dictionary that holds the votes received by each response."""
        self.votes[player_ids[0]] = list[int]()
        self.votes[player_ids[1]] = list[int]()

    def receive_response(self, response: PromptResponse):
        """
        Stores a response from a player. If the player has already responded to
        the prompt, the new response is ignored.

        Parameters:
            player_id (int): The player who is responding to the prompt
        """
        if response.player_id not in self.player_ids:
            raise PlayerResponseError(f"Player {response.player_id} is not part of this prompt!")

        if response.player_id in self.responses.keys():
            raise PlayerResponseError(f"Player {response.player_id} has already responded!")

        if response.prompt_id != self.id:
            raise PlayerResponseError("This message was for a different prompt!")

        self.responses[response.player_id] = response.player_response

    def receive_vote(self, vote: VoteResponse):
        """
        Stores a vote from a player. If the player has already voted or is one
        of the players on the prompt, it is ignored.
        """
        if vote.prompt_id != self.id:
            raise PlayerVoteError(f"This vote was for a different prompt!")

        if vote.player_id in self.player_ids:
            raise PlayerVoteError(f"Player {vote.player_id} is not allowed to vote on their own prompt!")

        for l in self.votes.values():
            for player_id in l:
                if player_id == vote.player_id:
                    raise PlayerVoteError(f"Player {player_id} has already voted!")

        self.votes[self.player_ids[vote.vote]].append(vote.player_id)


class PromptList:
    """
    Custom list class to provide extra methods for referencing Prompts.
    """

    def __init__(self) -> None:
        """ Creates a new PromptList initialized with a blank list. """
        self.prompts: list[Prompt] = list()

    def get_prompt_by_id(self, prompt_id: int) -> Prompt:
        """
        Gets a prompt from a PromptList by the prompt's ID.

        Parameters:
            prompt_id (int): The id of the prompt to get.

        Returns:
            The specified prompt.
            If the prompt is not in the list, an exception is thrown.
        """
        if len(self.prompts) == 0:
            raise PromptListEmpty()

        for prompt in self.prompts:
            if prompt.id == prompt_id:
                return prompt

        raise PromptNotFound(f"Prompt {prompt_id} does not exist!")

    def __len__(self) -> int:
        return len(self.prompts)

    def append(self, prompt: Prompt) -> None:
        self.prompts.append(prompt)

    def __contains__(self, prompt: Prompt) -> bool:
        return prompt in self.prompts

    def __iter__(self):
        return iter(self.prompts)

    def __getitem__(self, index: int) -> Prompt:
        if isinstance(index, slice):
            return [self.prompts[i] for i in range(*index.indices(len(self.prompts)))]
        else:
            return self.prompts[index]

    def pop(self, index: int) -> Prompt:
        return self.prompts.pop(index)

    def has_prompt_by_id(self, prompt_id: int) -> bool:
        try:
            self.get_prompt_by_id(prompt_id)
            return True
        except PromptListException:
            return False

    def get_index_by_id(self, prompt_id: int) -> int:
        for index in range(len(self.prompts)):
            if self.prompts[index].id == prompt_id:
                return index

        raise PromptNotFound(f"Prompt {prompt_id} not found!")

    def remove_prompt_by_id(self, prompt_id: int) -> Prompt:
        index = self.get_index_by_id(prompt_id)
        return self.pop(index)
