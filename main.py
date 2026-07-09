import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

from sistema import SistemaTareas

_PRIORIDAD_A_NUM = {"Alta": 3, "Media": 2, "Baja": 1}
_NUM_A_PRIORIDAD = {v: k for k, v in _PRIORIDAD_A_NUM.items()}
_PRIO_TAG = {3: "alta", 2: "media", 1: "baja"}


# --- Paleta: tema oscuro (estilo Catppuccin Mocha) ---
class _C:
    BG = "#1e1e2e"
    SURFACE = "#313244"
    SURFACE2 = "#45475a"
    INPUT = "#313244"
    ACCENT = "#89b4fa"
    ACCENT_HOVER = "#b4befe"
    TEXT = "#cdd6f4"
    SUBTLE = "#a6adc8"
    BORDER = "#45475a"
    DANGER = "#f38ba8"
    SUCCESS = "#a6e3a1"
    # tintes sutiles de fila por prioridad
    PRIO_HIGH = "#3a2230"
    PRIO_MED = "#3a2e22"
    PRIO_LOW = "#22302a"
    PRIO_SEL = "#45475a"


class Calendario:
    """Mini-calendario en tkinter puro (sin dependencias).

    popup modal: elige una fecha y la escribe como YYYY-MM-DD en el Entry dado.
    ponytail: sin tkcalendar para no añadir dependencia; cubre lo pedido.
    """

    def __init__(self, parent, entry_destino, inicio=None):
        import calendar
        from datetime import date

        self.entry = entry_destino
        self.cal = calendar
        self.hoy = date.today()
        if inicio:
            try:
                y, m, _d = map(int, inicio.split("-"))
                self.anio, self.mes = y, m
            except ValueError:
                self.anio, self.mes = self.hoy.year, self.hoy.month
        else:
            self.anio, self.mes = self.hoy.year, self.hoy.month

        self.win = tk.Toplevel(parent)
        self.win.title("Selecciona una fecha")
        self.win.transient(parent)
        self.win.grab_set()
        self.win.configure(background=_C.SURFACE)
        self.win.resizable(False, False)

        top = tk.Frame(self.win, bg=_C.SURFACE)
        top.pack(fill="x", padx=10, pady=(10, 4))
        tk.Button(top, text="‹", bg=_C.SURFACE2, fg=_C.TEXT, relief="flat",
                  command=self._mes_ant).pack(side="left")
        self.titulo = tk.Label(top, font=("Segoe UI", 11, "bold"),
                               bg=_C.SURFACE, fg=_C.TEXT)
        self.titulo.pack(side="left", expand=True, fill="x")
        tk.Button(top, text="›", bg=_C.SURFACE2, fg=_C.TEXT, relief="flat",
                  command=self._mes_sig).pack(side="right")

        self.grid = tk.Frame(self.win, bg=_C.SURFACE)
        self.grid.pack(padx=10, pady=(0, 10))
        self._dibujar()

    def _dibujar(self):
        for w in self.grid.winfo_children():
            w.destroy()
        nombre = self.cal.month_name[self.mes]
        self.titulo.config(text=f"{nombre} {self.anio}")
        for col, d in enumerate(("Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do")):
            tk.Label(self.grid, text=d, font=("Segoe UI", 8, "bold"),
                     bg=_C.SURFACE, fg=_C.SUBTLE, width=4).grid(
                row=0, column=col, padx=1, pady=2)

        dias = self.cal.monthcalendar(self.anio, self.mes)
        for r, semana in enumerate(dias, start=1):
            for c, dia in enumerate(semana):
                if dia == 0:
                    tk.Label(self.grid, text="", bg=_C.SURFACE, width=4
                             ).grid(row=r, column=c, padx=1, pady=1)
                else:
                    es_hoy = (dia == self.hoy.day and self.mes == self.hoy.month
                              and self.anio == self.hoy.year)
                    b = tk.Button(
                        self.grid, text=str(dia), width=4, relief="flat",
                        bg=_C.ACCENT if es_hoy else _C.SURFACE2,
                        fg=_C.BG if es_hoy else _C.TEXT,
                        activebackground=_C.ACCENT_HOVER,
                        activeforeground=_C.BG,
                        command=lambda d=dia: self._elegir(d),
                    )
                    b.grid(row=r, column=c, padx=1, pady=1)

    def _mes_ant(self):
        self.mes -= 1
        if self.mes == 0:
            self.mes, self.anio = 12, self.anio - 1
        self._dibujar()

    def _mes_sig(self):
        self.mes += 1
        if self.mes == 13:
            self.mes, self.anio = 1, self.anio + 1
        self._dibujar()

    def _elegir(self, dia):
        self.entry.delete(0, tk.END)
        self.entry.insert(
            0, f"{self.anio:04d}-{self.mes:02d}-{dia:02d}"
        )
        self.win.destroy()


