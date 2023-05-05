import pygame
from time import time
from src.base import Text
from src.const import RED, WHITE


class Settings:
    """
    -
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

    def update(self, action: str, key: int):
        if key != pygame.K_RETURN:
            self.keys[action] = key

    def can_change(self) -> bool:
        return time() - self.last_change > 0.15

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings):
        if (
            keys[settings.keys["UP"]]
            and not keys[settings.keys["DOWN"]]
            and self.can_change()
        ):
            self.selection = (self.selection - 1) % 5
            self.last_change = time()
        if (
            keys[settings.keys["DOWN"]]
            and not keys[settings.keys["UP"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % 5
            self.last_change = time()

    def get_object(self):
        # pygame.key.name()
        title = Text("Settings", 200, 200, size=90)

        up_text = Text("UP", 200, 300, RED if self.selection == 0 else WHITE, 40)
        up_key = Text(pygame.key.name(self.keys["UP"]), 400, 300, WHITE, 40)

        down_text = Text("DOWN", 200, 400, RED if self.selection == 1 else WHITE, 40)
        down_key = Text(pygame.key.name(self.keys["DOWN"]), 400, 400, WHITE, 40)

        right_text = Text("RIGHT", 200, 500, RED if self.selection == 2 else WHITE, 40)
        right_key = Text(pygame.key.name(self.keys["RIGHT"]), 400, 500, WHITE, 40)

        left_text = Text("LEFT", 200, 600, RED if self.selection == 3 else WHITE, 40)
        left_key = Text(pygame.key.name(self.keys["LEFT"]), 400, 600, WHITE, 40)

        shoot_text = Text("SHOOT", 200, 700, RED if self.selection == 4 else WHITE, 40)
        shoot_key = Text(pygame.key.name(self.keys["SHOOT"]), 400, 700, WHITE, 40)

        return (
            title,
            up_text,
            up_key,
            down_text,
            down_key,
            right_text,
            right_key,
            left_text,
            left_key,
            shoot_text,
            shoot_key,
        )
