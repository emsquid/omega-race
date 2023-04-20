import math
import pygame
from random import randrange, random
from src.const import WIN_WIDTH, WIN_HEIGHT, BLACK, WHITE, RED
from threading import Timer


class Object:
    """
    The most basic class, an Object represents anything in pygame
    It can move, and draw itself on the game
    """

    def __init__(
        self, width: int, height: int, x: int, y: int, direction: float, speed: int
    ):
        self.set_size(width, height)
        self.set_position(x, y)
        self.set_direction(direction)
        self.set_speed(speed)
        self.set_image()

    def set_size(self, width: int, height: int):
        """
        Set the size of the object, width and height should be positive
        """
        self.width = width
        self.height = height

    def set_position(self, x: int, y: int):
        """
        Set the position of the object, x and y should be positive
        """
        self.x = x
        self.y = y

    def set_direction(self, direction: float):
        """
        Set the direction of the object
        """
        self.direction = direction

    def set_speed(self, speed: int):
        """
        Set the speed of the object
        """
        self.speed = speed

    def set_image(self, filename: str = None, surface: pygame.Surface = None):
        """
        Set the image of the object,
        it can be retrieved from a file or given directly as a surface
        """
        if not filename is None:
            self.image = pygame.image.load(f"src/assets/{filename}")
        elif not surface is None:
            self.image = surface
        else:
            # Default case for development
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)

    def draw(self, surface: pygame.Surface):
        """
        Draw the object on the surface
        """
        surface.blit(self.image, (self.x, self.y))

    def move(self, dt: float):
        """
        Move the object
        We use dt to make the object move at the same speed on any computer
        """
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

    def collide(self, other) -> bool:
        """
        Check for collision with any other object
        """
        return (
            self.x <= other.x + other.width
            and other.x <= self.x + self.width
            and self.y <= other.y + other.height
            and other.y <= self.y + self.height
        )

    def explode(self, step: int = 1):
        if step <= 6:
            self.set_image(f"Explosion{step}.png")
            Timer(0.1, self.explode, [step + 1]).start()


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
