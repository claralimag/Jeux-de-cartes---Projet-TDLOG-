# Cards : defines the Card class and related functions (enumerate ?) 

class Suit(enum.Enum): #suit means "couleur" in french
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    JOKER = "joker"

class Value(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Card:
    def __init__(self, suit: Suit, value:Value):
        self.suit = suit
        self.value = value
    def __lt__(self,other):
        if self.suit == JOKER or other.suit == JOKER: #(self.suit.name?)
            return True
        if self.value == 2 or other.value == 2:
            return True
        if self.value <= other.value:
            return True
        if self.value == 13 and other.value == 1: #king<=ace
            return True
        return False #tous les autres Cards


a_color = Suit.CLUBS
a_value = Value.FIVE
other_value = Value.SIX
card_1 = Card(a_color,a_value)
card_2 = Card(a_color,other_value)
print(card1<=card2)