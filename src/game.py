import os
import pygame
from src.objects.base import Text
from src.objects.graphics import Background, Panel
from src.screens import Welcome, Home, Scores, Settings, Pause, GameOver
from src.engine import Engine
from src.config import Config
from src.mixer import Mixer
from src.data import Data
from src.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    WELCOME,
    HOME,
    PLAY,
    SCORES,
    SETTINGS,
    PAUSE,
    GAMEOVER,
    EXIT,
)


class Game:
    """
    The main game instance, handles display and inputs
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_icon(pygame.image.load("assets/images/Icon.png"))
        pygame.display.set_caption("Omega Race")

        self.display = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()

        self.config = Config()
        self.data = Data()
        self.mixer = Mixer(self.config)

        self.background = Background()
        self.panel = Panel(self.config)

        self.current = None
        self.screens = {
            WELCOME: Welcome(self.config, self.mixer),
            HOME: Home(self.config, self.mixer),
            PLAY: Engine(self.config, self.mixer),
            SCORES: Scores(self.config, self.mixer, self.data),
            SETTINGS: Settings(self.config, self.mixer),
            PAUSE: Pause(self.config, self.mixer),
            GAMEOVER: GameOver(self.config, self.mixer),
        }

    def handle_inputs(self):
        """
        Handle user events and keypresses depending on the current screen
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            else:
                self.screens[self.current].handle_event(event)

        self.screens[self.current].handle_keys()
        self.screens[self.current].handle_mouse()

        choice = self.screens[self.current].choice
        if choice is not None:
            if choice == PLAY:
                self.mixer.music("Battle.wav", 0.3)
                if self.current == PAUSE:
                    self.screens[PLAY].unpause()
                else:
                    self.screens[PLAY].start()
            if self.current == PLAY:
                self.mixer.music("Menu.wav", 1)
            if choice == GAMEOVER:
                score, level = self.screens[PLAY].score, self.screens[PLAY].level
                self.data.add_score(self.config.name, score, level)
            if choice == EXIT:
                self.exit()
            self.current = choice
            self.screens[self.current].reset()

    def update(self):
        """
        Update the situation of all objects depending on the current screen
        """
        dt = self.clock.tick(self.config.fps)

        self.data.update()
        self.mixer.update()
        self.background.update(dt)
        self.screens[self.current].update(dt)

        if self.current == PLAY:
            engine = self.screens[PLAY]
            lives, level, score = engine.lives, engine.level, engine.score
            self.panel.update(lives, level, score, max(score, self.data.highscore))

    def draw(self):
        """
        Draw the game objects on top of the background and display it
        """
        self.screens[self.current].draw(self.background.image)
        if self.current in [PLAY, PAUSE, GAMEOVER]:
            self.panel.draw(self.background.image)
        Text(str(int(self.clock.get_fps())), 50, 50).draw(self.background.image)
        size = self.display.get_size()
        pygame.transform.smoothscale(self.background.image, size, self.display)

    def run(self):
        """
        Run the game instance
        """
        self.current = WELCOME
        self.mixer.music("Menu.wav", 1)
        while True:
            self.handle_inputs()
            self.update()
            self.draw()
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        self.config.save()
        pygame.quit()
        os._exit(0)
