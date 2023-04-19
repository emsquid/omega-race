import pygame
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
            self.image = pygame.image.load(f"src/assets/{filename}")
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
