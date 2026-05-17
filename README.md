# iamodel — Sudoku + modelo IA (Python)

Proyecto en Python con dos partes principales:

1) **Juego de Sudoku**
- **Modo consola (CLI)**: `sudoku.py`
- **Modo gráfico (GUI)** con Pygame: `sudoku_gui.py`

2) **Modelo de IA (PyTorch) para predecir celdas faltantes**
- Definición de la red: `sudoku_model.py`
- Generación de dataset: `generate_dataset.py`
- Entrenamiento: `train_model.py`

Incluye generación de tableros completos, creación de puzzles por dificultad, validación de jugadas, pistas y resolución automática (en el juego), además del pipeline básico para entrenar un modelo que predice dígitos en celdas vacías.

## Características

### Juego

- Generación de tableros Sudoku válidos (9x9).
- Creación de puzzles con solución única.
- Dificultades disponibles: `easy`, `medium`, `hard`.
- Modo consola interactivo con comandos.
- Interfaz gráfica con selección de celdas, ingreso por teclado, botones de ayuda y resolución.
- Detección visual de celdas inválidas en la GUI.
- Medición de tiempo de partida y conteo de pistas usadas.

### IA / Entrenamiento

- `SudokuNet`: red convolucional residual que recibe un tablero (0–9; 0 = vacío) y produce logits para dígitos 1–9 por celda.
- Generación de dataset en `data/` como `puzzles.npy` y `solutions.npy`.
- Script de entrenamiento con métricas de **accuracy solo en celdas vacías** (`empty_acc`) y guardado del mejor modelo.

## Estructura del repositorio

```text
.
├── sudoku.py             # Lógica principal + modo CLI
├── sudoku_gui.py         # Interfaz gráfica con pygame
├── sudoku_model.py       # Modelo IA (PyTorch)
├── generate_dataset.py   # Generación de dataset (puzzles/soluciones)
├── train_model.py        # Entrenamiento del modelo
├── requirements.txt      # Dependencias de Python
└── .gitignore
```

## Requisitos

- Python 3.10+ recomendado
- Dependencias:
  - `pygame-ce==2.5.7`
  - `tk==0.1.0`
  - **PyTorch**, **NumPy** y **tqdm** (usados por `train_model.py` / `sudoku_model.py` / `generate_dataset.py`)

> Nota: La GUI usa `pygame`.

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

Si vas a entrenar el modelo, instala además (ejemplo):

```bash
pip install torch numpy tqdm
```

## Uso

### 1) Ejecutar modo consola (CLI)

```bash
python sudoku.py
```

Al iniciar, podrás elegir dificultad (`easy`, `medium`, `hard`).

#### Comandos en consola

- `fila columna numero`
  - Ejemplo: `3 5 7`
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

### 3) Generar dataset para entrenamiento

Genera `data/puzzles.npy` y `data/solutions.npy`:

```bash
python generate_dataset.py --n 20000 --out data
```

### 4) Entrenar el modelo

Entrena usando los `.npy` en `data/` y guarda el mejor modelo en `model.pth`:

```bash
python train_model.py --data data --epochs 20 --batch 256 --lr 1e-3 --out model.pth
```

La métrica principal mostrada es `empty_acc` (accuracy calculada solo en celdas que estaban vacías en el puzzle).

## Cómo funciona internamente (resumen)

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

### Modelo `SudokuNet`

- Entrada: `(B, 81)` con valores `0-9` (0 = celda vacía)
- One-hot a 10 canales y convolución 1x1 para embedding
- Varios bloques residuales 3x3
- Cabeza 1x1 para producir logits por dígito (1–9) en cada celda

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

Proyecto funcional para jugar Sudoku (consola y GUI) y para entrenar un modelo base de IA que predice dígitos en celdas vacías.

## Contribuciones

Si quieres mejorar el proyecto:

1. Haz un fork.
2. Crea una rama de feature.
3. Envía un Pull Request con una descripción clara de los cambios.

## Licencia

Este repositorio no incluye un archivo de licencia explícito en su estado actual.
