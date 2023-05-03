import pygame
from src.const import WHITE, RED
from src.base import Text


class Home:
    """
    -
    """

    def __init__(self):
        """
        -
        """
        self.selection = 0

    def draw(self, surface: pygame.Surface):
        """
        -
        """
        self.title = Text("Omega Race", 500, 100, WHITE, 90)
        self.title.draw(surface)

        self.play = Text("Play", 500, 350, RED if self.selection == 0 else WHITE, 40)
        self.play.draw(surface)

        self.scores = Text(
            "Scores", 500, 450, RED if self.selection == 1 else WHITE, 40
        )
        self.scores.draw(surface)

        self.settings = Text(
            "Settings", 500, 550, RED if self.selection == 2 else WHITE, 40
        )
        self.settings.draw(surface)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selection = (self.selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selection = (self.selection + 1) % 3
