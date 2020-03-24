import cv2
import pygame
import numpy as np

class Icon(object):

    PATH = "images/icon.png"
    image_icon = np.transpose(cv2.cvtColor(cv2.imread(PATH), cv2.COLOR_BGR2RGB), (1, 0, 2))

    @staticmethod
    def get_icon(x, y):
        return pygame.surfarray.make_surface(Icon.image_icon[16*x :16*(x+1), 16*y :16*(y+1)].copy())

    @staticmethod
    def get_pacman():        

        RIGHT = [Icon.get_icon(0, 0),
                 Icon.get_icon(1, 0),
                 Icon.get_icon(2, 0),
                 Icon.get_icon(1, 0)]

        LEFT =  [Icon.get_icon(0, 1),
                 Icon.get_icon(1, 1),
                 Icon.get_icon(2, 0),
                 Icon.get_icon(1, 1)]

        UP = [Icon.get_icon(0, 2),
              Icon.get_icon(1, 2),
              Icon.get_icon(2, 0),
              Icon.get_icon(1, 2)]

        DOWN = [Icon.get_icon(0, 3),
                Icon.get_icon(1, 3),
                Icon.get_icon(2, 0),
                Icon.get_icon(1, 3)]

        return {
            'up': UP,
            'down': DOWN,
            'right': RIGHT,
            'left': LEFT,
        }


    @staticmethod
    def get_monster(i):
        i = i % 6
        DOWN = [Icon.get_icon(6, 4 + i),
                Icon.get_icon(7, 4 + i)]

        LEFT =  [Icon.get_icon(2, 4 + i),
                 Icon.get_icon(3, 4 + i)]

        RIGHT = [Icon.get_icon(0, 4 + i),
                 Icon.get_icon(1, 4 + i)]

        UP =   [Icon.get_icon(4, 4 + i),
                Icon.get_icon(5, 4 + i)]

        return {
            'up': UP,
            'down': DOWN,
            'right': RIGHT,
            'left': LEFT,
        }
        
    @staticmethod
    def get_meal():
        return {
            "image": Icon.get_icon(3, 9)            
        }

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    d = Icon.get_pacman()
    for key in d.keys():
        print(key)
        for im in d[key]:
            plt.imshow(im)
            plt.show()

