from abc import ABC
from player_action import Player_Action, Play_Word

class Player(ABC):
    def __init__(self, name : str):
        self.name = name
    def play(self) -> Player_Action:
        pass

class Human_Player_for_Testing(Player):
    def play(self):
        print("Print the number of tiles your play will have")
        n = int(input())
        tiles = {}
        print("In each of the following lines introduce separed by space the square and the tile")
        for i in range(n):
            while True:
                try:
                    square, tile = input().split()
                    tiles[square] = tile
                    break
                except:
                    print("No pude leer esa ultima linea, repitela")
        return Play_Word(tiles)
