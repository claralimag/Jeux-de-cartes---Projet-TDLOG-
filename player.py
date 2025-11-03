# Defined by a name, a list of cards, a board (BoardPlayer) and a score (functions : add card, move card, play a card (add to board - maybe exception?), change score)
from cards import Card, Suit
from boardplayer import BoardPlayer


class Player :
    def __init__(self, name0 : str, cards0 : list[Card], board0 : BoardPlayer, score0 : int ) -> None:
        name : str = name0
        board : BoardPlayer = board0
        score: int = score0
        cards : list[Card] = cards0


    #The next functions are usefull when the player gets a new card 
    #This is usefull when the player chooses to draw a card
    def add_card(self, card : Card) -> None:
        '''
        input :
        card : card that was drawed by the player 
        
        '''
        self.cards.append(Card)
    
    #This is usefull when the player chooses to pick up the trash
    def add_card(self, listofcards : list[Card])-> None:
        '''
        input :
        listofcards : cards that were drawed by the player when they picked up the trash
        
        '''
        for el in listofcards:
            self.cards.append(el)
        
    #Updates the score when the player chooses to play a new set of cards
    def updatescore(self,scorepoints : int) -> None:
        '''
        input :
        scorepoints : new score won by the player 
        
        '''
        self.score += scorepoints

    #Updates the player's board when the player chooses to play a new set of cards
    def play_cards(self,listofcards : list[Card], whichgame : int) -> None:
        '''
        input :
        listofcards : cards selected by the player 
        whichgame : game selected by the player (if he selected,
        on the contrary it will be bigger then the number of games in the table)
        
        '''
        isclean : bool = True

        #can you play ?
        if not(Card.is_sequence(listofcards, isclean)):
            print("Problem with selected sequence")

        if whichgame > self.board.number_of_games : 
            newscore : int = self.board.add_to_existing_game(listofcards, whichgame, isclean)   #add to sequence of cards number whichgame listofcards, returns the new cards
            
        else:
            newscore : int = self.board.add_to_board(listofcards, isclean)   #add to the board a new sequence : listofcards, return the new cards
                
        self.updatescore(newscore)




