
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
    def follows(card1: "Card", card2: "Card") -> tuple[bool,bool]:
        """firt return bool is True if card1 is right before card2
        second bool is True if card1 is right before card2 in a pure manner """
        #If same suit:
        if card1.suit==card2.suit:
          if card1.value == card2.value - 1:
              return True,True
          if card1.value == 13 and card2.value == 1:  # Ace follows King
              return True,True
        #if different suits:
        if card1.suit == Suit.JOKER or card2.suit == Suit.JOKER:
            return True,False
        if card1.value == 2 or card2.value == 2:
            return True,False
        return False,False

    @staticmethod #si deux impurs cest false
    def is_sequence(card_list: list["Card"]) -> tuple[bool,bool,int]:
      """firt return bool says if card_list is a sequence,
      second bool is True if it's a pure sequence """
      pure = True
      nb_unpure = 0
      for i in range(len(card_list)-1):
        follows,pure_follows = Card.follows(card_list[i],card_list[i])
        if follows:
          if not pure_follows:
            pure = False
            nb_unpure += 1
        if not follows:
          return False
        return True,pure ,nb_unpure




      """
      Cette fonction prend en entrée une liste de carte. Si cette liste ne peut
      pas former une suite, la fonction renvoie none. Si elle peut former une
      suite, elle renvoie la liste ordonnée, avec la liste des jokers et/ou deux
      s'il en reste (à choisir où il faut les mettre). Elle a un parametre
      booléen ace_at_the_end qui permet de considérer le cas où l'on met l'ace à
      la fin, après le roi, ou avant le 2. Si ace_at_the end = True mais qu'il
      n'y a pas d'ace, on return False (pour le pas faire le test deux fois).
      Donc toujours faire le test avec ace_at_the_end=False dabord
      """
    @staticmethod #on a le droit a UN SEUL joker et traiter l'ace
    def order(card_list: list["Card"],ace_at_the_end=False) -> tuple[list["Card"],list["Card"]] | None:
      #try two cases: ace comes before 2, or ace comes after king
      #first case: if one comes before 2:
      non_joker_list = [card for card in card_list if card.suit != Suit.JOKER and card.value != 2]
      joker_list     = [card for card in card_list if card.suit == Suit.JOKER or card.value == 2]  # jokers and twos
      #check if there is a three?
      if not all(card.suit == non_joker_list[0].suit for card in non_joker_list):
        #if the cards have different suits, it's not orderable
        return None
      ordered_list = sorted(non_joker_list, key=lambda e: e.value) #sort cards
      if(ace_at_the_end):
        if ordered_list[0].value == 1:
          ordered_list.append(ordered_list.pop(0)) #put the 1 at the beginning
        else:
          False #because no ace
      i = 0
      joker_used = False # tracker (only one joker allowed)
      while i < len(ordered_list)-1: #because ordered_list is going to evolve . -1? DOUBLE CHECK THIS WORKS IF I ADD ELEMENT AT THE LAST MOMENt
        card1, card2 = ordered_list[i], ordered_list[i+1]
        if Card.follows(card1,card2)[0]:
          i+=1
        else: #if the cards aren't consecutive
          if card1.value == 1 and card2.value == 3: #in this case, we check if there is the 2 of the right color
            found_two = False
            two_index = None
            #looking for two
            for joker_index, joker_card in enumerate(joker_list):
              if joker_card.suit == card1.suit: #if there is a two of the right color, we put it
                found_two = True
                two_index = joker_index
                break
            if found_two:
              two_card = joker_list[two_index]
              ordered_list.insert(i+1,joker_card) #we place the card right after card 1.
              joker_list.pop(joker_index)
              i += 1
            else: #if not found two
              if len(joker_list)==0 or joker_used: #is there are no jokers, or already used, list can't be ordered
                return None
              joker_used = True
              ordered_list.insert(i+1,joker_list.pop()) #in all the other cases, we just add a joker
              i += 1
          else: #if we are not between a 1 and a 3:
            if len(joker_list)==0 or joker_used: #is there are no jokers, or already used, list can't be ordered
              return None
            joker_used = True
            ordered_list.insert(i+1,joker_list.pop()) #in all the other cases, we just add a joker
            i += 1
      return ordered_list, joker_list #joker_list might be empty


            

