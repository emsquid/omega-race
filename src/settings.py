import pygame
from time import time
from src.base import Text, Object
from src.const import RED, WHITE, GREY, BLACK


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
        # TODO: nom de merde
        self.menu_open = False

        self.title = Text("Settings", 500, 150, size=90)

        self.up_text = Text("UP", 300, 280, RED, size=40, anchor="left")
        self.up_key = Text(pygame.key.name(self.keys["UP"]), 600, 280, size=40)

        self.down_text = Text("DOWN", 300, 360, size=40, anchor="left")
        self.down_key = Text(pygame.key.name(self.keys["DOWN"]), 600, 360, size=40)

        self.left_text = Text("LEFT", 300, 440, size=40, anchor="left")
        self.left_key = Text(pygame.key.name(self.keys["LEFT"]), 600, 440, size=40)

        self.right_text = Text("RIGHT", 300, 520, size=40, anchor="left")
        self.right_key = Text(pygame.key.name(self.keys["RIGHT"]), 600, 520, size=40)

        self.shoot_text = Text("SHOOT", 300, 600, size=40, anchor="left")
        self.shoot_key = Text(pygame.key.name(self.keys["SHOOT"]), 600, 600, size=40)

        self.home = Text("HOME", 800, 700, size=40)

        # TODO: Make that better lol
        self.message = Object(500, 200, 500, 400)
        self.message.set_image()
        self.message.image.fill(GREY)
        self.message_text1 = Text("Please choose", 500, 380, BLACK, 40)
        self.message_text2 = Text("the new key", 500, 420, BLACK, 40)

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return not self.menu_open and time() - self.last_change >= 0.15

    def update(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key != pygame.K_RETURN and not key in self.keys.values():
            self.keys[action] = key

    def get_objects(self) -> tuple[Object]:
        """
        Get every object handled by the settings

        :return: tuple[Object], All objects
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
            obj + (self.message, self.message_text1, self.message_text2)
            if self.menu_open
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
            self.menu_open = True
            self.last_change = time()

    def handle_events(self, event: pygame.event.Event):
        """
        Handle a user event when the menu is open

        :param event: pygame.event.Event, The event (key) that was pressed
        """
        if self.menu_open:
            if self.selection == 0:
                self.update("UP", event)
            elif self.selection == 1:
                self.update("DOWN", event)
            elif self.selection == 2:
                self.update("LEFT", event)
            elif self.selection == 3:
                self.update("RIGHT", event)
            elif self.selection == 4:
                self.update("SHOOT", event)

            self.menu_open = False
            self.last_change = time()
