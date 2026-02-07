import tkinter as tk
from tkinter import ttk
from ui.Component_Dialog import info, show_popup
from storage.Storage_JSON import StorageJSON
from services.Component_Service import ComponentService


def search_component(self):
            popup = tk.Toplevel(self)
            popup.title("Buscar Componente")
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
            categorias = ["", "Resistencias", "Condensadores", "Diodos", "Transistores"]  # Ejemplo
            combo_categoria = ttk.Combobox(popup, values=categorias, state="readonly")
            combo_categoria.place(x=150, y=100)

            # Treeview para resultados
            columns = ("ID", "Nombre", "Categoría", "Cantidad", "Ubicación")
            result_tree = ttk.Treeview(popup, columns=columns, show="headings", height=15)
            for col in columns:
                result_tree.heading(col, text=col)
                result_tree.column(col, width=100)
            result_tree.place(x=20, y=150)

            encontrados = []  # Lista global dentro de la función para vincular selección

            # Función para mostrar detalles en popup
            def show_details(event):
                selection = result_tree.selection()
                if not selection:
                    return
                index = int(selection[0])  # id del item en Treeview coincide con índice en lista
                c = encontrados[index]

                detail_popup = tk.Toplevel(popup)
                detail_popup.title(f"Detalles de {c.nombre}")
                detail_popup.geometry("700x800")
                detail_popup.configure(bg="#333333")

                def info(popup, texto, x, y, tamaño=12, color="white"):
                    label = tk.Label(popup, text=texto, bg="#333333", fg=color, font=("Arial", tamaño))
                    label.place(x=x, y=y)

                y = 20  # posición inicial

                # Campos básicos
                if c.id: 
                    info(detail_popup, "ID:", 20, y, color="red")
                    info(detail_popup, f" {c.id}", 60, y, color="white")
                    y += 30
                if c.nombre: 
                    info(detail_popup, "Nombre:", 20, y, color="red")
                    info(detail_popup, f" {c.nombre}", 90, y, color="white")
                    y += 30
                if c.categoria: 
                    info(detail_popup, "Categoria:", 20, y, color="red")
                    info(detail_popup, f" {c.categoria}", 100, y, color="white")
                    y += 30
                if c.cantidad_total: 
                    info(detail_popup, "Cantidad:", 20, y, color="red")
                    info(detail_popup, f" {c.cantidad_total}", 100, y, color="white")
                    y += 30
                if c.ubicacion:
                    info(detail_popup, "Ubicacion:", 20, y, color="red")
                    info(detail_popup, f" {c.ubicacion}", 100, y, color="white")
                    y += 30
                if c.datasheet_url: 
                    info(detail_popup, "Datasheet:", 20, y, color="red")
                    info(detail_popup, f" {c.datasheet_url}", 100, y, color="white")
                    y += 30

                # Proyectos
                if c.proyectos:
                    info(detail_popup, "Proyectos:", 20, y, color="red")
                    y += 30
                    for p, qty in c.proyectos.items():
                        if qty:  # solo mostrar si hay cantidad
                            info(detail_popup, f"{p}: {qty}", 40, y)
                            y += 30

                # Última compra
                if c.ultima_compra:
                    info(detail_popup, "Ultima Compra:", 20, y, color="red")
                    y += 30
                    compra = c.ultima_compra
                    if compra.get('fecha'): 
                        info(detail_popup, f"Fecha: {compra['fecha']}", 40, y)
                        y += 30
                    if compra.get('precio_unitario'): 
                        info(detail_popup, f"Precio unitario: {compra['precio_unitario']}", 40, y)
                        y += 30
                    if compra.get('cantidad'): 
                        info(detail_popup, f"Cantidad: {compra['cantidad']}", 40, y)
                        y += 30
                    if compra.get('proveedor'): 
                        info(detail_popup, f"Proveedor: {compra['proveedor']}", 40, y)
                        y += 30

                # Historial (últimos 5)
                if c.historial:
                    info(detail_popup, "Historial:", 20, y, color="red")
                    y += 30
                    for h in c.historial[-5:]:
                        texto_hist = " - ".join(str(h.get(k, "")) for k in ['fecha','accion','cantidad','proyecto'] if h.get(k))
                        if texto_hist:  # solo mostrar si hay datos
                            info(detail_popup, texto_hist, 40, y)
                            y += 30

                tk.Button(detail_popup, text="Terminar", bg="green", fg="white", command=detail_popup.destroy).place(x=600, y=750)

            result_tree.bind("<Double-1>", show_details)

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
                    tk.messagebox.showinfo("Búsqueda", "No se encontraron componentes.")

            def back():
                popup.destroy()

            button_search = tk.Button(popup, text="Buscar", bg="green", fg="white", command=search)
            button_search.place(x=80, y=550)

            button_back = tk.Button(popup, text="Atras", bg="red", fg="white", command=back)
            button_back.place(x=180, y=550)