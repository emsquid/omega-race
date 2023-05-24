import pygame
from time import time
from src.objects.base import Object, Text
from src.objects.graphics import Border
from src.config import Config
from src.data import Data
from src.mixer import Mixer
from src.vector import Vector
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
    EXIT,
    WHITE,
    BLACK,
    GREY,
    RED,
    PLAYER_COLORS,
)


class Screen:
    """
    Represents a screen which can be displayed and handle inputs

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        self.config = config
        self.mixer = mixer

        self.objects: list[Object] = []
        self.choices: list[tuple[Object, int]] = []
        self.reset()

    def reset(self):
        """
        Reset the state of the screen
        """
        self.choice = None
        self.selection = 0 if not self.config.mouse else -1
        self.last_change = time()

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return time() - self.last_change >= 0.2

    def get_choice(self) -> int:
        """
        Get the final choice

        :return: int, The id of the selectionned choice
        """
        return (
            self.choices[self.selection][1]
            if 0 <= self.selection < len(self.choices)
            else None
        )

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single user event

        :param event: pygame.event.Event, The event that happened
        """
        pass

    def handle_keys(self):
        """
        Handle user key press in the screen
        """
        if self.config.mouse or not self.can_change():
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.choice = self.get_choice()
        if keys[self.config.keys["UP"]] and not keys[self.config.keys["DOWN"]]:
            self.selection = (self.selection - 1) % len(self.choices)
            self.last_change = time()
        if keys[self.config.keys["DOWN"]] and not keys[self.config.keys["UP"]]:
            self.selection = (self.selection + 1) % len(self.choices)
            self.last_change = time()

    def handle_mouse(self):
        """
        Handle user mouse press in the screen
        """
        if not self.config.mouse or not self.can_change():
            return

        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            self.choice = self.get_choice()

        pos = Vector(*pygame.mouse.get_pos())
        scaled_pos = pos * (WIN_WIDTH, WIN_HEIGHT) / pygame.display.get_window_size()
        selected = False
        for i in range(len(self.choices)):
            if self.choices[i][0].rect.collidepoint(scaled_pos.x, scaled_pos.y):
                self.selection = i
                selected = True

        self.selection = self.selection if selected else -1

    def draw(self, surface: pygame.Surface):
        """
        Draw the screen on the given surface

        :param surface: pygame.Surface, The surface to draw the screen on
        """
        for obj in self.objects:
            obj.draw(surface)

    def update_color(self, text: Text, number: int):
        """
        Update the color of the text based on its number

        :param text: Text, The text to update
        :param number: int, The number of the text (selection)
        """
        text.update(
            color=self.config.color
            if self.selection == number and self.config.color != WHITE
            else RED
            if self.selection == number
            else WHITE,
        )

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
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

        self.title = Text("Omega Race", CEN_X, WIN_HEIGHT / 5, 90)
        self.input_text = Text("Enter your name:", CEN_X, CEN_Y, 40)
        self.input = Text(self.config.name, CEN_X, CEN_Y + 50, 40, self.config.color)

        self.objects = [self.title, self.input_text, self.input]
        self.choices = [(self.input, HOME)]

    def get_choice(self) -> int:
        """
        Get the currently selectionned choice
        """
        return HOME if self.config.name != "" else None

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a user event

        :param event: pygame.event.Event, The event that happened
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.choice = self.get_choice()
            elif event.key == pygame.K_BACKSPACE:
                self.config.name = self.config.name[:-1]
            elif event.unicode.isalnum() and len(self.config.name) < 10:
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
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

        self.title = Text("Omega Race", CEN_X, WIN_HEIGHT / 5, 90)
        self.play = Text("Play", CEN_X, CEN_Y - 70, 40)
        self.scores = Text("Scores", CEN_X, CEN_Y + 30, 40)
        self.settings = Text("Settings", CEN_X, CEN_Y + 130, 40)
        self.exit = Text("Exit", CEN_X, CEN_Y + 230, 40)

        self.objects = [self.title, self.play, self.scores, self.settings, self.exit]
        self.choices = [
            (self.play, PLAY),
            (self.scores, SCORES),
            (self.settings, SETTINGS),
            (self.exit, EXIT),
        ]

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.update_color(self.play, 0)
        self.update_color(self.scores, 1)
        self.update_color(self.settings, 2)
        self.update_color(self.exit, 3)


