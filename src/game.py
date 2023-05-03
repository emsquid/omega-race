import os
import pygame
from src.base import Object
from src.menu import Home
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

        self.is_home = False
        self.is_playing = False

    def draw(self, *objects: tuple[Object]):
        """
        Draw the objects on top of the background and display it
        """
        for obj in objects:
            obj.draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
        self.screen.blit(game, (0, 0))

    def handle_events(self):
        """
        Handle user inputs
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            elif self.is_home:
                self.home.handle_event(event)
            elif self.is_playing:
                self.engine.handle_event(event)

    def update(self):
        """
        Update the situation of all objects
        """
        dt = self.clock.tick(60)
        self.background.update(dt)
        if self.is_home:
            pass
        if self.is_playing:
            self.engine.update(dt)

    def run(self):
        self.menu()

    def menu(self):
        self.is_home = True
        self.is_playing = False
        while self.is_home:
            self.handle_events()
            self.update()
            self.draw(self.home)
            pygame.display.update()

    def play(self):
        """
        Run the game instance
        """
        self.is_home = False
        self.is_playing = True
        while self.is_playing:
            self.handle_events()
            self.update()
            self.draw(*self.engine.get_objects())
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        os._exit(0)
