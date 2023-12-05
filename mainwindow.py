import customtkinter
from innerframe import Innerframe
from constraction import Construction

class PreprocessorWin(customtkinter.CTk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title("SAPR")
        self.geometry("810x480")
        self.grid_columnconfigure((0, 1), weight=1)

        # self.master.nametowidget('Окно препроцессора')
        self.make_widgets()

    def make_widgets(self):
        con = Construction(self)
        con.pack(side=customtkinter.LEFT)
        innframe = Innerframe(self, con)
        innframe.pack(side=customtkinter.RIGHT)
        # PreprocessorMenu(self.parent, innframe,con)

if __name__ == '__main__':

    print("SAPR starts...")
    app = PreprocessorWin()
    app.mainloop()
    # root.title("SAPR")
    # MainWindow(root)
    # root.mainloop()