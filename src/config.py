import pygame
from src.const import WHITE


class Config:
    """
    The Config stores user informations
    """

    def __init__(self):
        self.read()

    def update_key(self, action: str, key: int):
        """
        Update the key for an action

        :param action: str, The action to change the key for
        :param key: int, The new key
        """
        if key not in list(self.keys.values()) + [pygame.K_RETURN, pygame.K_ESCAPE]:
            self.keys[action] = key

    def read(self):
        """
        Read the config from file if it exists, else use defaults
        """
        try:
            with open(".config", "r") as file:
                config = eval(file.read())
                self.name = config["name"]
                self.keys = config["keys"]
                self.volume = config["volume"]
                self.fps = config["fps"]
                self.color = config["color"]
                self.mouse = config["mouse"]
        except Exception:
            self.name = ""
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
            self.color = WHITE
            self.mouse = False

    def save(self):
        """
        Save the config in a file
        """
        with open(".config", "w") as file:
            config = {
                "name": self.name,
                "keys": self.keys,
                "volume": self.volume,
                "fps": self.fps,
                "color": self.color,
                "mouse": self.mouse,
            }
            file.write(str(config))
