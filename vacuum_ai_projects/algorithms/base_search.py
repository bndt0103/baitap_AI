from models.node import Node
from models.state import State

ACTIONS = {
    "UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)
}

class BaseSearch:
    def __init__(self, grid_rows, grid_cols, obstacles):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.obstacles = set(obstacles)

    def get_successors(self, node):
        successors = []
        r, c = node.state.robot_pos
        for action_name, (dr, dc) in ACTIONS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.grid_rows and 0 <= nc < self.grid_cols:
                if (nr, nc) not in self.obstacles:
                    new_dirts = node.state.dirts - {(nr, nc)}
                    new_state = State((nr, nc), new_dirts)
                    new_node = Node(new_state, node, action_name, node.path_cost + 1)
                    successors.append(new_node)
        return successors