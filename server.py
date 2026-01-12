import socket
import builtins
from typing import List, Tuple

import main as game_main  
from player import Player
from boardplayer import BoardPlayer

HOST = "0.0.0.0"
PORT = 5050

REMOTES: List["Remote"] = []
CURRENT_PLAYER_INDEX = 0  # 0 ou 1


class Remote:
    def __init__(self, conn: socket.socket, addr: Tuple[str, int]):
        self.conn = conn
        self.addr = addr
        self.buffer = ""

    def send_line(self, line: str) -> None:
        if not line.endswith("\n"):
            line += "\n"
        self.conn.sendall(line.encode("utf-8", errors="replace"))

    def recv_line(self) -> str:
        while "\n" not in self.buffer:
            data = self.conn.recv(4096)
            if not data:
                return ""
            self.buffer += data.decode("utf-8", errors="replace")

        line, self.buffer = self.buffer.split("\n", 1)
        return line.rstrip("\r")


def broadcast_line(line: str) -> None:
    """Envoie une ligne à tous les clients."""
    for r in REMOTES:
        r.send_line(line)


def send_to_current(line: str) -> None:
    """Envoie une ligne uniquement au joueur courant."""
    REMOTES[CURRENT_PLAYER_INDEX].send_line(line)


def patched_print(*args, **kwargs):
    """
    Remplace print() :
    tout ce qui est imprimé est envoyé aux 2 joueurs.
    """
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    msg = sep.join(str(a) for a in args) + end

    for line in msg.splitlines():
        broadcast_line(line)


def patched_input(prompt=""):
    """
    Remplace input() :
    """
    send_to_current("INPUT: " + str(prompt))
    ans = REMOTES[CURRENT_PLAYER_INDEX].recv_line()
    if ans == "":
        raise ConnectionError("Client déconnecté.")
    return ans


def main():
    global REMOTES, CURRENT_PLAYER_INDEX

    # 1) Serveur écoute et accepte 2 clients
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(2)
    print(f"Serveur en écoute sur {HOST}:{PORT} (attend 2 joueurs)")

    REMOTES = []
    while len(REMOTES) < 2:
        conn, addr = server_sock.accept()
        r = Remote(conn, addr)
        REMOTES.append(r)
        print("Joueur connecté:", addr)
        r.send_line("--- BURACO (mode réseau console) ---")
        r.send_line("Connecté. En attente du second joueur...")

    # 2) Patch print/input pour passer par le réseau
    old_print = builtins.print
    old_input = builtins.input
    builtins.print = patched_print
    builtins.input = patched_input

  
    old_human_turn = game_main.human_turn

    def human_turn_wrapper(curr_p, game, first_game, curr_idx):
        global CURRENT_PLAYER_INDEX
        CURRENT_PLAYER_INDEX = curr_idx  # 0 ou 1
        return old_human_turn(curr_p, game, first_game, curr_idx)

    game_main.human_turn = human_turn_wrapper

    old_show_hand = Player.show_hand

    def show_hand_only_current(self):
        send_to_current(f"\nHand of {self.name}:")
        for idx, card in enumerate(self.cards):
            send_to_current(f"{idx}: {card}")

    Player.show_hand = show_hand_only_current

    try:
        # 5) Créer 2 joueurs humains (pas de Robot)
        p1 = Player("Joueur1", [], BoardPlayer(), 0)
        p2 = Player("Joueur2", [], BoardPlayer(), 0)

        # Demander les noms (ces input vont au joueur courant)
        CURRENT_PLAYER_INDEX = 0
        p1.name = input("Nom du joueur 1 : ").strip() or "Joueur1"
        CURRENT_PLAYER_INDEX = 1
        p2.name = input("Nom du joueur 2 : ").strip() or "Joueur2"

        # Message de démarrage
        broadcast_line("")
        broadcast_line("=== La partie commence ! ===")

        # 6) Lancer ton jeu existant tel quel
        game_main.play(p1, p2)

    except ConnectionError:
        old_print("Un client s'est déconnecté. Le serveur s'arrête.")
    finally:
        # Restore patches
        builtins.print = old_print
        builtins.input = old_input
        game_main.human_turn = old_human_turn
        Player.show_hand = old_show_hand

        # Fermer connexions
        for r in REMOTES:
            try:
                r.conn.close()
            except OSError:
                pass
        try:
            server_sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
