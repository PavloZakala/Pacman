class Direction:
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    STOP = 'STOP'

    REVERSE =  {UP: DOWN,
                DOWN: UP,
                LEFT:  RIGHT,
                RIGHT:  LEFT,
                STOP:  STOP}

    # LEFT =       {UP: LEFT,
    #               LEFT: DOWN,
    #               DOWN:  RIGHT,
    #               RIGHT:  UP,
    #               STOP:  STOP}

    # RIGHT = dict([(y,x) for x, y in LEFT.items()])

    ACTION = {
        "DOWN": lambda p: (p[0]+1, p[1]),
        "RIGHT": lambda p: (p[0], p[1]+1),
        "UP": lambda p: (p[0]-1, p[1]),
        "LEFT": lambda p: (p[0], p[1]-1),
    }
        
    ACTION_KEYS = [k for k in ACTION.keys()]

    ACTION_DIR_KEYS = {
        "right": [RIGHT, DOWN, LEFT, UP],
        "down": [DOWN, RIGHT, UP, LEFT],        
        "left": [LEFT, UP, RIGHT, DOWN],
        "up": [UP, LEFT, DOWN, RIGHT]
    }

    FULLACTION = {
        "DOWN": lambda p: (p[0]+1, p[1]),
        "RIGHT": lambda p: (p[0], p[1]+1),
        "UP": lambda p: (p[0]-1, p[1]),
        "LEFT": lambda p: (p[0], p[1]-1),
        "STOP": lambda p: p,
    }

    FULLACTION_KEYS = [k for k in FULLACTION.keys()]