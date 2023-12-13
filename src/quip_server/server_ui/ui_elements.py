"""
File: ui_elements.py
Author: Jason Dech (jasonmdech), Nolan Donovan (rndonovan)
Created: 2 December 2023
Purpose: Define classes for various elements of the GUI.
"""
from abc import ABC, abstractmethod

import pygame
from pygame import Rect
from pygame.event import Event
from pygame.font import Font
from pygame.surface import Surface

from quip_model.events import *
from quip_model.events import GameEvent

ColorRGB = tuple[int, int, int]
""" Custom type to represent an RGB color. """

Position = tuple[int, int]
""" Custom type to represent an x/y position on screen. """

BoxSize = tuple[int, int]
""" Custom type to represent the width and height of a box. """

SMALL_TEXT_SIZE = 16
""" Size of a 'Small' block of text. """

NORMAL_TEXT_SIZE = 24
""" Size of a 'Normal' block of text. """

LARGE_TEXT_SIZE = 36
""" Size of a 'Large' block of text. """

XL_TEXT_SIZE = 48
""" Size of an 'Extra Large' block of text. """

XXL_TEXT_SIZE = 72
""" Size of an 'Extra Extra Large' block of text. """

MEGA_TEXT_SIZE = 512
""" Size of a 'Mega' block of text. """

DEFAULT_SCREEN_COLOR = (255, 255, 255)
""" Default screen color is white. """

DEFAULT_TEXT_COLOR = (0, 0, 0)
""" Default text color is black. """

DEFAULT_BUTTON_COLOR = (0, 0, 0)
""" Default button color is black. """

DEFAULT_BUTTON_TEXT_COLOR = (255, 255, 255)
""" Default button text color is white. """

DEFAULT_BUTTON_HOVER_COLOR = (50, 50, 50)
""" Default button hover color is gray. """

DEFAULT_TIMER_POSITION = (30, 50)

UI_GAME_START_EVENT = pygame.event.custom_type()

VIP_GAME_START = pygame.event.custom_type()

TIMER_SECOND_PASSED = pygame.event.custom_type()

BEGIN_VOTING = pygame.event.custom_type()

SHOW_SCOREBOARD = pygame.event.custom_type()

JOIN_SCREEN_BG_COLOR = (67, 99, 63)

PROMPT_ANSWERING_SCREEN_BG_COLOR = (19, 81, 80)

VOTING_SCREEN_BG_COLOR = (60, 52, 83)

PROMPT_ANSWERING_SCREEN_BOTTOM_BAR_COLOR = (6, 41, 39)

SCOREBOARD_SCREEN_BG_COLOR = (31, 83, 113)

SCOREBOARD_NUMBER_COLOR = (16, 58, 91)

QUIP_TEXT_COLOR = (47, 130, 58)

LASH_TEXT_COLOR = (0, 109, 183)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

TEAL = (27, 200, 240)

SCORES_BOX_COLOR = (96, 142, 167)

# --- player colors ---
PURPLE = (139, 103, 255)
SALMON = (242, 110, 110)
CYAN = (3, 214, 254)
GREEN = (107, 201, 121)
ORANGE = (224, 155, 75)
YELLOW = (224, 218, 103)
PINK = (226, 125, 244)
BLUE = (95, 157, 241)

player_color_list = [
    PURPLE,
    SALMON,
    CYAN,
    GREEN,
    ORANGE,
    YELLOW,
    PINK,
    BLUE
]

player_color_mapping = dict[str, ColorRGB]()


