class CaballoTour:
    def __init__(self, n=8, inicio=(0, 0)):
        self.n = n
        self.inicio = inicio
        self.movimientos = []
        self.visitadas = set()

    def movimientos_legales(self, pos):
        x, y = pos
        saltos = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        legales = []
        for dx, dy in saltos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n and (nx, ny) not in self.visitadas:
                legales.append((nx, ny))
        return legales

    def buscar_tour(self, pos=None):
        """
        Realiza el tour completo usando backtracking con heurística de Warnsdorff:
        siempre mueve al vecino con menor número de salidas posibles.
        Devuelve True si se completa el tour, False si debe backtrack.
        """
        if pos is None:
            pos = self.inicio

        # Marca la casilla actual
        self.movimientos.append(pos)
        self.visitadas.add(pos)

        # Caso base: todas las casillas visitadas
        if len(self.movimientos) == self.n * self.n:
            return True

        # Calcula vecinos y ordénalos por grado (Warnsdorff)
        vecinos = self.movimientos_legales(pos)
        vecinos_ordenados = sorted(
            vecinos,
            key=lambda v: len(self.movimientos_legales(v))
        )

        # Explora recursivamente en orden creciente de grado
        for siguiente in vecinos_ordenados:
            if self.buscar_tour(siguiente):
                return True

        # Si ninguno funciona, backtrack
        self.visitadas.remove(pos)
        self.movimientos.pop()
        return False
