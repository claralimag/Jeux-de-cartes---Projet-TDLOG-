import boardplayer as bp
from boardgame import BoardGame
from player import Player, Robot, RobotEasy
from cards import Card, affiche_carte


def get_choice(prompt: str, max_val: int) -> int:
    """Ask the user for an integer between 0 and max_val (inclusive)."""
    while True:
        try:
            val = int(input(prompt))
            if 0 <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Invalid input. Please enter an integer between 0 and {max_val}.")


def input_cards() -> tuple[list[int], int]:
    """
    Ask the user which cards to play and which game (sequence) to target.

    :return: (list_of_indices, game_index)
             game_index = -1 means "new game on the board"
    """
    print("Enter the indices of the cards to play (e.g. 0 1 2), separated by spaces:")
    indexes = list(map(int, input("> ").split()))

    print("Enter the index of the game to extend (or -1 for a new game):")
    game_index = int(input("> "))

    return indexes, game_index


def robot_turn(curr_p: Robot, game: BoardGame, curr_idx: int) -> bool:
    """
    Handle one turn for a robot player.
    """
    # --- DRAW PHASE ---
    picked_from_discard = curr_p.robot_pick_cards(curr_idx, game.discard_pile, game.is_open)

    curr_p.show_hand()  #JUST FOR DEBUGGING

    if picked_from_discard and game.discard_pile:
        discard_pile = game.draw_from_discard()
        curr_p.add_cards(discard_pile)
        print(f"{curr_p.name} took {len(discard_pile)} cards from the discard pile.")
    else:
        card = game.draw_from_deck()
        curr_p.add_card(card)
        print(f"{curr_p.name} drew: {affiche_carte(card)}")

    curr_p.show_hand()  #JUST FOR DEBUGGING

    # --- ACTION PHASE ---
    card_to_discard = curr_p.robot_play(curr_idx) 

    # remove the discard card from hand calculation temporarily
    remaining_cards = len(curr_p.cards) - 1

    if remaining_cards == 0 and curr_p.first_game:
        print(f"--- {curr_p.name} FINISHED HAND & TAKES THE POT! ---")
        try:
            new_pot = game.take_pot()
            curr_p.add_cards(new_pot)
            curr_p.first_game = False
            curr_p.score += 100
        except RuntimeError:
            print("No pots left!")
            
    # --- DISCARD PHASE ---
    if card_to_discard:
        curr_p.update_cards([card_to_discard])
        game.add_to_discard(card_to_discard) 
        print(f"{curr_p.name} discarded: {affiche_carte(card_to_discard)}")
        
        # Check if the game ended (Robot went out)
        if len(curr_p.cards) == 0 and not curr_p.first_game:
            if game.can_end(curr_idx):
                self.points += 100
                return True
             
    curr_p.show_hand()  #JUST FOR DEBUGGING

    return False

def human_turn(curr_p: Player, game: BoardGame, curr_idx: int) -> tuple[bool, bool]:
    """
    Handle one turn for a human player.
    Returns (should_stop, first_game_updated)
    """
    # --- DRAW PHASE ---
    curr_p.show_hand()
    print("Draw phase: 0 = Deck | 1 = Take discard pile")
    choice = get_choice("Choice: ", 1)

    if choice == 1 and game.discard_pile:
        picked = game.draw_from_discard()
        curr_p.add_cards(picked)
        print(f"You took {len(picked)} cards from the discard pile.")
    else:
        card = game.draw_from_deck()
        curr_p.add_card(card)
        print(f"You drew: {affiche_carte(card)}")

    # --- ACTION PHASE ---
    while True:
        curr_p.show_hand()
        print("Actions:")
        print("  0 = End turn (discard)")
        print("  1 = Lay a new meld")
        print("  2 = Extend an existing meld")

        action = get_choice("Action: ", 2)
        if action == 0:
            break

        try:
            indexes, game_index = input_cards()
            if action == 1:
                game_index = -1

            cards_to_play = [curr_p.cards[i] for i in indexes if 0 <= i < len(curr_p.cards)]
            if not cards_to_play:
                print("No valid cards selected.")
                continue

            hand_nonempty = curr_p.update_cards(cards_to_play)

            # If the player emptied their hand
            if not hand_nonempty:
                if curr_p.first_game:
                    try:
                        new_pot = game.take_pot()
                        curr_p.add_cards(new_pot)
                        print(f"{curr_p.name} took a new pot with {len(new_pot)} cards.")
                        curr_p.points += 100
                        curr_p.first_game = False
                    except RuntimeError:
                        if game.can_end(curr_idx):
                            print("The game is over.")
                            return True
                        else:
                            print("You cannot end the game yet.")
                else:
                    if game.can_end(curr_idx):
                        print("The game is over.")
                        return True
                    else:
                        print("You cannot end the game yet.")

            # Try to play cards
            points = curr_p.play_cards(cards_to_play, game_index)
            if points > 0:
                print(f"You scored {points} points.")

        except ValueError:
            print("Invalid input (not an integer).")
        except IndexError:
            print("One of the indices is out of range.")

    # --- DISCARD PHASE ---
    curr_p.show_hand()
    if not curr_p.cards:
        print("You have no cards left to discard.")
        return False

    print("Choose the index of the card to discard:")
    idx = get_choice("> ", len(curr_p.cards) - 1)
    card_to_discard = curr_p.cards[idx]
    curr_p.update_cards([card_to_discard])
    game.add_to_discard(card_to_discard)
    print(f"Discarded: {affiche_carte(card_to_discard)}")

    return False


def play(player1: Player, player2: Player) -> None:
    """Main game loop for a 2-player Buraco."""
    print("--- BURACO CONSOLE ---")

    p1 = player1
    p2 = player2
    game = BoardGame([p1, p2], is_open=True)

    curr_idx = 0

    while True:
        curr_p = game.players[curr_idx]
        print(f"\n\n>>> {curr_p.name.upper()}'S TURN <<<")
        game.display_state()

        if isinstance(curr_p, Robot):
            should_stop = robot_turn(curr_p, game, curr_idx)
        else:
            should_stop= human_turn(curr_p, game, curr_idx)

        if should_stop:
            break

        if game.deck_empty():
            if not game.update_deck():
                print("Deck is empty and no more pots left. Game over.")
                break

        curr_idx = game.next_player_index(curr_idx)

    print("\nGame over. Final scores:")
    for p in game.players:
        print(f"{p.name}: {p.score} points")


if __name__ == "__main__":
    p1 = RobotEasy("Alice", [], bp.BoardPlayer(), 0)
    p2 = RobotEasy("Bot", [], bp.BoardPlayer(), 0)
    play(p1, p2)