class App:
    def __init__(self, root):
        self.sistema = SistemaTareas()
        self._setup_styles(root)
        root.title("Tareas")
        root.geometry("600x780")
        root.minsize(540, 700)
        root.configure(background=_C.BG)

        cont = ttk.Frame(root, padding=16)
        cont.pack(fill="both", expand=True)

        # --- Header ---
        header = ttk.Frame(cont)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="✓  Tareas", style="Title.TLabel").pack(side="left")
        self.contador_lbl = ttk.Label(
            header, text="0 tareas", style="Counter.TLabel"
        )
        self.contador_lbl.pack(side="right")

        # --- Card: Formulario ---
        form_card = self._card(cont)
        ttk.Label(form_card, text="Nueva tarea", style="Section.TLabel").pack(
            anchor="w", padx=16, pady=(14, 6)
        )
        form = ttk.Frame(form_card, style="Card.TFrame", padding=(16, 4, 16, 16))
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="ID", style="Field.TLabel").grid(
            row=0, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.id_entry = ttk.Entry(form)
        self.id_entry.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(form, text="Descripción", style="Field.TLabel").grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.desc_entry = ttk.Entry(form)
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(form, text="Prioridad", style="Field.TLabel").grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=6
        )
        self.prio_combo = ttk.Combobox(
            form, state="readonly", values=list(_PRIORIDAD_A_NUM)
        )
        self.prio_combo.current(1)  # Media por defecto
        self.prio_combo.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(form, text="Vence", style="Field.TLabel").grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=6
        )
        fecha_fila = ttk.Frame(form, style="Card.TFrame")
        fecha_fila.grid(row=3, column=1, sticky="ew", pady=6)
        fecha_fila.columnconfigure(0, weight=1)
        self.fecha_entry = ttk.Entry(fecha_fila)
        self.fecha_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(fecha_fila, text="📅", width=4,
                   command=lambda: self._abrir_calendario()).grid(
            row=0, column=1, padx=(6, 0)
        )

        for e in (self.id_entry, self.desc_entry, self.fecha_entry):
            e.bind("<Return>", lambda _evt: self.agregar())

        # --- Botones de acción ---
        botones = ttk.Frame(cont)
        botones.pack(fill="x", pady=(4, 16))
        ttk.Button(
            botones, text="+  Agregar", style="Primary.TButton", command=self.agregar
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(
            botones,
            text="✓  Completar tarea más urgente",
            style="Success.TButton",
            command=self.completar_urgente,
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        # --- Card: Búsqueda ---
        busq_card = self._card(cont)
        ttk.Label(busq_card, text="Buscar por ID", style="Section.TLabel").pack(
            anchor="w", padx=16, pady=(14, 6)
        )
        busq = ttk.Frame(busq_card, style="Card.TFrame", padding=(16, 4, 16, 14))
        busq.pack(fill="x")
        busq.columnconfigure(0, weight=1)
        self.buscar_entry = ttk.Entry(busq)
        self.buscar_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(busq, text="Buscar", command=self.buscar).grid(
            row=0, column=1, padx=(8, 0)
        )
        self.resultado_lbl = ttk.Label(
            busq_card, text="", style="Result.TLabel"
        )
        self.resultado_lbl.pack(anchor="w", padx=16, pady=(8, 0))
        self.buscar_entry.bind("<Return>", lambda _evt: self.buscar())

        # --- Card: Lista de tareas ---
        lista_card = self._card(cont)
        toolbar = ttk.Frame(lista_card, style="Card.TFrame", padding=(16, 14, 12, 6))
        toolbar.pack(fill="x")
        ttk.Label(toolbar, text="Tareas guardadas", style="Section.TLabel").pack(
            side="left"
        )
        ttk.Button(
            toolbar,
            text="Eliminar",
            style="Danger.TButton",
            command=self.eliminar,
        ).pack(side="right")

        cols = ("prio", "desc", "fecha", "id")
        self.lista = ttk.Treeview(
            lista_card,
            columns=cols,
            show="headings",
            selectmode="browse",
            height=12,
        )
        self.lista.heading("prio", text="Prioridad")
        self.lista.heading("desc", text="Descripción", anchor="center")
        self.lista.heading("fecha", text="Vence", anchor="center")
        self.lista.heading("id", text="ID")
        self.lista.column("prio", width=92, anchor="w")
        self.lista.column("desc", width=240, anchor="center")
        self.lista.column("fecha", width=96, anchor="center")
        self.lista.column("id", width=52, anchor="center")
        self.lista.tag_configure("alta", background=_C.PRIO_HIGH)
        self.lista.tag_configure("media", background=_C.PRIO_MED)
        self.lista.tag_configure("baja", background=_C.PRIO_LOW)
        self.lista.pack(fill="both", expand=True, padx=12, pady=(2, 14))

        self.refrescar_lista()

    # ----- Estilos -----
    def _setup_styles(self, root):
        style = ttk.Style(root)
        style.theme_use("clam")

        base = ("Segoe UI", "Cantarell", "Helvetica", "DejaVu Sans")
        f_text = tkfont.Font(family=base, size=10)
        f_field = tkfont.Font(family=base, size=10)
        f_title = tkfont.Font(family=base, size=20, weight="bold")
        f_section = tkfont.Font(family=base, size=11, weight="bold")
        f_btn = tkfont.Font(family=base, size=10, weight="bold")
        f_counter = tkfont.Font(family=base, size=10)
        f_head = tkfont.Font(family=base, size=9, weight="bold")

        style.configure(".", background=_C.BG, foreground=_C.TEXT, font=f_text,
                        borderwidth=0, focusborderwidth=0)
        style.configure("TFrame", background=_C.BG)
        style.configure("Card.TFrame", background=_C.SURFACE)

        # Labels
        style.configure("TLabel", background=_C.BG, foreground=_C.TEXT)
        style.configure("Title.TLabel", font=f_title, foreground=_C.TEXT,
                        background=_C.BG)
        style.configure("Counter.TLabel", font=f_counter, foreground=_C.SUBTLE,
                        background=_C.BG)
        style.configure("Section.TLabel", font=f_section, foreground=_C.TEXT,
                        background=_C.SURFACE)
        style.configure("Field.TLabel", font=f_field, foreground=_C.SUBTLE,
                        background=_C.SURFACE)
        style.configure("Result.TLabel", font=f_text, foreground=_C.ACCENT,
                        background=_C.SURFACE)

        # Entries
        style.configure("TEntry", fieldbackground=_C.INPUT, foreground=_C.TEXT,
                        bordercolor=_C.BORDER, lightcolor=_C.BORDER,
                        darkcolor=_C.BORDER, insertcolor=_C.TEXT, padding=7,
                        borderwidth=0)
        style.map("TEntry", bordercolor=[("focus", _C.ACCENT)],
                  lightcolor=[("focus", _C.ACCENT)],
                  darkcolor=[("focus", _C.ACCENT)])

        # Combobox (y su lista desplegable)
        style.configure("TCombobox", fieldbackground=_C.INPUT, foreground=_C.TEXT,
                        background=_C.SURFACE2, arrowcolor=_C.TEXT,
                        bordercolor=_C.BORDER, lightcolor=_C.BORDER,
                        darkcolor=_C.BORDER, insertcolor=_C.TEXT, padding=7)
        style.map("TCombobox",
                  fieldbackground=[("readonly", _C.INPUT)],
                  foreground=[("readonly", _C.TEXT)],
                  bordercolor=[("focus", _C.ACCENT)],
                  lightcolor=[("focus", _C.ACCENT)])
        root.option_add("*TCombobox*Listbox.background", _C.SURFACE)
        root.option_add("*TCombobox*Listbox.foreground", _C.TEXT)
        root.option_add("*TCombobox*Listbox.selectBackground", _C.ACCENT)
        root.option_add("*TCombobox*Listbox.selectForeground", _C.BG)

        # Botones
        style.configure("TButton", background=_C.SURFACE2, foreground=_C.TEXT,
                        borderwidth=0, focuscolor=_C.SURFACE2, padding=(14, 10),
                        font=f_btn)
        style.map("TButton", background=[("active", _C.BORDER)])
        style.configure("Primary.TButton", background=_C.ACCENT,
                        foreground=_C.BG, padding=(14, 11), font=f_btn)
        style.map("Primary.TButton",
                  background=[("active", _C.ACCENT_HOVER),
                              ("pressed", _C.ACCENT_HOVER)],
                  foreground=[("active", _C.BG)])
        style.configure("Success.TButton", background=_C.SUCCESS,
                        foreground=_C.BG, padding=(14, 11), font=f_btn)
        style.map("Success.TButton", background=[("active", "#c5f0b0")])
        style.configure("Danger.TButton", background="transparent",
                        foreground=_C.DANGER, padding=(10, 6), font=f_btn)
        style.map("Danger.TButton",
                  background=[("active", _C.SURFACE2)],
                  foreground=[("active", _C.DANGER)])

        # Treeview
        style.configure("Treeview", background=_C.SURFACE,
                        fieldbackground=_C.SURFACE, foreground=_C.TEXT,
                        borderwidth=0, rowheight=30)
        style.configure("Treeview.Heading", background=_C.SURFACE2,
                        foreground=_C.SUBTLE, borderwidth=0,
                        padding=(8, 7), font=f_head, relief="flat")
        style.map("Treeview", background=[("selected", _C.ACCENT)],
                  foreground=[("selected", _C.BG)])
        style.map("Treeview.Heading", background=[("active", _C.BORDER)])

    # ----- Helpers de layout -----
    @staticmethod
    def _card(parent):
        """Tarjeta con superficie diferenciada y esquinas separadas del fondo."""
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill="x", pady=(0, 14))
        return card

    def _abrir_calendario(self):
        Calendario(self.id_entry.winfo_toplevel(), self.fecha_entry,
                   inicio=self.fecha_entry.get().strip() or None)

    # ----- Acciones -----
    def agregar(self):
        try:
            id_tarea = int(self.id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        desc = self.desc_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        if not desc or not fecha:
            messagebox.showerror(
                "Error", "La descripción y la fecha son obligatorias."
            )
            return
        prioridad = _PRIORIDAD_A_NUM[self.prio_combo.get()]
        self.sistema.agregar_tarea(id_tarea, desc, prioridad, fecha)
        self._limpiar_form()
        self.refrescar_lista()

    def completar_urgente(self):
        t = self.sistema.obtener_mas_urgente()
        if t is None:
            messagebox.showinfo("Sin tareas", "No hay tareas pendientes.")
            return
        messagebox.showinfo(
            "Tarea completada",
            f"Se completó la tarea más urgente:\n\n{t!r}",
        )
        self.refrescar_lista()

    def buscar(self):
        try:
            id_tarea = int(self.buscar_entry.get().strip())
        except ValueError:
            self.resultado_lbl.config(text="ID inválido", foreground=_C.DANGER)
            return
        t = self.sistema.buscar_tarea(id_tarea)
        if t:
            self.resultado_lbl.config(text=str(t), foreground=_C.ACCENT)
        else:
            self.resultado_lbl.config(text="No encontrada", foreground=_C.DANGER)

    def eliminar(self):
        sel = self.lista.selection()
        if not sel:
            messagebox.showinfo(
                "Selecciona una tarea", "Marca una tarea de la lista para eliminar."
            )
            return
        id_tarea = int(sel[0])
        self.sistema.eliminar_tarea_especifica(id_tarea)
        self.refrescar_lista()

    # ----- Helpers -----
    def refrescar_lista(self):
        self.lista.delete(*self.lista.get_children())
        # Ordenadas por urgencia (prioridad desc) para reflejar el Heap
        tareas = sorted(
            self.sistema.listar_tareas(), key=lambda t: t.prioridad, reverse=True
        )
        for t in tareas:
            prio_txt = _NUM_A_PRIORIDAD.get(t.prioridad, "—")
            self.lista.insert(
                "", "end", iid=str(t.id_tarea),
                values=(prio_txt, t.descripcion, t.fecha_vencimiento, t.id_tarea),
                tags=(_PRIO_TAG.get(t.prioridad, "baja"),),
            )
        n = len(tareas)
        self.contador_lbl.config(text=f"{n} tarea{'s' if n != 1 else ''}")

    def _limpiar_form(self):
        for e in (self.id_entry, self.desc_entry, self.fecha_entry):
            e.delete(0, tk.END)
        self.id_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
