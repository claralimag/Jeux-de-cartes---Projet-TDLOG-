import pygame
import sys
import os
from typing import List, Tuple
from cards import Card, Suit
from boardplayer import BoardPlayer
from boardgame import BoardGame
from player import Player, Robot, RobotEasy
import boardplayer as bp

# Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
CARD_WIDTH = 60
CARD_HEIGHT = 84
FPS = 60

# Couleurs
BACKGROUND_COLOR = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)

class BuracoGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Buraco - Humain vs Robot")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.load_assets()
        
        # Initialisation du jeu comme dans main.py
        self.p1 = Player("Alice", [], bp.BoardPlayer(), 0)
        self.p2 = RobotEasy("Bot", [], bp.BoardPlayer(), 0)
        self.game = BoardGame([self.p1, self.p2], is_open=True)
        
        self.curr_idx = 0
        self.first_game_flags = [True, True]
        
        self.selected_cards = []
        self.turn_phase = "draw" # "draw", "action", "discard"
        self.message = "C'est votre tour ! Piochez ou prenez la poubelle."
        self.game_over = False

    def load_assets(self):
        self.card_images = {}
        suits = ["hearts", "diamonds", "clubs", "spades"]
        for suit in suits:
            for val in range(1, 14):
                if val == 1: name = "ace"
                elif val == 11: name = "jack"
                elif val == 12: name = "queen"
                elif val == 13: name = "king"
                else: name = str(val)
                
                filename = f"{name}_of_{suit}.png"
                try:
                    img = pygame.image.load(filename)
                    self.card_images[(suit, val)] = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                except:
                    # Fallback si l'image manque
                    img = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
                    img.fill(WHITE)
                    self.card_images[(suit, val)] = img
        
        try:
            self.card_images["joker"] = pygame.transform.scale(pygame.image.load("joker.png"), (CARD_WIDTH, CARD_HEIGHT))
            self.back_image = pygame.transform.scale(pygame.image.load("back_side.png"), (CARD_WIDTH, CARD_HEIGHT))
        except:
            self.card_images["joker"] = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            self.back_image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            self.back_image.fill((0, 0, 255))

    def get_card_image(self, card):
        if card.suit == Suit.JOKER:
            return self.card_images.get("joker")
        suit_map = {Suit.HEARTS: "hearts", Suit.DIAMONDS: "diamonds", Suit.CLUBS: "clubs", Suit.SPADES: "spades"}
        return self.card_images.get((suit_map.get(card.suit), card.value), self.back_image)

    def get_hand_card_pos(self, index):
        """Calcule la position d'une carte dans la main avec superposition horizontale."""
        margin_x = 10
        margin_y = SCREEN_HEIGHT - CARD_HEIGHT - 20
        overlap_x = 20 # On voit 20 pixels de chaque carte
        cards_per_row = (SCREEN_WIDTH // 3 - margin_x * 2 - CARD_WIDTH) // overlap_x + 1
        
        row = index // cards_per_row
        col = index % cards_per_row
        
        x = margin_x + col * overlap_x
        y = margin_y - row * (CARD_HEIGHT + 10)
        return x, y

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Trier les cartes du joueur par couleur puis valeur
        # Suit order: Clubs, Diamonds, Hearts, Spades, Joker
        suit_order = {Suit.CLUBS: 0, Suit.DIAMONDS: 1, Suit.HEARTS: 2, Suit.SPADES: 3, Suit.JOKER: 4}
        self.p1.cards.sort(key=lambda c: (suit_order.get(c.suit, 5), c.value))
        
        # Séparateurs
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH // 3, 0), (SCREEN_WIDTH // 3, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE, (2 * SCREEN_WIDTH // 3, 0), (2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 2)
        
        # Scores
        self.screen.blit(self.big_font.render(f"your score: {self.p1.score}", True, WHITE), (20, 20))
        self.screen.blit(self.big_font.render(f"robot score: {self.p2.score}", True, WHITE), (2 * SCREEN_WIDTH // 3 + 20, 20))
        
        # Message
        msg_surface = self.font.render(self.message, True, HIGHLIGHT_COLOR)
        self.screen.blit(msg_surface, (SCREEN_WIDTH // 3 + 10, SCREEN_HEIGHT - 40))

        # --- Zone Milieu (Pioche et Poubelle) ---
        mid_x = SCREEN_WIDTH // 3
        # Pioche
        if not self.game.deck_empty():
            self.screen.blit(self.back_image, (mid_x + 30, 50))
            self.screen.blit(self.font.render("Deck", True, WHITE), (mid_x + 30, 30))
        
        # Poubelle
        self.screen.blit(self.font.render("Discard Pile", True, WHITE), (mid_x + 30, 150))
        for i, card in enumerate(self.game.discard_pile):
            img = self.get_card_image(card)
            self.screen.blit(img, (mid_x + 30, 180 + i * 18))

        # --- Zone Joueur (Gauche) ---
        # Main du joueur (en bas, superposition horizontale)
        for i, card in enumerate(self.p1.cards):
            img = self.get_card_image(card)
            x, y = self.get_hand_card_pos(i)
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            if card in self.selected_cards:
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, rect.inflate(4, 4), 2)
            self.screen.blit(img, rect)

        # Melds du joueur
        for i, game_tuple in enumerate(self.p1.board.cardgames):
            meld_cards = game_tuple[0]
            for j, card in enumerate(meld_cards):
                img = self.get_card_image(card)
                self.screen.blit(img, (10 + i * 65, 80 + j * 15))

        # --- Zone Robot (Droite) ---
        # Main du robot (verso, en haut)
        for i in range(len(self.p2.cards)):
            x = 2 * SCREEN_WIDTH // 3 + 10 + (i % 6) * 12
            y = 50 + (i // 6) * 12
            self.screen.blit(self.back_image, (x, y))
            
        # Melds du robot
        for i, game_tuple in enumerate(self.p2.board.cardgames):
            meld_cards = game_tuple[0]
            for j, card in enumerate(meld_cards):
                img = self.get_card_image(card)
                self.screen.blit(img, (2 * SCREEN_WIDTH // 3 + 10 + i * 65, 250 + j * 15))

        pygame.display.flip()

    def handle_click(self, pos):
        if self.game_over or self.curr_idx != 0: return

        mid_x = SCREEN_WIDTH // 3
        
        # --- PHASE PIOCHE ---
        if self.turn_phase == "draw":
            # Clic sur Deck
            if pygame.Rect(mid_x + 30, 50, CARD_WIDTH, CARD_HEIGHT).collidepoint(pos):
                card = self.game.draw_from_deck()
                self.p1.add_card(card)
                self.turn_phase = "action"
                self.message = "Action : Sélectionnez des cartes pour poser/étendre ou cliquez sur la poubelle pour défausser."
                return
            # Clic sur Poubelle
            if self.game.discard_pile:
                discard_rect = pygame.Rect(mid_x + 30, 180, CARD_WIDTH, len(self.game.discard_pile) * 18 + CARD_HEIGHT)
                if discard_rect.collidepoint(pos):
                    cards = self.game.draw_from_discard()
                    self.p1.add_cards(cards)
                    self.turn_phase = "action"
                    self.message = "Action : Sélectionnez des cartes pour poser/étendre ou cliquez sur la poubelle pour défausser."
                    return

        # --- PHASE ACTION ---
        if self.turn_phase == "action":
            # Sélection de cartes en main (vérifier de la plus haute vers la plus basse)
            for i in range(len(self.p1.cards) - 1, -1, -1):
                card = self.p1.cards[i]
                x, y = self.get_hand_card_pos(i)
                if pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT).collidepoint(pos):
                    if card in self.selected_cards: self.selected_cards.remove(card)
                    else: self.selected_cards.append(card)
                    return

            # Poser un nouveau jeu (clic sur zone vide du plateau joueur)
            player_board_rect = pygame.Rect(0, 80, SCREEN_WIDTH // 3, 350)
            if player_board_rect.collidepoint(pos) and self.selected_cards:
                self.try_play_cards(-1) #changer try play a add to game/board
                return

            # Étendre un jeu existant
            for i, game_tuple in enumerate(self.p1.board.cardgames):
                meld_rect = pygame.Rect(10 + i * 65, 80, CARD_WIDTH, 250)
                if meld_rect.collidepoint(pos) and self.selected_cards:
                    self.try_play_cards(i) #ici il faut sans doute add to board game 
                    return

            # Défausser (clic sur la poubelle)
            if pygame.Rect(mid_x + 30, 180, CARD_WIDTH, 350).collidepoint(pos):
                if len(self.selected_cards) == 1:
                    # Défausse directe de la carte sélectionnée
                    card_to_discard = self.selected_cards[0]
                    self.p1.update_cards([card_to_discard])
                    self.game.add_to_discard(card_to_discard)
                    self.selected_cards = []
                    self.end_human_turn()
                elif not self.selected_cards:
                    # Mode défausse classique si rien n'est sélectionné
                    self.turn_phase = "discard"
                    self.message = "Défausse : Cliquez sur une carte de votre main pour terminer le tour."
                else:
                    self.message = "Erreur : Sélectionnez une seule carte pour défausser."
                return

        # --- PHASE DEFAUSSE ---
        if self.turn_phase == "discard":
            for i in range(len(self.p1.cards) - 1, -1, -1):
                card = self.p1.cards[i]
                x, y = self.get_hand_card_pos(i)
                if pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT).collidepoint(pos):
                    self.p1.update_cards([card])
                    self.game.add_to_discard(card)
                    self.end_human_turn()
                    return

    def try_play_cards(self, game_index):
        cards_to_play = self.selected_cards[:]
        
        try:
            # On tente de jouer les cartes
            # Note: Dans main.py, update_cards est appelé avant play_cards
            # Si play_cards échoue ou renvoie 0, on doit restaurer la main
            
            # Sauvegarde temporaire de la main
            original_hand = self.p1.cards[:]
            
            hand_nonempty = self.p1.update_cards(cards_to_play)
            points = self.p1.play_cards(cards_to_play, game_index)
            
            if points <= 0:
                # Action invalide selon les règles du jeu
                self.p1.cards = original_hand
                self.message = "Action invalide ! Essayez un autre coup."
            else:
                # Action réussie, gérer le pot/fin de jeu
                if not hand_nonempty:
                    if self.first_game_flags[0]:
                        try:
                            new_pot = self.game.take_pot()
                            self.p1.add_cards(new_pot)
                            self.first_game_flags[0] = False
                            self.message = "Vous avez pris le pot !"
                        except RuntimeError:
                            if self.game.can_end(0):
                                self.game_over = True
                                self.message = "Félicitations ! Vous avez gagné."
                    else:
                        if self.game.can_end(0):
                            self.game_over = True
                            self.message = "Félicitations ! Vous avez gagné."
                else:
                    self.message = f"Coup réussi ! (+{points} pts). Continuez ou défaussez."
            
        except Exception as e:
            # Capture toute erreur (ValueError, IndexError, etc.) pour éviter le crash
            self.message = f"Erreur : Action impossible. Réessayez."
            # Restaurer la main si elle a été modifiée
            if len(self.p1.cards) < len(original_hand):
                self.p1.cards = original_hand
        
        self.selected_cards = []

    def end_human_turn(self):
        if self.game_over: return
        
        # Vérifier si le deck est vide
        if self.game.deck_empty():
            if not self.game.update_deck():
                self.game_over = True
                self.message = "Jeu terminé : Deck vide."
                return

        self.curr_idx = self.game.next_player_index(self.curr_idx)
        self.robot_turn_logic()

    def robot_turn_logic(self):
        self.message = "Le robot réfléchit..."
        self.draw()
        pygame.time.delay(1000)
        
        # Appel de robot_turn de main.py (adapté)
        # robot_turn(curr_p, game, curr_idx, first_game)
        from main import robot_turn
        should_stop = robot_turn(self.p2, self.game, self.curr_idx, self.first_game_flags[1])
        
        if should_stop:
            self.game_over = True
            self.message = "Le robot a gagné."
            return

        if self.game.deck_empty():
            if not self.game.update_deck():
                self.game_over = True
                self.message = "Jeu terminé : Deck vide."
                return

        self.curr_idx = self.game.next_player_index(self.curr_idx)
        self.turn_phase = "draw"
        self.message = "C'est votre tour ! Piochez ou prenez la poubelle."

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = BuracoGUI()
    gui.run()
