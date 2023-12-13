"""
File: exceptions.py
Author: Jason Dech (jasonmdech)
Created: 29 November 2023
Purpose: Define custom exceptions used by the server program.
"""


# Player Exceptions
class PlayerException(Exception):
    pass


class PlayerNameAlreadyInUse(PlayerException):
    pass


class PlayerDoesNotExist(PlayerException):
    pass


class PlayerNicknameError(PlayerException):
    pass


class PlayerResponseError(PlayerException):
    pass


class PlayerVoteError(PlayerException):
    pass


class NotEnoughPlayers(PlayerException):
    pass


# PlayerList Exceptions
class PlayerListException(Exception):
    pass


class PlayerListEmpty(PlayerListException):
    pass


class PlayerNotFound(PlayerListException):
    pass


# PromptList Exceptions
class PromptListException(Exception):
    pass


class PromptListEmpty(PromptListException):
    pass


class PromptNotFound(PromptListException):
    pass
