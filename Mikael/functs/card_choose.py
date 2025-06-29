from Mikael.models.card_model import card

def choose_move (board_card: card, hand_cards: list[card]) -> card | None: 
    # Input  board_card : Referente a carta que esta jogada. A logica da jogada levara em consideracao essa carta.
    # Input  hand_cards : As cartas que devem ser levadas em consideracao para executar a jogada.
    # Output card      : Carta que deve e pode ser jogada.

    # Prioridades da jogada Cor, numero.

    for card in hand_cards:
        if card.cor.lower() == board_card.cor.lower():
            return card  # Cor compatível, retorna esta carta
        
    for card in hand_cards:
        if card.numero == board_card.numero:
            return card  # Numero compatível, retorna esta carta    

    return None
    #expeciais nao sao levadas em consideracao para essa versao 1.0.0
