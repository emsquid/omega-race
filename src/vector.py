from __future__ import annotations
from math import cos, sin, sqrt, atan2


class Vector:
    """
    Represent a vector in 2D

    :param x: float, The x coordinate of the vector
    :param y: float, The y coordinate of the vector
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other) -> Vector:
        """
        Get the sum of a vector and another object

        :param other: Any, The object to sum up with
        :return: Vector, The resulting vector
        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector(self.x + other[0], self.y + other[1])
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        else:
            raise TypeError(f"can't add '{type(other).__name__}' to Vector")

    def __sub__(self, other) -> Vector:
        """
        Get the substraction of a vector by another object

        :param other: Any, The object to sum up with
        :return: Vector, The resulting vector
        """
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector(self.x - other[0], self.y - other[1])
        elif isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        else:
            raise TypeError(f"can't substract '{type(other).__name__}' to Vector")

    def __mul__(self, other) -> Vector:
        """
        Get the product of a vector and another object

        :param other: Any, The object to product with
        :return: Vector, The resulting vector
        """
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector(self.x * other[0], self.y * other[1])
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError(f"can't multiply Vector by '{type(other).__name__}'")

    def __truediv__(self, other) -> Vector:
        """
        Get the division of a vector by another object

        :param other: Any, The object to divide by
        :return: Vector, The resulting vector
        """
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector(self.x / other[0], self.y / other[1])
        elif isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        else:
            raise TypeError(f"can't divide Vector by '{type(other).__name__}'")

    @property
    def norm(self) -> float:
        """
        Get the norm of the vector

        :return: float, The norm of the vector
        """
        return sqrt(self.x * self.x + self.y * self.y)

    @property
    def angle(self) -> float:
        """
        Get the angle of the vector

        :return: float, The angle in radians
        """
        return atan2(self.y, self.x)

    def det(self, other: Vector) -> float:
        """
        Get the determinant of two vectors

        :param other: Vector, The other vector
        :return: float, The resulting determinant
        """
        return self.x * other.y - self.y * other.x

    def dot(self, other: Vector) -> float:
        """
        Get the dot product of two vectors

        :param other: Vector, The other vector
        :return: float, The resulting dot product
        """
        return self.x * other.x + self.y * other.y

    def angle_to(self, other: Vector) -> float:
        """
        Get the angle to the other vector

        :param other: Vector, The other vector
        :return: float, The angle to the other vector
        """
        return atan2(self.det(other), self.dot(other))

    def copy(self) -> Vector:
        """
        Get a copy of the vector

        :return: Vector, A copy of the vector
        """
        return Vector(self.x, self.y)

    def normalized(self) -> Vector:
        """
        Get a normalized vector

        :return: Vector, the normalized vector
        """
        return Vector(self.x, self.y) / self.norm

    def normal(self) -> Vector:
        """
        Get the normal of the vector

        :return: Vector, The normal of the vector
        """
        return Vector(-self.y, self.x)

    def rotate(self, angle: float) -> Vector:
        """
        Rotate the vector by the given angle

        :param angle: float, The angle (radians) to rotate by
        :return: Vector, the rotated vector
        """
        return Vector(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle),
        )

    def reflect(self, normal: Vector) -> Vector:
        """
        Reflect the vector with the given normal

        :param normal: Vector, The normal to reflect with
        :return: Vector, the reflected vector
        """
        return self - normal * 2 * self.dot(normal)
