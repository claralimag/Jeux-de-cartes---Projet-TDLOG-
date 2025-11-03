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
            if not(self.board.cardgames[whichgame][1]):
                if not(isclean):
                    return -1        #the game is alredy not clean
        
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

        return True
    

    def scorenewgame(self,listofcards, whichgame, clean) -> int:
        s : int = 0

        for el in listofcards:
            s+= el.point

        if len(listofcards) >= 7 : #Is canastra ?
            if len(listofcards) == 13:
                if clean:
                    s+= 500
                else: 
                    s+= 250
            if len(listofcards) == 14:
                if clean:
                    s+= 1000
                else: 
                    s+= 500
            else:
                if clean:
                    s+= 200
                else: 
                    s+= 100
        
        self.cardgames[whichgame][2] = s

        return s 


    def scoreexistinggame(self, listofcards, clean, whichgame) -> int:
        
        original_game : list[Card] = self.cardgames[whichgame][0]

        n_list : int = len(listofcards)

        n_original : int = len(original_game)

        s : int = 0

        for el in listofcards:
            s+= el.point

        if n_list == 13 and n_original < 13  : 
            if clean:
                s+= 500
            else: 
                s+= 250
        
        elif n_list == 14 and n_original < 14:
            if clean:
                s+= 1000
            else: 
                s+= 500
        
        elif n_list >= 7 and n_original < 7:
            if clean:
                s+= 200
            else: 
                s+= 100
        
        self.cardgames[whichgame][2] += s

        return s 


    def add_to_existing_game(self, listofcards : list[Card], whichgame: int, clean: bool)  -> int:
        i : int = self.can_you_add_to_existing_game(listofcards, whichgame, clean)

        if i >= 0 :
            self.cardgames[whichgame][1] = clean

            if i == 0:
                self.cardgames[whichgame][0] = listofcards + self.cardgames[whichgame]

            else: 
                self.cardgames[whichgame][0] = self.cardgames[whichgame] + listofcards

            score = self.scoreexistinggame(listofcards, whichgame, clean) #update score

            return score
        
        else :
            print("Card's selection is not playable") 


    def add_to_board(self, listofcards : list[Card], clean) -> int:

        if self.can_you_play(listofcards, clean):
            
            self.cardgames.append(listofcards,clean, 0)
            self.number_of_games += 1
            score : int = self.scorenewgame(listofcards, self.number_of_games - 1, clean)

            return score

