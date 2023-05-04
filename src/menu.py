import pygame
from time import time
from src.const import WHITE, RED
from src.base import Object, Text
from src.graphics import Border
from src.settings import Settings


class Home:
    """"""

    def __init__(self):
        self.selection = 0
        self.last_change = 0
        self.title = Text("Omega Race", 500, 150, WHITE, 90)
        self.play = Text("Play", 500, 350, RED, 40)
        self.scores = Text("Scores", 500, 450, WHITE, 40)
        self.settings = Text("Settings", 500, 550, WHITE, 40)

    def get_objects(self) -> tuple[Object]:
        self.play.set_color(RED if self.selection == 0 else WHITE)
        self.scores.set_color(RED if self.selection == 1 else WHITE)
        self.settings.set_color(RED if self.selection == 2 else WHITE)
        return (self.title, self.play, self.scores, self.settings)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
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

    def can_change(self) -> bool:
        return time() - self.last_change > 0.15


class GameOver:
    """"""

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

    def get_objects(self) -> tuple[Object]:
        self.play.set_color(RED if self.selection == 0 else WHITE)
        self.home.set_color(RED if self.selection == 1 else WHITE)
        return (self.title, self.play, self.home, *self.borders)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
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

    def can_change(self) -> bool:
        return time() - self.last_change > 0.15
