# 🖥️ DataDesk Helpdesk System

**Sistema de Gestión de Tickets de Soporte Técnico**  
Una aplicación de escritorio profesional desarrollada en Python que optimiza la administración de incidencias internas mediante una interfaz gráfica intuitiva y persistencia de datos en JSON.

---

## 📸 Vista Previa

<!-- Reemplaza esta URL con la ruta de tu captura de pantalla o GIF -->
![Vista Principal de DataDesk](./screenshot.png)

> *Ejemplo de la interfaz principal con listado de tickets y panel métrico.*

---

## 🚀 Descripción del Proyecto

**DataDesk** es una solución completa para la gestión de tickets de soporte técnico. Desarrollada con **Python** y **Tkinter**, sigue el patrón de diseño **Separación de Responsabilidades (SoC)** para garantizar un código limpio, mantenible y escalable.

### ✅ Funcionalidades Clave

- **CRUD Completo**: Crear, leer, actualizar (estado) y eliminar tickets de soporte.
- **Persistencia de Datos**: Almacenamiento automático en archivo `tickets.json`.
- **Filtro en Tiempo Real**: Búsqueda dinámica de tickets por cualquier campo.
- **Panel Métrico**: Visualiza el total de tickets, pendientes y resueltos en tiempo real.
- **Interfaz Intuitiva**: Diseño organizado con `ttk.Frame`, `Treeview` y `Combobox`.
- **Validaciones y Alertas**: Manejo de errores y confirmaciones con `messagebox`.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Descripción |
|------------|-------------|
| **Python 3.x** | Lenguaje principal del proyecto |
| **Tkinter / TTK** | Librería estándar para la interfaz gráfica |
| **JSON** | Formato de almacenamiento de datos persistente |
| **Type Hints** | Tipado estático para mejorar la legibilidad y mantenimiento |

---

## 🏗️ Estructura del Proyecto

El código está organizado en tres módulos principales siguiendo el patrón SoC: