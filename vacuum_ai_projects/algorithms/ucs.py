from algorithms.base_search import BaseSearch
from models.node import Node

class UCS(BaseSearch):
    def search(self, initial_state):
        start_node = Node(initial_state, path_cost=0)
        frontier = [start_node] # Dùng list để tự tìm min cost rút ra
        explored = set()          
        yield {"log": f"INIT: Push Root {start_node.state} to FRONTIER", "frontier": list(frontier), "explored": list(explored)}
        while frontier:
            min_idx = 0
            for i in range(1, len(frontier)):
                if frontier[i].path_cost < frontier[min_idx].path_cost:
                    min_idx = i
            node = frontier.pop(min_idx)
            parent_info = f"({node.parent.state.robot_pos[0]}, {node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
            action_info = f"{node.action}" if node.action else "START"
            yield {"log": f"POP: {node.state} (Cost: {node.path_cost}, Action: {action_info}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored)}
            # Goal test sau khi pop
            if node.state.is_goal():
                yield {"log": "GOAL FOUND!", "solution": node}
                return
            explored.add(node.state)
            for child in self.get_successors(node):
                #get_successors ở BaseSearch đã ngầm tăng child.path_cost = node.path_cost + 1
                child_parent_info = f"({child.parent.state.robot_pos[0]}, {child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})"
                child_action_info = f"{child.action}"
                yield {"log": f"GENERATE: {child.state} (Cost: {child.path_cost}, Action: {child_action_info}, Parent: {child_parent_info})", "frontier": list(frontier), "explored": list(explored)}
                # Kiểm tra trạng thái trong Explored và Frontier
                in_explored = child.state in explored
                in_frontier = False
                frontier_idx = -1
                for idx, n in enumerate(frontier):
                    if n.state == child.state:
                        in_frontier = True
                        frontier_idx = idx
                        break
                # Nếu chưa từng xuất hiện thì push vào
                if not in_explored and not in_frontier:
                    frontier.append(child)
                    yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info})", "frontier": list(frontier), "explored": list(explored)}
                # Nếu đã nằm trong Frontier nhưng cost thấp hơn thì thay thế (ghi đè)
                elif in_frontier and frontier[frontier_idx].path_cost > child.path_cost:
                    frontier[frontier_idx] = child
                    yield {"log": f"    [!] REPLACE FRONTIER: {child.state} vừa được cập nhật với Cost thấp hơn ({child.path_cost})", "frontier": list(frontier), "explored": list(explored)}
        yield {"log": "FAILURE: No solution found.", "solution": None}