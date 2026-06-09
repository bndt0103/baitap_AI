import sys
sys.stdout.reconfigure(encoding='utf-8')
from models.state import State
from algorithms.sensorless_dfs import SensorlessDFS
from algorithms.partially_observable_dfs import PartiallyObservableDFS

tests = [
    ("3x3", 3, 3, (0,0), [(1,1),(2,2)], []),
    ("4x4+obs", 4, 4, (0,0), [(1,1),(2,2)], [(1,0)]),
    ("6x6", 6, 6, (0,0), [(3,3),(5,5)], [(2,2),(1,1)]),
    ("2x2", 2, 2, (0,0), [(1,1)], []),
]
for name, rows, cols, robot, dirts, obs in tests:
    init = State(robot, frozenset(dirts))
    for AlgoCls, aname in [(SensorlessDFS,"Sensorless"), (PartiallyObservableDFS,"PartObs")]:
        algo = AlgoCls(rows, cols, obs)
        sol = None
        for step in algo.search(init):
            if 'solution' in step: sol = step['solution']; break
        status = f"OK path={len(sol.get_path())}" if sol else "FAIL"
        print(f"  {name:8s} {aname:12s}: {status}")
print("ALL DONE!")
