#BoardPlayer : defines the board of a player (cards played, functions : add a card to the board to a sequence, add a collection of cards)
#BoardPlayer : defines the board of a player (cards played, functions : add a card to the board to a sequence, add a collection of cards)
from cards import Card
from copy import deepcopy

class BoardPlayer :
    """
    Stores all melds (sequences/sets) played by a single player.
    Each entry in self.cardgames is:
    [cards_in_meld (list[Card]), is_pure (bool), score_for_this_meld (int)]
    """
     
    def __init__(self):
        self.cardgames : list[list[list[Card], bool, int]]  = [] #bool stores if the game is clean and int stores the number of points
        self.numberofgames : int = 0

    
    def get_score(self, whichgame: int) -> int:
        """
        Compute the total score of a given meld (sequence/set),
        including base card points and canastra bonuses.
        """
        cards, is_pure, _ = self.cardgames[whichgame]

        # Base points: sum points of each card
        s = 0
        for el in cards:
            s += el.point

        n = len(cards)

        # Canastra bonus
        if n >= 7:
            if n == 13:
                s += 500 if is_pure else 250
            elif n == 14:
                s += 1000 if is_pure else 500
            else:
                # Any other canastra with 7–12 or >14 cards
                s += 200 if is_pure else 100

        return s    

    def add_to_board(self, cards_list : list[Card], whichgame: int)  -> int:
        """
        Try to play cards on the board.

        :param cards_list: cards the player wants to play
        :param whichgame: -1 -> start a new meld
                          0..N-1 -> extend existing meld at that index
        :return: points gained by this move (0 if invalid)
        """
        
        # --- Start a new meld ---
        if whichgame == -1:
            cards_list_copy = deepcopy(cards_list) 
            ordered_cards = Card.order(cards_list_copy)

            if not ordered_cards:
                # Cannot form a valid sequence/set
                return 0
            
            #if I am allowed to order
            is_clean = Card.is_sequence(ordered_cards)[1]
            self.cardgames.append([ordered_cards, is_clean, 0])
            self.numberofgames += 1

            this_game_idx = self.numberofgames - 1

            new_score = self.get_score(this_game_idx)
            self.cardgames[this_game_idx][2] = new_score
            return new_score
        
        # --- Extend an existing meld ---
        else: 
            if not (0 <= whichgame < len(self.cardgames)):
                # Invalid index
                return 0
            
             # Merge current cards with the existing sequence
            merged_cards = self.cardgames[whichgame][0] + cards_list
            ordered_cards = Card.order(merged_cards)

            if not ordered_cards:
                # Cannot form a valid sequence with the added cards
                return 0
            
            old_score = self.get_score(whichgame)

            # Update cards and purity
            self.cardgames[whichgame][0] = ordered_cards
            self.cardgames[whichgame][1] = Card.is_sequence(ordered_cards)[1]

            new_score = self.get_score(whichgame)
            self.cardgames[whichgame][2] = new_score

            # Return only the difference (points gained this move)
            return new_score - old_score

    def show_deck(self) -> None:
        """Display all melds played by the player."""
        for idx, (cards, is_pure, score) in enumerate(self.cardgames):
            meld_type = "Pure Sequence" if is_pure else "Impure Sequence"
            card_str = ', '.join([str(card) for card in cards])
            print(f"Meld {idx}: {meld_type} | Cards: {card_str} | Score: {score}")
            
   


