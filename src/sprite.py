import math
import pygame
import random
import numpy as np
from src.base import Object
from src.const import WHITE
from threading import Timer


class Player(Object):
    """ """

    def __init__(self):
        super().__init__(32, 32, 500, 200, -math.pi / 2, 0)
        self.set_image("Player.png")
        # left or right
        self.rotating = ""
        self.accelerate()

    def draw(self, surface: pygame.Surface):
        # Create the rotated image and center it properly
        angle = -360 * (self.direction + math.pi / 2) / (2 * math.pi)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        ).topleft
        surface.blit(rotated_image, rect)

    def move(self, dt):
        self.rotate(dt)
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

    def accelerate(self):
        self.speed += 0.1

    def rotate(self, dt: int):
        if self.rotating == "left":
            self.direction -= dt * math.pi / 1000
        elif self.rotating == "right":
            self.direction += dt * math.pi / 1000

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rotating = "left"
            elif event.key == pygame.K_RIGHT:
                self.rotating = "right"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.rotating == "left":
                self.rotating = ""
            elif event.key == pygame.K_RIGHT and self.rotating == "right":
                self.rotating = ""


class Mine(Object):
    """
    Mines doesn't move, but they still kill the player
    """

    def __init__(self, width: int, height: int, x: int, y: int, points: int):
        super().__init__(width, height, x, y, 0, 0)
        self.points = points


class PhotonMine(Mine):
    """
    The Photon Mine is half a Vapor Mine
    """

    def __init__(self, x: int, y: int):
        """
        initialisation
        """
        super().__init__(15, 15, x, y, 350)
        self.set_image("PhotonMine.png")


class VaporMine(Mine):
    """
    The Vapor Mine is twice a Photon Mine
    """

    def __init__(self, x: int, y: int):
        """
        initialisation
        """
        super().__init__(25, 25, x, y, 500)
        self.set_image("VaporMine.png")


class Ship(Object):
    """
    Ships are the enemies in the games, they will try to kill the player
    """

    def __init__(self, x: int, y: int, direction: float, speed: float, points: int):
        super().__init__(32, 32, x, y, direction, speed)
        self.rotation = 0
        self.points = points

    def draw(self, surface: pygame.Surface):
        """
        Draw the ship on the surface
        The ship also rotates
        """
        self.rotation += 1
        # Create the rotated image and center it properly
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        ).topleft
        surface.blit(rotated_image, rect)

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


class CommandShip(Ship):
    """
    The Command Ship is more dangerous, it moves and fires laser towards the player
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0, 0.1, 1500)
        self.set_image("CommandShip.png")

    def drop_mine(self, enemies: list):
        """
        Drop a Photon Mine at the ship's position
        """
        mine = PhotonMine(self.x, self.y)
        enemies.insert(0, mine)
        Timer(random.randint(15, 30), self.drop_mine, [enemies]).start()

    def shoot(self, player: Player, enemies):
        v1 = np.array([player.x - self.x, player.y - self.y])
        v1 = v1 / np.linalg.norm(v1)
        v2 = np.array([1, 0])
        if self.y < player.y:
            direction = np.arccos(np.dot(v2, v1))
        else:
            direction = -np.arccos(np.dot(v2, v1))
        laser = Laser(self.x, self.y, direction)
        enemies.append(laser)  # c'est nul il sont meme pas dans leurs liste
        Timer(5.0, self.shoot, [player, enemies]).start()


class DeathShip(Ship):
    """
    The Death Ship will bounce at full speed on every border
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 0, 0.3, 2000)
        self.set_image("DeathShip.png")

    def drop_mine(self, enemies: list):
        """
        Drop a Vapor Mine at the ship's position
        """
        mine_type = random.randint(0, 1)
        if mine_type == 1:
            mine = VaporMine(self.x, self.y)
        else:
            mine = PhotonMine(self.x, self.y)
        enemies.insert(0, mine)
        Timer(random.randint(5, 15), self.drop_mine, [enemies]).start()


class Laser(Object):
    """ """

    def __init__(self, x: int, y: int, direction: float):
        super().__init__(2, 10, x, y, direction, 0.2)
        image = pygame.Surface((2, 15))
        image.fill(WHITE)
        self.set_image(surface=image)
