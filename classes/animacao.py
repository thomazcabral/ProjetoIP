class Animacao:
    animacoes_ativas = []
    def __init__(self, frames, x, y):
        self.x = x
        self.y = y
        self.estagio = 0
        self.frames = frames
        Animacao.animacoes_ativas.append(self)
    def rodar(self, janela, offset_x, offset_y):
        janela.blit(self.frames[int(self.estagio)], (self.x - offset_x, self.y - offset_y))
        self.estagio += 0.25
        if self.estagio >= len(self.frames):
            Animacao.animacoes_ativas.remove(self)