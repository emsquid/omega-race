import os
import pygame
from random import randrange
from src.base import Object
from src.graphics import Background, ForceField
from src.sprites import (
    Player,
    DroidShip,
    CommandShip,
    DeathShip,
)
from src.const import WIN_WIDTH, WIN_HEIGHT, WHITE


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
        self.force_field = ForceField()

        self.player = Player()
        self.enemies = (
            [DroidShip(randrange(200, 800), randrange(550, 750)) for i in range(4)]
            + [CommandShip(randrange(200, 800), randrange(550, 750)) for i in range(2)]
            + [DeathShip(randrange(200, 800), randrange(550, 750)) for i in range(1)]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []

        self.running = False

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.rotating = "left"
                elif event.key == pygame.K_RIGHT:
                    self.player.rotating = "right"
                elif event.key == pygame.K_UP and self.player.can_thrust():
                    self.player.thrust()
                elif event.key == pygame.K_SPACE and self.player.can_shoot():
                    self.player.shoot(self.player_lasers)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.rotating == "left":
                    self.player.rotating = ""
                elif event.key == pygame.K_RIGHT and self.player.rotating == "right":
                    self.player.rotating = ""

    def draw(self, *objects: tuple[Object]):
        """
        Draw the objects on top of the background and display it
        """
        for obj in objects:
            obj.draw(self.background.image)
        game = pygame.transform.scale(self.background.image, self.screen.get_size())
        self.screen.blit(game, (0, 0))

    def update(self):
        """
        Update the situation of all objects
        """
        dt = self.clock.tick(60)

        self.player.move(dt)
        self.force_field.bounce(self.player)

        for enemy in self.enemies:
            enemy.move(dt)
            self.force_field.bounce(enemy)
            if self.player.collide(enemy):
                self.player.killed()
                enemy.explode()
                self.enemies.remove(enemy)
            if isinstance(enemy, CommandShip) and enemy.can_shoot():
                enemy.shoot(self.player, self.enemies_lasers)
            if isinstance(enemy, (CommandShip, DeathShip)) and enemy.can_drop():
                enemy.drop_mine(self.mines)

        for mine in self.mines:
            if self.player.collide(mine):
                mine.explode()
                self.mines.remove(mine)

        self.force_field.crash(self.player_lasers)
        for laser in self.player_lasers:
            laser.move(dt)
            for enemy in self.enemies + self.mines:
                if laser.collide(enemy):
                    self.player.kill(enemy)
                    enemy.explode()
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    else:
                        self.mines.remove(enemy)
                    self.player_lasers.remove(laser)
                    break

        self.force_field.crash(self.enemies_lasers)
        for laser in self.enemies_lasers:
            laser.move(dt)
            if laser.collide(self.player):
                laser.explode()
                self.enemies_lasers.remove(laser)

        self.background.move(dt)

        font = pygame.font.Font('assets/font1.ttf', 25)
        score_text = font.render("Score", True, WHITE)
        score = font.render(f'{self.player.score}',True,WHITE)
        self.background.image.blit(score_text, (330, 320))
        self.background.image.blit(score, (330,350))

    def run(self):
        """
        Run the game instance to make it playable
        """
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw(
                self.force_field,
                self.player,
                *self.enemies,
                *self.mines,
                *self.player_lasers,
                *self.enemies_lasers,
            )
            pygame.display.update()

    def exit(self):
        """
        Close the window and exit the program
        """
        pygame.quit()
        os._exit(0)
