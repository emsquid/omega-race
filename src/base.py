import pygame
from threading import Timer
from random import randrange, random
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED


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

    def set_image(self, name: str = None, surface: pygame.Surface = None):
        if not name is None:
            pass
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
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.stars = [
            [
                randrange(SCREEN_WIDTH),
                randrange(SCREEN_HEIGHT),
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
                star[0] = randrange(SCREEN_WIDTH)
                star[1] = SCREEN_HEIGHT


class Force_Field:
    def __init__(self):
        self.borders = {
            "x": [
                Object(3, 380, 980, 20),
                Object(3, 380, 980, 400),
                Object(3, 380, 20, 400),
                Object(3, 380, 20, 20),
            ],
            "y": [
                Object(480, 3, 20, 20),
                Object(480, 3, 500, 20),
                Object(480, 3, 500, 780),
                Object(480, 3, 20, 780),
            ],
        }
        # mettre le vecteur de changement de direction
        self.panel = {
            "x": [Object(3, 200, 300, 300), Object(3, 200, 700, 300)],
            "y": [Object(400, 3, 300, 300), Object(400, 3, 300, 500)],
        }

    def draw(self, surface: pygame.Surface):
        for obj in self.borders["x"]:
            obj.draw(surface)
        for obj in self.borders["y"]:
            obj.draw(surface)
        for obj in self.panel["x"]:
            obj.draw(surface)
        for obj in self.panel["y"]:
            obj.draw(surface)

    def bounce(self, object: Object):
        for border in self.borders["x"]:
            if object.collide(border):
                self.activate(border)
                object.dx *= -1
        for border in self.borders["y"]:
            if object.collide(border):
                self.activate(border)
                object.dy *= -1

    def activate(self, border: Object):
        image = pygame.Surface((self.width, self.height))
        image.fill(WHITE)
        border.set_image(surface=image)
        Timer(1, self.reset, border).run()

    def reset(self, border: Object):
        image = pygame.Surface((border.width, border.height))
        image.fill(WHITE, (0, 0, 3, 3))
        image.fill(WHITE, (border.width - 3, border.width - 3, 3, 3))
        border.set_image(surface=image)
