import customtkinter as ctk
from tkinter.ttk import Treeview
from tkinter import *

class Readybutton(ctk.CTkButton):
    def __init__(self, master=None):
        ctk.CTkButton.__init__(self, master, text="Готово")

class Table(ctk.CTkFrame):
    def __init__(self, master, title, columns):
        super().__init__(master)
        self.pack(expand="YES", fill="both")

        self.title_lbl = ctk.CTkLabel(self, text=title, )
        self.title_lbl.pack(side=ctk.TOP, fill=ctk.X, expand=ctk.YES)
        self.table_tree = Treeview(self, columns=columns)
        self.table_tree.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=ctk.YES)

        for i in range(len(columns)):
            self.table_tree.heading(columns[i], text=columns[i])




class Entyrods(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=ctk.BOTH, expand=ctk.YES)

        self.numb_lbl = ctk.CTkLabel(self, text='№:')
        self.numb_lbl.grid(row=0, column=0)
        self.numb_entry = ctk.CTkEntry(self, width=80)
        self.numb_entry.grid(row=0, column=1, padx=10)

        self.length_lbl = ctk.CTkLabel(self, text='L:')
        self.length_entry = ctk.CTkEntry(self, width=80)
        self.length_lbl.grid(row=1, column=0)
        self.length_entry.grid(row=1, column=1)

        self.e_lbl = ctk.CTkLabel(self, text='E:')
        self.e_lbl.grid(row=2, column=0)
        self.e_entry = ctk.CTkEntry(self, width=80)
        self.e_entry.grid(row=2, column=1)

        self.a_lbl = ctk.CTkLabel(self, text='A:')
        self.a_lbl.grid(row=0, column=3)
        self.a_entry = ctk.CTkEntry(self, width=80)
        self.a_entry.grid(row=0, column=4)

        self.sigma_lbl = ctk.CTkLabel(self, text='σ:')
        self.sigma_lbl.grid(row=1, column=3)
        self.sigma_entry = ctk.CTkEntry(self, width=80)
        self.sigma_entry.grid(row=1, column=4)

        self.q_lbl = ctk.CTkLabel(self, text='q:')
        self.q_lbl.grid(row=2, column=3)
        self.q_entry = ctk.CTkEntry(self, width=80)
        self.q_entry.grid(row=2, column=4)

        self.ready_btn = Readybutton(self)
        self.ready_btn.grid(row=3, column=0, rowspan=2, sticky=ctk.SE)


class Entrynodes(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=ctk.BOTH)

        self.numb_lbl = ctk.CTkLabel(self, text='№:  ')
        self.numb_entry = ctk.CTkEntry(self, width=200)
        self.force_lbl = ctk.CTkLabel(self, text='F:  ')
        self.force_entrys = ctk.CTkEntry(self, width=200)

        self.var = ctk.IntVar()

        self.obstacle_check = ctk.CTkCheckBox(self, text='Заделка', variable=self.var)
        self.ready_btn = Readybutton(self)

        self.numb_lbl.grid(row=0, column=0)
        self.numb_entry.grid(row=0, column=1)

        self.force_lbl.grid(row=2, column=0)
        self.force_entrys.grid(row=2, column=1)

        self.obstacle_check.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.ready_btn.grid(row=6, column=0, sticky=SE)

class Tablebuttons(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        # self.save_btn = ctk.CTkButton(self, text='Сохранить')
        self.minus_btn = ctk.CTkButton(self, text='Удалить узел')

        # self.save_btn.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.minus_btn.pack(side=LEFT, expand=YES, fill=BOTH)
