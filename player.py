import pygame
import cv2
import numpy as np
from icon_process import Icon

class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
    
    BASE_BLOCK_SIZE = 16

    def __init__(self, 
                 game, 
                 num, 
                 algorithm=None, 
                 goal_char='g', 
                 ignore_list = ['0'],
                 fear_list = [],
                 actions_image=Icon.get_pacman(), 
                 reway=False, 
                 deep_level=1,
                 check_fear=False):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.num = num
        self.reway = reway
        self.algorithm = algorithm(str(self.num), 
                                    [goal_char],
                                    fear_list=fear_list,
                                    ignore_list=ignore_list, 
                                    deep_level=deep_level,
                                    check_fear=check_fear)

        (self.y, self.x) = game.players[num]        

        self.actions_image = actions_image   
        
        self.map = None

        self.order = "right"
        self.anim_idx = 0

        self.image = self.actions_image[self.order][self.anim_idx]

        self.rect = self.image.get_rect()
        self.rect.top = self.BASE_BLOCK_SIZE * self.y
        self.rect.left = self.BASE_BLOCK_SIZE * self.x
        self.way = []
    
    
    def image_update(self):
        self.anim_idx += 1
        l = len(self.actions_image[self.order])
        self.image = self.actions_image[self.order][self.anim_idx % l]

        self.rect = self.image.get_rect()
        self.rect.top = self.BASE_BLOCK_SIZE * self.y
        self.rect.left = self.BASE_BLOCK_SIZE * self.x
        

    def step(self):
        if self.reway or len(self.way) == 0:            
            if self.num == 0:
                goal = [k for k in self.game.goal.keys() if self.game.goal[k]]
                fear_list = [self.game.ghost[i] for i in self.game.ghost.keys()]

                self.way = self.algorithm.get_way(
                    self.game.getInitBoard(), 
                    (self.y, self.x),
                    fear_list,
                    goal, 
                    self.order)
            else:
                goal = [self.game.players[0]]
                fear_list = [self.game.players[0]]

                self.way = self.algorithm.get_way(
                    self.game.getInitBoard(), 
                    (self.y, self.x),
                    fear_list,
                    goal,
                    self.order)

                
        p = self.way.pop(0)
        print(p)
        dy = self.y - p[0] 
        dx = self.x - p[1]
        self.y = p[0] 
        self.x = p[1] 

        if dx < 0:
            self.game.getNextState(self.num, 1)
            self.order = "right"
        elif dx > 0:
            self.game.getNextState(self.num, 3)
            self.order = "left"
        elif dy < 0:
            self.game.getNextState(self.num, 0)
            self.order = "down"
        elif dy > 0:
            self.game.getNextState(self.num, 2)
            self.order = "up"

        