class Scores(Screen):
    """
    The scores of the game

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    :param data: Data, The database for scores
    """

    def __init__(self, config: Config, mixer: Mixer, data: Data):
        super().__init__(config, mixer)
        self.data = data

        self.title = Text("Scores", CEN_X, WIN_HEIGHT / 5, 90)
        self.names = [Text("", 150, 253 + i * 40, anchor="left") for i in range(10)]
        self.scores = [Text("", 550, 253 + i * 40, anchor="right") for i in range(10)]
        self.levels = [Text("", 800, 253 + i * 40, anchor="right") for i in range(10)]
        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40)

        self.objects = [self.title, *self.names, *self.scores, *self.levels, self.home]
        self.choices = [(self.home, HOME)]

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        for i in range(10):
            if i < len(self.data.scores):
                self.names[i].update(content=f"{i+1}. {self.data.scores[i]['name']}")
                self.scores[i].update(content=f"{self.data.scores[i]['score']}")
                self.levels[i].update(content=f"Level {self.data.scores[i]['level']}")
            else:
                self.names[i].update(content=f"{i+1}. -----")
                self.scores[i].update(content="-----")
                self.levels[i].update(content="--")

        self.update_color(self.home, 0)


class Settings(Screen):
    """
    The settings of the game

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

        self.title = Text("Settings", CEN_X, WIN_HEIGHT / 5, 90)

        self.up_text = Text("UP :", CEN_X - 50, CEN_Y - 160, anchor="right")
        self.up_key = Text("", CEN_X + 100, CEN_Y - 160)

        self.down_text = Text("DOWN :", CEN_X - 50, CEN_Y - 120, anchor="right")
        self.down_key = Text("", CEN_X + 100, CEN_Y - 120)

        self.left_text = Text("LEFT :", CEN_X - 50, CEN_Y - 80, anchor="right")
        self.left_key = Text("", CEN_X + 100, CEN_Y - 80)

        self.right_text = Text("RIGHT :", CEN_X - 50, CEN_Y - 40, anchor="right")
        self.right_key = Text("", CEN_X + 100, CEN_Y - 40)

        self.shoot_text = Text("SHOOT :", CEN_X - 50, CEN_Y, anchor="right")
        self.shoot_key = Text("", CEN_X + 100, CEN_Y)

        self.pause_text = Text("PAUSE :", CEN_X - 50, CEN_Y + 40, anchor="right")
        self.pause_key = Text("", CEN_X + 100, CEN_Y + 40)

        self.mouse_text = Text("MOUSE :", CEN_X - 50, CEN_Y + 80, anchor="right")
        self.mouse = Text("OFF", CEN_X + 100, CEN_Y + 80)

        self.volume_text = Text("VOLUME :", CEN_X - 50, CEN_Y + 120, anchor="right")
        self.volume = Text(f"< {config.volume*100}% >", CEN_X + 100, CEN_Y + 120)

        self.fps_text = Text("FPS :", CEN_X - 50, CEN_Y + 160, anchor="right")
        self.fps = Text(f"< {config.fps} >", CEN_X + 100, CEN_Y + 160)

        self.color_text = Text("COLOR :", CEN_X - 50, CEN_Y + 200, anchor="right")
        self.color_arrows = Text("<       >", CEN_X + 100, CEN_Y + 200)
        self.color_circle = Object(CEN_X + 103, CEN_Y + 200, pygame.Surface((40, 40)))

        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40)

        popup_image = pygame.Surface((WIN_WIDTH / 2, WIN_HEIGHT / 4)).convert_alpha()
        popup_image.fill(GREY)
        Text("Please choose", CEN_X / 2, CEN_Y / 4 - 20, 40, BLACK).draw(popup_image)
        Text("the new key", CEN_X / 2, CEN_Y / 4 + 20, 40, BLACK).draw(popup_image)
        self.popup = Object(CEN_X, CEN_Y, popup_image)

        self.popup_open = False

        self.choices = [
            (self.up_key, None),
            (self.down_key, None),
            (self.left_key, None),
            (self.right_key, None),
            (self.shoot_key, None),
            (self.pause_key, None),
            (self.mouse, None),
            (self.volume, None),
            (self.fps, None),
            (self.color_arrows, None),
            (self.home, HOME),
        ]

    def can_change(self) -> bool:
        """
        Check if the selection can change

        :return: bool, Whether it's been long enough or not
        """
        return not self.popup_open and super().can_change()

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a user event when the popup is open

        :param event: pygame.event.Event, The event that happened
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
            elif self.selection == 5:
                self.config.update_key("PAUSE", event.key)

            self.popup_open = False
            self.last_change = time()

        if self.config.mouse and event.type == pygame.MOUSEWHEEL:
            scroll = event.y
            if self.selection == 7:
                self.config.volume = min(max(self.config.volume + 0.05 * scroll, 0), 1)
            if self.selection == 8:
                self.config.fps = min(max(self.config.fps + 5 * scroll, 30), 240)
            if self.selection == 9:
                index = PLAYER_COLORS.index(self.config.color)
                self.config.color = PLAYER_COLORS[(index + scroll) % len(PLAYER_COLORS)]

    def handle_keys(self):
        """
        Handle user inputs in the settings
        """
        if self.config.mouse or not self.can_change():
            return

        super().handle_keys()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.selection < 6:
                self.popup_open = True
            elif self.selection == 6:
                self.config.mouse = not self.config.mouse
            self.last_change = time()

        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            if self.selection == 7:
                self.config.volume = max(self.config.volume - 0.05, 0)
            if self.selection == 8:
                self.config.fps = max(self.config.fps - 5, 30)
            if self.selection == 9:
                index = PLAYER_COLORS.index(self.config.color)
                self.config.color = PLAYER_COLORS[(index - 1) % len(PLAYER_COLORS)]
            self.last_change = time()

        if keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            if self.selection == 7:
                self.config.volume = min(self.config.volume + 0.05, 1)
            if self.selection == 8:
                self.config.fps = min(self.config.fps + 5, 240)
            if self.selection == 9:
                index = PLAYER_COLORS.index(self.config.color)
                self.config.color = PLAYER_COLORS[(index + 1) % len(PLAYER_COLORS)]
            self.last_change = time()

    def handle_mouse(self):
        """
        Handle mouse use in the settings
        """
        if not self.config.mouse or not self.can_change():
            return

        super().handle_mouse()
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            if 0 <= self.selection < 6:
                self.popup_open = True
            elif self.selection == 6:
                self.config.mouse = not self.config.mouse
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation for all objects

        :param dt: int, The time delta between frames
        """
        self.up_key.update(content=pygame.key.name(self.config.keys["UP"]))
        self.update_color(self.up_key, 0)

        self.down_key.update(content=pygame.key.name(self.config.keys["DOWN"]))
        self.update_color(self.down_key, 1)

        self.left_key.update(content=pygame.key.name(self.config.keys["LEFT"]))
        self.update_color(self.left_key, 2)

        self.right_key.update(content=pygame.key.name(self.config.keys["RIGHT"]))
        self.update_color(self.right_key, 3)

        self.shoot_key.update(content=pygame.key.name(self.config.keys["SHOOT"]))
        self.update_color(self.shoot_key, 4)

        self.pause_key.update(content=pygame.key.name(self.config.keys["PAUSE"]))
        self.update_color(self.pause_key, 5)

        self.mouse.update(content="ON" if self.config.mouse else "OFF")
        self.update_color(self.mouse, 6)

        self.volume.update(content=f"< {round(self.config.volume*100)}% >")
        self.update_color(self.volume, 7)

        self.fps.update(content=f"< {self.config.fps} >")
        self.update_color(self.fps, 8)

        pygame.draw.circle(self.color_circle.image, self.config.color, (20, 20), 15)
        self.update_color(self.color_arrows, 9)

        self.update_color(self.home, 10)

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
            self.pause_text,
            self.pause_key,
            self.mouse_text,
            self.mouse,
            self.volume_text,
            self.volume,
            self.fps_text,
            self.fps,
            self.color_text,
            self.color_arrows,
            self.color_circle,
            self.home,
        ]

        if self.popup_open:
            self.objects.append(self.popup)


