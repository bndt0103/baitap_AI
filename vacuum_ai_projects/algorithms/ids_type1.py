from algorithms.base_search import BaseSearch
from models.node import Node

class IDSType1(BaseSearch):
    def search(self, initial_state):
        limit = 0
        while True: # Vòng lặp tăng dần độ sâu (Limit)
            yield {"log": f"\n=== BẮT ĐẦU VÒNG LẶP ITERATIVE DEEPENING VỚI Depth = {limit} ===", "frontier": [], "explored": []}
            start_node = Node(initial_state)
            frontier = [start_node] # Stack (LIFO)
            explored = set()
            cutoff_occurred = False # Cờ đánh dấu có bị giới hạn độ sâu cắt ngang không
            yield {"log": f"INIT: Push Root {start_node.state} to FRONTIER", "frontier": list(frontier), "explored": list(explored)}
            while frontier:
                node = frontier.pop() # LIFO
                parent_info = f"({node.parent.state.robot_pos[0]}, {node.parent.state.robot_pos[1]}|D:{len(node.parent.state.dirts)})" if node.parent else "ROOT"
                action_info = f"{node.action}" if node.action else "START"
                # In thêm thông số Depth vào log để dễ đối chiếu với Limit
                yield {"log": f"POP: {node.state} (Depth: {node.depth}, Action: {action_info}, Parent: {parent_info})", "frontier": list(frontier), "explored": list(explored)}
                # Goal Test SAU KHI POP
                if node.state.is_goal():
                    yield {"log": "GOAL FOUND!", "solution": node}
                    return
                explored.add(node.state)
                # Chỉ sinh node con nếu độ sâu hiện tại còn nhỏ hơn Limit
                if node.depth < limit:
                    successors = self.get_successors(node)
                    for child in reversed(successors):
                        child_parent_info = f"({child.parent.state.robot_pos[0]}, {child.parent.state.robot_pos[1]}|D:{len(child.parent.state.dirts)})"
                        child_action_info = f"{child.action}"
                        yield {"log": f"GENERATE: {child.state} (Depth: {child.depth}, Action: {child_action_info}, Parent: {child_parent_info})", "frontier": list(frontier), "explored": list(explored)}
                        if child.state not in explored and not any(n.state == child.state for n in frontier):
                            frontier.append(child)
                            yield {"log": f"PUSH FRONTIER: {child.state} (Action: {child_action_info})", "frontier": list(frontier), "explored": list(explored)}
                else:
                    cutoff_occurred = True
                    yield {"log": f"    [!] CUTOFF: Node đạt giới hạn độ sâu {limit}, ngừng sinh con nhánh này.", "frontier": list(frontier), "explored": list(explored)}
            # Nếu Frontier rỗng mà ko bị Cutoff -> Đã duyệt sạch toàn bộ cây mà ko có đích
            if not cutoff_occurred:
                yield {"log": f"FAILURE: State space exhausted. Không tìm thấy đích.", "solution": None}
                return
            # Tăng giới hạn độ sâu cho vòng lặp tiếp theo
            limit += 1