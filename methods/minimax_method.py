import sys

import numpy as np

from methods.base_method import BaseMethod
from utils.direction import Direction
import random 

class MiniMaxMethod(BaseMethod):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deep_level = kwargs.get("deep_level")
        self.check_fear = kwargs.get("check_fear")
        self.WALL += "".join(self.fear_list)

    def _do_action(self, current_map, potision, next_potision, set_char):
        (x, y) = potision
        (nx, ny) = next_potision
        user_idx = current_map[x][y]
        current_map[x][y] = set_char
        current_map[nx][ny] = user_idx

    def _find_user(self, current_map, user_id):
        for y, row in enumerate(current_map):
            x = row.find(user_id)
            if x >= 0:
                return (y, x)

    def _neighbors_dir(self, current_map, position, direct):
        
        for key in Direction.ACTION_DIR_KEYS[direct]:
            (y, x) = Direction.ACTION[key](position)
            if current_map[y][x] not in self.WALL:
                yield (y, x)

    def _get_direction(self, current_point, next_point):
        cy, cx = current_point
        ny, nx = next_point

        dy = cy - ny
        dx = cx - nx

        if dx < 0:
            return "right"
        elif dx > 0:
            return "left"
        elif dy < 0:
            return "down"
        elif dy > 0:
            return "up"

    def _check_fear(self, current_map, p):
        for act in Direction.ACTION_KEYS:
            (y, x) = Direction.ACTION[act](p)
            if current_map[y][x] in self.fear_list:
                return -100.0
        return 0

    def _minimax(self, 
                 current_map, 
                 agent_position, 
                 deep_id, 
                 eval, 
                 direct,
                 goal,
                 max_deep_level):
                 
        current = agent_position[deep_id % len(agent_position)]

        if deep_id >= max_deep_level:
            return eval, agent_position[deep_id % len(agent_position)]

        scores = []
        actions = list(self._neighbors_dir(current_map, current, direct))        
        if len(actions) == 0:
            return -1, agent_position[deep_id % len(agent_position)]

        for next_p in actions:
            ev = 0
            if deep_id % len(agent_position) == 0 and \
                self.check_fear:
                    ev = self._check_fear(current_map, next_p)
            next_char = current_map[next_p[0]][next_p[1]]

            if next_p in goal:
                ev += 1#(max_deep_level - deep_id + 1) / 3.0

            self._do_action(current_map, current, next_p, ' ') #agent_char[deep_id % len(agent_position)])
            agent_position[deep_id % len(agent_position)] = next_p            
            scores.append(self._minimax(current_map, 
                                        agent_position, 
                                        deep_id+1, 
                                        eval+ev,
                                        self._get_direction(current, next_p),
                                        goal,
                                        max_deep_level)[0])
                                                
            agent_position[deep_id % len(agent_position)] = current
            
            self._do_action(current_map, next_p, current, next_char)

        if deep_id % len(agent_position) == 0:
            best_score = max(scores)
        else:
            best_score = min(scores)
        
        idxs = [i for i in range(len(scores)) if scores[i] == best_score]

        if deep_id == 0:
            if len(idxs) > 2:
                return best_score, actions[random.choice(idxs)]
            else:
                return best_score, actions[idxs[0]]
        else:
            return best_score, actions[idxs[0]]

    def get_way(self, current_map, start, fear_positions, goal, direct):
        
        agent_position = [start] + fear_positions        

        next_position = self._minimax(current_map, 
                                      agent_position, 
                                      0, 
                                      0, 
                                      direct,
                                      goal,
                                      self.deep_level * len(agent_position))[1]
        # self.WALL = self.WALL[:-1]
        return [next_position]




