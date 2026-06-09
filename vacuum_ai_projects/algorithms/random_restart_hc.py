import random
from algorithms.base_search import BaseSearch
from models.node import Node

class RandomRestartHillClimbing(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        # 1. Khởi tạo: Số lần chạy lại tối đa
        MAX_RESTART = 10 

        # 2. CHO i = 1 đến MAX_RESTART:
        for i in range(1, MAX_RESTART + 1):
            yield {"log": f"\n=== [LƯỢT {i}/{MAX_RESTART}] KHỞI TẠO LẠI TỪ ĐẦU (RESTART) ===", "frontier": [], "explored": []}
            current = Node(initial_state)
            current.h = self.heuristic(current.state)
            yield {"log": f"INIT: Current_State = {current.state} (h={current.h})", "frontier": [], "explored": []}

            # TRONG KHI (đúng):
            while True:
                # NẾU Current_State == Goal:
                if current.state.is_goal():
                    yield {"log": f"GOAL FOUND (Tại lượt chạy thứ {i})! TRẢ VỀ Current_State.", "solution": current}
                    return
                # Sinh tất cả các trạng thái lân cận của Current_State
                neighbors = self.get_successors(current)
                for child in neighbors:
                    child.h = self.heuristic(child.state)
                    yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h})", "frontier": [], "explored": []}

                # Lọc ra tập Better_Neighbors = {Neighbor | Value(Neighbor) tốt hơn Value(Current_State)}
                better_neighbors = [child for child in neighbors if child.h < current.h]

                # NẾU Better_Neighbors RỖNG:
                if not better_neighbors:
                    yield {"log": f"  [!] Better_Neighbors RỖNG. Thoát vòng lặp TRONG KHI (Lượt {i} bị kẹt, nhảy sang lượt tiếp theo).", "solution": None}
                    break # Thoát vòng lặp While, nhảy sang vòng lặp For (Lượt i tiếp theo)
                # NGƯỢC LẠI:
                # Next_State = Chọn trạng thái tốt nhất từ tập Better_Neighbors
                min_h = min(child.h for child in better_neighbors)
                best_neighbors = [child for child in better_neighbors if child.h == min_h]
                # CHỌN NGẪU NHIÊN để tạo con đường khác biệt cho mỗi lần Restart
                next_state = random.choice(best_neighbors)
                yield {"log": f"  => TÌM THẤY {len(best_neighbors)} NEIGHBOR TỐT NHẤT (h={min_h}). CHỌN RANDOM Next_State = {next_state.state}", "frontier": [], "explored": []}
                current = next_state

        # 3. TRẢ VỀ "Thất bại" // Chạy hết sạch MAX_RESTART lượt mà không chạm được Goal
        yield {"log": f"FAILURE: Chạy hết sạch {MAX_RESTART} lượt mà không chạm được Goal. Không tìm thấy đường đi.", "solution": None}