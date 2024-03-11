from random import shuffle
from typing import List
from lexicon import letter_frecuencies


class Bag:
    def __init__(self):
        self.tiles = []
        self.actions = (
            []
        )  # here we store tuples (action_type, tiles). action_types can be DRAW or INSERT
        for letter in letter_frecuencies:
            for i in range(0, letter_frecuencies[letter]):
                self.tiles.append(letter)
                self.actions.append(("INIT", letter))
        shuffle(self.tiles)

    def draw(self, n: int) -> List[str]:
        """Takes n tiles out of the bag and returns those tiles\n
        If there are not enough tiles, returns None
        """
        if self.tiles_left < n:
            return None
        drawn_tiles = []
        for i in range(n):
            drawn_tiles.append(self.tiles.pop())
        self.actions.append(("DRAW", drawn_tiles))
        return drawn_tiles

    def insert(self, new_tiles: List[str]) -> None:
        """Insert the provided tiles in the bag"""
        self.tiles = self.tiles + new_tiles
        self.actions.append(("INSERT", new_tiles))
        shuffle(self.tiles)

    def revert_last_action(self) -> None:
        """Reverts last insertion or drawing"""
        action_type, tiles = self.actions[-1]
        match action_type:
            case "INIT":
                return
            case "DRAW":
                self.insert(tiles)
            case "INSERT":
                self.draw(tiles)
        self.actions.pop()
        self.actions.pop()
        return

    @property
    def tiles_left(self) -> int:
        return len(self.tiles)

    def __str__(self):
        return str(self.tiles_left) + " tiles left:\n" + str(self.tiles)

    def __repr__(self):
        return str(self)
