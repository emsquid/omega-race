import math
import pygame
from threading import Timer
from src.const import WHITE, RED


class Object:
    """
    The most basic class, an Object can represent anything in pygame
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
        Set the size of the object

        :param width: int > 0, The width of the object
        :param height: int > 0, The height of the object

        """
        self.width = width
        self.height = height

    def set_position(self, x: int, y: int):
        """
        Set the position of the object

        :param x: int > 0, The x coordinate of the object
        :param y: int > 0, The y coordinate of the object
        """
        self.x = x
        self.y = y

    def set_image(self, filename: str = None, surface: pygame.Surface = None):
        """
        Set the image of the object,

        :param filename: str = None, The file to retrieve the image from
        :param surface: pygame.Surface = None, The surface to use as an image
        """
        if not filename is None:
            self.image = pygame.image.load(f"assets/{filename}").convert_alpha()
        elif not surface is None:
            self.image = surface.convert_alpha()
        else:
            # Default case for development, should throw an error
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(RED)

    def draw(self, surface: pygame.Surface):
        """
        Draw the object on the surface

        :param surface: pygame.Surface, The surface to draw the object on
        """
        surface.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def collide(self, other) -> bool:
        """
        Check for collision with any other object

        :param other: Object (Entity), The object to check for collision with
        """
        return (
            (not isinstance(self, Entity) or self.alive)
            and (not isinstance(other, Entity) or other.alive)
            and self.x - self.width / 2 <= other.x + other.width / 2
            and other.x - other.width / 2 <= self.x + self.width / 2
            and self.y - self.height / 2 <= other.y + other.height / 2
            and other.y - other.height / 2 <= self.y + self.height / 2
        )


class Entity(Object):
    """
    An Entity is an Object with a life
    """

    def __init__(
        self,
        width: int,
        height: int,
        x: int,
        y: int,
        direction: float,
        rotation: float,
        speed: float,
    ):
        super().__init__(width, height, x, y)
        self.set_direction(direction)
        self.set_rotation(rotation)
        self.set_speed(speed)
        self.alive = True

    def set_direction(self, direction: float):
        """
        Set the direction of the entity

        :param direction: float, The direction (radians) the entity advances toward
        """
        self.direction = direction

    def set_rotation(self, rotation: float):
        """
        Set the rotation of the entity

        :param rotation: float, The rotation (radians) the entity has
        """
        self.rotation = rotation

    def set_speed(self, speed: float):
        """
        Set the speed of the entity

        :param speed: float, The speed at which the entity advances
        """
        self.speed = speed

    def die(self):
        """
        Make the entity die, when dead an entity doesn't move and isn't displayed
        """
        self.alive = False

    def draw(self, surface: pygame.Surface):
        """
        Draw the rotated entity on the surface

        :param surface: pygame.Surface, The surface to draw the object on
        """
        if not self.alive:
            return
        # Create the rotated image and center it properly
        angle = -360 * (self.rotation + math.pi / 2) / (2 * math.pi)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect)

    def move(self, dt: int):
        """
        Move the entity

        :param dt: int, The time delta between frames
        """
        if not self.alive:
            return
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt


class Text(Object):
    def __init__(
        self,
        content: str,
        x: int,
        y: int,
        size: int = 25,
        color: tuple = WHITE,
        anchor: str = "center",  # topleft, topright, center
    ):
        super().__init__(0, 0, x, y)
        self.font = pygame.font.Font("assets/font1.ttf", size)
        self.anchor = anchor
        self.update(content, color)

    def update(self, content: str = None, color: tuple = None):
        """
        Update the text image

        :param content: str, The content of the text
        :param color: tuple, The color (RGBA) of the text
        """
        self.content = content if content != None else self.content
        self.color = color if color != None else self.color
        self.image = self.font.render(self.content, True, self.color).convert_alpha()

    def draw(self, surface: pygame.Surface):
        """
        Draw the text on the surface

        :param surface: pygame.Surface, The surface to draw the text on
        """
        width, height = self.image.get_size()
        if self.anchor == "center":
            surface.blit(self.image, (self.x - width / 2, self.y - height / 2))
        elif self.anchor == "left":
            surface.blit(self.image, (self.x, self.y - height / 2))
        elif self.anchor == "right":
            surface.blit(self.image, (self.x - width, self.y - height / 2))
        elif self.anchor == "topleft":
            surface.blit(self.image, (self.x, self.y))
        elif self.anchor == "topright":
            surface.blit(self.image, (self.x - width, self.y))



class Explosion(Object):
    """
    Represent an animated explosion
    """

    def __init__(self, x: int, y: int):
        super().__init__(35, 35, x, y)
        self.done = False
        self.play()     

    def play(self, step: int = 1):
        """
        Play each step of the explosion

        :param step: 1 <= int <= 6, The step the explosion is at
        """            

        self.sound = pygame.mixer.Sound("assets/Explosion.wav")

        if step ==1:
            pygame.mixer.Sound.play(self.sound)
        if step <= 6:
            self.set_image(f"Explosion{step}.png")
            Timer(0.1, self.play, [step + 1]).start()
        else:
            self.done = True

    def draw(self, surface: pygame.Surface):
        """
        Draw the object on the surface

        :param surface: pygame.Surface, The surface to draw the explosion on
        """
        if self.done:
            return
        surface.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))