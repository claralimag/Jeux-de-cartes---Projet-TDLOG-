#BoardPlayer : defines the board of a player (cards played, functions : add a card to the board to a sequence, add a collection of cards)
from cards import Card

class BoardPlayer :
    def __init__(self):
        cardgames : list[tuple[list[Card], bool, int]]  = [] #bool stores if the game is clean and int stores the number of points
        numberofgames : int = 0

    #verifies if the list of cards can be added to a existing game :
    def can_you_add_to_existing_game(self, listofcards: list[Card], whichgame : int, isclean : bool) -> int:
        '''
        input :
        listofcards : cards selected by the player 
        whichgame : number of the existing game
        isclean : true if there's no joker

        output :
        -1 if you can't add to the new game, 0 if you can add it to the right, 1 to the left
        
        '''
        i : int = -1

        if whichgame < self.board.number_of_games:
            if not(self.board.isclean[whichgame]):
                if not(isclean):
                    return -1        #add exception explaining why
        
        color = listofcards[0].suit     #compute the cards suit
        number = listofcards[0].value   #compute the cards value

        if not(color == self.cardgames[whichgame[0]].suit):
            return -1
        
        if not(self.cardgames[whichgame[-1]].value - 1 == number): 
            if not(self.cardgames[whichgame[0]].value - 1 == listofcards[-1].value): 
                return -1
            else:
                i = 0
        else:
            i = 1

        for el in listofcards:
            if abs(number - el.value) > 1 or (el.suit == color):
                return -1
            
            else:
                number = el.value
        
        return i
        


    #Tests wether or not the cards selected by the player can be played
    def can_you_play(self, listofcards : list[Card], isclean : bool) -> bool:
        '''
        input :
        listofcards : cards selected by the player 

        output :
        true if the set of cards are playable 
        
        '''

        n : int = len(listofcards)

        if n<3:
            return False

        color = listofcards[0].suit     #compute the cards suit
        number = listofcards[0].value   #compute the cards value

        for el in listofcards:
            if abs(number - el.value) > 1 or (el.suit == color):
                return False
            
            else:
                number = el.value
        
        return True
    
    def scorenewgame(self,listofcards) -> int:
        pass

    def scoreexistinggame(self, listofcards, clean, whichgame) -> int:
        pass

    def add_to_existing_game(self, listofcards : list[Card], whichgame: int, clean: bool)  -> int:
        i : int = self.can_you_add_to_existing_game(listofcards, whichgame, clean)

        if i >= 0 :
            self.isclean[whichgame] = clean
            if i == 0:
                self.cardgames[whichgame] = listofcards + self.cardgames[whichgame]
            else: 
                self.cardgames[whichgame] = self.cardgames[whichgame] + listofcards

            score = self.scoreexistinggame(listofcards)
            return score
        
        else :
            print("Card's selection is not playable") 

    def add_to_board(self, listofcards : list[Card], clean) -> int:

        if self.can_you_play(listofcards, clean):
            
            self.cardgames.append(listofcards)
            self.isclean[-1] = clean
            self.number_of_games += 1
            score : int = self.scorenewgame(listofcards)
            return score

# BoardGame : defines the board of the game (players, deck, discard pile, functions : add player, remove player, draw card from deck, draw card from discard pile, add card to discard pile)

class BoardGame:
    def __init__():
        return
