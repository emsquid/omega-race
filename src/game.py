import os
import pygame
from time import time
from src.objects.graphics import Background, Panel
from src.screens import Welcome, Home, Scores, Settings, GameOver
from src.engine import Engine
from src.config import Config
from src.data import Data
from src.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    WELCOME,
    HOME,
    PLAY,
    SCORES,
    SETTINGS,
    GAMEOVER,
)


class Game:
    """
    The main game instance, handles display and inputs
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
        pygame.display.set_caption("Omega Race")

        self.display = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.panel = Panel()

        self.config = Config()
        self.data = Data()

        self.screens = {
            WELCOME: Welcome(self.config),
            HOME: Home(self.config),
            PLAY: Engine(self.config),
            SCORES: Scores(self.config, self.data),
            SETTINGS: Settings(self.config),
            GAMEOVER: GameOver(self.config),
        }
        self.current = WELCOME

    def draw(self):
        """
        Draw the game objects on top of the background and display it
        """
        objects = self.screens[self.current].get_objects()
        if self.current in [PLAY, GAMEOVER]:
            objects = objects + (self.panel,)

        for obj in objects:
            obj.draw(self.background.image)
        pygame.transform.smoothscale(
            self.background.image, self.display.get_size(), self.display
        )

    def handle_inputs(self):
        """
        Handle user events and keypresses depending on the current screen
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choice = self.screens[self.current].get_choice()
                    if choice is not None:
                        if choice == PLAY:
                            self.screens[PLAY].start()
                        # TODO: Not clean ;(
                        elif choice == SETTINGS:
                            self.screens[SETTINGS].last_change = time()
                        self.current = choice
                else:
                    self.screens[self.current].handle_event(event)

        keys = pygame.key.get_pressed()
        self.screens[self.current].handle_keys(keys)

    def update(self):
        """
        Update the situation of all objects depending on the current screen
        """
        dt = self.clock.tick(60)

        self.data.update()
        self.background.update(dt)
        self.screens[self.current].update(dt)

        if self.current == PLAY:
            engine = self.screens[PLAY]
            if engine.running():
                self.panel.update(
                    engine.lives,
                    engine.level,
                    engine.score,
                    max(engine.score, self.data.highscore()),
                )
            else:
                self.data.add_score(self.config.name, engine.score, engine.level)
                self.current = GAMEOVER

    def run(self):
        """
        Run the game instance
        """
        while True:
            self.handle_inputs()
            self.update()
            self.draw()
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        # TODO: Save config
        pygame.quit()
        os._exit(0)
