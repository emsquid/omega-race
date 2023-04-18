import pygame
from threading import Timer
from random import randrange, random
from src.const import WIN_WIDTH, WIN_HEIGHT, BLACK, WHITE, RED


class Object:
    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        x: int = 0,
        y: int = 0,
        dx: int = 0,
        dy: int = 0,
    ):
        self.set_size(width, height)
        self.set_position(x, y)
        self.set_direction(dx, dy)
        self.set_image()

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

    def set_direction(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def set_image(self, filename: str = None, surface: pygame.Surface = None):
        if not filename is None:
            self.image = pygame.image.load(f"assets/{filename}")
        elif not surface is None:
            self.image = surface
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self, dt: float):
        self.x += self.dx * dt
        self.y += self.dy * dt

    def collide(self, other) -> bool:
        return (
            self.x <= other.x + other.width
            and other.x <= self.x + self.width
            and self.y <= other.y + other.height
            and other.y <= self.y + self.height
        )


class Background:
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
        self.image.fill(BLACK)
        for star in self.stars:
            pygame.draw.line(self.image, WHITE, (star[0], star[1]), (star[0], star[1]))
            star[1] -= star[2] * dt
            if star[1] < 0:
                star[0] = randrange(WIN_WIDTH)
                star[1] = WIN_HEIGHT


class Force_Field:
    def __init__(self):
        self.borders = [
            # Left and right borders
            (Object(3, 383, 20, 20), (-1, 1)),
            (Object(3, 383, 20, 400), (-1, 1)),
            (Object(3, 383, 980, 20), (-1, 1)),
            (Object(3, 383, 980, 400), (-1, 1)),
            # Top and bottom borders
            (Object(483, 3, 20, 20), (1, -1)),
            (Object(483, 3, 500, 20), (1, -1)),
            (Object(483, 3, 500, 780), (1, -1)),
            (Object(483, 3, 20, 780), (1, -1)),
        ]

        self.panel = [
            (Object(3, 203, 300, 300), (-1, 1)),
            (Object(3, 203, 700, 300), (-1, 1)),
            (Object(403, 3, 300, 300), (1, -1)),
            (Object(403, 3, 300, 500), (1, -1)),
        ]

        for field, _ in self.borders + self.panel:
            self.reset(field)

    def draw(self, surface: pygame.Surface):
        for field, _ in self.borders + self.panel:
            field.draw(surface)

    def bounce(self, object: Object):
        for field, vector in self.borders + self.panel:
            if object.collide(field):
                self.activate(field)
                object.dx *= vector[0]
                object.dy *= vector[1]

    def activate(self, field: Object):
        if any(field == border for border, _ in self.borders):
            image = pygame.Surface((field.width, field.height))
            image.fill(WHITE)
            field.set_image(surface=image)
            Timer(0.15, self.reset, [field]).start()

    def reset(self, field: Object):
        if any(field == border for border, _ in self.borders):
            image = pygame.Surface((field.width, field.height))
            image.fill(WHITE, (0, 0, 3, 3))
            image.fill(WHITE, (field.width - 3, field.height - 3, 3, 3))
            field.set_image(surface=image)
        else:
            image = pygame.Surface((field.width, field.height))
            image.fill(WHITE)
            field.set_image(surface=image)
