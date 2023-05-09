import pygame
from time import time
from threading import Timer
from math import pi, cos, sin
from random import randrange, random
from src.objects.base import Object, Entity, Text
from src.objects.sprites import Player, Laser
from src.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    CEN_X,
    CEN_Y,
    PAN_WIDTH,
    PAN_HEIGHT,
    BLACK,
    WHITE,
    GREEN,
    YELLOW,
    ORANGE,
    RED,
)


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

        :param dt: int, The time delta between frames
        """
        # test = pygame.Surface((WIN_WIDTH, WIN_HEIGHT)).convert_alpha()
        # test.fill((0, 0, 0, min(int(dt * 3), 255)))
        # self.image.blit(test, (0, 0))
        self.image.fill(BLACK)
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
        self.level = Text("LEVEL 1", 460, 325, color=GREEN, anchor="topleft")
        self.score_text = Text("SCORE", 330, 325, anchor="topleft")
        self.score = Text("0", 330, 360, anchor="topleft")
        self.highscore_text = Text("HIGHSCORE", 330, 415, anchor="topleft")
        self.highscore = Text("0", 330, 445, anchor="topleft")
        self.image = pygame.image.load("assets/images/Player1.png")
        self.lives = 3

    def draw(self, surface: pygame.Surface):
        """
        Draw the panel elements on the surface

        :param surface: pygame.Surface, The surface to draw the panel on
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
        Update lives, level and scores

        :param lives: int, The lives of the player
        :param level: int, The level the player is at
        :param score: int, The score of the player
        :param highscore: int, The game highest score
        """
        self.lives = lives
        self.level.update(
            f"LEVEL {level}",
            [WHITE, GREEN, YELLOW, ORANGE, RED][min(level - 1, 4)],
        )
        self.score.update(content=str(score))
        self.highscore.update(content=str(highscore))


class Border(Object):
    """
    A Border draws the boundaries of the game field
    It will bounce entities on collision and crash lasers

    :param x: int, The x coordinate of the border
    :param y: int, The y coordinate of the border
    :param width: int, The width of the border
    :param height: int, The height of the border
    :param normal: float, The normal (radians) of the border (to bounce)
    :param visible: bool, Whether the border is usually visible or not
    """

    def __init__(
        self, x: int, y: int, width: int, height: int, normal: float, visible: bool
    ):
        super().__init__(x, y, width, height, pygame.Surface((width, height)))
        self.normal = normal
        self.visible = visible
        self.changed = True

    def show(self):
        """
        Make the border visible
        """
        self.visible = True
        self.changed = True

    def hide(self):
        """
        Make the border invisible
        """
        self.visible = False
        self.changed = True

    def blink(self):
        """
        Make the border blink, it will show then hide after 0.15s
        """
        if self.visible:
            return
        self.show()
        Timer(0.15, self.hide).start()

    def update(self):
        """
        Update the state of the border
        """
        if not self.changed:
            return
        image = pygame.Surface((self.width, self.height))
        if self.visible:
            image.fill(WHITE)
        else:
            image.fill(WHITE, (0, 0, 3, 3))
            image.fill(WHITE, (self.width - 3, self.height - 3, 3, 3))
        self.set_image(image)
        self.changed = False

    def bounce(self, entity: Entity):
        """
        Bounce entities that collide with this border

        :param entity: Entity, The entity to bounce
        """
        dot = cos(self.normal) * cos(entity.direction) + sin(self.normal) * sin(
            entity.direction
        )
        # We use dot product to know if the object should bounce on the collided border
        if entity.collide(self) and dot < 0:
            if round(cos(self.normal), 5) != 0:
                entity.set_direction(pi - entity.direction)
            else:
                entity.set_direction(-entity.direction)
            # Slow player
            if isinstance(entity, Player):
                entity.set_speed(entity.speed * 0.75)
                entity.last_collision = time()
            # Crash lasers
            elif isinstance(entity, Laser):
                entity.die()
            self.blink()


class ForceField:
    """
    The Force Field handles all borders simultaneously
    """

    def __init__(self):
        # Border for the boundaries of the game field
        self.borders = [
            # Left and right borders
            Border(20, WIN_HEIGHT / 4 + 10, 3, CEN_Y - 17, 0, False),
            Border(20, WIN_HEIGHT * 3 / 4 - 10, 3, CEN_Y - 17, 0, False),
            Border(WIN_WIDTH - 20, WIN_HEIGHT / 4 + 10, 3, CEN_Y - 17, pi, False),
            Border(WIN_WIDTH - 20, WIN_HEIGHT * 3 / 4 - 10, 3, CEN_Y - 17, pi, False),
            # Top and bottom borders
            Border(WIN_WIDTH / 4 + 10, 20, CEN_X - 17, 3, pi / 2, False),
            Border(WIN_WIDTH * 3 / 4 - 10, 20, CEN_X - 17, 3, pi / 2, False),
            Border(WIN_WIDTH / 4 + 10, WIN_HEIGHT - 20, CEN_X - 17, 3, -pi / 2, False),
            Border(
                WIN_WIDTH * 3 / 4 - 10, WIN_HEIGHT - 20, CEN_X - 17, 3, -pi / 2, False
            ),
            # Border for the display panel
            Border(CEN_X - PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, pi, True),
            Border(CEN_X + PAN_WIDTH / 2, CEN_Y, 3, PAN_HEIGHT + 3, 0, True),
            Border(CEN_X, CEN_Y - PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, -pi / 2, True),
            Border(CEN_X, CEN_Y + PAN_HEIGHT / 2, PAN_WIDTH + 3, 3, pi / 2, True),
        ]

    def draw(self, surface: pygame.Surface):
        """
        Draw all borders on the surface

        :param surface: pygame.Surface, The surface to draw the force field on
        """
        for border in self.borders:
            border.draw(surface)

    def update(self):
        """
        Update the state of the force field
        """
        for border in self.borders:
            border.update()

    def bounce(self, *entities: tuple[Entity]):
        """
        Check if the entities should bounce on any border

        :param entities: tuple[Entity], The entities to bounce
        """
        for entity in entities:
            for border in self.borders:
                border.bounce(entity)
