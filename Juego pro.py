import tkinter as tk
import os

TAMANO_CASILLA = 70       
COLOR_CLARO = "#FFFFFF"    
COLOR_OSCURO = "#000000"   
COLOR_SELECCION = "#7ae7ff" 
CARPETA_IMAGENES = "imagenes"

TABLERO = [
    ["torre_n", "caballo_n", "alfil_n", "reina_n", "rey_n", "alfil_n", "caballo_n", "torre_n"],
    ["peon_n",  "peon_n",    "peon_n",  "peon_n",  "peon_n", "peon_n",  "peon_n",    "peon_n"],
    ["",        "",          "",        "",        "",        "",        "",          ""],
    ["",        "",          "",        "",        "",        "",        "",          ""],
    ["",        "",          "",        "",        "",        "",        "",          ""],
    ["",        "",          "",        "",        "",        "",        "",          ""],
    ["peon_b",  "peon_b",    "peon_b",  "peon_b",  "peon_b", "peon_b",  "peon_b",    "peon_b"],
    ["torre_b", "caballo_b", "alfil_b", "reina_b", "rey_b", "alfil_b", "caballo_b", "torre_b"]
]

SIMBOLOS_PIEZAS = {
    "peon_b": "♙", "torre_b": "♖", "caballo_b": "♘", "alfil_b": "♗", "reina_b": "♕", "rey_b": "♔",
    "peon_n": "♟", "torre_n": "♜", "caballo_n": "♞", "alfil_n": "♝", "reina_n": "♛", "rey_n": "♚"
}

class AjedrezDosClics:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajedrez - Movimientos Reales")
        
        self.canvas = tk.Canvas(root, width=8*TAMANO_CASILLA, height=8*TAMANO_CASILLA)
        self.canvas.pack()
        
        self.imagenes_piezas = {}
        self.origen_seleccionado = None  
        self.recuadro_seleccion = None
        self.turno = "b"  
        
        self.cargar_imagenes()
        self.actualizar_interfaz()
        
        self.canvas.bind("<Button-1>", self.gestionar_clic)

    def cargar_imagenes(self):
        piezas = ["peon", "torre", "caballo", "alfil", "reina", "rey"]
        colores = ["b", "n"]
        for pieza in piezas:
            for color in colores:
                nombre_clave = f"{pieza}_{color}"
                ruta = os.path.join(CARPETA_IMAGENES, f"{nombre_clave}.png")
                if os.path.exists(ruta):
                    self.imagenes_piezas[nombre_clave] = tk.PhotoImage(file=ruta)
                else:
                    self.imagenes_piezas[nombre_clave] = None

    def actualizar_interfaz(self):
        """Borra todo el canvas y lo redibuja según el estado actual de la matriz TABLERO"""
        self.canvas.delete("all")
        
        for fila in range(8):
            for columna in range(8):
                color = COLOR_CLARO if (fila + columna) % 2 == 0 else COLOR_OSCURO
                x1, y1 = columna * TAMANO_CASILLA, fila * TAMANO_CASILLA
                x2, y2 = x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        if self.origen_seleccionado:
            f, c = self.origen_seleccionado
            x1, y1 = c * TAMANO_CASILLA, f * TAMANO_CASILLA
            x2, y2 = x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_SELECCION, outline="")

        for fila in range(8):
            for columna in range(8):
                nombre_pieza = TABLERO[fila][columna]
                if nombre_pieza != "":
                    x = (columna * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    y = (fila * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    
                    if self.imagenes_piezas.get(nombre_pieza) is not None:
                        self.canvas.create_image(x, y, image=self.imagenes_piezas[nombre_pieza])
                    else:
                        simbolo = SIMBOLOS_PIEZAS.get(nombre_pieza, "?")
                        color_pieza = nombre_pieza.split("_")[1]
                        
                        color_txt = "#FFFFFF" if color_pieza == "b" else "#000000"
                        color_borde = "#000000" if color_pieza == "b" else "#FFFFFF"
                        
                        fuente = ("Arial", 36, "bold")
                        self.canvas.create_text(x-1, y, text=simbolo, font=fuente, fill=color_borde)
                        self.canvas.create_text(x+1, y, text=simbolo, font=fuente, fill=color_borde)
                        self.canvas.create_text(x, y-1, text=simbolo, font=fuente, fill=color_borde)
                        self.canvas.create_text(x, y+1, text=simbolo, font=fuente, fill=color_borde)
                        
                        self.canvas.create_text(x, y, text=simbolo, font=fuente, fill=color_txt)

    def gestionar_clic(self, event):
        columna = event.x // TAMANO_CASILLA
        fila = event.y // TAMANO_CASILLA
        
        if self.origen_seleccionado is None:
            pieza = TABLERO[fila][columna]
            if pieza != "" and pieza.endswith(f"_{self.turno}"):
                self.origen_seleccionado = (fila, columna)
                self.actualizar_interfaz()
        
        else:
            f_origen, c_origen = self.origen_seleccionado
            
            if (fila, columna) == (f_origen, c_origen):
                self.origen_seleccionado = None
                self.actualizar_interfaz()
                return

            pieza = TABLERO[f_origen][c_origen]
            
            if self.es_movimiento_legal(pieza, f_origen, c_origen, fila, columna):
                TABLERO[fila][columna] = pieza
                TABLERO[f_origen][c_origen] = ""
                self.turno = "n" if self.turno == "b" else "b"
                
            self.origen_seleccionado = None
            self.actualizar_interfaz()

    def es_movimiento_legal(self, pieza, f1, c1, f2, c2):
        tipo_pieza = pieza.split("_")[0]
        color_pieza = pieza.split("_")[1]
        
        destino = TABLERO[f2][c2]
        if destino != "" and destino.endswith(f"_{color_pieza}"):
            return False
            
        df = f2 - f1  
        dc = c2 - c1  
        
        if tipo_pieza == "peon":
            direccion = -1 if color_pieza == "b" else 1
            fila_inicial = 6 if color_pieza == "b" else 1
            
            if dc == 0 and df == direccion and destino == "":
                return True
            if dc == 0 and f1 == fila_inicial and df == 2 * direccion and destino == "":
                if TABLERO[f1 + direccion][c1] == "":
                    return True
        
            if abs(dc) == 1 and df == direccion and destino != "":
                return True
            return False

        elif tipo_pieza == "caballo":
            return (abs(df) == 2 and abs(dc) == 1) or (abs(df) == 1 and abs(dc) == 2)

        elif tipo_pieza == "rey":
            return abs(df) <= 1 and abs(dc) <= 1

        elif tipo_pieza == "torre":
            if f1 != f2 and c1 != c2: return False 
            return self.camino_libre(f1, c1, f2, c2)

        elif tipo_pieza == "alfil":
            if abs(df) != abs(dc): return False 
            return self.camino_libre(f1, c1, f2, c2)

        elif tipo_pieza == "reina":
            if (f1 == f2 or c1 == c2) or (abs(df) == abs(dc)):
                return self.camino_libre(f1, c1, f2, c2)
            return False

        return False

    def camino_libre(self, f1, c1, f2, c2):
        paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
        paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)
        
        actual_f, actual_c = f1 + paso_f, c1 + paso_c
        while (actual_f, actual_c) != (f2, c2):
            if TABLERO[actual_f][actual_c] != "":
                return False
            actual_f += paso_f
            actual_c += paso_c
        return True

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AjedrezDosClics(ventana)
    ventana.mainloop()
