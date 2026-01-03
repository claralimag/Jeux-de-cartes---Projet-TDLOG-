# Defined by a name, a list of cards, a board (BoardPlayer) and a score (functions : add card, move card, play a card (add to board - maybe exception?), change score)
from cards import Card, Suit
from boardplayer import BoardPlayer
import random


class Player :
    def __init__(self, name: str, cards: list["Card"], board: "BoardPlayer", score: int = 0) -> None:
            """
            Initialize a player.

            :param name: Player's name
            :param cards: Initial hand (list of Card objects)
            :param board: Player's personal board (BoardPlayer instance)
            :param score: Initial score (default 0)
            """
            self.name = name
            self.cards = cards
            self.board = board
            self.score = score


    # ---------- Hand management (drawing / taking from discard pile) ----------

    def add_card(self, card: "Card") -> None:
        """
        Add a single card to the player's hand (normal draw).

        :param card: Card that was drawn by the player
        """
        self.cards.append(card)

    def add_cards(self, cards: list["Card"]) -> None:
        """
        Add multiple cards to the player's hand (e.g. taking the discard pile).

        :param cards: Cards that were taken by the player
        """
        self.cards.extend(cards)

    def order_hand(self) -> None:
        """
        Order the player's hand (useful after drawing new cards).
        """
        self.cards = Card.ordercards(self.cards)
        
    # ---------- Score management ----------
    def update_score(self, scorepoints: int) -> None:
        """
        Update the player's score.

        :param scorepoints: Points to add to the current score
        """
        self.score += scorepoints


    #Updates the player's board when the player chooses to play a new set of cards belonging to his set

     # ---------- Playing cards on the board ----------

    def play_cards(self, cards_to_play: list["Card"], game_index: int, from_trash: bool = False) -> int:
        """
        Play a set of cards on the player's board.

        :param cards_to_play: Cards selected by the player
        :param game_index: Index of the game/sequence chosen by the player.
                           Convention:
                             - if 0 <= game_index < board.number_of_games: extend an existing game
                             - otherwise (e.g. -1): create a new game on the board
        :param from_trash: True if these cards come from the discard pile (not used yet)
        :return: Points earned by playing these cards
        :raises ValueError: if the move is invalid
        """

        # Delegate validity checking + scoring to BoardPlayer
        # You changed BoardPlayer to handle "new vs existing" inside add_to_board
        newscore = self.board.add_to_board(cards_to_play, game_index)

        # If add_to_board returns 0, we treat it as an invalid move
        if newscore == 0:
            raise ValueError("Invalid meld / sequence.")

        # Update score and remove cards from the player's hand
        self.update_score(newscore)
        self.update_cards(cards_to_play)

        return newscore
    # ---------- Display and hand updates ----------

    def show_hand(self) -> None:
        """
        Print the player's hand with indices.
        """
        print(f"Hand of {self.name}:")
        for idx, card in enumerate(self.cards):
            print(f"{idx}: {card.value} of {card.suit}")

    def update_cards(self, cards_to_remove: list["Card"]) -> bool:
        """
        Remove a list of cards from the player's hand (after playing them).

        :param cards_to_remove: Cards that should be removed from the hand
        :return: True if the player still has cards in hand, False if the hand is now empty
        """
        for el in cards_to_remove:
            try:
                self.cards.remove(el)
            except ValueError:
                print(f"{el} is not in your hand")
                # Ignore and continue
                break

        return len(self.cards) > 0

    def new_cards(self, cards: list["Card"]) -> None:
        """
        Replace the player's hand completely (useful when taking a pot as a new hand).
        """
        self.cards = cards


