from tarea import Tarea


class MaxHeap:
    """Max-heap sobre una lista nativa, ordenado por tarea.prioridad."""

    def __init__(self):
        self._datos = []

    def __len__(self):
        return len(self._datos)

    def insertar(self, tarea):
        self._datos.append(tarea)
        self._flotar(len(self._datos) - 1)

    def extraer_max(self):
        if not self._datos:
            return None
        maximo = self._datos[0]
        ultimo = self._datos.pop()
        if self._datos:  # la raíz solo se reemplaza si queda algo
            self._datos[0] = ultimo
            self._hundir(0)
        return maximo

    def eliminar_por_id(self, id_tarea):
        for i, t in enumerate(self._datos):
            if t.id_tarea == id_tarea:
                ultimo = self._datos.pop()
                if i < len(self._datos):  # si no era el último, recolocar y reparar
                    self._datos[i] = ultimo
                    self._flotar(i)
                    self._hundir(i)
                return t
        return None

    def _flotar(self, i):
        datos = self._datos
        while i > 0:
            padre = (i - 1) // 2
            if datos[i].prioridad <= datos[padre].prioridad:
                break
            datos[i], datos[padre] = datos[padre], datos[i]
            i = padre

    def _hundir(self, i):
        n = len(self._datos)
        datos = self._datos
        while True:
            izq, der = 2 * i + 1, 2 * i + 2
            mayor = i
            if izq < n and datos[izq].prioridad > datos[mayor].prioridad:
                mayor = izq
            if der < n and datos[der].prioridad > datos[mayor].prioridad:
                mayor = der
            if mayor == i:
                break
            datos[i], datos[mayor] = datos[mayor], datos[i]
            i = mayor


if __name__ == "__main__":
    heap = MaxHeap()
    for id_t, desc, prio, fecha in [
        (1, "A", 2, "2026-07-07"),
        (2, "B", 3, "2026-07-08"),
        (3, "C", 1, "2026-07-09"),
        (4, "D", 3, "2026-07-10"),
    ]:
        heap.insertar(Tarea(id_t, desc, prio, fecha))

    # extraer_max debe devolver en orden descendente de prioridad
    orden = [heap.extraer_max() for _ in range(len(heap))]
    assert [t.prioridad for t in orden] == [3, 3, 2, 1], [t.prioridad for t in orden]

    # eliminar_por_id mantiene la propiedad del heap
    for t in orden:
        heap.insertar(t)
    heap.eliminar_por_id(2)  # prioridad 3
    resto = sorted(
        (t.prioridad for t in (heap.extraer_max() for _ in range(len(heap)))),
        reverse=True,
    )
    assert resto == [3, 2, 1], resto

    # caso límite: eliminar inexistente y heap vacío
    assert heap.eliminar_por_id(999) is None
    assert heap.extraer_max() is None

    print("OK")
