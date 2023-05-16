import pygame
from time import time
from math import pi, sqrt
from random import randrange, random, choice
from src.objects.base import Entity
from src.vector import Vector
from src.const import CEN_X, CEN_Y, PAN_WIDTH, PAN_HEIGHT, WHITE


class Laser(Entity):
    """
    Lasers are the main source of danger in the game

    :param x: int, The x coordinate of the laser
    :param y: int, The x coordinate of the laser
    :param direction: Vector, The direction
    """

    def __init__(self, x: int, y: int, direction: Vector):
        image = pygame.Surface((2, 15), pygame.SRCALPHA)
        image.fill(WHITE)
        super().__init__(x, y, image, direction, direction, 0.3)


class Player(Entity):
    """
    It's you, you can move, rotate, thrust and shoot, good luck

    :param color: tuple[int], The color of the player
    """

    def __init__(self, color: tuple[int]):
        direction = Vector(0, -1)
        super().__init__(500, 200, Player.create_image(color), direction, direction, 0)
        # left | right
        self.rotating = ""
        self.last_collision = 0
        self.last_shoot = 0

    def create_image(color: tuple[int], thrusting: bool = False) -> pygame.Surface:
        """
        Create the player image with the given color
        """
        n_details = 2 if thrusting else 1
        details = pygame.image.load(f"assets/images/PlayerDetails{n_details}.png")
        shell = pygame.image.load("assets/images/PlayerShell.png")
        color_mask = pygame.Surface(shell.get_size())
        color_mask.fill(color)
        shell.blit(color_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        shell.blit(details, (0, 0))
        return shell

    def can_thrust(self) -> bool:
        """
        Check if the player can thrust

        :return: bool, Whether you can thrust or not
        """
        return self.alive and time() - self.last_collision >= 0.3

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
        self.set_direction(self.rotation)
        self.speed = 0.2
        self.last_thrust = time()

    def shoot(self, lasers: list[Laser]):
        """
        Shoot a laser

        :param lasers: list[Laser], The lasers already in game
        """
        lasers.append(Laser(self.x, self.y, self.rotation))
        self.last_shoot = time()

    def rotate(self, dt: int):
        """
        Rotate the player

        :param dt: int, The time delta between frames
        """
        if self.rotating == "left":
            self.set_rotation(self.rotation.rotate(-dt * pi / 725))
        elif self.rotating == "right":
            self.set_rotation(self.rotation.rotate(dt * pi / 725))

    def update(self, dt: int):
        """
        Update the state of the player

        :param dt: int, The time delta between frames
        """
        super().update(dt)
        self.rotate(dt)


class Mine(Entity):
    """
    Mines doesn't move, but they still kill the player

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    :param image: str | pygame.Surface, The image of the mine
    :param points: int, The points the mine is worth
    """

    def __init__(self, x: int, y: int, image: str | pygame.Surface, points: int):
        super().__init__(x, y, image, Vector(0, 0), Vector(0, -1), 0)
        self.points = points


class PhotonMine(Mine):
    """
    The Photon Mine is half a Vapor Mine

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "PhotonMine.png", 350)


class VaporMine(Mine):
    """
    The Vapor Mine is twice a Photon Mine

    :param x: int, The x coordinate of the mine
    :param y: int, The y coordinate of the mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "VaporMine.png", 500)


