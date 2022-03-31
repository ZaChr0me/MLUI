import random

import numpy as np

from MCTS.MCTS import MCTS
from MCTS.Node import Node
from connect4.Game import GRID_SHAPE


class Agent():
    def __init__(self, name, nb_simulations, cpuct, model, turns_until_deterministic, temperature=1):

        self.name = name

        # We need a game state in order to initialize the MCTS, so we cannot do it now
        self.mcts = None
        # params for the MCTS
        self.nb_simulations = nb_simulations
        self.cpuct = cpuct
        self.model = model

        # After turns_until_deterministic turns, the agent choses its next move deterministically - ie. it always
        # choses the best action according to the MCTS. See _chooseAction(self, action_scores, stochastic) for more information
        self.turns_until_deterministic = turns_until_deterministic
        # In fact, this random choice is also mitigated by the "temperature":
        # probability(move being chosen) = N ^ (1/temperature)
        # => if temperature = 1: the "weight" of that move is equal to N in the probability distribution
        #       (favoring exploitation of the simulations of the MCTS)
        # => if temperature = infinite: the "weight" of all the moves is equal to 1 in the probability distribution
        #       (favoring exploration: whatever the results of the simulations of the MCTS, they are not taken into account,
        #       because all moves end up with the same probability)
        self.temperature = temperature

    def chose_action_from_mcts(self, state, turn, debug=False):

        ### If we are initializing the tree in order to compute the best next move for state 'state':
        ### as per the cheatsheet: the subtree of the previous chosen move is retained for calculating subsequent moves,
        ### the rest is discarded
        if self.mcts == None or state.id not in self.mcts.nodes_dict:
            # 1) either this is the very first move of the game, and the tree does not exist at all
            self.mcts = MCTS(Node(state), self.cpuct, self.model, debug=debug)
        else:
            # 2) or a previous move has been played already, and its subtree becomes the new tree
            self.mcts.root = self.mcts.nodes_dict[state.id]
            self.mcts.debug = debug

        ## YOUR CODE HERE: let the MCTS run self.nb_simulations simulations
        for simulation in range(self.nb_simulations):
            self.mcts.simulate()
        #### action_scores contains the scores of the possible actions
        #### probas_of_victory contains the proba of victory of the next state for each possible action
        ## YOUR CODE HERE call one of the functions below
        action_scores, probas_of_victory = self._getAV()
        ####pick the action
        ## YOUR CODE HERE  call one of the functions below
        action = self._chooseAction(action_scores, turn)
        ## YOUR CODE HERE  get the proba of victory of the selected action
        proba_victory = probas_of_victory[action]

        if debug:
            print('ACTION SCORES...%s', action_scores)
            print('CHOSEN ACTION...%d', action)
            print('CURRENT PROBA OF VICTORY...%f', proba_victory)

        return (action, action_scores, proba_victory)

    def _getAV(self):
        edges = self.mcts.root.edges
        action_scores = np.zeros(GRID_SHAPE[1], dtype=np.integer)
        probas_of_victory = np.zeros(GRID_SHAPE[1], dtype=np.float32)

        for action, edge in edges:
            action_scores[action] = pow(edge.stats['N'], 1 / self.temperature)
            probas_of_victory[action] = edge.stats['Q']

        action_scores = action_scores / (np.sum(action_scores) * 1.0)
        return action_scores, probas_of_victory

    def _chooseAction(self, action_scores, turn):

        # if stochastic = True: the agent choses randomly one action with respect to the propabilities computed by MTCS
        # if stochastic = False: the agent follows the action with the best probability computed by the MCTS
        # Example: the agent has 7 possible actions. After simulating all of them, the MCTS finds the following probabilities
        # of victory: action0 = 1% , action1 = 98% , action3 = 1%, action4 = 0%... (the sum of the probabilities must be 100%)
        # If stochastic = False, the agent will always chose action1 because it is the highest.
        # If stochastic = True, the agent will have 1% of probability to chose action1, 98% to chose action2, 1% to to chose action3.
        #
        # When stochastic=True, the idea is to encourage some exploration: if the agent always follows the MCTS, the games during training
        # will always be the same (or almost the same), and the agent will not have seen enough different possibilities.
        stochastic = True if turn < self.turns_until_deterministic else False
        if stochastic:
            action_idx = np.random.multinomial(1, action_scores)
            action = np.where(action_idx == 1)[0][0]
        else:
            actions = np.argwhere(action_scores == max(action_scores))
            action = random.choice(actions)[0]

        return action