class Robot(Player):
    def __init__(self, name0 : str, cards0 : list[Card], board0 : BoardPlayer, score0 : int ) -> None:
        super().__init__(name0, cards0, board0, score0)

    def robot_pick_cards(self, whichplayer : int, discard_pile: list[Card], open : bool) -> None:
        """
        input : int representing the number of the player in the game
        Looks if we can pick cards from the trash
        output : True if we can pick cards from the trash, False otherwise

        """
        pass 

    def play_a_card(self) -> bool:
        """
        Try to add ONE card from the hand to an existing meld on the board.
        Returns True if it played something, False otherwise.
        """
        for card in list(self.cards):  # copy so we can safely modify self.cards
            for j, (cards_in_meld, is_pure, pts) in enumerate(self.board.cardgames):
                # Build the combination this meld + this card
                merged = cards_in_meld + [card]

                # Use the SAME validator as BoardPlayer.add_to_board
                ordered = Card.order(merged)
                if ordered is None:
                    continue  # this card cannot go on this meld

                # We know add_to_board will accept this, so play it
                try:
                    self.play_cards([card], j, from_trash=False)
                except ValueError:
                    # In theory shouldn't happen now, but just in case
                    continue

                return True

        return False
        
    # ----------- PLAY A NEW CLEAN 3-CARD SEQUENCE -----------
    def clean_three_sequence_possible(self) -> bool:
        """
        Try to play a new pure sequence of at least 3 cards of the same suit (no jokers / 2s as wildcards).
        Returns True if something was played.
        """
        if len(self.cards) < 3:
            return False

        ordered = Card.ordercards(self.cards)
        if ordered is None:
            return False

        # Split by suit (without jokers)
        hearts   = [c for c in ordered if c.suit == Suit.HEARTS and c.value not in (2,)]
        diamonds = [c for c in ordered if c.suit == Suit.DIAMONDS and c.value not in (2,)]
        clubs    = [c for c in ordered if c.suit == Suit.CLUBS and c.value not in (2,)]
        spades   = [c for c in ordered if c.suit == Suit.SPADES and c.value not in (2,)]

        for color_cards in [hearts, diamonds, clubs, spades]:
            m = len(color_cards)
            if m < 3:
                continue
            # Try all windows of length >= 3
            for start in range(m - 2):
                for end in range(start + 3, m + 1):
                    sub = color_cards[start:end]
                    can_be_seq, is_pure, _ = Card.is_sequence(sub)
                    if can_be_seq and is_pure and len(sub) >= 3:
                        # Play these cards as a new meld
                        self.play_cards(sub, game_index=-1, from_trash=False)
                        return True

        return False
    

    def jocker_three_sequence_possible(self) -> bool:
        '''
            input : 
            None
            
            Looks if we can play a sequence of at least 3 cards on the board with a jocker

            output : 
            bool : True if we can play a sequence of at least 3 cards on the board, False otherwise
            
            '''
        n = len(self.cards)
        
        board_changed = False

        if n<3:
            return False

        ordered_cards = Card.ordercards(self.cards) #je suppose que cards.Card.order ordonne les cartes

        cards_heart = [card for card in ordered_cards if card.suit == Suit.HEARTS]
        cards_diamond = [card for card in ordered_cards if card.suit == Suit.DIAMONDS]
        cards_club = [card for card in ordered_cards if card.suit == Suit.CLUBS]
        cards_spade = [card for card in ordered_cards if card.suit == Suit.SPADES]

        jockers = [card for card in ordered_cards if card.suit == Suit.JOKER]

        cards_by_color = [cards_heart, cards_diamond, cards_club, cards_spade]

        random.shuffle(cards_by_color)  #to add some randomness in the robot's behavior: he won't always add a jocker to the same color
        for color_cards in cards_by_color:
            while len(color_cards) >= 2 and len(jockers) > 0:
                m = len(color_cards)
                i = 0
                while i < m - 3:
                    sub_sequence = color_cards[i:i+2] 
                    if Card.three_cards_with_jocker(jockers[0],sub_sequence):
                        color_cards.pop(i)
                        color_cards.pop(i+1)
                        J = jockers.pop(0)
                        self.play_cards(sub_sequence  + [J], -1, False)
                        self.update_cards(sub_sequence + [J])
                        i = 0  # restart from the beginning
                        m -= 2
                        board_changed = True
                    else:
                        i += 1

        return board_changed    


    def two_as_a_jocker_same_colors_sequence_possible(self) -> bool:
        '''
        input : 
        None
            
        Looks if we can play a sequence of at least 3 cards on the board with a two as a jocker

        output : 
                    
        bool : True if we can play a sequence of at least 3 cards on the board, False otherwise
            
        '''

        n = len(self.cards)
        
        board_changed = False

        if n<3:
            return False

        ordered_cards = Card.ordercards(self.cards) 
    
        cards_heart = [card for card in ordered_cards if card.suit == Suit.HEARTS]
        cards_diamond = [card for card in ordered_cards if card.suit == Suit.DIAMONDS]
        cards_club = [card for card in ordered_cards if card.suit == Suit.CLUBS]
        cards_spade = [card for card in ordered_cards if card.suit == Suit.SPADES]

        cards_by_color = [cards_heart, cards_diamond, cards_club, cards_spade]
        random.shuffle(cards_by_color)  #to add some randomness in the robot's behavior: he won't always add a jocker to the same color
        
        #two as a jocker of the same color
        for color_cards in cards_by_color:
            twos = [card for card in color_cards if card.value == 2]
            while len(color_cards) >= 2 and len(twos) > 0:
                m = len(color_cards)
                i = 0
                while i < m - 2:
                    sub_sequence = color_cards[i:i+2] 

                    if Card.three_cards_with_jocker(twos[0],sub_sequence) and ((not(sub_sequence[0].value == 2) and not(sub_sequence[1].value == 2)) or (sub_sequence[0].value == 2 and not(sub_sequence[1].value == 2) and len(twos) >=2) or (sub_sequence[1].value == 2 and not(sub_sequence[0].value == 2) and len(twos) >=2)):
                        color_cards.pop(i)
                        color_cards.pop(i)
                        two = twos.pop(0)
                        self.play_cards(sub_sequence + [two], -1, False)
                        self.update_cards(sub_sequence + [two])
                        i = 0  # restart from the beginning
                        m -= 2
                        board_changed = True
                    else:
                        i += 1

        return board_changed    
    

    def two_as_a_jocker_diff_colors_sequence_possible(self) -> bool:
        '''
        input : 
        None
            
        Looks if we can play a sequence of at least 3 cards on the board with a two as a jocker of different colors

        output : 
                    
        bool : True if we can play a sequence of at least 3 cards on the board, False otherwise
            
        '''

        n = len(self.cards)
        
        board_changed = False

        if n<3:
            return False

        ordered_cards = Card.ordercards(self.cards) 
    
        cards_heart = [card for card in ordered_cards if card.suit == Suit.HEART]
        cards_diamond = [card for card in ordered_cards if card.suit == Suit.DIAMOND]
        cards_club = [card for card in ordered_cards if card.suit == Suit.CLUB]
        cards_spade = [card for card in ordered_cards if card.suit == Suit.SPADE]

        cards_by_color = [cards_heart, cards_diamond, cards_club, cards_spade]
        cards_by_color = random.shuffle(cards_by_color)  #to add some randomness in the robot's behavior: he won't always add a jocker to the same color
        
        #two as a jocker of the same color
        for color_cards in cards_by_color:
            twos = [card for card in color_cards if card.value == 2 and not(card.suit == color_cards[0].suit)]
            while len(color_cards) >= 2 and len(twos) > 0:
                m = len(color_cards)
                i = 0
                while i < m - 2:
                    sub_sequence = color_cards[i:i+2] 

                    if Card.three_cards_with_jocker(twos[0],sub_sequence):
                        color_cards.pop(i)
                        two = twos.pop(0)
                        self.play_cards(sub_sequence + [two], -1, False)
                        self.update_cards(sub_sequence + [two])
                        i = 0  # restart from the beginning
                        m -= 2
                        board_changed = True
                    else:
                        i += 1

        return board_changed    
    

    def robot_play(self,whichgame) -> Card:
        pass


