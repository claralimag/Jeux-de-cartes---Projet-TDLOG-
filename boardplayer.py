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

    def add_to_board(self, cards_list : list[Card], whichgame: int)  -> int:
        #if it can be played, it is played and returns the new score
        # that should be added, and also modifies if it is pure of not.
        #if not, it returns 0
        #Start a new sequence
        if whichgame == -1:
            cards_list_copy = deepcopy(cards_list) 
            ordered_cards = Card.order(cards_list_copy)
            #if I am allowed to order
            if ordered_cards:
                is_clean = Card.is_sequence(ordered_cards)[1]
                self.numberofgames +=1
                self.cardgames.append([ordered_cards,is_clean,0]) #0 is paceholder until we get the score
                this_game_idx = self.numberofgames-1 #indexing stats at 0
                new_score = self.get_score(this_game_idx)
                self.cardgames[this_game_idx][2] = new_score #updating score
                return new_score
            #If not then can't play
            return 0
        else: 
            #add to sequence
            merged_cards = cards_list+self.cardgames[whichgame][0]
            ordered_cards = Card.order(merged_cards)
            if ordered_cards:
                old_score = self.get_score(whichgame)
                self.cardgames[whichgame][0] = ordered_cards
                self.cardgames[whichgame][1] = Card.is_sequence(ordered_cards)[1]
                new_score = self.get_score(whichgame)
                self.cardgames[whichgame][2] = new_score
                return new_score-old_score
        return 0
  
   


