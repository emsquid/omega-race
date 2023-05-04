import os
import pygame
from src.base import Object
from src.menu import Home, GameOver
from src.engine import Engine
from src.graphics import Background
from src.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    """
    The main game instance
    """

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
        pygame.display.set_caption("Omega Race")

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.home = Home()
        self.engine = Engine()
        self.gameover = GameOver()

        self.is_home = False
        self.is_playing = False
        self.is_gameover = False

    def draw(self, *objects: tuple[Object]):
        """
        Draw the objects on top of the background and display it
        """
        for obj in objects:
            obj.draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
        self.screen.blit(game, (0, 0))

    def handle_inputs(self):
        """
        Handle user events and keypresses
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
                    elif self.is_gameover:
                        if self.gameover.selection == 0:
                            self.play_screen()
                        elif self.gameover.selection == 1:
                            self.home_screen()

        keys = pygame.key.get_pressed()
        if self.is_home:
            self.home.handle_keys(keys)
        elif self.is_playing:
            self.engine.handle_keys(keys)
        elif self.is_gameover:
            self.gameover.handle_keys(keys)

    def update(self):
        """
        Update the situation of all objects
        """
        dt = self.clock.tick(60)
        self.background.update(dt)
        if self.is_home:
            pass
        if self.is_playing:
            if not self.engine.ended():
                self.engine.update(dt)
            else:
                self.gameover_screen()
        if self.is_gameover:
            pass

    def run(self):
        """
        Run the game instance
        """
        # self.home_screen()
        self.gameover_screen()

    def home_screen(self):
        """
        Home screen can lead you to play, scores and settings
        """
        self.is_home = True
        self.is_playing, self.is_gameover = False, False
        while self.is_home:
            self.handle_inputs()
            self.update()
            self.draw(*self.home.get_objects())
            pygame.display.update()

    def play_screen(self):
        """
        The war basically
        """
        self.engine.start()
        self.is_playing = True
        self.is_home, self.is_gameover = False, False
        while self.is_playing:
            self.handle_inputs()
            self.update()
            self.draw(*self.engine.get_objects())
            pygame.display.update()

    def gameover_screen(self):
        """
        Sadge you lost
        """
        self.is_gameover = True
        self.is_home, self.is_playing = False, False
        while self.is_gameover:
            self.handle_inputs()
            self.update()
            self.draw(*self.gameover.get_objects())
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        os._exit(0)
