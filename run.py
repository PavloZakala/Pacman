from datetime import datetime

import numpy as np
import pygame

from icon_process import Icon
from pacman_game import Pacman
from player import Player

from methods.a_star_method import AStarMethod
from methods.base_method import BaseMethod
from methods.bfs_method import BfsMethod
from methods.dfs_method import DfsMethod
from methods.greedy_method import GreedyMethod
from methods.minimax_method import MiniMaxMethod

from maps.base_map import BaseMap
from maps.free_map import FreeMap
from maps.maze_map import MazeMap

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
PURPLE = (255,0,255)
YELLOW   = (255, 255, 0)


class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, color, width=16, height=16):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Point(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, x, y, color=YELLOW, width=16, height=16):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        self.black_box = pygame.surfarray.make_surface(np.zeros((width, height)))
        self.x = x
        self.y = y

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.height = height
        pygame.draw.ellipse(self.image, color,[0,0,6,6])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 
        self.rect.top = y * width + (width - 6) // 2
        self.rect.left = x * height + (height - 6) // 2

        rect = self.black_box.get_rect()
        rect.top = y * width
        rect.left = x * height
        self.vis = True
        
    def update_pos(self, y, x):
        self.x = x
        self.y = y
        self.rect.top = self.y
        self.rect.left = self.x

    def update(self, vis=False):
        print("Unvize", self.y, self.x)
        self.vis = True if vis else False
        if self.vis:
            pygame.draw.ellipse(self.image, YELLOW ,[0,0,6,6])
            self.rect = self.image.get_rect()
            self.rect.top = self.y * self.width + (self.width - 6) // 2
            self.rect.left = self.x * self.height + (self.height - 6) // 2
        else:
            self.image = self.black_box
            self.rect = self.image.get_rect()
            self.rect.top = self.y * self.width
            self.rect.left = self.x * self.height

