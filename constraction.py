import customtkinter as ctk
from rod import Rodstable
from node import Nodestable

class Construction(ctk.CTkFrame):
    middle = int()

    def __init__(self,parent):
        super().__init__(parent)
        self.pack()
        self.cv = ctk.CTkCanvas(self, width=640, height=425, bg='white')
        self.cv.config(scrollregion=(0, 0, 3000, 500))

        self.sbar = ctk.CTkScrollbar(self, orientation=ctk.HORIZONTAL)
        self.ybar = ctk.CTkScrollbar(self, orientation=ctk.VERTICAL)
        self.sbar.pack(side=ctk.BOTTOM, fill=ctk.X, expand=ctk.YES)
        self.ybar.pack(side=ctk.LEFT, fill=ctk.Y, expand=ctk.YES)
        self.sbar.configure(command=self.cv.xview)
        self.ybar.configure(command=self.cv.yview)
        self.cv.configure(xscrollcommand=self.sbar.set)
        self.cv.configure(yscrollcommand=self.ybar.set)
        self.cv.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.YES)

        self.cv.bind("<1>", lambda event: self.cv.focus_set())
        self.cv.bind("<Left>", lambda event: self.cv.xview_scroll(-1, "units"))
        self.cv.bind("<Right>", lambda event: self.cv.xview_scroll(1, "units"))
        self.cv.bind("<Up>", lambda event: self.cv.yview_scroll(-1, "units"))
        self.cv.bind("<Down>", lambda event: self.cv.yview_scroll(1, "units"))
        self.cv.bind("<MouseWheel>", self._on_mousewheel)
        self.cv.bind('<Shift-MouseWheel>', self.scrollHorizontally)

        self.nodes_coord = []
        self.rods = Rodstable.dict_items
        self.nodes = Nodestable.dict_items
        self.l_list = []


        # self.draw_btn = ctk.CTkButton(self, text="Отрисовка")
        # self.draw_btn.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.YES)
        #
        # self.draw_btn.bind('<Button-1>', self.draw)

    def _on_mousewheel(self, event):
        self.cv.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scrollHorizontally(self, event):
        self.cv.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def draw(self, event):
        if self.cv.find_all():
            self.clear_all()

        begin_x = 50
        begin_y = 240
        one_a = 50
        h = int()
        for item in self.rods:
            l = 100 * self.rods[item][0]
            h = self.rods[item][1] * one_a

            if item == 1:
                Construction.middle = begin_y + h / 2
            if item >= 2:
                begin_y = Construction.middle - (h / 2)

            self.nodes_coord.append([begin_x, begin_y, h])
            self.l_list.append(l)

            self.cv.create_rectangle(begin_x, begin_y, begin_x + l, begin_y + h, tags='drawing')

            begin_x += l

        self.nodes_coord.append([begin_x, begin_y, h])

        for val in self.nodes:
            if self.nodes[val][1] != 0:
                self.draw_block(val)

    #отрисовка распределенной силы
    def draw_q_force(self):
        for val in self.rods:
            if self.rods[val][-1] != 0:
                value = self.rods[val][-1]
                x = self.nodes_coord[val - 1][0]
                end_x = x + self.l_list[val - 1]
                while x <= end_x:
                    if x + 20 < end_x:
                        if value > 0:
                            self.cv.create_line(x, Construction.middle, x + 20, Construction.middle, arrow=ctk.LAST,
                                                tags='q', fill="red")
                        else:
                            self.cv.create_line(x, Construction.middle, x + 20, Construction.middle, arrow=ctk.FIRST,
                                                tags='q', fill="red")
                    else:
                        adder = end_x - x
                        if value > 0:
                            self.cv.create_line(x, Construction.middle, x + adder, Construction.middle, arrow=ctk.LAST,
                                                tags='q', fill="red")
                        else:
                            self.cv.create_line(x, Construction.middle, x + adder, Construction.middle, arrow=ctk.FIRST,
                                                tags='q', fill="red")
                    x += 20

                begin_x = self.nodes_coord[val - 1][0]
                begin_y = self.nodes_coord[val - 1][1]
                begin_x += self.l_list[val - 1] / 4
                self.cv.create_line(begin_x, Construction.middle, begin_x + 20, begin_y - 30, tags='q')
                begin_x += 20
                begin_y -= 30
                self.cv.create_line(begin_x, begin_y, begin_x + 20, begin_y, tags='q')

                self.cv.create_text(begin_x + 10, begin_y - 10, text='%sq' % abs(value), tags='q')


    # отображение силы точечной
    def draw_force(self):
        for val in self.nodes:
            if self.nodes[val][0] != 0:
                draw_value = self.nodes[val][0]
                x = self.nodes_coord[val - 1][0]
                y = Construction.middle
                if draw_value > 0:
                    self.cv.create_line(x, y, x + 50, y, arrow=ctk.LAST, tags='force', fill="blue", width= 5)
                    self.cv.create_text(x + 25, y - 12, text='F%s = %s' % (val, draw_value), tags='force')
                else:
                    self.cv.create_line(x, y, x - 50, y, arrow=ctk.LAST, tags='force', fill="blue", width= 5)
                    self.cv.create_text(x - 25, y - 12, text='F%s = %s' % (val, abs(draw_value)), tags='force')

    #отрисовка блоков
    def draw_block(self, numb_node):
        x, y, shift = self.nodes_coord[numb_node - 1]
        if not isinstance(y, int):
            y = int(y)
        if not isinstance(shift, int):
            shift = int(shift)

        end = y + shift + 10
        self.cv.create_line(x, y - 10, x, end, tags='drawing')
        if numb_node == 1:
            for i in range(y - 10, end, 5):
                self.cv.create_line(x, i, x - 5, i + 5, tags='drawing')
        else:
            for i in range(end, y - 10, -5):
                self.cv.create_line(x, i, x + 5, i - 5, tags='drawing')

    def clear_all(self):
        self.cv.delete('drawing')
        self.cv.delete('force')
        self.cv.delete('rod_numb')
        self.cv.delete('node_numb')
        self.cv.delete('other')
        self.cv.delete('axes')
        self.cv.delete('q')
        self.nodes_coord = []
        self.l_list = []