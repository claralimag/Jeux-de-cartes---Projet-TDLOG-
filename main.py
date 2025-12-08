import boardplayer as bp 
import boardgame as bg
from cards import Card, Suit
from player import Player, Robot, RobotEasy
from boardplayer import BoardPlayer
from boardgame import BoardGame 
from random import randint

def get_choice(prompt, max_val):
    while True:
        try:
            val = int(input(prompt))
            if 0 <= val <= max_val:
                return val
        except ValueError:
            pass
        print("Entrée invalide.")

def input_cards() -> list[Card]:
        print("Entrez les indices des cartes à jouer (ex: 0 1 2) séparés par espace:")
        indexes = list(map(int, input("> ").split()))

        print("Entrez le numéro du jeu à compléter (ou -1 pour un nouveau jeu):")
        whichgame = int(input("> "))
        return indexes, whichgame

def robot_play_cards_easy(robot : Robot, board : BoardGame, whichplayer : int) -> Card:
        # input : Player representing the computer
        # output : Card to trow out in the trash 

        board.draw_from_discard(whichplayer)  #robot draws from the discard pile if possible

        card_to_throw = robot.robot_play_cards_easy(whichplayer) #robot plays a card if possible

        return card_to_throw


def play(player1 : Player, player2 : Player):
    print("--- BURACO CONSOLE ---")

# We create a board for each player
    bp1 = bp.BoardPlayer()
    bp2 = bp.BoardPlayer()
    p1 = player1
    p2 = player2

# We create the game board
    game = bg.BoardGame([p1, p2], open=True)
    game.setup_game()
    
    curr_idx = 0

    while True:
        curr_p = game.players[curr_idx]
        print(f"\n\n>>> C'EST A {curr_p.name.upper()} <<<")
        game.display_state()

        if isinstance(game.players[curr_idx], Robot):
                # 1. PIOCHE
                picked_cards = curr_p.robot_pick_cards(curr_idx, game.discard_pile, game.is_open) #True if we pick cards from the trash

                if picked_cards:
                        cards = game.draw_from_discard(curr_idx)
                        print(f"Le robot a ramassé {len(picked_cards)} cartes.")
                        curr_p.add_cards(cards)

                else :
                        card = game.draw_from_deck()
                        if card is None:
                                print("Plus de cartes ! Fin du jeu.")
                                break
                        curr_p.add_card(card)
                        print(f"Le robot a pioché : {card}")

                # 2. ACTIONS
                card_to_throw = curr_p.robot_play(curr_idx)
                game.add_to_discard(card_to_throw)
                curr_p.update_cards([card_to_throw])
                print(f"Le robot a défaussé : {card_to_throw}")

        else:
                curr_p.show_hand()

                # 1. PIOCHE 
                print("0: Deck | 1: Ramasser Défausse")
                choix = get_choice("Choix: ", 1)
                if choix == 1 and game.discard_pile:
                        picked = game.draw_from_discard(curr_idx)
                        print(f"Vous avez ramassé {len(picked)} cartes.")
                        curr_p.add_cards(picked)
                
                else:
                        card = game.draw_from_deck()
                        if card is None:
                                print("Plus de cartes ! Fin du jeu.")
                                break
                        curr_p.add_card(card)
                        print(f"Pioché : {card}")
                
                curr_p.show_hand()

                # 2. ACTIONS
                # stopping condition: 

                print("Actions: 0: Finir tour (Défausser) | 1: Poser un nouveau jeu | 2: Compléter un jeu")
                i = get_choice("Action: ", 2)

                while i > 0: 
                        print("Entrez les indices des cartes à jouer (ex: 0 1 2) séparés par espace et le jeu auquel tu souhaites ajouter (si c'est le cas):")
                        try:
                                selected_cards, whichgame = input_cards()
                                indexes = list(map(int, input("> ").split()))
                                cards_to_play = [curr_p.cards[i] for i in indexes if 0 <= i < len(curr_p.cards)]
        
                                curr_p.play_cards(cards_to_play,whichgame=whichgame)
        
                        except ValueError:
                                print("Entrée invalide.")
                                continue

                # 3. DEFAUSSE
                print("Choisissez l'index de la carte à défausser:")
                idx = get_choice("> ", len(curr_p.cards)-1)
                c = curr_p.cards[idx]
                curr_p.update_cards([c])
                game.add_to_discard(c)
                print(f"Défaussé: {c}")

        curr_idx = game.next_player_index(curr_idx)

    print("Fin du jeu. Merci d'avoir joué !")
    print("Scores finaux :")
    for p in game.players:
        print(f"{p.name} : {p.score} points")

#Commentaires : Il faut adapter boardgame ´pour considérer la version fermée ou ouverte du jeu. 
# Il faut regarder des stratégies plus complexes pour le robot (piocher dans la défausse seulement si ça l'aide à compléter un jeu, etc.)
# Il faut implémenter dans la deuxième partie la gestion des pots (vérifier si un joueur a vidé son boardplayer, distribuer les points des pots, etc.)
# Une fois ceci-fait il faut vérifier que les règles sont bien respectées: on ne peut finir que avec une canasta, etc.
# Traiter l'exception dans play_cards

if __name__ == "__main__":
    p1 = Player("Alice", [], bp.BoardPlayer(), 0)
    p2 = RobotEasy("Bot", [], bp.BoardPlayer(), 0)
    play(p1, p2)
    
