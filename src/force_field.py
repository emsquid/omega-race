import pygame
from threading import Timer
from src.base import Object
from src.const import WHITE


class Border(Object):
    def __init__(
        self, width: int, height: int, x: int, y: int, normal: (int, int), visible: bool
    ):
        super().__init__(width, height, x, y, 0, 0)
        self.normal = normal
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            image = pygame.Surface((self.width, self.height))
            image.fill(WHITE)
        else:
            image = pygame.Surface((self.width, self.height))
            image.fill(WHITE, (0, 0, 3, 3))
            image.fill(WHITE, (self.width - 3, self.height - 3, 3, 3))
        surface.blit(image, (self.x, self.y))

    def collide(self, other: Object) -> bool:
        return (
            self.x <= other.x + other.width
            and other.x <= self.x + self.width
            and self.y <= other.y + other.height
            and other.y <= self.y + self.height
        )

    def bounce(self, other: Object):
        dot = self.normal[0] * other.dx + self.normal[1] * other.dy
        if self.collide(other) and dot < 0:
            if self.normal[0] == 0:
                other.dy *= -1
            else:
                other.dx *= -1
            if not self.visible:
                self.blink()

    def reset(self):
        self.visible = False

    def blink(self):
        self.visible = True
        Timer(0.15, self.reset).start()


class ForceField:
    def __init__(self):
        self.borders = [
            # Left and right borders
            Border(3, 383, 20, 20, (1, 0), False),
            Border(3, 383, 20, 400, (1, 0), False),
            Border(3, 383, 980, 20, (-1, 0), False),
            Border(3, 383, 20, 400, (-1, 0), False),
            # Top and bottom borders
            Border(483, 3, 20, 20, (0, 1), False),
            Border(483, 3, 500, 20, (0, 1), False),
            Border(483, 3, 500, 780, (0, -1), False),
            Border(483, 3, 20, 780, (0, -1), False),
        ]

        self.panel = [
            Border(3, 203, 300, 300, (-1, 0), True),
            Border(3, 203, 700, 300, (1, 0), True),
            Border(403, 3, 300, 300, (0, -1), True),
            Border(403, 3, 300, 500, (0, 1), True),
        ]

    def draw(self, surface: pygame.Surface):
        for border in self.borders + self.panel:
            border.draw(surface)

    def bounce(self, object: Object):
        for border in self.borders + self.panel:
            border.bounce(object)
