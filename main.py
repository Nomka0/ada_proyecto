import tkinter as tk
from tkinter import ttk, messagebox

from sistema import SistemaTareas
from tarea import Tarea

_PRIORIDAD_A_NUM = {"Alta": 3, "Media": 2, "Baja": 1}
_NUM_A_PRIORIDAD = {v: k for k, v in _PRIORIDAD_A_NUM.items()}


class App:
    def __init__(self, root):
        self.sistema = SistemaTareas()
        root.title("Sistema de Tareas")
        root.geometry("500x620")

        # --- 1. Formulario de entrada ---
        form = tk.LabelFrame(root, text="Nueva tarea", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="ID:").grid(row=0, column=0, sticky="e")
        self.id_entry = tk.Entry(form)
        self.id_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(form, text="Descripción:").grid(row=1, column=0, sticky="e")
        self.desc_entry = tk.Entry(form)
        self.desc_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(form, text="Prioridad:").grid(row=2, column=0, sticky="e")
        self.prio_combo = ttk.Combobox(
            form, state="readonly", values=list(_PRIORIDAD_A_NUM)
        )
        self.prio_combo.current(1)  # Media por defecto
        self.prio_combo.grid(row=2, column=1, sticky="ew")

        tk.Label(form, text="Fecha:").grid(row=3, column=0, sticky="e")
        self.fecha_entry = tk.Entry(form)
        self.fecha_entry.grid(row=3, column=1, sticky="ew")
        form.columnconfigure(1, weight=1)

        # --- 2 y 3. Botones de acción ---
        botones = tk.Frame(root)
        botones.pack(fill="x", padx=10, pady=5)
        tk.Button(botones, text="Agregar Tarea", command=self.agregar).pack(
            side="left", expand=True, fill="x"
        )
        tk.Button(
            botones, text="Completar Más Urgente", command=self.completar_urgente
        ).pack(side="left", expand=True, fill="x")

        # --- 4. Búsqueda ---
        busq = tk.LabelFrame(root, text="Buscar por ID", padx=10, pady=10)
        busq.pack(fill="x", padx=10, pady=5)
        self.buscar_entry = tk.Entry(busq)
        self.buscar_entry.pack(side="left", fill="x", expand=True)
        tk.Button(busq, text="Buscar", command=self.buscar).pack(side="left", padx=5)
        self.resultado_lbl = tk.Label(busq, text="", fg="blue")
        self.resultado_lbl.pack(side="left")

        # --- 5. Panel de tareas en tiempo real ---
        panel = tk.LabelFrame(root, text="Tareas guardadas", padx=10, pady=10)
        panel.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista = tk.Listbox(panel)
        self.lista.pack(fill="both", expand=True)

        self.refrescar_lista()

    # --- Acciones ---
    def agregar(self):
        try:
            id_tarea = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID debe ser un entero")
            return
        desc = self.desc_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        if not desc or not fecha:
            messagebox.showerror("Error", "Descripción y fecha son obligatorias")
            return
        prioridad = _PRIORIDAD_A_NUM[self.prio_combo.get()]
        self.sistema.agregar_tarea(id_tarea, desc, prioridad, fecha)
        self._limpiar_form()
        self.refrescar_lista()

    def completar_urgente(self):
        t = self.sistema.obtener_mas_urgente()
        if t is None:
            messagebox.showinfo("Vacío", "No hay tareas")
            return
        messagebox.showinfo("Tarea completada", repr(t))
        self.refrescar_lista()

    def buscar(self):
        try:
            id_tarea = int(self.buscar_entry.get().strip())
        except ValueError:
            self.resultado_lbl.config(text="ID inválido", fg="red")
            return
        t = self.sistema.buscar_tarea(id_tarea)
        self.resultado_lbl.config(
            text=repr(t) if t else "No encontrada",
            fg="blue" if t else "red",
        )

    # --- Helpers ---
    def refrescar_lista(self):
        self.lista.delete(0, tk.END)
        # Ordenadas por urgencia (prioridad desc) para reflejar el Heap
        tareas = sorted(
            self.sistema.listar_tareas(), key=lambda t: t.prioridad, reverse=True
        )
        for t in tareas:
            self.lista.insert(tk.END, repr(t))

    def _limpiar_form(self):
        for e in (self.id_entry, self.desc_entry, self.fecha_entry):
            e.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
