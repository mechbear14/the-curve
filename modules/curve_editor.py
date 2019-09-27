import numpy as np
from math import fabs
import tkinter as tk


class Handle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ref = None

        self.render()

    def get(self):
        return self.x, self.y

    def render(self):
        coord = (self.x - 5, self.y - 5, self.x + 5, self.y + 5)
        self.ref = self.canvas.create_rectangle(coord, fill="", outline="#c80000", width="2")

    def move(self, x, y):
        self.x = x
        self.y = y
        coord = (x - 5, y - 5, x + 5, y + 5)
        self.canvas.coords(self.ref, coord)

    def destroy(self):
        self.canvas.delete(self.ref)


class Ruler:
    def __init__(self, normal_canvas, mapped_canvas):
        self.normal_canvas = normal_canvas
        self.mapped_canvas = mapped_canvas
        self.normal = np.arange(0.0, 1.01, 0.05)
        self.mapped = self.normal
        self.render_horizontal(self.normal_canvas, self.normal)
        self.render_vertical(self.mapped_canvas, self.mapped)

    def map(self, map_func):
        f = np.vectorize(map_func)
        self.mapped = f(self.normal)

    def render_horizontal(self, canvas, array):
        width, height = canvas.winfo_width(), canvas.winfo_height()
        canvas.create_rectangle((0, 0, width, height), fill="#ffffff")
        y_loc = height / 2
        for line_id in range(21):
            x_loc = array[line_id] * width
            if line_id % 5 == 0:
                coord = (x_loc, y_loc)
                canvas.create_text(coord, text=line_id * 5, fill="#808080")
            else:
                coord = (x_loc, y_loc - 2, x_loc, y_loc + 2)
                canvas.create_line(coord, width=2, fill="#808080")

    def render_vertical(self, canvas, array):
        width, height = canvas.winfo_width(), canvas.winfo_height()
        canvas.create_rectangle((0, 0, width, height), fill="#ffffff")
        x_loc = width / 2
        for line_id in range(21):
            y_loc = (1 - array[line_id]) * height
            if line_id % 5 == 0:
                coord = (x_loc, y_loc)
                canvas.create_text(coord, text=line_id * 5, fill="#808080")
            else:
                coord = (x_loc - 2, y_loc, x_loc + 2, y_loc)
                canvas.create_line(coord, width=2, fill="#808080")

    def update(self, map_func):
        self.map(map_func)
        self.mapped_canvas.delete(tk.ALL)
        self.render_vertical(self.mapped_canvas, self.mapped)


class Canvas:
    def __init__(self, ref, map_func):
        self.ref = ref
        self.width = self.ref.winfo_width() - 2
        self.height = self.ref.winfo_height() - 2
        self.map = map_func
        self.handles = list(map(self.point2handle, self.map.get_points()))
        self.curve_refs = []
        self.dragging = False
        self.dragging_handle_id = None
        self.attached = []

        self.draw_grid()
        self.draw_curve()
        self.draw_handles()

        self.ref.bind("<Button-1>", self.on_mouse_down)
        self.ref.bind("<Button-3>", self.on_mouse_right)
        self.ref.bind("<ButtonRelease-1>", self.on_mouse_up)

    def attach(self, obj):
        self.attached.append(obj)
        self.update()

    def canv2point(self, x, y):
        px = x / self.width
        py = 1 - y / self.height
        return px, py

    def point2canv(self, x, y):
        cx = x * self.width
        cy = (1 - y) * self.height
        return cx, cy

    def point2handle(self, point):
        handle_xy = self.point2canv(*point.get())
        return Handle(self.ref, *handle_xy)

    def draw_grid(self):
        self.ref.create_rectangle((1, 1, self.width - 1, self.height - 1), fill="#ffffff")
        small_space = self.width / 20
        for line_id in range(21):
            x_loc = line_id * small_space
            coord = (x_loc, 0, x_loc, self.height)
            line_width = 2 if line_id % 5 == 0 else 1
            self.ref.create_line(coord, fill="#c8c8c8", width=line_width)
            y_loc = line_id * small_space
            coord = (0, y_loc, self.width, y_loc)
            line_width = 2 if line_id % 5 == 0 else 1
            self.ref.create_line(coord, fill="#c8c8c8", width=line_width)

    def draw_curve(self):
        xs = np.arange(0.0, 1.01, 0.01)
        f = np.vectorize(self.map.map)
        ys = f(xs)
        for i in range(len(xs) - 1):
            p1 = self.point2canv(xs[i], ys[i])
            p2 = self.point2canv(xs[i+1], ys[i+1])
            coord = (*p1, *p2)
            self.curve_refs.append(self.ref.create_line(coord, fill="#800080", width=3))

    def draw_handles(self):
        for handle in self.handles:
            handle.render()

    def is_on_curve(self, mx, my):
        x, y = self.canv2point(mx, my)
        yy = self.map.map(x)
        cx, cy = self.point2canv(x, yy)
        return fabs(my - cy) < 10

    def on_which_handle(self, mx, my):
        for i, handle in enumerate(self.handles):
            hx, hy = handle.get()
            on_this_handle = fabs(mx - hx) < 10 and fabs(my - hy) < 10
            if on_this_handle:
                return i
        return -1

    def on_mouse_down(self, event):
        on_curve = self.is_on_curve(event.x, event.y)
        on_handle = self.on_which_handle(event.x, event.y)
        if on_curve:
            if on_handle > -1:
                self.dragging_handle_id = on_handle
            else:
                self.dragging_handle_id = self.add_handle(event.x, event.y)

            self.dragging = True
            self.ref.bind("<B1-Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        self.move_handle(self.dragging_handle_id, event.x, event.y)
        self.move_curve()
        self.update()

    def on_mouse_up(self, event):
        self.dragging = False
        self.dragging_handle_id = None
        self.ref.unbind("<B1-Motion>")

    def on_mouse_right(self, event):
        on_handle = self.on_which_handle(event.x, event.y)
        if on_handle > -1:
            self.drop_handle(on_handle)
        self.update()

    def add_handle(self, x, y):
        new_handle = Handle(self.ref, x, y)
        self.handles.append(new_handle)
        new_point = self.canv2point(x, y)
        self.map.add_point(*new_point)
        return len(self.handles) - 1

    def move_handle(self, i, x, y):
        self.handles[i].move(x, y)
        self.map.move_point(i, *self.canv2point(x, y))
        self.move_curve()

    def move_curve(self):
        xs = np.arange(0.0, 1.01, 0.01)
        f = np.vectorize(self.map.map)
        ys = f(xs)
        for i in range(len(xs) - 1):
            p1 = self.point2canv(xs[i], ys[i])
            p2 = self.point2canv(xs[i+1], ys[i+1])
            coord = (*p1, *p2)
            self.ref.coords(self.curve_refs[i], coord)

    def drop_handle(self, i):
        if len(self.handles) > 2:
            self.handles[i].destroy()
            self.handles.remove(self.handles[i])
            self.map.drop_point(i)
            self.move_curve()

    def update(self):
        for a in self.attached:
            a.update(self.map.map)