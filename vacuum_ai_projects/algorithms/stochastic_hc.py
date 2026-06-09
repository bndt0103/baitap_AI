import random
from algorithms.base_search import BaseSearch
from models.node import Node

class StochasticHillClimbing(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        # 1. Current_State = Start
        current = Node(initial_state)
        current.h = self.heuristic(current.state)
        yield {"log": f"INIT: Current_State = {current.state} (h={current.h})", "frontier": [], "explored": []}
        # 2. TRONG KHI (đúng):
        while True:
            # Nếu Current_State == Goal: TRẢ VỀ Current_State
            if current.state.is_goal():
                yield {"log": "GOAL FOUND! Trả về Current_State.", "solution": current}
                return
            better_neighbors = []
            # Sinh tất cả các trạng thái lân cận.
            # Lọc ra tập Better_Neighbors = {Neighbor | Value tốt hơn Current}
            for child in self.get_successors(current):
                child.h = self.heuristic(child.state)
                yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h})", "frontier": [], "explored": []}
                if child.h < current.h:
                    better_neighbors.append(child)
            # NẾU Better_Neighbors RỖNG:
            if not better_neighbors:
                # TRẢ VỀ Current_State (Dừng vì đã đạt cực đại/tiểu cục bộ)
                yield {"log": f"FAILURE: Tập Better_Neighbors RỖNG. Dừng vì đạt Local Optimum.", "solution": None}
                return
            else:
                # NGƯỢC LẠI:
                # Next_State = Chọn ngẫu nhiên một trạng thái từ tập Better_Neighbors
                next_state = random.choice(better_neighbors)
                yield {"log": f"  => TẬP BETTER CÓ {len(better_neighbors)} PHẦN TỬ. Chọn NGẪU NHIÊN Next_State = {next_state.state} (h={next_state.h})", "frontier": [], "explored": []}
                # Current_State = Next_State (Quay lại đầu vòng lặp)
                current = next_state