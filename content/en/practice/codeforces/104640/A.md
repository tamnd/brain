---
title: "CF 104640A - \u041f\u043e\u0431\u0435\u0433 \u041c\u0430\u0439\u043b\u0437\u0430"
description: "We are given two separate directed-unweighted weighted graphs that share the same set of vertex labels from 1 to n."
date: "2026-06-29T16:49:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104640
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104640
solve_time_s: 77
verified: true
draft: false
---

[CF 104640A - \u041f\u043e\u0431\u0435\u0433 \u041c\u0430\u0439\u043b\u0437\u0430](https://codeforces.com/problemset/problem/104640/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two separate directed-unweighted weighted graphs that share the same set of vertex labels from 1 to n. You can think of them as two parallel cities, each with n skyscrapers positioned in identical coordinates, but with different allowed movement routes inside each city.

Inside the first city, some pairs of skyscrapers are connected by bidirectional edges with given travel times. The second city has its own independent set of bidirectional edges with their own travel times. In addition to these internal movements, there is a special transition: from any skyscraper i in the first city, you can instantly “switch worlds” to skyscraper i in the second city, paying a fixed cost x seconds, and the same works in reverse.

You start at skyscraper s in the first world and want to reach skyscraper t in the second world in minimum total time, combining internal moves and world switches.

The key structure is that this is not two separate shortest path problems. Movement between worlds couples the two graphs, so the optimal route may alternate between worlds multiple times if that reduces cost.

The constraints matter directly for algorithm choice. With n up to 100000 and up to 10^6 edges per world, the combined graph has on the order of a few million edges plus 100000 cross edges. Any solution that tries to recompute shortest paths per query or uses dense representations would fail. A linear or near-linear graph traversal with a logarithmic factor, such as Dijkstra with a heap, is the only realistic option.

A naive mistake is to try computing shortest paths in each world separately and then combining answers greedily. That fails because switching worlds can unlock strictly cheaper routes.

For example, suppose in world 1 the path from s to t is very expensive, but from s to some i is cheap, and in world 2 the path from i to t is cheap. The optimal route must switch worlds at i, which a separated computation would never consider correctly.

Another subtle failure case is assuming at most one world switch is enough. That is false because you might enter world 2 early to bypass a long segment in world 1, then return to world 1 through another index, and later switch back again if needed.

## Approaches

The brute-force mental model is to treat every possible sequence of moves across both worlds as a state space search. Each state is defined not only by the current node but also by the current world. From a state (node, world), you can traverse all edges in that world or switch to the other world at the same index cost x.

This forms a graph with 2n vertices. Every original edge contributes to exactly one layer, and every index i contributes a cross-edge between (i, world1) and (i, world2). Running shortest path on this expanded graph gives the correct answer.

The straightforward implementation already leads directly to Dijkstra’s algorithm. The key insight is that although the problem looks like two graphs, it is actually a single sparse weighted graph with 2n nodes. The cross-world transitions are just additional edges. Once this reformulation is seen, no further trick is required.

A slower alternative would be to attempt dynamic programming over “number of switches” or repeatedly relax paths between graphs, but that degenerates into repeated shortest path computations and is too slow under 10^6 edges.

The correct approach is simply one Dijkstra run over the combined graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over paths / repeated recomputation | Exponential / O(k·(n+m) log n) | O(n+m) | Too slow |
| Dijkstra on 2-layer graph | O((n + m1 + m2) log n) | O(n + m1 + m2) | Accepted |

## Algorithm Walkthrough

We construct a graph with 2n nodes. Node i represents skyscraper i in world 1, and node i + n represents skyscraper i in world 2.

We then add all edges from the first world inside the first half, all edges from the second world inside the second half, and add cross edges of cost x between i and i + n.

We run Dijkstra from the start node s in world 1 and compute distances to all nodes. The answer is the distance to t in world 2, or infinity if unreachable.

## Algorithm Walkthrough

1. Build a graph with 2n vertices, splitting the problem into two layers, one for each world. This separation allows us to encode world switching as explicit edges instead of special logic.
2. For every edge u, v, c in the first world, add a bidirectional edge between u and v in layer 1 with weight c. This preserves all allowed movements inside world 1 exactly as given.
3. For every edge u, v, c in the second world, add a bidirectional edge between u + n and v + n with weight c. This mirrors the second world into the second half of the graph.
4. For every index i from 1 to n, add two edges: i to i + n and i + n to i, each with cost x. This models the teleport between identical skyscrapers across worlds. The correctness relies on the fact that switching worlds does not change the index, only the layer.
5. Run Dijkstra starting from s in world 1, which is node s. This explores all possible combinations of intra-world moves and switches in increasing order of total time.
6. Extract the distance to node t in world 2, which is node t + n. If this distance is still infinite, output -1.

### Why it works

Any valid journey corresponds exactly to a path in the constructed 2n-node graph, because every movement type in the original problem is represented as an edge. Conversely, every path in the constructed graph corresponds to a legal sequence of moves in the original setting. Since all edges have non-negative weights, Dijkstra guarantees that the first time we finalize a node, we have found the minimum possible cost to reach it. This ensures the computed distance to (t in world 2) is the optimal travel time among all possible mixed-world routes.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def solve():
    n, x = map(int, input().split())
    
    m1 = int(input())
    g = [[] for _ in range(2 * n)]
    
    for _ in range(m1):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, c))
        g[v].append((u, c))
    
    m2 = int(input())
    for _ in range(m2):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        u += n
        v += n
        g[u].append((v, c))
        g[v].append((u, c))
    
    for i in range(n):
        g[i].append((i + n, x))
        g[i + n].append((i, x))
    
    s, t = map(int, input().split())
    s -= 1
    t -= 1
    
    dist = [INF] * (2 * n)
    dist[s] = 0
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t + n:
            break
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    
    ans = dist[t + n]
    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the 2-layer graph construction. The adjacency list `g` holds both worlds simultaneously, with indices [0, n-1] representing world 1 and [n, 2n-1] representing world 2.

