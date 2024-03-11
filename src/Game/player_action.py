from abc import ABC
from typing import List, Dict
class Player_Action(ABC):
    pass

class Challenge(Player_Action):
    pass

class Play(Player_Action):
    pass

class Pass(Player_Action):
    pass

class Change(Player_Action):
    def __init__(self, tiles : List[str]):
        self.tiles = tiles
    
    @property
    def n_of_tiles(self):
        return len(self.tiles)

class Play_Word(Player_Action):
    def __init__(self, squares : Dict[str, str]):
        self.squares = squares
    
    @property
    def tiles(self):
        return list(self.squares.values())
    
    @property
    def n_of_tiles(self):
        return len(self.squares)