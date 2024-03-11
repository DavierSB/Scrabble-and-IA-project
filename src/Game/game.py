from player_handler import Player_Handler
from player_action import Challenge, Play, Change, Pass, Play_Word
from bag import Bag
from board import Board
from typing import List

class Game:
    def __init__(self, player1_handler : Player_Handler, player2_handler : Player_Handler, check_for_real_words : bool):
        self.player_handlers = [player1_handler, player2_handler]
        self.bag = Bag()
        self.board = Board()
        self.plays : List[List[Play]] = [[], []]
        self.check_for_real_words = check_for_real_words
        self.__player_in_turn_id = 0
        self.game_started = False

    @property
    def player_in_turn(self):
        return self.player_handlers[self.player_in_turn_id]
    
    @property
    def player_waiting(self):
        return self.player_handlers[self.player_waiting_id]
    
    @property
    def player_in_turn_id(self):
        return self.__player_in_turn_id

    @property
    def player_waiting_id(self):
        return self.player_in_turn_id ^ 1
    
    def start_game(self):
        """Starts the game"""
        self.player_in_turn.inform_start_of_game(1, self.player_waiting.player.name, self.check_for_real_words)
        self.player_waiting.inform_start_of_game(2, self.player_in_turn.player.name, self.check_for_real_words)
        self.draw(7)
        self.change_turn()
        self.draw(7)
        self.change_turn()
        self.game_started = True
    
    def turn(self):
        """Forwards the game one turn"""
        if not self.game_started:
            self.start_game()
            return
        action = self.player_in_turn.get_play()
        flag = False
        if isinstance(action, Challenge):
            self.challenge()
            flag = True
        while True:
            if flag:
                action = self.player_in_turn.get_play()
            flag = True
            if isinstance(action, Play_Word):
                if not(self.play(action)):
                    continue
                break
            if isinstance(action, Change):
                if not(self.change(action)):
                    continue
                break
            if isinstance(action, Pass):
                self.pass_turn()
                break
            if isinstance(action, Challenge):
                self.player_in_turn.inform_challenge_already_made()
        self.change_turn()
    
    def revert_last_turn(self):
        last_play = self.plays[self.player_waiting_id][-1]
        if last_play[0]:
            if last_play[1] is not None:
                self.board.revert_play()
            if last_play[2].split()[0] == "CHANGE":
                self.bag.revert_last_action()
            if last_play[2] != "PASS":
                self.bag.revert_last_action()
        self.player_waiting.revert_own_last_play()
        self.player_in_turn.revert_rival_last_play()
        self.plays[self.player_waiting_id].pop()
        self.change_turn()

    def challenge(self):
        result = self.board.challenge()
        if result[0]:
            self.bag.revert_last_action()
        self.plays[self.player_waiting_id][-1] = result
        self.player_in_turn.inform_challenge(result)
        self.player_waiting.inform_challenge_against(result)
    
    def play(self, play : Play_Word):
        play_tpl = self.board.add_play(play.squares, self.check_for_real_words)
        if not play_tpl[0]:
            self.player_in_turn.inform_failed_play(play_tpl[2])
            return False
        self.execute_play(play_tpl, play.n_of_tiles)
        return True
    
    def change(self, change : Change):
        if self.bag.tiles_left < change.n_of_tiles:
            self.player_in_turn.inform_failed_change(self.bag.tiles_left)
            return False
        self.execute_play((True, None, "CHANGE " + str(change.n_of_tiles)), change.n_of_tiles)
        return True
    
    def pass_turn(self):
        self.execute_play((True, None, "PASS"), 0)
    
    def execute_play(self, play : Play, n_of_tiles : int):
        self.player_in_turn.inform_own_play(play)
        self.player_waiting.inform_rival_play(play)
        self.plays[self.player_in_turn_id].append(play)
        if play[2] != "PASS":
            self.draw(min(n_of_tiles, self.bag.tiles_left))
    
    def draw(self, n : int):
        drawing = self.bag.draw(n)
        self.player_in_turn.draw(drawing)
        self.player_waiting.inform_rival_draw(len(drawing))
    
    def change_turn(self):
        self.__player_in_turn_id ^= 1
    
    def show(self):
        print("\n\nIn the bag we have:")
        self.bag.show()
        print("\n\nThe board is:")
        self.board.show()
        print("\n\nFrom the player in turn we know:")
        self.player_in_turn.show()
        print("\n\nFrom the player waiting we know:")
        self.player_waiting.show()