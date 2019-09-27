from .core import MapFn
from .utilities import fit2canvas
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk


class ImageObject:
    def __init__(self, image: Image):
        self.format = image.format
        self.curves = [MapFn(), MapFn(), MapFn(), MapFn()]
        self.image = image.convert("RGB")
        self.mapped_image = self.image
        self.selected = 3
        self.originals = [np.asarray(c) for c in image.split()]

    def update(self, to_update):
        mapped = []
        # if self.selected == 3:
        #     for o in to_update:
        #         norm = o / 255
        #         mapped.append(self.curves[3].map_v(norm) * 255)
        # else:
        #     for i, o in enumerate(to_update):
        #         if i != self.selected:
        #             mapped.append(o)
        #         else:
        #             norm = o / 255
        #             mapped.append(self.curves[3].map_v(self.curves[self.selected].map_v(norm)) * 255)
        for i, channel in enumerate(to_update):
            norm = channel / 255
            mapped.append(self.curves[3].map_v(self.curves[i].map_v(norm)) * 255)
        to_merge = [Image.fromarray(m.astype("uint8")).convert("L") for m in mapped]
        return Image.merge("RGB", tuple(to_merge))

    def select_channel(self, channel):
        if channel == "R":
            self.selected = 0
        elif channel == "G":
            self.selected = 1
        elif channel == "B":
            self.selected = 2
        elif channel == "RGB":
            self.selected = 3
        return self.curves[self.selected]

    def get_original(self):
        return self.image

    def get_mapped(self):
        return self.mapped_image

    def save(self, file_name):
        self.mapped_image = self.update(self.originals)
        self.mapped_image.save(file_name, self.format)

    def reset(self):
        self.curves = [MapFn(), MapFn(), MapFn(), MapFn()]
        self.mapped_image = self.image


class ImageContainer:
    def __init__(self, canvas):
        self.image_object = None
        self.canvas = canvas
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()
        self.thumbnail_channels = None
        self.image_ref = None
        self.ref = None

    def set_image(self, image):
        self.canvas.delete(tk.ALL)
        self.image_object = image
        self.get_resized()
        self.ref = self.canvas.create_image((self.width / 2, self.height / 2), image=self.image_ref)

    def select_channel(self, channel):
        return self.image_object.select_channel(channel)

    def get_resized(self):
        image = self.image_object.get_mapped()
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        im_width, im_height = image.size
        resized = image.resize(fit2canvas(im_width, im_height, width, height))
        self.thumbnail_channels = [np.asarray(c) for c in resized.split()]
        self.image_ref = ImageTk.PhotoImage(resized)

    def render(self):
        mapped = self.image_object.update(self.thumbnail_channels)
        self.image_ref = ImageTk.PhotoImage(mapped)
        self.canvas.itemconfig(self.ref, image=self.image_ref)

    def reset(self):
        self.image_object.reset()
        self.get_resized()
        self.canvas.itemconfig(self.ref, image=self.image_ref)
