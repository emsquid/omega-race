from src.base import Object
import pygame


class Ship(Object):
    """
    class Ship:

    -location (in px): x,y (type -> int)
    -direction (in px) : dx,dy (type -> int)
    -shape (in px) : hight,wigth (type -> int)
    -status (alive/destryd)  : status (type -> bool)

    """

    def __init__(self, x: int = 0, y: int = 0, dx: int = 0, dy: int = 0):
        """
        initilisation
        """
        super().__init__(32, 32, x, y, dx, dy)
        self.angle = 0
        self.speed = 0

    def draw(self, surface: pygame.Surface):
        self.angle += 1
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        ).topleft
        surface.blit(rotated_image, rect)

    def move(self, dt: float):
        self.x += self.dx * dt * self.speed
        self.y += self.dy * dt * self.speed

    def level_up(self):
        self.speed = self.speed * 1.25


class DroidShip(Ship):
    """
    class DroidShip:

    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 1, 1)
        self.set_image("DroidShip.png")
        self.speed = 0.01


class CommandShip(Ship):
    """
    class CommandShip:

    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 1, 1)
        self.set_image("CommandShip.png")
        self.speed = 0.1


class DeathShip(Ship):
    """
    class DeathShip:

    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, 1, 1)
        self.set_image("DeathShip.png")
        self.speed = 0.3
