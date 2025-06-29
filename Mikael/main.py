from Mikael.models.card_model  import card
from Mikael.functs.card_choose import choose_move

board: card = card(cor="verde", numero=5, posicao= 0)
Hand = [
        card(cor="vermelho", numero=1, posicao = 1),
        card(cor="Azul", numero=2, posicao = 2),
        card(cor="amarelo", numero=5, posicao = 3)
    ]

choose: card | None = choose_move(board, Hand).__repr__()
print (choose)