#Both Easy and Easy Medium robots have a similar behavior when playing cards : they don't take into account the optimality of their plays at the long run
class RobotEasy(Robot):
    def __init__(self, name0 : str, cards0 : list[Card], board0 : BoardPlayer, score0 : int ) -> None:
        super().__init__(name0, cards0, board0, score0)
       
    def robot_pick_cards(self, whichplayer : int, discard_pile: list[Card], open : bool) -> None:
        """
        input : int representing the number of the player in the game
        Looks if we can pick cards from the trash : if trash has at least 3 cards, we pick it
        output : True if we can pick cards from the trash, False otherwise

        """
        if len(discard_pile) >= 3 and open:
            self.add_card(discard_pile)
            return True
        else:
            return False
        

    def robot_play(self, whichplayer : int) -> Card:
        # input : Player representing the computer
        # output : Card to trow out in the trash 
        # If the robot can play cards, it plays them: even if its not optimal and it can only play a jocker if adding to an existing sequence
        
        playing_cards = self.play_a_card() 
        while playing_cards: #robot plays a card if possible
            playing_cards = self.play_a_card()
        
        playing_melds = self.clean_three_sequence_possible() #robot plays a sequence of at least 3 cards if possible
        while playing_melds:
            self.play_a_card() #robot adds cards to existing sequences if possible
            playing_melds = self.clean_three_sequence_possible() #robot plays a sequence of at least 3 cards if possible

        #Throw out a random card:
        n = len(self.cards)
            
        i = random.randint(0,n-1)
        
        return self.cards[i]


