import pygame


class Ship():
    """
    class Ship:

    -location (in px): x,y (type -> int)
    -direction (in px) : dx,dy (type -> int)
    -shape (in px) : hight,wigth (type -> int)
    -status (alive/destroyed)  : status (type -> bool)

    """

    def __init__(self, hight: int, width: int,
                 x: int, y: int, dx: int, dy: int):
        """
        initilisation
        """

        self.hight = hight
        self.width = width
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.status = True

    def bounceX(self):
        self.dx = -self.dx

    def bounceY(self):
        self.dy = -self.dy

    def destroy(self):
        self.status = False
