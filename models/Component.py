# models/Component.py
#
# Se crea el componente teniendo campos obligatorios y campos opcionales
#
from datetime import datetime

class Component:
    def __init__(
        self,
        id: str,
        nombre: str,
        categoria: str,
        cantidad_total: int,
        ubicacion: str,
        datasheet_url: str = "",
        proyectos: dict | None = None,
        ultima_compra: dict | None = None,
        historial: list | None = None,
        agotado: bool = False,
        ultima_modificacion: str | None = None
    ):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad_total = cantidad_total
        self.ubicacion = ubicacion
        self.datasheet_url = datasheet_url
        self.proyectos = proyectos or {}
        self.ultima_compra = ultima_compra
        self.historial = historial or []
        self.agotado = agotado
        self.ultima_modificacion = (
            ultima_modificacion or datetime.now().isoformat(timespec="minutes")
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "cantidad_total": self.cantidad_total,
            "ubicacion": self.ubicacion,
            "datasheet_url": self.datasheet_url,
            "proyectos": self.proyectos,
            "ultima_compra": self.ultima_compra,
            "historial": self.historial,
            "ultima_modificacion": self.ultima_modificacion,
            "agotado": self.agotado,
        }