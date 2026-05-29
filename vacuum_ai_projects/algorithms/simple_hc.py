from algorithms.base_search import BaseSearch
from models.node import Node

class SimpleHillClimbing(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        # 1. Current_State = Start
        current = Node(initial_state)
        current.h = self.heuristic(current.state)
        yield {"log": f"INIT: Current_State = {current.state} (h={current.h})", "frontier": [current], "explored": []}
        # 2. TRONG KHI (đúng):
        while True:
            # Nếu Current_State == Goal: TRẢ VỀ Current_State
            if current.state.is_goal():
                yield {"log": "GOAL FOUND! Trả về Current_State.", "solution": current}
                return
            found_better = False
            # Sinh các trạng thái lân cận của Current_State.
            for child in self.get_successors(current):
                child.h = self.heuristic(child.state)
                yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h})", "frontier": [current], "explored": []}
                # Tìm thấy Next_State ĐẦU TIÊN có Value tốt hơn (h nhỏ hơn)
                if child.h < current.h:
                    yield {"log": f"  => TÌM THẤY NEIGHBOR ĐẦU TIÊN TỐT HƠN! Current_State = Next_State", "frontier": [current], "explored": []}
                    current = child
                    found_better = True
                    break # Lập tức thoát vòng lặp sinh, tiếp tục vòng lặp While (Quay lại bước 2)
            # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn:
            if not found_better:
                yield {"log": f"FAILURE: Đã duyệt hết lân cận. Dừng vì đạt cực đại (tiểu) cục bộ.", "solution": None}
                return