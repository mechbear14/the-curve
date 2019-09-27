from modules.core import Point, MapFn, Canvas, Ruler
from services import ImageBox
import tkinter as tk
from tkinter import filedialog


image_box = ImageBox()


def open_image():
    image_box.open_image(filedialog.askopenfilename())


root = tk.Tk()

name = None

left_pane = tk.Frame(root, width=400, height=500)
left_pane.pack(side=tk.LEFT)

channel_box = tk.Frame(left_pane, width=400, height=100)
channel_box.pack()
label = tk.Label(channel_box, text="Channel: ")
label.pack(side=tk.LEFT)
variable = tk.StringVar(channel_box)
variable.set("RGB")
channel_list = tk.OptionMenu(channel_box, variable, "RGB", "R", "G", "B")
channel_list.pack(side=tk.LEFT)

canvas_pane = tk.Frame(left_pane, width=400, height=400)
canvas_pane.pack()
ruler_v = tk.Canvas(canvas_pane, width=50, height=350, background="#00c800")
ruler_h = tk.Canvas(canvas_pane, width=350, height=50, background="#0000c8")
canvas = tk.Canvas(canvas_pane, width=350, height=350, background="#c8c8c8")
ruler_v.grid(row=0, column=0)
canvas.grid(row=0, column=1)
ruler_h.grid(row=1, column=1)

right_pane = tk.Frame(root, width=400, height=500)
right_pane.pack(side=tk.LEFT)
tool_pane = tk.Frame(right_pane, width=400, height=100)
tool_pane.pack()
open_btn = tk.Button(tool_pane, text="Open...", command=open_image)
open_btn.pack(side=tk.LEFT)
save_btn = tk.Button(tool_pane, text="Save")
save_btn.pack(side=tk.LEFT)
reset_btn = tk.Button(tool_pane, text="Reset")
reset_btn.pack(side=tk.LEFT)
image_pane = tk.Frame(right_pane, width=400, height=400)
image_pane.pack()
image_canvas = tk.Canvas(image_pane, width=400, height=400, background="#008080")
image_canvas.pack()
image_box.set_canvas(image_canvas)


root.update()
map_func = MapFn([Point(0, 0), Point(1, 1)])
controller = Canvas(canvas, map_func)
ruler = Ruler(ruler_h, ruler_v)
controller.attach(ruler)

root.title("The Curve")
root.resizable(0, 0)
root.mainloop()
