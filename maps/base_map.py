import copy

class BaseMap:

    map = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', ],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ],
        ['O', ' ', 'O', 'O', ' ', 'O', 'O', ' ', 'O', ' ', 'O', 'O', ' ', 'O', 'O', ' ', 'O', ],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ],
        ['O', ' ', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', ' ', 'O', ],
        ['O', ' ', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', ' ', 'O', ],
        ['O', ' ', 'O', 'O', ' ', 'O', 'O', ' ', 'O', ' ', 'O', 'O', ' ', 'O', 'O', 'O', 'O', ],
        ['O', ' ', 'O', 'O', ' ', 'O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O', 'O', 'O', 'O', ],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ],
        ['O', 'O', 'O', 'O', ' ', 'O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O', 'O', ' ', 'O', ],
        ['O', 'O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', ' ', 'O', ],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ],
        ['O', ' ', 'O', 'O', ' ', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O', 'O', 'O', ' ', 'O', ],
        ['O', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ],
        ['O', 'O', ' ', 'O', ' ', 'O', ' ', 'O', 'O', 'O', ' ', 'O', ' ', 'O', ' ', 'O', 'O', ],
        ['O', ' ', ' ', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', ' ', ' ', 'O', ],
        ['O', ' ', 'O', 'O', 'O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O', 'O', 'O', ' ', 'O', ],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', ],
    ]

    def __init__(self, w, h):

        self.w = len(self.map[0])
        self.h = len(self.map)
    
    def get_map(self):

        return copy.deepcopy(self.map)