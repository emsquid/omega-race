import pygame
from time import time
from src.base import Text


class Settings:
    """
    The settings of the game
    """

    def __init__(self):
        self.keys = {
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "SHOOT": pygame.K_SPACE,
        }
        self.selection = 0
        self.menu_open = False  # nom de merde

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return time() - self.last_change >= 0.15

    def update(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key != pygame.K_RETURN:
            self.keys[action] = key

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings):
        """
        Handle user inputs in the settings

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if (
            keys[settings.keys["UP"]]
            and not keys[settings.keys["DOWN"]]
            and self.can_change()
        ):
            self.selection = (self.selection - 1) % 3
            self.last_change = time()
        if (
            keys[settings.keys["DOWN"]]
            and not keys[settings.keys["UP"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % 3
            self.last_change = time()

    def draw(self, surface):
        # pygame.key.name()
        title = Text("Settings", 200, 200, 90)