#Easy medium robots however deal better with jockers and twos as jokers than easy robots
class RobotEasyMedium(Robot):
    def __init__(self, name0 : str, cards0 : list[Card], board0 : BoardPlayer, score0 : int ) -> None:
        super().__init__(name0, cards0, board0, score0)
       
    #we need to change play a card : It shouldn't just play a jocker
    def play_a_card(self, whichplayer):
        '''
        input : 
        whichplayer : int representing the number of the player in the game
        Looks if we can play a card on the board and play it if possible
        output : 
        None
        '''
        card0 = self.cards[0]

        deck = self.board.cardgames

        n = len(self.cards)

        i = 0

        while i<n:
            for j in range(len(deck)):

                cards, is_pure, points = deck[j]

                if Card.card_to_game(cards + [card0]) and card0.suit != Suit.JOKER:   
                    self.play_cards([card0], j, False)
                    self.update_cards([card0])
                    i = 0  #restart from the beginning

                else:
                    i+=1

                card0 = self.cards[i]

    def play_a_card_with_jocker(self, whichplayer):
        '''
        input : 
        whichplayer : int representing the number of the player in the game
        Looks if we can play a card on the board and play it if possible
        output : 
        None
        '''
        card0 = self.cards[0]

        deck = self.board.cardgames

        n = len(self.cards)

        i = 0

        while i<n:
            for j in range(len(deck)):

                cards, is_pure, points = deck[j]

                if Card.card_to_game(cards + [card0]):    #je suppose que orderedCards verifie si la liste de cartes est une suite valide
                    self.play_cards([card0], j, False)
                    self.update_cards([card0])
                    i = 0  #restart from the beginning

                else:
                    i+=1

                card0 = self.cards[i]
    
    def robot_play(self, whichplayer : int) -> Card:
        # input : Player representing the computer
        # output : Card to trow out in the trash 
        # If the robot can play cards, it plays them: even if its not optimal and it can only play a jocker if adding to an existing sequence
        
        self.play_a_card(whichplayer) #robot plays a card if possible

        board_changed = self.clean_three_sequence_possible() #robot plays a sequence of at least 3 cards if possible
        
        if board_changed:
            self.play_a_card(whichplayer) #robot adds cards to existing sequences if possible

        board_changed = self.jocker_three_sequence_possible() #robot plays a sequence of at least 3 cards with a jocker if possible
        
        if board_changed:
            self.play_a_card(whichplayer) #robot adds cards to existing sequences if possible

        board_changed = self.two_as_a_jocker_same_colors_sequence_possible() #robot plays a sequence of at least 3 cards with a two as a jocker of same color if possible
        
        if board_changed:
            self.play_a_card(whichplayer) #robot adds cards to existing sequences if possible

        board_changed = self.two_as_a_jocker_diff_colors_sequence_possible() #robot plays a sequence of at least 3 cards with a two as a jocker of different colors if possible
        
        if board_changed:
            self.play_a_card_with_jocker(whichplayer) #robot adds cards to existing sequences if possible

        #Throw out a random card:
        n = len(self.cards)
            
        i = random.randint(0,n-1)
        
        return self.cards[i]
    
    
        
