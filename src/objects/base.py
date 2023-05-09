import math
import pygame
from time import time
from src.const import WHITE, RED


class Object:
    """
    The most basic class, an Object can represent anything in pygame

    :param x: int, The x coordinate of the object
    :param y: int, The y coordinate of the object
    :param image: str | pygame.Surface, The image of the object
    """

    def __init__(self, x: int, y: int, image):
        self.set_position(x, y)
        self.set_image(image)

    def set_position(self, x: int, y: int):
        """
        Set the position of the object

        :param x: int > 0, The x coordinate of the object
        :param y: int > 0, The y coordinate of the object
        """
        self.x = x
        self.y = y

    def set_image(self, image):
        """
        Set the image of the object,

        :param filename: str = None, The file to retrieve the image from
        :param surface: pygame.Surface = None, The surface to use as an image
        """
        if isinstance(image, str):
            self.image = pygame.image.load(f"assets/images/{image}").convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image.convert_alpha()
        else:
            # TODO: Default case for development, should throw an error
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface: pygame.Surface):
        """
        Draw the object on the surface

        :param surface: pygame.Surface, The surface to draw the object on
        """
        surface.blit(self.image, self.rect)

    def collide(self, other) -> bool:
        """
        Check for collision with any other object

        :param other: Object (Entity), The object to check for collision with
        """
        return (
            (not isinstance(self, Entity) or self.alive)
            and (not isinstance(other, Entity) or other.alive)
            and pygame.sprite.collide_mask(self, other)
        )


class Entity(Object):
    """
    An Entity is a moving Object

    :param x: int, The x coordinate of the entity
    :param y: int, The y coordinate of the entity
    :param image: str | pygame.Surface, The image of the entity
    :param direction: float, The direction (radians) the entity advances towards
    :param rotation: float, The rotation (radians) the entity has
    :param speed: float, The speed at which the entity advances
    """

    def __init__(
        self,
        x: int,
        y: int,
        image,
        direction: float,
        rotation: float,
        speed: float,
    ):
        super().__init__(x, y, image)
        self.set_direction(direction)
        self.set_rotation(rotation)
        self.set_speed(speed)
        self.alive = True

    def set_direction(self, direction: float):
        """
        Set the direction of the entity

        :param direction: float, The direction (radians) the entity advances towards
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
        self.mask = pygame.mask.from_surface(rotated_image)
        self.rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, self.rect)

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
    """
    Well, it's a text

    :param content: str, The content of the text
    :param x: int, The x coordinate of the text
    :param y: int, The y coordinate of the text
    :param size: int = 25, The size of the font
    :param color: tuple = WHITE, The color of the text
    :param anchor: str = "center" | "left" | "right" | "topleft" | "topright", The anchor for rendering
    """

    def __init__(
        self,
        content: str,
        x: int,
        y: int,
        size: int = 25,
        color: tuple = WHITE,
        anchor: str = "center",
    ):
        self.font = pygame.font.Font("assets/fonts/font.ttf", size)
        self.anchor = anchor
        self.update(content, color)
        super().__init__(x, y, self.image)

    def update(self, content: str = None, color: tuple = None):
        """
        Update the text image

        :param content: str, The content of the text
        :param color: tuple, The color (RGBA) of the text
        """
        self.content = content if content is not None else self.content
        self.color = color if color is not None else self.color
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

    :param x: int, The x coordinate of the explosion
    :param y: int, The x coordinate of the explosion
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "Explosion1.png")
        self.step = 0
        self.last_update = 0
        

    def can_update(self) -> bool:
        """
        Check if the explosion can be updated

        :return: bool, Whether it's been long enough or not
        """
        return self.step < 6 and time() - self.last_update > 0.1

    def update(self):
        """
        Update the state of the explosion
        """
        if not self.can_update():
            return
        self.step += 1
        self.set_image(f"Explosion{self.step}.png")
        self.last_update = time()

    def draw(self, surface: pygame.Surface):
        """
        Draw the explosion on the surface

        :param surface: pygame.Surface, The surface to draw the explosion on
        """
        if self.step >= 6 and time() - self.last_update > 0.1:
            return
        super().draw(surface)
