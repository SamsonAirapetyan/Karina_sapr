import customtkinter as ctk
import logging
from table import Table, Entyrods, Entrynodes, Tablebuttons
from CTkMessagebox import CTkMessagebox
from saveData import save_nodes
import rod

class Nodestable(ctk.CTkToplevel):
    count = 0
    dict_items = dict()

    @staticmethod
    def get_data_about_nodes():
        return Nodestable.dict_items

    @staticmethod
    def set_dict(data):
        if Nodestable.dict_items:
            Nodestable.dict_items.clear()

        for item in data:
            key = item[0]
            val = item[1:]
            Nodestable.dict_items[key] = val

    def __init__(self, inner):
        super().__init__( inner)
        # self.pack()

        self.colums = ('№', 'F', 'Заделка')
        self.tbl = Table(self, title='Узлы', columns=('№', 'F', 'Заделка'))
        self.tbl.table_tree['show'] = 'headings'

        self.entr = Entrynodes(self)  #проинициализированы кнопки добавления элементов
        self.btns = Tablebuttons(self)  #проинициализированы кнопки сохранения

        self.entr.ready_btn.bind('<Button-1>', self.fetch_res)
        # self.btns.save_btn.bind('<Button-1>', self.save_all)
        self.btns.minus_btn.bind('<Button-1>', self.delete_node)
        self.tbl.table_tree.bind('<ButtonRelease-1>', self.on_select)


        self.tbl.pack()
        self.btns.pack(anchor=ctk.SE, side=ctk.LEFT)
        self.entr.pack(anchor=ctk.W, pady=4)

        if Nodestable.dict_items:
            self.setter_nodes()

    def fetch_res(self, event):
        if self.entr.numb_entry.get():
            try:
                number_node = int(self.entr.numb_entry.get())
                if number_node <= 0:
                    CTkMessagebox(title='Warning Message!', icon="warning", message='Номер узла должен быть > 0')
                    self.entr.numb_entry.delete(0, ctk.END)
                    return
                if number_node > len(rod.Rodstable.dict_items)+1:
                    CTkMessagebox(title='Warning Message!', icon="warning", message='Кол-во узлов должно быть на единицу больше кол-ва стержней')
                    return
            except ValueError:
                CTkMessagebox(title='Error', icon="cancel", message='Значение должно быть целочисленным')
                self.entr.numb_entry.delete(0, ctk.END)
                return
        else:
            CTkMessagebox(title='Error', icon="cancel", message='Не введен № узла')
            if self.entr.force_entrys.get():
                self.entr.force_entrys.delete(0, ctk.END)
            return

        if self.entr.force_entrys.get():
            try:
                force = float(self.entr.force_entrys.get())
            except ValueError:
                CTkMessagebox(title='Error', icon="cancel", message='Значение должно быть целочисленным')
                self.entr.force_entrys.delete(0, ctk.END)
                return
        else:
            force = 0

        check_block = self.entr.var.get()
        if int(number_node) != 1 and int(number_node) != len(rod.Rodstable.dict_items)+1 and check_block :
            CTkMessagebox(title='Warning Message!', icon="warning", message='Вы уверены, что хотите опору вставить по середине стержня?')
            self.entr.obstacle_check.deselect()
            return

        if number_node in Nodestable.dict_items.keys():
            Nodestable.dict_items[number_node] = (force, check_block)
            if number_node <= Nodestable.count:
                self.clear_table()
                self.fill_table()
            else:
                self.tbl.table_tree.delete(number_node)
                self.tbl.table_tree.insert('', number_node, iid=int(number_node),
                                           values=(number_node, force, check_block))

        else:
            if number_node > Nodestable.count:
                for i in range(Nodestable.count + 1, number_node):
                    Nodestable.dict_items[i] = (0, 0)
                    self.tbl.table_tree.insert('', i, values=(i, 0, 0))

            Nodestable.dict_items[number_node] = (force, check_block)
            self.tbl.table_tree.insert('', number_node, values=(number_node, force, check_block))

        Nodestable.count = len(Nodestable.dict_items)
        self.set_vals_on_center()

    def set_vals_on_center(self):
        for col in self.colums:
            self.tbl.table_tree.column(col, anchor=ctk.CENTER)

    def delete_node(self, event):
        if Nodestable.count == 0:
            CTkMessagebox(title='Ошибка', message='В таблице не осталось заполненных полей')
            return

        number_to_del = ctk.CTkInputDialog(text='Введите № узла:' ,title="Удаление узла").get_input()
        number_to_del = int(number_to_del)
        if number_to_del not in Nodestable.dict_items:
            CTkMessagebox(title='Warning Message!', icon="warning", message='Вы пытаетесь удалить узел, которого '
                                          'не существует')
            return

        self.clear_table()

        Nodestable.dict_items.pop(number_to_del)
        Nodestable.count -= 1
        for item in Nodestable.dict_items:
            if item > number_to_del:
                Nodestable.dict_items[item - 1] = (Nodestable.dict_items[item][0],
                                                   Nodestable.dict_items[item][1])
                Nodestable.dict_items.pop(item)

        self.fill_table()

    def clear_table(self):
        self.tbl.table_tree.delete(*self.tbl.table_tree.get_children())

    def fill_table(self):
        for key in sorted(Nodestable.dict_items):
            val1, val2 = Nodestable.dict_items[key]
            self.tbl.table_tree.insert('', ctk.END, iid=key, values=(key, val1, val2))

    def on_select(self,event):
        # Получить данные из строки, которая сейчас в фокусе:
        cur_item = self.tbl.table_tree.item(self.tbl.table_tree.focus())

        # Определить номер текущей колонки по положению указателя мыши:
        col = self.tbl.table_tree.identify_column(event.x)

        print('cur_item =', cur_item)  #То что нам нужно. Значения всех ячеек
        self.clear_entry()
        self.entr.numb_entry.insert(0, str(cur_item['values'][0]))
        self.entr.force_entrys.insert(0, str(cur_item['values'][1]))
        if (int(cur_item['values'][2]) == 1):
            self.entr.obstacle_check.select()
        # print('col =', col)
        #
        # if col == '#0':  # Колонка дерева
        #     cell_value = cur_item['text']
        # else:  # Колонки значений
        #     # Номер колонки приходит в виде #2, отрезаем # в начале, приводим к целому числу
        #     index = int(col[1:]) - 1
        #     cell_value = cur_item['values'][index]
        #
        # print('cell_value =', cell_value)

    def clear_entry(self):
        self.entr.numb_entry.delete(0, 'end')
        self.entr.force_entrys.delete(0, 'end')
        self.entr.obstacle_check.deselect()

    def setter_nodes(self):
        Nodestable.count = len(Nodestable.dict_items)
        self.clear_table()

        self.fill_table()

        self.set_vals_on_center()

    def save_all(self, event):
        if rod.Rodstable.dict_items:
            if len(Nodestable.dict_items) - len(rod.Rodstable.dict_items) != 1:
                CTkMessagebox(title='Error', icon="cancel", message='Кол-во узлов должно быть на единицу больше кол-ва стержней')
                self.tbl.table_tree.delete(Nodestable.count)
                Nodestable.dict_items.pop(Nodestable.count)
                Nodestable.count -= 1
            else:
                save_nodes(Nodestable.dict_items)
        else:
            save_nodes(Nodestable.dict_items)