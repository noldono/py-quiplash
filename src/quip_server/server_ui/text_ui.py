"""
File: text_ui.py
Author: Jason Dech (jasonmdech)
Created: 30 November 2023
Purpose: Establish a simple event-based server text UI.
"""

import logging
import os
import sys

from src.quip_model.player import *

logger = logging.getLogger(__name__)


class ServerTextUI:
    def __init__(self):
        self.players_ready: list[str] = list()
        self.players: dict[int, str] = dict()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_last_line(self):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')

    def show_title_screen(self):
        self.clear_screen()
        print("Welcome to Quiplash!")

    def show_player_join_screen(self):
        print("Waiting for players to join...")

    def player_nickname(self, num: int, name: str):
        print(f"Player {name} has joined.")
        self.players[num] = name
        if len(self.players) < 2:
            self.player_VIP(num)

    def player_VIP(self, num: int):
        print(f"{self.players[num]} is the VIP.")

    def player_leave(self, num: int):
        print(f"Player {self.players[num]} has left the game.")
        del self.players[num]

    def show_prompt_responding_screen(self):
        self.clear_screen()
        self.players_ready.clear()
        print("Please answer the two prompts sent to your device.\n")

    def update_on_screen_timer(self, time: int):
        self.clear_last_line()
        self.clear_last_line()
        print(f"Time remaining: {time} seconds.")
        print(f"Players responded: {self.players_ready}")

    def show_prompt_for_voting(self, responses: list[str]):
        print(f"Response 1: {responses[0]}")
        print(f"Response 2: {responses[1]}\n")

    def reveal_prompt_authors(self, player_1_name: str, player_2_name: str):
        print(f"Response 1 written by {player_1_name}")
        print(f"Response 2 written by {player_2_name}")

    def reveal_votes(self, prompt_1_votes: list[str], prompt_2_votes: list[str]):
        print(f"Votes for Response 1: {prompt_1_votes}")
        print(f"Votes for Response 2: {prompt_2_votes}")

    def quiplash(self, nickname: str, bonus: int):
        print(f"{nickname} gets a quiplash! This earns {bonus} bonus points.")

    def reveal_prompt_points(self, points_0: int, points_1: int):
        print(f"Scores: {points_0}, {points_1}")

    def reveal_winner_bonus(self, nickname: str, points: int):
        print(f"{nickname} receives the win bonus of {points} points.")

    def reveal_scoreboard(self, players: PlayerList):
        players.sort()
        place = 1
        self.clear_screen()
        print("Scoreboard:")
        for p in players:
            print(f"{place}. {p.name}: {p.points}")
            place += 1
