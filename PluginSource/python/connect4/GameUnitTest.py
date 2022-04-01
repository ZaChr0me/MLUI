import unittest

from Game import *


class MyTestCase(unittest.TestCase):

    def test_something(self):
        env = Game()
        env.reset()
        next_state, value, done = env.step(3)

        assert (done == False)
        assert (value == 0)
        assert (np.array_equal(next_state.board, np.array([[0, 0, 0, 1, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0]])))
        next_state
        next_state, value, done = env.step(2)

        assert (done == False)
        assert (value == 0)
        assert (np.array_equal(next_state.board, np.array([[0, 0, -1, 1, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0]])))
        next_state
        next_state, value, done = env.step(3)
        next_state, value, done = env.step(2)
        next_state, value, done = env.step(3)
        next_state, value, done = env.step(2)
        next_state, value, done = env.step(3)

        assert (done == True)
        assert (value == -1)
        assert (np.array_equal(next_state.board, np.array([[0, 0, -1, 1, 0, 0, 0],
                                                           [0, 0, -1, 1, 0, 0, 0],
                                                           [0, 0, -1, 1, 0, 0, 0],
                                                           [0, 0, 0, 1, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0, 0]])))
        next_state

    def test_is_victory(self):
        # Test of the method game_state._isVictory: horizontal lines

        for ligne in range(0, GRID_SHAPE[0]):
            # On met toutes les façons d'aligner 4 PLAYER_1 dans la ligne ligne
            for column in range(0, GRID_SHAPE[1] + 1 - NB_TOKENS_VICTORY):
                board = np.full(GRID_SHAPE, NONE, dtype=np.int8)
                board[ligne, column:column + NB_TOKENS_VICTORY] = PLAYER_1
                # On remplit les lignes sous ligne avec PLAYER_2
                board[0:ligne, :] = PLAYER_2

                game_state = GameState(grid_shape=GRID_SHAPE, currentPlayer=PLAYER_1, board=board)

                for i in range(column, column + NB_TOKENS_VICTORY):
                    is_victory = game_state._isVictory(i, PLAYER_1)
                    assert (is_victory == True)

        # Test of the method game_state._isVictory: vertical lines

        for ligne in range(0, GRID_SHAPE[0] + 1 - NB_TOKENS_VICTORY):
            for column in range(0, GRID_SHAPE[1]):
                # On met toutes les façons d'aligner 4 PLAYER_1 dans la colonne column
                board = np.full(GRID_SHAPE, NONE, dtype=np.int8)
                board[ligne:ligne + NB_TOKENS_VICTORY, column] = PLAYER_1
                # On remplit les lignes sous ligne avec PLAYER_2
                board[0:ligne, :] = PLAYER_2
                game_state = GameState(grid_shape=GRID_SHAPE, currentPlayer=PLAYER_1, board=board)

                is_victory = game_state._isVictory(column, PLAYER_1)
                assert (is_victory == True)

        # Test of the method game_state._isVictory: diagonal 1 (bottom left to top right)

        for ligne in range(0, GRID_SHAPE[0] + 1 - NB_TOKENS_VICTORY):
            for column in range(0, GRID_SHAPE[1] + 1 - NB_TOKENS_VICTORY):
                # On aligne 4 PLAYER_1 dans la diagonale dont le point de départ (bas,gauche) est (ligne,column)
                board = np.full(GRID_SHAPE, NONE, dtype=np.int8)
                for i, j in zip(range(ligne, ligne + NB_TOKENS_VICTORY), range(column, column + NB_TOKENS_VICTORY)):
                    board[i, j] = PLAYER_1
                    board[0:i, j] = PLAYER_2
                    board[i, j + 1:] = PLAYER_2
                # On remplit les lignes sous ligne avec PLAYER_2
                board[0:ligne, :] = PLAYER_2
                game_state = GameState(grid_shape=GRID_SHAPE, currentPlayer=PLAYER_1, board=board)

                for i in range(column, column + NB_TOKENS_VICTORY):
                    is_victory = game_state._isVictory(i, PLAYER_1)
                    assert (is_victory == True)

        # Test of the method game_state._isVictory: diagonal 2 (bottom right to top left)

        for ligne in range(GRID_SHAPE[0] + 1 - NB_TOKENS_VICTORY, GRID_SHAPE[0]):
            for column in range(0, GRID_SHAPE[1] + 1 - NB_TOKENS_VICTORY):
                # On aligne 4 PLAYER_1 dans la diagonale dont le point de départ (bas,gauche) est (ligne,column)
                board = np.full(GRID_SHAPE, NONE, dtype=np.int8)
                for i, j in zip(range(ligne, ligne - NB_TOKENS_VICTORY, -1), range(column, column + NB_TOKENS_VICTORY)):
                    board[i, j] = PLAYER_1
                    board[0:i, j] = PLAYER_2
                    board[i, 0:j] = PLAYER_2
                # On remplit les lignes sous ligne avec PLAYER_2
                board[0:ligne - 3, :] = PLAYER_2
                game_state = GameState(grid_shape=GRID_SHAPE, currentPlayer=PLAYER_1, board=board)

                for i in range(column, column + NB_TOKENS_VICTORY):
                    is_victory = game_state._isVictory(i, PLAYER_1)
                    assert (is_victory == True)

if __name__ == '__main__':
    unittest.main()
