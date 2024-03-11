from player import Player
from player_action import Player_Action, Challenge, Change, Play_Word
from typing import List, Tuple
class Player_Handler:
    def __init__(self, player : Player) -> None:
        self.player = player
        self.points = 0
        self.hand = []
        self.history_of_hands = []
        self.plays = [[], []]
        self.order_to_play : int
        self.check_for_real_words : bool
    
    def get_play(self) -> Player_Action:
        while True:
            action = self.player.play()
            if isinstance(action, Change) or isinstance(action, Play_Word):
                if not(self.take_tiles_from_hand(action)):
                    self.inform_tiles_not_in_hand
                    continue
            if isinstance(action, Challenge):
                if not self.check_for_real_words:
                    self.inform_no_challenges_allowed()
                    continue
            return action
    
    def revert_own_last_play(self):
        last_play = self.plays[self.order_to_play][-1]
        if last_play[0]:
            if last_play[1] is not None:
                self.points -= last_play[1]
            if last_play[2] != "PASS":
                self.history_of_hands.pop()
                self.hand = self.history_of_hands[-1].copy()
        self.plays[self.order_to_play].pop()
    
    def revert_rival_last_play(self):
        self.plays[self.order_to_play ^ 1].pop()

    def draw(self, tiles : List[str]):
        self.hand.extend(tiles)
        self.history_of_hands.append(self.hand.copy())
    
    def take_tiles_from_hand(self, action : Play_Word | Change):
        new_hand = self.hand.copy()
        for tile in action.tiles:
            if tile in new_hand:
                new_hand.remove(tile)
            else:
                return False
        self.hand = new_hand
        return True

    def inform_start_of_game(self, order_to_play : int, other_player_name : str, check_for_real_words : bool):
        self.order_to_play = order_to_play - 1
        self.check_for_real_words = check_for_real_words
    
    def inform_own_play(self, play : Tuple[bool, int, str]):
        self.plays[self.order_to_play].append(play)
        if play[0] and (play[1] is not None):
            self.points += play[1]

    def inform_rival_play(self, play : Tuple[bool, int, str]):
        self.plays[self.order_to_play ^ 1].append(play)
    
    def inform_failed_play(self, msg : str):
        self.hand = self.history_of_hands[0]

    def inform_challenge(self, result : Tuple[bool, int, str]):
        self.plays[self.order_to_play ^ 1][-1] = result

    def inform_challenge_against(self, result : Tuple[bool, int, str]):
        if result[0]:
            self.points -= self.plays[-1][1]
            self.plays[self.order_to_play][-1] = result
            self.history_of_hands.pop()
            self.hand = self.history_of_hands[-1].copy()
            self.history_of_efective_actions.pop()

    def inform_challenge_already_made(self):
        pass

    def inform_no_challenges_allowed(self):
        pass
    
    def inform_failed_change(self, tiles_left_in_bag : int) -> None:
        pass

    def inform_tiles_not_in_hand(self) -> None:
        pass

    def inform_rival_draw(self, tiles_drawn : int) -> None:
        pass

    def show(self) -> None:
        print("Jugador " + self.player.name)
        print("Points " + str(self.points))
        print("Hand: " + str(self.hand))
        print(self.history_of_hands)