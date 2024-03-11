from player import Human_Player_for_Testing
from player_handler import Player_Handler
from game import Game
player1 = Human_Player_for_Testing("Davier")
player2 = Human_Player_for_Testing("reivaD")
game = Game(Player_Handler(player1), Player_Handler(player2), True)
game.start_game()
for i in range(5):
    game.show()
    print("\n NEXT TURN:")
    game.turn()
game.show()
input()
for i in range(5):
    game.revert_last_turn()
    game.show()
    input()