import tkinter as tk
from mechanical_sketch_page import MechanicalSketchPage
from config import CONFIGURATION as conf
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        # TkinterDnD.Tk.__init__(self, *args, **kwargs)
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("PDF Codepilot")
        self.state("zoomed")

        self.page_frame = tk.LabelFrame(self)
        self.page_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Button(self.page_frame, text="Mechanical Sketch", bg="brown", fg="white", font=conf["font"]).pack(side=tk.LEFT)


        self.main_frame = tk.LabelFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.mechanical_sketch_page = MechanicalSketchPage(self)
        self.mechanical_sketch_page.pack(fill=tk.BOTH, expand=1)





    # def mechanical_sketch_frame(self):
