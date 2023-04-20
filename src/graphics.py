import math
import pygame
from threading import Timer
from src.base import Object
from random import randrange, random
from src.const import WIN_WIDTH, WIN_HEIGHT, BLACK, WHITE


class Background:
    """
    The Background of the game, every other object will be displayed over it
    There are stars moving, so beautiful
    """

    def __init__(self):
        self.image = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.stars = [
            [
                randrange(WIN_WIDTH),
                randrange(WIN_HEIGHT),
                random() / 20,
            ]
            for i in range(100)
        ]

    def move(self, dt: int):
        """
        Move stars on the background
        """
        self.image.fill(BLACK)
        for star in self.stars:
            pygame.draw.line(self.image, WHITE, (star[0], star[1]), (star[0], star[1]))
            star[1] -= star[2] * dt
            if star[1] < 0:
                star[0] = randrange(WIN_WIDTH)
                star[1] = WIN_HEIGHT


class Border(Object):
    """
    A Border draws the boundaries of the game field
    It will bounce objects on collision
    """

    def __init__(
        self, width: int, height: int, x: int, y: int, normal: float, visible: bool
    ):
        super().__init__(width, height, x, y, normal, 0)
        self.normal = normal
        self.visible = visible

    def draw(self, surface):
        """
        Draw a border on the surface,
        The image differs if the border is visible
        """
        image = pygame.Surface((self.width, self.height))
        if self.visible:
            image.fill(WHITE)
        else:
            image.fill(WHITE, (0, 0, 3, 3))
            image.fill(WHITE, (self.width - 3, self.height - 3, 3, 3))
        surface.blit(image, (self.x, self.y))

    def bounce(self, other: Object):
        """
        Bounce objects that collide with this border
        The object should be a ship or the player
        """
        # We use dot product to know if the object should bounce on the collided border
        dot = math.cos(self.normal) * math.cos(other.direction) + math.sin(
            self.normal
        ) * math.sin(other.direction)
        if self.collide(other) and dot < 0:
            if round(math.cos(self.normal), 5) != 0:
                other.set_direction(math.pi - other.direction)
            else:
                other.set_direction(-other.direction)
            self.blink()

    def show(self):
        """
        Make the border visible
        """
        self.visible = True

    def hide(self):
        """
        Make the border invisible
        """
        self.visible = False

    def blink(self):
        """
        Make the border blink, it will show and hide after 0.15s
        """
        if not self.visible:
            self.show()
            Timer(0.15, self.hide).start()


class ForceField:
    """
    The Force Field handles all borders simultaneously
    """

    def __init__(self):
        # Border for the boundaries of the game field
        self.borders = [
            # Left and right borders
            Border(3, 383, 20, 20, 0, False),
            Border(3, 383, 20, 400, 0, False),
            Border(3, 383, 980, 20, math.pi, False),
            Border(3, 383, 980, 400, math.pi, False),
            # Top and bottom borders
            Border(483, 3, 20, 20, math.pi / 2, False),
            Border(483, 3, 500, 20, math.pi / 2, False),
            Border(483, 3, 20, 780, -math.pi / 2, False),
            Border(483, 3, 500, 780, -math.pi / 2, False),
        ]

        # Border for the display panel
        self.panel = [
            Border(3, 203, 700, 300, 0, True),
            Border(3, 203, 300, 300, math.pi, True),
            Border(403, 3, 300, 500, math.pi / 2, True),
            Border(403, 3, 300, 300, -math.pi / 2, True),
        ]

    def draw(self, surface: pygame.Surface):
        """
        Draw all borders on the surface
        """
        for border in self.borders + self.panel:
            border.draw(surface)

    def bounce(self, object: Object):
        """
        Check if the object should bounce on any border
        """
        for border in self.borders + self.panel:
            border.bounce(object)


class Explosion:
    pass
