import customtkinter as ctk
import logging

import node
from table import Table, Entyrods, Entrynodes, Tablebuttons
from CTkMessagebox import CTkMessagebox
from saveData import save_rods
from node import Nodestable

class Rodstable(ctk.CTkToplevel):
    count =0
    dict_items = dict()

    @staticmethod
    def get_data_about_rods():
        return Rodstable.dict_items

    @staticmethod
    def fill_dict(data):
        if Rodstable.dict_items:
            Rodstable.dict_items.clear()

        for item in data:
            key = item[0]
            val = item[1:]
            Rodstable.dict_items[key] = val

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info("Entry Rod info")
        # self.geometry("600x425")
        self.columns = ('№ стержня', 'L', 'A', 'E', 'σ', 'q')

        self.tbl = Table(self, "Стержень", columns=self.columns)
        self.tbl.table_tree['show'] = 'headings'
        self.tbl.pack()
        self.entr = Entyrods(self)
        # self.btns = Tablebuttons(self)
        self.btns = ctk.CTkButton(self,text="Удалить стержень")


        # self.btns.save_btn.bind('<Button-1>', self.save_all)
        self.entr.ready_btn.bind('<Button-1>', self.fetch_res)
        self.btns.bind('<Button-1>', self.delete_rode)
        self.tbl.table_tree.bind('<ButtonRelease-1>', self.on_select)
        self.tbl.pack()
        self.btns.pack(anchor=ctk.SE, side=ctk.LEFT )
        self.entr.pack(anchor=ctk.W, pady=4)
        if Rodstable.dict_items:
            self.setter_rodes()

    def clear_table(self):
        self.tbl.table_tree.delete(*self.tbl.table_tree.get_children())

    def fill_table(self):
        for item in sorted(Rodstable.dict_items):
            self.tbl.table_tree.insert('', ctk.END, iid=item, values=(item, Rodstable.dict_items[item][0],
                                                                    Rodstable.dict_items[item][1],
                                                                    Rodstable.dict_items[item][2],
                                                                    Rodstable.dict_items[item][3],
                                                                    Rodstable.dict_items[item][4]))
        logging.info("Got items for fill the table")

    def set_vals_on_center(self):
        for col in self.columns:
            self.tbl.table_tree.column(col, anchor=ctk.CENTER)

    def delete_rode(self, event):
        if Rodstable.count == 0:
            CTkMessagebox(title='Error', message='Ошибка удаления \nВ таблице не осталось заполненных полей',icon="cancel")
            return

        number_to_del = ctk.CTkInputDialog(text= 'Введите № стержня:', title="Удаление стержня").get_input()
        number_to_del = int(number_to_del)
        print(number_to_del)
        if number_to_del not in Rodstable.dict_items:
            CTkMessagebox(title='Warning Message!', message='Вы пытаетесь удалить стержень, которого '
                                          'не существует',icon="warning" )
            return

        self.clear_table()

        Rodstable.dict_items.pop(number_to_del)
        Rodstable.count -= 1
        for item in Rodstable.dict_items:
            if item > number_to_del:
                Rodstable.dict_items[item - 1] = (Rodstable.dict_items[item][0],
                                                  Rodstable.dict_items[item][1],
                                                  Rodstable.dict_items[item][2],
                                                  Rodstable.dict_items[item][3],
                                                  Rodstable.dict_items[item][4])
                Rodstable.dict_items.pop(item)

        self.fill_table()


    def fetch_res(self, event):
        if self.entr.numb_entry.get():
            try:
                number_rod = int(self.entr.numb_entry.get())
                if not number_rod >= 1:
                    CTkMessagebox(title='Warning Message!', message='Стержень с таким № не существует', icon="warning")
                    self.entr.numb_entry.delete(0, ctk.END)
                    return
            except ValueError:
                CTkMessagebox(title='Error', message='Значение должно быть целочисленным',icon="cancel" )
                self.entr.numb_entry.delete(0, ctk.END)
                return
        else:
            CTkMessagebox(title='Warning Message!',message= 'Не введён номер стержня',icon="warning" )
            if self.entr.length_entry.get():
                self.entr.length_entry.delete(0, ctk.END)

            if self.entr.a_entry.get():
                self.entr.a_entry.delete(0, ctk.END)

            if self.entr.e_entry.get():
                self.entr.e_entry.delete(0, ctk.END)

            if self.entr.sigma_entry.get():
                self.entr.sigma_entry.delete(0, ctk.END)

            if self.entr.q_entry.get():
                self.entr.q_entry.delete(0, ctk.END)
            return

        if self.entr.length_entry.get():
            try:
                length = float(self.entr.length_entry.get())
                if not length >= 1:
                    CTkMessagebox(title='Warning Message!', message='Длина должна быть > 0',icon="warning" )
                    self.entr.length_entry.delete(0, ctk.END)
                    return
            except ValueError:
                CTkMessagebox(title='Error', message='Значение должно быть целочисленным',icon="cancel" )
                self.entr.length_entry.delete(0, ctk.END)
                return
        else:
            length = 0

        if self.entr.a_entry.get():
            try:
                a = float(self.entr.a_entry.get())
                if not a >= 1:
                    CTkMessagebox(title='Warning Message!', message='Площадь должна быть >= 0',icon="warning" )
                    self.entr.a_entry.delete(0, ctk.END)
                    return
            except ValueError:
                CTkMessagebox(title='Error', message='Значение должно быть целочисленным',icon="cancel" )
                self.entr.a_entry.delete(0, ctk.END)
                return
        else:
            a = 0

        if self.entr.e_entry.get():
            try:
                e = float(self.entr.e_entry.get())
                if e < 0:
                    CTkMessagebox(title='Warning Message!', message='Модуль Юнга должен быть положительным',icon="warning" )
                    self.entr.e_entry.delete(0, ctk.END)
                    return
            except ValueError:
                CTkMessagebox(title='Error', message= 'Значение должно быть целочисленным', icon="cancel")
                self.entr.e_entry.delete(0, ctk.END)
                return
        else:
            e = 0

        if self.entr.sigma_entry.get():
            try:
                sigma = int(self.entr.sigma_entry.get())
                if not sigma >= 1:
                    CTkMessagebox(title='Warning Message!', message='Допускаемое напряжение должно быть положительным', icon="warning")
                    self.entr.sigma_entry.delete(0, ctk.END)
                    return
            except ValueError:
                CTkMessagebox(title='Error', message='Значение должно быть целочисленным',icon="cancel" )
                self.entr.sigma_entry.delete(0, ctk.END)
                return
        else:
            sigma = 0

        if self.entr.q_entry.get():
            try:
                q = float(self.entr.q_entry.get())
            except ValueError:
                CTkMessagebox(title='Error', message='Значение должно быть целочисленным',icon="cancel" )
                self.entr.q_entry.delete(0, ctk.END)
                return
        else:
            q = 0
        if number_rod in Rodstable.dict_items.keys():
            Rodstable.dict_items[number_rod] = (length, a, e, sigma, q)
            if number_rod <= Rodstable.count:
                self.clear_table()
                self.fill_table()
            else:
                self.tbl.table_tree.delete(number_rod)
                self.tbl.table_tree.insert('', number_rod, iid=number_rod, values=(number_rod, length, a, e, sigma, q))

        else:
            if number_rod > Rodstable.count:
                for i in range(Rodstable.count + 1, number_rod):
                    Rodstable.dict_items[i] = (0, 0, 0, 0, 0)
                    self.tbl.table_tree.insert('', i, values=(i, 0, 0, 0, 0, 0))

            Rodstable.dict_items[number_rod] = (length, a, e, sigma, q)
            self.tbl.table_tree.insert('', number_rod, values=(number_rod, length, a, e, sigma, q))

        Rodstable.count = len(Rodstable.dict_items)
        self.set_vals_on_center()

    #Save data of rodes
    def setter_rodes(self):
        Rodstable.count = len(Rodstable.dict_items)
        self.clear_table()

        self.fill_table()

        self.set_vals_on_center()

    def on_select(self,event):
        # Получить данные из строки, которая сейчас в фокусе:
        cur_item = self.tbl.table_tree.item(self.tbl.table_tree.focus())

        # print('cur_item =', cur_item)  #То что нам нужно. Значения всех ячеек
        # print('cur_item.value', cur_item['values'][0])
        self.clear_entry()
        self.entr.numb_entry.insert(0, str(cur_item['values'][0]))
        self.entr.length_entry.insert(0, str(cur_item['values'][1]))
        self.entr.a_entry.insert(0, str(cur_item['values'][2]))
        self.entr.e_entry.insert(0, str(cur_item['values'][3]))
        self.entr.sigma_entry.insert(0, str(cur_item['values'][4]))
        self.entr.q_entry.insert(0, str(cur_item['values'][5]))

    def clear_entry(self):
        self.entr.numb_entry.delete(0, 'end')
        self.entr.length_entry.delete(0, 'end')
        self.entr.e_entry.delete(0, 'end')
        self.entr.a_entry.delete(0, 'end')
        self.entr.sigma_entry.delete(0, 'end')
        self.entr.q_entry.delete(0, 'end')

    def save_all(self, event):
        for i in range(1, len(Rodstable.dict_items) + 2):
            Nodestable.dict_items[i] = (0, 0)
        Nodestable.count = len(Rodstable.dict_items) + 1
        save_rods(Rodstable.dict_items)
