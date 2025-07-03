from stock_uno.models.card_model  import card
from stock_uno.functs.card_choose import choose_move
from yolo_uno.yolo_handler import YoloUtils

board: card = card(cor="GREEN", numero=5, posicao= 0)

seeDeck = YoloUtils().seeDeck()
Hand: list[card] = seeDeck

choose: card | None = choose_move(board, Hand).__repr__()
print (choose)