class VisualGame(object):

    BASE_BLOCK_SIZE = 16

    def __init__(self, level_config):
        
        self.pacman_game = Pacman(height=level_config['H'], 
                                  width=level_config['W'], 
                                  num_ghost=len(level_config["players"].keys())-1, 
                                  goal_size=level_config['points_size'],
                                  inputMap=level_config["maze"])

        (W, H) = self.pacman_game.getBoardSize()

        self.screen = pygame.display.set_mode([(W)*self.BASE_BLOCK_SIZE, (H)*self.BASE_BLOCK_SIZE])
        self.center = ((W)*self.BASE_BLOCK_SIZE // 2, (H)*self.BASE_BLOCK_SIZE // 2)
        pygame.init()
        pygame.display.set_caption(self.pacman_game.name)

        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(BLACK)

        self.font24 = pygame.font.Font("freesansbold.ttf", 24)
        self.font72 = pygame.font.Font("freesansbold.ttf", 72)

        self.clock = pygame.time.Clock()
        pygame.font.init()

        self.players = []

        self.players_collide = pygame.sprite.RenderPlain()
        p = Player(game=self.pacman_game, num=0, 
                   algorithm=level_config["players"][0], 
                   reway=True, 
                   fear_list=[str(i) for i in self.pacman_game.ghost.keys()],
                   deep_level=level_config["pacman_deep"],
                   check_fear=True)

        self.players.append(p)
        self.players_collide.add(p)

        for num in self.pacman_game.ghost.keys():
            (y, x) = self.pacman_game.players[num]
            p = Player(self.pacman_game, num, 
                       algorithm=level_config["players"][num], 
                       actions_image=Icon.get_monster(num-1),
                       goal_char='0', 
                       ignore_list=list(self.pacman_game.ghost.keys()) + ['g'],
                       deep_level=level_config["gho_deep"])
            self.players.append(p)
            self.players_collide.add(p)
        
        self.goal = {}
        self.blocks_hit_list = pygame.sprite.RenderPlain()
        for y, x in self.pacman_game.goal.keys():
            g = Point(x=x, y=y)
            self.goal[(y, x)] = g
            self.blocks_hit_list.add(g)
                
        self.wall_list = self.setupRoomOne(self.pacman_game.getCanonicalForm(0))        

    def setupRoomOne(self, map):
    
        wall_list=pygame.sprite.RenderPlain()

        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == "O":
                    wall=Wall(self.BASE_BLOCK_SIZE*x, self.BASE_BLOCK_SIZE*y, BLUE)
                    wall_list.add(wall)
            
        return wall_list

    def play(self, speed=0.5):
        done = False
        end = False
        step_t = datetime.now()
        res = 0

        self.screen.fill(BLACK)
        
        self.blocks_hit_list.draw(self.screen)
        self.wall_list.draw(self.screen)
        self.players_collide.draw(self.screen)

        text= self.font24.render("Score: {}/{}".format(self.pacman_game.find_goal, len(self.goal)), True, RED)
        self.screen.blit(text, [10, 10])
        while not done:

            # Check is quit
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

            if not end:  # Is end game
                # Pacman step
                for p in self.players[1:]:
                    p.step()
                    p.image_update()

                # Check monster's result
                r = [self.pacman_game.getGameEnded(i) for i, _ in enumerate(self.players)][1:]
                # print(r)
                if sum(r) > 0:
                    print("Game over")
                    text= self.font24.render("Game over", True, RED)
                    (w, h) = text.get_size()
                    self.screen.blit(text, [self.center[0] - w//2, self.center[1] - h//2])
                    end = True
                    continue
                
                self.players[0].step()
                self.players[0].image_update()            

                pos = (self.players[0].y, self.players[0].x)
                if pos in self.pacman_game.goal.keys() and self.goal[pos].vis:
                    self.goal[pos].update()                    
                
                res = self.pacman_game.getGameEnded(0)    

                self.screen.fill(BLACK)

                # Draw all blocks
                self.blocks_hit_list.draw(self.screen)
                self.wall_list.draw(self.screen)
                self.players_collide.draw(self.screen)

                text= self.font24.render("Score: {}/{}".format(self.pacman_game.find_goal, len(self.goal)), True, RED)
                self.screen.blit(text, [10, 10])

                # WIN / Game over
                if res != 0:

                    if res > 0:
                        print("WIN")
                        ans= self.font24.render("WIN", True, GREEN)   
                    elif res < 0:
                        print("Game over")
                        ans= self.font24.render("Game over", True, GREEN)

                    (w, h) = ans.get_size()
                    self.screen.blit(ans, [self.center[0] - w//2, self.center[1] - h//2])
                    step_t = datetime.now()
                    end = True
            else:
                if (datetime.now() - step_t).total_seconds() > 10:
                    step_t = datetime.now()
                    done = True

            pygame.display.flip()
            self.clock.tick(1 / speed)

GAME_LEVELS = {
    0:{
        "W": 30, 
        "H": 30, 
        "maze": MazeMap,
        "points_size": 300,
        "pacman_deep": 10,
        "gho_deep": 1,
        "players": {
            0: MiniMaxMethod,            
        }               
    },
    1:{
        "W": 18, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 100,
        "pacman_deep": 4,
        "gho_deep": 2,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
        }               
    },
    2:{
        "W": 18, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 100,
        "pacman_deep": 6,
        "gho_deep": 2,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
            # 2: MiniMaxMethod,
        }               
    },
    3:{
        "W": 10, 
        "H": 20, 
        "maze": MazeMap,
        "points_size": 100,
        "pacman_deep": 5,
        "gho_deep": 2,
        "players": {
            0: MiniMaxMethod,
            1: MiniMaxMethod,
            2: MiniMaxMethod,
        }               
    }

}

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--level', default=1, metavar='N', type=int,
                        help='choose the level [0..4]')

    args = parser.parse_args()
    if args.level in GAME_LEVELS.keys():
        game = VisualGame(GAME_LEVELS[args.level])
        game.play(0.1)
    else:
        print("Level not found!! You can use".format(GAME_LEVELS.keys()))
