import math
import pygame
from threading import Timer
from src.const import WHITE, RED


# TODO: Test using pygame.sprite.Sprite/Group
class Object:
    """
    The most basic class, an Object represents anything in pygame
    It can draw itself on the game
    """

    def __init__(
        self,
        width: int,
        height: int,
        x: int,
        y: int,
    ):
        self.set_size(width, height)
        self.set_position(x, y)
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

    def set_image(self, filename: str = None, surface: pygame.Surface = None):
        """
        Set the image of the object,
        it can be retrieved from a file or given directly as a surface
        """
        if not filename is None:
            self.image = pygame.image.load(f"assets/{filename}")
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
        surface.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def collide(self, other) -> bool:
        """
        Check for collision with any other object
        """
        return (
            self.x - self.width / 2 <= other.x + other.width / 2
            and other.x - other.width / 2 <= self.x + self.width / 2
            and self.y - self.height / 2 <= other.y + other.height / 2
            and other.y - other.height / 2 <= self.y + self.height / 2
        )


class Entity(Object):
    def __init__(
        self,
        width: int,
        height: int,
        x: int,
        y: int,
        direction: float,
        rotation: float,
        speed: int,
    ):
        super().__init__(width, height, x, y)
        self.set_direction(direction)
        self.set_rotation(rotation)
        self.set_speed(speed)

    def set_direction(self, direction: float):
        """
        Set the direction of the sprite
        """
        self.direction = direction

    def set_rotation(self, rotation: float):
        """
        Set the rotation of the sprite
        """
        self.rotation = rotation

    def set_speed(self, speed: int):
        """
        Set the speed of the sprite
        """
        self.speed = speed

    def draw(self, surface: pygame.Surface):
        """
        Draw the sprite on the surface
        """
        # Create the rotated image and center it properly
        angle = -360 * (self.rotation + math.pi / 2) / (2 * math.pi)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect)

    def move(self, dt: float):
        """
        Move the object
        We use dt to make the object move at the same speed on any computer
        """
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt


class Text(Object):
    def __init__(
        self,
        content: str,
        x: int,
        y: int,
        color: tuple = WHITE,
        size: int = 25,
        anchor: str = "center",  # topleft, topright, center
    ):
        super().__init__(0, 0, x, y)
        self.font = pygame.font.Font("assets/font1.ttf", size)
        self.set_content(content)
        self.set_color(color)
        self.anchor = anchor

    def set_content(self, content: str):
        """
        Set the text content
        """
        self.content = content

    def set_color(self, color: tuple):
        """
        Set the text color
        """
        self.color = color

    def draw(self, surface: pygame.Surface):
        """
        Draw the text on the surface
        """
        text = self.font.render(self.content, True, self.color)
        width, height = text.get_size()
        if self.anchor == "center":
            surface.blit(text, (self.x - width / 2, self.y - height / 2))
        elif self.anchor == "topleft":
            surface.blit(text, (self.x, self.y))
        elif self.anchor == "topright":
            surface.blit(text, (self.x - width, self.y))


class Explosion(Object):
    def __init__(self, x: int, y: int):
        super().__init__(35, 35, x, y)
        self.done = False
        self.play()

    def play(self, step: int = 1):
        """
        Play each step of the explosion
        """
        if step <= 6:
            self.set_image(f"Explosion{step}.png")
            Timer(0.1, self.play, [step + 1]).start()
        else:
            self.done = True
