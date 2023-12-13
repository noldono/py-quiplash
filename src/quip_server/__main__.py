import logging
import sys

from .server_listener import GameListener
from .server_ui.server_gui import ServerGUI

UI_WINDOW_WIDTH = 1600
""" The height of the UI window. """

UI_WINDOW_HEIGHT = 900
""" The width of the UI window. """

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ui = ServerGUI(UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT)
    ui.thread.start()
    listener = GameListener(ui)
    listener.run()
