import pygame
from src.base import Object

class Ship(Object):
    """
    class Ship:

    -location (in px): x,y (type -> int)
    -direction (in px) : dx,dy (type -> int)
    -shape (in px) : hight,wigth (type -> int)
    -status (alive/destroyed)  : status (type -> bool)

    """

    def __init__(self, width: int, height: int
                 x: int, y: int, dx: int, dy: int):
        """
        initilisation
        """
        super.__init__(width, height,  x, y, dx, dy)

    def bounceX(self):
        self.dx = -self.dx

    def bounceY(self):
        self.dy = -self.dy

    def destroy(self):
        self.status = False
