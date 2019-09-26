from calculation import Point, MapFn
from PIL import Image, ImageTk
import numpy as np


class ImageBox:
    def __init__(self):
        self.image = None
        self.scaled_image = None
        self.scaled_image_ref = None
        self.canvas = None
        self.maps = [MapFn([Point(0, 0), Point(1, 1)])] * 4
        self.originals = [None, None, None]

    def open_image(self, file):
        image = Image.open(file).convert("RGB")
        r, g, b = image.split()
        rr = np.asarray(r) * 0.8
        gg = np.asarray(g) * 0.2
        bb = np.asarray(b) * 0.2
        rm = Image.fromarray(rr).convert(mode="L")
        gm = Image.fromarray(gg).convert(mode="L")
        bm = Image.fromarray(bb).convert(mode="L")
        final = Image.merge("RGB", (rm, gm, bm))
        self.image = final
        self.scaled_image = final.resize((400, round(400 / 1920 * 1080)))
        self.scaled_image_ref = ImageTk.PhotoImage(self.scaled_image)
        self.canvas.create_rectangle((0, 0, 400, 400), fill="")
        self.canvas.create_image((200, 200), image=self.scaled_image_ref)

    def set_canvas(self, canvas):
        self.canvas = canvas

    def reset(self):
        self.maps = [MapFn([Point(0, 0), Point(1, 1)])] * 4
        self.update()

    def select_channel(self, channel):
        if channel == "RGB":
            return self.maps[3]
        elif channel == "R":
            return self.maps[0]
        elif channel == "G":
            return self.maps[1]
        elif channel == "B":
            return self.maps[2]
        return None

    def update(self):
        pass

    def render(self):
        pass
