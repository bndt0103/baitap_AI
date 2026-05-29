from algorithms.base_search import BaseSearch
from models.node import Node

class IDAStar(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        start_node = Node(initial_state, path_cost=0)
        start_node.h = self.heuristic(start_node.state)
        start_node.f = start_node.path_cost + start_node.h
        
        threshold = start_node.f # Ngưỡng ban đầu (alpha) = f(start)

        while True:
            yield {"log": f"\n=== BẮT ĐẦU IDA* VỚI THRESHOLD (Ngưỡng f) = {threshold} ===", "frontier": [], "explored": []}
            frontier = [start_node] 
            explored = {} 
            next_threshold = float('inf')
            while frontier:
                node = frontier.pop()
                parent_info = f"({node.parent.state.robot_pos[0]},{node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
                yield {"log": f"POP: {node.state} (f={node.f}, g={node.path_cost}, h={node.h}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored.keys())}

                # Cắt tỉa nếu f(n) vượt quá ngưỡng hiện tại
                if node.f > threshold:
                    next_threshold = min(next_threshold, node.f)
                    yield {"log": f"    [!] CUTOFF: f(n)={node.f} > {threshold}. Lưu làm ngưỡng cho vòng sau.", "frontier": list(frontier), "explored": list(explored.keys())}
                    continue
                if node.state.is_goal():
                    yield {"log": "GOAL FOUND!", "solution": node}
                    return
                explored[node.state] = node.path_cost
                for child in reversed(self.get_successors(node)):
                    child.h = self.heuristic(child.state)
                    child.f = child.path_cost + child.h
                    yield {"log": f"GENERATE: {child.state} (f={child.f})", "frontier": list(frontier), "explored": list(explored.keys())}
                    if child.state not in explored or child.path_cost < explored[child.state]:
                        frontier.append(child)
                        yield {"log": f"PUSH FRONTIER: {child.state}", "frontier": list(frontier), "explored": list(explored.keys())}
            if next_threshold == float('inf'):
                yield {"log": "FAILURE: Không tìm thấy đường đi.", "solution": None}
                return
            threshold = next_threshold # Cập nhật ngưỡng mới