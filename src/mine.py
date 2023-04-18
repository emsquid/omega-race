import pygame


class Mine:
    """
    class Mine:

    - location (in px): x,y (type -> int)
    - shape (in px) : hight,wigth (type -> int)
    - status (alive/destroyed)  : status (type -> bool)

    """

    def __init__(
        self, height: int = None, width: int = None, x: int = None, y: int = None
    ):
        """
        initialisation
        """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.status = True

    def destroy(self):
        self.status = False
