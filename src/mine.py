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


class Photon_Mine(Mine):
    """
    class Photon_Mine:

    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        initialisation
        """
        super().__init__(self, 10, 5, x, y, 350)


class Vapor_Mine(Mine):
    """
    class Vapor_Mine:

    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        initialisation
        """
        super().__init__(self, 10, 10, x, y, 500)
