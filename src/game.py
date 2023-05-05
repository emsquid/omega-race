import os
import pygame
from time import time
from src.base import Object, Text
from src.menu import Home, GameOver
from src.engine import Engine
from src.graphics import Background, Panel
from src.scores import Scores
from src.settings import Settings
from src.const import WIN_WIDTH, WIN_HEIGHT, WHITE


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

        self.home = Home()
        self.engine = Engine()
        self.gameover = GameOver()
        self.scores = Scores()
        self.settings = Settings()

        self.is_home = False
        self.is_play = False
        self.is_gameover = False
        self.is_scores = False
        self.is_settings = False

    def draw(self, *objects: tuple[Object]):
        """
        Draw the objects on top of the background and display it

        :param *objects: tuple[Object], objects to draw
        """
        for obj in objects:
            obj.draw(self.background.image)
        Text(str(int(self.clock.get_fps())), 55, 40, WHITE).draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
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
                    if self.is_home:
                        if self.home.selection == 0:
                            self.play_screen()
                        elif self.home.selection == 1:
                            self.scores_screen()
                        elif self.home.selection == 2:
                            self.settings.last_change=time()
                            self.settings_screen()
                    elif self.is_settings:
                        if self.settings.selection == 5:
                            self.home_screen()
                    elif self.is_gameover:
                        if self.gameover.selection == 0:
                            self.play_screen()
                        elif self.gameover.selection == 1:
                            self.home_screen()
                elif self.is_settings:
                    self.settings.handle_events(event.key)

        keys = pygame.key.get_pressed()
        if self.is_home:
            self.home.handle_keys(keys, self.settings)
        elif self.is_play:
            self.engine.handle_keys(keys, self.settings)
        elif self.is_gameover:
            self.gameover.handle_keys(keys, self.settings)
        elif self.is_scores:
            self.scores.handle_keys(keys, self.settings)
        elif self.is_settings:
            self.settings.handle_keys(keys, self.settings)

    def update(self):
        """
        Update the situation of all objects depending on the current screen
        """
        dt = self.clock.tick(1000)
        self.background.update(dt)
        if self.is_home:
            pass
        if self.is_play:
            if self.engine.running():
                self.scores.update(self.engine.score)
                self.panel.update(
                    self.engine.lives,
                    self.engine.level,
                    self.engine.score,
                    self.scores.highscore,
                )
                self.engine.update(dt)
            else:
                self.gameover_screen()
        if self.is_gameover:
            pass
        if self.is_scores:
            pass
        if self.is_settings:
            pass

    def run(self):
        """
        Run the game instance
        """
        self.home_screen()

    def home_screen(self):
        """
        Home screen can lead you to play, scores and settings
        """
        self.is_home = True
        self.is_play, self.is_gameover, self.is_scores, self.is_settings = [False] * 4
        while self.is_home:
            self.handle_inputs()
            self.update()
            self.draw(*self.home.get_objects())
            pygame.display.update()

    def play_screen(self):
        """
        Play screen let you play the super cool game we made
        """
        self.engine.restart()
        self.is_play = True
        self.is_home, self.is_gameover, self.is_scores, self.is_settings = [False] * 4
        while self.is_play:
            self.handle_inputs()
            self.update()
            self.draw(*self.engine.get_objects(), self.panel)
            pygame.display.update()

    def gameover_screen(self):
        """
        GameOver screen let you play again or go back home after a loss
        """
        self.is_gameover = True
        self.is_home, self.is_play, self.is_scores, self.is_settings = [False] * 4
        while self.is_gameover:
            self.handle_inputs()
            self.update()
            self.draw(*self.gameover.get_objects(), self.panel)
            pygame.display.update()

    def scores_screen(self):
        """
        Scores screen is the hall of fame
        """
        self.is_scores = True
        self.is_home, self.is_gameover, self.is_play, self.is_settings = [False] * 4
        while self.is_scores:
            self.handle_inputs()
            self.update()
            self.draw(*self.scores.get_objects())
            pygame.display.update()

    def settings_screen(self):
        """
        Settings screen let you change your configuration
        """
        self.is_settings = True
        self.is_home, self.is_gameover, self.is_play, self.is_scores = [False] * 4
        while self.is_settings:
            self.handle_inputs()
            self.update()
            self.draw(*self.settings.get_objects())
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        os._exit(0)
