import os
import pygame
from time import time
from src.base import Object, Text
from src.menu import Welcome, Home, GameOver
from src.engine import Engine
from src.graphics import Background, Panel
from src.scores import Scores
from src.settings import Settings
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

        pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
        pygame.display.set_caption("Omega Race")

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.panel = Panel()

        self.welcome = Welcome()
        self.home = Home()
        self.engine = Engine()
        self.gameover = GameOver()
        self.scores = Scores()
        self.settings = Settings()

        self.current_screen = WELCOME

        self.name = ""

    def draw(self):
        """
        Draw the game objects on top of the background and display it
        """
        if self.current_screen == WELCOME:
            objects = self.welcome.get_objects()
        elif self.current_screen == HOME:
            objects = self.home.get_objects()
        elif self.current_screen == PLAY:
            objects = self.engine.get_objects() + (self.panel,)
        elif self.current_screen == SCORES:
            objects = self.scores.get_objects()
        elif self.current_screen == SETTINGS:
            objects = self.settings.get_objects()
        elif self.current_screen == GAMEOVER:
            objects = self.gameover.get_objects() + (self.panel,)
        else:
            objects = ()

        game = self.background.image
        for obj in objects:
            obj.draw(game)
        # TODO: Remove that when done
        Text(str(int(self.clock.get_fps())), 55, 40).draw(game)
        game = pygame.transform.smoothscale(game, self.screen.get_size())
        self.screen.blit(game, (0, 0))

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
                    if self.current_screen == WELCOME and self.welcome.name != "":
                        self.name = self.welcome.name
                        self.home_screen()
                    elif self.current_screen == HOME:
                        if self.home.selection == 0:
                            self.play_screen()
                        elif self.home.selection == 1:
                            self.scores_screen()
                        elif self.home.selection == 2:
                            self.settings.last_change = time()
                            self.settings_screen()
                    elif self.current_screen == SCORES:
                        self.home_screen()
                    elif self.current_screen == SETTINGS:
                        if self.settings.selection == 5:
                            self.home_screen()
                    elif self.current_screen == GAMEOVER:
                        if self.gameover.selection == 0:
                            self.play_screen()
                        elif self.gameover.selection == 1:
                            self.home_screen()
                elif self.current_screen == WELCOME:
                    self.welcome.handle_event(event)
                elif self.current_screen == SETTINGS:
                    self.settings.handle_event(event)

        keys = pygame.key.get_pressed()
        if self.current_screen == HOME:
            self.home.handle_keys(keys, self.settings)
        elif self.current_screen == PLAY:
            self.engine.handle_keys(keys, self.settings)
        elif self.current_screen == SETTINGS:
            self.settings.handle_keys(keys, self.settings)
        elif self.current_screen == GAMEOVER:
            self.gameover.handle_keys(keys, self.settings)

    def update(self):
        """
        Update the situation of all objects depending on the current screen
        """
        dt = self.clock.tick(1000)
        self.background.update(dt)
        if self.current_screen == WELCOME:
            self.welcome.update()
        elif self.current_screen == HOME:
            self.home.update()
        elif self.current_screen == PLAY:
            if self.engine.running():
                self.panel.update(
                    self.engine.lives,
                    self.engine.level,
                    self.engine.score,
                    max(self.engine.score, self.scores.highscore()),
                )
                self.engine.update(dt)
            else:
                self.scores.add_score(self.name, self.engine.score, self.engine.level)
                self.gameover_screen()
        elif self.current_screen == SCORES:
            self.scores.update()
        elif self.current_screen == SETTINGS:
            self.settings.update()
        elif self.current_screen == GAMEOVER:
            self.gameover.update()

    def run(self):
        """
        Run the game instance
        """
        self.welcome_screen()
        while True:
            self.handle_inputs()
            self.update()
            self.draw()
            pygame.display.update()

    def welcome_screen(self):
        """
        Welcome screen to get player's name
        """
        self.current_screen = WELCOME

    def home_screen(self):
        """
        Home screen can lead you to play, scores and settings
        """
        self.current_screen = HOME

    def play_screen(self):
        """
        Play screen let you play the super cool game we made
        """
        self.engine.start()
        self.current_screen = PLAY

    def scores_screen(self):
        """
        Scores screen is the hall of fame
        """
        self.current_screen = SCORES

    def settings_screen(self):
        """
        Settings screen let you change your configuration
        """
        self.current_screen = SETTINGS

    def gameover_screen(self):
        """
        GameOver screen let you play again or go back home after a loss
        """
        self.current_screen = GAMEOVER

    def exit(self):
        """
        Close the window and exit the program
        """
        # TODO: Save settings
        pygame.quit()
        os._exit(0)
