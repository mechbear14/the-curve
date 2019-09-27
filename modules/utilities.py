import numpy as np


def canv2point(point, canvas):
    x, y = point
    width, height = canvas.winfo_width(), canvas.winfo_height()
    px = x / width
    py = 1 - y / height
    return px, py


def point2canv(point, canvas):
    x, y = point
    width, height = canvas.winfo_width(), canvas.winfo_height()
    cx = x * width
    cy = (1 - y) * height
    return cx, cy


def func2plot(map_func, canvas):
    xs = np.arange(0.0, 0.01, 1.01)
    ys = map_func(xs)
    cs = []
    for i in range(len(xs)):
        cs.append(point2canv((xs, ys), canvas))
    return cs
