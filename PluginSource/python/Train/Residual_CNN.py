from keras.models import load_model, Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from keras import regularizers
from keras.optimizer_experimental.sgd import SGD

from keras.utils.vis_utils import plot_model

from python.GenericNeuralNetwork import softmax_cross_entropy_with_logits
from python.connect4.Game import GRID_SHAPE

VALUE_HEAD = 'value_head'
POLICY_HEAD = 'policy_head'

DRIVE_PATH = "./"

class Residual_CNN():
    def __init__(self, reg_const, input_dim, output_dim, hidden_layers):
        self.reg_const = reg_const
        self.input_dim = input_dim
        self.output_dim = output_dim

        self.hidden_layers = hidden_layers
        self.num_layers = len(hidden_layers)
        self.model = self._build_model()

    def predict(self, x):
        return self.model.predict(x)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size, callbacks=None):
        return self.model.fit(states, targets, epochs=epochs, verbose=verbose, validation_split=validation_split,
                              batch_size=batch_size, callbacks=callbacks)

    def write(self, agent_version, iteration):
        self.model.save(DRIVE_PATH + 'models/version_' + str(agent_version) + "_{0:0>4}".format(iteration) + '.h5')

    def read(self, agent_version, iteration, path=None):
        if path==None:
            path=DRIVE_PATH
        tmp_model = load_model(
            path + 'models/version_' + str(agent_version) + "_{0:0>4}".format(iteration) + '.h5',
            custom_objects={'softmax_cross_entropy_with_logits': softmax_cross_entropy_with_logits})
        self.model = tmp_model#.set_weights(tmp_model.get_weights())

    def conv_layer(self, x, filters, kernel_size):
        """	x: output of the previous layer
            filters and kernel_size: params of the Conv2D layer added by this function
            Result of this function: output of the LeakyRelu (see below)"""

        ## YOUR CODE HERE: a 'conv layer' is made of:
        ##    - a Conv2D layer of 'filters' filters, of size 'kernel_size', padding 'same',
        ##				with L2 regularization of constant self.reg_const, in order to avoid overfitting.
        ##			  Warning: as seen in the method 'evaluate_action_scores_from_model(state)', we are operating
        ##				in data_format equal to "channels_first".
        ##		- a BatchNormalization layer. As we are in data_format equal to "channels_first", you have to precise 'axis=1'
        ##		- a LeakyRelu layer
        x = Conv2D(filters=filters,
                   kernel_size=kernel_size,
                   data_format="channels_first",
                   padding="same",
                   use_bias=False,
                   activation='linear',
                   kernel_regularizer=regularizers.l2(self.reg_const))(x)
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        return x

    def residual_layer(self, input_block, filters, kernel_size):
        """	input_block: output of the previous layer
            filters and kernel_size: params of the Conv2D layers added by this function
            Result of this function: output of the LeakyRelu (see below)"""

        ## YOUR CODE HERE: a 'residual layer' is made of:
        ##			- a conv_layer with params input_block, filters, kernel_size
        ##			- a Conv2D with same params as above
        ##			- a BatchNormalization layer with 'axis=1'
        ##			- a layer adding input_block and the output of the BatchNormalization layer
        ##			- a LeakyRelu layer

        x = self.conv_layer(input_block, filters, kernel_size)

        x = Conv2D(filters=filters,
                   kernel_size=kernel_size,
                   data_format="channels_first",
                   padding="same",
                   use_bias=False,
                   activation='linear',
                   kernel_regularizer=regularizers.l2(self.reg_const))(x)

        x = BatchNormalization(axis=1)(x)

        x = add([input_block, x])

        x = LeakyReLU()(x)

        return (x)

    def value_head(self, x):
        """x: output of the previous layer"""

        ## YOUR CODE HERE: the 'value head' is made of:
        ##			- a Conv2D layer with 1 filter of size 1, data_format="channels_first", padding = 'same'
        ##				L2 regularization of self.reg_const
        ##			- a BatchNormalization with 'axis=1'
        ##			- a LeakyRelu layer
        ##			- the layer that you must put mandatorily between a Conv2D layer and a Dense layer
        ##			- a Dense layer with 20 neurons, and L2 regularization of self.reg_const
        ##			- a LeakyRelu layer
        ##			- a Dense layer of <how many neurons ????>, with activation <which activation ???>,
        ##				L2 regularization of self.reg_const and name = VALUE_HEAD
        ##
        ## You should easily deduce the number of neurons of the last layer, because we need
        ##	that head to output one value (the estimate of the value of the current board)
        ## You should also be able to deduce easily the activation function, because that value should be
        ##  between -1 and 1
        x = Conv2D(filters=1,
                   kernel_size=1,
                   data_format="channels_first",
                   padding="same",
                   use_bias=False,
                   activation='linear',
                   kernel_regularizer=regularizers.l2(self.reg_const))(x)
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(20,
                  kernel_regularizer=regularizers.l2(self.reg_const))(x)
        x = LeakyReLU()(x)

        x = Dense(1,
                  activation="tanh",
                  kernel_regularizer=regularizers.l2(self.reg_const),
                  name=VALUE_HEAD)(x)

        return (x)

    def policy_head(self, x):
        """x: output of the previous layer"""

        ## YOUR CODE HERE: the 'policy head' is made of:
        ##			- a Conv2D layer with 2 filters of size 1, data_format="channels_first", padding = 'same'
        ##				L2 regularization of self.reg_const
        ##			- a BatchNormalization with 'axis=1'
        ##			- a LeakyRelu layer
        ##			- the layer that you must put mandatorily between a Conv2D layer and a Dense layer
        ##			- a Dense layer with <how many neurons ????> neurons,
        ##				L2 regularization of self.reg_const and name = POLICY_HEAD
        ##
        ## You should easily be able to deduce the number of neurons of the last layer, because this head
        ##  must output a probability for the actions in the current state of the game.
        ##   Hint: this number is a param of this class.
        ##
        ## The output is a linear value, not a softmax, because we force the probabilities of the forbidden actions
        ## to 0 in agent.evaluate_action_scores_from_model(self, state). We do this by setting the output of the policy_head to -100 before
        ## computing the softmax.
        x = Conv2D(filters=2,
                   kernel_size=1,
                   data_format="channels_first",
                   padding="same",
                   use_bias=False,
                   activation='linear',
                   kernel_regularizer=regularizers.l2(self.reg_const))(x)
        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(self.output_dim,
                  activation="linear",
                  kernel_regularizer=regularizers.l2(self.reg_const),
                  name=POLICY_HEAD)(x)

        return (x)

    def _build_model(self):
        main_input = Input(shape=self.input_dim, name='main_input')

        x = self.conv_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

        ## YOUR CODE HERE: for each layer in self.hidden_layers after self.hidden_layers[0],
        ## add a residual_layer with the number of filters and the size given in self.hidden_layers[index_layer]
        for index_layer in range(1, len(self.hidden_layers)):
            x = self.residual_layer(x, self.hidden_layers[index_layer]['filters'],
                                    self.hidden_layers[index_layer]['kernel_size'])

        ## YOUR CODE HERE: append the head layer to the output of the last residual layer
        vh = self.value_head(x)
        ## YOUR CODE HERE: append the policy layer to the output of the last residual layer
        ph = self.policy_head(x)

        model = Model(inputs=[main_input], outputs=[vh, ph])

        return model

    def compile(self, learning_rate, momentum, loss_weights={VALUE_HEAD: 0.5, POLICY_HEAD: 0.5}):
        self.model.compile(loss={VALUE_HEAD: 'mean_squared_error', POLICY_HEAD: softmax_cross_entropy_with_logits},
                           optimizer=SGD(learning_rate=learning_rate, momentum=momentum),
                           loss_weights=loss_weights
                           )
        return self.model

REG_CONST = 0.0001

HIDDEN_CNN_LAYERS = [
	{'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	 , {'filters':75, 'kernel_size': (4,4)}
	]

residual_CNN = Residual_CNN(REG_CONST, (1,) + GRID_SHAPE,   GRID_SHAPE[1], HIDDEN_CNN_LAYERS)

plot_model(residual_CNN.model, show_shapes=True)