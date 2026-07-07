from tarea import Tarea


class NodoAVL:
    def __init__(self, tarea):
        self.tarea = tarea
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    @staticmethod
    def _altura(n):
        return n.altura if n else 0

    @staticmethod
    def _balance(n):
        return ArbolAVL._altura(n.izq) - ArbolAVL._altura(n.der) if n else 0

    @staticmethod
    def _actualizar_altura(n):
        n.altura = 1 + max(ArbolAVL._altura(n.izq), ArbolAVL._altura(n.der))

    # --- 4 rotaciones ---
    @staticmethod
    def _rotar_izq(x):
        y = x.der
        x.der = y.izq
        y.izq = x
        ArbolAVL._actualizar_altura(x)
        ArbolAVL._actualizar_altura(y)
        return y  # nueva raíz del subárbol

    @staticmethod
    def _rotar_der(y):
        x = y.izq
        y.izq = x.der
        x.der = y
        ArbolAVL._actualizar_altura(y)
        ArbolAVL._actualizar_altura(x)
        return x

    @staticmethod
    def _doble_izq_der(n):  # LR: rotar izq hijo izq, luego der n
        n.izq = ArbolAVL._rotar_izq(n.izq)
        return ArbolAVL._rotar_der(n)

    @staticmethod
    def _doble_der_izq(n):  # RL: rotar der hijo der, luego izq n
        n.der = ArbolAVL._rotar_der(n.der)
        return ArbolAVL._rotar_izq(n)

    @staticmethod
    def _reequilibrar(n):
        ArbolAVL._actualizar_altura(n)
        bal = ArbolAVL._balance(n)
        if bal > 1:  # pesado a la izquierda
            if ArbolAVL._balance(n.izq) < 0:  # hijo izq pesa a la derecha
                return ArbolAVL._doble_izq_der(n)
            return ArbolAVL._rotar_der(n)
        if bal < -1:  # pesado a la derecha
            if ArbolAVL._balance(n.der) > 0:  # hijo der pesa a la izquierda
                return ArbolAVL._doble_der_izq(n)
            return ArbolAVL._rotar_izq(n)
        return n

    @staticmethod
    def insertar(raiz, tarea):
        if raiz is None:
            return NodoAVL(tarea)
        if tarea.id_tarea < raiz.tarea.id_tarea:
            raiz.izq = ArbolAVL.insertar(raiz.izq, tarea)
        elif tarea.id_tarea > raiz.tarea.id_tarea:
            raiz.der = ArbolAVL.insertar(raiz.der, tarea)
        else:  # ponytail: ignoro duplicados; lanzar si hace falta unicidad estricta
            return raiz
        return ArbolAVL._reequilibrar(raiz)

    @staticmethod
    def buscar(raiz, id_tarea):
        if raiz is None:
            return None
        if id_tarea == raiz.tarea.id_tarea:
            return raiz.tarea
        if id_tarea < raiz.tarea.id_tarea:
            return ArbolAVL.buscar(raiz.izq, id_tarea)
        return ArbolAVL.buscar(raiz.der, id_tarea)

    @staticmethod
    def _min_nodo(n):
        while n.izq:
            n = n.izq
        return n

    @staticmethod
    def eliminar(raiz, id_tarea):
        if raiz is None:
            return None
        if id_tarea < raiz.tarea.id_tarea:
            raiz.izq = ArbolAVL.eliminar(raiz.izq, id_tarea)
        elif id_tarea > raiz.tarea.id_tarea:
            raiz.der = ArbolAVL.eliminar(raiz.der, id_tarea)
        else:
            if raiz.izq is None:
                return raiz.der
            if raiz.der is None:
                return raiz.izq
            # dos hijos: reemplazar por el sucesor in-order
            sucesor = ArbolAVL._min_nodo(raiz.der)
            raiz.tarea = sucesor.tarea
            raiz.der = ArbolAVL.eliminar(raiz.der, sucesor.tarea.id_tarea)
        return ArbolAVL._reequilibrar(raiz)

    @staticmethod
    def in_order(raiz):
        """Recorre in-order; devuelve la lista de tareas ordenadas por id."""
        out = []
        ArbolAVL._in_order(raiz, out)
        return out

    @staticmethod
    def _in_order(n, out):
        if n:
            ArbolAVL._in_order(n.izq, out)
            out.append(n.tarea)
            ArbolAVL._in_order(n.der, out)


if __name__ == "__main__":
    # Inserción desbalanceada: 1,2,3,4,5,6,7 en orden creciente.
    # Sin AVL esto sería una lista enlazada (altura 7); con AVL altura 3.
    raiz = None
    for i in range(1, 8):
        raiz = ArbolAVL.insertar(raiz, Tarea(i, f"T{i}", i % 3 + 1, "2026-07-07"))

    assert raiz.altura == 3, raiz.altura  # equilibrio automático

    # in-order respeta el orden de IDs
    ids = [t.id_tarea for t in ArbolAVL.in_order(raiz)]
    assert ids == list(range(1, 8)), ids

    # buscar O(log n): encuentra y devuelve el objeto
    t3 = ArbolAVL.buscar(raiz, 3)
    assert t3 is not None and t3.id_tarea == 3
    assert ArbolAVL.buscar(raiz, 99) is None  # ausente

    # eliminar la raíz y seguir balanceado
    raiz = ArbolAVL.eliminar(raiz, 4)
    assert raiz.altura <= 3
    assert ArbolAVL.buscar(raiz, 4) is None
    ids = [t.id_tarea for t in ArbolAVL.in_order(raiz)]
    assert ids == [1, 2, 3, 5, 6, 7], ids

    # factor de equilibrio de cada nodo en rango [-1, 1] tras eliminar
    def check(n):
        if n is None:
            return True
        b = ArbolAVL._balance(n)
        assert -1 <= b <= 1, b
        return check(n.izq) and check(n.der)

    assert check(raiz)

    print("OK")
