import numpy as np


class Handle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

    def update(self, x, y):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.render()

    def get(self):
        return self.x, self.y

    def render(self):
        coord = (self.x - 5, self.y - 5, self.x + 5, self.y + 5)
        self.canvas.create_rectangle(coord, fill="", outline="#c80000", width="2")


class Ruler:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()
        self.normal = np.arange(0.0, 1.01, 0.05)
        self.mapped = None
        self.horizontal = self.width > self.height

    def map(self, map_func):
        f = np.vectorize(map_func)
        self.mapped = f(self.normal)

    def render_horizontal(self, array):
        y_loc = self.height / 2
        for line_id in range(21):
            x_loc = array[line_id] * self.width
            if line_id % 5 == 0:
                coord = (x_loc, y_loc)
                self.canvas.create_text(coord, text=line_id * 5, fill="#808080")
            else:
                coord = (x_loc, y_loc - 2, x_loc, y_loc + 2)
                self.canvas.create_line(coord, width=2, fill="#808080")

    def render_vertical(self, array):
        x_loc = self.width / 2
        for line_id in range(21):
            y_loc = (1 - array[line_id]) * self.height
            if line_id % 5 == 0:
                coord = (x_loc, y_loc)
                self.canvas.create_text(coord, text=line_id * 5, fill="#808080")
            else:
                coord = (x_loc - 2, y_loc, x_loc + 2, y_loc)
                self.canvas.create_line(coord, width=2, fill="#808080")

    def render(self):
        self.canvas.create_rectangle((0, 0, self.width, self.height), fill="#ffffff")
        to_render = self.normal if self.mapped is None else self.mapped
        if self.horizontal:
            self.render_horizontal(to_render)
        else:
            self.render_vertical(to_render)


class Canvas:
    def __init__(self, ref, map_func):
        self.ref = ref
        self.width = self.ref.winfo_width() - 2
        self.height = self.ref.winfo_height() - 2
        self.map = map_func
        self.handles = list(map(self.point2handle, self.map.get_points()))
        self.dragging = False

        self.draw_grid()
        self.draw_curve()
        self.draw_handles()

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
            self.ref.create_line(coord, fill="#800080", width=3)

    def draw_handles(self):
        for handle in self.handles:
            handle.render()

    def is_on_curve(self):
        pass

    def is_on_handle(self):
        pass

    def on_mouse_down(self):
        pass

    def on_mouse_move(self):
        pass

    def on_mouse_up(self):
        pass

    def on_mouse_right(self):
        pass

    def update(self, ruler):
        pass
