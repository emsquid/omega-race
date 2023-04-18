import pygame


class Mine():
    """
    class Mine:

    -location (in px): x,y (type -> int)
    -shape (in px) : hight,wigth (type -> int)
    -status (alive/destroyed)  : status (type -> bool)

    """

    def __init__(self, hight: int, width: int, x: int, y: int):
        """
        initialisation
        """
        self.hight = hight
        self.width = width
        self.x = x
        self.y = y
        self.status = True

    def destroy(self):
        self.status = False
