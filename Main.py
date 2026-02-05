# Main.py
import sys
from pathlib import Path

# Añadir la carpeta raíz al path para poder importar paquetes correctamente
sys.path.append(str(Path(__file__).resolve().parent))

from ui.Main_Window import MainWindow

def main():
    app = MainWindow()
    app.configure(bg="gray10")  # fondo de la ventana
    app.mainloop()

if __name__ == "__main__":
    main()