class Pause(Screen):
    """

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

        self.title = Text("Pause", CEN_X, WIN_HEIGHT / 5, 90)
        self.play = Text("Resume", WIN_WIDTH / 4, WIN_HEIGHT * 3 / 4 + 50, 40)
        self.home = Text("Home", WIN_WIDTH * 3 / 4, WIN_HEIGHT * 3 / 4 + 50, 40)
        self.borders = [
            Border(CEN_X - PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, Vector(0, 0), True),
            Border(CEN_X + PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, Vector(0, 0), True),
            Border(CEN_X, CEN_Y - PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, Vector(0, 0), True),
            Border(CEN_X, CEN_Y + PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, Vector(0, 0), True),
        ]

        self.objects = [self.title, self.play, self.home, *self.borders]
        self.choices = [(self.play, PLAY), (self.home, HOME)]

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single user event

        :param event: pygame.event.Event, The event that happened
        """
        if event.type == pygame.KEYDOWN and event.key == self.config.keys["PAUSE"]:
            self.choice = PLAY
            self.last_change = time()

    def handle_keys(self):
        """
        Handle user inputs in the pause
        """
        if self.config.mouse or not self.can_change():
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.choice = self.get_choice()
        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            self.selection = (self.selection - 1) % len(self.choices)
            self.last_change = time()
        if keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            self.selection = (self.selection + 1) % len(self.choices)
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.update_color(self.play, 0)
        self.update_color(self.home, 1)


