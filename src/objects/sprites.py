import pygame
from time import time
from math import pi, atan2, sqrt
from random import randrange, random
from src.objects.base import Entity
from src.const import CEN_X, CEN_Y, PAN_WIDTH, PAN_HEIGHT, WHITE


class Laser(Entity):
    """
    Lasers are the main source of danger in the game

    :param x: int, The x coordinate of the laser
    :param y: int, The x coordinate of the laser
    :param direction: float, The direction (radians)
    """

    def __init__(self, x: int, y: int, direction: float):
        image = pygame.Surface((2, 15), pygame.SRCALPHA)
        image.fill(WHITE)
        super().__init__(x, y, 2, 10, image, direction, direction, 0.3)

        sound = pygame.mixer.Sound("assets/sounds/Laser.wav")
        sound.set_volume(0.25)
        sound.play()


class Player(Entity):
    """
    It's you, you can move, rotate, thrust and shoot, good luck
    """

    def __init__(self):
        super().__init__(500, 200, 31, 31, "Player1.png", -pi / 2, -pi / 2, 0)
        # LEFT | RIGHT
        self.rotating = ""
        self.last_collision = 0
        self.last_shoot = 0

    def can_thrust(self) -> bool:
        """
        Check if the player can thrust

        :return: bool, Whether you can thrust or not
        """
        return self.alive and time() - self.last_collision >= 0.4

    def can_shoot(self) -> bool:
        """
        Check if the player can shoot

        :return: bool, Whether you can shoot or not
        """
        return self.alive and time() - self.last_shoot >= 0.4

    def thrust(self):
        """
        Thrust in the direction the player is pointing
        """
        if self.can_thrust():
            self.speed = 0.2
            self.direction = self.rotation
            self.last_thrust = time()

    def shoot(self, lasers: list[Laser]):
        """
        Shoot a laser

        :param lasers: list[Laser], The lasers already in game
        """
        if self.can_shoot():
            lasers.append(Laser(self.x, self.y, self.rotation))
            self.last_shoot = time()

    def rotate(self, dt: int):
        """
        Rotate the player

        :param dt: int, The time delta between frames
        """
        if self.rotating == "LEFT":
            self.rotation -= dt * pi / 725
        elif self.rotating == "RIGHT":
            self.rotation += dt * pi / 725

    def move(self, dt: int):
        """
        Move and rotate if needed

        :param dt: int, The time delta between frames
        """
        super().move(dt)
        self.rotate(dt)


class Mine(Entity):
    """
    Mines doesn't move, but they still kill the player

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    :param width: int, The width of the mine
    :param height: int, The height coordinate of the mine
    :param image: str | pygame.Surface, The image of the mine
    :param points: int, The points the mine is worth
    """

    def __init__(self, x: int, y: int, width: int, height: int, image, points: int):
        super().__init__(x, y, width, height, image, -pi / 2, -pi / 2, 0)
        self.points = points


class PhotonMine(Mine):
    """
    The Photon Mine is half a Vapor Mine

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 15, 15, "PhotonMine.png", 350)


class VaporMine(Mine):
    """
    The Vapor Mine is twice a Photon Mine

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 25, 25, "VaporMine.png", 500)


class Ship(Entity):
    """
    Ships are the enemies in the games, they will try to kill the player

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param image: str | pygame.Surface, The image of the ship
    :param direction: float, The direction the ship advances towards
    :param speed: float, The speed of the ship
    :param points: int, The points the ship is worth
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(
        self,
        x: int,
        y: int,
        image,
        direction: float,
        speed: float,
        points: int,
        level: int,
    ):
        super().__init__(x, y, 31, 31, image, direction, direction, speed * sqrt(level))
        self.points = points
        self.distance = randrange(50, 250)

    def turn(self):
        """
        Change ship direction when reaching the right distance
        """
        # top left
        if (
            self.x + self.distance < CEN_X - PAN_WIDTH / 2
            and self.y < CEN_Y - PAN_HEIGHT / 2
        ):
            self.set_direction(pi / 2)
        # top right
        if (
            self.x > CEN_X + PAN_WIDTH / 2
            and self.y + self.distance < CEN_Y - PAN_HEIGHT / 2
        ):
            self.set_direction(pi)
        # bottom right
        if (
            self.x - self.distance > CEN_X + PAN_WIDTH / 2
            and self.y > CEN_Y + PAN_HEIGHT / 2
        ):
            self.set_direction(-pi / 2)
        # bottom left
        if (
            self.x < CEN_X - PAN_WIDTH / 2
            and self.y - self.distance > CEN_Y + PAN_HEIGHT / 2
        ):
            self.set_direction(0)

    def rotate(self, dt):
        """
        Rotate the ship

        :param dt: int, The time delta between frames
        """
        self.rotation += pi * dt / 4096

    def move(self, dt: int):
        """
        Move and also rotate

        :param dt: int, The time delta between frames
        """
        super().move(dt)
        self.rotate(dt)


class DroidShip(Ship):
    """
    The Droid Ship doesn't move a lot, but it can transfrom into a CommandShip

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        super().__init__(x, y, "DroidShip.png", 0, 0.01, 1000, level)


class CommandShip(Ship):
    """
    The Command Ship is more dangerous, it moves and fires laser towards the player

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        super().__init__(x, y, "CommandShip.png", 0, 0.05, 1500, level)
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()
        self.shoot_cooldown = randrange(3, 8)
        self.last_shoot = time()
        self.distance = randrange(50, 250)

    def can_drop(self) -> bool:
        """
        Check if the ship can drop a mine

        :return: bool, Whether the ship can drop a mine or not
        """
        return self.alive and time() - self.last_drop >= self.drop_cooldown

    def can_shoot(self) -> bool:
        """
        Check if the ship can shoot

        :return: bool, Whether the ship can shoot or not
        """
        return self.alive and time() - self.last_shoot >= self.shoot_cooldown

    def drop_mine(self, mines: list[Mine]):
        """
        Drop a Photon Mine at the ship's position

        :param mines: list[Mine], The mines already in the game
        """
        mines.insert(0, PhotonMine(self.x, self.y))
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()

    def shoot(self, player: Player, lasers: list[Laser]):
        """
        Shoot a laser towards the player

        :param player: Player, The player to shoot at
        :param lasers: list[Laser]: The lasers already in the game
        """
        direction = atan2(player.y - self.y, player.x - self.x)
        lasers.append(Laser(self.x, self.y, direction))
        self.shoot_cooldown = randrange(3, 8)
        self.last_shoot = time()


class DeathShip(Ship):
    """
    The Death Ship will bounce at full speed on every border

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        super().__init__(x, y, "DeathShip.png", random() * pi * 2, 0.2, 2000, level)
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()

    def can_drop(self) -> bool:
        """
        Check if the ship can drop a mine

        :return: bool, Whether the ship can drop a mine or not
        """
        return self.alive and time() - self.last_drop >= self.drop_cooldown

    def drop_mine(self, mines: list[Mine]):
        """
        Drop a Photon or Vapor Mine at the ship's position

        :param enemies: list[Mine], The mines already in the game
        """
        mine_type = randrange(0, 2)
        if mine_type == 1:
            mines.insert(0, VaporMine(self.x, self.y))
        else:
            mines.insert(0, PhotonMine(self.x, self.y))
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()

    def turn(self):
        # TODO: Follow player ?
        pass
