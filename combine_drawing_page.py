import filecmp
import tkinter as tk
from tkinter import messagebox

from utility import *
from dnd_listbox import DndListbox

from datetime import date
from pathlib import Path

class CombineDrawingPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.main_frame)
        self.app = app

        self.combine_list = []
        self.combine_name_extension = tk.StringVar()

        dnd_listbox_frame = tk.Frame(self)
        dnd_listbox_frame.pack(fill=tk.BOTH, expand=1)

        self.drop_file_listbox = DndListbox(
            dnd_listbox_frame,
            selectmode='single',
            width=200,
            height=30,
            font=conf["font"],
            file_list=self.combine_list
        )
        self.drop_file_listbox.grid(row=0, column=0, pady=(100, 0), padx=(200, 0))

        button_frame = tk.Frame(dnd_listbox_frame)
        button_frame.grid(row=0, column=1, pady=(100, 0))

        tk.Button(button_frame, text="Up", width=10, bg="brown", fg="white", font=conf["font"],
                  command=self.drop_file_listbox.move_up_item).grid(row=0, column=0, sticky=tk.N)
        tk.Button(button_frame, text="Down", width=10, bg="brown", fg="white", font=conf["font"],
                  command=self.drop_file_listbox.move_down_item).grid(row=1, column=0, sticky=tk.N)
        tk.Button(button_frame, text="Delete", width=10, bg="brown", fg="white", font=conf["font"],
                  command=self.drop_file_listbox.delete_item).grid(row=2, column=0, sticky=tk.N)
        tk.Button(button_frame, text="Open", width=10, bg="brown", fg="white", font=conf["font"],
                  command=self.drop_file_listbox.open_item).grid(row=3, column=0, sticky=tk.N)
        tk.Button(button_frame, text="Delete All", width=10, bg="brown", fg="white", font=conf["font"],
                  command=self.drop_file_listbox.delete_all).grid(row=4, column=0, sticky=tk.N)


        combine_name_frame = tk.Frame(dnd_listbox_frame)
        combine_name_frame.grid(row=1, column=0, columnspan=2)

        tk.Label(combine_name_frame, font=conf["font"], text="YYYYMMDD-Combined ").grid(row=0, column=0)
        tk.Entry(combine_name_frame, font=conf["font"], fg="blue", textvariable=self.combine_name_extension).grid(row=0, column=1)
        tk.Label(combine_name_frame, font=conf["font"], text=".pdf").grid(row=0, column=2)
        tk.Button(combine_name_frame, text="Combine", width=10, bg="brown", fg="white", font=conf["font"], command=self.combine_drawing).grid(row=0, column=3)



    def combine_drawing(self):
        #assuming all the drawing are in one subfolder
        #todo error if input file are not in the same subfolder

        current_pdf_parent_directory = Path(self.combine_list[0]).parent.absolute()
        if len(self.combine_name_extension.get()) == 0:
            combine_pdf_dir = os.path.join(current_pdf_parent_directory, date.today().strftime("%Y%m%d") + "-Combined.pdf")
        else:
            combine_pdf_dir = os.path.join(current_pdf_parent_directory, date.today().strftime("%Y%m%d") + "-Combined "  + self.combine_name_extension.get() + ".pdf")

        if file_exists(combine_pdf_dir):
            rewrite = messagebox.askyesno("File Found", f"{combine_pdf_dir} exists. Overwrite?")
            if not rewrite:
                return

        try:
            combine_pdf(self.combine_list, combine_pdf_dir)
            self.drop_file_listbox.delete_all()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "The file is opened, please close the file before combine")
            return
        open_pdf_in_bluebeam(combine_pdf_dir)

