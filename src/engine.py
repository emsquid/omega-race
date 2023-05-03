import pygame
import math
from random import randrange
from src.base import Object, Explosion
from src.graphics import ForceField, Panel
from src.sprites import Player, Ship, DroidShip, CommandShip, DeathShip


class Engine:
    """
    The Engine handles the game logic and interactions
    """

    def __init__(self):
        self.restart()
        self.lives = 3
        self.score = 0

    def restart(self):
        self.player = Player()
        self.enemies = (
            [DroidShip(randrange(200, 800), randrange(550, 750)) for i in range(4)]
            + [CommandShip(randrange(200, 800), randrange(550, 750)) for i in range(2)]
            + [DeathShip(randrange(200, 800), randrange(550, 750)) for i in range(1)]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []
        self.explosions = []

        self.panel = Panel()
        self.force_field = ForceField()

    def get_objects(self) -> list[Object]:
        """
        Return a list with every object handled by the engine
        """
        return (
            self.player,
            self.panel,
            self.force_field,
            *self.mines,
            *self.enemies,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.explosions,
        )

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the game
        """
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player.rotating = "left"
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.player.rotating = "right"
        else:
            self.player.rotating = ""
        if keys[pygame.K_UP]:
            self.player.thrust()
            self.player.set_image("Player2.png")
        else:
            self.player.set_image("Player1.png")
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_lasers)

    def transform(self, ship: Ship):
        """ """
        if isinstance(ship, CommandShip):
            for enemy in self.enemies:
                if isinstance(enemy, DroidShip):
                    self.enemies.remove(enemy)
                    self.enemies.append(CommandShip(enemy.x, enemy.y))
                    break
        elif isinstance(ship, DeathShip):
            for enemy in self.enemies:
                if isinstance(enemy, CommandShip):
                    self.enemies.remove(enemy)
                    self.enemies.append(DeathShip(enemy.x, enemy.y))
                    break

    def update_enemies(self, dt: int):
        """
        Update enemies situations
        """
        # TODO: player death
        for enemy in self.enemies:
            if self.player.collide(enemy):
                self.lives -= 1
                self.score += enemy.points
                # self.explosions.append(Explosion(enemy.x, enemy.y))
                self.restart()
            if isinstance(enemy, (DroidShip, CommandShip)):
                enemy.rotate()
            if isinstance(enemy, CommandShip) and enemy.can_shoot():
                enemy.shoot(self.player, self.enemies_lasers)
            if isinstance(enemy, (CommandShip, DeathShip)) and enemy.can_drop():
                enemy.drop_mine(self.mines)
            enemy.move(dt)

    def update_mines(self, dt: int):
        """
        Update mines situations
        """
        for mine in self.mines:
            if self.player.collide(mine):
                self.lives -= 1
                self.score += mine.points
                # self.explosions.append(Explosion(mine.x, mine.y))
                self.restart()

    def update_lasers(self, dt: int):
        """
        Update lasers situations
        """
        for laser in self.player_lasers:
            for enemy in self.enemies + self.mines:
                if enemy.collide(laser):
                    self.score += enemy.points
                    if enemy in self.enemies:
                        self.transform(enemy)
                        self.enemies.remove(enemy)
                    else:
                        self.mines.remove(enemy)
                    self.player_lasers.remove(laser)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    break
            laser.move(dt)

        for laser in self.enemies_lasers:
            if self.player.collide(laser):
                self.lives -= 1
                # self.explosions.append(Explosion(self.player.x, self.player.y))
                self.restart()
            laser.move(dt)

    def update_explosions(self, dt: int):
        """
        Update explosions situations
        """
        for explosion in self.explosions:
            if explosion.done:
                self.explosions.remove(explosion)

    def update(self, dt: int):
        """
        Update the game instance
        """
        # TODO: Clean all updaters
        self.update_enemies(dt)
        self.update_mines(dt)
        self.update_lasers(dt)
        self.update_explosions(dt)

        self.player.move(dt)
        self.panel.update(self.lives, self.score)
        self.force_field.bounce([self.player, *self.enemies])
        self.force_field.crash(self.player_lasers)
        self.force_field.crash(self.enemies_lasers)
