import sys
import copy
import numpy as np

from methods.base_method import BaseMethod


class DfsMethod(BaseMethod):

    WALL = "OX"

    def __back_track(self, current_map, way, p, l, best_way, mem_info):
        l += 1
        (y, x) = p
        (best_len, max_way) = best_way
        mem_info["way"] = max(mem_info["way"], sys.getsizeof(way))
        mem_info["best_way"] = max(mem_info["best_way"], sys.getsizeof(max_way))

        if l > best_len and best_len >= 0:
            return best_len, max_way
            
        if current_map[y][x] in self.GOAL:
            if l < best_len or best_len < 0:       
                mem_info["step_size"] += 1         
                return l, way + [p]
            else:
                return best_len, max_way
        else:
            current_map[y][x] = 'X'

            for (ny, nx) in self._neighbors(current_map, p):                            
                best_len, max_way = self.__back_track(current_map, way+[p], (ny, nx), l, (best_len, max_way), mem_info)

            current_map[y][x] = self.SPACE[0]
            mem_info["step_size"] += 4
            return best_len, max_way

    def _method(self, current_map, start_point):        

        copy_current_map = copy.deepcopy(current_map)
        mem_info = {}
        mem_info["copy_map"] = sys.getsizeof(copy_current_map) + sys.getsizeof(copy_current_map[0]) * len(copy_current_map)
        mem_info["way"] = 0
        mem_info["best_way"] = 0
        mem_info["step_size"] = 0

        (best_len, best_way) = self.__back_track(copy_current_map, [], start_point, 0, (-1, []), mem_info)

        mem_info["stack_values"] = best_len * sys.getsizeof(1.0)
        if best_len >= 0:
            
            if self.debug: 
                return (best_way[1:], mem_info)
            else:
                return best_way[1:]
        else:
            return super()._method(current_map, start_point)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



if __name__ == "__main__":
    from maps.free_map import FreeMap
    from maps.maze_map import MazeMap

    from datetime import datetime

    # Test params
    W = 8
    H = 8
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

    dfs = DfsMethod('0', ['g'], debug=True)

    print("************ DFS ************")
    for i, MAP in enumerate([MAP1, MAP2, MAP3]):
        print("Map: {}".format(i+1))
        start_time = datetime.now()
        (WAY1, mem_info) = dfs.get_way(MAP, (1, 1))
        print("Time: {}".format((datetime.now() - start_time).total_seconds()))
        print("Step_size: {}".format(mem_info["step_size"]))
        print("Memory use:\n")
        for key in mem_info.keys():
            print("\t {}:{}".format(key, mem_info[key]))
        print("Length {}".format(len(WAY1)))
