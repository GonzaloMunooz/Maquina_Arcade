class TorreHanoi:
    def __init__(self, discos):
        self.discos = list(range(discos, 0, -1))
        self.varillas = [self.discos.copy(), [], []]
        self.movimientos = []

    def mover(self, origen, destino):
        if not self.varillas[origen]:
            return False
        disco = self.varillas[origen][-1]
        if self.varillas[destino] and self.varillas[destino][-1] < disco:
            return False
        self.varillas[origen].pop()
        self.varillas[destino].append(disco)
        self.movimientos.append((origen, destino))
        return True

    def esta_completo(self, destino):
        return len(self.varillas[destino]) == len(self.discos)
