from algorithms.base_search import BaseSearch
from models.node import Node


class DFSType1(BaseSearch):
    def search(self, initial_state):
        start_node = Node(initial_state)
        frontier = [start_node]
        explored = set()
        yield {"log": f"INIT: Push Root {start_node.state} to FRONTIER", "frontier": list(frontier),
               "explored": list(explored)}
        while frontier:
            node = frontier.pop()
            parent_info = (f"({node.parent.state.robot_pos[0]}, "
                           f"{node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})") if node.parent else "ROOT"
            action_info = f"{node.action}" if node.action else "START"
            yield {"log": f"POP: {node.state} (Action: {action_info}, Parent: {parent_info})",
                   "frontier": list(frontier), "explored": list(explored)}
            if node.state.is_goal():
                yield {"log": "GOAL FOUND!", "solution": node}
                return
            explored.add(node.state)
            successors = self.get_successors(node)
            for child in reversed(successors):
                child_parent_info = (f"({child.parent.state.robot_pos[0]}, "
                                     f"{child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})")
                child_action_info = f"{child.action}"
                yield {"log": f"GENERATE: {child.state} (Action: {child_action_info}, Parent: {child_parent_info})",
                       "frontier": list(frontier), "explored": list(explored)}
                if child.state not in explored and not any(n.state == child.state for n in frontier):
                    frontier.append(child)
                    yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info})",
                           "frontier": list(frontier), "explored": list(explored)}
        yield {"log": "FAILURE: No solution found.", "solution": None}