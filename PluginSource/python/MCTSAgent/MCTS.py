import numpy as np

from MCTSAgent.Edge import Edge
from MCTSAgent.Node import Node
from connect4.Game import GameState, GRID_SHAPE

EPSILON = 0.2
ALPHA = 0.8


def computeU(N, P, epsilon, nu, action, sumN):
    U = ((1 - epsilon) * P + epsilon * nu[action]) * np.sqrt(sumN) / (1 + N)
    return U


class MCTS():

    def __init__(self, root, cpuct, model, debug=False):
        self.root = root
        # self.nodes_dict is not reset when we change the root of the tree, in order to be able to recover
        # already computed nodes, if the new tree extends to these nodes
        self.nodes_dict = {}
        # As per the cheatsheet: during the selection phase of the MCTS, the tree starts from the root
        # and choses the node which has the maximum value for Q+U, until it reaches a leaf.
        # Q is equal to the mean value of the next state. At the beginning, Q is totally wrong, but after
        # some time, it becomes more and more accurate.
        # U is a function of P (prior proba of selecting the move) and N (number of visits), that increases
        # if the move has not been explored much (ie. if N is small compared to the N of the other moves),
        # or if the prior probability of the action is high. It is also mitigated by cpuct: U = cpuct * function(P, N)
        # Therefore, if cpuct is high, U will keep on being more important than Q, even during the latest
        # stages, and exploration will keep on being favored, rather than exploitation of Q
        self.cpuct = cpuct
        # Model used to evaluate the leaves, each time the selection phase reaches a leaf of the tree.
        # It can be whatever we want: something totally random, a neural network...
        # It just must contain a method predict(self, board) which predicts V (value of the board)
        # and P (probabilies of the actions in this board state)
        self.model = model
        self.debug = debug
        self.addNode(root)

    def simulate(self):
        """Main function of the MCTS: does one simulation, ie. evaluates and expands the most promising leaf of the tree
        - selection: choses the most promising leaf (step 1 of the cheat sheet)
        - evaluate it: evaluates the allowed actions from this leaf, appends the corresponding nodes to the tree (step 2)
        - backfill the tree with the value of the leaf (step 3)
        """

        if self.debug:
            state = GameState.from_id(self.root.state_id, GRID_SHAPE)
            print('ROOT NODE...%s', self.root.state_id)
            print(state)
            print('CURRENT PLAYER...%d', state.currentPlayer)

        ##### MOVE THE LEAF NODE
        ## YOUR CODE HERE: move to a leaf (call one of the functions below)
        leaf, value, done, breadcrumbs = self.moveToLeaf()
        if self.debug:
            state = GameState.from_id(leaf.state_id, GRID_SHAPE)
            print(state)

        ##### EXPAND THE LEAF NODE
        ## YOUR CODE HERE: expand the leaf (call one of the functions below)
        self.expandLeaf(leaf, done)

        ##### BACKFILL THE VALUE THROUGH THE TREE
        ## YOUR CODE HERE: backfill the value (call one of the functions below)
        self.backFill(leaf, value, breadcrumbs)

    def moveToLeaf(self):
        """Goes down the tree until reaches the 'most promising leaf'"""

        if self.debug:
            print('------MOVING TO LEAF------')

        # list of the edges from the root to the leaf
        breadcrumbs = []
        currentNode = self.root

        done = False
        value = 0

        while not currentNode.isLeaf():

            if currentNode == self.root:
                epsilon = EPSILON
                nu = np.random.dirichlet([ALPHA] * len(currentNode.edges))
            else:
                epsilon = 0
                nu = [0] * len(currentNode.edges)
            ## YOUR CODE HERE: find the best next node, ie. the one which edge has the biggest Q + U
            ## Hint: each edge of the current node has Q = edge.stats['Q'], P = edge.stats['P'] and N = edge.stats['N']
            ## => you have to find the edge which maximizes Q+U, because that one is pointing out to the best next node
            ## NB: currentNode.edges returns a list of (action, edge), you have to iterate over that list
            ## For each edge: Q is directly found above, U is more complex, you have to compute it
            ## 1) see the comment in __init__(): U = self.cpuct * function(P, N)
            ## 2) basically, function(P, N) = P * sqrt(sum(N)) / (1+N), but we add
            ##   randomness at the root node, so function(P, N) becomes:
            ##   ((1-epsilon) * P + epsilon * nu[action]) * sqrt(sum(N)) / (1+N), where sum(N) is the sum of N of the edges of currentNode

            sumN = 0

            for action, edge in currentNode.edges:
                sumN += edge.stats['N']

            maxQU = -1
            for idx, (action, edge) in enumerate(currentNode.edges):
                Q = edge.stats['Q']
                P = edge.stats['P']
                N = edge.stats['N']
                U = computeU(N, P, epsilon, nu, idx, sumN)
                if Q + U > maxQU:
                    maxQU = Q + U
                    bestEdge = edge

            # At the very beginning, the tree is a single node, ie. a single leaf, and we don't enter into
            # this loop. Therefore, in that case,  currentNode keeps on being the root node, value, done
            # keep the values they have before the loop (ie. 0 and False), and breadcrumbs keeps on being empty
            state = GameState.from_id(currentNode.state_id, GRID_SHAPE)
            # YOUR CODE HERE: run the action corresponding to the best edge
            _, value, done = state.takeAction(bestEdge.action)

            ## YOUR CODE HERE: append the selected edge to breadcrumbs
            breadcrumbs.append(bestEdge)
            ## YOUR CODE HERE: the outNode of the selected edge
            currentNode = bestEdge.outNode

        return currentNode, value, done, breadcrumbs

    def expandLeaf(self, leaf, done):

        if self.debug:
            print('------EVALUATING LEAF------')

        if not done:

            state = GameState.from_id(leaf.state_id, GRID_SHAPE)
            current_proba_victory, action_scores, allowedActions = self.evaluate_action_scores_from_model(state)
            if self.debug:
                print('CURRENT PROBA VICTORY FOR %d: %f', state.currentPlayer, current_proba_victory)

            ## YOUR CODE HERE: for all the actions allowed in allowedActions:
            ## - execute the action, which leads to a new state 'newState'.
            ## If the node corresponding to 'newState' is not in nodes_dict, append it using the function self.addNode(node)
            ## Else fetch it from nodes_dict
            ## Then create the Edge linking leaf to that node, with prior = action_scores[action], and add it to leaf.edges
            ## (which is the list of the edges of leaf)

            for action in range(len(allowedActions)):
                if allowedActions[action]:
                    newState = state.takeAction(action)[0]
                    node = Node(newState)
                    if node in self.nodes_dict:
                        node = self.nodes_dict[node.state_id]
                    else:
                        self.addNode(node)

                    leaf.edges.append((action, Edge(leaf, node, action_scores[action], action)))

    def evaluate_action_scores_from_model(self, state):
        # state.board has shape (6,7), so it can be considered as a 1-layer image of shape:
        # - either (1,6,7) if channel layer first
        # - or (6,7,1) if channel last as usually done with Keras
        # Plus Keras needs a batch of inputs => we add an additional encapsulating array
        # => resulting shape is (1,1,6,7)
        inputToModel = np.array([[state.get_board_for_neural_network()]], dtype=np.int8)

        ## YOUR CODE HERE: let self.model do its predictions
        preds = self.model.predict(inputToModel)
        # preds[0] is an array of shape (1,1): the input was a batch of 1 board, and the neural network
        # predicts one value per board, between -1 and 1 because of the tanh activation for this head
        current_proba_victory = preds[0][0, 0]
        # preds[1] is an array of shape (1,7): the input was a batch of 1 board, and the neural network
        # predicts 7 values per board (the values for each possible action - more precisely a linear value
        # before transformation to a percentage via the softmax)
        logits = preds[1][0]

        # Forbidden actions must receive a probability equal to 0, therefore we force the output of the
        # neural network to -100 for them (so that the softmax would transform them to 0)
        allowedActions = state.allowedActions()
        forbiddenActions = [not (isallowed) for isallowed in allowedActions]
        logits[forbiddenActions] = -100

        # SOFTMAX
        odds = np.exp(logits)
        action_scores = odds / np.sum(odds)

        return ((current_proba_victory, action_scores, allowedActions))

    def backFill(self, leaf, value, breadcrumbs):
        """breadcrumbs contains the list of edges which led from the root node to the leaf.
        In this function, we iterate over that list, in oder to increment N (number of visits)
        of these edges, and also in order to update their W (total value of the next state)
        and their Q = W / N
        """

        ## Warning: there is a tricky trap with W: we want to add value or -value, depending on the
        ## player of the edge.
        ## Explanation:
        ## Let's say that the player at the leaf is 'leafPlayer': 'value' contains the value of the
        ## leaf according to 'leafPlayer'
        ## => during the iteration over the edges contained into breadcrumbs:
        ##    - if the player of edge.inNode is equal to 'leafPlayer': W = W + value
        ##		- else: W = W - value

        if self.debug:
            print('------DOING BACKFILL------')

        leafPlayer = GameState.current_player_from_id(leaf.state_id)

        ## YOUR CODE HERE:
        ## for each edge of breadcrumbs:
        ## - N is equal to edge.stats['N']. Increment it.
        ## - W is equal to edge.stats['W']. Add value or -value, as per the warning above.
        ##    You can get the player of edge.inNode with GameState.current_player_from_id(edge.inNode.state_id)
        ## - update edge.stats['Q'], as per the formula Q = W / N

        for edge in breadcrumbs:
            edge.stats['N'] += 1
            if leafPlayer == GameState.current_player_from_id(edge.inNode.state_id):
                edge.stats['W'] += value
            else:
                edge.stats['W'] -= value
            edge.stats['Q'] = edge.stats['W'] / edge.stats['N']

    def addNode(self, node):
        self.nodes_dict[node.state_id] = node
