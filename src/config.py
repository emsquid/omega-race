import pygame


class Config:
    """
    The Config stores user informations
    """

    def __init__(self):
        self.name = ""

        self.keys = {
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "SHOOT": pygame.K_SPACE,
        }

        self.volume = 1
        self.fps=120
    def update_key(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key != pygame.K_RETURN and key not in self.keys.values():
            self.keys[action] = key
