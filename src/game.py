import os
import pygame
from src.base import Object
from src.graphics import Background, ForceField
from src.sprite import Player, PhotonMine, VaporMine, DroidShip, CommandShip, DeathShip
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

    def handle_events(self, player: Player):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            else:
                player.handle_event(event)

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
        player = Player()
        enemies = [
            PhotonMine(800, 200),
            VaporMine(100, 100),
            DroidShip(500, 600),
            CommandShip(700, 650),
            DeathShip(50, 600),
        ]
        Timer(5.0, enemies[3].drop_mine, [enemies]).start()
        while True:
            self.handle_events(player)
            self.update(player, *enemies)
            self.draw(self.force_field, player, *enemies)
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        os._exit(0)
