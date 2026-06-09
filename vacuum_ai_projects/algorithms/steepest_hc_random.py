import random
from algorithms.base_search import BaseSearch
from models.node import Node

class SteepestAscentRandomHC(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        current = Node(initial_state)
        current.h = self.heuristic(current.state)
        yield {"log": f"INIT: Current_State = {current.state} (h={current.h})", "frontier": [], "explored": []}
        sideways_moves = 0
        max_sideways = 100 # Giới hạn 100 bước đi ngang liên tiếp để chống lặp vô hạn

        while True:
            if current.state.is_goal():
                yield {"log": "GOAL FOUND! Trả về Current_State.", "solution": current}
                return
            neighbors = self.get_successors(current)
            if not neighbors:
                yield {"log": "FAILURE: Không có lân cận. Dừng.", "solution": None}
                return
            # Tính h cho tất cả các trạng thái lân cận
            for child in neighbors:
                child.h = self.heuristic(child.state)
                yield {"log": f"GENERATE Neighbor: {child.state} (h={child.h})", "frontier": [], "explored": []}
            # 1. Tìm giá trị h nhỏ nhất trong số các lân cận
            min_h = min(child.h for child in neighbors)

            # 2. Gom TẤT CẢ các neighbor đạt được giá trị min_h này
            best_neighbors = [child for child in neighbors if child.h == min_h]

            # 3. NẾU h nhỏ nhất lại LỚN HƠN h hiện tại -> Kẹt ở đáy -> DỪNG
            if min_h > current.h:
                yield {"log": f"FAILURE: Neighbor tốt nhất (h={min_h}) LỚN HƠN Current (h={current.h}). Dừng vì không có đường đi.", "solution": None}
                return

            # 4. Kiểm soát số bước đi ngang để chống lặp vô hạn
            if min_h == current.h:
                sideways_moves += 1
                if sideways_moves > max_sideways:
                    yield {"log": f"FAILURE: Đã đi ngang {max_sideways} bước liên tiếp mà không tiến triển. Dừng để chống lặp vô hạn.", "solution": None}
                    return
            else:
                # Nếu tìm được h thực sự nhỏ hơn, reset lại bộ đếm đi ngang
                sideways_moves = 0 

            # 5. CHỌN NGẪU NHIÊN 1 trong số các neighbor tốt nhất
            chosen_neighbor = random.choice(best_neighbors)
            yield {"log": f"  => TÌM THẤY {len(best_neighbors)} NEIGHBOR CÙNG ĐẠT h MIN ({min_h}). CHỌN RANDOM: {chosen_neighbor.state}", "frontier": [], "explored": []}
            
            # Gán trạng thái mới và lặp lại
            current = chosen_neighbor