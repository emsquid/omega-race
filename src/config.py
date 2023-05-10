import os.path
import pygame


class Config:
    """
    The Config stores user informations
    """

    def __init__(self):
        self.name = ""
        self.read()

    def update_key(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key != pygame.K_RETURN and key not in self.keys.values():
            self.keys[action] = key

    def read(self):
        if os.path.exists(".config"):
            with open(".config", "r") as file:
                config = eval(file.read())
                self.keys = config["keys"]
                self.volume = config["volume"]
                self.fps = config["fps"]
        else:
            self.keys = {
                "UP": pygame.K_UP,
                "DOWN": pygame.K_DOWN,
                "LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT,
                "SHOOT": pygame.K_SPACE,
                "PAUSE": pygame.K_p,
            }
            self.volume = 1
            self.fps = 120

    def save(self):
        with open(".config", "w") as file:
            config = {
                "keys": self.keys,
                "volume": self.volume,
                "fps": self.fps,
            }
            file.write(str(config))
