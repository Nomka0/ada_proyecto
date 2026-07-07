# Sistema de Gestión de Tareas

Proyecto de estructuras de datos que integra un **Max-Heap** (cola de prioridad) y un **Árbol AVL** (índice por ID) para gestionar tareas, con una interfaz gráfica en **tkinter**.

## Integrantes

-  santi 
-  kevin 
-  juan josé

---

## 1. Descripción general

El sistema coordina dos estructuras de datos sobre los mismos objetos `Tarea`
(comparten referencias de memoria, no se duplican) para obtener lo mejor de
cada una:

| Estructura | Ordenada por | Operación eficiente | Uso en el sistema |
|------------|--------------|---------------------|-------------------|
| **MaxHeap** | `prioridad` | `extraer_max()` en O(log n) | Obtener la tarea más urgente al instante |
| **ArbolAVL** | `id_tarea` | `buscar()` en O(log n) | Buscar y eliminar tareas por ID rápidamente |

### ¿Cómo se integran?

La clase `SistemaTareas` (`sistema.py`) es el puente:

- **`agregar_tarea()`** crea un único objeto `Tarea` y lo inserta **a la vez**
  en el Heap y en el AVL. Ambas estructuras apuntan al mismo objeto, de modo
  que un cambio en una se refleja en la otra sin sincronización extra.
- **`obtener_mas_urgente()`** extrae el máximo del Heap (O(log n)) y borra
  esa misma tarea del AVL usando su ID (O(log n)). Así las dos estructuras
  quedan consistentes.
- **`buscar_tarea(id)`** consulta solo el AVL: búsqueda binaria O(log n),
  imposible de igualar recorriendo el Heap.
- **`eliminar_tarea_especifica(id)`** la borra del AVL y del Heap por ID.

> El Heap da la **urgencia**; el AVL da el **acceso por ID**. Juntas cubren los
> dos casos de uso sin sacrificar complejidad.

---

## 2. Requisitos previos

- **Python 3.8 o superior** (usa `tkinter`, incluido en la librería estándar).
- **No requiere librerías externas.** No hay `requirements.txt` ni `pip install`.
- En algunas distribuciones de Linux, `tkinter` viene por separado:

  ```bash
  # Debian / Ubuntu
  sudo apt install python3-tk
  # Fedora
  sudo dnf install python3-tkinter
  ```

---

## 3. Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/[usuario]/ada_pro.git
cd ada_pro

# 2. (Opcional) Ejecutar las pruebas internas de cada módulo
python3 tarea.py
python3 heap.py
python3 avl.py
python3 sistema.py

# 3. Lanzar la interfaz gráfica
python3 main.py
```

Se abrirá la ventana principal con el formulario, los botones de acción, la
búsqueda y el panel de tareas.

---

## 4. Guía rápida: 4 casos de prueba desde la GUI

Arranca la aplicación con `python3 main.py` y sigue cada caso.

### ✅ Caso 1 — Inserción

Verifica que una tarea nueva queda registrada en ambas estructuras.

1. Completa el formulario: **ID** = `1`, **Descripción** = `Estudiar`,
   **Prioridad** = `Alta`, **Fecha** = `2026-07-10`.
2. Pulsa **Agregar Tarea**. El formulario se limpia y la tarea aparece en el
   panel inferior.
3. Repite con ID `2`, `3`, prioridades `Media` y `Baja`.
4. **Resultado esperado:** las tres tareas aparecen ordenadas por prioridad
   en el panel (las `Alta` arriba).

### 🗑️ Caso 2 — Eliminación

Verifica la eliminación por ID en Heap y AVL a la vez.

1. En el área de búsqueda, escribe el **ID** de una tarea existente (p. ej. `2`).
2. Pulsa **Buscar** para confirmar que existe.
3. Pulsa **Completar Más Urgente**. Aparece un mensaje con la tarea de mayor
   prioridad; al cerrarlo, desaparece del panel.
4. Busca de nuevo ese ID: ahora dirá **"No encontrada"** (se borró del AVL).
5. **Resultado esperado:** la tarea ya no está en el panel ni en la búsqueda.

### 🔍 Caso 3 — Indexación

Verifica la búsqueda O(log n) por ID usando el AVL.

1. Agrega varias tareas con IDs distintos (p. ej. `10`, `25`, `7`, `42`).
2. En el área de búsqueda escribe un ID existente (p. ej. `25`) y pulsa
   **Buscar**.
3. **Resultado esperado:** se muestran los datos completos de la tarea al
   instante, en azul. Un ID inexistente muestra **"No encontrada"** en rojo.

### ⚖️ Caso 4 — Equilibrio

Verifica que el AVL se autoequilibra tras inserciones en orden (caso que
sin AVL degeneraría en lista).

1. Agrega tareas con IDs **correlativos**: `1`, `2`, `3`, `4`, `5`, `6`, `7`,
   todas con la misma prioridad y fecha.
2. Pulsa **Completar Más Urgente** repetidamente.
3. **Resultado esperado:** las tareas salen en el orden correcto de prioridad
   y la búsqueda de cualquier ID (p. ej. el `4`) sigue siendo inmediata,
   demostrando que el árbol no degeneró: su altura se mantiene ≈ log₂(n).

> Para una verificación programática del equilibrio, ejecuta
> `python3 avl.py`: su bloque `__main__` inserta 1–7 y comprueba que la
> altura es 3 (la de un árbol balanceado, no 7).

---

## 5. Estructura del proyecto

```
ada_pro/
├── tarea.py       # Clase Tarea (modelo de datos)
├── heap.py        # MaxHeap — cola de prioridad por prioridad
├── avl.py         # ArbolAVL — índice balanceado por id_tarea
├── sistema.py     # SistemaTareas — coordinador Heap + AVL
├── main.py        # Interfaz gráfica (tkinter)
└── README.md
```
