# services/Component_Service.py
from datetime import datetime
from models.Component import Component

class ComponentService:
    def __init__(self, storage):
        self.storage = storage

    def _now(self):
        return datetime.now().isoformat(timespec="minutes")

    def get_all(self) -> list[Component]:
        data = self.storage.load()
        return [
            Component.from_dict(c)
            for c in data["componentes"].values()
        ]

    def get(self, component_id: str) -> Component | None:
        data = self.storage.load()
        comp = data["componentes"].get(component_id)
        return Component.from_dict(comp) if comp else None

    # ---------- ACCIONES DE NEGOCIO ----------

    def usar(self, component_id: str, cantidad: int, proyecto: str):
        data = self.storage.load()
        comp = data["componentes"].get(component_id)

        if not comp:
            raise ValueError("Componente no existe")

        if cantidad <= 0:
            raise ValueError("Cantidad inválida")

        if comp["cantidad_total"] < cantidad:
            raise ValueError("Stock insuficiente")

        # stock
        comp["cantidad_total"] -= cantidad
        comp["agotado"] = comp["cantidad_total"] == 0

        # proyectos
        comp["proyectos"][proyecto] = (
            comp["proyectos"].get(proyecto, 0) + cantidad
        )

        # historial
        comp["historial"].append({
            "fecha": self._now(),
            "accion": "uso",
            "cantidad": -cantidad,
            "proyecto": proyecto
        })

        # metadata del componente
        comp["ultima_modificacion"] = self._now()

        self.storage.save(data)

    def comprar(self, component_id: str, cantidad: int, precio: float, proveedor: str):
        data = self.storage.load()
        comp = data["componentes"].get(component_id)

        if not comp:
            raise ValueError("Componente no existe")

        if cantidad <= 0:
            raise ValueError("Cantidad inválida")

        # stock
        comp["cantidad_total"] += cantidad
        comp["agotado"] = False

        # ultima compra
        comp["ultima_compra"] = {
            "fecha": self._now().split("T")[0],
            "precio_unitario": precio,
            "cantidad": cantidad,
            "proveedor": proveedor
        }

        # historial
        comp["historial"].append({
            "fecha": self._now(),
            "accion": "compra",
            "cantidad": cantidad,
            "precio_unitario": precio
        })

        comp["ultima_modificacion"] = self._now()

        self.storage.save(data)

# ------------ Modificaciones de campos ---------------

    def editar_campos(self, component_id: str, nombre: str = None,
                        categoria: str = None, ubicacion: str = None,
                        datasheet_url: str = None):
            """
            Modifica los campos de un componente que no sean cantidad.
            """
            data = self.storage.load()
            comp = data["componentes"].get(component_id)

            if not comp:
                raise ValueError(f"Componente '{component_id}' no existe")

            # Actualizar campos si se pasan valores
            if nombre is not None:
                comp["nombre"] = nombre.strip()
            if categoria is not None:
                comp["categoria"] = categoria.strip()
            if ubicacion is not None:
                comp["ubicacion"] = ubicacion.strip()
            if datasheet_url is not None:
                comp["datasheet_url"] = datasheet_url.strip()

            # Actualizar metadata
            comp["ultima_modificacion"] = self._now()

            # Guardar cambios
            self.storage.save(data)