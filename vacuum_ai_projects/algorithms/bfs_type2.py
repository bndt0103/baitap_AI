from collections import deque
from algorithms.base_search import BaseSearch
from models.node import Node


class BFSType2(BaseSearch):
    def search(self, initial_state):
        start_node = Node(initial_state)
        if start_node.state.is_goal():
            yield {"log": "GOAL FOUND AT ROOT!", "solution": start_node}
            return
        frontier = deque([start_node])
        explored = set()
        yield {"log": f"INIT: Push Root {start_node.state} to FRONTIER", "frontier": list(frontier),
               "explored": list(explored)}
        while frontier:
            node = frontier.popleft()
            parent_info = (f"({node.parent.state.robot_pos[0]}, "
                           f"{node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})") if node.parent else "ROOT"
            action_info = f"{node.action}" if node.action else "START"
            yield {"log": f"POP: {node.state} (Action: {action_info}, Parent: {parent_info})",
                   "frontier": list(frontier), "explored": list(explored)}
            explored.add(node.state)
            for child in self.get_successors(node):
                child_parent_info = (f"({child.parent.state.robot_pos[0]}, "
                                     f"{child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})")
                child_action_info = f"{child.action}"
                yield {"log": f"GENERATE: {child.state} (Action: {child_action_info}, Parent: {child_parent_info})",
                       "frontier": list(frontier), "explored": list(explored)}
                if child.state not in explored and not any(n.state == child.state for n in frontier):
                    if child.state.is_goal():
                        yield {"log": f"GOAL FOUND DURING GENERATION: {child.state}", "solution": child}
                        return
                    frontier.append(child)
                    yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info})",
                           "frontier": list(frontier), "explored": list(explored)}
        yield {"log": "FAILURE: No solution found.", "solution": None}
