import pygame
from time import time
from random import randrange
from src.thread import Timer
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
from src.vector import Vector
from src.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    CEN_Y,
    PAN_HEIGHT,
    PAUSE,
    GAMEOVER,
    ENEMY_NUMBER,
)


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
        self.restart()

    def restart(self):
        """
        Reset the game state, except for score and lives
        """
        self.enemies: list[Ship] = (
            [
                DroidShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT // 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["DroidShip"][min(self.level - 1, 4)])
            ]
            + [
                CommandShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT // 2 + 50, WIN_HEIGHT - 50),
                    self.level,
                )
                for i in range(ENEMY_NUMBER["CommandShip"][min(self.level - 1, 4)])
            ]
            + [
                DeathShip(
                    randrange(300, WIN_WIDTH - 300),
                    randrange(CEN_Y + PAN_HEIGHT // 2 + 50, WIN_HEIGHT - 50),
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

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a single user event

        :param event: pygame.event.Event, The event to handle
        """
        if event.type == pygame.KEYDOWN and event.key == self.config.keys["PAUSE"]:
            self.pause()

    def handle_keys(self):
        """
        Handle user inputs in the game
        """
        if self.config.mouse or not self.can_change():
            return

        keys = pygame.key.get_pressed()
        if keys[self.config.keys["LEFT"]] and not keys[self.config.keys["RIGHT"]]:
            self.player.rotating = "left"
        elif keys[self.config.keys["RIGHT"]] and not keys[self.config.keys["LEFT"]]:
            self.player.rotating = "right"
        else:
            self.player.rotating = ""

        if keys[self.config.keys["UP"]] and self.player.can_thrust():
            self.player.thrust()
            self.player.set_image(Player.create_image(self.config.color, True))
        else:
            self.player.set_image(Player.create_image(self.config.color))

        if keys[self.config.keys["SHOOT"]] and self.player.can_shoot():
            self.player.shoot(self.player_lasers)
            self.mixer.play("Laser", 0.1)

    def handle_mouse(self):
        """
        Handle mouse use in the game
        """
        if not self.config.mouse or not self.can_change():
            return

        pos = Vector(*pygame.mouse.get_pos())
        scaled_pos = pos * (WIN_WIDTH, WIN_HEIGHT) / pygame.display.get_window_size()
        vector = Vector(scaled_pos.x - self.player.x, scaled_pos.y - self.player.y)
        angle = self.player.rotation.angle_to(vector)
        if round(angle, 1) < 0:
            self.player.rotating = "left"
        elif round(angle, 1) > 0:
            self.player.rotating = "right"
        else:
            self.player.rotating = ""

        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.player.can_thrust():
            self.player.thrust()
            self.player.set_image(Player.create_image(self.config.color, True))
        else:
            self.player.set_image(Player.create_image(self.config.color))

        if buttons[2] and self.player.can_shoot():
            self.player.shoot(self.player_lasers)
            self.mixer.play("Laser", 0.1)

        if not pygame.mouse.get_focused():
            self.pause()

    def pause(self):
        """
        Pause the game
        """
        self.choice = PAUSE
        for enemy in self.enemies:
            if isinstance(enemy, CommandShip):
                enemy.shoot_cooldown_pause = time() - enemy.last_shoot
            if isinstance(enemy, (CommandShip, DeathShip)):
                enemy.drop_cooldown_pause = time() - enemy.last_drop

    def unpause(self):
        """
        Unpause the game
        """
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
        self.mixer.play("Explosion", 0.5)

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
            Timer(1, self.restart).start()

    def change_level(self):
        """
        Change the level of the game
        """
        if not self.level_changed and self.player.alive:
            self.level += 1
            self.level_changed = True
            Timer(1, self.restart).start()

    def update_enemies(self, dt: int):
        """
        Update enemies situations

        :param dt: int, The time delta between frames
        """
        for enemy in self.enemies:
            enemy.update(dt)
            if enemy.collide(self.player):
                enemy.die()
                self.player_death()
                self.create_explosion(self.player.x, self.player.y)
                self.score += enemy.points
            if isinstance(enemy, DroidShip) and enemy.can_see(self.player):
                enemy.follow(self.player)
            if isinstance(enemy, CommandShip) and enemy.can_shoot():
                enemy.shoot(self.player, self.enemies_lasers)
                self.mixer.play("Laser", 0.1)
            if isinstance(enemy, (CommandShip, DeathShip)) and enemy.can_drop():
                enemy.drop_mine(self.mines)

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
            laser.update(dt)
            for enemy in self.enemies + self.mines:
                if laser.collide(enemy):
                    laser.die()
                    enemy.die()
                    if isinstance(enemy, Ship):
                        self.ship_death(enemy)
                    self.create_explosion(enemy.x, enemy.y)
                    self.score += enemy.points
                    break

        for laser in self.enemies_lasers:
            laser.update(dt)
            if laser.collide(self.player):
                laser.die()
                self.player_death()
                self.create_explosion(self.player.x, self.player.y)

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

        self.player.update(dt)
        self.update_enemies(dt)
        self.update_mines(dt)
        self.update_lasers(dt)
        self.update_explosions(dt)

        self.force_field.update()
        self.force_field.bounce(
            self.player,
            *self.enemies,
            *self.player_lasers,
            *self.enemies_lasers,
        )

        self.objects = [
            *self.player_lasers,
            *self.enemies_lasers,
            *self.mines,
            *self.enemies,
            self.player,
            *self.explosions,
            self.force_field,
        ]

        # Level cleared
        if all(not enemy.alive for enemy in self.enemies):
            self.change_level()

        # Gameover
        if self.lives < 0 and self.player.alive:
            self.choice = GAMEOVER
