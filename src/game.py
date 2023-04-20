import sys
import pygame
from src.base import Object, Background
from src.force_field import ForceField
from src.sprite import Player, CommandShip, VaporMine, DeathShip
from src.const import WIN_WIDTH, WIN_HEIGHT
from threading import Timer

class Game:
    """
    The main game instance,
    it handles all objects and interactions
    """

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(pygame.image.load("src/assets/logo.ico"))
        pygame.display.set_caption("Space Invaders")

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.force_field = ForceField()

    def draw(self, *objects: list[Object]):
        """
        Draw the objects on top of the background and display it
        """
        for obj in objects:
            obj.draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
        self.screen.blit(game, (0, 0))

    def update(self, *objects: list[Object]):
        """
        Update the situation of all objects
        """
        dt = self.clock.tick(60)
        for obj in objects:
            obj.move(dt)
            self.force_field.bounce(obj)
        self.background.move(dt)

    def run(self):
        """
        Run the game instance to make it playable
        """
        ship = CommandShip(50, 600)
        mine = VaporMine(100, 100)
        enemies = [ship, mine]   
        Timer(5.0,ship.drop_mine, [enemies]).start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            self.update(*enemies)
            self.draw(self.force_field, *enemies)
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        sys.exit(0)
