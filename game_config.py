from methods.a_star_method import AStarMethod
from methods.base_method import BaseMethod
from methods.bfs_method import BfsMethod
from methods.dfs_method import DfsMethod
from methods.greedy_method import GreedyMethod
from methods.minimax_method import MiniMaxMethod

from maps.base_map import BaseMap
from maps.free_map import FreeMap
from maps.maze_map import MazeMap

GAME_LEVELS = {
    'bfs':{
        "W": 25, 
        "H": 25, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: BfsMethod,
        },   
    },   
    'dfs':{
        "W": 13, 
        "H": 13, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: BfsMethod,
        },
    },
    'A_star':{
        "W": 25, 
        "H": 25, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: BfsMethod,
        },
    },
    'greedy':{
        "W": 15, 
        "H": 15, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: BfsMethod,
        },
    },
    '0':{
        "W": 25, 
        "H": 25, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: MiniMaxMethod,
        }               
    },
    '1':{
        "W": 20, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 200,
        "pacman_deep": 6,
        "gho_deep": 1,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
        }               
    },
    '2':{
        "W": 20, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 200,
        "pacman_deep": 6,
        "gho_deep": 3,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
        }                 
    },
    '3':{
        "W": 20, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 200,
        "pacman_deep": 4,
        "gho_deep": 1,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,            
            2: MiniMaxMethod,
        }                 
    },
    '4':{
        "W": 22, 
        "H": 22, 
        "maze": MazeMap,
        "points_size": 200,
        "pacman_deep": 4,
        "gho_deep": 3,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,            
            2: MiniMaxMethod,
        }                 
    },    
    '5':{
        "W": 25, 
        "H": 25, 
        "maze": MazeMap,
        "points_size": 200,
        "pacman_deep": 3,
        "gho_deep": 1,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
            2: MiniMaxMethod,
            3: MiniMaxMethod,
        }                 
    }
}