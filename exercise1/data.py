from point import Point, Cluster

def getPointByName(name):
    for p in data:
        if p.name == name:
            return p

def getListOfNames():
    list = []
    for p in data:
        list.append(p.name)

    return p

data = [
    Point(2, 'x1'),
    Point(3, 'x2'),
    Point(4, 'x3'),
    Point(12, 'x4'),
    Point(13, 'x5'),
    Point(14, 'x6'),
    Point(15, 'x7'),
    Point(16, 'x8'),
]

cluster1 = Cluster(1, [data[0], data[1], data[2], data[3], data[4]], data)
cluster2 = Cluster(2, [data[5], data[6], data[7]], data)