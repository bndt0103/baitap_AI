class State:
    def __init__(self, robot_pos, dirts):
        self.robot_pos = robot_pos
        self.dirts = frozenset(dirts)

    def is_goal(self):
        return len(self.dirts) == 0

    def __eq__(self, other):
        return self.robot_pos == other.robot_pos and self.dirts == other.dirts

    def __hash__(self):
        return hash((self.robot_pos, self.dirts))

    def __str__(self):
        return f"Pos:{self.robot_pos}-Dirts:{len(self.dirts)}"