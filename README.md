# Jeux de cartes : Buraco - Projet TDLOG

Our goal is to implement a game of Buraco. 

Buraco is a brazilian game of cards that can be played with different games modes. We chose to implement a two person game with open trash.

# Game Rules : 

1. Deck Composition
   
The game is played using two standard 52-card decks, including jokers, shuffled together into a single deck.

2. Players

The game is played by two players
Players compete individually (no teams)

3. Initial Setup

Each player is dealt 11 cards. Two additional piles of 11 cards each are set aside face down as mortos. One card is placed face up to start the discard pile (trash). The remaining cards form the draw pile.

4. Objective

The objective of the game is to: Create valid melds, form at least one Buraco, take a morto, score more points than the opponent.

5. Turn Structure

On their turn, a player must perform the following actions in order:

Draw cards, choosing one option:

Draw one card from the draw pile, or take the entire discard pile.

Play melds (optional): Lay down new melds or add cards to existing melds.

Discard one card to end the turn.

6. Melds

A meld is a valid group of cards placed on the table.

Melds must be sequences of three or more cards with same suit, consecutive rank order. Wildcards may be used.

Example:
5♥ – 6♥ – 7♥

7. Wildcards
    
Jokers and twos (2s) act as wildcards. A meld cannot be composed entirely of wildcards. Each meld must contain at least two natural cards and at most one wildcard.

8. Buraco

A Buraco is a meld containing seven or more cards. Clean Buraco: contains no wildcards and dirty Buraco: contains one or more wildcards.

9. Mortos

Mortos are reserve piles that players must take before they can end the game. Each morto contains 11 cards. Mortos remain face down until taken. A player may take a morto only after playing all cards from their hand.  When a player takes a morto: the morto becomes their new hand and the player continues the game normally on subsequent turns.

10. Going Out

A player may go out when all of the following conditions are met: they have formed at least one Buraco, they have taken a morto (if available), they have played all cards from their hand, they discard their final card (unless the game ends by melding).

11. Scoring

Scoring is determined by: points from cards in melds, bonuses for clean and dirty Buracos, penalties for cards remaining in hand, bonuses for going out.








