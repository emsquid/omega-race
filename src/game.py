import sys
import pygame
from src.base import Object, Background, Force_Field
from src.ship import Ship
from src.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    """
    class Game:
    """

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load("src/assets/logo.ico"))
        pygame.display.set_caption("Space Invaders")

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.force_field = Force_Field()

    def draw(self, *objects: list[Object]):
        for obj in objects:
            obj.draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
        self.screen.blit(game, (0, 0))

    def update(self, dt: int, *objects: list[Object]):
        for obj in objects:
            obj.move(dt)
            self.force_field.bounce(obj)
        self.background.move(dt)

    def run(self):
        ship = Ship(20, 20, 40, 40, 0.1, 0.2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            dt = self.clock.tick(60)

            self.update(dt, ship)
            self.draw(self.force_field, ship)
            pygame.display.update()

    def exit(self):
        pygame.quit()
        sys.exit(0)
