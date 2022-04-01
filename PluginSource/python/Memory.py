from collections import deque

from MCTSAgent.AiVsAi import one_game_AI_versus_AI
from connect4.Game import Game

MEMORY_SIZE = 30000


class Memory:
    def __init__(self, size=MEMORY_SIZE):
        self.memory_size = size
        self.memory = deque(maxlen=self.memory_size)

    def __len__(self):
        return len(self.memory)

    def commit_memory(self, state, action_scores, victory_proba, value):
        self.memory.append({'state': state, 'AV': action_scores, 'VP': victory_proba, 'value': value})
        # Commit also the symetrical board and values, in order to improve the training
        symetrical_state = state.generate_symetric_state()
        # Get the corresponding action_scores
        symetrical_action_scores = action_scores[::-1]

        self.memory.append(
            {'state': symetrical_state, 'AV': symetrical_action_scores, 'VP': victory_proba, 'value': value})

    def clear_memory(self):
        self.memory = deque(maxlen=self.memory_size)

def feed_memory(ai_0, ai_1, nb_episodes, memory, debug=False):
    """
    Plays matches and stores each move in memory. The MCTS is the most important here: it evaluates the moves.
    The more simulations it does, the better the results => mcts_simulations should high enough.
    The neural network is secondary: it evaluates the leaves of the tree, when a leave is not the end of the game
    (ie. depending on the number of simulations, the simulations might not have enough moves to finish a game,
    and the neural network evaluates the last move of the simulation. Hence, even if the neural network gives poor
    results, the MCTS simulates enough moves to get a good evaluation of the scores of each possible action at
    the root of the tree.)

    Each move is stored in memory, along with the evaluation of the moves.
    Afterwards, when that "dataset" is big enough, the neural network is trained on it.

    That way, during the next call to this function, the MCTS will give better results, because its leaves will
    be better evaluated by the neural network, and so on: we get a virtuous circle.

    After enough iterations, we can stop using the MCTS and let directly the neural network play against a human
    or against another neural network, if we want to do some "genetic selection".
    """

    env = Game()

    ## YOUR CODE HERE: play nb_episodes games between ai_0 and ai_1
    ## As a reminder, one_game_AI_versus_AI() returns the list of the states of the game in 'result_states'
    ## 'result_states' is a list of (state, action_scores, proba_victory) that you must store in memory in order to train the neural network
    ##
    ## NB: memory.commit_memory(state, action_scores, proba_victory, value):
    ##   - state, action_scores, proba_victory are given by 'result_states', as seen above
    ##   - value is given by last_value returned by one_game_AI_versus_AI(), with several tricks:
    ##      *) one_game_AI_versus_AI() also returns last_state, but as seen previously, the winner is -last_state.currentPlayer,
    ##          because the winner just made his move, env.step() switched to the other player and detected that the game was finished
    ##          For example, player1 moved, he won, and env.step() switched to player2 and detected the victory of player1: state.currentPlayer contains player2
    ##          => the winner is -state.currentPlayer
    ##          => if the game was a drawn, the last player is -state.currentPlayer anyway
    ##      *) value = 0 at the first move, and 'last_value' or '-last_value' after: 1 if the move was played by the last player, -1 otherwise

    for episode in range(nb_episodes):
      result_states, state, value = one_game_AI_versus_AI(ai_0, ai_1, env, debug=debug)
      lastPlayer = state.currentPlayer
      for idx, result_state in enumerate(result_states):
        state = result_state[0]
        action_scores = result_state[1]
        proba_victory = result_state[2]
        currentPlayer = state.currentPlayer
        if idx == 0:
          value = 0
        elif (currentPlayer == lastPlayer):
          value = 1
        else:
          value = -1
        memory.commit_memory(state, action_scores, proba_victory, value)
