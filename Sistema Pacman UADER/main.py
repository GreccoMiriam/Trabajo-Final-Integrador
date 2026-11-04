import tkinter as tk
from tkinter import simpledialog, messagebox
from modelo import Pacman, Fantasma, TableroJuego
from persistencia import GestorPuntuaciones

# Definición del mapa (1: Paredes, 2: Puntos, 0: Espacios libres)
LABERINTO_EJEMPLO = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class JuegoPacmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Pacman - UADER")

        # Gestión de jugadores
        self.nombre_jugador = simpledialog.askstring("Jugador", "Ingrese su nombre para iniciar:")
        if not self.nombre_jugador:
            self.nombre_jugador = "Anónimo"

        self.gestor = GestorPuntuaciones()
        self.tablero = TableroJuego(LABERINTO_EJEMPLO)
        self.pacman = Pacman(pos_x=1, pos_y=1)
        self.fantasmas = [
            Fantasma("Blinky", pos_x=8, pos_y=1, color="red"),
            Fantasma("Pinky", pos_x=8, pos_y=6, color="pink")
        ]

        self.tam_bloque = 40
        self.ancho_canvas = len(LABERINTO_EJEMPLO[0]) * self.tam_bloque
        self.alto_canvas = len(LABERINTO_EJEMPLO) * self.tam_bloque

        # Interfaz Gráfica
        self.canvas = tk.Canvas(root, width=self.ancho_canvas, height=self.alto_canvas, bg="black")
        self.canvas.pack()

        self.label_info = tk.Label(root, font=("Arial", 14), fg="black")
        self.label_info.pack(pady=5)

        # Controles de teclado
        self.root.bind("<KeyPress>", self.cambiar_direccion)

        # Botones de control de partida y ranking
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Reiniciar", command=self.reiniciar_juego).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Ver Ranking (Top 5)", command=self.mostrar_ranking).pack(side=tk.LEFT, padx=5)

        self.partida_guardada = False
        self.ejecutar_ciclo()

    def cambiar_direccion(self, event):
        tecla = event.keysym
        if tecla == "Up":
            self.pacman.direccion = "UP"
        elif tecla == "Down":
            self.pacman.direccion = "DOWN"
        elif tecla == "Left":
            self.pacman.direccion = "LEFT"
        elif tecla == "Right":
            self.pacman.direccion = "RIGHT"

    def ejecutar_ciclo(self):
        if not self.tablero.juego_terminado and not self.tablero.victoria:
            self.tablero.actualizar_ciclo(self.pacman, self.fantasmas)
            self.actualizar_interfaz()
            self.root.after(350, self.ejecutar_ciclo)
        else:
            if not self.partida_guardada:
                self.gestor.guardar_puntuacion(self.nombre_jugador, self.tablero.puntaje)
                self.partida_guardada = True
                if self.tablero.victoria:
                    messagebox.showinfo("¡Victoria!", f"¡Felicitaciones {self.nombre_jugador}! Ganaste con {self.tablero.puntaje} puntos.")
                else:
                    messagebox.showerror("Game Over", f"Te quedaste sin vidas, {self.nombre_jugador}. Puntaje: {self.tablero.puntaje}")

    def actualizar_interfaz(self):
        self.canvas.delete("all")
        lab = self.tablero.laberinto

        # Dibujar tablero (paredes y puntos)
        for y in range(len(lab)):
            for x in range(len(lab[0])):
                x1 = x * self.tam_bloque
                y1 = y * self.tam_bloque
                x2 = x1 + self.tam_bloque
                y2 = y1 + self.tam_bloque

                if lab[y][x] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="blue")
                elif lab[y][x] == 2:
                    self.canvas.create_oval(x1 + 14, y1 + 14, x2 - 14, y2 - 14, fill="white")

        # Dibujar Pacman
        px1 = self.pacman.pos_x * self.tam_bloque + 5
        py1 = self.pacman.pos_y * self.tam_bloque + 5
        px2 = px1 + self.tam_bloque - 10
        py2 = py1 + self.tam_bloque - 10
        self.canvas.create_oval(px1, py1, px2, py2, fill=self.pacman.color)

        # Dibujar Fantasmas
        for f in self.fantasmas:
            fx1 = f.pos_x * self.tam_bloque + 5
            fy1 = f.pos_y * self.tam_bloque + 5
            fx2 = fx1 + self.tam_bloque - 10
            fy2 = fy1 + self.tam_bloque - 10
            self.canvas.create_oval(fx1, fy1, fx2, fy2, fill=f.color)

        # Estado en pantalla
        self.label_info.config(text=f"Jugador: {self.nombre_jugador}  |  Puntaje: {self.tablero.puntaje}  |  Vidas: {self.pacman.vidas}")

    def reiniciar_juego(self):
        self.tablero = TableroJuego(LABERINTO_EJEMPLO)
        self.pacman.reiniciar_posicion()
        self.pacman._vidas = 3
        for f in self.fantasmas:
            f.reiniciar_posicion()
        self.partida_guardada = False
        self.ejecutar_ciclo()

    def mostrar_ranking(self):
        ranking = self.gestor.obtener_mejores_puntuaciones(5)
        texto_ranking = "Mejores Puntuaciones (Top 5):\n\n"
        for i, item in enumerate(ranking, 1):
            texto_ranking += f"{i}. {item['nombre']} - {item['puntaje']} pts\n"
        if not ranking:
            texto_ranking += "Aún no hay puntuaciones registradas."
        messagebox.showinfo("Ranking", texto_ranking)

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoPacmanGUI(root)
    root.mainloop()