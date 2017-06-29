import math


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


class Point:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.processed = False
        self.core_object = False
        self.noise = False
        self.cluster = None
        self.name = name

    def __str__(self):
        return "{0}:=({1},{2})".format(self.name, self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (other.x == self.x) and (other.y == self.y) and (other.name == self.name)

    def __hash__(self):
        return hash((self.x, self.y, self.name))

    def distance_to(self, point):
        return distance(self, point)

class Cluster:
    i = 1
    def __init__(self):
        self.points = set()
        self.index = Cluster.i
        Cluster.i += 1

    def add_point(self, point):
        self.points.add(point)

    def remove_point(self, point):
        self.points.remove(point)
