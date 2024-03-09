from board import Board

board = Board()
print(board.add_play({'h8' : 'a', 'h9' : 'b', 'h10' : 'a'}))
print(board.add_play({'g10' : 'd', 'i10' : 'v', 'j10' : 'i', 'k10' : 'e', 'l10' : 'r'}))
print(board.add_play({'h7' : 'c', 'h11' : 'll', 'h12' : 'o'}))
print(board.add_play({'g6' : 'c', 'h6' : 'a', 'i6' : 's', 'j6' : 'a'}))
print(board.add_play({'i7' : 'e'}))