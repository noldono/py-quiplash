from threading import Thread

from flask import request
from gamedb import DuplicateUserIdError, NoSuchGameError

from .app import app, game_repository
from .errors import NotFoundError, ValidationError
from .props import *

active_games: dict[str, str] = {}


@app.route(f"{GAMES_PATH}", methods=["POST"])
def create_game():
    """
    Create a new (persistent) Game object.

    Sample POST:
    {
        "creator": "Nolan",
        "game_id": "XDFG",
        "creator_id": "435"
    }
    """

    if not request.is_json:
        raise ValidationError("request body must be JSON")

    input_data = request.get_json()
    creator = input_data.get(CREATOR)
    custom_id = input_data.get(GAME_ID)
    creator_id = input_data.get(CREATOR_ID)
    game = game_repository.create_game(creator=creator, players=[creator_id])

    if not creator or not creator_id:
        raise ValidationError("request must include a creator and their assigned ID")

    game_id = game.gid

    # Store the mapping of the custom_id to the game_id, this will allow players to easily reference it.
    active_games[custom_id] = game_id

    return {"game_id": game_id}, 201


@app.route(f"{GAMES_PATH}/<custom_id>", methods=['POST'])
def join_game(custom_id: str):
    """
    Adds a player to a game

    Sample POST:
    {
        "player_id": "466"
    }
    """
    try:
        input_data = request.get_json()
        game_id = active_games[custom_id]
        player_id = input_data[PLAYER_ID]
        game = game_repository.find_game(game_id)  # Just make sure the game exists
        players = game_repository.games.find_one({'gid': game_id}).get("players", [])

        if player_id in players:
            raise DuplicateUserIdError
        game_repository.games.find_one_and_update({'gid': game_id}, {"$push": {"players": player_id}})

    except NoSuchGameError as e:
        return NotFoundError(f"{e}")
    except DuplicateUserIdError as e:
        return ValidationError(f"{e}")

    return {"game_id": "random id"}, 200
