class Rio:
    rios = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 100
        self.altura = 100
        Rio.rios.append(self)
    def construir_ponte(self, mapa):
        mapa[(self.x, self.y)] = 32
        mapa[(self.x + 50, self.y)] = 33
        mapa[(self.x, self.y + 50)] = 34
        mapa[(self.x + 50, self.y + 50)] = 35
        Rio.rios.remove(self)
