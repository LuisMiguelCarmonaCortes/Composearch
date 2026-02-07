import tkinter as tk
from tkinter import ttk, messagebox
from storage.Storage_JSON import StorageJSON
from services.Component_Service import ComponentService


def delete_component(self):
    popup = tk.Toplevel(self)
    popup.title("Eliminar Componente")
    popup.geometry("600x600")
    popup.configure(bg="#333333")

    storage = StorageJSON("Componentes.json")
    service = ComponentService(storage)

    # Campos de búsqueda
    tk.Label(popup, text="ID:", bg="#333333", fg="white").place(x=20, y=20)
    entry_id = tk.Entry(popup, width=30)
    entry_id.place(x=150, y=20)

    tk.Label(popup, text="Nombre:", bg="#333333", fg="white").place(x=20, y=60)
    entry_name = tk.Entry(popup, width=30)
    entry_name.place(x=150, y=60)

    tk.Label(popup, text="Categoría:", bg="#333333", fg="white").place(x=20, y=100)
    categorias = ["", "Resistencias", "Condensadores", "Diodos", "Transistores"]  # ejemplo
    combo_categoria = ttk.Combobox(popup, values=categorias, state="readonly")
    combo_categoria.place(x=150, y=100)

    # Treeview para mostrar resultados
    columns = ("ID", "Nombre", "Categoría", "Cantidad", "Ubicación")
    result_tree = ttk.Treeview(popup, columns=columns, show="headings", height=15)
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, width=100)
    result_tree.place(x=20, y=150)

    encontrados = []

    # Función de búsqueda
    def search():
        result_tree.delete(*result_tree.get_children())
        nonlocal encontrados
        encontrados = []

        id_query = entry_id.get().lower()
        name_query = entry_name.get().lower()
        categoria_query = combo_categoria.get()

        componentes = service.get_all()

        for c in componentes:
            if id_query and not c.id.lower().startswith(id_query):
                continue
            if name_query and name_query not in c.nombre.lower():
                continue
            if categoria_query and c.categoria != categoria_query:
                continue
            index = len(encontrados)
            encontrados.append(c)
            result_tree.insert("", "end", iid=index, values=(c.id, c.nombre, c.categoria, c.cantidad_total, c.ubicacion))

        if not encontrados:
            messagebox.showinfo("Búsqueda", "No se encontraron componentes.")

    # Función para eliminar el componente seleccionado
    def eliminar():
        selection = result_tree.selection()
        if not selection:
            messagebox.showwarning("Eliminar", "Seleccione un componente para eliminar.")
            return
        index = int(selection[0])
        comp = encontrados[index]

        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar '{comp.nombre}'?")
        if not confirm:
            return

        # Eliminar del JSON
        json_data = storage.load()
        if comp.id in json_data["componentes"]:
            del json_data["componentes"][comp.id]
            storage.save(json_data)

        # Actualizar lista y Treeview
        encontrados.pop(index)
        result_tree.delete(selection)
        messagebox.showinfo("Eliminado", f"Componente '{comp.nombre}' eliminado.")

    def back():
        popup.destroy()

    # Botones
    button_search = tk.Button(popup, text="Buscar", bg="green", fg="white", command=search)
    button_search.place(x=80, y=550)

    button_delete = tk.Button(popup, text="Borrar", bg="red", fg="white", command=eliminar)
    button_delete.place(x=180, y=550)

    button_back = tk.Button(popup, text="Atras", bg="blue", fg="white", command=back)
    button_back.place(x=280, y=550)