class GameOver(Screen):
    """
    The GameOver in the game

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

        self.title = Text("Game Over", CEN_X, WIN_HEIGHT / 5, 90)
        self.play = Text("Play Again", WIN_WIDTH / 4, WIN_HEIGHT * 3 / 4 + 50, 40)
        self.home = Text("Home", WIN_WIDTH * 3 / 4, WIN_HEIGHT * 3 / 4 + 50, 40)
        self.borders = [
            Border(CEN_X - PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, Vector(0, 0), True),
            Border(CEN_X + PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, Vector(0, 0), True),
            Border(CEN_X, CEN_Y - PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, Vector(0, 0), True),
            Border(CEN_X, CEN_Y + PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, Vector(0, 0), True),
        ]

        self.objects = [self.title, self.play, self.home, *self.borders]
        self.choices = [(self.play, PLAY), (self.home, HOME)]

    def handle_keys(self):
        """
        Handle user inputs in the game over
        """
        if self.config.mouse or not self.can_change():
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.choice = self.get_choice()
        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            self.selection = (self.selection - 1) % len(self.choices)
            self.last_change = time()
        if keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            self.selection = (self.selection + 1) % len(self.choices)
            self.last_change = time()

    def update(self, dt: int):
        """
        Update the situation of all objects

        :param dt: int, The time delta between frames
        """
        self.update_color(self.play, 0)
        self.update_color(self.home, 1)
