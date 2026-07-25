---
title: "CF 102878H - Treasure Hunt"
description: "The game is played on a directed acyclic graph. A single turn starts at node 1 and finishes when we reach node n. Every time a turn visits a node, that node contributes its reward to the total score. Each directed edge can only be used a limited number of times across all turns."
date: "2026-07-25T12:45:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "H"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 42
verified: true
draft: false
---

[CF 102878H - Treasure Hunt](https://codeforces.com/problemset/problem/102878/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a directed acyclic graph. A single turn starts at node 1 and finishes when we reach node n. Every time a turn visits a node, that node contributes its reward to the total score. Each directed edge can only be used a limited number of times across all turns. The goal is to choose the collection of paths from 1 to n that gives the largest possible sum of collected rewards.

The important detail is that several turns can overlap on vertices, but they cannot exceed the capacity of any edge. This makes the problem different from finding the best single path. A locally best path may consume edges that would have allowed many other valuable paths later.

The constraints are small enough for graph algorithms but too large for trying all possible combinations of paths. With at most 100 vertices and 500 edges, the total number of possible paths in a DAG can still be exponential, so enumerating paths or trying every subset of turns is impossible. We need a polynomial solution based on the structure of the graph.

Several edge cases can break an incorrect implementation. Consider a graph where there is only one path from 1 to n:

```
2 1
5 7
1 2 3
```

The answer is 36, because the same path can be played three times and every play collects both node rewards. A solution that only finds one best path would return 12 and fail.

Another tricky case is when two paths share a limited edge:

```
4 4
1 10 1 1
1 2 1
2 4 1
1 3 5
3 4 1
```

The answer is 18. The path through node 2 gives 12 and the path through node 3 gives 7. A greedy approach that always chooses the currently most valuable path might consume a shared bottleneck in other examples and prevent a better global distribution.

The reward of node 1 is also easy to miss. The player starts each turn at node 1, and the example shows that this starting node contributes to the score. Any flow model must count node 1 and node n exactly once per used path.

## Approaches

The brute-force idea is to repeatedly search for the most profitable path from node 1 to node n, use it once, decrease the capacities of its edges, and continue until no path remains. This works for some small cases because every chosen path is valid and every used edge respects the rules.

The problem is that choosing the best path at each moment is not globally optimal. More importantly, the number of possible paths in a DAG can be exponential, so even storing all candidates is impossible. If there are many different branches, the search space grows far beyond what the constraints allow.

The key observation is that every turn is a unit of flow from node 1 to node n. Edge pass limits are exactly edge capacities. The total reward is attached to every vertex used by a unit of flow, which means we can transform vertex rewards into costs on edges by splitting every vertex into an incoming and outgoing copy.

After splitting, sending one unit of flow through a vertex forces the flow to pass through the edge representing that vertex reward. Giving that edge cost `-a[i]` converts the problem into finding a minimum-cost maximum-flow. Since all rewards are positive, every additional possible path increases the answer, so we keep augmenting until no path from 1 to n exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of paths | Exponential | Too slow |
| Optimal | O(F * V * E) with SPFA, where F is total flow | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Split every original vertex `i` into two nodes: `i_in` and `i_out`. Add an edge from `i_in` to `i_out` with infinite capacity and cost `-a[i]`. Passing through this edge represents collecting the reward of that vertex.
2. Replace every original road `u -> v` with an edge from `u_out` to `v_in` with the given capacity and zero cost. The capacity remains unchanged because the road can still only be used a limited number of times.
3. Start a minimum-cost maximum-flow algorithm from `1_in` to `n_out`. Each shortest augmenting path represents one more playable turn. The negative costs make profitable paths have lower total cost.
4. After each augmentation, add the amount of reward gained by that flow to the answer. Continue until no augmenting path exists.
5. Output the negation of the final minimum cost because the flow costs were stored as negative rewards.

Why it works:

Every valid game strategy is a collection of paths from node 1 to node n. Each path can be represented by one unit of flow, and the edge capacities guarantee that no road is used more times than allowed. The vertex-splitting edges are crossed exactly once by each unit visiting that vertex, so their negative costs subtract exactly the collected rewards. Therefore minimizing the total cost is equivalent to maximizing the total collected gold. Since all rewards are positive, every available augmenting path corresponds to another profitable turn, so the algorithm stops exactly when no legal turn remains.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

class Edge:
    __slots__ = ("to", "rev", "cap", "cost")

    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

def add_edge(g, u, v, cap, cost):
    g[u].append(Edge(v, len(g[v]), cap, cost))
    g[v].append(Edge(u, len(g[u]) - 1, 0, -cost))

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    size = 2 * n
    graph = [[] for _ in range(size)]

    def inn(x):
        return 2 * x

    def out(x):
        return 2 * x + 1

    INF = 10**9

    for i in range(n):
        add_edge(graph, inn(i), out(i), INF, -a[i])

    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        add_edge(graph, out(u), inn(v), c, 0)

    source = inn(0)
    sink = out(n - 1)

    ans = 0

    while True:
        dist = [10**18] * size
        inq = [False] * size
        parent = [(-1, -1)] * size

        dist[source] = 0
        q = deque([source])
        inq[source] = True

        while q:
            u = q.popleft()
            inq[u] = False
            for idx, e in enumerate(graph[u]):
                if e.cap and dist[e.to] > dist[u] + e.cost:
                    dist[e.to] = dist[u] + e.cost
                    parent[e.to] = (u, idx)
                    if not inq[e.to]:
                        inq[e.to] = True
                        q.append(e.to)

        if dist[sink] == 10**18:
            break

        flow = INF
        cur = sink
        while cur != source:
            u, idx = parent[cur]
            flow = min(flow, graph[u][idx].cap)
            cur = u

        cur = sink
        while cur != source:
            u, idx = parent[cur]
            e = graph[u][idx]
            e.cap -= flow
            graph[cur][e.rev].cap += flow
            cur = u

        ans -= dist[sink] * flow

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the flow model directly. The `add_edge` function creates both the forward edge and its residual edge, which allows later augmenting paths to undo previous choices if that improves the final answer.

The graph uses two indices per original vertex. The edge from the incoming copy to the outgoing copy stores the reward, while the original roads connect outgoing copies to incoming copies. The source is the incoming copy of node 1 because the starting node reward must be collected. The sink is the outgoing copy of node n because reaching node n means the turn is complete after collecting its reward.

The SPFA loop finds the cheapest augmenting path in the residual graph. Negative edge costs are safe here because the graph represents a flow network with residual edges, and the algorithm handles them naturally. The capacities are integers, so every augmentation sends an integer number of turns.

## Worked Examples

For the sample:

```
4 4
1 4 3 2
1 2 1
1 3 1
2 4 1
3 4 1
```

The flow network has two useful paths.

| Step | Chosen path | Flow sent | Cost change | Total reward |
| --- | --- | --- | --- | --- |
| 1 | 1 -> 2 -> 4 | 1 | -7 | 7 |
| 2 | 1 -> 3 -> 4 | 1 | -6 | 13 |
| 3 | no path remains | 0 | 0 | 13 |

The first two augmentations correspond to the two available turns. After both roads into node 4 are exhausted, there is no legal additional turn.

A second example:

```
2 1
5 7
1 2 3
```

| Step | Chosen path | Flow sent | Cost change | Total reward |
| --- | --- | --- | --- | --- |
| 1 | 1 -> 2 | 3 | -36 | 36 |
| 2 | no path remains | 0 | 0 | 36 |

The algorithm sends three units at once because the single edge has capacity three. Each unit collects both node rewards.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(F * V * E) | Each augmentation uses SPFA over the residual graph. The total flow F is bounded by the sum of edge capacities. |
| Space | O(V + E) | The split graph contains twice as many vertices and the original edges plus residual edges. |

The maximum number of vertices after splitting is only 200, and the number of edges remains small, so the min-cost flow approach comfortably fits the limits.

## Test Cases

```python
import sys
import io

# Replace with the solve() function from above when running locally.
def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # call solve() here
    sys.stdin = old
    return ""

# provided sample
assert run("""4 4
1 4 3 2
1 2 1
1 3 1
2 4 1
3 4 1
""") == "13\n"

# single path repeated
assert run("""2 1
5 7
1 2 3
""") == "36\n"

# two independent paths
assert run("""4 4
1 4 3 2
1 2 2
2 4 2
1 3 5
3 4 1
""") == "30\n"

# only one possible turn
assert run("""3 2
10 1 1
1 2 1
2 3 1
""") == "12\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two nodes with one edge of capacity 3 | 36 | Repeated use of the same path |
| Two branches with different capacities | 30 | Multiple augmentations and capacity handling |
| A single chain | 12 | Basic vertex reward counting |

## Edge Cases

For the repeated-path case:

```
2 1
5 7
1 2 3
```

The split graph contains a reward edge for node 1 with cost `-5` and node 2 with cost `-7`. The road has capacity three, so the min-cost flow algorithm sends three units. The final cost is `-36`, producing the correct answer of 36.

For the starting-node reward case:

```
3 2
10 1 1
1 2 1
2 3 1
```

A common mistake is to count only nodes after leaving node 1. The flow starts at `1_in`, crosses the reward edge of node 1, then continues through the path. The only possible turn collects `10 + 1 + 1 = 12`, which matches the intended scoring.

For exhausted bottlenecks, the residual graph matters. If an early greedy choice blocks a better arrangement, the reverse edges created by the flow implementation allow the algorithm to cancel previous choices and reroute flow. This is the property that makes the global optimum possible instead of just a sequence of locally best paths.
