from core import MapFn
from PIL import Image, ImageTk


class ImageContainer:
    def __init__(self, image: Image):
        self.curves = [MapFn(), MapFn(), MapFn(), MapFn()]
        self.image = image
        self.original_r = None
        self.original_g = None
        self.original_b = None
        self.ref = None

    def export(self):
        pass

    def render(self, canvas):
        pass

    def update(self):
        pass
