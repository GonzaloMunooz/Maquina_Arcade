class Reina:
    def __init__(self, fila, col):
        self.fila = fila
        self.col = col

class TableroReinas:
    def __init__(self, n):
        self.n = n
        self.reinas = []

    def puede_colocar(self, fila, col):
        for r in self.reinas:
            if r.fila == fila or r.col == col or abs(r.fila - fila) == abs(r.col - col):
                return False
        return True

    def colocar_reina(self, fila, col):
        if self.puede_colocar(fila, col):
            self.reinas.append(Reina(fila, col))
            return True
        return False

    def esta_completo(self):
        return len(self.reinas) == self.n
