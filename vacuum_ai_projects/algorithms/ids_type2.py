from algorithms.base_search import BaseSearch
from models.node import Node

class IDSType2(BaseSearch):
    def search(self, initial_state):
        limit = 0
        while True:
            yield {"log": f"\n=== BẮT ĐẦU VÒNG LẶP ITERATIVE DEEPENING VỚI Depth  = {limit} ===", "frontier": [], "explored": []}
            start_node = Node(initial_state)
            # Goal Test ROOT
            if start_node.state.is_goal():
                yield {"log": "GOAL FOUND AT ROOT!", "solution": start_node}
                return
            frontier = [start_node]
            explored = set()
            cutoff_occurred = False
            yield {"log": f"INIT: Push Root {start_node.state} to FRONTIER", "frontier": list(frontier), "explored": list(explored)}
            while frontier:
                node = frontier.pop()
                parent_info = f"({node.parent.state.robot_pos[0]}, {node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
                action_info = f"{node.action}" if node.action else "START"
                yield {"log": f"POP: {node.state} (Depth: {node.depth}, Action: {action_info}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored)}
                explored.add(node.state)
                if node.depth < limit:
                    successors = self.get_successors(node)
                    for child in reversed(successors):
                        child_parent_info = f"({child.parent.state.robot_pos[0]}, {child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})"
                        child_action_info = f"{child.action}"
                        yield {"log": f"GENERATE: {child.state} (Depth: {child.depth}, Action: {child_action_info}, Parent: {child_parent_info})", "frontier": list(frontier), "explored": list(explored)}
                        if child.state not in explored and not any(n.state == child.state for n in frontier):
                            # Goal test ngay lúc sinh ra
                            if child.state.is_goal():
                                yield {"log": f"GOAL FOUND DURING GENERATION: {child.state}", "solution": child}
                                return
                            frontier.append(child)
                            yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info})", "frontier": list(frontier), "explored": list(explored)}
                else:
                    cutoff_occurred = True
                    yield {"log": f"    [!] CUTOFF: Node đạt giới hạn độ sâu {limit}, ngừng sinh con nhánh này.", "frontier": list(frontier), "explored": list(explored)}
            if not cutoff_occurred:
                yield {"log": f"FAILURE: State space exhausted. Không tìm thấy đích.", "solution": None}
                return

            limit += 1