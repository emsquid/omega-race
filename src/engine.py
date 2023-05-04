import pygame
from random import randrange
from src.base import Object, Explosion
from src.graphics import ForceField, Panel
from src.sprites import Player, Ship, DroidShip, CommandShip, DeathShip
from src.const import ENEMY_NUMBER


class Engine:
    """
    The Engine handles the game logic and interactions
    """

    def __init__(self):
        pass

    def start(self):
        self.level = 0
        self.lives = 3
        self.score = 0
        self.reset()

    def reset(self):
        """
        Reset the game state, except for score and lives
        """
        self.player = Player()
        self.enemies = (
            [
                DroidShip(randrange(200, 800), randrange(550, 750), self.level)
                for i in range(ENEMY_NUMBER["DroidShip"][self.level])
            ]
            + [
                CommandShip(randrange(200, 800), randrange(550, 750), self.level)
                for i in range(ENEMY_NUMBER["CommandShip"][self.level])
            ]
            + [
                DeathShip(randrange(200, 800), randrange(550, 750), self.level)
                for i in range(ENEMY_NUMBER["DeathShip"][self.level])
            ]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []
        self.explosions = []

        self.panel = Panel()
        self.force_field = ForceField()

    def change_level(self):
        self.level += 1
        self.reset()

    def get_objects(self) -> list[Object]:
        """
        Return a list with every object handled by the engine
        """
        return (
            self.panel,
            self.force_field,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.mines,
            *self.enemies,
            self.player,
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

    def ship_death(self, ship: Ship):
        """
        Handle ship death
        Transfrom another ship into a better ship when one dies
        """
        self.enemies.remove(ship)
        if isinstance(ship, CommandShip):
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                if isinstance(enemy, DroidShip):
                    self.enemies[i] = CommandShip(enemy.x, enemy.y, self.level)
                    break
        elif isinstance(ship, DeathShip):
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                if isinstance(enemy, CommandShip):
                    self.enemies[i] = DeathShip(enemy.x, enemy.y, self.level)
                    break

    def player_death(self):
        """
        Handle player death from the given enemy
        """
        # TODO: Handle player final death
        self.lives -= 1
        self.reset()

    def update_enemies(self, dt: int):
        """
        Update enemies situations
        """
        for enemy in self.enemies:
            if self.player.collide(enemy):
                self.player_death()
                self.score += enemy.points
                # self.explosions.append(Explosion(enemy.x, enemy.y))
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
                self.player_death()
                self.score += mine.points
                # self.explosions.append(Explosion(mine.x, mine.y))

    def update_lasers(self, dt: int):
        """
        Update lasers situations
        """
        for laser in self.player_lasers:
            for enemy in self.enemies + self.mines:
                if enemy.collide(laser):
                    self.score += enemy.points
                    if enemy in self.enemies:
                        self.ship_death(enemy)
                    else:
                        self.mines.remove(enemy)
                    self.player_lasers.remove(laser)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    break
            laser.move(dt)

        for laser in self.enemies_lasers:
            if self.player.collide(laser):
                self.player_death()
                # self.explosions.append(Explosion(self.player.x, self.player.y))
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

        if len(self.enemies) == 0:
            self.change_level()
