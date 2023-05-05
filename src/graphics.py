import math
import pygame
from threading import Timer
from time import time
from random import randrange, random
from src.base import Object, Entity, Text
from src.sprites import Player, Laser
from src.const import WIN_WIDTH, WIN_HEIGHT, BLACK, WHITE, GREEN, YELLOW, ORANGE, RED


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

    def update(self, dt: int):
        """
        Move stars on the background
        """
        test = pygame.Surface((WIN_WIDTH, WIN_HEIGHT)).convert_alpha()
        test.fill((0, 0, 0, 20))
        self.image.blit(test, (0, 0))
        for star in self.stars:
            pygame.draw.line(self.image, WHITE, (star[0], star[1]), (star[0], star[1]))
            star[1] -= star[2] * dt
            if star[1] < 0:
                star[0] = randrange(WIN_WIDTH)
                star[1] = WIN_HEIGHT


class Panel:
    """
    The Panel is used to display scores and player lives
    """

    def __init__(self):
        self.level = Text("LEVEL 1", 460, 325, GREEN, anchor="topleft")
        self.score_text = Text("SCORE", 330, 325, anchor="topleft")
        self.score = Text("0", 330, 360, anchor="topleft")
        self.highscore_text = Text("HIGHSCORE", 330, 415, anchor="topleft")
        self.highscore = Text("0", 330, 445, anchor="topleft")
        self.image = pygame.image.load("assets/Player1.png")
        self.lives = 3

    def draw(self, surface: pygame.Surface):
        """
        Draw the panel elements on the surface
        """
        self.level.draw(surface)
        self.score_text.draw(surface)
        self.score.draw(surface)
        self.highscore_text.draw(surface)
        self.highscore.draw(surface)
        for i in range(self.lives):
            surface.blit(self.image, (630, 330 + 50 * i))

    def update(self, lives: int, level: int, score: int, highscore: int):
        """
        Update lives and score
        """
        self.lives = lives
        self.level.set_content(f"LEVEL {level}")
        self.level.set_color([WHITE, GREEN, YELLOW, ORANGE, RED][min(level - 1, 4)])
        self.score.set_content(str(score))
        self.highscore.set_content(str(highscore))


class Border(Object):
    """
    A Border draws the boundaries of the game field
    It will bounce objects on collision
    """

    def __init__(
        self, width: int, height: int, x: int, y: int, normal: float, visible: bool
    ):
        super().__init__(width, height, x, y)
        self.normal = normal
        self.visible = visible

    def draw(self, surface):
        """
        Draw a border on the surface,
        The image differs if the border is visible
        """
        image = pygame.Surface((self.width, self.height))
        if self.visible:
            image.fill(WHITE)
        else:
            image.fill(WHITE, (0, 0, 3, 3))
            image.fill(WHITE, (self.width - 3, self.height - 3, 3, 3))
        surface.blit(image, (self.x - self.width / 2, self.y - self.height / 2))

    def bounce(self, sprite: Entity):
        """
        Bounce objects that collide with this border
        The object should be a ship or the player
        """
        # We use dot product to know if the object should bounce on the collided border
        dot = math.cos(self.normal) * math.cos(sprite.direction) + math.sin(
            self.normal
        ) * math.sin(sprite.direction)
        if self.collide(sprite) and dot < 0:
            if round(math.cos(self.normal), 5) != 0:
                sprite.set_direction(math.pi - sprite.direction)
            else:
                sprite.set_direction(-sprite.direction)
            if isinstance(sprite, Player):
                sprite.set_speed(sprite.speed * 0.75)
                sprite.last_collision = time()
            self.blink()

    def show(self):
        """
        Make the border visible
        """
        self.visible = True

    def hide(self):
        """
        Make the border invisible
        """
        self.visible = False

    def blink(self):
        """
        Make the border blink, it will show then hide after 0.15s
        """
        if not self.visible:
            self.show()
            Timer(0.15, self.hide).start()


class ForceField:
    """
    The Force Field handles all borders simultaneously
    """

    def __init__(self):
        # Border for the boundaries of the game field
        self.borders = [
            # Left and right borders
            Border(3, 383, 20, 210, 0, False),
            Border(3, 383, 20, 590, 0, False),
            Border(3, 383, 980, 210, math.pi, False),
            Border(3, 383, 980, 590, math.pi, False),
            # Top and bottom borders
            Border(483, 3, 260, 20, math.pi / 2, False),
            Border(483, 3, 740, 20, math.pi / 2, False),
            Border(483, 3, 260, 780, -math.pi / 2, False),
            Border(483, 3, 740, 780, -math.pi / 2, False),
            # Border for the display panel
            Border(3, 203, 700, 400, 0, True),
            Border(3, 203, 300, 400, math.pi, True),
            Border(403, 3, 500, 500, math.pi / 2, True),
            Border(403, 3, 500, 300, -math.pi / 2, True),
        ]

    def draw(self, surface: pygame.Surface):
        """
        Draw all borders on the surface
        """
        for border in self.borders:
            border.draw(surface)

    def bounce(self, *sprites: tuple[Entity]):
        """
        Check if the objects should bounce on any border
        """
        for obj in sprites:
            for border in self.borders:
                border.bounce(obj)

    def crash(self, *lasers: tuple[Laser]):
        """
        Check if the lasers should crash on any border
        """
        for laser in lasers:
            for border in self.borders:
                if laser.collide(border):
                    laser.die()
                    border.blink()
                    break
