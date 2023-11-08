from deck_of_cards import deck_of_cards as doc

class bac_deck(doc.DeckOfCards):
    def __init__(self, deckNum = 1):
        super().__init__()

        for i in range(1,deckNum):
            self.add_deck()
        for card in self.deck:
            if card.value > 10:
                card.value = 10
    
