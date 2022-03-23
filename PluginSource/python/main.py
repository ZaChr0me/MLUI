# This is a sample Python script.
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from keras.utils.vis_utils import plot_model

from GenericNeuralNetwork import GenericNetwork

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_dim = {"input1": (1, 1, 75),
                 "input2": (1, 1, 1)}
    outputDim = {"output1": (3,),
                 "output2": (2,),
                 "output3": (1,)}
    genericNetwork = GenericNetwork(input_dim, outputDim, layers_dim=(8, 2), residual=2)
    genericNetwork.model.summary()
    plot_model(genericNetwork.model, show_shapes=True)
    """
    vectorIn = AiInput((3,))
    vectorIn.model.summary()

    boolOut = BoolAiOutput(vectorIn.model).head
    boolOut = Model(inputs=vectorIn.model.input, outputs=boolOut)
    boolOut.summary()
    """
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
