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
    xs = np.arange(0.0, 1.01, 0.01)
    ys = map_func(xs)
    cs = []
    for i in range(len(xs)):
        cs.append(point2canv((xs[i], ys[i]), canvas))
    return cs


def fit2canvas(width, height, canvas_width, canvas_height):
    attempt = height / (width / canvas_width) > canvas_height
    if attempt:
        return round(canvas_width / (height / canvas_height)), canvas_height
    else:
        return canvas_width, round(height / (width / canvas_width))
