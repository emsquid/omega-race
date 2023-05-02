import math
import pygame
from time import time
from threading import Timer
from random import randrange, random
from src.base import Entity
from src.const import WHITE


class Laser(Entity):
    """
    Lasers are the main source of danger here
    """

    def __init__(self, x: int, y: int, direction: float):
        super().__init__(2, 10, x, y, direction, direction, 0.3)
        image = pygame.Surface((2, 15), pygame.SRCALPHA)
        image.fill(WHITE)
        self.set_image(surface=image)


class Player(Entity):
    """
    It's you, you can move, rotate, thrust and shoot, good luck
    """

    def __init__(self):
        super().__init__(32, 32, 500, 200, -math.pi / 2, -math.pi / 2, 0)
        self.set_image("Player1.png")
        self.lives = 3
        self.score = 0
        # left or right
        self.rotating = ""
        self.last_thrust = time() - 0.5
        self.last_shoot = time() - 1

    def can_thrust(self) -> bool:
        """
        Whether you can thrust or not
        """
        return time() - self.last_thrust >= 0.5

    def can_shoot(self) -> bool:
        """
        Whether you can shoot or not
        """
        return time() - self.last_shoot >= 1

    def move(self, dt):
        """
        Move and rotate if needed
        """
        self.rotate(dt)
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

    def thrust(self):
        """
        Thrust in the direction the player is pointing
        """
        # TODO: Rework image change, will depend on Sprite usage
        self.speed = 0.25
        self.direction = self.rotation
        self.last_thrust = time()
        self.set_image("Player2.png")
        Timer(0.2, self.set_image, ["Player1.png"]).start()

    def shoot(self, lasers: list[Laser]):
        """
        Shoot a laser
        """
        x, y = self.image.get_rect(topleft=(self.x, self.y)).center
        lasers.append(Laser(x, y, self.rotation))
        self.last_shoot = time()

    def rotate(self, dt: int):
        """
        Rotate the player
        """
        if self.rotating == "left":
            self.rotation -= dt * math.pi / 1000
        elif self.rotating == "right":
            self.rotation += dt * math.pi / 1000

    def kill(self, enemy: Entity):
        """
        Kill the enemy and get its points
        """
        self.score += enemy.points

    def die(self):
        """
        The player dies and loses a life
        """
        self.lives -= 1


class Mine(Entity):
    """
    Mines doesn't move, but they still kill the player
    """

    def __init__(self, width: int, height: int, x: int, y: int, points: int):
        super().__init__(width, height, x, y, -math.pi / 2, -math.pi / 2, 0)
        self.points = points


class PhotonMine(Mine):
    """
    The Photon Mine is half a Vapor Mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(15, 15, x, y, 350)
        self.set_image("PhotonMine.png")


class VaporMine(Mine):
    """
    The Vapor Mine is twice a Photon Mine
    """

    def __init__(self, x: int, y: int):
        super().__init__(25, 25, x, y, 500)
        self.set_image("VaporMine.png")


class Ship(Entity):
    """
    Ships are the enemies in the games, they will try to kill the player
    """

    def __init__(self, x: int, y: int, direction: float, speed: float, points: int):
        super().__init__(32, 32, x, y, direction, direction, speed)
        self.points = points

    def move(self, dt: int):
        """
        Move and also rotate
        """
        self.rotation += 2 * math.pi / 360
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

    def level_up(self):
        """
        Level up the ship, increasing its speed
        """
        self.speed = self.speed * 1.25


class DroidShip(Ship):
    """
    The Droid Ship doesn't move a lot, but it can transfrom into a CommandShip
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0, 0.01, 1000)
        self.set_image("DroidShip.png")
        self.last_rotate = time() - 1
        self.distance = randrange(450, 500)

    def rotate(self):
        if (
            time() - self.last_rotate > 1
            and math.sqrt((self.x - 500) ** 2 + (self.y - 400) ** 2) > self.distance
        ):
            self.direction -= math.pi / 2
            self.last_rotate = time()


class CommandShip(Ship):
    """
    The Command Ship is more dangerous, it moves and fires laser towards the player
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0, 0.1, 1500)
        self.set_image("CommandShip.png")
        self.last_drop = time()
        self.last_shoot = time()
        self.last_rotate = time() - 1
        self.distance = randrange(450, 500)

    def can_drop(self) -> bool:
        """
        Whether the ship can drop a mine or not
        """
        return time() - self.last_drop >= 15

    def can_shoot(self) -> bool:
        """
        Whether the ship can shoot or not
        """
        return time() - self.last_shoot >= 5

    def drop_mine(self, enemies: list):
        """
        Drop a Photon Mine at the ship's position
        """
        enemies.insert(0, PhotonMine(self.x, self.y))
        self.last_drop = time()

    def rotate(self):
        if (
            time() - self.last_rotate > 1
            and math.sqrt((self.x - 500) ** 2 + (self.y - 400) ** 2) > self.distance
        ):
            self.direction -= math.pi / 2
            self.last_rotate = time()

    def shoot(self, player: Player, lasers: list[Laser]):
        """
        Shoot a laser towards the player
        """
        x, y = self.image.get_rect(topleft=(self.x, self.y)).center
        direction = math.atan2(player.y - self.y, player.x - self.x)
        lasers.append(Laser(x, y, direction))
        self.last_shoot = time()


class DeathShip(Ship):
    """
    The Death Ship will bounce at full speed on every border
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, random() * math.pi * 2, 0.3, 2000)
        self.set_image("DeathShip.png")
        self.last_drop = time()

    def can_drop(self) -> bool:
        """
        Whether the ship can drop a mine or not
        """
        return time() - self.last_drop >= 15

    def drop_mine(self, enemies: list):
        """
        Drop a Photon or Vapor Mine at the ship's position
        """
        mine_type = randrange(0, 2)
        if mine_type == 1:
            enemies.insert(0, VaporMine(self.x, self.y))
        else:
            enemies.insert(0, PhotonMine(self.x, self.y))
        self.last_drop = time()
