from algorithms.base_search import BaseSearch
from models.node import Node
from models.state import State
from collections import deque


class SensorlessDFS(BaseSearch):
    """Sensorless (Conformant) Search - Tìm kiếm KHÔNG CÓ CẢM BIẾN.
    Robot không biết vị trí -> tìm chuỗi hành động đảm bảo dọn sạch từ MỌI vị trí."""

    def simulate(self, state, action):
        r, c = state.robot_pos
        dirts = set(state.dirts)
        if action == "UP" and r > 0 and (r-1,c) not in self.obstacles: r -= 1
        elif action == "DOWN" and r < self.grid_rows-1 and (r+1,c) not in self.obstacles: r += 1
        elif action == "LEFT" and c > 0 and (r,c-1) not in self.obstacles: c -= 1
        elif action == "RIGHT" and c < self.grid_cols-1 and (r,c+1) not in self.obstacles: c += 1
        elif action == "SUCK": dirts.discard((r,c))
        return State((r,c), frozenset(dirts))

    def _bfs_path(self, start, goal, free):
        if start == goal: return []
        q = deque([(start, [])])
        vis = {start}
        while q:
            (r,c), path = q.popleft()
            for a,(dr,dc) in [("UP",(-1,0)),("DOWN",(1,0)),("LEFT",(0,-1)),("RIGHT",(0,1))]:
                n = (r+dr, c+dc)
                if n in free and n not in vis:
                    if n == goal: return path + [a]
                    vis.add(n); q.append((n, path + [a]))
        return []

    def _build_plan(self, start_pos, free):
        """Xây dựng kế hoạch: Coerce về góc, rồi duyệt toàn bộ ô từ vị trí thực tế."""
        coerce = ["UP"]*(self.grid_rows-1) + ["LEFT"]*(self.grid_cols-1)
        # Mô phỏng coerce trên vị trí thực tế để biết robot thực sự ở đâu
        r, c = start_pos
        for action in coerce:
            if action == "UP" and r > 0 and (r-1,c) not in self.obstacles: r -= 1
            elif action == "LEFT" and c > 0 and (r,c-1) not in self.obstacles: c -= 1
        actual_after_coerce = (r, c)

        # Duyệt BFS từ vị trí thực tế để thăm MỌI ô trống
        q, vis, order = deque([actual_after_coerce]), {actual_after_coerce}, [actual_after_coerce]
        while q:
            pos = q.popleft()
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                n = (pos[0]+dr, pos[1]+dc)
                if n in free and n not in vis:
                    vis.add(n); order.append(n); q.append(n)
        # Tạo đường đi qua tất cả ô, SUCK tại mỗi ô
        sweep = ["SUCK"]  # SUCK tại ô xuất phát sau coerce
        cur = actual_after_coerce
        for t in order[1:]:
            for a in self._bfs_path(cur, t, free):
                sweep.append(a)
                sweep.append("SUCK")
            cur = t
        return coerce + sweep

    def _belief_to_frontier(self, belief, action=None):
        return [Node(s, action=action) for s in sorted(belief, key=lambda s: (s.robot_pos, len(s.dirts)))]

    def search(self, initial_state):
        free = {(r,c) for r in range(self.grid_rows) for c in range(self.grid_cols)
                if (r,c) not in self.obstacles}
        belief = frozenset(State(p, initial_state.dirts) for p in free)
        explored = set()

        yield {"log": f"INIT: Sensorless Search - Belief = {len(belief)} vị trí có thể",
               "frontier": self._belief_to_frontier(belief), "explored": list(explored)}

        plan = self._build_plan(initial_state.robot_pos, free)
        yield {"log": f"GENERATE: Kế hoạch Conformant {len(plan)} hành động (COERCE → SWEEP)",
               "frontier": self._belief_to_frontier(belief), "explored": list(explored)}

        step = 0
        for action in plan:
            new_belief = frozenset(self.simulate(s, action) for s in belief)
            step += 1
            for s in belief: explored.add(s)
            belief = new_belief
            positions = len({s.robot_pos for s in belief})
            dirts = sum(len(s.dirts) for s in belief)

            if step <= 8 or step % 10 == 0 or dirts == 0:
                yield {"log": f"POP Bước {step}: {action} → Belief:{len(belief)} | Vị trí:{positions} | Rác:{dirts}",
                       "frontier": self._belief_to_frontier(belief, action),
                       "explored": list(explored)}

            if all(s.is_goal() for s in belief):
                for s in belief: explored.add(s)
                yield {"log": f"GOAL FOUND! Bước {step}: Mọi {len(belief)} trạng thái đều sạch!",
                       "frontier": self._belief_to_frontier(belief, action),
                       "explored": list(explored)}
                break

        # Tạo solution trên trạng thái thực tế
        executed = plan[:step]
        node = Node(initial_state)
        self.nodes_generated = step + 1
        for a in executed:
            node = Node(self.simulate(node.state, a), parent=node, action=a, path_cost=node.path_cost+1)

        if node.state.is_goal():
            yield {"log": f"Chuỗi: {' → '.join(executed[:20])}{'...' if len(executed)>20 else ''}",
                   "frontier": [], "explored": list(explored)}
            yield {"log": "GOAL FOUND!", "solution": node}
        else:
            yield {"log": "FAILURE: Không tìm được lời giải conformant.", "solution": None}