_PRIORIDAD = {3: "Alta", 2: "Media", 1: "Baja"}


class Tarea:
    def __init__(self, id_tarea, descripcion, prioridad, fecha_vencimiento):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.fecha_vencimiento = fecha_vencimiento

    def __repr__(self):
        prio = _PRIORIDAD.get(self.prioridad, "Desconocida")
        return (
            f"Tarea(id={self.id_tarea}, '{self.descripcion}', "
            f"prioridad={prio}, vence={self.fecha_vencimiento})"
        )


if __name__ == "__main__":
    t = Tarea(1, "Comprar pan", 3, "2026-07-07")
    assert "Alta" in repr(t) and "Comprar pan" in repr(t), repr(t)
    print(t)
