from .client_ui import GameUI
import argparse
import sys

WS_URL = "ws://127.0.0.1:10020/ws/some-game-id"
API_URL = "http://127.0.0.1:10021"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game-url", default=WS_URL, help="URL for the game")
    parser.add_argument("-a", "--api-url", default=API_URL, help="URL for the api")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    ui = GameUI(url=args.game_url, api_url=args.api_url)
    ui.run()
