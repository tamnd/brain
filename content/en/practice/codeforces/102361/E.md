---
title: "CF 102361E - Escape"
description: "We have an n × m grid containing empty cells and blocked cells. Each robot starts immediately above the grid in a distinct column and initially moves downward. Each exit is immediately below the grid in a distinct column. A robot normally continues straight."
date: "2026-08-13T00:11:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "E"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 226
verified: true
draft: false
---

[CF 102361E - Escape](https://codeforces.com/problemset/problem/102361/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × m` grid containing empty cells and blocked cells. Each robot starts immediately above the grid in a distinct column and initially moves downward. Each exit is immediately below the grid in a distinct column.

A robot normally continues straight. The only way to change direction is to place one of four corner-shaped turning devices on an empty cell. Each device connects exactly one horizontal side of the cell with one vertical side, so geometrically it behaves like a corner. A device cannot be crossed from an incompatible direction.

Robots are allowed to occupy the same empty cell, so ordinary cell occupancy is not a capacity constraint. The difficulty comes from the fact that a turning device occupies its whole cell. A robot that does not use the device cannot pass straight through that cell. This creates a useful separation property between different robot paths.

For every test case, the input gives the grid, the starting columns of all robots, and the columns of all exits. The question is whether we can place turning devices so that every robot eventually reaches some exit without touching a blocked cell or using a device from an illegal direction. We only need to output `Yes` or `No`.

The grid dimensions are at most `100 × 100`, so there are at most `10,000` cells. There can be at most `100` robots. A solution with roughly `O(nm)` or `O(anm)` operations is easily manageable. A solution that enumerates configurations of the cells is hopeless, because even before considering the robot movements, every empty cell has five possibilities: no device or one of four device orientations. The number of configurations can reach `5^(nm)`, which is already astronomically large for `nm = 10,000`. The original contest listing gives a one-second time limit, so the intended solution needs to exploit the grid structure rather than search configurations.

Several edge cases are easy to mishandle.

Consider a single blocked cell:

```
1
1 1 1 1
1
1
1
```

The only robot starts above the only cell, and the only exit is below it. Since the cell is blocked, the correct answer is `No`. An implementation that connects every source column directly to its vertical grid node without checking whether the first cell is empty would incorrectly accept it.

The same issue occurs at the bottom:

```
1
1 1 1 1
1
1
1
```

Here the grid is blocked, so there is no usable path to the exit. More generally, an exit below a blocked bottom cell cannot be reached. The graph must only connect exits to vertical states of empty bottom cells.

A one-row maze also requires care because a robot may need to turn horizontally and then turn downward again within the same row:

```
1
1 2 1 1
00
1
2
```

The answer is `Yes`. The robot enters column `1` vertically, turns right in the first cell, turns downward in the second cell, and leaves through exit `2`. A graph that assumes every vertical movement must pass through at least two different rows would miss this valid construction.

Finally, consider the official second sample:

```
1
3 4 2 2
0000
0011
0000
3 4
2 4
```

The answer is `No`. The robot starting in column `3` and the robot starting in column `4` can both be made to approach exit `4` only by sharing a turning structure that cannot be occupied by two different paths in the required way. A naive reachability check that computes one path for each robot independently can say `Yes`, because each robot separately has a route to an exit. The real problem is whether all routes can coexist in one placement of devices.

## Approaches

The direct brute-force approach is to decide what happens in every empty cell. Each cell has five choices: leave it empty, or install one of the four possible corner devices. For a configuration, we can simulate every robot while remembering its current cell and direction. Since the state is a pair consisting of a cell and one of four directions, a deterministic robot can be simulated for at most `4nm` states before either reaching an exit or repeating a state. Reaching a repeated state means the robot is trapped in a cycle.

If there are `k` empty cells, the configuration count is `5^k`. In the worst case `k = nm = 10,000`, so even just enumerating the configurations requires `5^10000` cases. Adding simulation of up to `a` robots would give roughly `O(5^(nm) · a · nm)`, which is completely infeasible.

The useful observation is that the geometry lets us forget the exact orientation of a device for a moment. Think about a cell from two different viewpoints. A robot can be moving vertically through the cell, or it can be moving horizontally through the cell. A turning device is precisely what connects these two possibilities.

For every empty cell `(i,j)`, create two graph vertices. Let `V(i,j)` represent vertical movement through the cell, and let `H(i,j)` represent horizontal movement through the cell.

If two vertically adjacent cells are both empty, a robot can continue vertically between their `V` vertices. Similarly, two horizontally adjacent empty cells are connected between their `H` vertices.

Inside one empty cell, connect `V(i,j)` and `H(i,j)`. Using this connection means placing a turning device there. The direction of the corresponding flow determines which of the four corner orientations is required. The two opposite directions of the same connection correspond to the two legal ways of traversing the same corner.

There is a second geometric observation that explains why unit capacities are sufficient. Two robots cannot share a useful straight segment and later separate. If a turning device is placed on their shared segment, the robot that does not turn would have to pass straight through a cell occupied by a turning device, which is illegal. If no such device exists, the two robots remain on the same trajectory until the exit, and distinct exits cannot make that shared trajectory serve as two different routes. Thus a feasible solution can be represented by paths that do not compete for the same horizontal or vertical track. This is the key reason for using capacity one on the track edges. The standard solutions for this problem use exactly this two-layer grid construction and maximum flow.

The source connects to `V(1,p)` for every robot starting at column `p`. This models the fact that every robot enters the first row vertically. For every exit column `e`, connect `V(n,e)` to the sink, because reaching the bottom of that cell while moving downward means that the robot can leave the maze.

The resulting graph has only `O(nm)` vertices and edges. We then ask whether the maximum flow equals the number of robots. If it does, the flow decomposes into valid source-to-exit paths, and each connection between a horizontal and vertical state tells us where to put a turning device. If the maximum flow is smaller than the number of robots, some robot cannot be assigned a compatible path.

The standard editorial construction is usually implemented with Dinic's algorithm. Since every relevant capacity is one and the total desired flow is at most `a ≤ 100`, we can use an even simpler specialized maximum-flow implementation: repeatedly run BFS to find one augmenting path and send one unit through it. At most `a` augmentations are necessary. This gives an `O(aE)` bound, which is easily small enough here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(5^(nm) · a · nm)` | `O(nm)` | Too slow |
| Optimal | `O(a · nm)` | `O(nm)` | Accepted |

## Algorithm Walkthrough

1. Create two vertices for every grid cell, one representing vertical movement and one representing horizontal movement. Blocked cells receive no usable edges. The split is necessary because a turn is exactly a transition from one movement type to the other.
2. For every pair of vertically adjacent empty cells, connect their vertical vertices in both directions with capacity `1`. A robot can travel straight up or down along this connection. The capacity represents the fact that two feasible robot trajectories cannot compete for the same directed track.
3. For every pair of horizontally adjacent empty cells, connect their horizontal vertices in both directions with capacity `1`. This is the horizontal equivalent of the previous step.
4. For every empty cell, connect its horizontal vertex and vertical vertex in both directions with capacity `1`. Using this edge means that the cell contains a turning device. For example, a flow entering the vertical state from above and leaving through the horizontal state corresponds to an appropriate `NE` or `NW` device depending on which horizontal direction the flow takes. Reversing the movement gives the corresponding legal reverse traversal.
5. Add a super-source and a super-sink. For each robot at column `p`, connect the source to `V(1,p)` with capacity `1`, provided that the first cell is empty. The capacity one represents one robot starting there.
6. For every exit at column `e`, connect `V(n,e)` to the sink with capacity `1`, provided that the bottom cell is empty. The robot must be moving downward when it leaves the maze, so the exit belongs to the vertical layer.
7. Compute the maximum flow from the source to the sink. We repeatedly run BFS on the residual graph, recover one augmenting path with parent pointers, and increase the flow by one. Since every original edge has capacity one and we only need at most `a` units of flow, no more than `a` augmentations are required.
8. Compare the resulting flow with `a`. If the flow equals the number of robots, print `Yes`. Otherwise print `No`.

### Why it works

The central invariant is that every source-to-sink flow path describes one legal robot trajectory. Moving along a vertical edge means continuing vertically through adjacent empty cells. Moving along a horizontal edge means continuing horizontally through adjacent empty cells. Switching between the two layers means placing one corner device in that cell. Since every such transition has unit capacity, the construction cannot assign the same directed turning resource or straight track to two incompatible robot paths.

Conversely, take any valid arrangement of turning devices. Follow each robot from its starting point to its exit and record whether it is moving vertically or horizontally at every cell. Straight movement becomes an edge inside one layer, while every legal turn becomes an edge between the two layers. The resulting robot trajectories form source-to-sink flow paths. The geometric separation property prevents conflicting paths from requiring the same unit-capacity resource. Thus every valid escape arrangement gives a flow of value `a`, and every flow of value `a` gives a realizable set of robot trajectories. By the max-flow characterization, checking whether the maximum flow is `a` is exactly the required decision.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

def solve_case(n, m, a, b, grid, robots, exits):
    cells = n * m
    source = 2 * cells
    sink = source + 1
    vertex_count = sink + 1

    # Forward-star representation of the residual graph.
    head = [-1] * vertex_count
    to = []
    cap = []
    nxt = []

    def add_edge(u, v, c):
        idx = len(to)
        to.append(v)
        cap.append(c)
        nxt.append(head[u])
        head[u] = idx

        to.append(u)
        cap.append(0)
        nxt.append(head[v])
        head[v] = idx + 1

    def add_bidir(u, v):
        add_edge(u, v, 1)
        add_edge(v, u, 1)

    def hnode(i, j):
        return (i * m + j) * 2

    def vnode(i, j):
        return (i * m + j) * 2 + 1

    # Source to robots and bottom cells to sink.
    for p in robots:
        j = p - 1
        if grid[0][j] == '0':
            add_edge(source, vnode(0, j), 1)

    for e in exits:
        j = e - 1
        if grid[n - 1][j] == '0':
            add_edge(vnode(n - 1, j), sink, 1)

    # Grid graph.
    for i in range(n):
        for j in range(m):
            if grid[i][j] != '0':
                continue

            v = vnode(i, j)
            h = hnode(i, j)

            # A turn in this cell.
            add_bidir(h, v)

            # Continue vertically.
            if i > 0 and grid[i - 1][j] == '0':
                add_bidir(vnode(i - 1, j), v)

            # Continue horizontally.
            if j > 0 and grid[i][j - 1] == '0':
                add_bidir(hnode(i, j - 1), h)

    flow = 0

    # Since all useful capacities are one and a <= 100, repeatedly
    # finding one augmenting path is fast enough.
    while flow < a:
        parent = [-1] * vertex_count
        parent[source] = -2

        q = deque([source])

        while q and parent[sink] == -1:
            u = q.popleft()
            e = head[u]

            while e != -1:
                if cap[e] > 0:
                    v = to[e]
                    if parent[v] == -1:
                        parent[v] = e
                        if v == sink:
                            break
                        q.append(v)
                e = nxt[e]

        if parent[sink] == -1:
            break

        # Every augmenting path carries exactly one unit.
        v = sink
        while v != source:
            e = parent[v]
            cap[e] -= 1
            cap[e ^ 1] += 1
            v = to[e ^ 1]

        flow += 1

    return flow == a

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, m, a, b = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        robots = list(map(int, input().split()))
        exits = list(map(int, input().split()))

        answers.append(
            "Yes" if solve_case(n, m, a, b, grid, robots, exits)
            else "No"
        )

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The graph uses two integer IDs for each cell. `hnode(i, j)` is the horizontal state and `vnode(i, j)` is the vertical state. Keeping the two states separate is what lets a single cell represent both straight movement possibilities and a possible turn.

The `add_bidir` helper deserves attention. A bidirectional capacity-one connection is implemented as two independent directed capacity-one edges. Each directed edge also receives its own residual edge. This is different from adding one ordinary residual edge pair, because movement in both directions is physically possible.

The source only connects to an empty first-row cell. This avoids accidentally allowing a robot to enter a blocked cell. The same check is performed for the bottom row before connecting an exit to the sink.

The graph construction only checks the cell above and the cell to the left. When processing `(i,j)`, the corresponding edges to those neighbors have not been added before, so each undirected grid adjacency is inserted exactly once. `add_bidir` then creates both directions.

The flow search uses BFS over residual edges. `parent[v]` stores the edge used to first reach `v`, allowing the complete augmenting path to be reconstructed from the sink. Since every augmentation adds exactly one unit and there are at most `100` robots, the loop terminates after at most `100` successful augmentations. No integer overflow is possible in Python, and in fact all capacities and the answer are at most `100`.

The code uses zero-based grid coordinates internally. The input columns are one-based, so every robot or exit column is converted with `p - 1`. This is the main indexing detail that tends to cause mistakes in this implementation.

## Worked Examples

The official sample contains two test cases. Written in the normal multiline form, it is:

```
2
3 4 2 2
0000
0011
0000
1 4
2 4
3 4 2 2
0000
0011
0000
3 4
2 4
```

For the first case, the two robots can use separate turning structures. One route starts in column `1`, travels down to the last row, turns right, and leaves through exit `2`. The other starts in column `4`, turns left near the top, travels down through column `3`, turns right near the bottom, and leaves through exit `4`.

| Augmentation | Source robot | Main graph route | Flow |
| --- | --- | --- | --- |
| 1 | column 1 | vertical column 1 → horizontal row 3 → vertical column 2 → sink | 1 |
| 2 | column 4 | vertical column 4 → horizontal row 1 → vertical column 3 → horizontal row 3 → vertical column 4 → sink | 2 |

After the second augmentation the flow equals `a = 2`, so the algorithm prints `Yes`. The trace demonstrates why a robot can turn multiple times and why the two-layer representation is sufficient to encode all four device orientations.

For the second case, the robots start in columns `3` and `4`. The robot from column `4` can be routed toward exit `4`, but the robot from column `3` also needs the same lower turning structure to reach exit `4` while avoiding the blocked cells in row `2`. The residual network can find only one compatible source-to-sink path.

| Augmentation | Source robot | Result | Flow |
| --- | --- | --- | --- |
| 1 | one of columns 3 or 4 | reaches an available exit path | 1 |
| 2 | remaining robot | no augmenting path remains | 1 |

The maximum flow is `1`, smaller than `a = 2`, so the answer is `No`. This demonstrates why checking reachability separately for every robot is insufficient. The paths have to coexist under the same grid and device constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(a · nm)` | The graph has `O(nm)` edges, and at most `a ≤ 100` unit augmentations are performed. |
| Space | `O(nm)` | There are `O(nm)` graph vertices and residual edges. |

For `n,m ≤ 100`, the graph contains at most `20,002` vertices. The number of residual edges is also linear in the number of cells. Since at most `100` augmentations are needed, the specialized augmenting-path implementation performs only a small number of full graph searches. This is comfortably within the intended complexity for the contest constraints. The official contest listing gives a one-second time limit and 1024 MB of memory, while accepted solutions use the same two-layer maximum-flow construction.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official samples
sample = """\
2
3 4 2 2
0000
0011
0000
1 4
2 4
3 4 2 2
0000
0011
0000
3 4
2 4
"""

assert run(sample) == "Yes\nNo", "official sample"

# Minimum-size open maze.
assert run("""\
1
1 1 1 1
0
1
1
""") == "Yes", "single open cell"

# Minimum-size blocked maze.
assert run("""\
1
1 1 1 1
1
1
1
""") == "No", "single blocked cell"

# One-row maze requiring two turns.
assert run("""\
1
1 2 1 1
00
1
2
""") == "Yes", "horizontal detour in one row"

# Maximum-size empty maze.
grid = "\n".join(["0" * 100 for _ in range(100)])
max_case = (
    "1\n"
    "100 100 100 100\n"
    + grid + "\n"
    + " ".join(map(str, range(1, 101))) + "\n"
    + " ".join(map(str, range(1, 101))) + "\n"
)

assert run(max_case) == "Yes", "maximum all-empty case"

# Boundary case with a blocked bottom exit cell.
assert run("""\
1
2 2 1 1
00
01
1
2
""") == "No", "blocked exit cell"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 × 1` with grid `0` | `Yes` | Minimum dimensions and direct vertical escape |
| `1 × 1` with grid `1` | `No` | Blocked starting cell |
| `1 × 2` with grid `00`, robot `1`, exit `2` | `Yes` | Boundary turns and one-row movement |
| `100 × 100` all zeros with 100 robots and 100 exits | `Yes` | Maximum dimensions, maximum flow value, and large graph construction |
| `2 × 2`, grid `00 / 01`, exit column `2` | `No` | Blocked bottom exit and boundary indexing |

## Edge Cases

The blocked starting cell case is handled before any flow can leave the source. For

```
1
1 1 1 1
1
1
1
```

the only grid cell is blocked, so the source receives no edge at all. The BFS immediately finds that the sink is unreachable, the flow remains `0`, and the result is `No`.

A blocked exit cell behaves symmetrically. Consider

```
1
2 2 1 1
00
01
1
2
```

The robot starts above column `1`, while the only exit is below column `2`. Although the first row is open, the bottom cell in column `2` is blocked. The implementation refuses to add the edge `V(2,2) -> sink`, so no path can terminate at that exit. The maximum flow is `0`, producing `No`.

The one-row boundary case is more subtle:

```
1
1 2 1 1
00
1
2
```

The source connects to the vertical state of cell `(1,1)`. The first turn uses the edge between `V(1,1)` and `H(1,1)`, the horizontal edge moves to `H(1,2)`, and the second turn moves to `V(1,2)`. Finally `V(1,2)` connects to the sink. The flow is `1`, so the answer is `Yes`. No special case for `n = 1` is needed because the graph representation already handles it naturally.

The shared-path case is captured by the official second sample:

```
1
3 4 2 2
0000
0011
0000
3 4
2 4
```

The two robots have individually plausible routes, but the required routes compete for the same unit-capacity structure. Once one route consumes that resource, the second source has no residual path to an exit. The maximum flow stops at `1`, while two units are required, so the algorithm returns `No`.

The maximum-size all-empty case tests the opposite extreme:

```
100 × 100 grid of zeros
100 robots in columns 1 through 100
100 exits in columns 1 through 100
```

Every robot can simply continue downward without using a turning device. The graph contains all `20,000` movement states, but the source-to-sink flow has value exactly `100`. This confirms that the implementation does not accidentally require a turn when a straight path already exists and that the graph remains manageable at the largest dimensions.
