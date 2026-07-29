import json
import os
from datetime import datetime
from typing import List, Optional, Dict

class Ticket:
    """Clase que representa un ticket de soporte"""
    def __init__(self, id: int, usuario: str, descripcion: str, 
                 categoria: str, prioridad: str, estado: str = "Pendiente"):
        self.id = id
        self.usuario = usuario
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.estado = estado
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Convierte el ticket a diccionario para JSON"""
        return {
            "id": self.id,
            "usuario": self.usuario,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un ticket desde un diccionario"""
        ticket = cls(
            id=data["id"],
            usuario=data["usuario"],
            descripcion=data["descripcion"],
            categoria=data["categoria"],
            prioridad=data["prioridad"],
            estado=data.get("estado", "Pendiente")
        )
        ticket.fecha_creacion = data.get("fecha_creacion", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return ticket

class TicketManager:
    """Gestiona la creación, almacenamiento y búsqueda de tickets"""
    def __init__(self, archivo_json: str = "tickets.json"):
        self.archivo_json = archivo_json
        self.tickets: List[Ticket] = []
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los tickets desde el archivo JSON"""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tickets = [Ticket.from_dict(t) for t in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.tickets = []
        else:
            self.tickets = []
    
    def _guardar_datos(self):
        """Guarda los tickets en el archivo JSON"""
        with open(self.archivo_json, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tickets], f, indent=2, ensure_ascii=False)
    
    def _generar_id(self) -> int:
        """Genera un nuevo ID para el ticket"""
        if not self.tickets:
            return 1
        return max(t.id for t in self.tickets) + 1
    
    def crear_ticket(self, usuario: str, descripcion: str, 
                     categoria: str, prioridad: str) -> Ticket:
        """Crea un nuevo ticket"""
        ticket = Ticket(
            id=self._generar_id(),
            usuario=usuario,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            estado="Pendiente"
        )
        self.tickets.append(ticket)
        self._guardar_datos()
        return ticket
    
    def cambiar_estado(self, ticket_id: int) -> bool:
        """Cambia el estado de un ticket (Pendiente -> Resuelto)"""
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                if ticket.estado == "Pendiente":
                    ticket.estado = "Resuelto"
                else:
                    ticket.estado = "Pendiente"
                self._guardar_datos()
                return True
        return False
    
    def eliminar_ticket(self, ticket_id: int) -> bool:
        """Elimina un ticket por su ID"""
        for i, ticket in enumerate(self.tickets):
            if ticket.id == ticket_id:
                del self.tickets[i]
                self._guardar_datos()
                return True
        return False
    
    def buscar_tickets(self, criterio: str = "") -> List[Ticket]:
        """Busca tickets que coincidan con el criterio"""
        if not criterio:
            return self.tickets.copy()
        
        criterio_lower = criterio.lower()
        resultados = []
        for ticket in self.tickets:
            if (criterio_lower in ticket.usuario.lower() or
                criterio_lower in ticket.descripcion.lower() or
                criterio_lower in ticket.categoria.lower() or
                criterio_lower in ticket.estado.lower()):
                resultados.append(ticket)
        return resultados
    
    def obtener_metricas(self) -> Dict[str, int]:
        """Obtiene métricas de los tickets"""
        total = len(self.tickets)
        pendientes = sum(1 for t in self.tickets if t.estado == "Pendiente")
        resueltos = sum(1 for t in self.tickets if t.estado == "Resuelto")
        return {
            "total": total,
            "pendientes": pendientes,
            "resueltos": resueltos
        }