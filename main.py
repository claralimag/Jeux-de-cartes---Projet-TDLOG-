import player
import cards
import boardplayer as bp 
import boardgame as bg
from cards import Card, Suit
from player import Player, Robot
from boardplayer import BoardPlayer
from boardgame import BoardGame 
from random import randint

def robot_play_cards_easy(robot : Robot, board : BoardGame, whichplayer : int) -> Card:
        # input : Player representing the computer
        # output : Card to trow out in the trash 

        board.draw_from_discard(whichplayer)  #robot draws from the discard pile if possible

        card_to_throw = robot.robot_play_cards_easy(whichplayer) #robot plays a card if possible

        return card_to_throw



    

