# storage/Storage_JSON.py
import json
from datetime import datetime
from pathlib import Path

class StorageJSON:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> dict:
        if not self.file_path.exists():
            return {
                "metadata": {
                    "version": "1.0",
                    "ultima_actualizacion": None
                },
                "componentes": {}
            }

        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict):
        data["metadata"]["ultima_actualizacion"] = (
            datetime.now().isoformat(timespec="minutes")
        )

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)