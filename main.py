import tkinter as tk
from components import *


class App:
    def __init__(self, master):
        self.image = None
        self.image_container = None
        self.curve = None

        channel_select_box = tk.Frame(master, width=400, height=100)
        channel_select_box.grid(row=0, column=0)
        curve_editor_box = tk.Frame(master, width=400, height=400)
        curve_editor_box.grid(row=1, column=0)
        file_ops_box = tk.Frame(master, width=400, height=100)
        file_ops_box.grid(row=0, column=1)
        image_canvas_box = tk.Frame(master, width=400, height=400)
        image_canvas_box.grid(row=1, column=1)

        self.channel_select = ChannelSelectComponent(channel_select_box)
        self.curve_editor = CurveEditorComponent(curve_editor_box)
        self.file_ops = FileOpsComponent(file_ops_box)
        self.image_canvas = ImageComponent(image_canvas_box)

        master.update()

        self.channel_select.bind(self)
        self.curve_editor.bind(self)
        self.file_ops.bind(self)
        self.image_canvas.bind(self)


root = tk.Tk()
app = App(root)
root.title("The Curve")
root.resizable(0, 0)
root.mainloop()
