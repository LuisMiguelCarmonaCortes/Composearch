#ui/Component_Dialog.py
import tkinter as tk

def info(self, text, posx, posy, tam):
    label = tk.Label(self, text=text, bg="gray10", fg="white", font=("Arial", tam))
    label.place(x=posx, y=posy)

def show_popup(self, message: str):
    popup_msg = tk.Toplevel(self)
    popup_msg.title("Información")
    popup_msg.geometry("500x100")
    popup_msg.configure(bg="#333333")

    label = tk.Label(popup_msg, text=message, bg="#333333", fg="white", font=("Arial", 10))
    label.pack(expand=True, pady=20)

    # Botón para cerrar
    btn = tk.Button(popup_msg, text="Cerrar", bg="green", fg="white", command=popup_msg.destroy)
    btn.pack(pady=5)