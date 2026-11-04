from abc import ABC, abstractmethod
import random

class Entidad(ABC):
    def __init__(self, pos_x, pos_y, color):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._color = color

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, valor):
        self._pos_x = valor

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, valor):
        self._pos_y = valor

    @property
    def color(self):
        return self._color

    def mover(self, dx, dy):
        self._pos_x += dx
        self._pos_y += dy

    @abstractmethod
    def actualizar(self, *args, **kwargs):
        pass


class Pacman(Entidad):
    def __init__(self, pos_x, pos_y, color="yellow", vidas=3):
        super().__init__(pos_x, pos_y, color)
        self._direccion = "STOP"
        self._vidas = vidas
        self._pos_inicial = (pos_x, pos_y)

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, nueva_dir):
        self._direccion = nueva_dir

    @property
    def vidas(self):
        return self._vidas

    def perder_vida(self):
        if self._vidas > 0:
            self._vidas -= 1

    def reiniciar_posicion(self):
        self._pos_x, self._pos_y = self._pos_inicial
        self._direccion = "STOP"

    def actualizar(self, laberinto):
        dx, dy = 0, 0
        if self._direccion == "UP":
            dy = -1
        elif self._direccion == "DOWN":
            dy = 1
        elif self._direccion == "LEFT":
            dx = -1
        elif self._direccion == "RIGHT":
            dx = 1

        nueva_x = self._pos_x + dx
        nueva_y = self._pos_y + dy

        # Validar límites y paredes (1: pared)
        if 0 <= nueva_y < len(laberinto) and 0 <= nueva_x < len(laberinto[0]):
            if laberinto[nueva_y][nueva_x] != 1:
                self._pos_x = nueva_x
                self._pos_y = nueva_y
                return True
        return False


class Fantasma(Entidad):
    def __init__(self, nombre, pos_x, pos_y, color="red"):
        super().__init__(pos_x, pos_y, color)
        self._nombre = nombre
        self._pos_inicial = (pos_x, pos_y)

    @property
    def nombre(self):
        return self._nombre

    @property
    def pos_inicial(self):
        return self._pos_inicial

    def reiniciar_posicion(self):
        self._pos_x, self._pos_y = self._pos_inicial

    def actualizar(self, laberinto):
        # Movimiento autónomo aleatorio
        direcciones = [("UP", 0, -1), ("DOWN", 0, 1), ("LEFT", -1, 0), ("RIGHT", 1, 0)]
        validas = []
        for _, dx, dy in direcciones:
            nx, ny = self._pos_x + dx, self._pos_y + dy
            if 0 <= ny < len(laberinto) and 0 <= nx < len(laberinto[0]):
                if laberinto[ny][nx] != 1:
                    validas.append((dx, dy))
        
        if validas:
            dx, dy = random.choice(validas)
            self._pos_x += dx
            self._pos_y += dy


class TableroJuego:
    def __init__(self, laberinto_inicial):
        self._laberinto = [fila[:] for fila in laberinto_inicial]
        self._puntaje = 0
        self._juego_terminado = False
        self._victoria = False

    @property
    def laberinto(self):
        return self._laberinto

    @property
    def puntaje(self):
        return self._puntaje

    @property
    def juego_terminado(self):
        return self._juego_terminado

    @property
    def victoria(self):
        return self._victoria

    def actualizar_ciclo(self, pacman, fantasmas):
        if self._juego_terminado or self._victoria:
            return

        # Mover Pacman y consumir puntos (2: punto)
        movido = pacman.actualizar(self._laberinto)
        if movido:
            px, py = pacman.pos_x, pacman.pos_y
            if self._laberinto[py][px] == 2:
                self._laberinto[py][px] = 0
                self._puntaje += 10

        # Mover fantasmas de forma autónoma
        for fantasma in fantasmas:
            fantasma.actualizar(self._laberinto)

        # Verificar colisiones con fantasmas
        for fantasma in fantasmas:
            if pacman.pos_x == fantasma.pos_x and pacman.pos_y == fantasma.pos_y:
                pacman.perder_vida()
                self._reiniciar_posiciones_entidades(pacman, fantasmas)
                if pacman.vidas <= 0:
                    self._juego_terminado = True
                break

        # Verificar si se consumieron todos los puntos (Victoria)
        puntos_restantes = any(2 in fila for fila in self._laberinto)
        if not puntos_restantes:
            self._victoria = True

    def _reiniciar_posiciones_entidades(self, pacman, fantasmas):
        pacman.reiniciar_posicion()
        for fantasma in fantasmas:
            fantasma.reiniciar_posicion()