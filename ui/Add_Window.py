import tkinter as tk
from ui.Component_Dialog import info, show_popup
from storage.Storage_JSON import StorageJSON
from models.Component import Component

def agregar_componente(self):
            # Crear la ventana emergente
            popup = tk.Toplevel(self)
            popup.title("Agregar Componente")
            popup.geometry("400x450")
            popup.configure(bg="#333333")
        
            # Cargar JSON para obtener categorías existentes
            storage = StorageJSON("Componentes.json")
            json_data = storage.load()
            categorias_existentes = list({comp["categoria"] for comp in json_data["componentes"].values()})
            if not categorias_existentes:
                categorias_existentes = ["Sin Categoría"]
        
            # Campos del formulario
            fields = ["ID", "Nombre", "Categoría", "Cantidad Total", "Ubicación", "Datasheet URL"]
            inputs = {}
        
            for i, field in enumerate(fields):
                label = tk.Label(popup, text=field, bg="#333333", fg="white")
                label.place(x=20, y=20 + i*50)
        
                if field == "Categoría":
                    var_categoria = tk.StringVar(popup)
                    var_categoria.set(categorias_existentes[0])
                    dropdown = tk.OptionMenu(popup, var_categoria, *categorias_existentes)
                    dropdown.config(width=27, bg="white")
                    dropdown.place(x=150, y=20 + i*50)
                    inputs[field] = var_categoria
                else:
                    entry = tk.Entry(popup, width=30)
                    entry.place(x=150, y=20 + i*50)
                    inputs[field] = entry
        
            # Función para cerrar el popup
            def back():
                popup.destroy()
        
            # Función para mostrar un popup de información
            def show_popup(message: str):
                popup_msg = tk.Toplevel(self)
                popup_msg.title("Información")
                popup_msg.geometry("300x100")
                popup_msg.configure(bg="#333333")
                label = tk.Label(popup_msg, text=message, bg="#333333", fg="white", font=("Arial", 12))
                label.pack(expand=True, pady=20)
                btn = tk.Button(popup_msg, text="Cerrar", bg="green", fg="white", command=popup_msg.destroy)
                btn.pack(pady=5)
        
            # Función para guardar el componente
            def guardar():
                data_input = {field: entrada.get() if not isinstance(entrada, tk.StringVar) else entrada.get()
                              for field, entrada in inputs.items()}
        
                if not data_input["ID"] or not data_input["Nombre"]:
                    show_popup("ID y Nombre son obligatorios!")
                    return
        
                # Crear objeto Component
                comp = Component(
                    id=data_input["ID"],
                    nombre=data_input["Nombre"],
                    categoria=data_input["Categoría"],
                    cantidad_total=int(data_input.get("Cantidad Total") or 0),
                    ubicacion=data_input.get("Ubicación") or "",
                    datasheet_url=data_input.get("Datasheet URL") or ""
                )
        
                # Guardar en JSON (reemplaza si ya existe)
                json_data["componentes"][comp.id] = comp.to_dict()
                storage.save(json_data)
        
                show_popup(f"Componente '{comp.nombre}' agregado!")
                popup.destroy()
        
            # Botones
            button_save = tk.Button(popup, text="Guardar", bg="green", fg="white", command=guardar)
            button_save.place(x=80, y=380)
        
            button_back = tk.Button(popup, text="Atras", bg="red", fg="white", command=back)
            button_back.place(x=180, y=380)