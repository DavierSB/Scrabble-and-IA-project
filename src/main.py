from Game.board import Board


# Prueba

board = Board()
print(board.add_play({"h8": "a", "h9": "b", "h10": "a"}, False))
board.show()
print(
    board.add_play({"g10": "d", "i10": "v", "j10": "i", "k10": "e", "l10": "r"}, False)
)
board.show()
print("CHALLENGING LAST WORD")
print(board.challenge())
board.show()
print(board.add_play({"h7": "c", "h11": "ll", "h12": "o"}))
board.show()
print(board.add_play({"g6": "c", "h6": "a", "i6": "s", "j6": "a"}))
board.show()
print(board.add_play({"i7": "e"}))
board.show()
print(
    board.add_play(
        {"k5": "a", "k6": "s", "k7": "e", "k8": "s", "k9": "i", "k10": "n", "k11": "a"}
    )
)
board.show()
print(
    board.add_play(
        {"j2": "a", "j3": "s", "j4": "a", "j5": "c", "j7": "d", "j8": "o", "j9": "s"}
    )
)
board.show()