The most delicate part is index handling. All vertices are converted to zero-based indexing, and the second world is shifted by +n. Cross edges are added uniformly for every i, ensuring symmetry between switching directions.

The Dijkstra loop uses a standard priority queue. The early break when reaching the target is optional but safe because Dijkstra guarantees that the first time we pop the target with minimal distance, it is optimal.

## Worked Examples

### Sample 1

We track only key state transitions conceptually, focusing on shortest distances discovered.

| Step | Node processed | Distance | Key relaxation effect |
| --- | --- | --- | --- |
| 1 | s (world 1) | 0 | Initializes reachability |
| 2 | neighbors in world 1 | various | Expands within first graph |
| 3 | switch to world 2 nodes | x | Introduces entry into second world |
| 4 | internal world 2 traversal | improves | Finds cheaper route toward t |
| final | t in world 2 | 6 | Optimal meeting time |

This trace shows that the optimal path may require entering world 2 early rather than finishing world 1 first.

### Constructed Sample 2

Let n = 3, x = 5.

World 1 edges:

1-2 cost 2, 2-3 cost 100

World 2 edges:

1-2 cost 1, 2-3 cost 1

Start s = 1, t = 3.

The algorithm finds:

1 → switch to world 2 at cost 5 → 1 in world 2

Then 1 → 2 → 3 cost 2

Total = 5 + 2 = 7

A world-1-only route costs 2 + 100 = 102, showing why switching early dominates.

| Step | Position | Cost |
| --- | --- | --- |
| start | 1 (w1) | 0 |
| switch | 1 (w2) | 5 |
| move | 2 (w2) | 6 |
| move | 3 (w2) | 7 |

This confirms that optimal paths heavily depend on inter-world transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m1 + m2) log n) | Dijkstra over 2n nodes with all edges in a sparse heap |
| Space | O(n + m1 + m2) | adjacency list for both worlds plus cross edges |

The total number of edges is linear in the input size, so the logarithmic factor from the priority queue is the only overhead. With m up to 2·10^6, this comfortably fits within typical limits for Python if implemented with efficient I/O and adjacency lists.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import inf
    import heapq

    input = sys.stdin.readline

    INF = 10**30

    n, x = map(int, input().split())
    m1 = int(input())
    g = [[] for _ in range(2 * n)]

    for _ in range(m1):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        g[u].append((v, c))
        g[v].append((u, c))

    m2 = int(input())
    for _ in range(m2):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        u += n; v += n
        g[u].append((v, c))
        g[v].append((u, c))

    for i in range(n):
        g[i].append((i + n, x))
        g[i + n].append((i, x))

    s, t = map(int, input().split())
    s -= 1; t -= 1

    dist = [INF] * (2 * n)
    dist[s] = 0
    pq = [(0, s)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    ans = dist[t + n]
    return "-1" if ans == INF else str(ans)

# provided sample
assert run("""6 2
7
1 3 2
6 4 1
4 1 5
5 3 2
1 2 1
1 5 4
2 3 4
6
4 2 1
2 1 5
5 2 3
3 1 5
1 5 4
2 6 1
5 6
""").strip() == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | 6 | correctness of mixed-world routing |
| n=1, x=10, no edges, s=t=1 | 10 | single switch handling |
| two nodes only direct second-world edge better | small value | cross-world advantage |
| disconnected graphs | -1 | unreachable detection |

## Edge Cases

One edge case is when there are no intra-world edges at all. The only possible moves are world switches, so the path becomes a simple chain of alternating switches. The algorithm handles this because Dijkstra still explores cross edges normally, and the answer becomes multiples of x if reachable.

Another case is when the optimal path requires multiple switches. For instance, using world 2 to shortcut part of the journey, returning to world 1 to reach another region, then switching again. The 2n-node graph naturally allows this, and Dijkstra explores such sequences without restriction.

A final case is when s equals t. Even then, the answer is not necessarily zero, because the destination is specifically in world 2. The algorithm correctly forces at least one transition unless s already equals t and a zero-cost path exists in world 2 without leaving.
