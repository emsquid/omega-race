import pygame
from src.base import Object, Text
from src.settings import Settings


class Scores:
    """
    The scores of the game
    """

    def __init__(self):
        self.highscore = 0

        self.title = Text("Scores", 500, 150, size=90)

    def get_objects(self) -> tuple[Object]:
        """
        Get every object handled by the scores

        :return: tuple[Object], All objects
        """
        # TODO
        return [self.title]

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
        """
        Handle user inputs in the settings

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        pass

    def update(self, score: int):
        """
        Update the highscore

        :param score: int, The current score
        """
        self.highscore = max(score, self.highscore)
