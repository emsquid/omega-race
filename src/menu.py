import pygame
from time import time
from src.base import Object, Text
from src.graphics import Border
from src.settings import Settings
from src.const import WHITE, RED


class Home:
    """
    The Home of the game
    """

    def __init__(self):
        self.selection = 0
        self.last_change = 0
        self.title = Text("Omega Race", 500, 150, WHITE, 90)
        self.play = Text("Play", 500, 350, RED, 40)
        self.scores = Text("Scores", 500, 450, WHITE, 40)
        self.settings = Text("Settings", 500, 550, WHITE, 40)

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return time() - self.last_change >= 0.15

    def get_objects(self) -> tuple[Object]:
        """
        Get every object from the home

        :return: tuple[Object], All objects
        """
        self.play.update(color=RED if self.selection == 0 else WHITE)
        self.scores.update(color=RED if self.selection == 1 else WHITE)
        self.settings.update(color=RED if self.selection == 2 else WHITE)
        return (self.title, self.play, self.scores, self.settings)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
        """
        Handle user inputs in the home

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


class GameOver:
    """
    The GameOver in the game
    """

    def __init__(self):
        self.selection = 0
        self.last_change = 0
        self.title = Text("Game Over", 500, 165, WHITE, 90)
        self.play = Text("Play Again", 250, 650, RED, 40)
        self.home = Text("Home", 750, 650, WHITE, 40)
        self.borders = [
            Border(3, 203, 700, 400, 0, True),
            Border(3, 203, 300, 400, 0, True),
            Border(403, 3, 500, 500, 0, True),
            Border(403, 3, 500, 300, 0, True),
        ]

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return time() - self.last_change >= 0.15

    def get_objects(self) -> tuple[Object]:
        """
        Get every object from the game over

        :return: tuple[Object], All objects
        """
        self.play.update(color=RED if self.selection == 0 else WHITE)
        self.home.update(color=RED if self.selection == 1 else WHITE)
        return (self.title, self.play, self.home, *self.borders)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
        """
        Handle user inputs in the game over

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if (
            keys[settings.keys["LEFT"]]
            and not keys[settings.keys["RIGHT"]]
            and self.can_change()
        ):
            self.selection = (self.selection - 1) % 2
            self.last_change = time()
        if (
            keys[settings.keys["RIGHT"]]
            and not keys[settings.keys["LEFT"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % 2
            self.last_change = time()
