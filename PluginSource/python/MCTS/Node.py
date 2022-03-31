class Node():

    def __init__(self, state):
        self.state_id = state.id
        self.edges = []

    def isLeaf(self):
        if len(self.edges) > 0:
            return False
        else:
            return True
