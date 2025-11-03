
from enum import Enum

# Cards : defines the Card class and related functions (enumerate ?) 

class Suit(Enum): #suit means "couleur" in french
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    JOKER = "joker" 

class Card:
    def __init__(self, suit: Suit, value: int):
        if not suit == Suit.JOKER:
            if not (1 <= value <= 13):
              raise ValueError("value must be between 1 and 13")
        self.value = value
        self.suit = suit
        if self.suit == Suit.JOKER:
            self.point = 10
        else:
            if self.value == 1:
                self.point = 15
            if self.value == 2:
                self.point = 10
            if self.value in [3,4,5,6,7]:
                self.point = 5
            if self.value in [8,9,10,11,12,13]:
                self.point = 10
            

    @staticmethod
    def follows(card1: "Card", card2: "Card", pure : bool) -> bool:
        """Return True iff card2 comes right after card1."""
        if card1.value == card2.value - 1:
            pure = True
            return True
        if card1.value == 13 and card2.value == 1:  # Ace follows King
            pure = True
            return True
        if card1.suit == "joker" or card2.suit == "joker":
            pure = False 
            return True
        if card1.value == 2 or card2.value == 2:
            pure = False
            return True
        return False
    
    @staticmethod
    def same_suit(card1: "Card", card2: "Card", pure : bool) -> bool:
        if card1.suit == card2.suit:
            return True
        if card1.value == 2 or card2.value == 2 :
            pure = False
            return True
        if card1.suit == "jocker" or card2.suit == "jocker":
            pure = False
            return True

    @staticmethod
    def is_sequence(card_list: list["Card"], is_pure: bool) -> bool:
      
      nb_cards = len(card_list)
      nb_not_pure : int = 0

      for i in range(nb_cards-1):
        
        pure_suit : bool = True

        pure_follow : bool = True

        if not Card.follows(card_list[i],card_list[i+1],pure_suit):
          return False
        
        if not Card.same_suit(card_list[i], card_list[i+1],pure_follow):
            return False
        
        pure = pure_suit or pure_follow
        
        if not pure:
            if nb_not_pure == 0:
                is_pure = pure
                nb_not_pure += 1

            else:
                return False

      return True


            

