import tensorflow as tf
from keras import Input, regularizers
from keras.layers import Flatten, Dense
from keras.models import Model

REG_CONST = 0.0001


class AiInput:
    def __init__(self, size, dtype=tf.int32) -> None:
        self.inputs = Input(shape=size, dtype=dtype, name="Input_Vector_of_{0}_{1}".format(size, dtype.name))
        self.model = Model(inputs=self.inputs, outputs=self.inputs)


class AiOutput:
    id = 0

    def __init__(self, model, params=None):
        if params is None:
            params = []
        self.head = self.build(model, params)

    def build(self, model, params):
        AiOutput.id += 1
        return

    def flatten(model):
        # if tf.size(model.output) < 2:
        # return (model.output)
        return Flatten()(model)


class ChoiceAiOutput(AiOutput):
    def __init__(self, model, params=[3]):
        super(ChoiceAiOutput, self).__init__(model, params)

    def build(self, model, params):
        super(ChoiceAiOutput, self).build(model, params)
        x = Dense(params[0],
                  activation="linear",
                  kernel_regularizer=regularizers.l2(REG_CONST),
                  name="Output_{0}_choices_{1}".format(AiOutput.id, params[0]))(AiOutput.flatten(model))
        return x


class BoolAiOutput(AiOutput):
    def __init__(self, model):
        super(BoolAiOutput, self).__init__(model)

    def build(self, model, params):
        super(BoolAiOutput, self).build(model, params)
        x = Dense(1,
                  activation="tanh",
                  kernel_regularizer=regularizers.l2(REG_CONST),
                  name="Output_{0}_Bool".format(AiOutput.id))(AiOutput.flatten(model))
        return x
