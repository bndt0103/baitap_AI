from algorithms.base_search import BaseSearch
from models.node import Node

class GreedySearch(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        # Tính khoảng cách Manhattan tới cục rác GẦN NHẤT
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1
    def search(self, initial_state):
        # 1. Khởi tạo tập FRONTIER = {Start}, Tính h(Start)
        start_node = Node(initial_state)
        start_node.h = self.heuristic(start_node.state)
        frontier = [start_node]
        # 2. Khởi tạo tập REACHED = {}
        explored = set() 
        yield {"log": f"INIT: Push Root {start_node.state} (h={start_node.h}) to FRONTIER", "frontier": list(frontier), "explored": list(explored)}
        # 3. TRONG KHI (FRONTIER không rỗng):
        while frontier:
            # 3.a. Chọn trạng thái n từ FRONTIER có h(n) nhỏ nhất
            min_idx = 0
            for i in range(1, len(frontier)):
                if frontier[i].h < frontier[min_idx].h:
                    min_idx = i
            node = frontier.pop(min_idx)
            parent_info = f"({node.parent.state.robot_pos[0]}, {node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
            action_info = f"{node.action}" if node.action else "START"
            yield {"log": f"POP: {node.state} (h={node.h}, Action: {action_info}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored)}
            # 3.b. NẾU n == Goal
            if node.state.is_goal():
                yield {"log": "GOAL FOUND!", "solution": node}
                return
            # 3.c. Loại bỏ n khỏi FRONTIER và thêm n vào REACHED
            explored.add(node.state)
            # 3.d. Với mỗi trạng thái m kề với n:
            for child in self.get_successors(node):
                # Tính giá trị heuristic h(m)
                child.h = self.heuristic(child.state)
                child_parent_info = f"({child.parent.state.robot_pos[0]}, {child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})"
                child_action_info = f"{child.action}"
                yield {"log": f"GENERATE: {child.state} (h={child.h}, Action: {child_action_info}, Parent: {child_parent_info})", "frontier": list(frontier), "explored": list(explored)}
                in_explored = child.state in explored
                in_frontier = any(n.state == child.state for n in frontier)
                # 3.d.i. NẾU m chưa có trong cả FRONTIER và REACHED
                if not in_explored and not in_frontier:
                    frontier.append(child)
                    yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info}, h={child.h})", "frontier": list(frontier), "explored": list(explored)}
                # 3.d.ii. NẾU m đã có trong FRONTIER hoặc REACHED: Bỏ qua
                else:
                    yield {"log": f"    [!] Bỏ qua {child.state} vì đã nằm trong Frontier hoặc Reached.", "frontier": list(frontier), "explored": list(explored)}
        # 4. TRẢ VỀ "Thất bại"
        yield {"log": "FAILURE: No solution found.", "solution": None}