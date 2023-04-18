import sys
import pygame
from src.base import Object, Background, Force_Field
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT


class Game:
    """
    class Game:
    """

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load("src/assets/logo.ico"))
        pygame.display.set_caption("Space Invaders")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.force_field = Force_Field()

    def draw(self, *objects: list[Object]):
        for obj in objects:
            obj.draw(self.background.image)
        self.screen.blit(self.background.image, (0, 0))

    def update(self, dt: int, *objects: list[Object]):
        for obj in objects:
            obj.move(dt)
        self.background.move(dt)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            dt = self.clock.tick(60)

            self.update(dt)
            self.draw(self.force_field)
            pygame.display.update()

    def exit(self):
        pygame.quit()
        sys.exit(0)
