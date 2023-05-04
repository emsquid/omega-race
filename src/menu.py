import pygame
from time import time
from src.const import WHITE, RED
from src.base import Object, Text


class Home:
    """"""

    def __init__(self):
        self.selection = 0
        self.last_change = 0

    def get_objects(self) -> tuple[Object]:
        title = Text("Omega Race", 500, 150, WHITE, 90)
        play = Text("Play", 500, 350, RED if self.selection == 0 else WHITE, 40)
        scores = Text("Scores", 500, 450, RED if self.selection == 1 else WHITE, 40)
        settings = Text("Settings", 500, 550, RED if self.selection == 2 else WHITE, 40)
        return (title, play, scores, settings)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and self.can_change():
            self.selection = (self.selection - 1) % 3
            self.last_change = time()
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and self.can_change():
            self.selection = (self.selection + 1) % 3
            self.last_change = time()

    def can_change(self) -> bool:
        return time() - self.last_change > 0.15


class GameOver:
    """"""

    def __init__(self):
        self.selection = 0
        self.last_change = 0

    def get_objects(self) -> tuple[Object]:
        title = Text("Game Over", 500, 150, WHITE, 90)
        play = Text("Play Again", 250, 650, RED if self.selection == 0 else WHITE, 40)
        home = Text("Home", 750, 650, RED if self.selection == 1 else WHITE, 40)
        return (title, play, home)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and self.can_change():
            self.selection = (self.selection - 1) % 2
            self.last_change = time()
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and self.can_change():
            self.selection = (self.selection + 1) % 2
            self.last_change = time()

    def can_change(self) -> bool:
        return time() - self.last_change > 0.15
