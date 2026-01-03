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

    @staticmethod
    def is_sequence(card_list: list["Card"]) -> tuple[bool, bool, int]:
        """
        First bool:  True if card_list is a valid sequence
        Second bool: True if the sequence is pure
        int:         number of impurities (jokers / 2s etc. used as wildcards)
        """
        # A sequence of length < 2 is never valid here
        if len(card_list) < 2:
            return False, False, 0

        pure = True
        nb_unpure = 0

        for i in range(len(card_list) - 1):
            card1 = card_list[i]
            card2 = card_list[i + 1]

            follows, pure_follows = Card.follows(card1, card2)

            if not follows:
                # Not a sequence at all
                return False, False, 0

            if not pure_follows:
                pure = False
                nb_unpure += 1

        # If we got here, every neighboring pair "follows"
        return True, pure, nb_unpure

    @staticmethod
    def ordercards(card_list: list["Card"]) -> list["Card"] | None:
      joker_list     = [c for c in card_list if c.suit == Suit.JOKER]  # jokers

      heart_list   = [c for c in card_list if c.suit == Suit.HEARTS]
      diamond_list = [c for c in card_list if c.suit == Suit.DIAMONDS]
      club_list    = [c for c in card_list if c.suit == Suit.CLUBS]
      spade_list   = [c for c in card_list if c.suit == Suit.SPADES]

      #sort cards by suit
      heart_list_sorted = sorted(heart_list, key=lambda e: e.value)
      diamond_list_sorted = sorted(diamond_list, key=lambda e: e.value)
      club_list_sorted = sorted(club_list, key=lambda e: e.value)
      spade_list_sorted = sorted(spade_list, key=lambda e: e.value)

      return heart_list_sorted + diamond_list_sorted + club_list_sorted + spade_list_sorted + joker_list

    @staticmethod
    def card_to_game(card: "Card", cards : list["Card"], is_pure: bool) -> bool:
        '''
        input : 
        card : Card to test
        cards : list of Card representing a game on the board
        is_pure : bool representing if the game is pure or not
        
        Looks if we can play the card on the game

        output : 
        bool : True if we can play the card on the game, False otherwise
        
        '''
        begin = cards[0]
        end = cards[-1]

        if card.suit == Suit.JOKER:
            return is_pure
            
        if card.suit != begin.suit:
            return False
            
        if card.value == begin.value - 1 or card.value == end.value + 1:
            return True
            
        if card.value == 1 and end.value == 13:
            return True
            
        return False
    
    @staticmethod
    def three_cards_with_jocker(card : "Card", cards_list : list["Card"]) -> bool:
      cards_list = sorted(cards_list, key=lambda e: e.value)

      assert len(cards_list) == 2
      assert card.suit == Suit.JOKER or card.value == 2

      if cards_list[1].value - cards_list[0].value == 2:
          return True
      
      if cards_list[0].value == 1 and cards_list[1].value == 12:
          return True
      
      return False 
    
      """
      Cette fonction prend en entrée une liste de carte. Si cette liste ne peut
      pas former une suite, la fonction renvoie none. Si elle peut former une
      suite, elle renvoie la liste ordonnée
      """
    @staticmethod #on a le droit a UN SEUL joker et traiter l'ace
    def order(card_list: list["Card"]) -> list["Card"] | None:

      if len(card_list)<3 or len(card_list)>14:
        return None

      non_joker_list = [card for card in card_list if card.suit != Suit.JOKER and card.value != 2]
      joker_list     = [card for card in card_list if card.suit == Suit.JOKER or card.value == 2]  # jokers and twos

      this_suit = non_joker_list[0].suit

      if not all(card.suit == this_suit for card in non_joker_list):
        #if the cards have different suits, it's not orderable
        return None

      nb_jokers_init = len(joker_list)
      twos_list = [card for card in joker_list if card.suit == this_suit]
      joker_list = [card for card in joker_list if card.suit != this_suit]
      ordered_list = sorted(non_joker_list, key=lambda e: e.value) #sort cards

      #forbidden to have more than 2 jokers
      if len(joker_list)> 2:
        return None
      if len(joker_list)==1 and len(twos_list)>=2:
        #one of the twos would be used as a joker (forbidden)
        return None

      #dealing with small cases
      if len(ordered_list) == 0:
        return None  #twos and jokers won't work (at least 3 cards)
      if len(ordered_list)==1:
        #if there is only one card, we will need a two and
        # a joker, and the only possibilities are:
        #it is a one, and we check if we can play 1,2,joker
        #it is a 3, and we check if we can play 2,3,joker (or joker,2,3)
        #it is a 4, and we can play 2,joker,4
        if len(twos_list) == 1 and nb_jokers_init == 2: #a two and a joker
          joker_card = joker_list.pop() if joker_list else twos_list.pop()
          if ordered_list[0].value==1:
            return [ordered_list[0],twos_list.pop(),joker_card]
          if ordered_list[0].value==3:
            return [twos_list.pop(),ordered_list.pop(),joker_card]
          if ordered_list[0].value==4:
            return (twos_list.pop(),joker_card,ordered_list.pop())
        #if we had one card and none if this worked, then it's a fail
        return None

      #now, there are at least two elements in ordered_list
      # we seperate the aces to treat them at the end
      aces = []
      if ordered_list[0].value == 1: #if 1 ace
        aces.append(ordered_list.pop(0))
      if ordered_list and ordered_list[0].value == 1: #if 2 aces
        aces.append(ordered_list.pop(0))
      if ordered_list and ordered_list[0].value == 1: #if 3 aces: not orderable
        return None

      #if there were two aces and ordered_list is empty, can't be ordered
      if len(ordered_list) == 0:
        return None
      if len(ordered_list) == 1:
        #we have 1 or 2 aces
        if len(aces) == 2:
          return None
        if len(aces)==1:
          #from [1] [2] [joker or 2] to [1,2,joker or 2]
          if ordered_list[0].value == 2 and nb_jokers_init == 1:
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.insert(0,aces.pop())
            ordered_list.append(joker_card)
            return ordered_list
          #from [1] [3] [joker or 2] to [1,joker or 2,3]
          if ordered_list[0].value == 3 and nb_jokers_init == 1:
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.insert(0,joker_card)
            ordered_list.insert(0,aces.pop())
            return ordered_list
          #from [1] [3] [2,joker] to [1,2,3,joker]
          if ordered_list[0].value == 3 and nb_jokers_init==2:
            ordered_list.insert(0,twos_list.pop())
            ordered_list.insert(0,aces.pop())
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.append(joker_card)
            return ordered_list
          #from [1] [queen] [joker] to [queen,joker,1]
          if ordered_list[0].value == 12 and nb_jokers_init == 1:
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.append(joker_card)
            ordered_list.append(aces.pop())
            return ordered_list
          #from [1] [king] [joker] to [joker,king,1]
          if ordered_list[0].value == 13 and nb_jokers_init == 1:
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.insert(0,joker_card)
            ordered_list.append(aces.pop())
            return ordered_list
        #if we are in none of these cases with 1 card in orded list and 1 ace,
        #then can't be ordered
        return None

      i = 0 #iterator for traking where we are in the list
      joker_used = False # tracker (only one joker allowed)
      while i < len(ordered_list)-1: #because ordered_list is going to evolve . -1? DOUBLE CHECK THIS WORKS IF I ADD ELEMENT AT THE LAST MOMENt
        card1, card2 = ordered_list[i], ordered_list[i+1]
        follows, pure_follows = Card.follows(card1,card2)

        if pure_follows:
          i+=1

        elif follows:
          #in this case, card1 = a joker, card2 = not a joker.
          #We need to check that we have value, joker, value+2
          if ordered_list[i-1].value+2 == card2.value:
            i+=1
          else:
            return None

        #now we treat the case where the cards aren't consecutive at all
        else:
          #We check if we can add a two or a joker in the gap
          if card1.value == 1 and card2.value == 3:
            if len(twos_list)>0:
              ordered_list.insert(i+1,twos_list.pop())
              i+=1
            #if we are not able to put a two
            else:
              #is there are no jokers, or already used, list can't be ordered
              if len(joker_list)+len(twos_list)==0 or joker_used:
                return None
              #else, we play a joker
              joker_used = True
              joker_card = joker_list.pop() if joker_list else twos_list.pop()
              ordered_list.insert(i+1,joker_card)
              i += 1
          #case for when we are not between a 1 and a 3:
          else:
            if len(joker_list)+len(twos_list)==0 or joker_used:
              return None
            joker_used = True
            joker_card = joker_list.pop() if joker_list else twos_list.pop()
            ordered_list.insert(i+1,joker_card)
            i += 1
      #now, if we have jokers or twos left:
      #we check if we can add a natural 2
      if ordered_list[0].value==3 and len(twos_list)>0:
        ordered_list.insert(0,twos_list.pop())
      #now, we check if we don't have too many jokers
      nb_jokers_left = len(twos_list)+len(joker_list)
      if nb_jokers_left > 1:
        return None

      # Now we need to check all the cases with the jokers and aces.
      # Not hard but needs to be checked by hand.
      if len(aces)==2:
        #from [2,...,13] to [1...13,1]:
        if ordered_list[0].value == 2 and ordered_list[-1].value == 13 and nb_jokers_left == 0:
          ordered_list.insert(0,aces.pop())
          ordered_list.append(aces.pop())
          return ordered_list
        #from [3,...,12] [2,joker] to [1,2,3,...,12,joker,1]
        if ordered_list[0].value == 3 and ordered_list[-1].value == 12 and nb_jokers_left == 2:
          ordered_list.insert(0,twos_list.pop())
          ordered_list.insert(0,aces.pop())
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(joker_card)
          return ordered_list
        #from [2,...,12], [2 or joker] to [1,2,...,12,2 or joker,1]
        if ordered_list[0].value == 2 and ordered_list[-1].value == 12 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.insert(0,aces.pop())
          ordered_list.append(joker_card)
          ordered_list.append(aces.pop())
          return ordered_list
        #from [3,...,13] [2 or joker] to [1,2 or joker,3,...,13,1]
        if ordered_list[0].value == 3 and ordered_list[-1].value == 13 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(aces.pop())
          ordered_list.insert(0,joker_card)
          ordered_list.insert(0,aces.pop())
          return ordered_list
      if len(aces)==1:
        #from [2,...,x(<=13)] to [1,2,...,x]
        if ordered_list[0].value == 2 and nb_jokers_left == 0:
          ordered_list.insert(0,aces.pop())
          return ordered_list
        #from [2,...x<13] [2 or joker] to [1,2,...x<13,2 or joker]
        if ordered_list[0].value == 2 and ordered_list[-1].value < 13 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.insert(0,aces.pop())
          ordered_list.append(joker_card)
          return ordered_list
        #from [3,...,x(<=13)] [2 or joker] to [1,2 or joker,3,...x]
        if ordered_list[0].value == 3 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.insert(0,joker_card)
          ordered_list.insert(0,aces.pop())
          return ordered_list
        #from [3,...,x<13] [2,joker] to [1,2,3,...,x<13,joker]
        if ordered_list[0].value == 3 and ordered_list[-1].value < 13 and nb_jokers_left == 2:
          ordered_list.insert(0,twos_list.pop())
          ordered_list.insert(0,aces.pop())
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(joker_card)
          return ordered_list
        #from [x>=2,...,13] to [x>=2,...,13,1]
        if ordered_list[-1].value == 13 and nb_jokers_left == 0:
          ordered_list.append(aces.pop())
          return ordered_list
        #from [x>=2,...,13] [2 or joker] to [2 or joker,x,...,13,1]
        if ordered_list[-1].value == 13 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.insert(0,joker_card)
          ordered_list.append(aces.pop())
          return ordered_list
        #from [x>=2,...,12] [2 or joker] to [x,...12,2 or joker,1]
        if ordered_list[-1].value == 12 and nb_jokers_left == 1:
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(joker_card)
          ordered_list.append(aces.pop())
          return ordered_list
        #from [3,...,12] [2 , 2 or joker] to [2,3,...12,2 or joker,1]
        if ordered_list[0].value == 3 and ordered_list[-1].value == 12 and nb_jokers_left == 2:
          ordered_list.append(twos_list.pop())
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(joker_card)
          ordered_list.append(aces.pop())
          return ordered_list

      if len(aces)==0:
        if nb_jokers_left == 0:
          return ordered_list
        #the only case we can use the 2 jokers left is if the 2 is natural
        if ordered_list[0].value == 3 and nb_jokers_left == 2:
          ordered_list.insert(0,twos_list.pop())
          joker_card = twos_list.pop() if twos_list else joker_list.pop()
          ordered_list.append(joker_card)
          return ordered_list
        #if there is one joker left, we either place it before 3 if its a two,
        # or put it at the end
        if nb_jokers_left == 1:
          if ordered_list[0].value == 3 and len(twos_list) > 0:
            ordered_list.insert(0,twos_list.pop())
            return ordered_list
          else:
            joker_card = twos_list.pop() if twos_list else joker_list.pop()
            ordered_list.append(joker_card)
            return ordered_list
      return None
