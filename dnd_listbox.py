from tkinterdnd2 import *
import tkinter as tk
from tkinter import messagebox
import os

from utility import open_pdf_in_bluebeam, extract_disk_and_project_name
from config import CONFIGURATION as conf


class DndListbox(tk.Listbox):
    def __init__(self, *args, **kwargs):

        self.files_list = kwargs.pop("file_list")

        if "app" in kwargs.keys():
            self.app = kwargs.pop("app")
        else:
            self.app = None

        tk.Listbox.__init__(self, *args, **kwargs)

        self.drop_target_register(DND_FILES, DND_TEXT)
        self.dnd_bind('<<DropEnter>>', self.drop_enter)
        self.dnd_bind('<<DropPosition>>', self.drop_position)
        self.dnd_bind('<<DropLeave>>', self.drop_leave)
        self.dnd_bind('<<Drop>>', self.drop)
        self.dnd_bind('<<DragInitCmd>>', self.drag_init_listbox)
        self.dnd_bind('<<DragEndCmd>>', self.drag_end)

    def drop_enter(self, event):
        # print('Drop enter')
        event.widget.focus_force()
        return event.action
    def drop_position(self, event):
        # print("drop position")
        return event.action
    def drop_leave(self, event):
        # print("drop leave")
        return event.action
    def drop(self, event):
        if event.data:
            files = self.tk.splitlist(event.data)
            if not self.app is None and len(self.files_list) == 0:
                first_file = files[0]
                if not self.load_project_based_on_file(first_file):
                    return

            for f in files:
                if os.path.exists(f):
                    self.insert('end', f)
                    self.files_list.append(f)
                else:
                    print(f'Not dropping file {f}: file does not exist.')
            #only consider the first file here

        return event.action

    def load_project_based_on_file(self, file):
        disk, project_name, filename = extract_disk_and_project_name(file)

        if disk != conf["working_dir"]:
            messagebox.showerror(title="Error", message=f"You should input the file from {conf['working_dir']}")
            return False
        elif not "-" in project_name:
            messagebox.showerror(title="Error", message=f"Can's find the project number or quotation number from {project_name}")
            return False
        quotation_number = project_name.split("-")[0]
        data = self.app.search_bar_page.check(None, quotation_number)

        if len(set(data)) == 1:
            if len(self.app.quotation_number.get()) != 0:
                self.app.save()
            self.app.set_quotation_number(data[0])
            return True
        else:
            messagebox.showerror(title="Error", message=f"Cannot find the project with {quotation_number}")
            return False

    def drag_init_listbox(self, event):
        data = ()
        if self.curselection():
            data = tuple([self.get(i) for i in self.curselection()])
        return ((ASK, COPY), (DND_FILES, DND_TEXT), data)

    def drag_end(self, event):
        # print('Drag ended for widget:', event.widget)
        pass

    def get_files_list(self):
        return self.files_list

    def move_up_item(self):
        index = self.curselection()[0]
        if index == 0:
            return
        item = self.get(tk.ACTIVE)

        self.delete(index)
        self.insert(index-1, item)

        # self.selection_set(index-1)

        self.files_list[index], self.files_list[index-1] = self.files_list[index-1], self.files_list[index]

        self.selection_clear(0, tk.END)
        self.selection_set(index-1)
    def move_down_item(self):
        index = self.curselection()[0]
        if index == len(self.files_list) - 1:
            return
        item = self.get(tk.ACTIVE)

        self.delete(index)
        self.insert(index + 1, item)

        # self.select_set(index + 1)
        # self.selection_set(index + 1)

        self.files_list[index], self.files_list[index + 1] = self.files_list[index + 1], self.files_list[index]

    def delete_item(self):
        index = self.curselection()[0]

        self.delete(index)
        self.files_list.pop(index)

        # self.selection_set(index - 1)
        # self.select_set(index - 1)

    def delete_all(self):
        for _ in range(len(self.files_list)):
            self.delete(0)
        self.files_list = []


    def open_item(self):
        item = self.get(tk.ACTIVE)
        open_pdf_in_bluebeam(item)

    #todo fix pointer error
    def load(self, file_list):
        self.files_list = file_list
        for file in self.files_list:
            self.insert(tk.END, file)

