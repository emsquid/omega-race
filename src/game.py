import os
import pygame
from threading import Timer
from src.base import Object
from src.graphics import Background, ForceField
from src.sprite import (
    Player,
    Mine,
    PhotonMine,
    VaporMine,
    Ship,
    DroidShip,
    CommandShip,
    DeathShip,
)
from src.const import WIN_WIDTH, WIN_HEIGHT


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

    def update(self, *objects: tuple[Object]):
        """
        Update the situation of all objects
        """
        player = [obj for obj in objects if isinstance(obj, Player)][0]
        mines = [obj for obj in objects if isinstance(obj, Mine)]
        ships = [obj for obj in objects if isinstance(obj, Ship)]

        # for obj in objects:
        # if obj.state == "Dead":
        # del obj

        dt = self.clock.tick(60)
        for obj in objects:
            obj.move(dt)
            self.force_field.bounce(obj)
        self.background.move(dt)

        for obj in mines + ships:
            if player.collide(obj):
                obj.explode()

    def run(self):
        """
        Run the game instance to make it playable
        """
        player = Player()
        enemies = [
            PhotonMine(800, 200),
            VaporMine(100, 100),
            DroidShip(500, 600),
            CommandShip(170, 265),
            DeathShip(50, 600),
        ]
        for enemy in enemies:
            if type(enemy) == DeathShip or type(enemy) == CommandShip:
                Timer(5.0, enemy.drop_mine, [enemies]).start()
                            
        Timer(5.0, enemies[0].explode).start()
        Timer(4.0, enemies[3].shoot, [player,enemies]).start()   
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
