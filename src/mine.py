from src.base import Object


class Mine(Object):
    """
    class Mine:

    - position (in px): x,y (type -> int)
    - shape (in px) : height,width (type -> int)
    - status (alive/destroyed)  : status (type -> bool)

    """

    def __init__(
        self, width: int = 0, height: int = 0, x: int = 0, y: int = 0, points: int = 0
    ):
        """
        initialisation
        """
        super().__init__(width, height, x, y)
        self.points = points


class PhotonMine(Mine):
    """
    class Photon_Mine:

    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        initialisation
        """
        super().__init__(15, 15, x, y, 350)
        self.set_image("PhotonMine2.png")


class VaporMine(Mine):
    """
    class Vapor_Mine:

    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        initialisation
        """
        super().__init__(25, 25, x, y, 500)
        self.set_image("VaporMine2.png")
