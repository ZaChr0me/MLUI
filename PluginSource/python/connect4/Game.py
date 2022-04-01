import numpy as np
import functools
import copy

GRID_SHAPE = (6, 7)

PLAYER_1 = 1
NONE = 0
PLAYER_2 = -1
RENDER_PLAYERS = {PLAYER_1: 'X', NONE: '-', PLAYER_2: 'O'}

NB_TOKENS_VICTORY = 4

# 0 and 1 are the only possible values, due to the way the neural network is working (it predicts a sigmoid)
VALUE_DEFAULT_ACTION = 0
VALUE_VICTORY = 1

from scipy.signal import convolve2d

# List of victory configurations as kenels
VICTORY_KERNELS = [np.array([[1, 0, 0, 0],  # falling diagonal
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]) / 4,
                   np.array([[0, 0, 0, 1],  # rising diagonal
                             [0, 0, 1, 0],
                             [0, 1, 0, 0],
                             [1, 0, 0, 0]]) / 4,
                   np.array([[1, 1, 1, 1]]) / 4,  # line
                   np.array([[1], [1], [1], [1]]) / 4]  # column


# Check if the player won the game using a list of win configurations (kernels)
def check_victory(board, current_player=1, kernels=VICTORY_KERNELS):
    for kernel in kernels:
        conv = convolve2d(board, kernel)
        if any(current_player in line for line in conv):
            return True
    return False


def generate_next_board(board, current_player, action):
    next_board = copy.deepcopy(board)
    for i in range(0, len(next_board)):
        if next_board[i][action] == 0:
            next_board[i][action] = current_player
            break
    return next_board


class GameState():

    def __init__(self, currentPlayer, grid_shape=GRID_SHAPE, board=None):

        self.currentPlayer = currentPlayer
        if board is not None:
            self.board = board
        else:
            self.board = np.full(grid_shape, NONE, dtype=np.int8)
        self.id = self._generate_id()

    def generate_symetric_state(self):

        """Trick: in order to improve the learning speed of the neural network, we store in memory the state
        # of the game AND its symetric."""

        # YOUR CODE HERE: generate a new instance of GameState, with the same current player and the symetric of the board,
        # along the 3rd column.
        # For example, if the board of the game state is:
        # [0, 0, 1, 0, 0, 0, -1]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # Then its symetric is:
        # [-1, 0, 0, 0, 1, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        # [0, 0, 0, 0, 0, 0, 0]
        symetric_game_state = GameState(self.currentPlayer, board=np.flip(self.board, 1))
        return symetric_game_state

    def get_board_for_neural_network(self):
        """ If it is PLAYER_2 turn, we inverse the point of view.
        That way, the neural network is always player 1 and its opponent is always player -1
        => The neural network can play against itself, instead of needing another neural network as opponent."""
        result = self.board * self.currentPlayer

        return result

    def allowedActions(self):
        """Returns one boolean per possible action.
        Example: [True, True, False, True, True, True, True] if action number 2 is not allowed.
        An action is not allowed when the corresponding column is full.
        """
        # TODO Your code here: allowed_actions must be an array of size 7 (number of possible actions),
        # and it should return one boolean per possible action, telling if that action is allowed or not
        allowed_actions = []
        for i in self.board[-1]:
            allowed_actions.append(i == 0)
        return allowed_actions

    def checkForEndGame(self):
        """Returns true if no action is possible (ie. if the board is full)"""
        """Does NOT check for victory of the players"""
        # TODO Your code here
        result = False
        if not any(0 in x for x in self.board):  # Check for any empty slot on board
            result = True
        return result

    def takeAction(self, action):
        """action must be between 0 (leftmost) and 6 (rightmost, ie. grid_shape[1]-1)"""
        """Computes (newState, value, done)"""
        """newState: GameState representing the state of the game after the current player has taken action"""
        """value: reward for that action"""
        """done: 1 if end of the game, 0 otherwise"""

        # YOUR CODE HERE: currentPlayer plays the action 'action'
        # next_state: new instance of GameState, with the new currentPlayer, and the new board
        # value: -VALUE_VICTORY if currentPlayer has won, else VALUE_DEFAULT_ACTION
        # done: True if the game is finished, ie. if currentPlayer has won, or if no action is possible

        # -value instead of value because this function outputs the value of the new state (ie. next_state)
        # from the point of vue (POV) of the new player (ie. of the player who will play after the current one)

        next_board = generate_next_board(self.board, self.currentPlayer, action)

        next_state = GameState(-self.currentPlayer, board=next_board)
        if self._isVictory(action, self.currentPlayer):
            value = -VALUE_VICTORY
            done = True
        else:
            value = VALUE_DEFAULT_ACTION
            done = next_state.checkForEndGame()

        return (next_state, value, done)

    def _generate_id(self):
        """Computes a unique id for that state (another identical state will have the same id)"""
        """The id is as small as possible for saving memory space (even so, it is a 85-bits integer)"""

        board_as_line = np.reshape(self.board, -1)
        player1_line = (board_as_line == PLAYER_1)
        player2_line = (board_as_line == PLAYER_2)
        result_line = np.concatenate((player1_line, player2_line, [self.currentPlayer == PLAYER_1])).tolist()
        # See https://stackoverflow.com/questions/25583312/changing-an-array-of-true-and-false-answers-to-a-hex-value-python
        result_line_val = functools.reduce(lambda byte, bit: byte * 2 + bit, result_line, 0)
        return result_line_val

    @staticmethod
    def from_id(id, grid_shape):
        """Generates a GameState from id"""

        # See https://stackoverflow.com/questions/33608280/convert-4-bit-integer-into-boolean-list/33608387
        nb_booleans = grid_shape[0] * grid_shape[1] * 2 + 1
        full_state = np.flip(np.array([bool(id & (1 << n)) for n in range(nb_booleans)]))
        player1_board = full_state[:grid_shape[0] * grid_shape[1]].reshape(grid_shape[0], grid_shape[1])
        player2_board = full_state[grid_shape[0] * grid_shape[1]:-1].reshape(grid_shape[0], grid_shape[1])
        current_player = full_state[-1]

        board = player1_board * PLAYER_1 + player2_board * PLAYER_2
        current_player = PLAYER_1 if current_player else PLAYER_2

        result = GameState(current_player, board=board.astype(np.int8))
        return result

    @staticmethod
    def current_player_from_id(id):

        current_player = bool(id & (1 << 0))
        current_player = PLAYER_1 if current_player else PLAYER_2
        return current_player

    def _isVictory(self, latestAction, currentPlayer):
        """Returns True if latestAction led currentPlayer to victory"""
        # YOUR CODE HERE: True if the latest action of currentPlayer could align NB_TOKENS_VICTORY
        # horizontally, vertically or in diagonal
        next_board = generate_next_board(self.board, self.currentPlayer, latestAction)

        return check_victory(next_board, currentPlayer)

    def __repr__(self):
        """String representation of the GameState object."""
        result = ''
        for r in reversed(range(self.board.shape[0])):
            result = result + str([RENDER_PLAYERS[x] for x in self.board[r]]) + '\n'

        return result


class Game:

    def __init__(self, grid_shape=GRID_SHAPE):
        self.gameState = None
        self.grid_shape = grid_shape
        self.name = 'connect4'
        self.action_size = grid_shape[1]
        self.reset()

    def reset(self):
        self.gameState = GameState(grid_shape=self.grid_shape, currentPlayer=PLAYER_1)
        return self.gameState

    def step(self, action):
        next_state, value, done = self.gameState.takeAction(action)
        # updates current game state
        self.gameState = next_state

        return (next_state, value, done)
