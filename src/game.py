import os
import pygame
from src.base import Object, Text
from src.graphics import Background
from src.engine import Engine
from src.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    """
    The main game instance,
    it handles all objects and interactions
    """

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load("assets/Icon.png"))
        pygame.display.set_caption("Omega Race")

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.engine = Engine()

        self.running = False

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
            elif self.running:
                self.engine.handle_event(event)

    def update(self):
        """
        Update the situation of all objects
        """
        dt = self.clock.tick(60)
        self.background.update(dt)
        if self.running:
            self.engine.update(dt)

    def run(self):
        """
        Run the game instance
        """
        self.running = True
        while self.running:
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
