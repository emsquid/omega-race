import pygame
from src.const import SCREEN_WIDTH, SCREEN_HEIGHT


class Object:
    def __init__(self, width: int = 0,  height: int = 0,
                 x: int = 0, y: int = 0, dx: int = 0, dy: int = 0):
        """
        initialisation
        """
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

    def set_image(self, name: str):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))

    def move(self, dt: float):
        if self.x < 0 or self.x+self.width > SCREEN_WIDTH:
            self.dx = -self.dx
        if self.y < 0 or self.y + self.height > SCREEN_HEIGHT:
            self.dy = -self.dy
        self.x += self.dx*dt
        self.y += self.dy*dt

    def collide(self, other) -> bool:
        return (self.x <= other.x+other.width 
                and other.x <= self.x+self.width
                and self.y <= other.y+other.height 
                and other.y <= self.y+self.height)
