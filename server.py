import socket
import builtins
from typing import List, Tuple, Any

import main as game_main
from player import Player
from boardplayer import BoardPlayer

HOST = "0.0.0.0"
PORT = 5050

REMOTES: List["Remote"] = []
CURRENT_PLAYER_INDEX = 0  # 0 ou 1


class Remote:
    """Connexion client """
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


def broadcast(msg: str) -> None:
    """Envoie un message à tout le monde."""
    for line in str(msg).splitlines():
        for r in REMOTES:
            r.send_line(line)


def send_to_current(msg: str) -> None:
    """Envoie un message uniquement au joueur courant."""
    r = REMOTES[CURRENT_PLAYER_INDEX]
    for line in str(msg).splitlines():
        r.send_line(line)


def net_print(*args, **kwargs):
    """print() -> broadcast réseau (tout le monde voit)."""
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    text = sep.join(str(a) for a in args) + end
    # On envoie ligne par ligne (plus propre côté client)
    for line in text.splitlines():
        broadcast(line)


def net_input(prompt: str = "") -> str:
    """input() -> uniquement au joueur courant."""
    send_to_current("INPUT: " + str(prompt))
    ans = REMOTES[CURRENT_PLAYER_INDEX].recv_line()
    if ans == "":
        raise ConnectionError("Client déconnecté.")
    return ans


def as_bool_should_stop(x: Any) -> bool:
    if isinstance(x, tuple) and len(x) >= 1:
        return bool(x[0])
    return bool(x)


def main():
    global REMOTES, CURRENT_PLAYER_INDEX

    # 1) Écoute et accepte 2 clients
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, PORT))
    srv.listen(2)
    print(f"[SERVER] écoute sur {HOST}:{PORT} (attend 2 joueurs)")

    REMOTES = []
    while len(REMOTES) < 2:
        conn, addr = srv.accept()
        r = Remote(conn, addr)
        REMOTES.append(r)
        print("[SERVER] connecté:", addr)
        r.send_line("--- BURACO (réseau console) ---")
        r.send_line("Connecté. Attente du second joueur...")

    # 2) Patch print/input pour le réseau
    old_print = builtins.print
    old_input = builtins.input
    builtins.print = net_print
    builtins.input = net_input

    # 3) Patch human_turn pour router input vers le bon joueur
    old_human_turn = game_main.human_turn

    def human_turn_wrapper(curr_p, game, curr_idx):
        global CURRENT_PLAYER_INDEX
        CURRENT_PLAYER_INDEX = curr_idx
        return old_human_turn(curr_p, game, curr_idx)

    game_main.human_turn = human_turn_wrapper

    # 4) Patch show_hand : main visible seulement au joueur courant
    old_show_hand = Player.show_hand

    def show_hand_only_current(self):
        send_to_current(f"\nHand of {self.name}:")
        for idx, card in enumerate(self.cards):
            # __str__ de Card utilise affiche_carte chez toi
            send_to_current(f"{idx}: {card}")

    Player.show_hand = show_hand_only_current

    try:
        # 5) Crée 2 joueurs 
        p1 = Player("Joueur1", [], BoardPlayer(), 0)
        p2 = Player("Joueur2", [], BoardPlayer(), 0)

        # Noms 
        CURRENT_PLAYER_INDEX = 0
        p1.name = input("Nom du joueur 1 : ").strip() or "Joueur1"
        CURRENT_PLAYER_INDEX = 1
        p2.name = input("Nom du joueur 2 : ").strip() or "Joueur2"

        broadcast("")
        broadcast("=== La partie commence ! ===")

        # 6) Lance le jeu 
        game_main.play(p1, p2)

    except ConnectionError:
        old_print("[SERVER] Un client s'est déconnecté. Arrêt.")
    finally:
        # restore patches
        builtins.print = old_print
        builtins.input = old_input
        game_main.human_turn = old_human_turn
        Player.show_hand = old_show_hand

        for r in REMOTES:
            try:
                r.conn.close()
            except OSError:
                pass
        try:
            srv.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
