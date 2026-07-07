from tarea import Tarea
from heap import MaxHeap
from avl import ArbolAVL


class SistemaTareas:
    def __init__(self):
        self.heap = MaxHeap()
        self.avl_raiz = None  # AVL funciona con raíz explícita, no instancia

    def agregar_tarea(self, id_tarea, descripcion, prioridad, fecha_vencimiento):
        t = Tarea(id_tarea, descripcion, prioridad, fecha_vencimiento)
        self.heap.insertar(t)  # misma referencia de memoria en ambas estructuras
        self.avl_raiz = ArbolAVL.insertar(self.avl_raiz, t)
        return t

    def obtener_mas_urgente(self):
        t = self.heap.extraer_max()
        if t is not None:
            self.avl_raiz = ArbolAVL.eliminar(self.avl_raiz, t.id_tarea)
        return t

    def buscar_tarea(self, id_tarea):
        return ArbolAVL.buscar(self.avl_raiz, id_tarea)

    def listar_tareas(self):
        return ArbolAVL.in_order(self.avl_raiz)

    def eliminar_tarea_especifica(self, id_tarea):
        t = self.buscar_tarea(id_tarea)
        if t is None:
            return None
        self.avl_raiz = ArbolAVL.eliminar(self.avl_raiz, id_tarea)
        self.heap.eliminar_por_id(id_tarea)
        return t


if __name__ == "__main__":
    s = SistemaTareas()
    for i, p in [(1, 2), (2, 3), (3, 1), (4, 3), (5, 2)]:
        s.agregar_tarea(i, f"T{i}", p, "2026-07-07")

    assert s.buscar_tarea(3) is not None
    assert s.obtener_mas_urgente().prioridad == 3
    assert s.buscar_tarea(2) is None  # extraída → ya no en AVL
    assert s.eliminar_tarea_especifica(4) is not None
    assert s.buscar_tarea(4) is None
    print("OK")
