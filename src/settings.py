import pygame
from time import time
from src.base import Text, Object
from src.const import WIN_WIDTH, WIN_HEIGHT, CEN_X, CEN_Y, RED, WHITE, GREY, BLACK


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
        self.last_change = 0
        self.popup_open = False

        self.title = Text("Settings", CEN_X, WIN_HEIGHT / 5, 90)

        self.up_text = Text("UP", CEN_X - 200, CEN_Y - 120, 40, RED, anchor="left")
        self.up_key = Text(pygame.key.name(self.keys["UP"]), 600, 280, 40)

        self.down_text = Text("DOWN", CEN_X - 200, CEN_Y - 40, 40, anchor="left")
        self.down_key = Text(pygame.key.name(self.keys["DOWN"]), 600, 360, 40)

        self.left_text = Text("LEFT", CEN_X - 200, CEN_Y + 40, 40, anchor="left")
        self.left_key = Text(pygame.key.name(self.keys["LEFT"]), 600, 440, 40)

        self.right_text = Text("RIGHT", CEN_X - 200, CEN_Y + 120, 40, anchor="left")
        self.right_key = Text(pygame.key.name(self.keys["RIGHT"]), 600, 520, 40)

        self.shoot_text = Text("SHOOT", CEN_X - 200, CEN_Y + 200, 40, anchor="left")
        self.shoot_key = Text(pygame.key.name(self.keys["SHOOT"]), 600, 600, 40)

        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40)

        # TODO: Make that better lol
        self.popup = Object(CEN_X, WIN_HEIGHT / 4, 500, 400)
        self.popup.image.fill(GREY)
        self.popup_text_1 = Text("Please choose", CEN_X, CEN_Y - 20, 40, BLACK)
        self.popup_text_2 = Text("the new key", CEN_X, CEN_Y + 20, 40, BLACK)

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return not self.popup_open and time() - self.last_change >= 0.15

    def update_key(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key != pygame.K_RETURN and not key in self.keys.values():
            self.keys[action] = key

    def update(self):
        """
        Update the situation for all objects
        """
        self.up_text.update(color=RED if self.selection == 0 else WHITE)
        self.up_key.update(content=pygame.key.name(self.keys["UP"]))

        self.down_text.update(color=RED if self.selection == 1 else WHITE)
        self.down_key.update(content=pygame.key.name(self.keys["DOWN"]))

        self.left_text.update(color=RED if self.selection == 2 else WHITE)
        self.left_key.update(content=pygame.key.name(self.keys["LEFT"]))

        self.right_text.update(color=RED if self.selection == 3 else WHITE)
        self.right_key.update(content=pygame.key.name(self.keys["RIGHT"]))

        self.shoot_text.update(color=RED if self.selection == 4 else WHITE)
        self.shoot_key.update(content=pygame.key.name(self.keys["SHOOT"]))

        self.home.update(color=RED if self.selection == 5 else WHITE)

    def get_objects(self) -> tuple[Object]:
        """
        Get every object handled by the settings

        :return: tuple[Object], All objects
        """
        obj = (
            self.title,
            self.up_text,
            self.up_key,
            self.down_text,
            self.down_key,
            self.left_text,
            self.left_key,
            self.right_text,
            self.right_key,
            self.shoot_text,
            self.shoot_key,
            self.home,
        )

        return (
            obj + (self.popup, self.popup_text_1, self.popup_text_2)
            if self.popup_open
            else obj
        )

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
            self.selection = (self.selection - 1) % 6
            self.last_change = time()
        if (
            keys[settings.keys["DOWN"]]
            and not keys[settings.keys["UP"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % 6
            self.last_change = time()
        if keys[pygame.K_RETURN] and self.can_change():
            self.popup_open = True
            self.last_change = time()

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a user event when the popup is open

        :param event: pygame.event.Event, The event (key) that was pressed
        """
        if self.popup_open and event.type == pygame.KEYDOWN:
            if self.selection == 0:
                self.update_key("UP", event.key)
            elif self.selection == 1:
                self.update_key("DOWN", event.key)
            elif self.selection == 2:
                self.update_key("LEFT", event.key)
            elif self.selection == 3:
                self.update_key("RIGHT", event.key)
            elif self.selection == 4:
                self.update_key("SHOOT", event.key)

            self.popup_open = False
            self.last_change = time()
