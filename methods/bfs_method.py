import sys

import numpy as np

from methods.base_method import BaseMethod
from utils.direction import Direction

class BfsMethod(BaseMethod):

    def _method(self, current_map, start_point):
        mem_info = {}
        way_map = np.ones((len(current_map), len(current_map[0])), dtype="int") * -1
        way_map = way_map.tolist()
        mem_info["way_map"] = sys.getsizeof(way_map) + sys.getsizeof(way_map[0]) * len(way_map)
        
        mem_info["queue"] = 0

        step_size = 0
        queue = [start_point]

        l = 0
        done = False
        goal = None

        while len(queue) != 0 and not done:
            new_queue = []
            for p in queue:            
                way_map[p[0]][p[1]] = l
                
                for (ny, nx) in self._neighbors(current_map, p):
                    if way_map[ny][nx] < 0 and (ny, nx) not in new_queue:
                        new_queue.append((ny, nx))                

                if current_map[p[0]][p[1]] in self.GOAL:
                    done = True
                    goal = (p[0], p[1])
                    break

                step_size +=1
            l += 1
            queue = new_queue
            mem_info["queue"] = max(mem_info["queue"], sys.getsizeof(queue))

        if done:
            gy, gx = goal
            l = way_map[gy][gx]
            way = []
            check = [(gy, gx)]
            for i in range(l, -1, -1):
                new_check = []
                for p in check:
                    if way_map[p[0]][p[1]] == i:
                        way.insert(0, (p[0], p[1]))
                        new_check += [Direction.ACTION[k](p) for k in Direction.ACTION_KEYS]
                        step_size +=1
                        break
                check = new_check

            mem_info["way"] = sys.getsizeof(way)
            mem_info["step_size"] = step_size
            if self.debug: 
                return (way[1:], mem_info)
            else:
                return way[1:]
        else:
            return super()._method(current_map, start_point)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    from maps.free_map import FreeMap
    from maps.maze_map import MazeMap
    from utils.print_map import print_map
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
    MAP3[-2][-2] = 'g'
    MAP3[1][1] = '0'


    bfs = BfsMethod('0', ['g'], debug=True)

    print("************ BFS ************")
    for i, MAP in enumerate([MAP1, MAP2, MAP3]):
        print("Map: {}".format(i+1))
        start_time = datetime.now()
        (WAY1, mem_info) = bfs.get_way(MAP)
        print("Time: {}".format((datetime.now() - start_time).total_seconds()))
        print("Step_size: {}".format(mem_info["step_size"]))
        print("Memory use:\n")
        for key in mem_info.keys():
            print("\t {}:{}".format(key, mem_info[key]))
        print("Length {}".format(len(WAY1)))

