import logging
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from saveData import get_data, save_data
from rod import Rodstable
from node import Nodestable
from constraction import Construction
INNERFRAME_WIDTH = 640
INNERFRAME_HEIGHT = 120

class Innerframe(ctk.CTkFrame):

        def __init__(self, master,frame):
            super().__init__(master)
            self.const = frame
            self.make_widgets()

        def make_widgets(self):
            self.rods_btn = ctk.CTkButton(self, text="Открыть файл",
                                          command=self.open_file)
            self.rods_btn.pack(side=ctk.TOP, expand="YES", fill="both", ipady=10, pady=8)
            self.rods_btn = ctk.CTkButton(self, text="Сохранить файл",
                                          command=self.save_file)
            self.rods_btn.pack(side=ctk.TOP, expand="YES", fill="both", ipady=10, pady=8)
            self.rods_btn = ctk.CTkButton(self, text="Параметры стержней",
                                       command=self.open_rods_win)
            self.rods_btn.pack(side=ctk.TOP, expand="YES", fill="both" , ipady=10, pady=8)
            self.nodes_btn = ctk.CTkButton(self, text="Параметры узлов",
                                        command=self.open_nodes_win)
            self.nodes_btn.pack(side=ctk.TOP, expand="YES", fill="both" , ipady=10, pady=8)

            self.show = ctk.CTkButton(self, text="Отрисовка",
                                           command=self.show_draw)
            self.show.pack(side=ctk.TOP, expand="YES", fill="both", ipady=10, pady=8)

        def open_rods_win(self):
            logging.info("Ddetected pushing into rod button")
            self.rod = Rodstable(self)
            self.rod.focus()

        def open_nodes_win(self):
            logging.info("Ddetected pushing into Nodes button")
            self.node = Nodestable(self)
            self.node.focus()


        def show_draw(self):
            self.const.draw(1)
            if not self.const.cv.gettags('q'):
                self.const.draw_q_force()
            else:
                self.const.cv.delete('q')
            if not self.const.cv.gettags('force'):
                self.const.draw_force()
            else:
                self.const.cv.delete('force')

        def open_file(self):
            filename = askopenfilename(parent=self, defaultextension='.db', filetypes=[('Database', '.db'),
                                                                                       ('SQLite3', '.sqlite3'),
                                                                                       ('SQLite', '.sqlite')], initialdir='C:/Users/Samson/OneDrive/Документы/sapr')
            save_filename = open('C:/Users/Samson/OneDrive/Документы/sapr/filepath.txt', 'w')
            save_filename.write(filename)

            rods, nodes = get_data(filename)

            Rodstable.fill_dict(rods)
            Nodestable.set_dict(nodes)
            self.show_draw()
        def save_file(self):
            filename = asksaveasfilename(parent=self, defaultextension='.db', filetypes=[('Database', '.db'),
                                                                                       ('SQLite3', '.sqlite3'),
                                                                                       ('SQLite', '.sqlite')],
                                       initialdir='C:/Users/Samson/OneDrive/Документы/sapr')

            save_filename = open('C:/Users/Samson/OneDrive/Документы/sapr/filepath.txt', 'w')
            save_filename.write(filename)

            rods = Rodstable.get_data_about_rods()
            nodes = Nodestable.get_data_about_nodes()
            save_data(filename, rods, nodes)