import pygame
from random import randrange
from threading import Timer
from src.base import Object, Explosion
from src.graphics import ForceField
from src.sprites import Player, Ship, DroidShip, CommandShip, DeathShip
from src.settings import Settings
from src.const import ENEMY_NUMBER


class Engine:
    """
    The Engine handles the game logic and interactions
    """

    def __init__(self):
        pass

    def start(self):
        self.level = 1
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
                for i in range(ENEMY_NUMBER["DroidShip"][self.level - 1])
            ]
            + [
                CommandShip(randrange(200, 800), randrange(550, 750), self.level)
                for i in range(ENEMY_NUMBER["CommandShip"][self.level - 1])
            ]
            + [
                DeathShip(randrange(200, 800), randrange(550, 750), self.level)
                for i in range(ENEMY_NUMBER["DeathShip"][self.level - 1])
            ]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []
        self.explosions = []

        self.force_field = ForceField()

        self.level_changed = False

    def get_objects(self) -> list[Object]:
        """
        Return a list with every object handled by the engine
        """
        return [
            self.force_field,
            *self.mines,
            *self.enemies,
            self.player,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.explosions,
        ]

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
        """
        Handle user inputs in the game
        """
        if keys[settings.keys["LEFT"]] and not keys[settings.keys["RIGHT"]]:
            self.player.rotating = "left"
        elif keys[settings.keys["RIGHT"]] and not keys[settings.keys["LEFT"]]:
            self.player.rotating = "right"
        else:
            self.player.rotating = ""
        if keys[settings.keys["UP"]]:
            self.player.thrust()
            self.player.set_image("Player2.png")
        else:
            self.player.set_image("Player1.png")
        if keys[settings.keys["SHOOT"]]:
            self.player.shoot(self.player_lasers)

    def ship_death(self, ship: Ship):
        """
        Handle ship death
        Transfrom another ship into a better ship when one dies
        """
        if isinstance(ship, CommandShip):
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                if enemy.alive and isinstance(enemy, DroidShip):
                    transform = CommandShip(enemy.x, enemy.y, self.level)
                    transform.set_direction(enemy.direction)
                    self.enemies[i] = transform
                    break
        elif isinstance(ship, DeathShip):
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                if enemy.alive and isinstance(enemy, CommandShip):
                    transform = DeathShip(enemy.x, enemy.y, self.level)
                    transform.set_direction(enemy.direction)
                    self.enemies[i] = transform
                    break

    def player_death(self):
        """
        Handle player death
        """
        if self.player.alive:
            self.lives -= 1
            self.player.die()
            Timer(0.7, self.reset).start()

    def change_level(self):
        if not self.level_changed:
            self.level = min(self.level + 1, 5)
            self.level_changed = True
            Timer(0.7, self.reset).start()

    def update_enemies(self, dt: int):
        """
        Update enemies situations
        """
        for enemy in self.enemies:
            if enemy.collide(self.player):
                enemy.die()
                self.player_death()
                self.score += enemy.points
                self.explosions.append(Explosion(self.player.x, self.player.y))
            if isinstance(enemy, (DroidShip, CommandShip)):
                enemy.turn()
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
            if mine.collide(self.player):
                mine.die()
                self.player_death()
                self.score += mine.points
                self.explosions.append(Explosion(self.player.x, self.player.y))

    def update_lasers(self, dt: int):
        """
        Update lasers situations
        """
        for laser in self.player_lasers:
            for enemy in self.enemies + self.mines:
                if laser.collide(enemy):
                    laser.die()
                    enemy.die()
                    self.score += enemy.points
                    if enemy in self.enemies:
                        self.ship_death(enemy)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    break
            laser.move(dt)

        for laser in self.enemies_lasers:
            if laser.collide(self.player):
                laser.die()
                self.player_death()
                self.explosions.append(Explosion(self.player.x, self.player.y))
            laser.move(dt)

    def update(self, dt: int):
        """
        Update the game instance
        """
        self.update_enemies(dt)
        self.update_mines(dt)
        self.update_lasers(dt)

        self.player.move(dt)
        self.force_field.bounce(self.player, *self.enemies)
        self.force_field.crash(*self.player_lasers, *self.enemies_lasers)

        if all(not enemy.alive for enemy in self.enemies):
            self.change_level()

    def running(self) -> bool:
        return self.lives >= 0 or not self.player.alive
