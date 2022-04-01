class Edge():

    def __init__(self, inNode, outNode, prior, action):
        self.inNode = inNode
        self.outNode = outNode
        self.action = action

        self.stats = {
            'N': 0,
            'W': 0,
            'Q': 0,
            'P': prior,
        }
