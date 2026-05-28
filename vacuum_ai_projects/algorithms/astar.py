from algorithms.base_search import BaseSearch
from models.node import Node

class AStar(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        # 1. Khởi tạo tập FRONTIER = {Start} với f(Start) = g(Start) + h(Start)
        start_node = Node(initial_state, path_cost=0)
        start_node.h = self.heuristic(start_node.state)
        start_node.f = start_node.path_cost + start_node.h
        frontier = [start_node]
        # 2. Khởi tạo tập REACHED = {} (Dùng Dictionary để lưu kèm g_cost)
        explored = {} 
        yield {"log": f"INIT: Push Root {start_node.state} (f={start_node.f}, g={start_node.path_cost}, h={start_node.h}) to FRONTIER", "frontier": list(frontier), "explored": list(explored.keys())}
        # 3. TRONG KHI (FRONTIER không rỗng):
        while frontier:
            # 3.a. Chọn trạng thái n từ FRONTIER có f(n) nhỏ nhất
            min_idx = 0
            for i in range(1, len(frontier)):
                if frontier[i].f < frontier[min_idx].f:
                    min_idx = i
            node = frontier.pop(min_idx)
            parent_info = f"({node.parent.state.robot_pos[0]}, {node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
            action_info = f"{node.action}" if node.action else "START"
            yield {"log": f"POP: {node.state} (f={node.f}, g={node.path_cost}, h={node.h}, Action: {action_info}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored.keys())}
            # 3.b. NẾU n == Goal
            if node.state.is_goal():
                yield {"log": "GOAL FOUND!", "solution": node}
                return
            # 3.c. Loại bỏ n khỏi FRONTIER và thêm n vào REACHED
            explored[node.state] = node.path_cost
            # 3.d. Với mỗi trạng thái m kề với n:
            for child in self.get_successors(node):
                # i. Tính toán chi phí thực tế mới (get_successors đã ngầm gán g_new(m) = g(n) + 1)
                child.h = self.heuristic(child.state)
                child.f = child.path_cost + child.h
                child_parent_info = f"({child.parent.state.robot_pos[0]}, {child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})"
                child_action_info = f"{child.action}"
                yield {"log": f"GENERATE: {child.state} (f={child.f}, g={child.path_cost}, h={child.h}, Action: {child_action_info}, Parent: {child_parent_info})", "frontier": list(frontier), "explored": list(explored.keys())}
                in_explored = child.state in explored
                frontier_idx = -1
                for idx, n in enumerate(frontier):
                    if n.state == child.state:
                        frontier_idx = idx
                        break
                in_frontier = frontier_idx != -1
                # ii. NẾU m đã nằm trong REACHED
                if in_explored:
                    if child.path_cost >= explored[child.state]:
                        yield {"log": f"    [!] Bỏ qua {child.state} vì đã có trong Reached với g_cost (tệ hơn).", "frontier": list(frontier), "explored": list(explored.keys())}
                        continue
                    else:
                        # Xóa m khỏi REACHED, đưa m quay lại FRONTIER để xét tiếp
                        del explored[child.state]
                        frontier.append(child)
                        yield {"log": f"    [!] PHỤC HỒI: {child.state} tìm được đường đi ngắn hơn (g={child.path_cost}). Xóa khỏi Reached, đưa lại vào Frontier.", "frontier": list(frontier), "explored": list(explored.keys())}
                        continue
                # iii. NẾU m đã nằm trong FRONTIER
                if in_frontier:
                    if child.path_cost < frontier[frontier_idx].path_cost:
                        frontier[frontier_idx] = child
                        yield {"log": f"    [!] CẬP NHẬT FRONTIER: {child.state} tìm được đường đi ngắn hơn (g={child.path_cost}, f={child.f}).", "frontier": list(frontier), "explored": list(explored.keys())}
                    else:
                        yield {"log": f"    [!] Bỏ qua {child.state} vì đã có trong Frontier với g_cost tốt hơn.", "frontier": list(frontier), "explored": list(explored.keys())}
                    continue
                # iv. NẾU m chưa có mặt trong cả FRONTIER và REACHED
                frontier.append(child)
                yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info}, f={child.f})", "frontier": list(frontier), "explored": list(explored.keys())}
        # 4. TRẢ VỀ "Thất bại"
        yield {"log": "FAILURE: No solution found.", "solution": None}