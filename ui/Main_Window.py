# ui/Main_Window.py
import tkinter as tk
from ui.Component_Dialog import info, show_popup
from ui.Add_Window import agregar_componente
from ui.Search_Window import search_component
from ui.Delete_Window import delete_component

WIDTH = 800
HEIGHT = 600

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Composerch - Gestión de Componentes")
        self.geometry(f"{WIDTH}x{HEIGHT}")


        # ========== Buttons ==========

        button = tk.Button(self, text="AGREGAR", width=20, bg="green", fg="white", command=lambda: agregar_componente(self))
        button.place(x=330 , y=100)

        button = tk.Button(self, text="BUSCAR", width=20, bg="blue", fg="white", command=lambda: search_component(self))
        button.place(x=330 , y=150)

        button = tk.Button(self, text="MODIFICAR", width=20, bg="darkorange", fg="white")
        button.place(x=330 , y=200)

        button = tk.Button(self, text="ELIMINAR", width=20, bg="red", fg="white", command=lambda: delete_component(self))
        button.place(x=330 , y=250)

        button = tk.Button(self, text="INFO", width=20, bg="black", fg="white")
        button.place(x=330 , y=300)

        button = tk.Button(self, text="CONTACTAR", width=20, bg="black", fg="white")
        button.place(x=330 , y=350)

        button = tk.Button(self, text="SALIR", width=20, bg="red", fg="white", command= self.destroy)
        button.place(x=330 , y=450)

        # ========== Text ==========

        info(self, "Bienvenido a la aplicacion de organización de componentes", 200, 50, 12)

        info(self, "Autor:",20, 500, 12)
        info(self, "Luis Miguel Carmona Cortés", 20, 525, 15)

        info(self, "Version:",700, 500, 12)
        info(self, "V1.0", 700, 525, 15)

if __name__ == "__main__":
    app = MainWindow()
    app.configure(bg="gray10")
    app.mainloop()