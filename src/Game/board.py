import string
from .lexicon import lexicon, letter_punctuations, square_multiplicator
from typing import List, Tuple, Dict


class Board:
    def __init__(self):
        self.squares = (
            {}
        )  # A dictionary where the keys are the name of the squares and the values are the tile located in the square, for example ("a1", "s")
        self.border_squares = set(
            ["h8"]
        )  # A set with the names of the squares that has no tile, but are adjacent to squares with tiles placed
        for row in range(1, 16):
            for column in string.ascii_lowercase[:15]:
                self.squares[column + str(row)] = None
        self.plays = []
        self.border_squares_history = (
            []
        )  # stores border_squares at each moment for comodity and speed

    def add_play(
        self, play: Dict[str, str], check_for_real_words=True
    ) -> Tuple[
        bool, int, str
    ]:  # devuelve la validacion, los puntos, y un string que nombra la jugada
        """Adds a play to the board if the play is valid.\n
        Returns a tuple, where the first element states if is a valid play, the second one the punctuation and the third one an string describing the play\n
        parameters:
        play : describes the play as a dictionary, where the keys are positions and the values are the tile placed at each position. For example ("b2", "t")
        check_for_real_words : by default True. When True, only accepts a play if all the formed words are valid
        """
        valid, msg = self.__check_for_placing_errors(play)
        if not valid:
            return (False, None, msg)
        direction = msg
        words = self.__get_all_new_words(play, direction, check_for_real_words)
        valid, points, msg = Board.__elaborate_answer(words)
        if valid:
            self.__update(play)
        return (valid, points, msg)

    def revert_play(self) -> None:
        """Reverts last recorded play"""
        for square in self.plays[-1]:
            self.squares[square] = None
        self.plays.pop()
        self.border_squares_history.pop()
        self.border_squares = set(self.border_squares_history[-1])

    def challenge(self) -> Tuple[bool, int, str]:
        """Challenges last play. Returns a tuple describing the play, if last play was valid, or describing the error if it wasnt
        The tuple describing the play or error is the same as in add_play
        """
        play = self.plays[-1]
        self.revert_play()
        return self.add_play(play)

    # Private methods

    @property
    def has_started(self) -> bool:
        return self.squares["h8"] is not None

    def __check_for_placing_errors(self, play: Dict[str, str]) -> Tuple[bool, str]:
        """Given a play described as in add_play, checks for placing errors\n
        Returns a tuple which first element is a boolean, that is False when there is a colocation error\n
        The second element of the tuple is a string, that if the word is valid contains the direction of the word, and otherwise contains the error messsage
        """
        if not (self.has_started) and not ("h8" in play):
            return False, "The first play should touch the center square"
        direction = Board.__find_direction_of_play(play)
        if not direction:
            return False, "Bad colocation of tiles"
        if not self.__check_connection(play, direction):
            return False, "Play must be connected"
        return True, direction

    def __find_direction_of_play(play: Dict[str, str]) -> str:
        """Given a play described as in add_play, determines whether the play is placed vertically, horizontally or has no direction"""
        if len(play) == 1:
            return "horizontal"
        last_position = None
        direction = None
        for position in play:
            if last_position == None:
                last_position = position
                continue
            vertical = last_position[0] == position[0]
            last_position = position
            if direction is None:
                direction = "vertical" if vertical else "horizontal"
                continue
            if vertical:
                if direction == "horizontal":
                    return None
                continue
            if direction == "vertical":
                return None
        return direction

    def __check_connection(self, play: Dict[str, str], direction: str) -> bool:
        """Given a play described as in add_play, checks if the play is connected with the tiles in the board"""
        squares_used = Board.__sort_squares_used(list(play.keys()), direction)
        move, _ = Board.__movements(direction)
        for i in range(len(squares_used) - 1):
            square = move(squares_used[i])
            expected_square = squares_used[i + 1]
            while square != expected_square:
                if (square is None) or (self.squares[square] is None):
                    # We have reached the end of the board or an empty unused square without visiting all used squares
                    return False
                square = move(square)
        return any(
            (sqr in self.border_squares) for sqr in squares_used
        )  # Finally, if a border square is used, the word is connected

    def __get_all_new_words(
        self, play: Dict[str, str], direction: str, check_for_real_words: str
    ) -> List[Tuple[str, str, int]]:
        """Given a play as described in add_play, returns a list with all the words formed by the play\n
        The words are described as tuples (start_square, word, points).\n
        If check_for_real_words is True, each word will be valid only if is a real word\n
        Each invalid word points will be None
        """
        words = (
            []
        )  # List of tuples. Each tuple describes one of the new words formed: (start_position, word, points). For example ("f3", "casa", "6")
        words.append(self.__get_word(play, direction, check_for_real_words))
        direction = "vertical" if direction == "horizontal" else "horizontal"
        move, move_back = Board.__movements(direction)
        for square in play:
            if (self.squares[move(square)] is not None) or (
                self.squares[move_back(square)] is not None
            ):
                words.append(
                    self.__get_word(
                        {square: play[square]}, direction, check_for_real_words
                    )
                )
        return words

    def __get_word(
        self, play: Dict[str, str], direction: str, check_for_real_words: str
    ) -> Tuple[str, str, int]:
        """Given a play as described in add_play, returns the word in the given direction\n
        The word is described as in __get_all_new_words.\n
        """
        squares_used = Board.__sort_squares_used(list(play.keys()), direction)
        move, move_back = Board.__movements(direction)
        start_square = squares_used[0]
        back_square = move_back(start_square)
        while (back_square is not None) and (self.squares[back_square] is not None):
            start_square = back_square
            back_square = move_back(start_square)
        word = ""
        points = 0
        word_multiplicator = 1
        square = start_square
        tile = play.get(square, self.squares[square])
        while (square is not None) and (tile is not None):
            word = word + tile
            sqr_word_multiplicator, sqr_tile_multiplicator = (
                (square_multiplicator(square)) if square in play else (1, 1)
            )
            points += letter_punctuations(tile) * sqr_tile_multiplicator
            word_multiplicator *= sqr_word_multiplicator
            square = move(square)
            tile = play.get(square, self.squares[square])
        points *= word_multiplicator
        if check_for_real_words and not (lexicon.validate(word)):
            points = None
        if (
            len(play) == 7
        ):  # En este caso el jugador coloco toda su mano, y estamos en presencia de un scrabble
            points = points + 50
        return (start_square, word, points)

    def __update(self, play: Dict[str, str]) -> None:
        """Given a play described as in add_play, puts the play in the board and updates the border squares, and the history of plays and border_squares"""
        for square in play:
            self.squares[square] = play[square]
        for square in play:
            if square in self.border_squares:
                self.border_squares.remove(square)
            neighbors = [
                Board.up_a_square(square),
                Board.down_a_square(square),
                Board.left_a_square(square),
                Board.right_a_square(square),
            ]
            for neighbor in neighbors:
                if self.squares[neighbor] is None:
                    self.border_squares.add(neighbor)
        self.plays.append(play)
        self.border_squares_history.append(list(self.border_squares))

    @staticmethod
    def __elaborate_answer(words: List[Tuple[str, str, int]]) -> Tuple[bool, int, str]:
        """Given a list of the words formed by a play, Returns a tuple, where the first element states if is a valid play, the second one the punctuation and the third one a message\n
        Such message will be listing the wrong words if the play is not valid, and otherwise will be a description of the play
        """
        points = 0
        wrong_words = []
        msg = ""
        for word in words:
            if word[2] is None:
                wrong_words.append(word[1])
            else:
                points += word[2]
                msg += word[0] + " " + word[1] + " " + str(word[2]) + ", "
        if len(wrong_words) > 0:
            msg = "Invalid words: " + ", ".join(wrong_words)
            return (False, None, msg)
        return (True, points, msg[:-2])

    @staticmethod
    def __sort_squares_used(squares: List[str], direction: str) -> List[str]:
        """Sorts the squares acording a direction"""
        sorting_criteria = (
            (lambda sqr: sqr[0])
            if (direction == "horizontal")
            else (lambda sqr: int(sqr[1:]))
        )
        squares.sort(key=sorting_criteria)
        return squares

    @staticmethod
    def __movements(direction: str):
        """Returns a tuple with the functions for moving front and back in the given direction"""
        if direction == "horizontal":
            return Board.right_a_square, Board.left_a_square
        return Board.down_a_square, Board.up_a_square

    @staticmethod
    def right_a_square(position: str) -> str:
        """Given a square name, returns the name of the square at its right, or None if there isn't"""
        column = position[0]
        if column == "o":
            return None
        return chr(ord(column) + 1) + position[1:]

    @staticmethod
    def left_a_square(position: str) -> str:
        """Given a square name, returns the name of the square at its left, or None if there isn't"""
        column = position[0]
        if column == "a":
            return None
        return chr(ord(column) - 1) + position[1:]

    @staticmethod
    def down_a_square(position: str) -> str:
        """Given a square name, returns the name of the square below, or None if there isn't"""
        row = position[1:]
        if row == "15":
            return None
        return position[0] + str(int(row) + 1)

    @staticmethod
    def up_a_square(position: str) -> str:
        """Given a square name, returns the name of the square above, or None if there isn't"""
        row = position[1:]
        if row == "1":
            return None
        return position[0] + str(int(row) - 1)

    def show(self):
        for row in range(1, 16):
            line = ""
            for column in range(1, 16):
                square = chr(ord("a") + column - 1) + str(row)
                tile = self.squares[square]
                if tile is None:
                    word_multiplicator, letter_multiplicator = square_multiplicator(
                        square
                    )
                    if word_multiplicator > 1:
                        tile = str(word_multiplicator) + "Xw"
                    if letter_multiplicator > 1:
                        tile = str(letter_multiplicator) + "Xl"
                    if tile is None:
                        tile = ""
                line = line + " " + tile
                for i in range(0, 4 - len(tile)):
                    line = line + " "
                line = line + "|"
            print(line)
