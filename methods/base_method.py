import sys
import numpy as np

from utils.direction import Direction

sys.setrecursionlimit(1000)

class BaseMethod(object):
    
    WALL = "O"
    SPACE = " "
    GOAL = "g"

    def _distanse(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _neighbors(self, current_map, position):
        
        for key in Direction.ACTION_KEYS:
            (y, x) = Direction.ACTION[key](position)
            if current_map[y][x] not in self.WALL:
                yield (y, x)

    def _find_goal(self, current_map, st):
        min_d = 100000000000
        goal_point = None
        for y, row in enumerate(current_map):
            for x, c in enumerate(row):
                if c in self.GOAL:
                    if goal_point is None or self._distanse(st, (y, x)) < min_d:
                        min_d = self._distanse(st, (y, x))
                        goal_point = (y, x)                    
        return goal_point

    def _method(self, current_map, start_point):
        
        list_neighbors = [p for p in self._neighbors(current_map, start_point)]

        idx = np.random.randint(len(list_neighbors))
        return [list_neighbors[idx]]
    
    def _map_simplify(self, current_map, user_position):

        new_map = []

        # (uy, ux) = self._get_user_position(current_map)
        (uy, ux) = user_position

        for row in current_map:
            new_row = []
            for c in row:
                if c in self.goal_list:
                    new_row.append(self.GOAL[0])
                elif c in self.ignore_list:
                    new_row.append(self.SPACE[0])
                else:
                    new_row.append(self.WALL[0])
            new_map.append(new_row)

        for y, row in enumerate(current_map):
            new_row = []
            for x, c in enumerate(row):
                if c in self.fear_list:
                    new_map[y+1][x] = self.WALL[0]
                    new_map[y-1][x] = self.WALL[0]
                    new_map[y][x+1] = self.WALL[0]
                    new_map[y][x-1] = self.WALL[0]

        new_map[uy][ux] = self.SPACE[0]
        return new_map

    def _get_user_position(self, current_map):

        for y, row in enumerate(current_map):
            for x, c in enumerate(row):
                if c == self.user_idx:
                    return (y, x)
        return None                
    
    def __init__(self, *args, **kwargs):        
        self.user_idx = args[0]
        self.goal_list = args[1]
        self.fear_list = kwargs.get("fear_list")
        self.ignore_list = kwargs.get("ignore_list")
        self.debug = kwargs.get("debug")

    def get_way(self, current_map, start, fear_positions, goal, direct):

        current_map = self._map_simplify(current_map, start)
        
        return self._method(current_map, start)