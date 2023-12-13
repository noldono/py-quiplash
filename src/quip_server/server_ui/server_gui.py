"""
File: server_gui.py
Author: Jason Dech (jasonmdech)
Created: 2 December 2023
Purpose: Main server GUI file.
"""

import pygame
import logging
import os
from queue import Queue, Empty
from threading import Thread

from .ui_elements import *

logger = logging.getLogger(__name__)

class ServerGUI:
    """Class that handles all operations of the server-side GUI."""

    def __init__(self, width: int, height: int):
        """
        Creates a new Server GUI.

        Parameters:
            width (int): The width of the GUI window.
            height (int): The height of the GUI window.
        """

        self.width = width
        """ The width of the GUI window. """

        self.height = height
        """ The height of the GUI window. """

        self.is_running = True
        """ Keeps track of if the GUI is running. """

        self.event_queue: Queue[GameEvent] = Queue()
        """ Queue for handling external events that relate to the GUI. """

        self.thread: Thread = Thread(target=self.run)

        self.screen = None
        """ The main screen of the GUI. """

        pygame.init()

        self.clock = pygame.time.Clock()
        """ The GUI's clock. """

        self.current_screen: Screen = PlayerJoinScreen(
            JOIN_SCREEN_BG_COLOR, self.width, self.height
        )
        """ Keeps track of the currently displayed screen. """

    def run(self):
        """ Main UI loop after displaying the first screen. """
        # Display title screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quiplash")

        self.current_screen.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

        while self.is_running:
            for event in pygame.event.get():
                self.handle_ui_event(event)

            try:
                event = self.event_queue.get_nowait()
                self.current_screen.handle_external_event(event, self.screen)

            except Empty:
                pass

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_ui_event(self, event: Event):
        """ Handles PyGame Events. """

        time_to_exit = event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

        if time_to_exit:
            logger.debug("UI: Exiting...")
            self.is_running = False
            return

        next_screen = self.current_screen.handle_event(event, self.screen)
        if next_screen is not None:
            self.current_screen = next_screen
            self.current_screen.draw(self.screen)

    def stop(self):
        self.is_running = False
