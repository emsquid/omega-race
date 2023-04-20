import math
import pygame
from threading import Timer
from src.const import RED


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
        # Create the rotated image and center it properly
        angle = -360 * (self.direction + math.pi / 2) / (2 * math.pi)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        )
        surface.blit(rotated_image, rect)

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
        # TODO
        if step <= 6:
            self.set_image(f"Explosion{step}.png")
            Timer(0.1, self.explode, [step + 1]).start()
