import player
import cards
import boardplayer
import boardgame
from random import randint

def single_player(nom : str) -> None :

    board_person : boardplayer.BoardPlayer = boardplayer.BoardPlayer()
    person : player.Player = player.Player(str, [], board_person, 0)
    

def cards_to_add(cards : list[Card], board : BoardPlayer):
    #look for a jocker:
    existsjocker = 0
    n = len(cards)
    if cards[-1] == Suit.JOCKER:
        existsjocker += 1  
    
    dico = {}
    for i in in range(len(board.cardgames)):
        el = board.cardgames[i]
        last = el[0][-1]
        first = el[0][0]
        j = 0 
        while j<n:
            if cards[j] - last== 1: 
                try:
                    dico[i].append(cards[j])
                    last = cards[j]
                    j = 0
                except:
                    dico[i] = [cards[j]]
                    last = cards[j]
                    j=0
            
            if cards[j] - last == 2 and existsjocker>0:
                try:
                    dico[i].append(Suit.JOCKER)
                    existsjocker -= 1
                    dico[i].append(cards[j])
                    last = cards[j]
                    j = 0
                except:
                    dico[i] = [Suit.JOCKER] + [cards[j]]
                    existsjocker -= 1
                    last = cards[j]
                    j=0
                    
            
            if begin - cards[j] == 1: 
                try:
                    dico[i].append(cards[j])
                    last = cards[j]
                    j = 0
                except:
                    dico[i] = [cards[j]]
                    last = cards[j]
                    j=0
            
            if begin - cards[j] == 2 and existsjocker>0:
                try:
                    dico[i].append(Suit.JOCKER)
                    existsjocker -= 1
                    dico[i].append(cards[j])
                    last = cards[j]
                    j = 0
                except:
                    dico[i] = [Suit.JOCKER] + [cards[j]]
                    existsjocker -= 1
                    last = cards[j]
                    j=0
            else: 
                j=j+1
                
    return dico
                


def finds_seqs_by_color(cards : list[Card]):
    seqs = []
    seqs0 = [cards[0]]
    for i in range(1,len(cards)):
        if cards[i] - cards[i-1] == 1: 
    
    
def sequences(cards : list[Card])
    #Assuning cards is ordered
    cards_by_color = {}
    
    for el in list[Card]:
        try:
            cards_by_color[el.suit].append(el)
        except:
            cards_by_color[el.suit] = [el]
    
    n = len(cards_by_color)
    list = []
    for key in cards_by_color:
        list.append(find_seqs_by_color(cards_by_color))
    
    return list
    

    
            
            
    
    

def robot_easy(robot : Player, open : bool, int: whichplayer) -> Card :
    # input : Player representing the computer
    # output : Card to trow out in the trash 
    if open:
        draw_from_discard(whichplayer)
        
    cards_to_add = can_add(robot.cards, robot.board) #dictionnary where key = where you can add a card and dico[key] list of carda you can add
    sequences = exists_sequence(robot.cards)
    deal_with_jocker(cards_to_add, sequences)
    
    for key in cards_to_add:
        robot.play_cards(cards_to_add[key], key, False)
        
    for el in sequences:
        robot.play_cards(el,-1)
    
    #Throw out a random card:
    n = len(robot.cards)
    
    i = randint(0,n)
    
    return robot.cards[i]
        

    

