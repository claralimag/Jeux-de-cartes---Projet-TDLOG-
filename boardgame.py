# BoardGame : defines the board of the game (players, deck, discard pile, functions : add player, remove player, draw card from deck, draw card from discard pile, add card to discard pile)
import random
from player import Player
from rules import Rules
from cards import Card, Suit


class BoardGame:
    def __init__(self, players0 : list[Player], open : bool):

        self.players = players0

        #Initial deck 
        self.deck = []

        #Initial pot 
        self.pots : tuple[list[Card], list[Card]]

        #Init discard pile :
        self.discard_pile = []

        #Open Buraco
        self.is_open : bool = open

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def draw_from_deck(self):
        if not self.deck:
            raise Exception("Deck is empty!")
        return self.deck.pop()

    def draw_from_discard(self, whichplayer : int) -> None:
        if not self.discard_pile:
            raise Exception("Discard pile is empty!")
        
        self.players[whichplayer].add_card(self.discard_pile)
        self.discard_pile = []

    def draw_from_discard(self, whichplayer : int, cards : list[Card]) -> None:
        if not self.discard_pile:
            raise Exception("Discard pile is empty!")
        
        score : int = self.players[whichplayer].play_cards(self.discard_pile + cards)

        if score == 0:
            print("You can't draw from the trash")

        else:
            self.discard_pile = []

    def add_to_discard(self, card):
        self.discard_pile.append(card)

    # Distribution initiale et gestion du tour
    def setup_game(self, rules: Rules):
        """Crée le jeu, mélange les cartes et distribue aux joueurs"""
        # Création du paquet (2x52 + jokers)
        from cards import Card, Suit
        self.deck = []
        for _ in range(2):
            for s in [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]:
                for v in range(1, 14):
                    self.deck.append(Card(s, v))
        # Jokers
        for _ in range(4):
            self.deck.append(Card(Suit.JOKER, 0))

        random.shuffle(self.deck)

        pot_1 : list[Card] = []
        pot_2 : list[Card] = []

        # Distribuer 11 cartes à chaque joueur
        for _ in range(rules.cards_per_player):
            el1 = random.randint(0,len(self.deck))
            pot_1.append(self.deck(el1))
            self.deck.pop(el1)

            el2 = random.randint(0,len(self.deck))
            pot_2.append(self.deck(el2))
            self.deck.pop(el2)

            for p in self.players:
                p.add_card(self.deck.pop())

        self.pots : tuple[list[Card], list[Card]] = [pot_1, pot_2]

        # Première carte sur la défausse
        self.discard_pile.append(self.deck.pop())

    def next_player_index(self, current_index):
        """Retourne l’indice du joueur suivant"""
        return (current_index + 1) % len(self.players)

    def display_state(self):
        """Affiche un petit résumé du plateau"""
        print("\n========== TABLE ==========")
        for p in self.players:
            print(f"{p.name} ({len(p.cards)} cartes, score={p.score})")
        print(f"Défausse : {self.discard_pile[-1]}")
        print("============================\n")
