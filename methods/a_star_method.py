import sys

import numpy as np

from utils.priority_queue import PriorityQueue
from methods.base_method import BaseMethod

class AStarMethod(BaseMethod):

    def _method(self, current_map, start_point):

        goal_point = self._find_goal(current_map, start_point)
        mem_info = {}

        queue = PriorityQueue()
        queue.put(start_point, 0)
        cost_so_far = {start_point: 0}
        came_from = {start_point: None}
        mem_info["queue"] = 0
        mem_info["step_size"] = 0

        if goal_point is None:
            return super()._method(current_map, start_point)
                    
        while not queue.empty():
            current  = queue.get()
            if current == goal_point:
                break

            for next_p in self._neighbors(current_map, current):
                score = cost_so_far[current] + 1
                if next_p not in cost_so_far or score < cost_so_far[next_p]:
                    cost_so_far[next_p] = score
                    priority = score + self._distanse(next_p, goal_point)
                    queue.put(next_p, priority)
                    came_from[next_p] = current
                mem_info["step_size"] += 1

            mem_info["queue"] = max(mem_info["queue"], sys.getsizeof(queue.elements))

        mem_info["cost_so_far"] = sys.getsizeof(cost_so_far)
        mem_info["came_from"] = sys.getsizeof(came_from)


        way = []
        current = goal_point
        if goal_point not in came_from.keys():
            return super()._method(current_map, start_point)

        while current is not None:
            way.insert(0, current)
            current = came_from[current]

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

    mazemap = MazeMap(20, 20)
    MAP3 = mazemap.get_map()
    MAP3[10][13] = 'g'
    MAP3[1][1] = '0'

    a_star = AStarMethod('0', ['g'], debug=True)

    print("************ A* ************")
    for i, MAP in enumerate([MAP1, MAP2, MAP3]):
        print("Map: {}".format(i+1))
        start_time = datetime.now()
        (WAY1, mem_info) = a_star.get_way(MAP, (1,1))
        print("Time: {}".format((datetime.now() - start_time).total_seconds()))
        print("Step_size: {}".format(mem_info["step_size"]))        
        print("Memory use:\n")
        for key in mem_info.keys():
            print("\t {}:{}".format(key, mem_info[key]))
        print("Length {}".format(len(WAY1)))

