
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
    def __init__(self, suit: Suit, value: int):
        if not (1 <= value <= 13):
          raise ValueError("value must be between 1 and 13")
        self.value = value
        self.suit = suit
        if self.suit == "joker":
            self.point = 10
        else:
            if card.value == 1:
                self.point = 15
            if card.value == 2:
                self.point = 10
            if card.value in [3,4,5,6,7]:
                self.point = 5
            if card.value in [8,9,10,11,12,13]:
                self.point = 10
            

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

    @staticmethod 
    def is_canastra(card_list: List["Card"]) -> bool, bool:
        if len(card_list) >= 7:
            return is_sequence(card_list)
        else:
            return False

    @staticmethod
    def is_fivehunderd_canastra(card_list : List["Card]):
        if 
    
    @staticmethod
    def sequence_points(card_list: List["Card"]) -> int:
        points = 0
        for card in card_list:
            if card.suit == "joker": #joker has an arbitrary value, it shouldn't be taken into acount.
                points += 50
            else:
                if card.value == 1:
                    points += 15
                if card.value == 2:
                    points += 10
                if card.value in [3,4,5,6,7]:
                    points += 5
                if card.value in [8,9,10,11,12,13]:
                    points += 10
            (canstra,pure_canastra) = is_canatra(card_list)
            if canstra:
                points +=100
            if pure_canastra:
                points += 100
            

