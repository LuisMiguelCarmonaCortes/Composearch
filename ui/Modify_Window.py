# ui/Modify_Window.py
import tkinter as tk
from tkinter import ttk, messagebox
from storage.Storage_JSON import StorageJSON
from services.Component_Service import ComponentService
from models.Component import Component

def modify_component(self):
    popup = tk.Toplevel(self)
    popup.title("Modificar Componente")
    popup.geometry("700x650")
    popup.configure(bg="#333333")

    storage = StorageJSON("Componentes.json")
    service = ComponentService(storage)

    # =========================
    # Buscador por ID
    # =========================
    tk.Label(popup, text="Buscar por ID:", bg="#333333", fg="white").place(x=20, y=20)
    entry_search = tk.Entry(popup, width=30)
    entry_search.place(x=150, y=20)

    # Botón de búsqueda
    def search():
        tree.delete(*tree.get_children())
        encontrados.clear()

        query = entry_search.get().lower()
        componentes = service.get_all()

        for c in componentes:
            if query and not c.id.lower().startswith(query):
                continue

            index = len(encontrados)
            encontrados.append(c)

            tree.insert(
                "", "end",
                iid=index,
                values=(c.id, c.nombre, c.categoria, c.cantidad_total, c.ubicacion)
            )

        if not encontrados:
            messagebox.showinfo("Buscar", "No se encontraron componentes.")

    tk.Button(popup, text="Buscar", bg="green", fg="white", command=search).place(x=400, y=18)

    # =========================
    # Treeview de resultados
    # =========================
    columns = ("ID", "Nombre", "Categoría", "Cantidad", "Ubicación")
    tree = ttk.Treeview(popup, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.place(x=20, y=60)

    encontrados = []

    # =========================
    # Formulario edición
    # =========================
    labels = ["Nombre", "Categoría", "Cantidad Total", "Ubicación", "Datasheet URL"]
    inputs = {}

    for i, label in enumerate(labels):
        tk.Label(popup, text=label, bg="#333333", fg="white").place(x=20, y=280 + i * 40)
        entry = tk.Entry(popup, width=40)
        entry.place(x=150, y=280 + i * 40)
        inputs[label] = entry

    selected_component = {"obj": None}

    # =========================
    # Cargar selección desde Treeview
    # =========================
    def load_selected(event):
        selection = tree.selection()
        if not selection:
            return

        index = int(selection[0])
        c = encontrados[index]
        selected_component["obj"] = c

        inputs["Nombre"].delete(0, tk.END)
        inputs["Nombre"].insert(0, c.nombre)

        inputs["Categoría"].delete(0, tk.END)
        inputs["Categoría"].insert(0, c.categoria)

        inputs["Cantidad Total"].delete(0, tk.END)
        inputs["Cantidad Total"].insert(0, c.cantidad_total)

        inputs["Ubicación"].delete(0, tk.END)
        inputs["Ubicación"].insert(0, c.ubicacion)

        inputs["Datasheet URL"].delete(0, tk.END)
        inputs["Datasheet URL"].insert(0, c.datasheet_url)

    tree.bind("<Double-1>", load_selected)

    # =========================
    # Modificar cantidad
    # =========================
    def modificar_cantidad(valor):
        c = selected_component["obj"]
        if not c:
            messagebox.showwarning("Modificar", "Selecciona un componente primero")
            return

        try:
            actual = int(inputs["Cantidad Total"].get())
            nueva = actual + valor
            if nueva < 0:
                messagebox.showwarning("Cantidad", "No puede ser negativa")
                return

            # Calcular delta respecto al valor actual en la variable c.cantidad_total
            delta = nueva - c.cantidad_total

            if delta > 0:
                service.comprar(c.id, delta, precio=0, proveedor="modificación")
            elif delta < 0:
                service.usar(c.id, -delta, proyecto="modificación")

            # Actualizar la variable c.cantidad_total para futuras operaciones
            c.cantidad_total = nueva

            # Reflejar en el Entry
            inputs["Cantidad Total"].delete(0, tk.END)
            inputs["Cantidad Total"].insert(0, nueva)

        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
    # =========================
    # Guardar cambios
    # =========================
    def guardar():
        c = selected_component["obj"]
        if not c:
            messagebox.showwarning("Modificar", "Selecciona un componente primero")
            return

        service.editar_campos(
            component_id=c.id,
            nombre=inputs["Nombre"].get(),
            categoria=inputs["Categoría"].get(),
            ubicacion=inputs["Ubicación"].get(),
            datasheet_url=inputs["Datasheet URL"].get()
        )

        messagebox.showinfo("Modificar", "Componente actualizado correctamente")
        popup.destroy()

    # =========================
    # Botones
    # =========================
    tk.Button(popup, text="+1", bg="green", fg="white", command=lambda: modificar_cantidad(1)).place(x=150, y=500)
    tk.Button(popup, text="-1", bg="orange", fg="white", command=lambda: modificar_cantidad(-1)).place(x=200, y=500)
    tk.Button(popup, text="Guardar", bg="green", fg="white", command=guardar).place(x=80, y=560)
    tk.Button(popup, text="Atrás", bg="red", fg="white", command=popup.destroy).place(x=180, y=560)

    # =========================
    # Botones de modificación de cantidad
    # =========================
    tk.Button(popup, text="+1", bg="green", fg="white", command=lambda: modificar_cantidad(1)).place(x=150, y=500)
    tk.Button(popup, text="-1", bg="orange", fg="white", command=lambda: modificar_cantidad(-1)).place(x=200, y=500)

    # Entry para cantidad personalizada
    tk.Label(popup, text="Cantidad:", bg="#333333", fg="white").place(x=260, y=505)
    entry_cantidad = tk.Entry(popup, width=5)
    entry_cantidad.place(x=320, y=505)

    # Botón Aplicar cantidad personalizada
    def aplicar_cantidad():
        try:
            valor = int(entry_cantidad.get())
            modificar_cantidad(valor)
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido")

    tk.Button(popup, text="Aplicar", bg="blue", fg="white", command=aplicar_cantidad).place(x=380, y=500)