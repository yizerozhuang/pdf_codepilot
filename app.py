import tkinter as tk
from tkinter import messagebox

from search_bar_page import SearchBarPage
from combine_drawing_page import CombineDrawingPage
from mechanical_sketch_page import MechanicalSketchPage
from mechanical_drawing_page import MechanicalDrawingPage

from utility import read_json, open_folder, open_link_with_edge, save_tk_to_json, load_json_to_tk
from config import CONFIGURATION as conf
from tkinterdnd2 import TkinterDnD

import os


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        # TkinterDnD.Tk.__init__(self, *args, **kwargs)

        TkinterDnD.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.__init__(self, *args, **kwargs)
        self.title("PDF Codepilot")
        self.state("zoomed")

        self.quotation_number = tk.StringVar()
        self.project_number = tk.StringVar()
        self.project_name = tk.StringVar()
        self.data = {}
        self.sketch_dir = tk.StringVar()
        self.drawing_dir = tk.StringVar()

        self.utility_frame_setup()
        self.main_frame_setup()
        self.page_frame_setup()

        self.protocol("WM_DELETE_WINDOW", self.confirm)

    def utility_frame_setup(self):
        self.utility_frame = tk.LabelFrame(self)
        self.utility_frame.pack(fill=tk.X, side=tk.TOP)

        info_frame = tk.LabelFrame(self.utility_frame)
        info_frame.pack(side=tk.LEFT)

        tk.Label(info_frame, text="Project Number:", font=conf["font"]).grid(row=0, column=0, sticky="w")
        tk.Label(info_frame, text="Quotation Number:", font=conf["font"]).grid(row=1, column=0, sticky="w")
        tk.Label(info_frame, text="Project Name:", font=conf["font"]).grid(row=2, column=0, sticky="w")

        tk.Label(info_frame, textvariable=self.project_number, font=conf["font"], width=50).grid(row=0, column=1, sticky="w")
        tk.Label(info_frame, textvariable=self.quotation_number, font=conf["font"], width=50).grid(row=1, column=1, sticky="w")
        tk.Label(info_frame, textvariable=self.project_name, font=conf["font"], width=50).grid(row=2, column=1, sticky="w")

        search_frame = tk.Frame(info_frame)
        search_frame.grid(row=3, column=0, columnspan=2)
        self.utility_search_string_var = tk.StringVar()
        tk.Entry(search_frame, fg="blue", font=conf["font"], textvariable=self.utility_search_string_var).grid(row=0, column=0)
        tk.Button(search_frame, text="Clear Up", command=self.utility_reset, bg="brown", fg="white",
                  font=conf["font"]).grid(row=0, column=1)
        tk.Button(search_frame, text="Search", command=self.utility_search, bg="brown", fg="white",
                  font=conf["font"]).grid(row=0, column=2)
        self.bind("<Control-Key-space>", self.utility_search)

        function_frame = tk.LabelFrame(self.utility_frame)
        function_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(function_frame, text="Open Folder", font=conf["font"], bg="brown", fg="white", width=12,
                  command=self.open_folder).grid(row=0, column=0)
        tk.Button(function_frame, text="Open Asana", font=conf["font"], bg="brown", fg="white", width=12,
                  command=self.open_asana).grid(row=0, column=1)

    def main_frame_setup(self):
        self.main_frame = tk.LabelFrame(self)


        self.search_bar_page = SearchBarPage(self)
        self.combine_page = CombineDrawingPage(self)
        self.mechanical_sketch_page = MechanicalSketchPage(self)
        self.mechanical_drawing_page = MechanicalDrawingPage(self)

    def page_frame_setup(self):
        self.page_frame = tk.LabelFrame(self)
        self.page_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.current_page = self.mechanical_sketch_page
        self.show_page(self.current_page)

        tk.Button(self.page_frame, text="Search", bg="brown", fg="white", font=conf["font"],
                  command=lambda: self.show_page(self.search_bar_page)).pack(side=tk.LEFT)
        tk.Button(self.page_frame, text="Combine", bg="brown", fg="white", font=conf["font"],
                  command=lambda: self.show_page(self.combine_page)).pack(side=tk.LEFT)
        tk.Button(self.page_frame, text="Sketch", bg="brown", fg="white", font=conf["font"],
                  command=lambda: self.show_page(self.mechanical_sketch_page)).pack(side=tk.LEFT)
        # tk.Button(self.page_frame, text="Drawing", bg="brown", fg="white", font=conf["font"],
        #           command=lambda: self.show_page(self.mechanical_drawing_page)).pack(side=tk.LEFT)

    def show_page(self, page):
        self.current_page.pack_forget()
        self.current_page = page
        self.current_page.pack(fill=tk.BOTH, expand=1)

    def load_bridge_json(self):
        return read_json(os.path.join(conf["database_dir"], self.quotation_number.get(), "data.json"))


    def set_quotation_number(self, data):
        self.quotation_number.set(data[0])
        self.project_number.set(data[1])
        self.project_name.set(data[2])

        self.data_json = self.load_bridge_json()

        self.current_folder_address = os.path.join(conf["working_dir"], self.data_json["Current_folder_address"])

        self.sketch_dir.set(str(os.path.join(conf["working_dir"],
                                             self.data_json["Current_folder_address"],
                                             self.project_name.get()+"-"+conf["sketch_name"])))

        self.drawing_dir.set(str(os.path.join(conf["working_dir"],
                             self.data_json["Current_folder_address"],
                             self.project_name.get() + "-" + conf["drawing_name"])))


        self.initial_pdf_database()

        self.load()


    def save(self):
        data_dir = os.path.join(conf["database_dir"], self.quotation_number.get(), "pdf.json")
        save_tk_to_json(self, data_dir)
    def load(self):
        data_dir = os.path.join(conf["database_dir"], self.quotation_number.get(), "pdf.json")
        load_json_to_tk(self, data_dir)

        self.mechanical_sketch_page.drop_file_listbox.delete_all()


    def initial_pdf_database(self):
        if os.path.exists(os.path.join(conf["database_dir"], self.quotation_number.get(), "pdf.json")):
            return
        pdf_data_template_dir = os.path.join(conf["database_dir"], "pdf_data_template.json")
        load_json_to_tk(self, pdf_data_template_dir)
        self.save()




    def utility_reset(self):
        # reset(self)
        # todo:reset the project

        if len(self.quotation_number.get()) != 0:
            self.save()

        self.quotation_number.set("")
        self.project_number.set("")
        self.project_name.set("")

        pdf_data_template_dir = os.path.join(conf["database_dir"], "pdf_data_template.json")
        load_json_to_tk(self, pdf_data_template_dir)

        self.mechanical_sketch_page.drop_file_listbox.reset()

        self.sketch_dir = ""
        self.drawing_dir = ""

        self.utility_search_string_var.set("")

    def utility_search(self, *args):
        data = self.search_bar_page.check(None, self.utility_search_string_var.get().strip())

        if len(set(data)) == 1:
            self.set_quotation_number(data[0])
        else:
            self.search_bar_page.entry.delete(0, "end")
            self.search_bar_page.entry.insert(0, self.utility_search_string_var.get().strip())
            self.search_bar_page.check(None)
            self.search_bar_page.refresh()
            self.show_page(self.search_bar_page)
        self.utility_search_string_var.set("")


    def open_folder(self):

        if len(self.quotation_number.get()) == 0:
            messagebox.showerror("Error", "Please login a Project before open folder")
            return

        folder = os.path.join(conf["working_dir"], self.load_bridge_json()["Current_folder_address"])
        open_folder(folder)

    def open_asana(self):

        if len(self.quotation_number.get()) == 0:
            messagebox.showerror("Error", "Please login a Project before open asana")
            return

        link = self.load_bridge_json()["Asana_url"]+"/f"
        open_link_with_edge(link)

    def app_pack(self, frame, input):
        if type(input) == str:
            tk.Label(frame, text=input, font=conf["font"]).pack(anchor=tk.NW)
        elif type(input)== list:
            for item in input:
                tk.Label(frame, text=item, font=conf["font"]).pack(anchor=tk.NW)
    # def mechanical_sketch_frame(self):


    def confirm(self):
        if len(self.quotation_number.get()) == 0:
            self.destroy()
        else:
            try:
                self.save()
            except Exception as e:
                print(e)
            self.destroy()