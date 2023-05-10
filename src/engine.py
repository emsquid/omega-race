import pygame
from time import time
from random import randrange
from threading import Timer
from src.objects.base import Explosion
from src.objects.sprites import (
    Player,
    Ship,
    DroidShip,
    CommandShip,
    DeathShip,
    Mine,
    Laser,
)
from src.objects.graphics import ForceField
from src.screens import Screen
from src.config import Config
from src.mixer import Mixer
from src.const import WIN_WIDTH, WIN_HEIGHT, CEN_Y, PAN_HEIGHT, ENEMY_NUMBER


class Engine(Screen):
    """
    The Engine handles the game logic and interactions

    :param config: Config, The game configuration
    :param mixer: Mixer, The game mixer for music and sounds
    """

    def __init__(self, config: Config, mixer: Mixer):
        super().__init__(config, mixer)

    def start(self):
        """
        Completely start the game
        """
        self.level = 1
        self.lives = 3
        self.score = 0
        self.paused = False
        self.reset()

    def reset(self):
        """
        Reset the game state, except for score and lives
        """
        self.enemies: list[Ship] = (
            [
                DroidShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["DroidShip"][min(self.level - 1, 4)])
            ]
            + [
                CommandShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["CommandShip"][min(self.level - 1, 4)])
            ]
            + [
                DeathShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT / 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["DeathShip"][min(self.level - 1, 4)])
            ]
        )
        self.mines: list[Mine] = []
        self.player_lasers: list[Laser] = []
        self.enemies_lasers: list[Laser] = []
        self.explosions: list[Explosion] = []
        self.player = Player(self.config.color)

        self.force_field = ForceField()

        self.level_changed = False

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """
        Handle user inputs in the game

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        if self.paused:
            return

        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            self.player.rotating = "LEFT"
        elif keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            self.player.rotating = "RIGHT"
        else:
            self.player.rotating = ""

        if keys[self.config.keys["UP"]] and self.player.can_thrust():
            self.player.thrust()
            self.player.set_image(Player.create_image(self.config.color, True))
        else:
            self.player.set_image(Player.create_image(self.config.color))

        if keys[self.config.keys["SHOOT"]] and self.player.can_shoot():
            self.player.shoot(self.player_lasers)
            self.mixer.play("Laser.wav", 0.15)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single user event

        :param event: pygame.event.Event, The event (key) that was pressed
        """
        if (
            not self.level_changed
            and self.player.alive
            and event.type == pygame.KEYDOWN
            and event.key == self.config.keys["PAUSE"]
        ):
            if not self.paused:
                self.pause()
            else:
                self.unpause()

    def pause(self):
        """
        Pause the game
        """
        self.paused = True
        for enemy in self.enemies:
            if isinstance(enemy, CommandShip):
                enemy.shoot_cooldown_pause = time() - enemy.last_shoot
            if isinstance(enemy, (CommandShip, DeathShip)):
                enemy.drop_cooldown_pause = time() - enemy.last_drop

    def unpause(self):
        """
        Unpause the game
        """
        self.paused = False
        for enemy in self.enemies:
            if isinstance(enemy, CommandShip):
                enemy.last_shoot = time() - enemy.shoot_cooldown_pause
            if isinstance(enemy, (CommandShip, DeathShip)):
                enemy.last_drop = time() - enemy.drop_cooldown_pause

    def create_explosion(self, x: int, y: int):
        """
        Create an explosion

        :param x: int, The x coordinate of the explosion
        :param y: int, The y coordinate of the explosion
        """
        self.explosions.append(Explosion(x, y))
        self.mixer.play("Explosion.wav", 1)

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
                self.create_explosion(self.player.x, self.player.y)
                self.score += enemy.points
            if isinstance(enemy, DroidShip) and enemy.can_see(self.player):
                enemy.follow(self.player)
            if isinstance(enemy, CommandShip) and enemy.can_shoot():
                enemy.shoot(self.player, self.enemies_lasers)
                self.mixer.play("Laser.wav", 0.15)
            if isinstance(enemy, (CommandShip, DeathShip)) and enemy.can_drop():
                enemy.drop_mine(self.mines)
            enemy.update(dt)

    def update_mines(self, dt: int):
        """
        Update mines situations

        :param dt: int, The time delta between frames
        """
        for mine in self.mines:
            if mine.collide(self.player):
                mine.die()
                self.player_death()
                self.create_explosion(self.player.x, self.player.y)
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
                    self.create_explosion(enemy.x, enemy.y)
                    self.score += enemy.points
                    break
            laser.update(dt)

        for laser in self.enemies_lasers:
            if laser.collide(self.player):
                laser.die()
                self.player_death()
                self.create_explosion(self.player.x, self.player.y)
            laser.update(dt)

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
        if self.paused:
            return

        self.update_enemies(dt)
        self.update_mines(dt)
        self.update_lasers(dt)
        self.update_explosions(dt)

        self.player.update(dt)
        self.force_field.update()
        self.force_field.bounce(
            self.player,
            *self.enemies,
            *self.player_lasers,
            *self.enemies_lasers,
        )

        self.objects = [
            self.force_field,
            *self.player_lasers,
            *self.enemies_lasers,
            *self.mines,
            *self.enemies,
            self.player,
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
