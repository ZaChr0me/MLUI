import sys
sys.path.append(r"C:\Users\souli\Documents\Travail\EFREI\M2\PFE\MLUI\PluginSource")

from python.MCTSAgent.Agent import Agent
from python.Train.Residual_CNN import HIDDEN_CNN_LAYERS
from python.Train.Residual_CNN import Residual_CNN, REG_CONST
from python.connect4.Game import GRID_SHAPE, Game, GameState
from IPython.display import clear_output
import numpy as np

NB_SIMULATION = 50
TOURNAMENT_NUMBER = 1
AGENT_VERSION = 9

residual_CNN = Residual_CNN(REG_CONST, (1,) + GRID_SHAPE,   GRID_SHAPE[1], HIDDEN_CNN_LAYERS)
residual_CNN.read(TOURNAMENT_NUMBER, AGENT_VERSION,"./python/Train/")

ai_agent = Agent("Demo ML Agent", nb_simulations=NB_SIMULATION, cpuct=1, model=residual_CNN,
                    turns_until_deterministic=0, temperature=1)

print("Ai loaded")

def play(board=None, me=1):
    print("\nLet's play")
    print(board)
    #Default board
    #if board==None:
    board = [[0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    #Convert board for the AI
    board = np.array(board, dtype=np.int8)  
    print("board converted")

    #Create game state
    state = GameState(me, board=board)
    print(state)

    #Ask agent for its decision
    action, _, _ = ai_agent.chose_action_from_mcts(state, 1)
    print("decision: ", action)
    return action
    """
    
    #Make a prediction on the board
    result = residual_CNN.predict(inputToModel)  
    print(result)

    #Send the action decided by the AI
    choice = np.argmax(result[1][0])
    return  choice
    """

def playerVersusAI(ai_player, ai_plays_first=False, debug=False):

    env = Game()
    state = env.reset()

    turn = 0
    done = False

    while not done:

        print(env.gameState)

        turn = turn + 1
        is_ai_current_player = True if (turn % 2 == 0) and not ai_plays_first else False

        ## If the AI player has to play
        if is_ai_current_player:
            action, action_scores, current_proba_victory = ai_player.chose_action_from_mcts(state, turn, debug)
            
            if not debug:
                clear_output(wait=True)
            print('action: ', action)
            print(['{0:.2f}'.format(np.round(x,2)) for x in action_scores])
            print('proba of victory before playing the action: ', np.round(current_proba_victory,2))
        else:
            correct_action = False
            while not correct_action:
                print("Please enter an integer between 0 and " + str(GRID_SHAPE[1]-1))
                action = int(input())
                correct_action = True if (action >= 0 and action < GRID_SHAPE[1]) else False

            if not debug:
                clear_output(wait=True)

        state, value, done = env.step(action)
        print('Current state value (1 if victory, 0 otherwise): ', value)
        print('done: ', done)
        
    # Print the board when the game is finished
    print(env.gameState)

if __name__ == '__main__':
    playerVersusAI(ai_agent)