import math
import random
from algorithms.base_search import BaseSearch
from models.node import Node

class SimulatedAnnealing(BaseSearch):
    def heuristic(self, state):
        if not state.dirts: return 0
        min_dist = min(abs(state.robot_pos[0] - d[0]) + abs(state.robot_pos[1] - d[1]) for d in state.dirts)
        return min_dist + len(state.dirts) - 1

    def search(self, initial_state):
        current_state = Node(initial_state)
        current_state.h = self.heuristic(current_state.state)
        T0 = 100.0       
        Tmin = 0.01      
        alpha = 0.95     
        T = T0
        yield {"log": f"INIT: Current State = {current_state.state} (h={current_state.h}). T0={T}, Tmin={Tmin}, alpha={alpha}", "frontier": [], "explored": []}
        while T > Tmin:
            if current_state.state.is_goal():
                yield {"log": f"GOAL FOUND! Tìm thấy đích tại Nhiệt độ T = {T:.4f}", "solution": current_state}
                return
            neighbors = self.get_successors(current_state)
            if not neighbors:
                yield {"log": "FAILURE: Không có trạng thái lân cận để đi.", "solution": None}
                return
            next_state = random.choice(neighbors)
            next_state.h = self.heuristic(next_state.state)
            yield {"log": f"GENERATE Random Neighbor: {next_state.state} (h={next_state.h})", "frontier": [], "explored": []}
            delta = next_state.h - current_state.h
            if delta < 0:
                yield {"log": f"  => CHẤP NHẬN: Nước đi TỐT HƠN (Delta = {delta} < 0). Current = Next.", "frontier": [], "explored": []}
                current_state = next_state
            else:
                p = math.exp(-delta / T)
                rand_val = random.uniform(0, 1) 
                if rand_val < p:
                    yield {"log": f"  => CHẤP NHẬN RỦI RO: Nước đi TỆ HƠN. Xác suất p = {p:.4f}, Random = {rand_val:.4f} < p.", "frontier": [], "explored": []}
                    current_state = next_state
                else:
                    yield {"log": f"  => TỪ CHỐI: Nước đi TỆ HƠN. Xác suất p = {p:.4f}, Random = {rand_val:.4f} >= p.", "frontier": [], "explored": []}
            T = alpha * T
        yield {"log": f"FAILURE: Nhiệt độ đã giảm xuống T_min ({Tmin}) mà không chạm Goal.", "solution": None}