class Button:
    """A class to represent a UI Button and handle all of its interactions."""

    def __init__(
            self,
            center_x: int,
            center_y: int,
            width: int,
            height: int,
            text: str,
            color: ColorRGB,
            hover_color: ColorRGB,
            action: Callable,
    ):
        """
        Creates a new button.

        Parameters:
            center_x (int): The center x coordinate of the button.
            center_y (int): The center y coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text that goes in the button.
            color (ColorRGB): The normal color of the button.
            hover_color (ColorRGB): The color of the button when the mouse is on it.
            action (callable): What the button does when clicked.
        """
        pygame.init()
        self.rect = Rect(0, 0, width, height)
        """ The rectangle that makes up the button. """

        self.rect.center = (center_x, center_y)
        """ Setting the center point of the rectangle. """

        self.text = text
        """ The text that goes in the button. """

        self.color = color
        """ The normal color of the button. """

        self.hover_color = hover_color
        """ The color of the button when the mouse is hovering over it. """

        self.action = action
        """ What the button does when it is clicked. """

        self.font = Font(None, NORMAL_TEXT_SIZE)
        """ The font that the button text is written in. """

        self.is_hovered = False
        """ Keeps track of if the mouse is hovering over the button. """

    def draw(self, surface: Surface):
        """
        Draws the button within the UI.

        Parameters:
            surface (Surface): The surface to draw the button on.
        """
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: Event, surface: Surface):
        """
        Handles various button events.

        Parameters:
            event (Event): The event to be handled.
        """
        if event.type == pygame.MOUSEMOTION:
            previous_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)

            # Check if the hover state changed
            if previous_hovered != self.is_hovered:
                self.draw(surface)
                pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.action()


class Text:
    """Class to represent a piece of text to be drawn to the screen."""

    def __init__(
            self, text: str, font_size: int, color: ColorRGB, center_position: Position
    ):
        """
        Creates a new text object.

        Parameters:
            text (str): The actual text to display.
            font_size (int): The size the text font.
            color (ColorRGB): The color of the text.
            center_position (Position): The center_position of the text.
        """
        self.text: str = text
        """ The displayed text. """

        self.font: Font = Font(None, font_size)
        """ The font of the displayed text. """

        self.color: ColorRGB = color
        """ The color of the displayed text. """

        self.center_position: Position = center_position
        """ The center position on screen where the text is displayed. """

        surface, rect = self.render_text()
        self.surface = surface
        self.rect = rect
        """ The surface created from rendering the text. """

    def render_text(self) -> tuple[Surface, Rect]:
        """Renders the given text in the given font."""
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.center_position)
        return text_surface, text_rect

    def draw(self, surface: Surface):
        """Draws the text to the given Surface."""
        surface.blit(self.surface, self.rect)

    def update_text(self, new_text: str, surface: Surface):
        """Updates text after the object has been drawn."""
        self.text = new_text
        self.surface, self.rect = self.render_text()
        self.draw(surface)
        pygame.display.update()


class TextInBox(Text):
    """A type of Text object that is drawn within a rectangle."""

    def __init__(
            self,
            text: str,
            font_size: int,
            color: ColorRGB,
            center_position: Position,
            box_size: BoxSize,
            box_color: ColorRGB,
            radius: int = None
    ):
        """
        Creates a new TextInBox.

        Parameters:
            text (str): The actual text to display.
            font_size (int): The size of the text font.
            color (ColorRGB): The color of the text.
            center_position (Position): The position of the text.
            box_size (BoxSize): The size of the box.
            box_color (ColorRGB): The color of the box.
        """
        super().__init__(text, font_size, color, center_position)
        self.box_size: BoxSize = box_size
        self.box_color: ColorRGB = box_color
        self.box_rect: Rect = self.calculate_box_rect()
        self.radius = radius

    def calculate_box_rect(self) -> Rect:
        """
        Creates a pygame rectangle based on the text's surface, object's
        position, and box's dimensions.
        """
        text_width, text_height = self.surface.get_size()
        box_width, box_height = self.box_size
        return Rect(
            self.center_position[0] - box_width / 2,
            self.center_position[1] - box_height / 2,
            box_width,
            box_height,
        )

    def clear(self, bg_color: ColorRGB, surface: Surface):
        self.box_color = bg_color
        self.update_text("", surface)

    def draw(self, surface: Surface):
        """Draws the object to the given surface."""
        if self.radius is not None:
            pygame.draw.rect(surface, self.box_color, self.box_rect, border_radius=self.radius)
        else:
            pygame.draw.rect(surface, self.box_color, self.box_rect)
        super().draw(surface)

    def update_text(self, new_text: str, surface: Surface):
        self.text = new_text
        self.surface, self.rect = super().render_text()
        self.draw(surface)
        pygame.display.update()