class Ship(Entity):
    """
    Ships are the enemies in the games, they will try to kill the player

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param image: str | pygame.Surface, The image of the ship
    :param direction: Vector, The direction the ship advances towards
    :param speed: float, The speed of the ship
    :param points: int, The points the ship is worth
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(
        self,
        x: int,
        y: int,
        image: str | pygame.Surface,
        direction: Vector,
        speed: float,
        points: int,
        level: int,
    ):
        super().__init__(x, y, image, direction, direction, speed * sqrt(level))
        self.distance = randrange(50, 250)
        self.points = points

    def can_see(self, entity: Entity) -> bool:
        """
        Check if the ship can see the player

        :return: bool, Whether the ship can see the player or not
        """

        panel_x, panel_y = CEN_X - PAN_WIDTH / 2, CEN_Y - PAN_HEIGHT / 2
        panel_rect = pygame.Rect(
            panel_x - 10, panel_y - 10, PAN_WIDTH + 20, PAN_HEIGHT + 20
        )
        intersections = panel_rect.clipline(self.x, self.y, entity.x, entity.y)
        return self.alive and len(intersections) == 0

    def turn(self):
        """
        Change ship direction when reaching the right distance
        """
        # TODO: Look for improvements here
        # top left
        if (
            self.x + self.distance < CEN_X - PAN_WIDTH / 2
            and self.y < CEN_Y - PAN_HEIGHT / 2
        ) or (
            self.x < CEN_X - PAN_WIDTH / 2
            and CEN_Y - PAN_HEIGHT / 2 < self.y < CEN_Y + PAN_HEIGHT / 2 + self.distance
        ):
            self.set_direction(Vector(0, 1))
        # top right
        if (
            self.x > CEN_X + PAN_WIDTH / 2
            and self.y + self.distance < CEN_Y - PAN_HEIGHT / 2
        ) or (
            CEN_X - PAN_WIDTH / 2 - self.distance < self.x < CEN_X + PAN_WIDTH / 2
            and self.y < CEN_Y - PAN_HEIGHT / 2
        ):
            self.set_direction(Vector(-1, 0))
        # bottom right
        if (
            self.x - self.distance > CEN_X + PAN_WIDTH / 2
            and self.y > CEN_Y + PAN_HEIGHT / 2
        ) or (
            self.x > CEN_X + PAN_WIDTH / 2
            and CEN_Y - PAN_HEIGHT / 2 - self.distance < self.y < CEN_Y + PAN_HEIGHT / 2
        ):
            self.set_direction(Vector(0, -1))
        # bottom left
        if (
            self.x < CEN_X - PAN_WIDTH / 2
            and self.y - self.distance > CEN_Y + PAN_HEIGHT / 2
        ) or (
            CEN_X - PAN_WIDTH / 2 < self.x < CEN_X + PAN_WIDTH / 2 + self.distance
            and self.y > CEN_Y + PAN_HEIGHT / 2
        ):
            self.set_direction(Vector(1, 0))

    def rotate(self, dt: int):
        """
        Rotate the ship

        :param dt: int, The time delta between frames
        """
        self.set_rotation(self.rotation.rotate(pi * dt / 4096))

    def update(self, dt: int):
        """
        Update the state of the ship

        :param dt: int, The time delta between frames
        """
        super().update(dt)
        self.rotate(dt)
        self.turn()


class DroidShip(Ship):
    """
    The Droid Ship doesn't move a lot, but it can transfrom into a CommandShip

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        direction = Vector(1, 0)
        super().__init__(x, y, "DroidShip.png", direction, 0.01, 1000, level)

    def follow(self, player: Player):
        """
        Follow the player

        :param player: Player, The player to follow
        """
        direction = Vector(player.x - self.x, player.y - self.y)
        self.set_direction(direction)


class CommandShip(Ship):
    """
    The Command Ship is more dangerous, it moves and fires laser towards the player

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        direction = Vector(1, 0)
        super().__init__(x, y, "CommandShip.png", direction, 0.05, 1500, level)
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()
        self.shoot_cooldown = randrange(3, 8)
        self.last_shoot = time()
        self.init = time()

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
        direction = Vector(player.x - self.x, player.y - self.y)
        lasers.append(Laser(self.x, self.y, direction))
        self.shoot_cooldown = randrange(3, 8)
        self.last_shoot = time()

    def update(self, dt):
        self.set_image(
            "DroidShip.png"
            if time() - self.init < 2 and time() % 1 < 0.5
            else "Transformation1.png"
            if time() - self.init < 2
            else "CommandShip.png"
        )
        super().update(dt)


class DeathShip(Ship):
    """
    The Death Ship will bounce at full speed on every border

    :param x: int, The x coordinate of the ship
    :param y: int, The y coordinate of the ship
    :param level: int, The level the ship is at (increases speed)
    """

    def __init__(self, x: int, y: int, level: int):
        direction = Vector(random(), random())
        super().__init__(x, y, "DeathShip.png", direction, 0.2, 2000, level)
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()
        self.init = time()

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
        mines.insert(0, choice((VaporMine, PhotonMine))(self.x, self.y))
        self.drop_cooldown = randrange(10, 20)
        self.last_drop = time()

    def turn(self):
        pass

    def update(self, dt):
        self.set_image(
            "CommandShip.png"
            if time() - self.init < 2 and time() % 1 < 0.5
            else "Transformation2.png"
            if time() - self.init < 2
            else "DeathShip.png"
        )
        super().update(dt)
