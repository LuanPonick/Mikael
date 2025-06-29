from Mikael.models.card_model  import Card
from Mikael.functs.card_choose import choose_move

board: Card = Card(cor="verde", numero=5, posicao= 0)
Hand = [
        Card(cor="vermelho", numero=1, posicao = 1),
        Card(cor="Azul", numero=2, posicao = 2),
        Card(cor="amarelo", numero=5, posicao = 3)
    ]

choose: Card | None = choose_move(board, Hand).__repr__()
print (choose)
