"""
File: responses.py
Author: Jason Dech (jasonmdech@vt.edu)
Created: 4 November 2023
Purpose: Define some structures to hold particular client responses.
"""


class PromptResponse:
    """
    The PromptResponse class is a way to represent client responses to prompts.
    These are created by the network handler and sent to the associated Prompt.
    """

    def __init__(self, prompt_id: int, player_id: int, player_response: str):
        """
        Creates a PromptResponse object with the response string, the associated 
        prompt id, and the player who sent it.

        Args:
            id (int): The prompt ID that this response is going to.
            player_name (str): The nickname of the player that responded.
            player_response (str): The player's response.
        """
        self.prompt_id = prompt_id
        """ The ID of the prompt that the player is responding to. """

        self.player_id = player_id
        """ The nickname that the response comes from. """

        self.player_response = player_response
        """ The player's response for the prompt. """


class VoteResponse:
    """
    The VoteResponse is a way to represent client votes. These are created by
    the network handler and passed to the associated Prompt.
    """

    def __init__(self, prompt_id: int, player_id: int, vote: int):
        """
        Creates a VoteResponse object with the prompt id, id of the player who
        cast the vote, and the vote itself.

        Parameters:
            prompt_id (int): The ID of the prompt.
            player_id (int): The ID of the player who voted.
            vote (int): The response that the player voted for (0 or 1).
        """
        self.prompt_id = prompt_id
        """ The ID of the prompt. """

        self.player_id = player_id
        """ The ID of the player who voted. """

        self.vote = vote
        """ The response that the player voted for (0 or 1). """
