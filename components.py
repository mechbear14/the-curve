from modules.curve_editor import CurveEditor
from modules.image_container import ImageObject, ImageContainer
import tkinter as tk
from tkinter import filedialog
from PIL import Image


class ImageComponent:
    def __init__(self, parent):
        self.image_canvas = tk.Canvas(parent, width=400, height=400, background="#008080")
        self.image_canvas.pack()
        self.top_level = None

    def bind(self, top_level):
        self.top_level = top_level
        self.top_level.image_container = ImageContainer(self.image_canvas)


class FileOpsComponent:
    def __init__(self, parent):
        open_btn = tk.Button(parent, text="Open...", command=self.open_image)
        open_btn.pack(side=tk.LEFT)
        save_btn = tk.Button(parent, text="Save", command=self.save_image)
        save_btn.pack(side=tk.LEFT)
        reset_btn = tk.Button(parent, text="Reset", command=self.reset_image)
        reset_btn.pack(side=tk.LEFT)
        self.top_level = None

    def bind(self, top_level):
        self.top_level = top_level

    def open_image(self):
        image_path = filedialog.askopenfilename()
        if image_path is not None and len(image_path) > 0:
            try:
                image = Image.open(image_path)
                self.top_level.image = ImageObject(image)
                self.top_level.image_container.set_image(self.top_level.image)
                self.top_level.channel_select.set_to("RGB")
            except OSError:
                print("Not an image file")
        else:
            return

    def save_image(self):
        image_path = filedialog.asksaveasfilename()
        if image_path is not None and len(image_path) > 0:
            self.top_level.image.save(image_path)
        else:
            return

    def reset_image(self):
        if self.top_level.image is not None:
            self.top_level.image_container.reset()
            self.top_level.channel_select.set_to("RGB")


class ChannelSelectComponent:
    def __init__(self, parent):
        label = tk.Label(parent, text="Channel: ")
        label.pack(side=tk.LEFT)
        self.channel = tk.StringVar(parent)
        self.channel.set("RGB")
        channel_list = tk.OptionMenu(parent, self.channel, "RGB", "R", "G", "B", command=self.update)
        channel_list.pack(side=tk.LEFT)
        self.top_level = None

    def bind(self, top_level):
        self.top_level = top_level

    def set_to(self, option):
        self.channel.set(option)
        self.update(option)

    def update(self, value):
        map_func = self.top_level.image_container.select_channel(value)
        print(map_func)
        update_func = self.top_level.image_container.render
        self.top_level.curve.bind(map_func, update_func)


class CurveEditorComponent:
    def __init__(self, parent):
        self.ruler_v = tk.Canvas(parent, width=50, height=350, background="#00c800")
        self.ruler_h = tk.Canvas(parent, width=350, height=50, background="#0000c8")
        self.canvas = tk.Canvas(parent, width=350, height=350, background="#c8c800")
        self.ruler_v.grid(row=0, column=0)
        self.canvas.grid(row=0, column=1)
        self.ruler_h.grid(row=1, column=1)
        self.top_level = None

    def bind(self, top_level):
        self.top_level = top_level
        self.top_level.curve = CurveEditor(self.canvas, self.ruler_h, self.ruler_v)
