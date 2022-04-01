import numpy as np
from IPython.display import clear_output

from connect4.Game import Game


def one_game_AI_versus_AI(ai_0, ai_1, env, debug=False):
    state = env.reset()
    turn = 0
    done = False

    result_states = []

    ## YOUR CODE HERE: play a game between ai_0 and ai_1, until the game is finished (ie. until it is done)
    ## result_states must contain the list of (state, action_scores, proba_victory) of the game, except for the last state
    ## state must contain the last state
    ## value must contain the value of the last state

    while not done:

        print(env.gameState)

        turn += 1

        ## If AI 0
        if (turn % 2 == 1):
            action, action_scores, current_proba_victory = ai_0.chose_action_from_mcts(state, turn, debug)
        ## If AI 1
        else:
            action, action_scores, current_proba_victory = ai_1.chose_action_from_mcts(state, turn, debug)

        if not debug:
            clear_output(wait=True)
        print('action: ', action)
        print(['{0:.2f}'.format(np.round(x, 2)) for x in action_scores])
        print('proba of victory before playing the action: ', np.round(current_proba_victory, 2))

        state, value, done = env.step(action)
        print('Current state value (1 if victory, 0 otherwise): ', value)
        print('done: ', done)
        if not done:
            result_states.append((state, action_scores, current_proba_victory))

    # Print the board when the game is finished
    print(env.gameState)

    ## As a reminder:
    ## agent.chose_action_from_mcts(state, turn) choses an action and outputs various other useful information
    ## env.step(action) executes the action and outputs various useful information

    return result_states, state, value


def AI_versus_AI(ai_0, ai_1, nb_episodes, debug=False):
    env = Game()
    scores = {ai_0.name: 0, "drawn": 0, ai_1.name: 0}

    ## YOUR CODE HERE: play nb_episodes games between ai_0 and ai_1, ie. call one_game_AI_versus_AI() nb_episodes times
    ## Warning with the state and value returned by one_game_AI_versus_AI():
    ## The winner made his move, env.step() switched to the other player and detected that the game was finished, and now the 'current player' is the loser
    ## For example, player1 moved, he won, env.step() switched to player2 and detected the victory of player1: state.currentPlayer contains player2
    ## => the winner is -state.currentPlayer in the state returned by one_game_AI_versus_AI()
    ## => value has to be inversed as well, because it contains the value of the game from the point of view of player2
    ##    value = 0 if nobody wins (ie. when there is a drawn)

    for i in range(nb_episodes):
        result_states, state, value = one_game_AI_versus_AI(ai_0, ai_1, env, debug)
        if -state.currentPlayer == 1:
            scores[ai_0.name] += 1
        elif -state.currentPlayer == -1:
            scores[ai_1.name] += 1
        else:
            scores["drawn"] += 1

    # Increment by 1 the score of the AIs when they win, and return the scores - don't forget to increment the number of drawns when nobody wins

    return scores
