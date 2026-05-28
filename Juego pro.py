import tkinter as tk
import os

TAMANO_CASILLA = 70       
COLOR_CLARO = "#FFFFFF"    
COLOR_OSCURO = "#000000"   
COLOR_SELECCION = "#7ae7ff" 
COLOR_POSIBLE = "#a3e4d7" 
CARPETA_IMAGENES = "imagenes"
TIEMPO_INICIAL = 600 

SIMBOLOS_PIEZAS = {
    "peon_b": "♙", "torre_b": "♖", "caballo_b": "♘", "alfil_b": "♗", "reina_b": "♕", "rey_b": "♔",
    "peon_n": "♟", "torre_n": "♜", "caballo_n": "♞", "alfil_n": "♝", "reina_n": "♛", "rey_n": "♚"
}

class AjedrezCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajedrez Profesional - Reglas Completas")
        
        self.tablero = [
            ["torre_n", "caballo_n", "alfil_n", "reina_n", "rey_n", "alfil_n", "caballo_n", "torre_n"],
            ["peon_n"] * 8,
            [""] * 8, [""] * 8, [""] * 8, [""] * 8,
            ["peon_b"] * 8,
            ["torre_b", "caballo_b", "alfil_b", "reina_b", "rey_b", "alfil_b", "caballo_b", "torre_b"]
        ]
        self.turno = "b"  
        self.origen_seleccionado = None
        self.movimientos_posibles = [] 
        self.imagenes_piezas = {}
        
        self.rey_movido = {"b": False, "n": False}
        self.torre_movida = {"b": [False, False], "n": [False, False]} 
        self.ultimo_avance_doble_peon = None 
        
        self.tiempo = {"b": TIEMPO_INICIAL, "n": TIEMPO_INICIAL}
        self.juego_activo = True
        
        self.panel_superior = tk.Frame(root, bg="#2c3e50")
        self.panel_superior.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_reloj_b = tk.Label(self.panel_superior, text="Blancas: 10:00", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
        self.lbl_reloj_b.pack(side=tk.LEFT, padx=20)
        
        self.lbl_estado = tk.Label(self.panel_superior, text="Turno: Blancas", font=("Arial", 14), fg="#f1c40f", bg="#2c3e50")
        self.lbl_estado.pack(side=tk.TOP)
        
        self.lbl_reloj_n = tk.Label(self.panel_superior, text="Negras: 10:00", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
        self.lbl_reloj_n.pack(side=tk.RIGHT, padx=20)
        
        self.canvas = tk.Canvas(root, width=8*TAMANO_CASILLA, height=8*TAMANO_CASILLA)
        self.canvas.pack()
        
        self.cargar_imagenes()
        self.actualizar_interfaz()
        
        self.canvas.bind("<Button-1>", self.gestionar_clic)
        self.actualizar_reloj()

    def cargar_imagenes(self):
        piezas = ["peon", "torre", "caballo", "alfil", "reina", "rey"]
        for pieza in piezas:
            for color in ["b", "n"]:
                nombre_clave = f"{pieza}_{color}"
                ruta = os.path.join(CARPETA_IMAGENES, f"{nombre_clave}.png")
                self.imagenes_piezas[nombre_clave] = tk.PhotoImage(file=ruta) if os.path.exists(ruta) else None

    def actualizar_interfaz(self):
        self.canvas.delete("all")
        
        for fila in range(8):
            for columna in range(8):
                color = COLOR_CLARO if (fila + columna) % 2 == 0 else COLOR_OSCURO
                x1, y1 = columna * TAMANO_CASILLA, fila * TAMANO_CASILLA
                self.canvas.create_rectangle(x1, y1, x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA, fill=color, outline="")

        for (f, c) in self.movimientos_posibles:
            x1, y1 = c * TAMANO_CASILLA, f * TAMANO_CASILLA
            radio = 12
            centro_x, centro_y = x1 + TAMANO_CASILLA // 2, y1 + TAMANO_CASILLA // 2
            self.canvas.create_oval(centro_x - radio, centro_y - radio, centro_x + radio, centro_y + radio, fill=COLOR_POSIBLE, outline="")

        if self.origen_seleccionado:
            f, c = self.origen_seleccionado
            x1, y1 = c * TAMANO_CASILLA, f * TAMANO_CASILLA
            self.canvas.create_rectangle(x1, y1, x1 + TAMANO_CASILLA, y1 + TAMANO_CASILLA, fill=COLOR_SELECCION, outline="")

        for fila in range(8):
            for columna in range(8):
                nombre_pieza = self.tablero[fila][columna]
                if nombre_pieza != "":
                    x = (columna * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    y = (fila * TAMANO_CASILLA) + (TAMANO_CASILLA // 2)
                    
                    if self.imagenes_piezas.get(nombre_pieza):
                        self.canvas.create_image(x, y, image=self.imagenes_piezas[nombre_pieza])
                    else:
                        simbolo = SIMBOLOS_PIEZAS.get(nombre_pieza, "?")
                        color_pieza = nombre_pieza.split("_")[1]
                        
                        color_txt = "#FFFFFF" if color_pieza == "b" else "#000000"
                        color_borde = "#000000" if color_pieza == "b" else "#FFFFFF"
                        fuente = ("Arial", 36, "bold")
                        
                        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            self.canvas.create_text(x+dx, y+dy, text=simbolo, font=fuente, fill=color_borde)
                        self.canvas.create_text(x, y, text=simbolo, font=fuente, fill=color_txt)

    def actualizar_reloj(self):
        if not self.juego_activo:
            return
        
        self.tiempo[self.turno] -= 1
        
        if self.tiempo[self.turno] <= 0:
            self.tiempo[self.turno] = 0
            self.juego_activo = False
            ganador = "Negras" if self.turno == "b" else "Blancas"
            self.lbl_estado.config(text=f"¡Tiempo agotado! Ganan las {ganador}", fg="#e74c3c")
        
        for c, lbl in [("b", self.lbl_reloj_b), ("n", self.lbl_reloj_n)]:
            minutos = self.tiempo[c] // 60
            segundos = self.tiempo[c] % 60
            lbl.config(text=f"{'Blancas' if c=='b' else 'Negras'}: {minutos:02d}:{segundos:02d}")
            
        self.root.after(1000, self.actualizar_reloj)

    def gestionar_clic(self, event):
        if not self.juego_activo: return
        
        columna = event.x // TAMANO_CASILLA
        fila = event.y // TAMANO_CASILLA
        
        if self.origen_seleccionado is None:
            pieza = self.tablero[fila][columna]
            if pieza != "" and pieza.endswith(f"_{self.turno}"):
                self.origen_seleccionado = (fila, columna)
                
                self.movimientos_posibles = []
                for f2 in range(8):
                    for c2 in range(8):
                        if self.es_movimiento_legal_completo(pieza, fila, columna, f2, c2):
                            self.movimientos_posibles.append((f2, c2))
                self.actualizar_interfaz()
        else:
            f_orig, c_orig = self.origen_seleccionado
            if (fila, columna) == (f_orig, c_orig):
                self.origen_seleccionado = None
                self.movimientos_posibles = [] 
                self.actualizar_interfaz()
                return

            pieza = self.tablero[f_orig][c_orig]
            
            if self.es_movimiento_legal_completo(pieza, f_orig, c_orig, fila, columna):
                self.ejecutar_movimiento(pieza, f_orig, c_orig, fila, columna)
                
                self.turno = "n" if self.turno == "b" else "b"
                self.lbl_estado.config(text=f"Turno: {'Blancas' if self.turno == 'b' else 'Negras'}")
                
                if self.esta_en_jaque(self.turno, self.tablero):
                    if self.tiene_movimientos_legales(self.turno):
                        self.lbl_estado.config(text=f"¡Jaque a las {'Blancas' if self.turno == 'b' else 'Negras'}!", fg="#e74c3c")
                    else:
                        self.lbl_estado.config(text=f"¡Jaque Mate! Ganan las {'Negras' if self.turno == 'b' else 'Blancas'}", fg="#2ecc71")
                        self.juego_activo = False
                elif not self.tiene_movimientos_legales(self.turno):
                    self.lbl_estado.config(text="Tablas por Ahogado", fg="#95a5a6")
                    self.juego_activo = False
                    
            self.origen_seleccionado = None
            self.movimientos_posibles = [] 
            self.actualizar_interfaz()

    def es_movimiento_legal_completo(self, pieza, f1, c1, f2, c2):
        legal_base, tipo_mov = self.es_movimiento_legal_base(pieza, f1, c1, f2, c2)
        if not legal_base:
            return False
            
        tablero_clon = [fila[:] for fila in self.tablero]
        color = pieza.split("_")[1]
        
        tablero_clon[f2][c2] = pieza
        tablero_clon[f1][c1] = ""
        if tipo_mov == "al_paso" and self.ultimo_avance_doble_peon:
            _, cp = self.ultimo_avance_doble_peon
            tablero_clon[f1][cp] = ""
            
        if self.esta_en_jaque(color, tablero_clon):
            return False
            
        if tipo_mov == "enroque":
            paso_c = 1 if c2 > c1 else -1
            if self.esta_en_jaque(color, self.tablero) or \
               self.casilla_amenazada(color, f1, c1 + paso_c, self.tablero):
                return False
                
        return True

    def es_movimiento_legal_base(self, pieza, f1, c1, f2, c2):
        tipo, color = pieza.split("_")
        destino = self.tablero[f2][c2]
        df, dc = f2 - f1, c2 - c1
        
        if destino != "" and destino.endswith(f"_{color}"): 
            return False, None

        if tipo == "peon":
            dir_p = -1 if color == "b" else 1
            f_ini = 6 if color == "b" else 1
            
            if dc == 0 and df == dir_p and destino == "": 
                return True, "normal"
            if dc == 0 and f1 == f_ini and df == 2 * dir_p and destino == "" and self.tablero[f1 + dir_p][c1] == "":
                return True, "doble_peon"
            if abs(dc) == 1 and df == dir_p and destino != "": 
                return True, "normal"
            if abs(dc) == 1 and df == dir_p and destino == "" and self.ultimo_avance_doble_peon == (f1, c2):
                return True, "al_paso"
            return False, None

        elif tipo == "caballo":
            if (abs(df) == 2 and abs(dc) == 1) or (abs(df) == 1 and abs(dc) == 2):
                return True, "normal"
            return False, None

        elif tipo == "rey":
            if abs(df) <= 1 and abs(dc) <= 1: 
                return True, "normal"
            if df == 0 and abs(dc) == 2 and not self.rey_movido[color]:
                if dc == 2 and not self.torre_movida[color][1] and self.camino_libre(f1, c1, f1, 7): # Corto
                    return True, "enroque"
                if dc == -2 and not self.torre_movida[color][0] and self.camino_libre(f1, c1, f1, 0): # Largo
                    return True, "enroque"
            return False, None

        elif tipo == "torre":
            if (f1 == f2 or c1 == c2) and self.camino_libre(f1, c1, f2, c2): return True, "normal"
        elif tipo == "alfil":
            if abs(df) == abs(dc) and self.camino_libre(f1, c1, f2, c2): return True, "normal"
        elif tipo == "reina":
            if (f1 == f2 or c1 == c2 or abs(df) == abs(dc)) and self.camino_libre(f1, c1, f2, c2): return True, "normal"
            
        return False, None

    def camino_libre(self, f1, c1, f2, c2):
        paso_f = 0 if f1 == f2 else (1 if f2 > f1 else -1)
        paso_c = 0 if c1 == c2 else (1 if c2 > c1 else -1)
        curr_f, curr_c = f1 + paso_f, c1 + paso_c
        while (curr_f, curr_c) != (f2, c2):
            if self.tablero[curr_f][curr_c] != "": return False
            curr_f += paso_f
            curr_c += paso_c
        return True

    def ejecutar_movimiento(self, pieza, f1, c1, f2, c2):
        tipo, color = pieza.split("_")
        _, tipo_mov = self.es_movimiento_legal_base(pieza, f1, c1, f2, c2)
        
        self.tablero[f2][c2] = pieza
        self.tablero[f1][c1] = ""
        
        self.ultimo_avance_doble_peon = (f2, c2) if tipo_mov == "doble_peon" else None
        
        if tipo_mov == "al_paso":
            self.tablero[f1][c2] = ""
            
        if tipo_mov == "enroque":
            if c2 == 6: 
                self.tablero[f2][5] = f"torre_{color}"
                self.tablero[f2][7] = ""
            elif c2 == 2: 
                self.tablero[f2][3] = f"torre_{color}"
                self.tablero[f2][0] = ""

        if tipo == "peon" and (f2 == 0 or f2 == 7):
            self.tablero[f2][c2] = f"reina_{color}"
            
        if tipo == "rey": self.rey_movido[color] = True
        if tipo == "torre":
            if c1 == 0: self.torre_movida[color][0] = True
            if c1 == 7: self.torre_movida[color][1] = True

    def casilla_amenazada(self, color_defensor, f, c, matriz):
        color_atacante = "n" if color_defensor == "b" else "b"
        for fila_a in range(8):
            for col_a in range(8):
                p_atacante = matriz[fila_a][col_a]
                if p_atacante != "" and p_atacante.endswith(f"_{color_atacante}"):
                    es_legal, _ = self.es_movimiento_legal_base(p_atacante, fila_a, col_a, f, c)
                    if es_legal:
                        return True
        return False

    def esta_en_jaque(self, color, matriz):
        for fila in range(8):
            for col in range(8):
                if matriz[fila][col] == f"rey_{color}":
                    return self.casilla_amenazada(color, fila, col, matriz)
        return False

    def tiene_movimientos_legales(self, color):
        for f1 in range(8):
            for c1 in range(8):
                pieza = self.tablero[f1][c1]
                if pieza != "" and pieza.endswith(f"_{color}"):
                    for f2 in range(8):
                        for c2 in range(8):
                            if self.es_movimiento_legal_completo(pieza, f1, c1, f2, c2):
                                return True
        return False

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AjedrezCompleto(ventana)
    ventana.mainloop()
