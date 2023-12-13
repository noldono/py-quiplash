import queue
import sys
from queue import Queue
from threading import Timer

import pygame
import pyautogui
from requests.exceptions import *

from .api_client import UsersApiClient, GamesApiClient
from .client_controller import GameController, GameClient
from .ui_elements.elements import Button, TextBox
from .ui_elements.screens import Screen

BACKGROUND_COLOR = (70, 60, 90)
TEXT_COLOR = (255, 255, 255)


class GameUI:

    def __init__(self, url, api_url):
        self.points = None
        self.win = None
        self.client = None
        self.username = None
        self.prompts = list[str]()
        self.id = int()
        self.prompt_0_id = int()
        self.prompt_1_id = int()
        self.prompt_vote_id = int()
        self.response_0 = None
        self.response_1 = None
        self.prompt_to_vote = str
        self.font = None
        self.previous_screen = None
        self.current_screen: Screen = Screen.HOME
        self.vip = False
        self.url = url
        self.api_url = api_url
        self.controller = None
        self.api = UsersApiClient(self.api_url)
        self.games_api = GamesApiClient(self.api_url)
        self.login_uid = None
        self.login_pass = None
        self.error = None
        self.client_running = False

        pygame.init()

        super(GameUI, self).__init__()
        self.event_queue = Queue()

        # Set up the display
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quiplash")

        # Set up the clock
        self.clock = pygame.time.Clock()

        # Set up response timer
        self.response_timer = Timer(59, self.force_response)

        # The back button
        self.back_button = Button(20, 20, 20, 20, "<", (50, 50, 50), (140, 140, 140), text_color=(255, 255, 255),
                                  action=self.on_back)

        # HOME WIDGETS
        self.home_play_button = Button(300, 250, 200, 50, "Play", (50, 50, 50), (100, 100, 100),
                                       self.on_play)
        self.home_login_button = Button(300, 310, 200, 50, "Login", (50, 50, 50), (100, 100, 100),
                                        self.on_login_clicked)
        self.home_create_acc_button = Button(300, 370, 200, 50, "Create Account", (50, 50, 50), (100, 100, 100),
                                             self.on_create_acc_clicked)

        # NICKNAME SCREEN WIDGETS
        self.nick_text_box = TextBox(300, 250, 200, 30, character_limit=10, callback=self.submit_nickname)
        self.nick_submit_button = Button(300, 320, 200, 50, "Play", (50, 50, 50), (100, 100, 100),
                                         self.on_button_click, [self.nick_text_box])

        # VIP SCREEN WIDGETS
        self.vip_start_button = Button(300, 320, 200, 50, "Start Game", (50, 50, 50), (100, 100, 100),
                                       self.start_game)

        # RESPONSE 0 SCREEN WIDGETS
        self.resp0_text_box = TextBox(220, 250, 350, 30, character_limit=25, callback=self.record_response_0)
        self.resp0_submit_button = Button(300, 320, 200, 50, "Submit", (50, 50, 50), (100, 100, 100),
                                          self.on_button_click, [self.resp0_text_box])

        # RESPONSE 1 SCREEN WIDGETS
        self.resp1_text_box = TextBox(220, 250, 350, 30, character_limit=25, callback=self.record_response_1)
        self.resp1_submit_button = Button(300, 320, 200, 50, "Submit", (50, 50, 50), (100, 100, 100),
                                          self.on_button_click, [self.resp1_text_box])

        # VOTING SCREEN WIDGETS
        self.vote_button_0 = Button(500, 200, 200, 50, "Vote", (50, 50, 50), (100, 100, 100),
                                    self.vote_resp_0)
        self.vote_button_1 = Button(500, 320, 200, 50, "Vote", (50, 50, 50), (100, 100, 100),
                                    self.vote_resp_1)

        # LOGIN SCREEN WIDGETS
        self.login_uid_text_box = TextBox(300, 250, 200, 30, character_limit=15, callback=self.record_uid)
        self.login_password_text_box = TextBox(300, 320, 200, 30, callback=self.record_pass)
        self.login_submit_button = Button(300, 400, 200, 50, "Login", (50, 50, 50), (100, 100, 100),
                                          self.submit_login_info,
                                          [self.login_uid_text_box, self.login_password_text_box])

        # CREATE ACCOUNT SCREEN WIDGETS
        self.create_acc_uid_text_box = TextBox(300, 250, 200, 30, callback=self.record_uid)
        self.create_acc_password_text_box = TextBox(300, 320, 200, 30, callback=self.record_pass)
        self.create_acc_nickname_text_box = TextBox(300, 385, 200, 30, character_limit=10, callback=self.set_nickname)
        self.create_acc_submit_button = Button(300, 450, 200, 50, "Create Account", (50, 50, 50), (100, 100, 100),
                                               self.submit_account_info,
                                               [self.create_acc_uid_text_box, self.create_acc_password_text_box,
                                                self.create_acc_nickname_text_box])

        self.controller = GameController(self)
        self.client = GameClient(self.url, on_event=self.controller.handle_event)

        # Flag to indicate whether the UI thread should keep running
        self.running = True

    def run(self):
        self.font = pygame.font.Font(None, 36)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                # Only listen for events relevant to the current screen
                match self.current_screen:
                    case Screen.HOME:
                        self.home_login_button.handle_event(event)
                        self.home_create_acc_button.handle_event(event)
                        self.home_play_button.handle_event(event)
                    case Screen.NICKNAME:
                        self.nick_submit_button.handle_event(event)
                        self.nick_text_box.handle_event(event)
                        self.back_button.handle_event(event)
                    case Screen.VIP_SCREEN:
                        self.vip_start_button.handle_event(event)
                    case Screen.RESPONSE_0:
                        self.resp0_text_box.handle_event(event)
                        self.resp0_submit_button.handle_event(event)
                    case Screen.RESPONSE_1:
                        self.resp1_text_box.handle_event(event)
                        self.resp1_submit_button.handle_event(event)
                    case Screen.VOTING:
                        self.vote_button_0.handle_event(event)
                        self.vote_button_1.handle_event(event)
                    case Screen.LOGIN:
                        self.login_submit_button.handle_event(event)
                        self.login_password_text_box.handle_event(event)
                        self.login_uid_text_box.handle_event(event)
                        self.back_button.handle_event(event)
                    case Screen.CREATE_ACCOUNT:
                        self.create_acc_nickname_text_box.handle_event(event)
                        self.create_acc_submit_button.handle_event(event)
                        self.create_acc_uid_text_box.handle_event(event)
                        self.create_acc_password_text_box.handle_event(event)
                        self.back_button.handle_event(event)

            # Poll the event queue for external events
            try:
                event = self.event_queue.get_nowait()
                self.handle_external_events(event)
                print(event)
            except queue.Empty:
                pass

            match self.current_screen:
                case Screen.HOME:
                    self.load_home_screen()
                case Screen.NICKNAME:
                    self.load_play_screen()
                case Screen.VIP_SCREEN:
                    self.load_vip_screen()
                case Screen.WAITING_SCREEN:
                    self.load_waiting_screen()
                case Screen.RESPONSE_0:
                    self.load_resp0_screen()
                case Screen.RESPONSE_1:
                    self.load_resp1_screen()
                case Screen.VOTING:
                    self.load_voting_screen()
                case Screen.LOGIN:
                    self.load_login_screen()
                case Screen.CREATE_ACCOUNT:
                    self.load_create_acc_screen()

        self.exit_game()

    def exit_game(self):
        self.client.send({"type": "leave", "player_num": self.id})
        self.client.stop()
        pygame.quit()
        sys.exit()

    def handle_external_events(self, event):
        event_type = event["event"]
        match event_type:
            case "PlayerVIPEvent":
                self.vip = True
                self.change_screen(Screen.VIP_SCREEN)
            case "DistributePromptEvent":
                self.prompts = [event["prompt_0"], event["prompt_1"]]
                self.change_screen(Screen.RESPONSE_0)
                self.response_timer.start()  # Start 60-second timer
            case "BeginPromptVotingEvent":
                self.response_timer.cancel()
                self.response_0 = event["response_0"]
                self.response_1 = event["response_1"]
                self.prompt_to_vote = event["prompt"]
                self.change_screen(Screen.VOTING)
            case "EndPromptVotingEvent":
                self.change_screen(Screen.WAITING_SCREEN)
            case "ScoreboardEvent":
                self.handle_scoreboard_event(event)
            case "NicknameAlreadyExistsEvent":
                self.change_screen(Screen.HOME)
                self.error = "Nickname already exists!"
                self.display_error()
            case "PlayerJoinEvent":
                if not self.vip:
                    self.change_screen(Screen.WAITING_SCREEN)
            case "GameFullEvent":
                self.change_screen(Screen.HOME)
                self.error = "The game is full!"
                self.display_error()

    def on_button_click(self):
        print("Button clicked!")

    def submit_nickname(self, nickname):
        try:
            if nickname == "" and self.login_uid is not None:
                self.create_game(self.login_uid)
            elif nickname != "":
                self.create_game(nickname)
                self.username = nickname
            else:
                self.error = "You must specify a nickname since you're not logged in!"
                self.display_error()
                self.current_screen = Screen.HOME
                return
        except OSError:
            # If the server is already running, do nothing.
            pass

        # Launch the client
        if not self.client_running:
            self.controller.run(self.client)
            self.client_running = True

        name = nickname if nickname != "" else self.username
        self.client.send({"type": "nickname", "content": name})

    def submit_login_info(self):
        print("SUBMITTING LOGIN INFO")
        self.api.auth(self.login_uid, self.login_pass)
        try:
            result = self.api.login_user(f'/users/{self.login_uid}/login')
            if result[0]["authenticated"] == "True":
                self.username = self.login_uid
        except HTTPError as e:
            self.error = str(e)

        self.change_screen(Screen.HOME)

    def submit_account_info(self):
        self.api.auth(self.login_uid, self.login_pass)
        data = {
            "uid": self.login_uid,
            "password": self.login_pass,
            "full_name": "N/A",
            "nickname": self.username
        }
        try:
            self.api.create_user(data)
        except HTTPError as e:
            self.error = str(e)
            self.display_error()
        self.change_screen(Screen.HOME)

    def submit_scoring_info(self):
        try:
            win = 1 if self.win else 0
            _ = self.api.add_stats("both", self.points, f'/users/{self.login_uid}/custom', win)
        except HTTPError as e:
            self.error = str(e)
            self.display_error()

        self.change_screen(Screen.HOME)

    def create_game(self, creator):
        self.games_api.create_game(GamesApiClient.GAMES_PATH, creator=creator, creator_id=str(self.id))

    def record_response_0(self, response):
        self.response_0 = response
        self.change_screen(Screen.RESPONSE_1)

    def record_response_1(self, response):
        self.response_1 = response
        data = {"type": "responses", "player_num": self.id,
                "prompt_0_id": self.prompt_0_id, "prompt_1_id": self.prompt_1_id,
                "response_0": self.response_0, "response_1": self.response_1}
        self.client.send(data)
        self.change_screen(Screen.WAITING_SCREEN)

    def on_play(self):
        self.change_screen(Screen.NICKNAME)

    def on_login_clicked(self):
        self.change_screen(Screen.LOGIN)

    def record_pass(self, pwd: str):
        self.login_pass = pwd

    def record_uid(self, uid: str):
        self.login_uid = uid

    def on_create_acc_clicked(self):
        self.change_screen(Screen.CREATE_ACCOUNT)

    def start_game(self):
        self.client.send({"type": "start"})

    def on_back(self):
        self.change_screen(self.previous_screen)

    def vote_resp_0(self):
        data = {"type": "vote", "player_num": self.id, "prompt_id": self.prompt_vote_id, "vote": 0}
        self.client.send(data)
        self.change_screen(Screen.WAITING_SCREEN)

    def vote_resp_1(self):
        data = {"type": "vote", "player_num": self.id, "prompt_id": self.prompt_vote_id, "vote": 1}
        self.client.send(data)
        self.change_screen(Screen.WAITING_SCREEN)

    def force_response(self):
        print("FORCEFULLY SUBMITTING RESPONSES")
        match self.current_screen:
            case Screen.RESPONSE_0:
                if self.handle_char_limit(self.resp0_text_box):
                    self.resp0_text_box.submit_text(self.resp0_text_box.text)
                    self.resp1_text_box.submit_text("")
                    self.change_screen(Screen.WAITING_SCREEN)
                else:
                    self.resp1_text_box.submit_text("")
                    self.change_screen(Screen.WAITING_SCREEN)
            case Screen.RESPONSE_1:
                if self.handle_char_limit(self.resp0_text_box):
                    self.resp1_text_box.submit_text(self.resp1_text_box.text)
                else:
                    self.resp1_text_box.submit_text("")

    def handle_char_limit(self, box: TextBox) -> bool:
        return len(box.text) < box.character_limit

    def load_home_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.home_play_button.draw(self.screen)
        self.home_login_button.draw(self.screen)
        self.home_create_acc_button.draw(self.screen)
        self.display_nickname()
        font = pygame.font.Font(None, 72)
        # Render text
        text = font.render("QUIPLASH", True, (0, 255, 6))  # Change the text and color as needed
        shadow = font.render("QUIPLASH", True, (36, 50, 50))
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))
        shadow_rect = text.get_rect(center=(self.width // 2 - 3, (self.height // 2) - 97))
        self.display_error()
        # Blit the text onto the screen
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_play_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.back_button.draw(self.screen)
        self.nick_text_box.draw(self.screen)
        self.nick_submit_button.draw(self.screen)
        self.display_nickname()
        # Render text
        text = self.font.render("Enter Display Name", True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_vip_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.vip_start_button.draw(self.screen)
        self.display_nickname()
        # Render text
        text = self.font.render("Start the Game When All Players Have Joined", True,
                                TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_waiting_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        # Render text
        text = self.font.render("STAND BY", True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))
        self.display_nickname()

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_login_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.back_button.draw(self.screen)
        self.display_nickname()
        small_font = pygame.font.Font(None, 24)
        # Render text
        text = self.font.render("Login To Your Account", True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))

        text2 = small_font.render("User ID", True, TEXT_COLOR)
        text2_rect = text2.get_rect(center=(self.width // 2, (self.height // 2) - 60))

        text3 = small_font.render("Password", True, TEXT_COLOR)
        text3_rect = text3.get_rect(center=(self.width // 2, (self.height // 2) + 10))

        self.login_uid_text_box.draw(self.screen)
        self.login_password_text_box.draw(self.screen)
        self.login_submit_button.draw(self.screen)

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(text3, text3_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_create_acc_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.back_button.draw(self.screen)
        self.display_nickname()
        small_font = pygame.font.Font(None, 24)
        # Render text
        text = self.font.render("Create Your Account", True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 200))

        text2 = small_font.render("User ID", True, TEXT_COLOR)
        text2_rect = text2.get_rect(center=(self.width // 2, (self.height // 2) - 60))

        text3 = small_font.render("Password", True, TEXT_COLOR)
        text3_rect = text3.get_rect(center=(self.width // 2, (self.height // 2) + 10))

        text4 = small_font.render("Nickname", True, TEXT_COLOR)
        text4_rect = text3.get_rect(center=(self.width // 2, (self.height // 2) + 75))

        self.create_acc_uid_text_box.draw(self.screen)
        self.create_acc_password_text_box.draw(self.screen)
        self.create_acc_submit_button.draw(self.screen)
        self.create_acc_nickname_text_box.draw(self.screen)

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(text3, text3_rect)
        self.screen.blit(text4, text4_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_resp0_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.display_nickname()
        # Render text
        text = self.font.render(self.prompts[0], True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))
        self.resp0_text_box.draw(self.screen)
        self.resp0_submit_button.draw(self.screen)

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_resp1_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.display_nickname()
        # Render text
        text = self.font.render(self.prompts[1], True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 100))
        self.resp1_text_box.draw(self.screen)
        self.resp1_submit_button.draw(self.screen)

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def load_voting_screen(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)  # Set background color as needed
        self.display_nickname()
        # Render text

        text = self.font.render(self.prompt_to_vote, True, TEXT_COLOR)  # Change the text and color as needed
        text_rect = text.get_rect(center=(self.width // 2, (self.height // 2) - 200))
        self.vote_button_0.draw(self.screen)
        self.vote_button_1.draw(self.screen)

        resp_font = pygame.font.Font(None, 24)
        resp0 = resp_font.render(self.response_0, True,
                                 TEXT_COLOR)  # Change the text and color as needed
        resp0_rect = resp0.get_rect(center=((self.width // 2) - 50, (self.height // 2) - 70))

        resp1 = resp_font.render(self.response_1, True,
                                 TEXT_COLOR)  # Change the text and color as needed
        resp1_rect = resp1.get_rect(center=((self.width // 2) - 50, (self.height // 2) + 50))

        # Blit the text onto the screen
        self.screen.blit(text, text_rect)
        self.screen.blit(resp0, resp0_rect)
        self.screen.blit(resp1, resp1_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def change_screen(self, new_screen: Screen):
        self.previous_screen = self.current_screen
        self.current_screen = new_screen

    def set_nickname(self, nickname):
        self.username = nickname

    def display_nickname(self):
        if self.username is not None:
            font = pygame.font.Font(None, 24)
            if self.api.authenticated():
                text = font.render(f'Logged in as: {self.login_uid}', True, TEXT_COLOR)
            else:
                text = font.render(f'Playing as guest: {self.username}', True, TEXT_COLOR)
            text_rect = text.get_rect(center=(self.width // 2, 10))
            self.screen.blit(text, text_rect)

    def display_error(self):
        if self.error:
            pyautogui.alert(self.error)
            self.error = None

    def handle_scoreboard_event(self, event):
        names = event["names_in_order"]
        points = event["points_in_order"]
        index = 0
        for i in range(len(names)):
            if self.username == names[i]:
                index = i

        self.points = points[index]
        if index == 0:
            self.win = True

        self.submit_scoring_info()
