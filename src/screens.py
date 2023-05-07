import pygame
from time import time
from src.objects.base import Object, Text
from src.objects.graphics import Border
from src.config import Config
from src.data import Data
from src.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    CEN_X,
    CEN_Y,
    PAN_WIDTH,
    PAN_HEIGHT,
    HOME,
    PLAY,
    SCORES,
    SETTINGS,
    WHITE,
    BLACK,
    GREY,
    RED,
    GREEN,
)


class Screen:
    """
    Represents a screen which can be displayed and handle inputs

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        self.config = config
        self.last_change = 0

        self.selection = 0
        self.choices = []
        self.objects = []

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return time() - self.last_change >= 0.15

    def get_choice(self) -> int:
        """
        Get the currently selectionned choice
        """
        return (
            self.choices[self.selection] if self.selection < len(self.choices) else None
        )

    def get_objects(self) -> tuple[Object]:
        """
        Get every object from the screen

        :return: tuple[Object], All objects
        """
        return (*self.objects,)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single user event

        :param event: pygame.event.Event, The event (key) that was pressed
        """
        pass

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the screen

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if (
            keys[self.config.keys["UP"]]
            and not keys[self.config.keys["DOWN"]]
            and self.can_change()
        ):
            self.selection = (self.selection - 1) % len(self.choices)
            self.last_change = time()
        if (
            keys[self.config.keys["DOWN"]]
            and not keys[self.config.keys["UP"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % len(self.choices)
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        pass


class Welcome(Screen):
    """
    The Welcome of the game, gain time for loading things and getting name

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

        self.title = Text("Omega Race", CEN_X, WIN_HEIGHT / 5, 90)
        self.input_text = Text("Enter your name:", CEN_X, CEN_Y, 40)
        self.input = Text(self.config.name, CEN_X, CEN_Y + 50, 40, GREEN)

        self.choices = [HOME]
        self.objects = [self.title, self.input_text, self.input]

    def get_choice(self) -> int:
        """
        Get the currently selectionned choice
        """
        return super().get_choice() if self.config.name != "" else None

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a user event

        :param event: pygame.event.Event, The event (key) that was pressed
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.config.name = self.config.name[:-1]
            elif event.unicode.isalnum() and len(self.config.name) < 15:
                self.config.name += event.unicode.upper()

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.input.update(content=self.config.name + ("_" if time() % 1 > 0.5 else " "))


class Home(Screen):
    """
    The Home of the game

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

        self.title = Text("Omega Race", CEN_X, WIN_HEIGHT / 5, 90)
        self.play = Text("Play", CEN_X, CEN_Y - 50, 40, RED)
        self.scores = Text("Scores", CEN_X, CEN_Y + 50, 40)
        self.settings = Text("Settings", CEN_X, CEN_Y + 150, 40)

        self.choices = [PLAY, SCORES, SETTINGS]
        self.objects = [self.title, self.play, self.scores, self.settings]

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.play.update(color=RED if self.selection == 0 else WHITE)
        self.scores.update(color=RED if self.selection == 1 else WHITE)
        self.settings.update(color=RED if self.selection == 2 else WHITE)


class Scores(Screen):
    """
    The scores of the game

    :param config: Config, The game configuration
    :param data: Data, The database for scores
    """

    def __init__(self, config: Config, data: Data):
        super().__init__(config)
        self.data = data

        self.title = Text("Scores", CEN_X, WIN_HEIGHT / 5, 90)
        self.names = [
            Text(f"{i+1}. -----", 150 - i, 240 + i * 40, anchor="topleft")
            for i in range(10)
        ]
        self.scores = [
            Text("-----", 550, 240 + i * 40, anchor="topright") for i in range(10)
        ]
        self.levels = [
            Text("--", 800, 240 + i * 40, anchor="topright") for i in range(10)
        ]
        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40, RED)

        self.choices = [HOME]
        self.objects = [self.title, *self.names, *self.scores, *self.levels, self.home]

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        for i in range(10):
            if i < len(self.data.scores):
                self.names[i].update(content=f"{i+1}. {self.data.scores[i]['name']}")
                self.scores[i].update(content=f"{self.data.scores[i]['score']}")
                self.levels[i].update(content=f"{self.data.scores[i]['level']}")


class Settings(Screen):
    """
    The settings of the game

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

        self.title = Text("Settings", CEN_X, WIN_HEIGHT / 5, 90)

        self.up_text = Text("UP", CEN_X - 200, CEN_Y - 120, 40, RED, anchor="left")
        self.up_key = Text(pygame.key.name(self.config.keys["UP"]), 600, 280, 40)

        self.down_text = Text("DOWN", CEN_X - 200, CEN_Y - 40, 40, anchor="left")
        self.down_key = Text(pygame.key.name(self.config.keys["DOWN"]), 600, 360, 40)

        self.left_text = Text("LEFT", CEN_X - 200, CEN_Y + 40, 40, anchor="left")
        self.left_key = Text(pygame.key.name(self.config.keys["LEFT"]), 600, 440, 40)

        self.right_text = Text("RIGHT", CEN_X - 200, CEN_Y + 120, 40, anchor="left")
        self.right_key = Text(pygame.key.name(self.config.keys["RIGHT"]), 600, 520, 40)

        self.shoot_text = Text("SHOOT", CEN_X - 200, CEN_Y + 200, 40, anchor="left")
        self.shoot_key = Text(pygame.key.name(self.config.keys["SHOOT"]), 600, 600, 40)

        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40)

        # TODO: Make that better lol
        self.popup = Object(CEN_X, CEN_Y, WIN_WIDTH / 2, WIN_HEIGHT / 4)
        self.popup.image.fill(GREY)
        self.popup_text_1 = Text("Please choose", CEN_X, CEN_Y - 20, 40, BLACK)
        self.popup_text_2 = Text("the new key", CEN_X, CEN_Y + 20, 40, BLACK)

        self.popup_open = False

        self.choices = [None, None, None, None, None, HOME]

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return not self.popup_open and super().can_change()

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the settings

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        super().handle_keys(keys)
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
                self.config.update_key("UP", event.key)
            elif self.selection == 1:
                self.config.update_key("DOWN", event.key)
            elif self.selection == 2:
                self.config.update_key("LEFT", event.key)
            elif self.selection == 3:
                self.config.update_key("RIGHT", event.key)
            elif self.selection == 4:
                self.config.update_key("SHOOT", event.key)

            self.popup_open = False
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation for all objects

        :param dt: int, The time delta between frames
        """
        self.up_text.update(color=RED if self.selection == 0 else WHITE)
        self.up_key.update(content=pygame.key.name(self.config.keys["UP"]))

        self.down_text.update(color=RED if self.selection == 1 else WHITE)
        self.down_key.update(content=pygame.key.name(self.config.keys["DOWN"]))

        self.left_text.update(color=RED if self.selection == 2 else WHITE)
        self.left_key.update(content=pygame.key.name(self.config.keys["LEFT"]))

        self.right_text.update(color=RED if self.selection == 3 else WHITE)
        self.right_key.update(content=pygame.key.name(self.config.keys["RIGHT"]))

        self.shoot_text.update(color=RED if self.selection == 4 else WHITE)
        self.shoot_key.update(content=pygame.key.name(self.config.keys["SHOOT"]))

        self.home.update(color=RED if self.selection == 5 else WHITE)

        self.objects = [
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
        ]

        if self.popup_open:
            self.objects.extend((self.popup, self.popup_text_1, self.popup_text_2))


class GameOver(Screen):
    """
    The GameOver in the game

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

        self.title = Text("Game Over", CEN_X, WIN_HEIGHT / 5, 90)
        self.play = Text("Play Again", WIN_WIDTH / 4, WIN_HEIGHT * 3 / 4 + 50, 40, RED)
        self.home = Text("Home", WIN_WIDTH * 3 / 4, WIN_HEIGHT * 3 / 4 + 50, 40)
        self.borders = [
            Border(CEN_X - PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, 0, True),
            Border(CEN_X + PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, 0, True),
            Border(CEN_X, CEN_Y - PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, 0, True),
            Border(CEN_X, CEN_Y + PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, 0, True),
        ]

        self.choices = [PLAY, HOME]
        self.objects = [self.title, self.play, self.home, *self.borders]

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the game over

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if (
            keys[self.config.keys["LEFT"]]
            and not keys[self.config.keys["RIGHT"]]
            and self.can_change()
        ):
            self.selection = (self.selection - 1) % 2
            self.last_change = time()
        if (
            keys[self.config.keys["RIGHT"]]
            and not keys[self.config.keys["LEFT"]]
            and self.can_change()
        ):
            self.selection = (self.selection + 1) % 2
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.play.update(color=RED if self.selection == 0 else WHITE)
        self.home.update(color=RED if self.selection == 1 else WHITE)
        for border in self.borders:
            border.update()
