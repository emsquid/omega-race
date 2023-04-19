from src.base import Object
import pygame
from src.mine import PhotonMine, VaporMine


class Ship(Object):
    """
    Ships are the enemies in the games, they will try to kill the player
    """

    def __init__(self, x: int, y: int, dx: int, dy: int, points: int):
        super().__init__(32, 32, x, y, dx, dy)
        self.rotation = 0
        self.speed = 0
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

    def move(self, dt: float):
        """
        Move the ship
        The ship movements are also affected by its speed
        """
        self.x += self.dx * dt * self.speed
        self.y += self.dy * dt * self.speed

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
        super().__init__(x, y, 1, 0, 1000)
        self.set_image("DroidShip.png")
        self.speed = 0.01


class CommandShip(Ship):
    """
    The Command Ship is more dangerous, it moves and fires laser towards the player
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 1, 0, 1500)
        self.set_image("CommandShip.png")
        self.speed = 0.1

    def drop_mine(self, enemies: list):
        """
        Drop a Photon Mine at the ship's position
        """
        mine = PhotonMine(self.x, self.y)
        enemies.append(mine)


class DeathShip(Ship):
    """
    The Death Ship will bounce at full speed on every border
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 1, 0, 2000)
        self.set_image("DeathShip.png")
        self.speed = 0.3

    def drop_mine(self, enemies: list):
        """
        Drop a Vapor Mine at the ship's position
        """
        mine = VaporMine(self.x, self.y)
        enemies.append(mine)
