import pygame
import pyautogui
import sys


class TextBox:
    def __init__(self, x, y, width, height, font_size=24, character_limit=sys.maxsize, callback=None):
        pygame.init()
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.active = False  # Flag to indicate if the text box is currently active (selected)
        self.submit_text = callback
        self.character_limit = character_limit

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, surface):
        color = (255, 255, 255)
        pygame.draw.rect(surface, color, self.rect)

        color = (40, 40, 40) if not self.active else (0, 255, 6)
        pygame.draw.rect(surface, color, self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action, text_boxes=None,
                 text_color=(255, 255, 255)):
        if text_boxes is None:
            text_boxes = []
        pygame.init()
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False
        self.connected_text_boxes = text_boxes
        self.text_color = text_color

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                # If the button is connected to a text box, submit the text upon click
                if self.connected_text_boxes is not None and len(self.connected_text_boxes) > 0:
                    for box in self.connected_text_boxes:
                        if handle_char_limit(box):
                            box.submit_text(box.text)
                self.action()


def handle_char_limit(box: TextBox) -> bool:
    char_limit_error = f"You have exceeded the character limit of {box.character_limit}"
    if len(box.text) > box.character_limit:
        pyautogui.alert(char_limit_error)
        return False
    return True
