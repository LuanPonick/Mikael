class Card:
    def __init__(self, cor: str, numero: int, posicao: int):
        self.cor = cor
        self.numero = numero
        self.posicao = posicao

    def __repr__(self):
        return f"(cor='{self.cor}', numero={self.numero}, posicao={self.posicao})"