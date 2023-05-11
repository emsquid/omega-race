from __future__ import annotations
import pygame
from time import time
from math import pi, degrees
from src.vector import Vector
from src.const import WHITE


class Object:
    """
    The most basic class, an Object can represent anything in pygame

    :param x: int, The x coordinate of the object
    :param y: int, The y coordinate of the object
    :param image: str | pygame.Surface, The image of the object
    """

    def __init__(self, x: int, y: int, image: str | pygame.Surface):
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

    def set_image(self, image: str | pygame.Surface):
        """
        Set the image of the object,

        :param image: str | pygame.Surface, The image of the object
        """
        if isinstance(image, str):
            self.image = pygame.image.load(f"assets/images/{image}").convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image.convert_alpha()
        else:
            raise TypeError(f"'{type(image).__name__} can't be used as an image")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface: pygame.Surface):
        """
        Draw the object on the surface

        :param surface: pygame.Surface, The surface to draw the object on
        """
        surface.blit(self.image, self.rect)

    def collide(self, other: Object) -> bool:
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
    :param direction: Vector, The direction the entity advances towards
    :param rotation: Vector, The rotation the entity has
    :param speed: float, The speed at which the entity advances
    """

    def __init__(
        self,
        x: int,
        y: int,
        image: str | pygame.Surface,
        direction: Vector,
        rotation: Vector,
        speed: float,
    ):
        super().__init__(x, y, image)
        self.set_direction(direction)
        self.set_rotation(rotation)
        self.set_speed(speed)
        self.alive = True

    def set_image(self, image: str | pygame.Surface):
        """
        Set the image of the entity,

        :param image: str | pygame.Surface, The image of the entity
        """
        if isinstance(image, str):
            self.image = pygame.image.load(f"assets/images/{image}").convert_alpha()
        elif isinstance(image, pygame.Surface):
            self.image = image.convert_alpha()
        self.base_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_direction(self, direction: Vector):
        """
        Set the direction of the entity

        :param direction: Vector, The direction the entity advances towards
        """
        if round(direction.norm, 5) != 0:
            self.direction = direction.normalized()
        else:
            self.direction = direction.copy()

    def set_rotation(self, rotation: Vector):
        """
        Set the rotation of the entity

        :param rotation: Vector, The rotation the entity has
        """
        if round(rotation.norm, 5) != 0:
            self.rotation = rotation.normalized()
        else:
            self.rotation = rotation.copy()

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
        super().draw(surface)

    def move(self, dt: int):
        """
        Move the entity

        :param dt: int, The time delta between frames
        """
        if not self.alive:
            return
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt

    def update(self, dt: int):
        """
        Update the state of the entity

        :param dt: int, The time delta between frames
        """
        if not self.alive:
            return
        self.move(dt)
        # Create the rotated image and center it properly
        angle = -degrees(self.rotation.angle + pi / 2)
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))


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
        self.image = self.font.render(content, True, color).convert_alpha()
        super().__init__(x, y, self.image)
        self.update(content, color, anchor)

    def update(self, content: str = None, color: tuple = None, anchor: str = None):
        """
        Update the text image

        :param content: str, The content of the text
        :param color: tuple, The color (RGBA) of the text
        """
        self.content = content if content is not None else self.content
        self.color = color if color is not None else self.color
        self.anchor = anchor if anchor is not None else self.anchor
        self.image = self.font.render(self.content, True, self.color).convert_alpha()
        if self.anchor == "center":
            self.rect = self.image.get_rect(center=(self.x, self.y))
        elif self.anchor == "left":
            self.rect = self.image.get_rect(midleft=(self.x, self.y))
        elif self.anchor == "right":
            self.rect = self.image.get_rect(midright=(self.x, self.y))


class Explosion(Object):
    """
    Represent an animated explosion

    :param x: int, The x coordinate of the explosion
    :param y: int, The x coordinate of the explosion
    """

    def __init__(self, x: int, y: int):
        self.step = 1
        self.last_update = time()
        super().__init__(x, y, "Explosion1.png")

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
        self.last_update = time()
        self.set_image(f"Explosion{self.step}.png")

    def draw(self, surface: pygame.Surface):
        """
        Draw the explosion on the surface

        :param surface: pygame.Surface, The surface to draw the explosion on
        """
        if self.step >= 6 and time() - self.last_update > 0.1:
            return
        super().draw(surface)
