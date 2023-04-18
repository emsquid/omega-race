import sys
import pygame
from src.base import Object
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT


class Game:
    """
    class Game:


    """

    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_icon(pygame.image.load("src/assets/logo.ico"))
        pygame.display.set_caption("Space Invaders")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw(self, **objects: list[Object]) -> None:
        pass

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            pygame.display.update()

    def exit(self) -> None:
        pygame.quit()
        sys.exit(0)
