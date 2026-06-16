from algorithms.base_search import BaseSearch
from models.node import Node
from models.state import State

MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}


class AndOrSearch(BaseSearch):
    """AND-OR Graph Search – Nondeterministic (AIMA 4th Ed).

    Mô hình Erratic Vacuum:
      - Di chuyển vào ô bẩn → Nondeterministic:
        + Outcome 1: hút sạch ô hiện tại
        + Outcome 2: hút sạch ô hiện tại VÀ 1 ô bẩn lân cận (bonus)
      - Di chuyển vào ô sạch → Deterministic
    Cả 2 outcome đều tiến triển (dirts giảm) → không cycle → luôn có lời giải.
    """

    MAX_DEPTH = 100

    def _move_to(self, state, nr, nc, extra_clean=None):
        """Di chuyển robot tới (nr,nc), hút rác tại đó, tùy chọn hút thêm 1 ô."""
        if 0 <= nr < self.grid_rows and 0 <= nc < self.grid_cols \
                and (nr, nc) not in self.obstacles:
            dirts = state.dirts - {(nr, nc)}
            if extra_clean:
                dirts = dirts - {extra_clean}
            return State((nr, nc), dirts)
        return None

    def get_results(self, state, action):
        """Trả về tập kết quả nondeterministic."""
        dr, dc = MOVES[action]
        r, c = state.robot_pos
        nr, nc = r + dr, c + dc

        normal = self._move_to(state, nr, nc)
        if normal is None:
            return []

        # Nếu ô đích có rác → nondeterministic (bonus clean 1 ô lân cận)
        if (nr, nc) in state.dirts:
            # Tìm 1 ô bẩn lân cận để "bonus clean"
            for adr, adc in MOVES.values():
                ar, ac = nr + adr, nc + adc
                if (ar, ac) in state.dirts and (ar, ac) != (nr, nc):
                    bonus = self._move_to(state, nr, nc, extra_clean=(ar, ac))
                    if bonus and bonus != normal:
                        return [normal, bonus]
                    break

        return [normal]

    # ---------- AND-OR-GRAPH SEARCH (AIMA pseudocode) ----------

    def search(self, initial_state):
        self.failed_states = set()
        self.nodes_generated = 1
        yield {"log": "INIT: AND-OR GRAPH SEARCH (Nondeterministic – Erratic Vacuum)"}

        plan = yield from self._or_search(initial_state, [], 0)

        if plan is None:
            yield {"log": "FAILURE: Không tìm thấy kế hoạch.", "solution": None}
            return

        actions = self._flatten(plan, initial_state)
        yield {"log": f"GOAL FOUND! Đường đi: {' -> '.join(actions)} ({len(actions)} bước)"}

        node = Node(initial_state)
        for act in actions:
            dr, dc = MOVES[act]
            r, c = node.state.robot_pos
            ns = self._move_to(node.state, r + dr, c + dc) or node.state
            node = Node(ns, parent=node, action=act, path_cost=node.path_cost + 1)
            self.nodes_generated += 1
        yield {"log": "Gửi kết quả...", "solution": node}

    def _or_search(self, state, path, depth):
        indent = "  " * depth
        if state.is_goal():
            yield {"log": f"{indent}OR: {state} -> GOAL!"}
            return []
        if depth > self.MAX_DEPTH or state in path:
            if state in path:
                yield {"log": f"{indent}OR: CYCLE {state}"}
            return None
        if state in self.failed_states:
            yield {"log": f"{indent}OR: Prune {state}"}
            return None

        for action in MOVES:
            results = self.get_results(state, action)
            if not results:
                continue
            yield {"log": f"{indent}OR: [{action}] -> {len(results)} kết quả"}
            and_plan = yield from self._and_search(results, path + [state], depth + 1)
            if and_plan is not None:
                yield {"log": f"{indent}OR: [{action}] thành công!"}
                return [action, and_plan]

        self.failed_states.add(state)
        yield {"log": f"{indent}OR: Ngõ cụt {state}"}
        return None

    def _and_search(self, states, path, depth):
        indent = "  " * depth
        plans = {}
        for i, s in enumerate(states):
            yield {"log": f"{indent}AND: kết quả {i+1}/{len(states)}: {s}"}
            plan_s = yield from self._or_search(s, path, depth + 1)
            if plan_s is None:
                yield {"log": f"{indent}AND: Thất bại tại {s}"}
                return None
            plans[s] = plan_s
        yield {"log": f"{indent}AND: Tất cả {len(states)} nhánh OK!"}
        return plans

    def _flatten(self, plan, state):
        if not plan:
            return []
        action, and_plan = plan
        dr, dc = MOVES[action]
        r, c = state.robot_pos
        intended = self._move_to(state, r + dr, c + dc)
        ns = intended if intended in and_plan else next(iter(and_plan))
        return [action] + self._flatten(and_plan[ns], ns)