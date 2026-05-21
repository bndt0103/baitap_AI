class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def get_path(self):
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]