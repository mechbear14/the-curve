from .utilities import canv2point, point2canv, func2plot
from .core import Point, MapFn
import numpy as np
from math import fabs
import tkinter as tk


class Handle:
    def __init__(self, point, canvas):
        self.point = point
        self.canvas = canvas
        self.x, self.y = point2canv(point.get(), canvas)
        coord = (self.x - 5, self.y - 5, self.x + 5, self.y + 5)
        self.ref = self.canvas.create_rectangle(coord, fill="", outline="#c80000", width="2")

    def move(self, x, y):
        self.x = x
        self.y = y
        coord = (x - 5, y - 5, x + 5, y + 5)
        self.canvas.coords(self.ref, coord)

    def destroy(self):
        self.canvas.delete(self.ref)

    def is_on_handle(self, mouse_x, mouse_y):
        return fabs(mouse_x - self.x) < 10 and fabs(mouse_y - self.y) < 10


class Curve:
    def __init__(self, map_func, canvas):
        self.func = map_func
        self.canvas = canvas
        self.refs = []

        cs = func2plot(map_func.map_v, canvas)
        for i in range(len(cs) - 1):
            coord = (*cs[i], *cs[i+1])
            self.refs.append(canvas.create_line(coord, fill="#800080", width=3))

    def move(self):
        cs = func2plot(self.func.map_v, self.canvas)
        for i in range(len(cs) - 1):
            coord = (*cs[i], *cs[i+1])
            self.canvas.coords(self.refs[i], coord)

    def is_on_curve(self, mouse_x, mouse_y):
        x, y = canv2point((mouse_x, mouse_y), self.canvas)
        yy = self.func.map(x)
        cx, cy = point2canv((x, yy), self.canvas)
        return fabs(mouse_y - cy) < 10

    def set_func(self, map_func):
        self.func = map_func
        self.move()


class Ruler:
    def __init__(self, map_func, normal_canvas, mapped_canvas):
        self.func = map_func
        self.normal_canvas = normal_canvas
        self.mapped_canvas = mapped_canvas
        self.refs = []

        xs = np.arange(0.0, 1.01, 0.05)

        # TODO: Refactor these three loops
        x_locs = xs * self.normal_canvas.winfo_width()
        y_loc = self.normal_canvas.winfo_height() / 2
        for line_id in range(21):
            if line_id % 5 == 0:
                coord = (x_locs[line_id], y_loc)
                self.normal_canvas.create_text(coord, text=line_id * 5, fill="#808080")
            else:
                coord = (x_locs[line_id], y_loc - 2, x_locs[line_id], y_loc + 2)
                self.normal_canvas.create_line(coord, width=2, fill="#808080")

        x_loc = self.mapped_canvas.winfo_width() / 2
        y_locs = (1 - self.func.map_v(xs)) * self.mapped_canvas.winfo_height()
        for line_id in range(21):
            if line_id % 5 == 0:
                coord = (x_loc, y_locs[line_id])
                self.refs.append(self.mapped_canvas.create_text(coord, text=line_id * 5, fill="#808080"))
            else:
                coord = (x_loc - 2, y_locs[line_id], x_loc + 2, y_locs[line_id])
                self.refs.append(self.mapped_canvas.create_line(coord, width=2, fill="#808080"))

    def update(self):
        xs = np.arange(0.0, 1.01, 0.05)
        x_loc = self.mapped_canvas.winfo_width() / 2
        y_locs = (1 - self.func.map_v(xs)) * self.mapped_canvas.winfo_height()
        for line_id in range(21):
            if line_id % 5 == 0:
                coord = (x_loc, y_locs[line_id])
            else:
                coord = (x_loc - 2, y_locs[line_id], x_loc + 2, y_locs[line_id])
            self.mapped_canvas.coords(self.refs[line_id], coord)

    def set_func(self, map_func):
        self.func = map_func
        self.update()


class CurveEditor:
    def __init__(self, canvas, ruler_in, ruler_out):
        self.canvas = canvas
        self.bound = MapFn()
        self.update_func = None
        self.handles = [Handle(p, self.canvas) for p in self.bound.get_points()]
        self.draw_grid()
        self.curve = Curve(self.bound, self.canvas)
        self.ruler = Ruler(self.bound, ruler_in, ruler_out)
        self.dragging = None

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<Button-3>", self.on_mouse_right)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def bind(self, map_func, update_fn=None):
        self.bound = map_func
        if update_fn is not None:
            self.update_func = update_fn
        for h in self.handles:
            h.destroy()
        self.handles = [Handle(p, self.canvas) for p in map_func.get_points()]
        self.curve.set_func(map_func)
        self.ruler.set_func(map_func)

    def reset(self):
        self.bind(MapFn(), None)

    def on_which_handle(self, mouse_x, mouse_y):
        for i, handle in enumerate(self.handles):
            if handle.is_on_handle(mouse_x, mouse_y):
                return i
        return -1

    def draw_grid(self):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        small_space = width / 20
        for line_id in range(21):
            x_loc = line_id * small_space
            coord = (x_loc, 0, x_loc, height)
            line_width = 2 if line_id % 5 == 0 else 1
            self.canvas.create_line(coord, fill="#c8c8c8", width=line_width)
            y_loc = line_id * small_space
            coord = (0, y_loc, width, y_loc)
            line_width = 2 if line_id % 5 == 0 else 1
            self.canvas.create_line(coord, fill="#c8c8c8", width=line_width)

    def on_mouse_down(self, event):
        on_curve = self.curve.is_on_curve(event.x, event.y)
        on_handle = self.on_which_handle(event.x, event.y)
        if on_curve:
            if on_handle > -1:
                self.dragging = on_handle
            else:
                self.dragging = self.add_handle(event.x, event.y)
            self.canvas.bind("<B1-Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        self.bound.move_point(self.dragging, *canv2point((event.x, event.y), self.canvas))
        self.handles[self.dragging].move(event.x, event.y)
        self.curve.move()
        self.ruler.update()

    def on_mouse_up(self, event):
        if self.update_func is not None:
            self.update_func()
        self.dragging = None
        self.canvas.unbind("<B1-Motion>")

    def on_mouse_right(self, event):
        on_handle = self.on_which_handle(event.x, event.y)
        if on_handle > -1:
            self.drop_handle(on_handle)
        if self.update_func is not None:
            self.update_func()

    def add_handle(self, mouse_x, mouse_y):
        x, y = canv2point((mouse_x, mouse_y), self.canvas)
        new_point = Point(x, y)
        self.bound.add_point(*new_point.get())
        self.handles.append(Handle(new_point, self.canvas))
        self.curve.move()
        self.ruler.update()
        return len(self.handles) - 1

    def drop_handle(self, i):
        if len(self.handles) > 2:
            self.handles[i].destroy()
            self.handles.remove(self.handles[i])
            self.bound.drop_point(i)
            self.curve.move()
            self.ruler.update()
