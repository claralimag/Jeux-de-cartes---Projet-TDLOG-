#BoardPlayer : defines the board of a player (cards played, functions : add a card to the board to a sequence, add a collection of cards)
#BoardPlayer : defines the board of a player (cards played, functions : add a card to the board to a sequence, add a collection of cards)
from cards import Card
from copy import deepcopy

class BoardPlayer :
    def __init__(self):
        self.cardgames : list[tuple[list[Card], bool, int]]  = [] #bool stores if the game is clean and int stores the number of points
        self.numberofgames : int = 0

    
    def get_score(self, whichgame) -> int:
        s : int = 0
        cards = self.cardsgame[whichgame][0]
        is_pure = self.cardsgame[whichgame][1]
        for el in cards:
            s+= el.point

        if len(cards) >= 7 : #Is canastra ?
            if len(cards) == 13:
                if is_pure:
                    s+= 500
                else: 
                    s+= 250
            if len(cards) == 14:
                if is_pure:
                    s+= 1000
                else: 
                    s+= 500
            else:
                if is_pure:
                    s+= 200
                else: 
                    s+= 100

        return s 

    def add_to_existing_game(self, cards_list : list[Card], whichgame: int)  -> int:
        #if it can be played, it is played and returns the new score
        # that should be added, and also modifies if it is pure of not.
        #if not, it returns 0
        cards_list2 = deepcopy(cards_list) #FROM HERE
        merged_cards = cards_list+self.cardgames[whichgame][0]
        ordered_cards = Card.order(merged_cards)
        if ordered_cards:
            self.cardgames[whichgame][0] = ordered_cards
            self.cardgames[whichgame][1] = Card.is_sequence(ordered_cards)[1]
            new_score = ordered_cards.get_score() - cards_list.get_score()
            return new_score
        return 0
   


