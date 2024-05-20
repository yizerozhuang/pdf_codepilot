import tkinter as tk
from tkinter import ttk, filedialog

from config import CONFIGURATION as conf
from util import extract_disk_and_project_name, flatten_and_resize_pdf, grays_scale_pdf, compress, align, open_pdf_in_bluebeam

from datetime import date

class MechanicalSketchPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.main_frame)

        self.current_project = tk.StringVar()
        self.current_project_frame = tk.LabelFrame(self)
        self.current_project_frame.pack(fill=tk.X, side=tk.TOP)
        self.current_project_entry = tk.Entry(self.current_project_frame, width=100, state=tk.DISABLED, textvariable=self.current_project, font=conf["font"])
        self.current_project_entry.pack(side=tk.LEFT)

        self.procedure_part()

        self.first_step()
        self.second_step()
        self.third_step()
        self.forth_step()
        self.fifth_step()
        self.sixth_step()
        self.seventh_step()

    def procedure_part(self):

        self.procedure_frame = tk.LabelFrame(self)
        self.procedure_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.procedure_frames = {}
        self.procedure_buttons= {}

        show_procedure_function = lambda procedure: lambda: self.show_procedure(procedure)
        for i, procedure in enumerate(conf["sketch_procedures"]):
            self.procedure_frames[procedure] = tk.LabelFrame(self)
            self.procedure_buttons[procedure] = tk.Button(self.procedure_frame, width=10, command=show_procedure_function(procedure), text=procedure, font=conf["font"], bg="brown", fg="white")
            self.procedure_buttons[procedure].grid(row=i, column=0, sticky="W")


        self.current_procedure = conf["sketch_procedures"][0]
        self.show_procedure(self.current_procedure)



    def show_procedure(self, procedure):
        self.procedure_buttons[self.current_procedure].config(bg="brown", fg="white")
        self.procedure_frames[self.current_procedure].pack_forget()

        self.current_procedure = procedure

        self.procedure_buttons[self.current_procedure].config(bg="white", fg="black")
        self.procedure_frames[self.current_procedure].pack(fill=tk.BOTH, expand=1)

    def first_step(self):
        procedure = conf["sketch_procedures"][0]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                Procedure:
                1.Review All arch drawing and figured out what drawings will be needed for the sketch.
                2.If arch drawings already combined, delete the drawings does not need to proceed
                """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)
        # tk.Button(frame, text="Upload File", bg="brown", fg="white", font=conf["font"]).grid(row=1, column=0, sticky="W")

    def second_step(self):
        procedure = conf["sketch_procedures"][1]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                Procedure:
                check arch drawings if the scale as indicated and input the right scale and paper size
                """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)

    def third_step(self):
        procedure = conf["sketch_procedures"][2]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                        Procedure:
                        Dialoge box to put all drawings in, then combined, flattern and rename properly
                        provide paper size and scale to mechanical sketch, usually, scale is 1:50 or 1:100 and redo until perfect
                        Note:  Ensure you use the latest architectural drawings provided by the client for this sample
                        """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)

        upload_frame = tk.LabelFrame(frame)
        upload_frame.grid(row=1, column=0)

        tk.Label(upload_frame, text="Convert From", font=conf["content_font"]).grid(row=0, column=0, columnspan=4, sticky="W")

        self.input_scale = tk.StringVar()
        self.input_size = tk.StringVar()
        tk.Label(upload_frame, text="1:", font=conf["content_font"]).grid(row=1, column=0)
        tk.Entry(upload_frame, textvariable=self.input_scale, font=conf["content_font"], fg="blue", width=4).grid(row=1, column=1)
        tk.Label(upload_frame, text="@", font=conf["content_font"]).grid(row=1, column=2)
        ttk.Combobox(upload_frame, textvariable=self.input_size, values=conf["input_sizes"],state="readonly", font=conf["content_font"], width=3).grid(row=1, column=3)

        tk.Label(upload_frame, text="To", font=conf["content_font"]).grid(row=2, column=0, columnspan=4, sticky="W")

        self.output_scale = tk.StringVar()
        self.output_size = tk.StringVar()
        tk.Label(upload_frame, text="1:", font=conf["content_font"]).grid(row=3, column=0)
        ttk.Combobox(upload_frame, textvariable=self.output_scale, values=conf["output_scales"], state="readonly", font=conf["content_font"], width=3).grid(row=3, column=1)
        tk.Label(upload_frame, text="@", font=conf["content_font"]).grid(row=3, column=2)
        ttk.Combobox(upload_frame, textvariable=self.output_size, values=conf["output_sizes"], state="readonly", font=conf["content_font"], width=3).grid(row=3, column=3)

        tk.Button(upload_frame, text="Import File(s)", bg="brown", fg="white", font=conf["content_font"], command=self.import_file).grid(row=4, column=0, columnspan=4, sticky="W")


    def import_file(self):
        files = filedialog.askopenfilenames()
        if len(files)==0:
            return
        elif len(files) == 1:
            input_file = files[0]
            disk, project_name, file_name = extract_disk_and_project_name(input_file)
            current_project = "\\".join([disk, project_name])
            self.current_project.set("\\".join([disk, project_name]))
            self.sketch_dir = f"{current_project}\\{project_name}-Mechanical Sketch.pdf"

            flatten_and_resize_pdf(input_file, self.input_scale.get(), self.input_size.get(), self.output_scale.get(), self.output_size.get(), self.sketch_dir)
        else:
            # assuming all the file are import from the same
            disk, project_name, file_name = extract_disk_and_project_name(files[0])
            current_project = "\\".join([disk, project_name])
            self.current_project.set("\\".join([disk, project_name]))


            self.sketch_dir = f"{current_project}\\{project_name}-Mechanical Sketch.pdf"

        open_pdf_in_bluebeam(self.sketch_dir)

    def forth_step(self):
        procedure = conf["sketch_procedures"][3]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                        Procedure:
                        Choose a basepoint and apply to all pages
                        Align the basepoint manually for each page
                        Click The Align
                        """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)
        upload_frame = tk.LabelFrame(frame)
        upload_frame.grid(row=1, column=0)

        tk.Button(upload_frame, text="Align", bg="brown", fg="white", font=conf["content_font"], command=self.align).grid(row=0, column=0)

    def align(self):
        self.sketch_dir = r"P:\bluebeam_codepilot_test_folder\bluebeam_codepilot_test_folder-Mechanical Sketch.pdf"
        align(self.sketch_dir)
        open_pdf_in_bluebeam(self.sketch_dir)

    def fifth_step(self):
        procedure = conf["sketch_procedures"][4]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                        Procedure:
                        erase content which is not needed, as per 10.11
                        or erase content by remove colour
                        or grayscale
                        """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)

        button_frame = tk.LabelFrame(frame)
        button_frame.grid(row=1, column=0)

        tk.Button(button_frame, text="Remove Color", bg="brown", fg="white", font=conf["content_font"]).grid(row=0, column=0)
        tk.Button(button_frame, text="Grayscale", bg="brown", fg="white", font=conf["content_font"], command=self.grays_scale).grid(row=0, column=1)

    def grays_scale(self):
        grays_scale_pdf(self.sketch_dir)

    def sixth_step(self):
        procedure = conf["sketch_procedures"][5]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                        Procedure:
                        luminocity to 45%
                        """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)

        button_frame = tk.LabelFrame(frame)
        button_frame.grid(row=1, column=0)

        tk.Button(button_frame, text="Luminocity to 45%", bg="brown", fg="white", font=conf["content_font"]).grid(row=0, column=0)

    def seventh_step(self):
        procedure = conf["sketch_procedures"][6]
        frame = self.procedure_frames[procedure]
        procedure_text = """
                        Procedure:
                        Check the file size. If it is too large, use the "Reduce File Size" function to decrease it to less than 20 MB.
                        """
        tk.Label(frame, text=procedure_text, font=conf["content_font"]).grid(row=0, column=0)

        button_frame = tk.LabelFrame(frame)
        button_frame.grid(row=1, column=0)

        tk.Button(button_frame, text="Compress", bg="brown", fg="white", font=conf["content_font"], command=self.compress).grid(row=0, column=0)
    def compress(self):
        compress(self.sketch_dir)