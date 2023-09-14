class Rio:
    rios = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 100
        self.altura = 100
        Rio.rios.append(self)