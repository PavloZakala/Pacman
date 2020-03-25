import random
import numpy as np
import copy

from base_game import BaseGame
from maps.base_map import BaseMap
from utils.direction import Direction

class Pacman(BaseGame):

    name = "Pac-Man"
    
    GOAL = 'g'

    action = {
        0: lambda y, x: (y+1, x),
        1: lambda y, x: (y, x+1),
        2: lambda y, x: (y-1, x),
        3: lambda y, x: (y, x-1),
    }

    def __init__(self, width=20, height=10, num_ghost=0, goal_size=100, inputMap=BaseMap):

        self.width = width
        self.height = height

        current_map = inputMap(width, height)

        self.start_board  = current_map.get_map()
        self.board = copy.deepcopy(self.start_board)
        self.width = len(self.board[0])
        self.height = len(self.board)

        (y, x) = self.set_position(self.board)
        self.pacman = (y, x)
        self.board[y][x] = str(0)
        

        self.ghost = {}
        self.check_goal = {}
        self.player_goal = {}

        for i in range(1, num_ghost+1):
            (y, x) = self.set_position(self.board)
            self.ghost[i] = (y, x)
            self.board[y][x] = str(i)
            self.player_goal[i] = '0'
            self.check_goal[i] = lambda s, p: s == p

        self.goal = {}
        self.find_goal = 0

        for i in range(goal_size):
            p = self.set_position(self.board, drop=True)
            if p is None:
                continue
            (y, x) = p
            self.goal[(y, x)] = True
            self.board[y][x] = self.GOAL

        self.check_goal[0] = lambda s: len(s.goal) == self.find_goal
        
        self.players = self.ghost.copy()
        self.players[0] = self.pacman
        self.player_goal[0] = self.GOAL


    def set_position(self, board, drop=False):
        i = 0
        while True:
            y = random.randint(0, self.height-1)
            x = random.randint(0, self.width-1)
            i += 1
            if board[y][x] == ' ':                
                return (y, x)
            if (i > 500) and drop:
                return None
                


    def getBoardSize(self):

        return (self.width, self.height)

    def getNextState(self, p, a):
        
        (y, x) = self.players[p]
        
        (ny, nx) = self.action[a](y, x)

        if self.board[ny][nx] in self.player_goal[p] and p == 0:
            self.goal[(ny, nx)] = False
            self.find_goal += 1

        self.board[y][x] = ' '        
        self.board[ny][nx] = str(p)

        self.players[p] = (ny, nx)

        for (y, x) in self.goal.keys():
            if self.goal[(y, x)] and self.board[y][x] == ' ':
                self.board[y][x] = 'g'

        return self.board, (p + 1) % len(self.players)

    def getValidMoves(self, p):
        
        (y, x) = self.players[p]
        res = [True for i in range(4)]
        if y == 0 or self.board[2*y-1][2*x+1] == 'O':
            res[0] = False
        if x == 0 or self.board[2*y+1][2*x-1] == 'O':
            res[1] = False

        if y == self.height - 1 or self.board[2*y+3][2*x+1] == 'O':
            res[2] = False
        if x == self.width - 1 or self.board[2*y+1][2*x+3] == 'O':
            res[3] = False
        return res

    def getGameEnded(self, num):
        if num == 0:
            if any([self.getGameEnded(i) for i in self.ghost.keys()]):
                return -1
            elif len(self.goal) == self.find_goal:
                return 1
            else:
                return 0
        else:
            p_num = self.players[num]
            if p_num == self.players[0]:
                return 1
            else:
                return 0
            

    def stringRepresentation(self):
        return "\n".join(["".join(s) for s in self.board])

    def getCanonicalForm(self, num):
        return [sb.copy() for sb in self.start_board]

    def getInitBoard(self):
        return copy.deepcopy([sb for sb in self.board])

if __name__ == "__main__":
    pacman = Pacman(num_ghost=0)
    print(pacman.stringRepresentation())