from algorithms.base_search import BaseSearch
from models.node import Node

class SteepestAscentHillClimbing(BaseSearch):
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
            # Sinh TẤT CẢ các trạng thái lân cận của Current_State
            neighbors = self.get_successors(current)
            if not neighbors:
                yield {"log": f"FAILURE: Không có lân cận. Dừng.", "solution": None}
                return  
            # Khởi tạo Best_Neighbor tạm thời là phần tử đầu tiên
            best_neighbor = neighbors[0]
            best_neighbor.h = self.heuristic(best_neighbor.state)
            yield {"log": f"GENERATE Neighbor: {best_neighbor.state} (h={best_neighbor.h})", "frontier": [], "explored": []}
            # Chọn ra trạng thái lân cận tốt nhất là Best_Neighbor
            for i in range(1, len(neighbors)):
                child = neighbors[i]
                child.h = self.heuristic(child.state)
                yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h})", "frontier": [], "explored": []}
                if child.h < best_neighbor.h:
                    best_neighbor = child
            # NẾU Value(Best_Neighbor) tốt hơn Value(Current_State)
            if best_neighbor.h < current.h:
                yield {"log": f"  => CHỌN NEIGHBOR TỐT NHẤT: {best_neighbor.state} (h={best_neighbor.h}). Quay lại đầu vòng lặp.", "frontier": [], "explored": []}
                # Current_State = Best_Neighbor (Quay lại đầu vòng lặp)
                current = best_neighbor
            else:
                # NGƯỢC LẠI: TRẢ VỀ Current_State (Dừng vì đã đạt cực đại/tiểu cục bộ)
                yield {"log": f"FAILURE: Neighbor tốt nhất (h={best_neighbor.h}) KHÔNG vượt qua Current (h={current.h}). Dừng vì kẹt ở Local Optimum.", "solution": None}
                return