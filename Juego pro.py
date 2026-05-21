import tkinter as tk

# =========================================================
# CONFIGURACIÓN (¡Edita los colores y el tamaño aquí!)
# =========================================================
TAMANO_CASILLA = 8        # En este método, el tamaño se mide en "caracteres" (5 a 10 es ideal)
COLOR_CLARO = "#ffffff"    # Crema clásico
COLOR_OSCURO = "#000000"   # Marrón clásico
# =========================================================

root = tk.Tk()
root.title("Tablero de Ajedrez")

# Dibujamos las 8x8 casillas usando una cuadrícula (grid)
for fila in range(8):
    for columna in range(8):
        
        # Si la suma de fila y columna es par -> color claro. Si no -> oscuro.
        if (fila + columna) % 2 == 0:
            color_actual = COLOR_CLARO
        else:
            color_actual = COLOR_OSCURO
            
        # Creamos la casilla como un bloque de color vacío
        casilla = tk.Label(
            root, 
            bg=color_actual, 
            width=TAMANO_CASILLA * 2,  # Multiplicamos por 2 porque los caracteres son más altos que anchos
            height=TAMANO_CASILLA
        )
        
        # Colocamos la casilla en su fila y columna correspondiente
        casilla.grid(row=fila, column=columna)

root.mainloop()