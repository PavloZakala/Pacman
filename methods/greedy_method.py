import sys
import copy
import numpy as np

from utils.priority_queue import PriorityQueue
from methods.base_method import BaseMethod

class GreedyMethod(BaseMethod):

    WALL = "OX"

    def _sort_neighbors(self, current_map, p, goal):
        ns = []

        for (ny, nx) in self._neighbors(current_map, p):
            d = self._distanse((ny, nx), goal)
            ns.append((d, (ny, nx)))
        return sorted(ns, key=lambda x: x[0])


    def _method(self, current_map, start_point):
        
        goal_point = self._find_goal(current_map, start_point)

        mem_info = {}
        return_stack = []
        
        current = start_point
        num_map = copy.deepcopy(current_map)
        mem_info["num_map"] = sys.getsizeof(num_map)
        mem_info["step_size"] = 0
        mem_info["return_stack"] = 0
        came_from = {start_point: None}

        if goal_point is None:
            return super()._method(current_map, start_point)
            
        while True:

            neighbors = self._sort_neighbors(current_map, current, goal_point)
            num_map[current[0]][current[1]] = 'X'                

            if len(neighbors) == 1:
                _, next_p = neighbors[0]
            elif len(neighbors) == 0:
                _, next_p = return_stack.pop(0)
            else:
                _, next_p = neighbors[0]
                return_stack = return_stack + neighbors[1:]
            
            came_from[next_p] = current

            if next_p == goal_point:
                break
            
            current = next_p
            mem_info["step_size"] += 1
            mem_info["return_stack"] = max(mem_info["return_stack"], sys.getsizeof(return_stack))

        mem_info["came_from"] = sys.getsizeof(came_from)

        way = []
        current = goal_point
        for _ in range(300):
            if current is None:
                break
            way.insert(0, current)
            current = came_from[current]
            mem_info["step_size"] += 1

        if self.debug:
            return (way[1:], mem_info)
        else:
            return way[1:]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    from maps.free_map import FreeMap
    from maps.maze_map import MazeMap

    from datetime import datetime

    # Test params
    W = 10
    H = 10
    POINTS = [((1, 1), (H-2, W-2))]
    MAP1 = []
    
    for i in range(H):
        if i in [0, H-1]:
            MAP1.append(['O' for j in range(W)])
        else:
            MAP1.append(['O' if j in [0, W-1] else ' ' for j in range(W)])
    
    MAP1[-2][-2] = 'g'
    MAP1[1][1] = '0'

    freemap = FreeMap(width=W, height=H)
    MAP2 = freemap.get_map()
    MAP2[-2][-2] = 'g'
    MAP2[1][1] = '0'

    mazemap = MazeMap(10, 10)
    MAP3 = mazemap.get_map()
    MAP3[8][8] = 'g'
    MAP3[1][1] = '0'

    greedy = GreedyMethod('0', ['g'], debug=True)

    print("************ Greedy ************")
    for i, MAP in enumerate([MAP1, MAP2, MAP3]):
        print("Map: {}".format(i+1))
        start_time = datetime.now()
        (WAY1, mem_info) = greedy.get_way(MAP)
        print("Time: {}".format((datetime.now() - start_time).total_seconds()))
        print("Step_size: {}".format(mem_info["step_size"]))
        print("Memory use:\n")
        for key in mem_info.keys():
            print("\t {}:{}".format(key, mem_info[key]))
        print("Length {}".format(len(WAY1)))