class UITimer:
    def __init__(self, duration: int, center_position: Position):
        self.duration = duration
        self.time_remaining = duration
        self.running = False

        self.text = TextInBox(
            str(self.time_remaining),
            XL_TEXT_SIZE,
            WHITE,
            center_position,
            (50, 50),
            BLACK,
        )

    def draw(self, surface: Surface):
        """Draw the timer's duration as a Text object."""
        self.text.draw(surface)

    def update_time(self, surface: Surface):
        """Decrement the time and update to the surface."""
        self.time_remaining -= 1
        self.text.update_text(str(self.time_remaining), surface)
        if self.time_remaining == 0:
            self.running = False

    def start(self):
        """Starts the timer."""
        pygame.time.set_timer(TIMER_SECOND_PASSED, 1000, self.time_remaining)
        self.running = True

    def stop(self):
        """Stops the timer."""
        self.running = False
        pygame.time.set_timer(TIMER_SECOND_PASSED, 0)
        self.time_remaining = self.duration

    def handle_event(self, event: Event, surface: Surface):
        if event.type == TIMER_SECOND_PASSED and self.running:
            self.update_time(surface)


class Screen(ABC):
    """
    Class to define all of the elements that a particular view of the game needs
    and some other useful functionality.
    """

    def __init__(
            self, bg_color: ColorRGB, texts: list[Text], ui_width: int, ui_height: int
    ):
        """
        Creates a new Screen.

        Parameters:
            bg_color (ColorRGB): The screen's background color.
            texts (list[Text]): List of text objects belonging to the screen.
        """
        self.bg_color: ColorRGB = bg_color
        self.texts: list[Text] = texts
        self.ui_width: int = ui_width
        self.ui_height: int = ui_height

    @abstractmethod
    def draw(self, surface: Surface):
        """Draws the screen to a given surface."""
        surface.fill(self.bg_color)
        for text in self.texts:
            text.draw(surface)

    @abstractmethod
    def handle_event(self, event: Event, surface: Surface):
        pass

    @abstractmethod
    def handle_external_event(self, event: GameEvent, surface: Surface):
        pass


