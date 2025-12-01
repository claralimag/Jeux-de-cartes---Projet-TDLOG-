# Defined by a name, a list of cards, a board (BoardPlayer) and a score (functions : add card, move card, play a card (add to board - maybe exception?), change score)
from cards import Card, Suit, orderedCards
from boardplayer import BoardPlayer
import boardgame
import cards
import random


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

    #Updates the player's board when the player chooses to play a new set of cards belonging to his set

    def play_cards(self, listofcards : list[Card], whichgame : int, trash : bool) -> int:
        '''
        input :
        listofcards : cards selected by the player 
        whichgame : game selected by the player (if he selected,
        on the contrary it will be bigger then the number of games in the table)
        
        '''
        if whichgame < self.board.number_of_games and whichgame > 0: 
            newscore : int = self.board.add_to_existing_game(listofcards, whichgame)   #add to sequence of cards number whichgame listofcards, returns the new cards
            
        else:
            newscore : int = self.board.add_to_board(listofcards)   #add to the board a new sequence : listofcards, return the new cards
                
        #can you play ?
        if newscore == 0:
            print("Problem with selected sequence")

        self.updatescore(newscore)

        return newscore

        
    
    def update_cards(self,listofcards) -> None:
        for el in listofcards:
                try:
                    self.cards.remove(el)   
                except ValueError:
                    print(f"{el} is not in your deck")
                    pass 
                    



class Robot(Player):
    def __init__(self, name0 : str, cards0 : list[Card], board0 : BoardPlayer, score0 : int ) -> None:
        super().__init__(name0, cards0, board0, score0)

    
    def play_a_card(self, whichplayer :int) -> None :
        '''
        input : 
        whichplayer : int representing the number of the player in the game
        
        Looks if we can play a card on the board and play it if possible

        output : 
        None
        
        '''
        card0 = self.Robot.cards[0]

        deck = self.board.cardgames

        n = len(self.cards)

        i = 0

        while i<n:
            for j in range(len(deck)):

                cards, is_pure, points = deck[j]

                if Card.order(cards + [card0]):    #je suppose que orderedCards verifie si la liste de cartes est une suite valide
                    self.play_cards([card0], j, False)
                    self.update_cards([card0])
                    i = 0  #restart from the beginning

                else:
                    i+=1

                card0 = self.cards[i]
        
            
    def clean_three_sequence_possible(self) -> bool:
            '''
            input : 
            None
            
            Looks if we can play a sequence of at least 3 cards on the board : same color, in order

            output : 
            bool : True if we can play a sequence of at least 3 cards on the board, False otherwise
            
            '''
            n = len(self.cards)

            board_changed = False

            if n<3:
                return False

            ordered_cards = Card.ordercards(self.cards) #je suppose que cards.Card.order ordonne les cartes

            cards_heart = [card for card in ordered_cards if card.suit == Suit.HEART]
            cards_diamond = [card for card in ordered_cards if card.suit == Suit.DIAMOND]
            cards_club = [card for card in ordered_cards if card.suit == Suit.CLUB]
            cards_spade = [card for card in ordered_cards if card.suit == Suit.SPADE]

            for color_cards in [cards_heart, cards_diamond, cards_club, cards_spade]:
                while len(color_cards) >= 3:
                    m = len(color_cards)
                    i = 0
                    while i < m - 3:
                        sub_sequence = color_cards[i:i+3]
                        if Card.order(sub_sequence):
                                color_cards.pop(i)
                                color_cards.pop(i+1)
                                color_cards.pop(i+2)
                                self.play_cards(sub_sequence, -1, False)
                                self.update_cards(sub_sequence)
                                i = 0  # restart from the beginning
                                m -= 3
                                board_changed = True
                        else:
                            i += 1

            return board_changed
       
    def robot_play_cards_easy(self, whichplayer : int) -> Card:
        # input : Player representing the computer
        # output : Card to trow out in the trash 
        # If the robot can play cards, it plays them: even if its not optimal and it can only play a jocker if adding to an existing sequence
        
        self.play_a_card(whichplayer) #robot plays a card if possible

        board_changed = self.clean_three_sequence_possible() #robot plays a sequence of at least 3 cards if possible
        
        if board_changed:
            self.play_a_card(whichplayer) #robot adds cards to existing sequences if possible

        #Throw out a random card:
        n = len(self.cards)
            
        i = random.randint(0,n-1)
        
        return self.cards[i]
        
