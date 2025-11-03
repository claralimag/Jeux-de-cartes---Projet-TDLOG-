
from enum import Enum
from typing import List

# Cards : defines the Card class and related functions (enumerate ?) 

class Suit(Enum): #suit means "couleur" in french
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    JOKER = "joker"

class Card:
    def __init__(self, suit: Suit, value: int, face_up : bool):
        if not (1 <= value <= 13):
          raise ValueError("value must be between 1 and 13")
        self.value = value
        self.suit = suit
        self.face_up = face_up #if card is face-up (seen) or face-down (hidden) 

    @staticmethod
    def follows(card1: "Card", card2: "Card") -> bool:
        """Return True iff card2 comes right after card1."""
        if card1.suit == "joker" or card2.suit == "joker":
            return True
        if card1.value == 2 or card2.value == 2:
            return True
        if card1.value == card2.value - 1:
            return True
        if card1.value == 13 and card2.value == 1:  # Ace follows King
            return True
        return False

    @staticmethod
    def follows_pure(card1: "Card", card2: "Card") -> bool:
        """Return True iff card2’s value is exactly one higher than card1’s."""
        if card1.value == card2.value - 1:
            return True
        if card1.value == 13 and card2.value == 1:  # Ace follows King
            return True
        return False

    @staticmethod
    def is_sequence(card_list: List["Card"]) -> bool:
      nb_cards = len(card_list)
      for i in range(nb_cards-1):
        if not Card.follows(card_list[i],card_list[i+1]):
          return False
      return True

    @staticmethod
    def is_pure_sequence(card_list: List["Card"]) -> bool:
      nb_cards = len(card_list)
      for i in range(nb_cards-1):
        if not Card.follows_pure(card_list[i],card_list[i+1]):
          return False
      return True

