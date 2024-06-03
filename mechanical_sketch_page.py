import shutil
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import *
from tkinter import messagebox


from config import CONFIGURATION as conf
from utility import *
from dnd_listbox import DndListbox



from datetime import date, datetime
from pathlib import Path
import json
import _thread




class MechanicalSketchPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.main_frame)
        self.app = app

        # self.project_dir = tk.StringVar()
        # self.project_frame = tk.LabelFrame(self)
        # self.project_frame.pack(fill=tk.X, side=tk.TOP)
        # self.project_entry = tk.Entry(self.project_frame, width=100, state=tk.DISABLED, textvariable=self.project_dir, font=conf["font"])
        # self.project_entry.pack(side=tk.LEFT)

        self.sketch_dir = self.app.sketch_dir

        self.current_project_part()
        self.sketch_dir.trace("w", self.update_current_project_entry)


        self.procedure_part()

        self.first_step()
        self.second_step()
        self.third_step()
        # self.forth_step()
        # self.fifth_step()
        # self.sixth_step()
        # self.seventh_step()

    def update_current_project_entry(self, *args):
        if os.path.exists(self.sketch_dir.get()):
            self.current_project_entry.config(text=self.sketch_dir.get())

    def current_project_part(self):
        self.current_project_frame = tk.LabelFrame(self)
        self.current_project_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Label(self.current_project_frame, text="Current Working Sketch", font=conf["font"]).grid(row=0, column=0)
        self.current_project_entry = tk.Label(self.current_project_frame, font=conf["font"], width=100, text="")
        self.current_project_entry.grid(row=0, column=1)

    def procedure_part(self):

        self.procedure_frame = tk.LabelFrame(self)
        self.procedure_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.procedure_frames = {}
        self.procedure_buttons= {}

        show_procedure_function = lambda procedure: lambda: self.show_procedure(procedure)
        for i, procedure in enumerate(conf["sketch_procedures"]):
            self.procedure_frames[procedure] = tk.LabelFrame(self)
            self.procedure_buttons[procedure] = tk.Button(self.procedure_frame, width=13, command=show_procedure_function(procedure), text=procedure, font=conf["font"], bg="brown", fg="white")
            self.procedure_buttons[procedure].grid(row=i, column=0, sticky="W")


        self.current_procedure = conf["sketch_procedures"][0]
        self.show_procedure(self.current_procedure)



    def show_procedure(self, procedure):
        self.procedure_buttons[self.current_procedure].config(bg="brown", fg="white")
        self.procedure_frames[self.current_procedure].pack_forget()

        self.current_procedure = procedure

        self.procedure_buttons[self.current_procedure].config(bg="white", fg="black")
        self.procedure_frames[self.current_procedure].pack(fill=tk.BOTH, expand=1)

    # def drop(self, event):
    #     # This function is called, when stuff is dropped into a widget
    #     stringvar.set(self, event.data)
    #
    # def drag_command(self, event):
    #     # This function is called at the start of the drag,
    #     # it returns the drag type, the content type, and the actual content
    #     return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")

    # def drop_inside_list_box(self, event):
    #     self.data["Log Files"]["External Files"].set(event.data.split("{")[-1].split("}")[0])

    def first_step(self):
        procedure = conf["sketch_procedures"][0]
        frame = self.procedure_frames[procedure]

        procedure_texts = [
                "Procedures:",
                "1.1.Open the external folder within the project directory to access the architectural drawings.",
                "1.2.Review all latest architectural drawings and figured out what drawings will be needed for the sketch",
                "(pdf. file including proposed floor plan pages and some other necessary information pages).",
                "1.3.Make sure all the sketch pages(proposed floor plan pages) have the same scale and paper size.",
                "1.4.If arch drawings are already combined, import the combined file.",
                "If arch drawings are separated, import the files based on floor level order.",
            ]
        self.app.app_pack(frame, procedure_texts)

        self.sketch_combine_files_list = []

        dnd_listbox_frame = tk.Frame(frame)
        self.drop_file_listbox = DndListbox(
            dnd_listbox_frame,
            selectmode='single',
            width=100,
            font=conf["font"],
            file_list=self.sketch_combine_files_list,
            app=self.app
        )
        self.drop_file_listbox.grid(row=0, column=0)
        button_frame = tk.Frame(dnd_listbox_frame)
        button_frame.grid(row=0, column=1, sticky="n")
        tk.Button(button_frame, text="Up", width=10, bg="brown", fg="white", font=conf["font"], command=self.drop_file_listbox.move_up_item).pack()
        tk.Button(button_frame, text="Down", width=10, bg="brown", fg="white", font=conf["font"], command=self.drop_file_listbox.move_down_item).pack()
        tk.Button(button_frame, text="Delete", width=10, bg="brown", fg="white", font=conf["font"], command=self.drop_file_listbox.delete_item).pack()
        tk.Button(button_frame, text="Open", width=10, bg="brown", fg="white", font=conf["font"], command=self.drop_file_listbox.open_item).pack()
        tk.Button(button_frame, text="Delete All", width=10, bg="brown", fg="white", font=conf["font"], command=self.drop_file_listbox.delete_all).pack()

        dnd_listbox_frame.pack(anchor=tk.W)

        # self.drop_file_listbox.bind("<<Drop>>", lambda e: self.drop_file_listbox.insert(0, e.data))


        self.app.app_pack(frame, "1.5.Input original scale and paper size into the table.")
        # self.drop_file_listbox.drop_target_register(DND_FILES)
        # self.drop_file_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)

        # tk.Label(upload_frame, text="1:", font=conf["font"]).grid(row=1, column=0)
        # tk.Entry(upload_frame, textvariable=self.app.data["input_scale"], font=conf["font"], fg="blue", width=4).grid(row=1, column=1)
        # tk.Label(upload_frame, text="@", font=conf["font"]).grid(row=1, column=2)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["input_size"], values=conf["input_sizes"],state="readonly", font=conf["font"], width=3).grid(row=1, column=3)
        # tk.Label(upload_frame, text="To", font=conf["font"]).grid(row=2, column=0, columnspan=4, sticky="W")
        #
        # self.app.data["output_scale"] = tk.StringVar()
        # self.app.data["output_size"] = tk.StringVar()
        # tk.Label(upload_frame, text="1:", font=conf["font"]).grid(row=3, column=0)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["output_scale"], values=conf["output_scales"], state="readonly", font=conf["font"], width=3).grid(row=3, column=1)
        # tk.Label(upload_frame, text="@", font=conf["font"]).grid(row=3, column=2)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["output_size"], values=conf["output_sizes"], state="readonly", font=conf["font"], width=3).grid(row=3, column=3)
        #
        # tk.Button(upload_frame, text="Import File(s)", bg="brown", fg="white", font=conf["font"], command=self.import_file).grid(row=4, column=0, columnspan=4, sticky="W")
        input_frame = tk.Frame(frame)
        input_frame.pack(anchor=tk.W)
        
        self.app.data["input_scale"] = tk.StringVar(value="50")
        self.app.data["input_size"] = tk.StringVar(value="A3")
        self.app.data["input_custom_scale"] = tk.StringVar()
        self.app.data["input_custom_size_x"] = tk.StringVar()
        self.app.data["input_custom_size_y"] = tk.StringVar()

        tk.Radiobutton(input_frame, text="1:50", variable=self.app.data["input_scale"], value="50", font=conf["font"]).grid(row=0, column=0)
        tk.Radiobutton(input_frame, text="1:100", variable=self.app.data["input_scale"], value="100", font=conf["font"]).grid(row=1, column=0)
        tk.Radiobutton(input_frame, text="1:150", variable=self.app.data["input_scale"], value="150", font=conf["font"]).grid(row=2, column=0)
        tk.Radiobutton(input_frame, text="1:200", variable=self.app.data["input_scale"], value="200", font=conf["font"]).grid(row=3,
                                                                                                                  column=0)

        custom_frame = tk.Frame(input_frame)
        custom_frame.grid(row=4, column=0)
        tk.Radiobutton(custom_frame, variable=self.app.data["input_scale"], value="custom").grid(row=0, column=0)
        tk.Label(custom_frame, text="1:", font=conf["font"]).grid(row=0, column=1)
        tk.Entry(custom_frame, textvariable=self.app.data["input_custom_scale"], font=conf["font"], fg="blue", width=3).grid(row=0, column=2)

        tk.Radiobutton(input_frame, text="A3", variable=self.app.data["input_size"], value="A3", font=conf["font"]).grid(row=0, column=1)
        tk.Radiobutton(input_frame, text="A2", variable=self.app.data["input_size"], value="A2", font=conf["font"]).grid(row=1, column=1)
        tk.Radiobutton(input_frame, text="A1", variable=self.app.data["input_size"], value="A1", font=conf["font"]).grid(row=2, column=1)
        tk.Radiobutton(input_frame, text="A0", variable=self.app.data["input_size"], value="A0", font=conf["font"]).grid(row=3, column=1)
        tk.Label(input_frame, text="(mm)", font=conf["font"]).grid(row=4, column=2)


        custom_frame = tk.Frame(input_frame)
        custom_frame.grid(row=4, column=1)
        tk.Radiobutton(custom_frame, variable=self.app.data["input_size"], value="custom").grid(row=0, column=0)
        tk.Entry(custom_frame, textvariable=self.app.data["input_custom_size_x"], font=conf["font"], fg="blue", width=3).grid(row=0, column=1)
        tk.Label(custom_frame, text=":", font=conf["font"]).grid(row=0, column=2)
        tk.Entry(custom_frame, textvariable=self.app.data["input_custom_size_y"], font=conf["font"], fg="blue", width=3).grid(row=0, column=3)
        self.app.app_pack(frame, "1.6.Input expected scale and paper size into the table.")

        output_frame = tk.Frame(frame)
        output_frame.pack(anchor=tk.W)
        
        self.app.data["output_scale"] = tk.StringVar(value="50")
        self.app.data["output_size"] = tk.StringVar(value="A3")
        self.app.data["output_custom_scale"] = tk.StringVar()
        self.app.data["output_custom_size_x"] = tk.StringVar()
        self.app.data["output_custom_size_y"] = tk.StringVar()

        tk.Radiobutton(output_frame, text="1:50", variable=self.app.data["output_scale"], value="50", font=conf["font"]).grid(row=0, column=0)
        tk.Radiobutton(output_frame, text="1:100", variable=self.app.data["output_scale"], value="100", font=conf["font"]).grid(row=1, column=0)

        custom_frame = tk.Frame(output_frame)
        custom_frame.grid(row=2, column=0)
        tk.Radiobutton(custom_frame, variable=self.app.data["output_scale"], value="custom").grid(row=0, column=0)
        tk.Label(custom_frame, text="1:", font=conf["font"]).grid(row=0, column=1)
        tk.Entry(custom_frame, textvariable=self.app.data["output_custom_scale"], font=conf["font"], fg="blue", width=3).grid(row=0, column=2)

        tk.Radiobutton(output_frame, text="A3", variable=self.app.data["output_size"], value="A3", font=conf["font"]).grid(row=0, column=1)
        # tk.Radiobutton(output_frame, text="A2", variable=self.app.data["output_size"], value="A2", font=conf["font"]).grid(row=1, column=1)
        tk.Radiobutton(output_frame, text="A1", variable=self.app.data["output_size"], value="A1", font=conf["font"]).grid(row=1, column=1)
        tk.Radiobutton(output_frame, text="A0", variable=self.app.data["output_size"], value="A0", font=conf["font"]).grid(row=2, column=1)
        tk.Label(output_frame, text="(mm)", font=conf["font"]).grid(row=4, column=2)

        custom_frame = tk.Frame(output_frame)
        custom_frame.grid(row=4, column=1)
        tk.Radiobutton(custom_frame, variable=self.app.data["output_size"], value="custom").grid(row=0, column=0)
        tk.Entry(custom_frame, textvariable=self.app.data["output_custom_size_x"], font=conf["font"], fg="blue", width=3).grid(row=0, column=1)
        tk.Label(custom_frame, text=":", font=conf["font"]).grid(row=0, column=2)
        tk.Entry(custom_frame, textvariable=self.app.data["output_custom_size_y"], font=conf["font"], fg="blue", width=3).grid(row=0, column=3)

        # self.app.app_pack(frame, "7.Select the output type of the drawing.")
        #
        # type_frame = tk.Frame(frame)
        # type_frame.pack()
        #
        # self.output_type = tk.StringVar(value="Sketch")
        # self.sketch_name = tk.StringVar(value="-Mech Sketch.pdf")
        # self.combine_skectch_name = tk.StringVar()
        #
        # tk.Radiobutton(type_frame, variable=self.output_type, value="Sketch").grid(row=0, column=0)
        # sketch_name_frame = tk.Frame(type_frame)
        # sketch_name_frame.grid(row=0, column=1)
        #
        #
        # tk.Label(sketch_name_frame, textvariable=self.sketch_name, font=conf["font"]).pack()
        # self.project_dir.trace("w", self.config_sketch_name)
        #
        # tk.Radiobutton(type_frame, variable=self.output_type, value="Combine").grid(row=0, column=2)
        # combine_frame = tk.Frame(type_frame)
        # combine_frame.grid(row=0, column=3)
        #
        # tk.Label(combine_frame, text=f"{date.today().strftime('%Y%m%d')}-Combined ", font=conf["font"]).grid(row=0, column=0)
        # tk.Entry(combine_frame, textvariable=self.combine_skectch_name, fg="blue", width=10, font=conf["font"]).grid(row=0, column=1)
        # tk.Label(combine_frame, text=".pdf", width=5, font=conf["font"]).grid(row=0, column=2)

        self.app.app_pack(frame, ["1.7.Save and close the architectural drawings.", "1.8.Click ‘Process’, Sketch file will be automatically opened"])

        tk.Button(frame, text="Process", bg="brown", fg="white", font=conf["font"], command=self.page_one_process).pack(anchor=tk.W)





    # def config_sketch_name(self, *args):
    #     project_dir = self.project_dir.get()
    #     sketch_name = get_sketch_name(project_dir)
    #     self.sketch_name.set(sketch_name)
        
    def second_step(self):
        procedure = conf["sketch_procedures"][1]
        frame = self.procedure_frames[procedure]
        procedure_texts = [
            "Procedures:",
            "2.1. Check the drawing and delete any unnecessary pages.",
            "2.2. Choose a basepoint symbol (1 site/lot boundary; 2 grid lines; 3 lift shaft; 4 external wall, etc.).",
            "2.3. Move to a suitable basepoint location at the first page.",
            "2.4. Right click the symbol, Click ‘Apply to all pages’. ",
            "2.5. Manually move the remaining symbols to the basepoint location of each floor.",
            "2.6. Save and close",
            "2.7. Click 'Align', Sketch will be automatically opened."
        ]
        self.app.app_pack(frame, procedure_texts)
        tk.Button(frame, text="Align", bg="brown", fg="white", font=conf["font"], command=self.align).pack(anchor=tk.W)

    def align(self):
        try:
            align(self.sketch_dir.get())
            self.open_sketch()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please save and close the Drawing before align")
            return
        self.show_procedure(conf["sketch_procedures"][2])


    def third_step(self):
        procedure = conf["sketch_procedures"][2]
        frame = self.procedure_frames[procedure]
        procedure_texts = [
            "Procedures:",
            "3.1. Check if the drawing is aligned.",
            "3.2. Delete irrelevant content on the architectural drawing by using the 'Erase Content' command. ",
            "Relevant contents include grid lines, furniture, walls, doors, columns, and room names.",
            "Irrelevant content includes dimensions and equipment numbers.",
            "3.3. If the drawing contains irrelevant details in a specific colour, ",
            "you can process and remove the colour using the 'Modify Colours' function ",
            "3.4. In the ‘Document’ - ‘Process’ – ‘Colour Processing’  tab. ",
            "3.5. In 'Modify Colours,' select the source colour you want to remove and set it to 'No colour.' , the details will be immediately removed from the drawing.",
        ]
        self.app.app_pack(frame, procedure_texts)
        # tk.Button(frame, text="Remove Color", bg="brown", fg="white", font=conf["font"]).pack(anchor=tk.W)
        self.app.app_pack(frame, "3.6. Save and close the sketch", )
        self.app.app_pack(frame, "3.7. Use the ‘Greyscale’ button to simplify the sketch",)
        tk.Button(frame, text="Grayscale", bg="brown", fg="white", font=conf["font"], command=self.grays_scale).pack(anchor=tk.W)
        self.app.app_pack(frame, "3.8. In the ‘Colour Processing’ tab, Change the process type to 'Luminosity, Saturation, and Hue.' Set the luminosity to 45.")
        # tk.Button(frame, text="Luminocity to 45%", bg="brown", fg="white", font=conf["font"]).pack(anchor=tk.W)
        self.app.app_pack(frame,"3.9. Save and close the sketch")
        self.app.app_pack(frame,"3.10. Add some tags to each floor Stating the floor level, paper size and scale, Such as A1@1:50")

        level_frame = tk.Frame(frame)
        level_frame.pack(anchor=tk.W)

        self.app.data["tag_level"] = [tk.StringVar() for _ in range(conf["level_number"])]

        tk.Label(level_frame, text="Level", font=conf["font"]).grid(row=0, column=0)
        # tk.Label(level_frame, text="Drawing Name", font=conf["font"]).grid(row=0, column=1)
        # tk.Label(level_frame, text="Revision", font=conf["font"]).grid(row=0, column=2)

        for i in range(conf["level_number"]):
            tk.Entry(level_frame, width=34, font=conf["font"], fg="blue", textvariable=self.app.data["tag_level"][i]).grid(row=i + 1, column=0, padx=(10, 0))
            # tk.Entry(level_frame, width=50, font=conf["font"], fg="blue",
            #          ).grid(row=i + 1, column=1)
            # tk.Entry(level_frame, width=20, font=conf["font"], fg="blue",
            #          ).grid(row=i + 1, column=2, padx=(0, 10))

        tk.Button(frame, text="Add Tags", bg="brown", fg="white", font=conf["font"], command=self.add_tags).pack(anchor=tk.W)
        self.app.app_pack(frame, "3.11. Save and close, the sketch setup procedure is finished")

    def get_paper_size(self):
        return get_paper_size(self.sketch_dir.get(), 1)
    def add_tags(self):
        # all_page_size = json.load(open("page_size.json"))
        tag = ""
        if self.app.data["output_scale"].get() == "custom":
            tag+=f"1:{self.app.data['output_custom_scale'].get()}@"
        else:
            tag+=f"1:{self.app.data['output_scale'].get()}@"


        if self.app.data["output_size"].get() == "custom":
            tag += f"{self.app.data['output_custom_size_x'].get()}:{self.app.data['output_custom_size_y'].get()}"
        else:
            tag += f"{self.app.data['output_size'].get()}"


        tag_x = 0
        tag_y = 0.1
        # tag_y = round(output_size_y*0.9, 1)

        if self.app.data["output_size"].get() == "A3":
            markup_type = "Textbox-Size24"
        elif self.app.data["output_size"].get() == "A1":
            markup_type = "Textbox-Size48"
        else:
            markup_type = "Textbox-Size96"


        try:
            add_tags(self.sketch_dir.get(),markup_type, tag_x, tag_y, tag, self.app.data["tag_level"])
            self.open_sketch()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please save and close the drawing before adding tags")
            return
        # upload_frame = tk.LabelFrame(frame)
        # upload_frame.grid(row=1, column=0)
        #
        # tk.Label(upload_frame, text="Convert From", font=conf["font"]).grid(row=0, column=0, columnspan=4, sticky="W")
        #
        # self.app.data["input_scale"] = tk.StringVar()
        # self.app.data["input_size"] = tk.StringVar()
        # tk.Label(upload_frame, text="1:", font=conf["font"]).grid(row=1, column=0)
        # tk.Entry(upload_frame, textvariable=self.app.data["input_scale"], font=conf["font"], fg="blue", width=4).grid(row=1, column=1)
        # tk.Label(upload_frame, text="@", font=conf["font"]).grid(row=1, column=2)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["input_size"], values=conf["input_sizes"],state="readonly", font=conf["font"], width=3).grid(row=1, column=3)
        #
        # tk.Label(upload_frame, text="To", font=conf["font"]).grid(row=2, column=0, columnspan=4, sticky="W")
        #
        # self.app.data["output_scale"] = tk.StringVar()
        # self.app.data["output_size"] = tk.StringVar()
        # tk.Label(upload_frame, text="1:", font=conf["font"]).grid(row=3, column=0)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["output_scale"], values=conf["output_scales"], state="readonly", font=conf["font"], width=3).grid(row=3, column=1)
        # tk.Label(upload_frame, text="@", font=conf["font"]).grid(row=3, column=2)
        # ttk.Combobox(upload_frame, textvariable=self.app.data["output_size"], values=conf["output_sizes"], state="readonly", font=conf["font"], width=3).grid(row=3, column=3)
        #
        # tk.Button(upload_frame, text="Import File(s)", bg="brown", fg="white", font=conf["font"], command=self.page_one_process).grid(row=4, column=0, columnspan=4, sticky="W")

    def open_sketch_thread(self):
        open_pdf_in_bluebeam(self.sketch_dir.get())
    def open_sketch(self):
        _thread.start_new_thread(self.open_sketch_thread, ())
    def page_one_process(self):
        files = self.drop_file_listbox.get_files_list()

        if len(self.app.quotation_number.get())==0:
            messagebox.showerror("Error", "Please Enter a project before resize")
            return

        #todo error handliung: if the input file is not a pdf
        if len(files)==0:
            messagebox.showerror("Error", "Please input at least one pdf file in the dialog box")
            return
        elif len(files) == 1:
            input_file = files[0]
            # disk, project_name, file_name = extract_disk_and_project_name(input_file)
            # current_project = "\\".join([disk, project_name])
            # # self.project_dir.set("\\".join([disk, project_name]))
            # self.sketch_dir = f"{current_project}\\{project_name}-Mechanical Sketch.pdf"
        else:
            # assuming all the file are import from the same
            #
            # disk, project_name, file_name = extract_disk_and_project_name(files[0])
            #
            # current_project = "\\".join([disk, project_name])
            # # self.project_dir.set("\\".join([disk, project_name]))
            # self.sketch_dir = f"{current_project}\\{project_name}-Mechanical Sketch.pdf"

            current_pdf_parent_directory = Path(files[0]).parent.absolute()
            combine_pdf_dir = os.path.join(current_pdf_parent_directory, date.today().strftime("%Y%m%d")+"-Combined.pdf")
            try:
                combine_pdf(files, combine_pdf_dir)
                self.drop_file_listbox.delete_all()
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Please close the pdf while combining")
                return

            input_file=combine_pdf_dir

        #todo error handling
        if self.app.data["input_scale"].get() == "custom":
            input_scale = self.app.data["input_custom_scale"].get()
            # if not is_float(input_scale):
            #     messagebox.showerror("Error", "Please enter correct input scale")
            #     return
        else:
            input_scale = self.app.data["input_scale"].get()

        if self.app.data["output_scale"].get() == "custom":
            output_scale = self.app.data["output_custom_scale"].get()
            # if not is_float(output_scale):
            #     messagebox.showerror("Error", "Please enter correct output scale")
            #     return
        else:
            output_scale = self.app.data["output_scale"].get()

        page_size_json_dir = os.path.join(conf["database_dir"], "page_size.json")
        all_page_size = json.load(open(page_size_json_dir))

        if self.app.data["input_size"].get() == "custom":
            input_size_x = convert_mm_to_pixel(self.app.data["input_custom_size_x"].get())
            input_size_y = convert_mm_to_pixel(self.app.data["input_custom_size_y"].get())
            # if not is_float(input_size_x) or is_float(input_size_y):
            #     messagebox.showerror("Error", "Please enter correct input size width and height")
            #     return
        else:
            input_size_x = convert_mm_to_pixel(all_page_size[self.app.data["input_size"].get()]["width"])
            input_size_y = convert_mm_to_pixel(all_page_size[self.app.data["input_size"].get()]["height"])

        if self.app.data["output_size"].get() == "custom":
            output_size_x = convert_mm_to_pixel(self.app.data["output_custom_size_x"].get())
            output_size_y = convert_mm_to_pixel(self.app.data["output_custom_size_y"].get())
        else:
            output_size_x = convert_mm_to_pixel(all_page_size[self.app.data["output_size"].get()]["width"])
            output_size_y = convert_mm_to_pixel(all_page_size[self.app.data["output_size"].get()]["height"])
            # if not is_float(output_size_x) or is_float(output_size_y):
            #     messagebox.showerror("Error", "Please enter correct output size width and height")
            #     return

        if file_exists(self.sketch_dir.get()):
            rewrite = messagebox.askyesno("File Found", f"{self.sketch_dir.get()} exists. Put in the SS?")
            if rewrite:
                ss_dir = os.path.join(self.app.current_folder_address, "SS")
                current_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
                os.mkdir(os.path.join(ss_dir, current_time))
                shutil.move(self.sketch_dir.get(), os.path.join(ss_dir, current_time))
            else:
                return



        try:
            resize_pdf(input_file, input_scale, input_size_x, input_size_y,
                       output_scale, output_size_x, output_size_y, self.sketch_dir.get())
            flatten_pdf(self.sketch_dir.get(), self.sketch_dir.get())
            self.open_sketch()
            self.update_current_project_entry()
            self.drop_file_listbox.delete_all()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please Close the pdf while resizing")
            return
        self.show_procedure(conf["sketch_procedures"][1])
    # def forth_step(self):
    #     procedure = conf["sketch_procedures"][3]
    #     frame = self.procedure_frames[procedure]
    #     procedure_text = """
    #                     Procedure:
    #                     Choose a basepoint and apply to all pages
    #                     Align the basepoint manually for each page
    #                     Click The Align
    #                     """
    #     tk.Label(frame, text=procedure_text, font=conf["font"]).grid(row=0, column=0)
    #     upload_frame = tk.LabelFrame(frame)
    #     upload_frame.grid(row=1, column=0)
    #
    #     tk.Button(upload_frame, text="Align", bg="brown", fg="white", font=conf["font"], command=self.align).grid(row=0, column=0)
    #
    # def align(self):
    #     self.sketch_dir = r"P:\bluebeam_codepilot_test_folder\bluebeam_codepilot_test_folder-Mechanical Sketch.pdf"
    #     align(self.sketch_dir)
    #     open_pdf_in_bluebeam(self.sketch_dir)

    # def fifth_step(self):
    #     procedure = conf["sketch_procedures"][4]
    #     frame = self.procedure_frames[procedure]
    #     procedure_text = """
    #                     Procedure:
    #                     erase content which is not needed, as per 10.11
    #                     or erase content by remove colour
    #                     or grayscale
    #                     """
    #     tk.Label(frame, text=procedure_text, font=conf["font"]).grid(row=0, column=0)
    #
    #     button_frame = tk.LabelFrame(frame)
    #     button_frame.grid(row=1, column=0)
    #
    #     tk.Button(button_frame, text="Remove Color", bg="brown", fg="white", font=conf["font"]).grid(row=0, column=0)
    #     tk.Button(button_frame, text="Grayscale", bg="brown", fg="white", font=conf["font"], command=self.grays_scale).grid(row=0, column=1)

    def grays_scale(self):
        try:
            grays_scale_pdf(self.sketch_dir.get())
            open_pdf_in_bluebeam(self.sketch_dir.get())
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Please Save and close the file before gray scale")
    def compress(self):
        compress(self.sketch_dir.get())