from game import Game
from chopsticks_logger import logger
import sys

def __main__():
    game = Game('computer', 'human')
    if game.player1.left_hand.modifier == 7:
        sys.setrecursionlimit(2000)
    game.print_status()
    game.start()
            
if __name__ == "__main__":
    __main__()