class PlayerJoinScreen(Screen):
    """Contains everything necessary to the game's player join screen."""

    def __init__(self, bg_color: ColorRGB, ui_width: int, ui_height: int):
        """
        Creates a new Player Join Screen.

        Parameters:
            bg_color (ColorRGB): The screen's background color.
            ui_width (int): The screen's width.
            ui_height (int): The screen's height.
        """
        texts = [
            Text(
                "Waiting for players to join.",
                LARGE_TEXT_SIZE,
                DEFAULT_TEXT_COLOR,
                (ui_width // 2, 100),
            ),
            TextInBox(
                "QUIP",
                XXL_TEXT_SIZE,
                QUIP_TEXT_COLOR,
                (ui_width // 2 - 65, ui_height // 2 + 50),
                (125, 50),
                DEFAULT_SCREEN_COLOR
            ),
            TextInBox(
                "LASH",
                XXL_TEXT_SIZE,
                LASH_TEXT_COLOR,
                (ui_width // 2 + 65, ui_height // 2 + 50),
                (140, 50),
                DEFAULT_SCREEN_COLOR
            )
        ]

        super().__init__(bg_color, texts, ui_width, ui_height)

        box_size = (100, 100)
        box_spacing = 150
        vertical_offset = 50
        self.player_boxes = [
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[0],
                (
                    ui_width // 2,
                    int(ui_height / 2 - 1.5 * box_spacing + vertical_offset),
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[1],
                (
                    ui_width // 2 + box_spacing,
                    ui_height // 2 - box_spacing + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[2],
                (
                    int(ui_width / 2 + 1.5 * box_spacing),
                    ui_height // 2 + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[3],
                (
                    ui_width // 2 + box_spacing,
                    ui_height // 2 + box_spacing + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[4],
                (
                    ui_width // 2,
                    int(ui_height / 2 + 1.5 * box_spacing + vertical_offset),
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[5],
                (
                    ui_width // 2 - box_spacing,
                    ui_height // 2 + box_spacing + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[6],
                (
                    int(ui_width / 2 - 1.5 * box_spacing),
                    ui_height // 2 + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                player_color_list[7],
                (
                    ui_width // 2 - box_spacing,
                    ui_height // 2 - box_spacing + vertical_offset,
                ),
                box_size,
                (50, 50, 50),
            ),
        ]
        self.players: dict[int, str] = dict()

    def draw(self, surface: Surface):
        """Draw the screen."""
        super().draw(surface)
        for box in self.player_boxes:
            box.draw(surface)

    def handle_event(self, event: Event, surface: Surface):
        if event.type == VIP_GAME_START:
            return PromptAnsweringScreen(
                PROMPT_ANSWERING_SCREEN_BG_COLOR, self.ui_width, self.ui_height, self.players
            )

        return None

    def _handle_nickname_event(self, event: GameEvent, surface: Surface):
        self.players[event.player_num] = event.name

        # map player name to color
        player_color_mapping[event.name] = player_color_list[0]
        del player_color_list[0]

        for box in self.player_boxes:
            if len(box.text) != 0:
                continue

            box.update_text(event.name, surface)
            return

    def _handle_leave_event(self, event: PlayerLeaveEvent, surface: Surface):
        if event.player_num not in self.players.keys():
            return

        player_left_updated = False
        for i in range(len(self.player_boxes)):
            if not player_left_updated:
                if self.player_boxes[i].text != self.players[event.player_num]:
                    continue

                player_color_list.append(self.player_boxes[i].color)
                del player_color_mapping[self.players[event.player_num]]
                
                if i < 7:
                    self.player_boxes[i].color = self.player_boxes[i + 1].color
                    self.player_boxes[i].update_text(self.player_boxes[i + 1].text, surface)
                else:
                    self.player_boxes[i].color = player_color_list[0]
                    del player_color_list[0]
                    self.player_boxes[i].update_text("", surface)

                del self.players[event.player_num]
                player_left_updated = True
            elif i < 7:
                self.player_boxes[i].color = self.player_boxes[i + 1].color
                self.player_boxes[i].update_text(self.player_boxes[i + 1].text, surface)
            else:
                self.player_boxes[i].color = player_color_list[0]
                self.player_boxes[i].update_text("", surface)

    def handle_external_event(self, event: GameEvent, surface: Surface):
        match event:
            case PlayerNicknameEvent():
                self._handle_nickname_event(event, surface)
            case PlayerLeaveEvent():
                self._handle_leave_event(event, surface)
            case RoundStartedEvent():
                pygame.event.post(Event(VIP_GAME_START))
            case _:
                pass


class PromptAnsweringScreen(Screen):
    """The screen that appears when players are answering prompts."""

    def __init__(
            self, bg_color: ColorRGB, ui_width: int, ui_height: int, players: dict[int, str]
    ):
        """Creates a new prompt answering screen."""
        texts = [
            Text(
                "Write your answers on your device now!",
                LARGE_TEXT_SIZE,
                DEFAULT_TEXT_COLOR,
                (ui_width // 2, ui_height - 250),
            ),
            TextInBox(
                "",
                NORMAL_TEXT_SIZE,
                PROMPT_ANSWERING_SCREEN_BOTTOM_BAR_COLOR,
                (ui_width // 2, ui_height - 100),
                (ui_width, 200),
                PROMPT_ANSWERING_SCREEN_BOTTOM_BAR_COLOR
            )
        ]
        super().__init__(bg_color, texts, ui_width, ui_height)

        self.timer = UITimer(60, DEFAULT_TIMER_POSITION)

        self.players = players

        self.player_boxes = self._init_player_boxes()

    def _init_player_boxes(self) -> list[TextInBox]:
        num_players = len(self.players)
        box_spacing = 50
        box_size = (100, 100)
        box_color = (50, 50, 50)
        total_box_width = num_players * box_size[0] + (num_players - 1) * box_spacing

        starting_center_position_x = (self.ui_width - total_box_width) // 2 + box_size[
            0
        ] // 2

        player_boxes = list[TextInBox]()

        for box_index, player_name in enumerate(self.players.values()):
            center_position_x = starting_center_position_x + box_index * (
                    box_size[0] + box_spacing
            )
            center_position_y = self.ui_height - 100
            player_boxes.append(
                TextInBox(
                    player_name,
                    NORMAL_TEXT_SIZE,
                    player_color_mapping[player_name],
                    (center_position_x, center_position_y),
                    box_size,
                    box_color,
                )
            )

        return player_boxes

    def draw(self, surface: Surface):
        super().draw(surface)
        self.timer.draw(surface)
        for box in self.player_boxes:
            box.draw(surface)
        self.timer.start()

    def handle_event(self, event: Event, surface: Surface):
        if event.type == BEGIN_VOTING:
            return PromptVotingScreen(
                VOTING_SCREEN_BG_COLOR, self.ui_width, self.ui_height, surface
            )
        else:
            self.timer.handle_event(event, surface)

    def _handle_leave_event(self, event: PlayerLeaveEvent, surface: Surface):
        pass

    def _handle_response_event(self, event: PlayerResponseEvent, surface: Surface):
        player_name = self.players[event.player_num]

        player_box = next(
            (box for box in self.player_boxes if box.text == player_name), None
        )

        new_box = TextInBox(
            player_name,
            NORMAL_TEXT_SIZE,
            player_color_mapping[player_name],
            (player_box.center_position[0], 150),
            player_box.box_size,
            player_box.box_color,
        )

        self.player_boxes.remove(player_box)
        self.player_boxes.append(new_box)

        player_box.clear(PROMPT_ANSWERING_SCREEN_BOTTOM_BAR_COLOR, surface)
        new_box.draw(surface)
        pygame.display.update()

    def _handle_all_players_responded(self, surface: Surface):
        self.timer.stop()
        pygame.event.post(Event(BEGIN_VOTING))
        pass

    def handle_external_event(self, event: GameEvent, surface: Surface):
        match event:
            case PlayerLeaveEvent():
                self._handle_leave_event(event, surface)
            case PlayerResponseEvent():
                self._handle_response_event(event, surface)
            case BeginVotingEvent():
                self._handle_all_players_responded(surface)
            case _:
                pass


class PromptVotingScreen(Screen):
    """Screen where prompts are displayed and voted on."""

    def __init__(
            self,
            bg_color: ColorRGB,
            ui_width: int,
            ui_height: int,
            surface: Surface,
            prompt: Prompt = None,
    ):
        """Creates a new Voting Screen."""
        self.prompt = prompt
        texts = [
            Text(
                "Pick your favorite on your device now!",
                LARGE_TEXT_SIZE,
                DEFAULT_TEXT_COLOR,
                (ui_width // 2, ui_height - 100)
            ),
            TextInBox(
                "or",
                LARGE_TEXT_SIZE,
                BLACK,
                (ui_width // 2, ui_height // 2),
                (50, 50),
                TEAL,
                25
            )
        ]
        self.surface = surface
        super().__init__(bg_color, texts, ui_width, ui_height)

        self.timer = UITimer(15, DEFAULT_TIMER_POSITION)
        self.prompt_text = Text(
            "", XL_TEXT_SIZE, TEAL, (ui_width // 2, 100)
        )
        self.response_0_text = TextInBox(
            "",
            XL_TEXT_SIZE,
            BLACK,
            (ui_width // 2 - 400, ui_height // 2),
            (650, 200),
            WHITE
        )
        self.response_1_text = TextInBox(
            "",
            XL_TEXT_SIZE,
            BLACK,
            (ui_width // 2 + 400, ui_height // 2),
            (650, 200),
            WHITE
        )

        if prompt:
            self.set_prompt(prompt, self.surface)

    def set_prompt(self, prompt: Prompt, surface: Surface):
        """Sets the prompt to a new one and updates all GUI objects."""
        if self.timer.running:
            self.timer.stop()
        self.prompt = prompt
        self.prompt_text.update_text(prompt.prompt, surface)
        self.response_0_text.update_text(
            prompt.responses[prompt.player_ids[0]], surface
        )
        self.response_1_text.update_text(
            prompt.responses[prompt.player_ids[1]], surface
        )

    def draw(self, surface: Surface):
        super().draw(surface)
        self.prompt_text.draw(surface)
        self.response_0_text.draw(surface)
        self.response_1_text.draw(surface)
        self.timer.draw(surface)
        self.timer.start()

    def _reveal_names(self, name_0: str, name_1: str, surface: Surface):
        """Helper to draw_results. Draws the player names for each response."""
        name_0_text = Text(
            name_0,
            LARGE_TEXT_SIZE,
            player_color_mapping[name_0],
            (self.response_0_text.center_position[0],
             self.response_0_text.center_position[1] + (self.response_0_text.box_size[1] // 2) - 25)
        )
        name_1_text = Text(
            name_1,
            LARGE_TEXT_SIZE,
            player_color_mapping[name_1],
            (self.response_1_text.center_position[0],
             self.response_1_text.center_position[1] + (self.response_1_text.box_size[1] // 2) - 25)
        )
        name_0_text.draw(surface)
        name_1_text.draw(surface)

    def _reveal_voters(
            self, voters_0: list[str], voters_1: list[str], surface: Surface
    ):
        """Helper to draw_results. Draws the voters' names to the screen."""

        left_center = self.response_0_text.center_position
        right_center = self.response_1_text.center_position

        spacing = 10
        box_width = 80
        box_height = 30

        top_row = left_center[1] - self.response_0_text.box_size[1] // 2 - spacing * 2 - box_height - box_height // 2
        bottom_row = top_row + box_height + spacing

        column_0_left = left_center[0] - spacing - box_width
        column_0_right = left_center[0] + spacing + box_width

        column_1_left = right_center[0] - spacing - box_width
        column_1_right = right_center[0] + spacing + box_width

        left_voter_positions = [
            (left_center[0], bottom_row),
            (column_0_left, bottom_row),
            (column_0_right, bottom_row),
            (left_center[0], top_row),
            (column_0_left, top_row),
            (column_0_right, top_row)
        ]

        right_voter_positions = [
            (right_center[0], bottom_row),
            (column_1_right, bottom_row),
            (column_1_left, bottom_row),
            (right_center[0], top_row),
            (column_1_right, top_row),
            (column_1_left, top_row)
        ]

        for index, voter_name in enumerate(voters_0):
            vote = TextInBox(
                voter_name,
                NORMAL_TEXT_SIZE,
                player_color_mapping[voter_name],
                left_voter_positions[index],
                (box_width, box_height),
                DEFAULT_BUTTON_COLOR
            )
            vote.draw(surface)

        for index, voter_name in enumerate(voters_1):
            vote = TextInBox(
                voter_name,
                NORMAL_TEXT_SIZE,
                player_color_mapping[voter_name],
                right_voter_positions[index],
                (box_width, box_height),
                DEFAULT_BUTTON_COLOR
            )
            vote.draw(surface)

        top_left_corner = (left_center[0] - self.response_0_text.box_size[0] // 2,
                           left_center[1] - self.response_0_text.box_size[1] // 2)

        top_right_corner = (right_center[0] + self.response_1_text.box_size[0] // 2,
                            right_center[1] - self.response_1_text.box_size[1] // 2)

        player_0_votes = TextInBox(
            str(len(voters_0)),
            LARGE_TEXT_SIZE,
            WHITE,
            (top_left_corner[0] - 25, top_left_corner[1] - 25),
            (50, 50),
            BLACK,
            25
        )

        player_1_votes = TextInBox(
            str(len(voters_1)),
            LARGE_TEXT_SIZE,
            WHITE,
            (top_right_corner[0] + 25, top_right_corner[1] - 25),
            (50, 50),
            BLACK,
            25
        )

        player_0_votes.draw(surface)
        player_1_votes.draw(surface)

    def _reveal_tie(self, surface: Surface):

        tie_text = Text(
            "TIE",
            XL_TEXT_SIZE,
            DEFAULT_TEXT_COLOR,
            (self.ui_width // 2, self.ui_height - 200)
        )

        tie_text.draw(surface)

    def _reveal_winner_or_quiplasher(self, quiplash_occurred: bool, player_index: int, surface: Surface):

        win_text = "QUIPLASH!" if quiplash_occurred else "WINNER"

        winner_text_x_position = self.response_0_text.center_position[0] if player_index == 0 else \
            self.response_1_text.center_position[0]

        winner_text = Text(
            win_text,
            XL_TEXT_SIZE,
            TEAL if quiplash_occurred else BLACK,
            (winner_text_x_position, self.ui_height - 200)
        )

        winner_text.draw(surface)

    def _reveal_points(self, player_0_points: int, player_1_points: int, surface: Surface):

        player_0_points_text = Text(
            f"+{player_0_points}",
            XL_TEXT_SIZE,
            WHITE,
            (self.response_0_text.center_position[0] - self.response_0_text.box_size[0] // 2, self.ui_height - 200)
        )

        player_1_points_text = Text(
            f"+{player_1_points}",
            XL_TEXT_SIZE,
            WHITE,
            (self.response_1_text.center_position[0] + self.response_1_text.box_size[0] // 2, self.ui_height - 200)
        )

        player_0_points_text.draw(surface)
        player_1_points_text.draw(surface)

    def draw_results(self, results: EndPromptVotingEvent, surface: Surface):
        """Draws the players and points to the screen."""
        self.timer.stop()
        self._reveal_names(results.player_0_name, results.player_1_name, surface)
        self._reveal_voters(results.player_0_voter_names, results.player_1_voter_names, surface)

        if results.tie:
            self._reveal_tie(surface)
        else:
            winner_index = 0 if results.winner == results.player_0_name else 1
            quiplash_occurred = results.quiplasher is not None
            self._reveal_winner_or_quiplasher(quiplash_occurred, winner_index, surface)

        self._reveal_points(results.player_0_points_awarded, results.player_1_points_awarded, surface)

    def handle_event(self, event: Event, surface: Surface):
        if event.type == TIMER_SECOND_PASSED:
            self.timer.handle_event(event, surface)
        elif event.type == SHOW_SCOREBOARD:
            scoreboard_screen = ScoreboardScreen(
                SCOREBOARD_SCREEN_BG_COLOR,
                self.ui_width,
                self.ui_height,
                event.dict["names_in_order"],
                event.dict["points_in_order"],
            )
            return scoreboard_screen

    def handle_external_event(self, event: GameEvent, surface: Surface):
        match event:
            case BeginPromptVotingEvent():
                self.set_prompt(event.prompt, surface)
                self.draw(surface)
            case EndPromptVotingEvent():
                self.draw_results(event, surface)
            case ScoreboardEvent():
                internal_event = Event(
                    SHOW_SCOREBOARD,
                    {
                        "names_in_order": event.names_in_order,
                        "points_in_order": event.points_in_order,
                    },
                )

                pygame.event.post(internal_event)


class ScoreboardScreen(Screen):
    def __init__(
            self,
            bg_color: ColorRGB,
            ui_width: int,
            ui_height: int,
            players_in_order: list[str],
            points_in_order: list[str],
    ):
        texts = [
            TextInBox(
                "scores",
                XL_TEXT_SIZE,
                BLACK,
                (100, 50),
                (125, 40),
                SCORES_BOX_COLOR
            )
        ]
        self.players_in_order = players_in_order
        self.points_in_order = points_in_order

        super().__init__(bg_color, texts, ui_width, ui_height)

        self.place_boxes: list[TextInBox] = self._init_place_boxes(
            players_in_order, points_in_order
        )

    def _init_place_boxes(self, players: list[str], points: list[str]):
        boxes = []
        for i in range(len(players)):
            size = 240 - (i * 20)
            x = ((self.ui_width / 2) - 375) + (i % 4) * 250
            v_offset = -(5 + (size / 2)) if i < 4 else 75 + (size / 2)
            y = (self.ui_height / 2) + v_offset

            boxes.append(
                Text(
                    str(i + 1),
                    MEGA_TEXT_SIZE - i * 20,
                    SCOREBOARD_NUMBER_COLOR,
                    (int(x), int(y))
                )
            )

            boxes.append(
                TextInBox(
                    f"{players[i]}",
                    LARGE_TEXT_SIZE - i * 2,
                    player_color_mapping[players[i]],
                    (int(x), int(y - (size / 8))),
                    (size // 2, size // 4),
                    DEFAULT_BUTTON_COLOR,
                )
            )
            boxes.append(
                Text(
                    str(points[i]),
                    XL_TEXT_SIZE - i * 4,
                    WHITE,
                    (int(x), int(y + (size / 8))),
                )
            )
        return boxes

    def draw(self, surface: Surface):
        super().draw(surface)
        for box in self.place_boxes:
            box.draw(surface)

    def handle_event(self, event: Event, surface: Surface):
        pass

    def handle_external_event(self, event: GameEvent, surface: Surface):
        pass
