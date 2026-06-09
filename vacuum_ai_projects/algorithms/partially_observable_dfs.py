from algorithms.base_search import BaseSearch
from models.node import Node
from models.state import State
from collections import deque


class PartiallyObservableDFS(BaseSearch):
    """Partially Observable Search - Tìm kiếm với CẢM BIẾN CỤC BỘ.
    Robot biết: có rác tại ô hiện tại? + tường ở 4 hướng? Nhưng KHÔNG biết vị trí."""

    MAX_STEPS = 500

    def get_percept(self, s):
        r, c = s.robot_pos
        return ((r,c) in s.dirts,
                r == 0 or (r-1,c) in self.obstacles,
                r == self.grid_rows-1 or (r+1,c) in self.obstacles,
                c == 0 or (r,c-1) in self.obstacles,
                c == self.grid_cols-1 or (r,c+1) in self.obstacles)

    def simulate(self, state, action):
        r, c = state.robot_pos
        dirts = set(state.dirts)
        if action == "UP" and r > 0 and (r-1,c) not in self.obstacles: r -= 1
        elif action == "DOWN" and r < self.grid_rows-1 and (r+1,c) not in self.obstacles: r += 1
        elif action == "LEFT" and c > 0 and (r,c-1) not in self.obstacles: c -= 1
        elif action == "RIGHT" and c < self.grid_cols-1 and (r,c+1) not in self.obstacles: c += 1
        elif action == "SUCK": dirts.discard((r,c))
        return State((r,c), frozenset(dirts))

    def _choose_action(self, actual, belief, free):
        if actual.robot_pos in actual.dirts: return "SUCK"
        if len(belief) <= 1 and actual.dirts:
            q, vis = deque([(actual.robot_pos, [])]), {actual.robot_pos}
            while q:
                (r,c), path = q.popleft()
                for a,(dr,dc) in [("UP",(-1,0)),("DOWN",(1,0)),("LEFT",(0,-1)),("RIGHT",(0,1))]:
                    n = (r+dr, c+dc)
                    if n in free and n not in vis:
                        if n in actual.dirts: return (path + [a])[0]
                        vis.add(n); q.append((n, path + [a]))
        best, best_score = None, float('inf')
        for action in ["UP","DOWN","LEFT","RIGHT"]:
            new_a = self.simulate(actual, action)
            if new_a.robot_pos == actual.robot_pos: continue
            predicted = {self.simulate(s, action) for s in belief}
            updated = {s for s in predicted if self.get_percept(s) == self.get_percept(new_a)}
            score = len(updated) if updated else len(predicted)
            if score < best_score: best_score, best = score, action
        return best or "SUCK"

    def _belief_to_frontier(self, belief, action=None):
        """Chuyển belief state thành danh sách Node để hiển thị Frontier."""
        return [Node(s, action=action) for s in sorted(belief, key=lambda s: (s.robot_pos, len(s.dirts)))]

    def search(self, initial_state):
        free = {(r,c) for r in range(self.grid_rows) for c in range(self.grid_cols)
                if (r,c) not in self.obstacles}

        belief = {State(p, initial_state.dirts) for p in free}
        percept = self.get_percept(initial_state)
        belief = {s for s in belief if self.get_percept(s) == percept}
        explored = set()  # Các trạng thái đã xử lý

        p = percept
        yield {"log": f"INIT: Partially Observable | Sensor:[Rác:{p[0]} T↑:{p[1]} T↓:{p[2]} T←:{p[3]} T→:{p[4]}] → Belief:{len(belief)}",
               "frontier": self._belief_to_frontier(belief), "explored": list(explored)}

        actual, actions, step = initial_state, [], 0
        while step < self.MAX_STEPS:
            if actual.is_goal():
                for s in belief: explored.add(s)
                yield {"log": f"GOAL FOUND! Bước {step}: Dọn sạch! Belief:{len(belief)}",
                       "frontier": self._belief_to_frontier(belief),
                       "explored": list(explored)}
                break
            step += 1
            action = self._choose_action(actual, belief, free)

            # Cập nhật explored trước khi chuyển sang trạng thái mới
            for s in belief: explored.add(s)

            # PREDICT → UPDATE
            predicted = {self.simulate(s, action) for s in belief}
            new_actual = self.simulate(actual, action)
            new_p = self.get_percept(new_actual)
            updated = {s for s in predicted if self.get_percept(s) == new_p}
            if not updated: updated = predicted

            tag = " 🧹HÚT" if action == "SUCK" and actual.robot_pos in actual.dirts else ""
            yield {"log": f"POP Bước {step}: {action}{tag} | PREDICT:{len(predicted)} → UPDATE:{len(updated)} | Rác:{len(new_actual.dirts)}"
                          f"{' ✅HỘI TỤ!' if len(updated)==1 else ''}",
                   "frontier": self._belief_to_frontier(updated, action),
                   "explored": list(explored)}

            actual, belief = new_actual, updated
            actions.append(action)

        # Tạo solution node cho animation
        node = Node(initial_state)
        self.nodes_generated = step + 1
        for a in actions:
            node = Node(self.simulate(node.state, a), parent=node, action=a, path_cost=node.path_cost+1)

        if actual.is_goal():
            yield {"log": f"Chuỗi: {' → '.join(actions[:20])}{'...' if len(actions)>20 else ''}",
                   "frontier": [], "explored": list(explored)}
            yield {"log": "GOAL FOUND!", "solution": node}
        else:
            yield {"log": f"FAILURE: Không dọn xong trong {self.MAX_STEPS} bước.", "solution": None}