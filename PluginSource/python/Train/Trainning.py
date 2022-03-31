# The one variable left for us to decide
from os import mkdir

import numpy as np
import tensorflow as tf
from keras.utils.vis_utils import plot_model

from AiInput import REG_CONST
from MCTS.Agent import Agent
from MCTS.AiVsAi import AI_versus_AI
from Memory import feed_memory, Memory
from Train.Residual_CNN import Residual_CNN, HIDDEN_CNN_LAYERS, VALUE_HEAD, POLICY_HEAD, DRIVE_PATH
from connect4.Game import GRID_SHAPE

NB_SIMULATION = 100
AGENT_VERSION = "2"
MOMENTUM = 0.9
LEARNING_RATE = 0.1
tournament_number = 0
current_iteration = 0
nb_iterations = 1
nb_games_per_iteration = 10

## YOUR CODE HERE: instanciate the first agent: as many simulations as you want (not too big, otherwise the computation will be too long)
## it must use residual_CNN as a model, cpuct=1, temperature=1, turns_until_deterministic=10

residual_CNN = Residual_CNN(REG_CONST, (1,) + GRID_SHAPE, GRID_SHAPE[1], HIDDEN_CNN_LAYERS)
residual_CNN.compile(learning_rate=LEARNING_RATE, momentum=MOMENTUM, loss_weights={VALUE_HEAD: 0.5, POLICY_HEAD: 0.5})
agent_cnn_1 = Agent("Agent CNN 1", nb_simulations=NB_SIMULATION, cpuct=1, model=residual_CNN,
                    turns_until_deterministic=10, temperature=1)

# residual_CNN.compile(learning_rate=LEARNING_RATE, momentum=MOMENTUM, loss_weights={VALUE_HEAD: 0.5, POLICY_HEAD: 0.5})


## YOUR CODE HERE: instanciate another residual CNN, with the same params as residual_CNN
## Compile it with LEARNING_RATE, MOMENTUM, loss_weights={VALUE_HEAD: 0.5, POLICY_HEAD: 0.5},
## in order to make it trainable
residual_CNN_2 = Residual_CNN(REG_CONST, (1,) + GRID_SHAPE, GRID_SHAPE[1], HIDDEN_CNN_LAYERS)
residual_CNN_2.compile(learning_rate=LEARNING_RATE, momentum=MOMENTUM, loss_weights={VALUE_HEAD: 0.5, POLICY_HEAD: 0.5})

## YOUR CODE HERE: instanciate the 2nd agent: same number of simulations as agent_cnn_1 (in order to avoid giving an advantage during the tournaments)
## it must use residual_CNN_2 as a model, cpuct=1, temperature=1, turns_until_deterministic=10
agent_cnn_2 = Agent("Agent CNN 2", nb_simulations=NB_SIMULATION, cpuct=1, model=residual_CNN_2,
                    turns_until_deterministic=10, temperature=1)

import pickle

stop_after_2_bad_epochs = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=2)

BATCH_SIZE = 256
EPOCHS = 50


def train_neural_network(agent_cnn_1, agent_cnn_2, agent_version, current_iteration, nb_iterations,
                         nb_games_per_iteration, memory):
    for iteration in range(current_iteration, nb_iterations):
        ## YOUR CODE HERE:
        ##   - feed the memory by playing nb_games_per_iteration games between agent_cnn_1 and itself
        ##   - train agent_cnn_2 on the content of the memory, during EPOCHS epochs, with BATCH_SIZE, stopping after 2 bad epochs.
        ##        don't forget to use state.get_board_for_neural_network() when you create the input of the neural network
        ##        The targets (or labels) can be created with:
        ## training_targets = {VALUE_HEAD: np.array([row['value'] for row in memory.memory])
        ##          , POLICY_HEAD: np.array([row['AV'] for row in memory.memory])}
        feed_memory(agent_cnn_1, agent_cnn_1, nb_games_per_iteration, memory)

        training_states = np.array([[row['state'].get_board_for_neural_network()] for row in memory.memory])
        training_targets = {VALUE_HEAD: np.array([row['value'] for row in memory.memory]),
                            POLICY_HEAD: np.array([row['AV'] for row in memory.memory])}

        agent_cnn_2.model.fit(training_states,
                              targets=training_targets,
                              epochs=EPOCHS,
                              verbose=1,
                              validation_split=0.2,
                              batch_size=BATCH_SIZE,
                              callbacks=stop_after_2_bad_epochs)

        agent_cnn_2.model.write(agent_version, iteration)
        pickle.dump(memory,
                    open(DRIVE_PATH + "memory/memory_" + str(agent_version) + "_" + str(iteration).zfill(4) + ".p",
                         "wb"))

        ## Optionally, you can upload the files on your Google drive automatically, see
        ## https://colab.research.google.com/drive/100Z7aLvJgqJeBoSNwjXUp6gBSZojiRZ1#scrollTo=Nsq6rFIAMSIn for an example
        ## If you do it, upload the latest file found in the folder 'memory' and the latest file found in the folder 'models'


memory = Memory()

import glob
import os

latest_saved_iteration = 0
files_in_run_folder = list(glob.iglob(DRIVE_PATH + "memory/memory*.p"))
if len(files_in_run_folder) > 0:
    latestFile = max(files_in_run_folder, key=os.path.getctime)
    # See https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    tournament_number = int(latestFile[latestFile.find('_') + len('_'):latestFile.rfind('_')])
    current_iteration = int(latestFile[latestFile.rfind('_') + len('_'):latestFile.rfind('.p')])

    print(
        'LOADING MEMORY for tournament ' + str(tournament_number) + ' and iteration ' + str(current_iteration))
    memory = pickle.load(open(
        DRIVE_PATH + "memory/memory_" + str(tournament_number) + "_" + str(current_iteration).zfill(4) + ".p",
        "rb"))

    print('LOADING MODEL for tournament ' + str(tournament_number) + ' and iteration ' + str(current_iteration))
    agent_cnn_2.model.read(tournament_number, current_iteration)
    agent_cnn_1.model.read(tournament_number, current_iteration)

    current_iteration += 1
    if current_iteration >= nb_iterations:
        tournament_number += 1
        current_iteration = current_iteration % nb_iterations

plot_model(agent_cnn_2.model.model, show_shapes=True)

SCORING_THRESHOLD = 1.3

while 1:
    ## YOUR CODE HERE:
    ## - train agent_cnn_2 as many times as you want, from the results of the games between agent_cnn_1 and itself
    ## - then play a few games between agent_cnn_1 and agent_cnn_2 and compare the scores
    train_neural_network(agent_cnn_1, agent_cnn_2, tournament_number, current_iteration, nb_iterations,
                         nb_games_per_iteration, memory)
    tournament_number += 1
    current_iteration = (current_iteration + 1) % nb_iterations

    scores = AI_versus_AI(agent_cnn_1, agent_cnn_2, 10)
    score_agent_1 = scores[agent_cnn_1.name]
    score_agent_2 = scores[agent_cnn_2.name]

    #    if the score of agent_cnn_2 is more than SCORING_THRESHOLD * the score of agent_cnn_1, update agent_cnn_1 with agent_cnn_2
    if score_agent_2 > score_agent_1 * SCORING_THRESHOLD:
        print(agent_cnn_2.name + " became the best ! Let us copy it into " + agent_cnn_1.name)
        agent_cnn_1.model.model.set_weights(agent_cnn_2.model.model.get_weights())
    else:
        print("The best is still" + agent_cnn_1.name + ". Maybe next time !")
