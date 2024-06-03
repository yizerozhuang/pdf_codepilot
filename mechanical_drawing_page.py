import tkinter as tk

from utility import *


class MechanicalDrawingPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.main_frame)
        self.app = app
        self.procedure_part()

        self.first_step()

    def procedure_part(self):

        self.procedure_frame = tk.LabelFrame(self)
        self.procedure_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.procedure_frames = {}
        self.procedure_buttons = {}

        show_procedure_function = lambda procedure: lambda: self.show_procedure(procedure)
        for i, procedure in enumerate(conf["drawing_procedures"]):
            self.procedure_frames[procedure] = tk.LabelFrame(self)
            self.procedure_buttons[procedure] = tk.Button(self.procedure_frame, width=13,
                                                          command=show_procedure_function(procedure), text=procedure,
                                                          font=conf["font"], bg="brown", fg="white")
            self.procedure_buttons[procedure].grid(row=i, column=0, sticky="W")

        self.current_procedure = conf["drawing_procedures"][0]
        self.show_procedure(self.current_procedure)

    def show_procedure(self, procedure):
        self.procedure_buttons[self.current_procedure].config(bg="brown", fg="white")
        self.procedure_frames[self.current_procedure].pack_forget()

        self.current_procedure = procedure

        self.procedure_buttons[self.current_procedure].config(bg="white", fg="black")
        self.procedure_frames[self.current_procedure].pack(fill=tk.BOTH, expand=1)

    def first_step(self):
        procedure = conf["drawing_procedures"][0]
        frame = self.procedure_frames[procedure]

        self.app.data["template_type"] = tk.StringVar(value="Restaurant")

        template_type_frame = tk.Frame(frame)
        template_type_frame.pack()
        tk.Radiobutton(template_type_frame, text="Restaurant", value="Restaurant", variable=self.app.data["template_type"], font=conf["font"]).grid(row=0, column=0)
        tk.Radiobutton(template_type_frame, text="Others", value="Others", variable=self.app.data["template_type"], font=conf["font"]).grid(row=0, column=1)

        tk.Button(frame, text="Copy Template", font=conf["font"], bg="brown", fg="white").pack()




