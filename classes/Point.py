import math


class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    # covered with tests
    def get_x(self):
        return self._x

    # covered with tests
    def set_x(self, x):
        self._x = x

    # covered with tests
    def get_y(self):
        return self._y

    # covered with tests
    def set_y(self, y):
        self._y = y

    # covered with tests
    def __eq__(self, other):
        if isinstance(other, Point):
            # Use math.isclose with a default relative tolerance of 1e-9 and an absolute tolerance of 0.0
            return math.isclose(self._x, other.get_x()) and math.isclose(self._y, other.get_y())
        return False

    # covered with tests
    def __str__(self):
        return f'Point({self.get_x()}, {self.get_y()})'

    # covered with tests
    __repr__ = __str__

    # covered with tests
    def __hash__(self):
        return hash((self._x, self._y))

    # covered with tests
    def distance_to(self, other):
        return math.sqrt((self._x - other.get_x()) ** 2 + (self._y - other.get_y()) ** 2)

    def __add__(self, other):
        return Point(self._x + other.get_x(), self._y + other.get_y())

    def __sub__(self, other):
        return Point(self._x - other.get_x(), self._y - other.get_y())

    def __mul__(self, scalar):
        return Point(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar):
        return Point(self._x / scalar, self._y / scalar)

    def to_list(self):
        return [self._x, self._y]

    @staticmethod
    def from_list(data):
        return Point(data[0], data[1])