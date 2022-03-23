# Imports
# Import keras
from keras.layers import Dense, concatenate, add
from keras.models import Model
from AiInput import AiInput, ChoiceAiOutput


class GenericNetwork:
    def __init__(self, inputs_branches, output_branches, layers_dim=(2, 64), residual=1, activation="linear"):
        self.inputs_branches = inputs_branches
        self.output_branches = output_branches
        self.layersDim = layers_dim
        self.residual = residual
        self.activation = activation

        self.model = self._build()

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
