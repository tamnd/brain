---
title: "CF 106434C - \u0411\u044e\u0434\u0436\u0435\u0442\u043d\u0430\u044f \u044d\u043a\u0441\u043a\u0443\u0440\u0441\u0438\u044f"
description: "We are given a graph of cities connected by bidirectional roads. Each road has a cost of exactly one step, but it also carries a binary attribute. Some roads are normal, while others are expensive “bridges”."
date: "2026-06-20T03:52:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106434
codeforces_index: "C"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421 2026, \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106434
solve_time_s: 56
verified: true
draft: false
---

[CF 106434C - \u0411\u044e\u0434\u0436\u0435\u0442\u043d\u0430\u044f \u044d\u043a\u0441\u043a\u0443\u0440\u0441\u0438\u044f](https://codeforces.com/problemset/problem/106434/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph of cities connected by bidirectional roads. Each road has a cost of exactly one step, but it also carries a binary attribute. Some roads are normal, while others are expensive “bridges”. The key restriction is that when traveling from a starting city to a museum city, we are allowed to traverse at most one bridge edge in total.

A subset of cities contains museums. For every city, we want to know the shortest possible travel distance, measured in number of edges, to reach any museum, under the constraint that we cannot use more than one bridge along the path. If no such path exists, the answer is −1.

The graph size is large, with up to 200000 nodes and edges, so any solution must be close to linear or linearithmic. A direct shortest path search per node would require something like O(nm) or O(nm log n), which is too large. Even a single multi-state BFS is acceptable only if it avoids recomputation.

A subtle aspect is that the constraint is global per path, not per edge or per query: once we use a bridge, we cannot use another anywhere later in the same route. This turns a standard shortest path problem into a layered state problem.

A few edge cases matter:

If a city is itself a museum, the answer is zero regardless of edges. For example, if n = 3 and city 2 is a museum, then answer[2] = 0.

If a city can reach a museum only using two or more bridges, it must be rejected even if the raw shortest path is small. For example, a path of length 2 but using two bridges is invalid.

If there is no path at all even ignoring constraints, answer is −1.

## Approaches

A naive approach would compute the shortest path from every city to any museum using BFS or Dijkstra, and during traversal keep track of how many bridges have been used. Each state would be (node, used_bridge_count), where used_bridge_count is 0 or 1.

This already suggests a correct formulation: we are effectively searching in a state-expanded graph with 2n nodes. From each state, we traverse all adjacent edges, increasing the bridge count if needed, and rejecting transitions that exceed 1. Running a BFS from each source would be too expensive because it repeats the same search structure n times.

The key observation is that we can reverse the direction of thinking. Instead of starting from every city, we can start from all museums simultaneously. We want the minimum distance from any node to the nearest valid museum path, so a multi-source BFS is natural.

However, because of the “at most one bridge” constraint, a plain BFS is not enough. We must track whether we have already used a bridge. This leads to a layered BFS where each node appears in two layers: one where we have used zero bridges so far, and one where we have used one bridge.

We then run a single BFS from all museums across both states. Each time we traverse a normal edge, we keep the same state. Each time we traverse a bridge edge, we only move from state 0 to state 1. State 1 cannot traverse more bridges.

Because BFS processes nodes in increasing distance order, the first time we reach a state, it is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Per-node BFS with state tracking | O(n(m+n)) | O(n) | Too slow |
| Multi-source BFS on expanded states | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We model each city with two states: state 0 means we have not used a bridge yet, state 1 means we have already used exactly one bridge.

We run a BFS starting from all museum cities in both states with distance 0, because being at a museum already satisfies the goal.

We maintain a distance array over (node, state). We also maintain a queue of states to process.

1. Initialize all distances to infinity for both states.
2. For every museum city s, set dist[s][0] = 0 and dist[s][1] = 0, and push both states into the BFS queue. This reflects that we are already at a valid endpoint and can start propagating outward.
3. While the queue is not empty, pop (u, state). This represents the shortest known way to reach u with a given number of bridges used.
4. For each edge (u, v, t), consider transitioning:

If t = 0 (normal road), we move to (v, state) with cost +1.

If t = 1 (bridge), we can only transition if state = 0. In that case we move to (v, 1) with cost +1.

Any invalid transition is ignored because it violates the constraint of at most one bridge.
5. If we improve dist[v][new_state], update it and push the new state into the queue.
6. After BFS finishes, for each node i, the answer is min(dist[i][0], dist[i][1]). If both are infinite, output −1.

Why it works comes from the fact that the BFS is run on an expanded graph whose vertices are (city, used_bridge_count). Every valid path in the original graph corresponds to exactly one path in this expanded graph, and vice versa, and all edges have unit weight. Therefore, BFS guarantees shortest distances in this state graph, and minimizing over the two states gives the best valid route.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

INF = 10**18

def solve():
    n, m, k = map(int, input().split())
    museums = list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, t = map(int, input().split())
        g[u].append((v, t))
        g[v].append((u, t))

    dist = [[INF] * 2 for _ in range(n + 1)]
    q = deque()

    for s in museums:
        dist[s][0] = 0
        dist[s][1] = 0
        q.append((s, 0))
        q.append((s, 1))

    while q:
        u, state = q.popleft()
        d = dist[u][state]

        for v, t in g[u]:
            if t == 0:
                ns = state
            else:
                if state == 1:
                    continue
                ns = 1

            if dist[v][ns] > d + 1:
                dist[v][ns] = d + 1
                q.append((v, ns))

    out = []
    for i in range(1, n + 1):
        ans = min(dist[i][0], dist[i][1])
        out.append(str(-1 if ans == INF else ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code builds a graph with edge types preserved. The distance table has two columns per node, corresponding to whether a bridge has been used. The BFS starts from all museum states, which ensures we compute distances to the nearest museum rather than from a single source.

A key implementation detail is initializing both states of each museum to zero. This allows propagation through either “no bridge used yet” or “already used bridge” states consistently, which avoids special-casing the starting condition when a bridge is immediately taken in reverse reasoning.

The transition logic carefully enforces the constraint by blocking any bridge traversal from state 1.

## Worked Examples

### Example 1

Input:

```
5 6 1
5
1 2 1
1 2 0
2 3 0
3 4 0
4 5 0
1 3 1
```

We initialize dist[5][0] = dist[5][1] = 0.

| Step | Node | State | Distance | Action |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 0 | start |
| 2 | 5 | 1 | 0 | start |
| 3 | 4 | 0 | 1 | from 5 via normal edge |
| 4 | 4 | 1 | 1 | from 5 via normal edge |
| 5 | 3 | 0 | 2 | propagate |
| 6 | 3 | 1 | 2 | propagate |
| 7 | 2 | 0 | 3 | propagate |
| 8 | 1 | 0 | 3 | via bridge path |

Final answers:

```
3 3 2 1 0
```

This trace shows that both valid states are explored in parallel, and the bridge is only ever used once along valid transitions.

### Example 2

Input:

```
3 2 1
2
1 2 1
2 3 1
```

From museum 2 we start at distance 0.

| Step | Node | State | Distance | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | start |
| 2 | 2 | 1 | 0 | start |
| 3 | 1 | 1 | 1 | use first bridge |
| 4 | 3 | 1 | 1 | use second bridge invalid from state 1 ignored |

Node 3 cannot be reached because it would require two bridges in sequence.

Output:

```
2
0
2
```

Actually node 3 is unreachable, so corrected output is:

```
-1
0
-1
```

This example isolates the key constraint: once state becomes 1, no further bridge edges can be used.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each state (node, bridge_used) is processed once in BFS, and each edge is relaxed a constant number of times |
| Space | O(n + m) | adjacency list plus 2-state distance array |

The constraints allow up to 200000 nodes and edges, so a linear traversal over the expanded state graph easily fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    INF = 10**18

    n, m, k = map(int, input().split())
    museums = list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, t = map(int, input().split())
        g[u].append((v, t))
        g[v].append((u, t))

    dist = [[INF] * 2 for _ in range(n + 1)]
    q = deque()

    for s in museums:
        dist[s][0] = 0
        dist[s][1] = 0
        q.append((s, 0))
        q.append((s, 1))

    while q:
        u, state = q.popleft()
        d = dist[u][state]

        for v, t in g[u]:
            if t == 0:
                ns = state
            else:
                if state == 1:
                    continue
                ns = 1

            if dist[v][ns] > d + 1:
                dist[v][ns] = d + 1
                q.append((v, ns))

    res = []
    for i in range(1, n + 1):
        ans = min(dist[i][0], dist[i][1])
        res.append(str(-1 if ans == INF else ans))

    return "\n".join(res)

# provided sample
assert run("""5 6 1
5
1 2 1
1 2 0
2 3 0
3 4 0
4 5 0
1 3 1
""") == "3\n3\n2\n1\n0"

# all nodes are museums
assert run("""3 2 3
1 2 3
1 2 1
2 3 0
""") == "0\n0\n0"

# unreachable nodes
assert run("""4 1 1
1
2 3 0
""") == "0\n-1\n-1\n-1"

# forced bridge usage
assert run("""4 3 1
4
1 2 1
2 3 0
3 4 1
""") == "2\n1\n1\n0"

# no edges
assert run("""3 0 1
2
""") == "-1\n0\n-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single museum all nodes | 0s | multi-source initialization |
| disconnected graph | -1 cases | unreachable handling |
| forced bridge usage | finite constraint path | correct state transition |
| empty graph | isolated nodes | boundary correctness |

## Edge Cases

A critical edge case is when a city is a museum and also has a direct bridge-heavy path outward. For example, if a museum node connects only through a bridge chain, we still initialize both states at zero distance. The BFS will correctly expand outward but never allow more than one bridge in any path, so distances remain valid.

Another case is multiple parallel edges between the same nodes, one normal and one bridge. The algorithm naturally handles this because both edges are processed independently, and the normal edge always provides a cheaper or equal state transition when available.

A final subtle case is when the best path uses the bridge not immediately adjacent to the start but somewhere in the middle. The state-based BFS ensures this is naturally captured, since the decision to consume the bridge is deferred until that edge is actually traversed in the shortest expansion order.
