# Imports
# Import keras
from keras.layers import Dense, concatenate, add
from keras.models import Model, load_model
from keras.optimizer_v2.gradient_descent import SGD
import tensorflow as tf

from python.AiInput import AiInput, ChoiceAiOutput

MODEL_PATHS = "./models"
VALUE_HEAD = "value_head"
POLICY_HEAD = "policy_head"


def softmax_cross_entropy_with_logits(y_true, y_prediction):
    p = y_prediction
    pi = y_true

    zero = tf.zeros(shape=tf.shape(pi), dtype=tf.float32)
    where = tf.equal(pi, zero)

    negatives = tf.fill(tf.shape(pi), -100.0)
    p = tf.where(where, negatives, p)

    loss = tf.nn.softmax_cross_entropy_with_logits(labels=pi, logits=p)

    return loss


class GenericNetwork:
    def __init__(self, inputs_branches, output_branches, layers_dim=(2, 64), residual=1, activation="linear"):
        self.inputs_branches = inputs_branches
        self.output_branches = output_branches
        self.layersDim = layers_dim
        self.residual = residual
        self.activation = activation

        self.model = self._build()

    def predict(self, x):
        return self.model.predict(x)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size, callbacks=None):
        return self.model.fit(states, targets, epochs=epochs, verbose=verbose, validation_split=validation_split,
                              batch_size=batch_size, callbacks=callbacks)

    def write(self, agent_version, iteration):
        self.model.save(MODEL_PATHS + '/version_' + str(agent_version) + "_{0:0>4}".format(iteration) + '.h5')

    def read(self, agent_version, iteration):
        tmp_model = load_model(
            MODEL_PATHS + '/version_' + str(agent_version) + "_{0:0>4}".format(iteration) + '.h5',
            custom_objects={'softmax_cross_entropy_with_logits': softmax_cross_entropy_with_logits})
        self.model.set_weights(tmp_model.get_weights())

    def compile(self, learning_rate, momentum, loss_weights=None):
        if loss_weights is None:
            loss_weights = {VALUE_HEAD: 0.5, POLICY_HEAD: 0.5}
        self.model.compile(loss={VALUE_HEAD: 'mean_squared_error', POLICY_HEAD: softmax_cross_entropy_with_logits},
                           optimizer=SGD(lr=learning_rate, momentum=momentum),
                           loss_weights=loss_weights
                           )
        return self.model

    def inputs(self):
        input_branches = []
        for input_branch in self.inputs_branches:
            x = AiInput(self.inputs_branches[input_branch])
            input_branches.append(x)

        return input_branches

    def outputs(self, x):
        output_branches = []
        for _ in self.output_branches:
            head = ChoiceAiOutput(x)
            output_branches.append(head.head)

        return output_branches

    def dense_layers(self, x):
        x = Dense(self.layersDim[0], activation=self.activation)(x)
        return x

    def residual_block(self, x, block_function):
        x = block_function(x)
        for layer in range(1, self.layersDim[0] // self.residual):
            input_layer = x
            for res in range(0, self.residual):
                x = block_function(x)
            x = add([input_layer, x])
        return x

    def _build(self):
        input_branches = self.inputs()

        input_starts = []
        input_ends = []
        for in_branch in input_branches:
            input_ends.append(in_branch.model.output)
            input_starts.append(in_branch.model.input)

        combined = concatenate(input_ends)
        combined = self.residual_block(combined, self.dense_layers)

        output_branches = self.outputs(combined)
        # output_branches = [Dense(3, activation=self.activation)(combined)]

        model = Model(inputs=input_starts, outputs=output_branches)
        return model
