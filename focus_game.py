# Author: Timothy Hong
# Date: 12/2/2020
# Description: CS 162 final project with two player functionality from the abstract board game Focus.
# The game includes a Player class which holds functionality related to the player while the FocusGame
# class holds functionality related to gameplay. Players can make a single move, multiple move, or a reserved
# move. A player wins when CAPTURE_TO_WIN opponent pieces have been captured or the opponent has been
# "dominated" (can no longer make any legal moves).

# Updated 6/17/2021

from random import randint


class Player:
    """
    The Player class contains methods related to the player of the game Focus.
    """

    def __init__(self, player_name, color):
        """
        Constructor that initializes the class with the player name and player color.
        :param player_name: the name of the player
        :param color: the player's color
        """
        self._name = player_name
        self._color = color
        self._active = True         # False when a player has been eliminated
        self._reserve = 0           # num reserve pieces
        self._captured = 0          # num pieces player has captured

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    def get_reserve(self):
        return self._reserve

    def set_reserve(self, number):
        self._reserve = number

    def inc_reserve(self, number):
        self._reserve += number

    def get_captured(self):
        return self._captured

    def set_captured(self, number):
        self._captured = number

    def inc_captured(self, number):
        self._captured += number

    def get_active(self):
        return self._active

    def set_active(self, bool):
        self._active = bool

