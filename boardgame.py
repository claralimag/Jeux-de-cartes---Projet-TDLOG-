# BoardGame : defines the board of the game (players, deck, discard pile, functions : add player, remove player, draw card from deck, draw card from discard pile, add card to discard pile)
import random
from player import Player
from cards import Card, Suit
from typing import Optional 

class BoardGame:
    def __init__(self, players: list[Player], is_open: bool) -> None:
        """
         Main game board.
        :param players: List of players sitting at the table
        :param is_open: True if the game is "open buraco", False otherwise
        """

    def __init__(self, players: list[Player], is_open: bool) -> None:
        """
        Main game board.

        :param players: List of players sitting at the table
        :param is_open: True if the game is "open buraco", False otherwise
        """
        self.players: list[Player] = players
        self.is_open: bool = is_open

        # --- Build and shuffle the full deck ---
        self.deck: list[Card] = []
        for _ in range(2):
            for s in [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]:
                for v in range(1, 14):
                    self.deck.append(Card(s, v))
        for _ in range(4):  # Jokers
            self.deck.append(Card(Suit.JOKER, 0))
        random.shuffle(self.deck)

        # --- Create the two pots (11 cards each) ---
        pot_1: list[Card] = [self.deck.pop() for _ in range(11)]
        pot_2: list[Card] = [self.deck.pop() for _ in range(11)]
        self.pots: list[list[Card]] = [pot_1, pot_2]

        # --- Deal 11 cards to each player ---
        for _ in range(11):
            for p in self.players:
                p.add_card(self.draw_from_deck())

        # --- Initialize discard pile ---
        self.discard_pile: list[Card] = []
        self.add_to_discard(self.draw_from_deck())


    # ---------- Player management ----------

    def add_player(self, player: Player) -> None:
        """Add a player to the table."""
        self.players.append(player)

    def remove_player(self, player: Player) -> None:
        """Remove a player from the table."""
        self.players.remove(player)

    # ---------- Deck / discard pile management ----------

    def draw_from_deck(self) -> Card:
        """
        Draw a single card from the top of the deck.

        :return: Card drawn from the deck
        :raises RuntimeError: if the deck is empty
        """
        if not self.deck :
            raise RuntimeError("Deck is empty!")
        
        return self.deck.pop()

    def draw_from_discard(self) -> list[Card]:
        """
        Take the whole discard pile (used when a player picks up the discard).

        :return: List of cards that were in the discard pile
        :raises RuntimeError: if the discard pile is empty
        """
        if not self.discard_pile:
            raise RuntimeError("Discard pile is empty!")

        cards = self.discard_pile.copy()
        self.discard_pile.clear()
        return cards

    def add_to_discard(self, card: Card) -> None:
        """
        Add a single card on top of the discard pile.

        :param card: Card to add to the discard pile
        """
        self.discard_pile.append(card)
    
    def take_pot(self) -> list[Card]:
        """
        Give a new pot (set of 11 cards) to a player/team.

        :return: The list of cards in the pot
        :raises RuntimeError: if there is no pot left
        """
        if not self.pots:
            raise RuntimeError("No pots left!")

        return self.pots.pop()
    
    def deck_empty(self) -> bool:
        """Return True if the deck is empty."""
        return len(self.deck) == 0

    def update_deck(self) -> bool:
        """
        Refill the deck using one of the remaining pots.
        :return: True if the deck was refilled, False if no pots remain
        """
        if self.pots:
            self.deck = self.pots.pop()
            return True
        return False
    
    def can_end(self, whichplayer: int) -> bool:
        """
        Check if the player can end the game.
        (Example condition: has at least one clean sequence of 7+ cards)
        """
        player = self.players[whichplayer]
        for seq in player.board:  # adapt depending on BoardPlayer structure
            # Suppose each element of player.board is (sequence, is_clean)
            if len(seq[0]) >= 7 and seq[1]:
                return True
        return False

# ---------- Turn management / display ----------

    def next_player_index(self, current_index: int) -> int:
        """
        Return the index of the next player at the table (circular).

        :param current_index: Index of the current player
        :return: Index of the next player
        """
        return (current_index + 1) % len(self.players)

    def display_state(self) -> None:
        """
        Print a small summary of the table:
        - each player with hand size and score
        - top card of the discard pile
        """
        print("\n========== TABLE ==========")
        for p in self.players:
            print(f"{p.name} ({len(p.cards)} cards, score={p.score})")

        if self.discard_pile:
            print(f"Discard (top): {self.discard_pile[-1]}")
        else:
            print("Discard: empty")

        print("============================\n")