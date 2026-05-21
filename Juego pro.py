import tkinter as tk
import os

# =========================================================
# CONFIGURACIÓN (Fácil de editar)
# =========================================================
TAMANO_CASILLA = 70       # Tamaño de cada casilla en píxeles
COLOR_CLARO = "#ffffff"    # Blanco
COLOR_OSCURO = "#000000"   # Negro
COLOR_SELECCION = "#ffeb3b" # Amarillo para la casilla seleccionada
CARPETA_IMAGENES = "imagenes"  # Carpeta de tus fichas personalizadas
# =========================================================

TABLERO_INICIAL = [
    ["torre_n", "caballo_n", "alfil_n", "reina_n", "rey_n", "alfil_n", "caballo_n", "torre_n"],
    ["peon_n",  "peon_n",    "peon_n",  "peon_n",  "peon_n", "peon_n",  "peon_n",    "peon_n"],
    ["",        "",          "",        "",        "",       "",        "",          ""],
    ["",        "",          "",        "",        "",       "",        "",          ""],
    ["",        "",          "",        "",        "",       "",        "",          ""],
    ["",        "",          "",        "",        "",       "",        "",          ""],
    ["peon_b",  "peon_b",    "peon_b",  "peon_b",  "peon_b", "peon_b",  "peon_b",    "peon_b"],
    ["torre_b", "caballo_b", "alfil_b", "reina_b", "rey_b", "alfil_b", "caballo_b", "torre_b"]
]

class AjedrezDosClics:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajedrez - Selección por Clic")
        
        self.canvas = tk.Canvas(root, width=8*TAMANO_CASILLA, height=8*TAMANO_CASILLA)
        self.canvas.pack()
        
        self.imagenes_piezas = {}
        self.pieza_seleccionada = None
        self.recuadro_seleccion = None
        
        self.cargar_imagenes()
        self.dibujar_tablero()
        self.colocar_piezas()
        
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

    def dibujar_tablero(self):
        for fila in range(8):
            for columna in range(8):
                color = COLOR_CLARO if (fila + columna) % 2 == 0 else COLOR_OSCURO
                x1, y1 = columna * TAMANO_CASILLA, fila * TAMANO_CASILLA
                x2, y2 = x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="tablero")

    def colocar_piezas(self):
        for fila in range(8):
            for columna in range(8):
                nombre_pieza = TABLERO_INICIAL[fila][columna]
                if nombre_pieza != "":
                    x = (columna * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    y = (fila * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    
                    if self.imagenes_piezas.get(nombre_pieza) is not None:
                        self.canvas.create_image(x, y, image=self.imagenes_piezas[nombre_pieza], tags="pieza")
                    else:
                        inicial = nombre_pieza[0].upper()
                        color_txt = "blue" if nombre_pieza.endswith("_b") else "red"
                        self.canvas.create_text(x, y, text=inicial, font=("Arial", 22, "bold"), fill=color_txt, tags="pieza")

    def gestionar_clic(self, event):
        columna = event.x // TAMANO_CASILLA
        fila = event.y // TAMANO_CASILLA
        
        centro_x = (columna * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
        centro_y = (fila * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
        
        elementos = self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        
        pieza_clicada = None
        for item in elementos:
            # 🔧 CORREGIDO AQUÍ: Se cambió get_tags por gettags
            if "pieza" in self.canvas.gettags(item):
                pieza_clicada = item
                break

        if self.pieza_seleccionada is None:
            if pieza_clicada is not None:
                self.pieza_seleccionada = pieza_clicada
                
                x1, y1 = columna * TAMANO_CASILLA, fila * TAMANO_CASILLA
                x2, y2 = x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA
                self.recuadro_seleccion = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_SELECCION, outline="")
                
                self.canvas.tag_raise(self.recuadro_seleccion, "tablero")
                self.canvas.tag_raise(self.pieza_seleccionada)
        
        else:
            if pieza_clicada == self.pieza_seleccionada:
                self.limpiar_seleccion()
                return
            
            if pieza_clicada is not None:
                self.canvas.delete(pieza_clicada)
            
            self.canvas.coords(self.pieza_seleccionada, centro_x, centro_y)
            self.limpiar_seleccion()

    def limpiar_seleccion(self):
        if self.recuadro_seleccion:
            self.canvas.delete(self.recuadro_seleccion)
            self.recuadro_seleccion = None
        self.pieza_seleccionada = None

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AjedrezDosClics(ventana)
    ventana.mainloop()
