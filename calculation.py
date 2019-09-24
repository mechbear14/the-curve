class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def get(self):
        return self.x, self.y


class MapFn:
    def __init__(self, points):
        self.points = points
        self.xs = list(map(lambda p: p.get()[0], points))
        self.ys = list(map(lambda p: p.get()[1], points))

    def map(self, x):
        result = 0
        for i in range(len(self.ys)):
            yi = self.ys[i]
            py = 1
            for j in range(len(self.xs)):
                if i != j:
                    py *= (x - self.xs[j]) / (self.xs[i] - self.xs[j])
                    if py == 0:
                        break
            result += yi * py
        return result

    def add_point(self, x, y):
        self.points.append(Point(x, y))

    def move_point(self, i, x, y):
        self.points[i].update(x, y)

    def drop_point(self, i):
        try:
            self.points.remove(self.points[i])
        except ValueError:
            print(f"Point {i} is not in the points")