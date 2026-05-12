# iamodel — Sudoku en Python (CLI + GUI)

Proyecto de Sudoku hecho en Python con dos formas de juego:

- **Modo consola (CLI)** en `sudoku.py`
- **Modo gráfico (GUI)** con Pygame en `sudoku_gui.py`

Incluye generación de tableros completos, creación de puzzles por dificultad, validación de jugadas, pistas y resolución automática.

## Características

- Generación de tableros Sudoku válidos (9x9).
- Creación de puzzles con solución única.
- Dificultades disponibles:
  - `easy`
  - `medium`
  - `hard`
- Modo consola interactivo con comandos.
- Interfaz gráfica con selección de celdas, ingreso por teclado, botones de ayuda y resolución.
- Detección visual de celdas inválidas en la GUI.
- Medición de tiempo de partida y conteo de pistas usadas.

## Estructura del repositorio

```text
.
├── sudoku.py          # Lógica principal + modo CLI
├── sudoku_gui.py      # Interfaz gráfica con pygame
├── requirements.txt   # Dependencias de Python
└── .gitignore
```

## Requisitos

- Python 3.10+ recomendado
- Dependencias de `requirements.txt`:
  - `pygame-ce==2.5.7`
  - `tk==0.1.0`

> Nota: la GUI usa `pygame`.

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/xalbertho/iamodel.git
cd iamodel
```

2. (Opcional) Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

En Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Uso

### 1) Ejecutar modo consola (CLI)

```bash
python sudoku.py
```

Al iniciar, podrás elegir dificultad (`easy`, `medium`, `hard`).

#### Comandos en consola

- `fila columna numero`  
  Ejemplo: `3 5 7`
- `hint` → coloca una pista aleatoria.
- `solve` → completa el tablero automáticamente.
- `restart` → reinicia la partida actual.
- `quit` → salir.

### 2) Ejecutar modo gráfico (GUI)

```bash
python sudoku_gui.py
```

#### Controles GUI

- **Mouse**:
  - Clic en celda para seleccionarla.
  - Clic en botones:
    - `New Game`
    - `Hint`
    - `Solve`
    - dificultad: `easy`, `medium`, `hard`
- **Teclado**:
  - `1` a `9` para colocar número.
  - `Backspace` / `Delete` para limpiar celda.
  - Flechas para mover selección.
  - `Esc` para deseleccionar.

## Cómo funciona internamente

### Generación de tablero completo

En `sudoku.py`:

- `generate_full_board()` crea una matriz 9x9 vacía.
- `_fill(board)` aplica backtracking con números aleatorios para completar un Sudoku válido.
- `_valid(board, row, col, n)` valida reglas por fila, columna y subcuadro 3x3.

### Creación de puzzle por dificultad

- `make_puzzle(difficulty)` parte de un tablero completo.
- Remueve celdas aleatoriamente.
- Usa `_count_solutions(board, limit=2)` para asegurar solución única.
- Mantiene pistas objetivo según `CLUES`:
  - easy: 45
  - medium: 35
  - hard: 25

### Juego y validación

- `is_complete(board)` verifica si no quedan ceros.
- `solve(board)` resuelve por backtracking.
- En GUI, `Game._check_invalid()` marca celdas en conflicto para mostrar errores visualmente.

## Personalización rápida

Puedes ajustar dificultad editando `CLUES` en `sudoku.py`:

```python
CLUES = {"easy": 45, "medium": 35, "hard": 25}
```

Más pistas = puzzle más fácil.

## Solución de problemas

- **La GUI no abre**
  - Verifica instalación de dependencias:
    ```bash
    pip install -r requirements.txt
    ```
  - Revisa versión de Python y que el entorno virtual esté activo.

- **Error al ejecutar `python`**
  - Prueba con `python3` según tu sistema.

- **No se instalan paquetes**
  - Actualiza pip:
    ```bash
    python -m pip install --upgrade pip
    ```

## Estado del proyecto

Proyecto funcional para jugar Sudoku en consola y en GUI local.

## Contribuciones

Si quieres mejorar el proyecto:

1. Haz un fork.
2. Crea una rama de feature.
3. Envía un Pull Request con una descripción clara de los cambios.

## Licencia

Este repositorio no incluye un archivo de licencia explícito en su estado actual.
