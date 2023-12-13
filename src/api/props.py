from gamedb import User

# This module defines the property names used in JSON requests and responses
# and provides functions used to produce JSON from objects such as User.

CODE = "code"
CREATION_DATE = "creation_date"
CUSTOM = "custom"
FULL_NAME = "full_name"
HREF = "href"
MESSAGE = "message"
NICKNAME = "nickname"
PASSWORD = "password"
UID = "uid"
AUTHENTICATED = "authenticated"
ATTRIBUTE = "attribute"
POINTS = "points"
WINS = "wins"

USERS_PATH = "/users"

# Game Related
GAMES_PATH = "/games"
GAME_ID = "game_id"
CREATOR = "creator"
CREATOR_ID = "creator_id"
PLAYER_ID = "player_id"


def user_to_dict(user: User) -> dict:
    """ Converts a User object to a dictionary which can be easily converted
        to JSON by Flask.

    Args:
        user (User): the user object to be converted

    Returns:
        dict: a dictionary containing those attributes of the User object
              that are relevant for an API client, along with some additional
              "links" that a client can use to manipulate the User object as
              a resource
    """
    data = {
        HREF: f"{USERS_PATH}/{user.uid}",
        PASSWORD: f"{USERS_PATH}/{user.uid}/password",
        UID: user.uid,
        CREATION_DATE: user.creation_date.astimezone().isoformat(),
    }
    if user.nickname is not None:
        data.update({NICKNAME: user.nickname})
    if user.full_name is not None:
        data.update({FULL_NAME: user.full_name})
    if user.custom is not None:
        data.update({CUSTOM: user.custom})
    return data
