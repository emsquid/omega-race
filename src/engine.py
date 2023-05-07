import pygame
from random import randrange
from threading import Timer
from src.objects.base import Explosion
from src.objects.sprites import Player, Ship, DroidShip, CommandShip, DeathShip
from src.objects.graphics import ForceField
from src.screens import Screen
from src.config import Config
from src.const import WIN_WIDTH, WIN_HEIGHT, CEN_Y, PAN_HEIGHT, ENEMY_NUMBER


# TODO: Add pause
class Engine(Screen):
    """
    The Engine handles the game logic and interactions

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def start(self):
        """
        Completely start the game
        """
        self.level = 1
        self.lives = 3
        self.score = 0
        self.reset()

    def reset(self):
        """
        Reset the game state, except for score and lives
        """
        self.enemies = (
            [
                DroidShip(
                    randrange(200, WIN_WIDTH - 200),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["DroidShip"][min(self.level - 1, 4)])
            ]
            + [
                CommandShip(
                    randrange(200, WIN_WIDTH - 200),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["CommandShip"][min(self.level - 1, 4)])
            ]
            + [
                DeathShip(
                    randrange(200, WIN_WIDTH - 200),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["DeathShip"][min(self.level - 1, 4)])
            ]
        )
        self.mines = []
        self.player_lasers = []
        self.enemies_lasers = []
        self.explosions = []
        self.player = Player()

        self.force_field = ForceField()

        self.level_changed = False

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the game

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            self.player.rotating = "LEFT"
        elif keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            self.player.rotating = "RIGHT"
        else:
            self.player.rotating = ""

        if keys[self.config.keys["UP"]]:
            self.player.thrust()
            self.player.set_image("Player2.png")
        else:
            self.player.set_image("Player1.png")

        if keys[self.config.keys["SHOOT"]]:
            self.player.shoot(self.player_lasers)

    def ship_death(self, ship: Ship):
        """
        Handle ship death
        Transfrom another ship into a better ship when one dies

        :param ship: Ship, The ship that died
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
                    self.enemies[i] = transform
                    break

    def player_death(self):
        """
        Handle player death
        """
        if not self.level_changed and self.player.alive:
            self.lives -= 1
            self.player.die()
            Timer(0.7, self.reset).start()

    def change_level(self):
        """
        Change the level of the game
        """
        if not self.level_changed and self.player.alive:
            self.level += 1
            self.level_changed = True
            Timer(0.7, self.reset).start()

    def update_enemies(self, dt: int):
        """
        Update enemies situations

        :param dt: int, The time delta between frames
        """
        for enemy in self.enemies:
            if enemy.collide(self.player):
                enemy.die()
                self.player_death()
                self.explosions.append(Explosion(self.player.x, self.player.y))
                self.score += enemy.points
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

        :param dt: int, The time delta between frames
        """
        for mine in self.mines:
            if mine.collide(self.player):
                mine.die()
                self.player_death()
                self.explosions.append(Explosion(self.player.x, self.player.y))
                self.score += mine.points

    def update_lasers(self, dt: int):
        """
        Update lasers situations

        :param dt: int, The time delta between frames
        """
        for laser in self.player_lasers:
            for enemy in self.enemies + self.mines:
                if laser.collide(enemy):
                    laser.die()
                    enemy.die()
                    if enemy in self.enemies:
                        self.ship_death(enemy)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    self.score += enemy.points
                    break
            laser.move(dt)

        for laser in self.enemies_lasers:
            if laser.collide(self.player):
                laser.die()
                self.player_death()
                self.explosions.append(Explosion(self.player.x, self.player.y))
            laser.move(dt)

    def update_explosions(self, dt: int):
        """
        Update explosions situations

        :param dt: int, The time delta between frames
        """
        for explosion in self.explosions:
            explosion.update()

    def update(self, dt: int):
        """
        Update the game instance

        :param dt: int, The time delta between frames
        """
        self.update_enemies(dt)
        self.update_mines(dt)
        self.update_lasers(dt)
        self.update_explosions(dt)

        self.player.move(dt)
        self.force_field.update()
        self.force_field.bounce(
            self.player,
            *self.enemies,
            *self.player_lasers,
            *self.enemies_lasers,
        )

        self.objects = [
            self.force_field,
            *self.mines,
            *self.enemies,
            self.player,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.explosions,
        ]

        if all(not enemy.alive for enemy in self.enemies):
            self.change_level()

    def running(self) -> bool:
        """
        Check if the game is still considered running

        :return: bool, Whether the game is running or not
        """
        return self.lives >= 0 or not self.player.alive
