from calculation import Point, MapFn
import numpy as np
from math import fabs

points = [Point(0, 0), Point(1, 1), Point(-1, -1), Point(2, 8)]
mapFn = np.vectorize(MapFn(points).map)
correctFn = np.vectorize(lambda x: x * x * x)

xs = np.arange(0.0, 1.0, 0.01)
y1s = mapFn(xs)
y2s = correctFn(xs)

for i in range(len(xs)):
    try:
        assert fabs(y1s[i] - y2s[i]) < 1E-6
    except AssertionError:
        print(f"y1 is {y1s[i]}")
        print(f"correct value is {y2s[i]}")
