from components import Canvas, Ruler
from calculation import Point, MapFn
import tkinter as tk

root = tk.Tk()
canvas_pane = tk.Frame(root, width=400, height=400)
canvas_pane.pack()
ruler_v = tk.Canvas(canvas_pane, width=50, height=350, background="#00c800")
ruler_h = tk.Canvas(canvas_pane, width=350, height=50, background="#0000c8")
canvas = tk.Canvas(canvas_pane, width=350, height=350, background="#c8c8c8")
ruler_v.grid(row=0, column=0)
canvas.grid(row=0, column=1)
ruler_h.grid(row=1, column=1)

root.update()
map_func = MapFn([Point(0, 0), Point(1, 1)])
controller = Canvas(canvas, map_func)
ruler = Ruler(ruler_h, ruler_v)
controller.attach(ruler)
root.title("The Curve")
root.resizable(0, 0)
root.mainloop()
