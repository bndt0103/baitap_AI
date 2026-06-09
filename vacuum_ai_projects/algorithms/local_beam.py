import random
from algorithms.base_search import BaseSearch
from models.node import Node

class LocalBeamSearch(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        k = 2 # Số lượng trạng thái trong chùm
        start_node = Node(initial_state)
        start_node.h = self.heuristic(start_node.state)
        
        # 1. KHỞI TẠO: Sinh ngẫu nhiên k trạng thái từ Start
        initial_neighbors = self.get_successors(start_node)
        for child in initial_neighbors:
            child.h = self.heuristic(child.state)
        if not initial_neighbors:
            yield {"log": "FAILURE: Start không có lân cận nào để khởi tạo chùm.", "solution": None}
            return
        num_to_pick = min(k, len(initial_neighbors))
        current_state_set = random.sample(initial_neighbors, num_to_pick)
        yield {"log": f"INIT: Khởi tạo chùm (k={k}) bằng {num_to_pick} lân cận ngẫu nhiên từ Start.", "frontier": [], "explored": []}

        # 2. TRONG KHI (đúng):
        while True:
            neighbor_states = []
            # 2.1 SINH TRẠNG THÁI LÂN CẬN 
            for state_node in current_state_set:
                for child in self.get_successors(state_node):
                    child.h = self.heuristic(child.state)
                    neighbor_states.append(child)   
                    yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h}) từ cha {state_node.state}", "frontier": [], "explored": []}

            # 2.2 KIỂM TRA ĐÍCH
            for neighbor in neighbor_states:
                if neighbor.state.is_goal():
                    yield {"log": f"GOAL FOUND! Trạng thái {neighbor.state} là đích.", "solution": neighbor}
                    return
            if not neighbor_states:
                yield {"log": "FAILURE: Tập Neighbor_States rỗng. Không tìm thấy đường đi.", "solution": None}
                return

            # 2.3 LỰA CHỌN CHÙM
            # Sắp xếp Neighbor_States theo thứ tự giá trị h tốt dần
            neighbor_states.sort(key=lambda n: n.h)
            # Lấy k trạng thái tốt nhất
            current_state_set = neighbor_states[:k]
            best_logs = ", ".join([f"{n.state}(h={n.h})" for n in current_state_set])
            yield {"log": f"  => LỰA CHỌN CHÙM: Chọn ra {len(current_state_set)} trạng thái tốt nhất: {best_logs}", "frontier": [], "explored": []}