class FocusGame:
    """
    The FocusGame class contains methods related to playing the Focus game. It utilizes the Player class.
    """
    MAX_PLAYERS = 4
    MIN_PLAYERS = 2
    VALID_COLORS = ["G", "R", "B", "Y"]
    CAPTURE_TO_WIN = 6
    BOARD_SIZE = 8              # set by game rules; should not be changed
    INVALID_SPACE = "*"
    VALID_SPACE = " "

    def __init__(self, players):
        """
        :param players: a list of tuples (player_name, player_color)
        """
        # input is list check
        if not isinstance(players, list):
            print("Input should be a list of tuples (player_name, player_color)")
            raise self.InvalidInitializationError

        selected_names = []
        selected_colors = []

        # check each tuple
        for player in players:
            # elements are tuples check
            if not isinstance(player, tuple):
                print("Input should be a list of tuples (player_name, player_color)")
                raise self.InvalidInitializationError

            # valid player name check
            if isinstance(player[0], str) and player[0] not in selected_names:
                selected_names.append(player[0])
            else:
                print("Invalid player name. Ensure there are no duplicate names.")
                raise self.InvalidInitializationError

            # valid color check
            if isinstance(player[1], str) and player[1].upper() in self.VALID_COLORS and player[1].upper() not in selected_colors:
                selected_colors.append(player[1])
            else:
                print("One or more players have an invalid color. Valid colors are:", self.VALID_COLORS)
                raise self.InvalidInitializationError

        # initialize board
        self._current_turn = None
        self._players = {i: j for i, j in enumerate([Player(player[0], player[1]) for player in players])}
        self._num_players = len(self._players.keys())
        self._num_active_players = len(self._players.keys())
        self._board = None

        self.reset_board()

    def select_first_player(self):
        """
        Picks a random player to go first.
        :return: the index of the player to go first
        """
        return randint(0, self._num_players - 1)

    def reset_board(self):
        """
        Resets board to initial state based on number of players. Board is represented as a 3d list.
        """
        # get player colors
        selected_colors = []
        for key in self._players.keys():
            selected_colors.append(self._players.get(key).get_color().upper())

        # create empty BOARD_SIZE * BOARD_SIZE board
        self._board = [[[] for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        # two players
        if self._num_players == 2:
            for i in range(self.BOARD_SIZE):
                for j in range(self.BOARD_SIZE):
                    # border rows/cols are unique
                    if i == 0 or i == self.BOARD_SIZE - 1 or j == 0 or j == self.BOARD_SIZE - 1:
                        if i not in range(2, self.BOARD_SIZE - 2) or j not in range(2, self.BOARD_SIZE - 2):
                            self._board[i][j].append(self.INVALID_SPACE)
                        else:
                            self._board[i][j].append(self.VALID_SPACE)
                    # if (row + col) mod 2 is odd, fill with second color
                    elif ((i - 1) + ((j - 1) // 2)) % 2:
                        self._board[i][j].append(selected_colors[1])
                    # fill with first color
                    else:
                        self._board[i][j].append(selected_colors[0])

        # three players
        elif self._num_players == 3:
            for i in range(self.BOARD_SIZE):
                for j in range(self.BOARD_SIZE):
                    # border rows/cols are unique
                    if i == 0 or i == self.BOARD_SIZE - 1 or j == 0 or j == self.BOARD_SIZE - 1:
                        if i not in range(2, self.BOARD_SIZE - 2) or j not in range(2, self.BOARD_SIZE - 2):
                            self._board[i][j].append(self.INVALID_SPACE)
                        else:
                            self._board[i][j].append(self.VALID_SPACE)
                    # if on diagonal, fill with first color
                    elif (i - 1) % 3 == ((j - 1) // 2) % 3:
                        self._board[i][j].append(selected_colors[0])
                    # if row = col - 1 (mod 3), fill with third color
                    elif (i - 1) % 3 == (((j - 1) // 2) - 1) % 3:
                        self._board[i][j].append(selected_colors[2])
                    # fill with second color
                    else:
                        self._board[i][j].append(selected_colors[1])

        # four players
        elif self._num_players == 4:
            for i in range(self.BOARD_SIZE):
                for j in range(self.BOARD_SIZE):
                    # block off invalid spaces
                    if (i == 0 or i == self.BOARD_SIZE - 1) and (j not in range(2, self.BOARD_SIZE - 2)):
                        self._board[i][j].append(self.INVALID_SPACE)
                    elif (i == 1 or i == self.BOARD_SIZE - 2) and (j == 0 or j == self.BOARD_SIZE - 1):
                        self._board[i][j].append(self.INVALID_SPACE)
                    # fill in each quadrant starting with bottom-right
                    elif i >= self.BOARD_SIZE // 2 and j >= self.BOARD_SIZE // 2:
                        if i % 2:
                            self._board[i][j].append(selected_colors[0])
                        else:
                            self._board[i][j].append(selected_colors[1])
                    # bottom-left quadrant
                    elif i >= self.BOARD_SIZE // 2 > j:
                        if j % 2:
                            self._board[i][j].append(selected_colors[2])
                        else:
                            self._board[i][j].append(selected_colors[1])
                    # top-left quadrant
                    elif i < self.BOARD_SIZE // 2 and j < self.BOARD_SIZE //2:
                        if i % 2:
                            self._board[i][j].append(selected_colors[3])
                        else:
                            self._board[i][j].append(selected_colors[2])
                    # top-right quadrant
                    elif i < self.BOARD_SIZE // 2 <= j:
                        if j % 2:
                            self._board[i][j].append(selected_colors[3])
                        else:
                            self._board[i][j].append(selected_colors[0])

        # reset player's active status, captured, and reserve pieces
        # for three players, each player gets an extra starting reserve piece
        for key in self._players.keys():
            if self._num_players == 3:
                self._players.get(key).set_reserve(1)
            else:
                self._players.get(key).set_reserve(0)
            self._players.get(key).set_captured(0)
            self._players.get(key).set_active(True)

        # set current turn to None
        self._current_turn = None

    def next_turn(self):
        """
        Cycles turns through active players.
        """
        current_player_index = (self._current_turn + 1) % self._num_players
        while self._players.get(current_player_index).get_active() is False:
            current_player_index = (current_player_index + 1) % self._num_players
        self._current_turn = current_player_index

    def move_piece(self, player_index, from_tuple, to_tuple, num_pieces):
        """
        Method to move pieces on the board.
        :param player_index: The index/key of the player moving.
        :param from_tuple: The tuple representing the location to move from.
        :param to_tuple: The tuple representing the location to move to.
        :param num_pieces: The number of pieces to move.
        """
        if self.validate_move(player_index, from_tuple, to_tuple, num_pieces):
            # valid move; update board, check for victory, and toggle next turn
            self.update_board(player_index, from_tuple, to_tuple, num_pieces)
            # check for domination
            for i in range(self._num_players):
                if i != player_index and self.check_domination_loss(i):
                    # remove player from rotation
                    self._players.get(i).set_active(False)
                    self._num_active_players -= 1
                    print(self._players.get(i).get_name() + " has been dominated!")

            # check for victory; if it exists, set turn to None so no one can move
            if self.check_capture_victory(player_index) or self._num_active_players == 1:
                self._current_turn = None
                print(self._players.get(player_index).get_name() + " wins!")
            else:
                self.next_turn()
                print("Successfully moved!")
        else:
            print("Invalid move!")

    def validate_move(self, player_index, from_tuple, to_tuple, num_pieces):
        """
        Validates a given move.
        -Checks that the player is valid and has the current turn.
        -Checks that the from_tuple is valid.
        -Checks that the to_tuple is valid.
        -Checks that to_tuple can be reached by from_tuple in exactly num_pieces moves.
        :param player_index: the index/key of the player
        :param from_tuple: (x, y) to move from
        :param to_tuple: (x, y) to move to
        :param num_pieces: the number of pieces to move
        :return: True if valid; else False
        """
        if not (self.validate_turn(player_index) and self.validate_from_tuple(from_tuple) and
                self.validate_to_tuple(to_tuple) and self.validate_distance(from_tuple, to_tuple, num_pieces)):
            return False
        return True

    def reserved_move(self, player_index, to_tuple):
        """
        If player has reserve moves left to play, plays it at to_tuple.
        :param player_index: The index/key of the player.
        :param to_tuple: The tuple representing the location to move to.
        :return: None if valid; else "no pieces in reserve" message
        """
        if self.validate_reserved_move(player_index, to_tuple):
            # valid move; update board, check for victory, and toggle next turn
            self._board[to_tuple[0]][to_tuple[1]].append(self._players.get(player_index).get_color())
            # decrement player's reserve count
            self._players.get(player_index).inc_reserve(-1)
            # check if added piece has made the stack too large and update accordingly
            if len(self._board[to_tuple[0]][to_tuple[1]]) > 5:
                self.capture_or_reserve(player_index, self._board[to_tuple[0]][to_tuple[1]][0])
                self._board[to_tuple[0]][to_tuple[1]].pop(0)

            # check for domination
            for i in range(self._num_players):
                if i != player_index and self.check_domination_loss(i):
                    # remove player from rotation
                    self._players.get(i).set_active(False)
                    self._num_active_players -= 1
                    print(self._players.get(i).get_name() + " has been dominated!")

            # check for victory; if it exists, set turn to None so no one can move
            if self.check_capture_victory(player_index) or self._num_active_players == 1:
                self._current_turn = None
                print(self._players.get(player_index).get_name() + " wins!")
            else:
                self.next_turn()
                print("Successfully moved!")
        else:
            print("Invalid reserve move!")

    def validate_reserved_move(self, player_index, to_tuple):
        """
        Validates a given reserved move.
        -Checks that player is valid and has the current turn.
        -Checks that to_tuple is valid.
        -Checks that player has a reserve piece to play.
        :param player_index: the index/key of the player
        :param to_tuple: (x, y) to move to
        :return: True if valid; else False
        """
        if not self.validate_turn(player_index) or not self.validate_to_tuple(to_tuple) or \
                self._players.get(player_index).get_reserve() <= 0:
            return False
        return True

    def validate_turn(self, player_index):
        """
        Validates a player_index and that it matches the current turn.
        :param player_index: the index/key of the player
        :return: True if valid; else False
        """
        # check that player index is valid and matches current turn.
        if not self._players.get(player_index) or player_index != self._current_turn:
            return False
        return True

    def validate_from_tuple(self, from_tuple):
        """
        Validates a tuple (x, y) is a valid from_tuple for the current board state.
        -Checks that from_tuple is a tuple (x, y) where x and y are integers bounded by the BOARD_SIZE
        and that the top of the stack at (x, y) contains a color matching the current_turn.
        :param from_tuple: a tuple (x, y) to move from
        :return: True if valid; else False
        """
        # check that tuples are tuples
        if not isinstance(from_tuple, tuple):
            return False
        # check that tuples contain ints
        elif not isinstance(from_tuple[0], int) or not isinstance(from_tuple[1], int):
            return False
        # check that tuples are valid
        elif from_tuple[0] not in range(0, self.BOARD_SIZE) or from_tuple[1] not in range(0, self.BOARD_SIZE):
            return False
        # check that from_tuple is valid for player to move from
        elif self._board[from_tuple[0]][from_tuple[1]][-1] != self._players.get(self._current_turn).get_color().upper():
            return False
        return True

    def validate_to_tuple(self, to_tuple):
        """
        Validates a tuple (x, y) is a valid to_tuple for the current board state.
        -Checks that to_tuple is a tuple (x, y) where x and y are integers bounded by the BOARD_SIZE.
        :param to_tuple: a tuple (x, y) to move to
        :return: True if valid; else False
        """
        # check that tuples are tuples
        if not isinstance(to_tuple, tuple):
            return False
        # check that tuples contain ints
        elif not isinstance(to_tuple[0], int) or not isinstance(to_tuple[1], int):
            return False
        # check that tuples are valid
        elif to_tuple[0] not in range(0, self.BOARD_SIZE) or to_tuple[1] not in range(0, self.BOARD_SIZE):
            return False
        # check that to_tuple is not occupied by INVALID_SPACE
        elif self._board[to_tuple[0]][to_tuple[1]] == [self.INVALID_SPACE]:
            return False
        return True

    def validate_distance(self, from_tuple, to_tuple, num_pieces):
        """
        Validates num_pieces and that to_tuple can be reached horizontally or vertically from from_tuple
        in exactly num_pieces moves.
        :param from_tuple: the tuple (x, y) to move from
        :param to_tuple: the tuple (x, y) to move to
        :param num_pieces: the number of pieces to move
        :return: True if valid; else False
        """
        # check that num_pieces is valid
        if not isinstance(num_pieces, int) or num_pieces <= 0 or num_pieces > 5:
            return False
        # check that there are enough pieces to move
        elif len(self._board[from_tuple[0]][from_tuple[1]]) < num_pieces:
            return False
        # check that to_tuple is reachable in num_pieces moves
        elif not (from_tuple[0] - to_tuple[0] == 0 and abs(from_tuple[1] - to_tuple[1]) == num_pieces) and not \
                (from_tuple[1] - to_tuple[1] == 0 and abs(from_tuple[0] - to_tuple[0]) == num_pieces):
            return False
        return True

    def update_board(self, player_index, from_tuple, to_tuple, num_pieces):
        """
        Updates the game board with the validated move from from_tuple to to_tuple with num_pieces.
        :param player_index: The index/key of the player whose move it was.
        :param from_tuple: The tuple representing the location to move from.
        :param to_tuple: The tuple representing the location to move to.
        :param num_pieces: The number of pieces to move.
        :return: None
        """
        from_stack = self._board[from_tuple[0]][from_tuple[1]]
        # remove the top num_pieces off from_stack
        self._board[from_tuple[0]][from_tuple[1]] = from_stack[:-num_pieces]
        # add the top num_pieces to top of to_stack
        self._board[to_tuple[0]][to_tuple[1]] += from_stack[-num_pieces:]
        # check that to_tuple location doesn't have more than 5 pieces
        # if it does, remove bottom piece until only 5 remain
        while len(self._board[to_tuple[0]][to_tuple[1]]) > 5:
            self.capture_or_reserve(player_index, self._board[to_tuple[0]][to_tuple[1]][0])
            self._board[to_tuple[0]][to_tuple[1]].pop(0)

    def capture_or_reserve(self, player_index, piece):
        """
        Captures or reserves a given piece depending on the given player_color.
        :param player_index: The index/key of the player capturing/reserving the piece.
        :param piece: The char (e.g. "R") indicating the color of the piece to be captured or reserved.
        :return: None
        """
        # add to reserve if colors equal
        if self._players.get(player_index).get_color() == piece:
            self._players.get(player_index).inc_reserve(1)
            print(self._players.get(player_index).get_name() + " gained a reserve piece!")
        # add to captured if colors not equal
        else:
            self._players.get(player_index).inc_captured(1)
            print(self._players.get(player_index).get_name() + " captured a piece!")

    def check_capture_victory(self, player_index):
        """
        Checks the current game state for player victory where player has captured CAPTURE_TO_WIN pieces.
        :param player_index: The index/key of the player to check for victory.
        :return: True if victory exists; else False
        """
        if self._players.get(player_index).get_captured() >= self.CAPTURE_TO_WIN:
            return True
        return False

    def check_domination_loss(self, player_index):
        """
        Checks the current game state for player loss where player has been "dominated"
        such that they can no longer move and have no reserve pieces left to play.
        :param player_index: The index/key of the player to check for loss.
        :return: True if domination loss exists; else False
        """
        for row in self._board:
            for piece in row:
                # there exists at least one piece that belongs to player
                if len(piece) > 0 and piece[-1] == self._players.get(player_index).get_color():
                    return False
        return True

    def show_pieces(self, from_tuple):
        """
        Displays the pieces located at from_tuple in a list format, starting with the bottom-most piece.
        :param from_tuple: The tuple representing the location to show pieces at.
        :return: a list representation of the pieces at from_tuple
        """
        if isinstance(from_tuple, tuple) and isinstance(from_tuple[0], int) and isinstance(from_tuple[1], int) \
            and 0 <= from_tuple[0] < self.BOARD_SIZE and 0 <= from_tuple[1] < self.BOARD_SIZE:
            return self._board[from_tuple[0]][from_tuple[1]]
        return None

    def show_reserve(self, player_index):
        """
        Shows the count of reserve pieces for the player.
        :param player_index: The index/key of the player.
        :return: Number of reserve pieces the player has left.
        """
        if self._players.get(player_index):
            return self._players.get(player_index).get_reserve()
        return None

    def show_captured(self, player_index):
        """
        Shows the number of pieces captured by the player.
        :param player_index: The index/key of the player.
        :return: Number of pieces player_name has captured.
        """
        if self._players.get(player_index):
            return self._players.get(player_index).get_captured()
        return None

    def display_board(self):
        """
        Optional test method that visualizes the current board state.
        :return: None
        """
        # offset column numbers
        print('  ', end='')
        # print column numbers
        for i in range(self.BOARD_SIZE):
            print(i, end=' ' * (self.BOARD_SIZE + 3))
        print()
        # print row numbers and display pieces
        for i in range(len(self._board)):
            print(i, end=' ')
            for stack in self._board[i]:
                print(stack, end=' ' * (self.BOARD_SIZE - len(stack)))
            print()

    def set_stack(self, to_tuple, stack_list):
        """
        Test method that sets stack at a given location. Used for testing victory conditions
        of a board without playing a million moves.
        :param to_tuple: The tuple representing the location to change stack of.
        :param stack_list: The stack list to replace at the to_tuple location.
        :return: None
        """
        self._board[to_tuple[0]][to_tuple[1]] = stack_list

    def play_game(self):
        """
        Test method to play the game.
        :return: None
        """
        # select first player randomly
        self._current_turn = self.select_first_player()
        print(self._players.get(self._current_turn).get_name() + "'s piece was chosen randomly to go first!")

        while self._current_turn is not None:
            self.display_board()
            print(self._players.get(self._current_turn).get_name() + " (" + self._players.get(self._current_turn).get_color() + ")'s turn.")
            player_input = input("What would you like to do?\nOptions:\n1) Regular Move\n2) Reserved Move" +
                                 "\n3) Show Captured Pieces\n4) Show Reserved Pieces\n5) Exit\nEnter Option Number:\n> ")
            while len(player_input) != 1 or ord(player_input) > 53 or ord(player_input) < 49:
                player_input = input("Enter a valid number (1-5).\nWhat would you like to do?\nOptions:\n1) Regular Move\n2) Reserved Move" +
                                     "\n3) Show Captured Pieces\n4) Show Reserved Pieces\n5) Exit\nEnter Option Number:\n> ")
            if int(player_input) == 1:
                # get from_tuple
                from_tuple = input("Where would you like to move from? Enter 'row, column' or enter 'q' to go back.\n> ")
                if from_tuple.lower() == "q":
                    continue
                from_tuple = self.string_to_2_tuple(from_tuple)
                while not (from_tuple and self.validate_from_tuple(from_tuple)):
                    from_tuple = input("Invalid location.\nWhere would you like to move from? Enter 'row, column' or enter 'q' to go back.\n> ")
                    if from_tuple.lower() == "q":
                        break
                    from_tuple = self.string_to_2_tuple(from_tuple)
                if from_tuple == "q":
                    continue
                # get to_tuple
                to_tuple = input("Where would you like to move to? Enter 'row, column' or enter 'q' to go back.\n> ")
                if to_tuple.lower() == "q":
                    continue
                to_tuple = self.string_to_2_tuple(to_tuple)
                while not (to_tuple and self.validate_to_tuple(to_tuple)):
                    to_tuple = input("Invalid location.\nWhere would you like to move to? Enter 'row, column' or enter 'q' to go back.\n> ")
                    if to_tuple.lower() == "q":
                        break
                    to_tuple = self.string_to_2_tuple(to_tuple)
                if to_tuple == "q":
                    continue
                # get num_pieces
                num_pieces = input("How many pieces would you like to move? Enter a number or enter 'q' to go back.\n> ")
                if num_pieces.lower() == "q":
                    continue
                num_pieces = self.string_to_int(num_pieces)
                while not (num_pieces and self.validate_move(self._current_turn, from_tuple, to_tuple, num_pieces)):
                    num_pieces = input("Invalid move.\nHow many pieces would you like to move? Enter a number or enter 'q' to go back.\n> ")
                    if num_pieces.lower() == "q":
                        break
                    num_pieces = self.string_to_int(num_pieces)
                if num_pieces == "q":
                    continue
                # move piece
                self.move_piece(self._current_turn, from_tuple, to_tuple, num_pieces)
            elif int(player_input) == 2:
                # get to_tuple
                to_tuple = input("Where would you like to move to? Enter 'row, column' or enter 'q' to go back.\n> ")
                if to_tuple.lower() == "q":
                    continue
                to_tuple = self.string_to_2_tuple(to_tuple)
                while not (to_tuple and self.validate_to_tuple(to_tuple) and self.validate_reserved_move(self._current_turn, to_tuple)):
                    to_tuple = input("Invalid location.\nWhere would you like to move to? Enter 'row, column' or enter 'q' to go back.\n> ")
                    if to_tuple.lower() == "q":
                        break
                    to_tuple = self.string_to_2_tuple(to_tuple)
                if to_tuple == "q":
                    continue
                # move piece
                self.reserved_move(self._current_turn, to_tuple)
            elif int(player_input) == 3:
                print(self._players.get(self._current_turn).get_name() + " has captured " + str(self.show_captured(self._current_turn)) + " pieces.")
            elif int(player_input) == 4:
                print(self._players.get(self._current_turn).get_name() + " has " + str(self.show_reserve(self._current_turn)) + " reserved pieces.")
            elif int(player_input) == 5:
                print("Thanks for playing! Goodbye.")
                break

    def string_to_2_tuple(self, string):
        """
        Helper function that takes a comma separated string and converts it to a 2-tuple with integers.
        :param string: comma separated string
        :return: an integer 2-tuple or None if string is invalid
        """
        split_string = string.split(",")
        if len(split_string) != 2:
            return
        # strip white space
        split_string = [e.strip() for e in split_string]
        try:
            x_val = int(split_string[0])
        except (TypeError, ValueError):
            return
        try:
            y_val = int(split_string[1])
        except (TypeError, ValueError):
            return
        return x_val, y_val

    def string_to_int(self, string):
        """
        Helper function that takes a string and tries to convert it to int.
        :param string: string representation of an integer
        :return: integer representation of string; else None
        """
        try:
            res = int(string)
        except (TypeError, ValueError):
            return
        return res

    class InvalidMoveError(Exception):
        """
        Raised when an invalid move is attempted.
        """
        pass

    class InvalidInitializationError(Exception):
        """
        Raised when the game is initialized with invalid input.
        """
        pass


def main():
    """
    Test code
    :return:
    """
    game = FocusGame([("Tim", "R"), ("Kyle", "G"), ("Benny", "Y"), ("Kenny", "B")])
    game.set_stack((3, 3), ["R", "R", "G", "R"])
    game.set_stack((4, 4), ["G", "G", "Y", "R"])
    game.play_game()


if __name__ == "__main__":
    main()
