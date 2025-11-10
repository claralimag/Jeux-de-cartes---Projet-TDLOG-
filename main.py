import player
import cards
import boardplayer
import boardgame

def single_player(nom : str) -> None :

    board_person : boardplayer.BoardPlayer = boardplayer.BoardPlayer()
    person : player.Player = player.Player(str, [], board_person, 0)
    



