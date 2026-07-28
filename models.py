#models.py
#Módulo encargado de la capa de datos y la lógica de negocio

import json
from pathlib import Path
from typing import List, Dict, Optional

class Ticket:
 # Representa una entidad individual de Ticket de soporte

  def __init__(self, ticket_id: int, usuario: str, descripcion: str,
                categoria: str, prioridad: str, estado: str = "Pendiente"):
     self.id = ticket_id
     self.usuario = usuario
     self.descripcion = descripcion
     self.categoria = categoria
     self.prioridad = prioridad
     self.estado = estado

  def to_dict(self) -> Dict:
    """ Serializa el objeto a diccionario para guardalo en JSON"""
    return{
      "Id":self.id,
      "Usuario": self.usuarios,
      "descripcion": self.descripcion,
      "categoria": self.categoria,
      "prioridad": self.prioridad,
      "estado": self.estado
    }  

  @classmethod
  def from_dict(cls, data: Dict) -> 'Ticket':
    """Deserializa un diccionario JSON en un objeto Ticket"""
    return cls(
       Ticket_id = data["id"],
       usuario = data["usuario"],
       descripcion = data["descripcion"],
       categoria=data["categoria"],
       prioridad = data["prioridad"],
       estado = data.get("Estado", "Pendiente")

    )


class TicketManager:
 #gestor encargado del CRUD y la persistencia en el archivo JSON

   def __init__(self, filepath: str= "tickets.json"):
     self. filepath = Path(filepath)
     self.tickets: list[Ticket] = []
     self.cargar_datos()

   def cargar_datos(self) -> None:  
     #Cargar los tickets desde el archivo JSON si exite
     if not self.filepath.exists():
        self.tickets = []
        return
     try:
       with open(self.filepath, "r", encoding="utf-8") as file:
                 data= json.load(file)
                 self.tickets = [Ticket.from_dict(item) for item in data]
                 
     except(json.JSONDecodeError, KeyError):
        self.tickets=[]

   def guardar_datos(self) -> None:
      """Persiste la lista actual de tickets en el archivo JSON"""
      try:
         with open(self.filepath, "w", encoding="utf-8") as file:
            data = [ticket.to_dict() for ticket in self.tickets]
            json.dump(data, file, indent=4, ensure_ascii=False)
      except IOError as e:
         raise Exception(f"Error al escribir en el disco: {e}")

   def crear_ticket(self, usuario: str, descripcion: str, categoria: str, prioridad:str) -> Ticket:
      """Genera un nuevo ticket con ID autoincremental y lo guarda"""
      nuevo_id = 1 if not self.tickets else max(t.id for t in self.tickets)+1
      nuevo_ticket = Ticket(
             ticket_id=nuevo_id,
             usuario=usuario,
             descripcion=descripcion,
             categoria=categoria,
             prioridad=prioridad 
      )
      self.tickets.append(nuevo_ticket)
      self.guardar_datos()
      return nuevo_ticket

   def cambiar_estado(self, ticket_id: int) -> Optional[Ticket]:
      """Alterna el estado del ticket entre Pendiente y Resuelto"""
      ticket = self.obtener_por_id(ticket_id)
      if ticket:
         ticket.estado = "Resuelto" if ticket.estado =="Pendiente" else "Pendiente"
         self.guardar_datos()
         return ticket
      return None  


   def eliminar_ticket(self, ticket_id: int) -> bool:
      """ELiminar un ticket por su ID"""
      ticket = self.obtener_por_id(ticket_id)
      if ticket:
         self.tickets.remove(ticket)
         self-self.guardar_datos()
         return True
      return False

   def obtener_por_id(self, ticket_id: int) -> Optional[Ticket]:
      """Buscar y retorna un ticket especifico"""
      for ticket in self.tickets:
         if ticket.id == ticket_id:
            return ticket
      return None

   def buscar_tickets(self, criterio: str = "") -> List[Ticket]:
      """Filtrar los tickets por cualquier campo coincidente"""
      if not criterio:
         return self.tickets
      criterio_lower = criterio.lower()
      return [
         t for t in self.tickets
         if criterio_lower in f"{t.usuario} {t.descripcion} {t.categoria} {t.prioridad} {t.estado}".lower()
      ]        


   def obtener_metrica(self) -> Dict[str, int]:
      """Retornar estadisticas clave del conjunto de datos para finalizar el cambio hola """


   
   
