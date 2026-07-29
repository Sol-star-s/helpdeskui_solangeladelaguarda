import tkinter as tk
from models import TicketManager
from views import HelpdeskUI

def main():
    # 1. Instancia el gestor de datos (BACKEND/model)
    manager = TicketManager("tickets.json")
    
    # 2. Inicializar tkinter
    root = tk.Tk()
    
    # 3. Inyectar el modelo en la interfaz (inyección de dependencias)
    app = HelpdeskUI(root, manager)
    
    # 4. Iniciar el bucle de eventos
    root.mainloop()

if __name__ == "__main__":
    main()