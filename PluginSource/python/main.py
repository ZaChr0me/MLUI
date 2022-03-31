# This is a sample Python script.
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from keras.utils.vis_utils import plot_model
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np

from python.GenericNeuralNetwork import GenericNetwork
from python.Train.Residual_CNN import HIDDEN_CNN_LAYERS
from python.Train.Residual_CNN import Residual_CNN, REG_CONST
from python.connect4.Game import GRID_SHAPE

inputs = [Input((1,))]
outputs = [Dense(2)(inputs[0])]
genericNetwork = Model(inputs=inputs, outputs=outputs)

residual_CNN = Residual_CNN(REG_CONST, (1,) + GRID_SHAPE,   GRID_SHAPE[1], HIDDEN_CNN_LAYERS)
residual_CNN.read(1,9,"./python/Train/")

def predict():
    board = [[0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    inputToModel = np.array([[board]], dtype=np.int8)  
    result = residual_CNN.predict(inputToModel)  
    print(result)
    choice = np.argmax(result[1][0])
    return  choice#genericNetwork.predict([1])[0,0]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_dim = {"input1": (1, 1, 75),
                 "input2": (1, 1, 1)}
    outputDim = {"output1": (3,),
                 "output2": (2,),
                 "output3": (1,)}
    # genericNetwork = GenericNetwork(input_dim, outputDim, layers_dim=(8, 2), residual=2)
    # genericNetwork.model.summary()
    genericNetwork.summary()
    plot_model(genericNetwork, show_shapes=True)

    print("The AI want to play at ", predict())
    """
    vectorIn = AiInput((3,))
    vectorIn.model.summary()

    boolOut = BoolAiOutput(vectorIn.model).head
    boolOut = Model(inputs=vectorIn.model.input, outputs=boolOut)
    boolOut.summary()
    """
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
