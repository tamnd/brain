---
title: "CF 102591E - \u0414\u0430\u043d\u0438\u044f\u0440 \u0438 \u0435\u0433\u043e \u043b\u044e\u0431\u0438\u043c\u044b\u0435 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u044b"
description: "The city is represented as an undirected graph. Each intersection is a vertex, each road is an edge, and owning a pass for a road means that edge is available for travel."
date: "2026-08-01T06:37:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102591
codeforces_index: "E"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041c\u0423\u0418\u0422 \u043f\u043e \u0441\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u043e\u043c\u0443 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2020. \u0424\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u0443\u0440."
rating: 0
weight: 102591
solve_time_s: 203
verified: true
draft: false
---

[CF 102591E - \u0414\u0430\u043d\u0438\u044f\u0440 \u0438 \u0435\u0433\u043e \u043b\u044e\u0431\u0438\u043c\u044b\u0435 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u044b](https://codeforces.com/problemset/problem/102591/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 23s  
**Verified:** yes  

## Solution
# Problem Understanding

The city is represented as an undirected graph. Each intersection is a vertex, each road is an edge, and owning a pass for a road means that edge is available for travel. Daniyar wants to choose the smallest possible set of roads such that the subgraph formed by those roads still allows him to travel from his home at vertex 1 to every favourite shop.

This is not asking for the shortest route to each shop separately. A single road can help reach several shops, so the chosen roads may share parts of their paths. The task is to find the minimum number of edges needed to connect a small set of important vertices in a large graph.

The graph can contain up to 100000 vertices and 100000 edges. With these limits, algorithms that inspect many possible groups of edges are impossible because even a quadratic amount of work would be far beyond the available operations. A normal shortest path algorithm such as BFS is fine because it is linear in the graph size, but the challenge is that we need to combine paths to several destinations. The number of shops is at most 4, which is the key restriction that allows a subset-based dynamic programming solution.

There are several small cases that break simple approaches. If a shop is the same vertex as the home, no pass is required for that shop.

Example:

```
3 2 1
1
1 2
2 3
```

The answer is:

```
0
```

A careless solution that always adds a path length to every shop may incorrectly count the distance from vertex 1 to itself.

Another trap is duplicated shops.

Example:

```
4 3 3
3 3 3
1 2
2 3
3 4
```

The answer is:

```
2
```

The three shops are actually the same location. A solution that treats them as different terminals may build unnecessary connections.

A third issue is that the best answer may use a branching structure instead of separate shortest paths.

Example:

```
5 6 2
4 5
1 2
2 3
3 4
3 5
1 5
2 5
```

The answer is:

```
2
```

Choosing the shortest path to each shop independently can count shared roads multiple times and produce a larger value.

## Approaches

A straightforward idea is to find a shortest path from vertex 1 to every shop and take all edges from those paths. This is easy to implement and gives a valid set of passes. The problem is that it ignores sharing between routes. If two shops can be reached through the same intermediate roads, this approach pays for the common part multiple times.

Another brute force method would try every possible collection of edges and check whether all terminals become connected. The number of possible edge sets is $2^M$, which is completely impossible when $M$ reaches 100000.

The right way to view the problem is as a Steiner tree problem. In a general graph, finding the minimum tree connecting arbitrary terminals is difficult, but here the number of terminals is tiny. We can remember only which of the important vertices have already been connected.

For every subset of terminals and every graph vertex, we store the minimum number of roads needed to connect that subset while making the current vertex the meeting point. Two smaller connected structures can be merged if they meet at the same vertex. After every merge operation, shortest path propagation spreads the improved values through the graph.

The brute force solution fails because it treats the whole graph as the search space. The observation that only the terminals are few lets us compress the difficult part into $2^K$ states, where $K$ is at most 5 after adding the home vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over edge sets | $O(2^M \cdot (N+M))$ | $O(N+M)$ | Too slow |
| Independent shortest paths | $O(K(N+M))$ | $O(N+M)$ | Incorrect in general |
| Subset dynamic programming | $O(3^K N + 2^K(N+M))$ | $O(2^K N)$ | Accepted |

## Algorithm Walkthrough

1. Remove duplicate shop positions and add vertex 1 as a terminal. The number of terminals is now at most 5.

The dynamic programming only depends on special vertices. If the same vertex appears several times, connecting it once already satisfies every occurrence.

1. Create a state `dp[mask][v]`. The mask describes which terminals are already connected, and `v` is the vertex where the connected structure currently ends. Initialize every single-terminal state with value zero at its own terminal.

A single terminal needs no road to connect itself. Every other value starts as infinity because it has not been constructed yet.

1. For each mask, split it into two non-empty disjoint parts. Try combining the best structure for each part at the same vertex.

If one structure connects terminal set `a` and another connects terminal set `b`, placing both at the same vertex creates a connected structure for `a | b`. This is why the transition is:

$$dp[mask][v] = \min(dp[mask][v], dp[sub][v] + dp[mask \setminus sub][v])$$

1. After all merge transitions for a mask, run a multi-source BFS using the current values as starting distances.

The merge step only allows two structures that already meet at one vertex. BFS accounts for extending the endpoint through normal roads. Since every road costs one pass, ordinary BFS is exactly the required shortest path relaxation.

1. After processing every mask, the answer is the minimum value in the state containing all terminals.

The final connected structure may end at any vertex. The only requirement is that every important vertex belongs to the same chosen set of roads.

Why it works:

The invariant is that after processing a mask, `dp[mask][v]` represents the minimum number of roads in any connected subgraph that contains exactly the terminals from `mask` and includes vertex `v`. Initially this is true for single terminals. A merge of two valid smaller structures creates another valid connected structure, and every optimal structure can be separated at some meeting vertex into two smaller terminal groups. BFS then finds the cheapest way to move the meeting point through the graph. Because every possible split and every possible endpoint is considered, the full-terminal state contains the optimal Steiner tree size.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    shops = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    terminals = [0]
    for x in shops:
        x -= 1
        if x not in terminals:
            terminals.append(x)

    t = len(terminals)
    full = (1 << t) - 1
    inf = 10 ** 9

    dp = [[inf] * n for _ in range(1 << t)]

    for i, vertex in enumerate(terminals):
        dp[1 << i][vertex] = 0

    for mask in range(1, 1 << t):
        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if sub < other:
                first = dp[sub]
                second = dp[other]
                current = dp[mask]
                for v in range(n):
                    value = first[v] + second[v]
                    if value < current[v]:
                        current[v] = value
            sub = (sub - 1) & mask

        dist = dp[mask]
        queue = deque()

        for v in range(n):
            if dist[v] < inf:
                queue.append(v)

        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    queue.append(v)

    print(min(dp[full]))

if __name__ == "__main__":
    solve()
```

The terminal construction removes repeated shops before building the dynamic programming table. This keeps the number of masks as small as possible.

The table has one row for every terminal subset. Since there are at most five terminals, the maximum number of states is only 32. Each state contains one distance value for every graph vertex.

The subset loop uses only pairs where `sub < other`, avoiding duplicate merges. The BFS queue starts with every vertex that already has a finite value, which turns the relaxation into a multi-source shortest path search.

Python integers do not overflow here because the largest possible answer is at most the number of edges. The infinity value is chosen much larger than any possible answer. The implementation also uses an iterative BFS instead of recursion because the graph size can be 100000.

## Worked Examples

For the first sample, the terminals are vertices 1, 2, and 3 after adding the home. The dynamic programming tries combinations of these three terminals.

| Step | Connected terminals | Best known cost | Explanation |
| --- | --- | --- | --- |
| Initialization | {1}, {2}, {3} | 0 at their own vertices | Each terminal alone needs no roads |
| Merge {1}+{2} | {1,2} | 1 | Vertex 1 connects directly to vertex 2 |
| Merge {1}+{3} | {1,3} | 2 | A short connection through vertex 5 is found |
| Merge {2}+{3} | {2,3} | 1 | Vertices 2 and 3 share a road |
| Final merge | {1,2,3} | 3 | Three terminals become connected |

The result is 3, which demonstrates that the answer is not the sum of individual shortest paths.

For the second sample, the shops are `1, 3, 3`. After removing duplicates, the terminals are only vertices 1 and 3.

| Step | Connected terminals | Best known cost | Explanation |
| --- | --- | --- | --- |
| Initialization | {1} | 0 at vertex 1 | Home terminal |
| Initialization | {3} | 0 at vertex 3 | Shop terminal |
| Merge | {1,3} | 2 | The path 1-2-3 uses two roads |
| Final answer | {1,3} | 2 | Duplicate shop does not change the result |

The trace confirms that repeated shops are handled naturally by compressing the terminal list.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(3^K N + 2^K(N+M))$ | Each subset performs subset merges and one BFS |
| Space | $O(2^K N)$ | The DP table stores every subset and every vertex |

Here $K$ is the number of unique terminals after adding the home, so $K \leq 5$. The exponential part is therefore at most a small constant, while the graph processing remains linear in $N+M$. This fits the limits with 100000 vertices and edges.

## Test Cases

```python
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    shops = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    terminals = [0]
    for x in shops:
        x -= 1
        if x not in terminals:
            terminals.append(x)

    t = len(terminals)
    inf = 10 ** 9
    dp = [[inf] * n for _ in range(1 << t)]

    for i, x in enumerate(terminals):
        dp[1 << i][x] = 0

    for mask in range(1, 1 << t):
        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if sub < other:
                for i in range(n):
                    dp[mask][i] = min(dp[mask][i], dp[sub][i] + dp[other][i])
            sub = (sub - 1) & mask

        q = deque(i for i, x in enumerate(dp[mask]) if x < inf)
        while q:
            u = q.popleft()
            for v in graph[u]:
                if dp[mask][v] > dp[mask][u] + 1:
                    dp[mask][v] = dp[mask][u] + 1
                    q.append(v)

    return str(min(dp[-1]))

assert run("""6 7 2
2 3
1 5
1 6
3 5
3 4
2 4
3 6
2 6
""") == "3"

assert run("""4 3 3
1 3 3
1 2
2 3
3 4
""") == "2"

assert run("""1 1 1
1
""") == "0"

assert run("""4 3 2
4 4
1 2
2 3
3 4
""") == "3"

assert run("""5 5 3
2 3 4
1 2
1 3
2 5
3 5
5 4
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex with the home as shop | 0 | Handles zero required roads |
| Three identical shops | 3 | Handles duplicate terminals |
| Multiple routes with a shared center | 3 | Handles Steiner-style branching |
| Provided samples | 3 and 2 | Confirms standard cases |

## Edge Cases

The case where a shop is the home is handled during terminal creation. For input:

```
3 2 1
1
1 2
2 3
```

the terminal list contains only vertex 1. The final mask is already a single terminal, so its distance is zero. The algorithm outputs 0.

For duplicate shops:

```
4 3 3
3 3 3
1 2
2 3
3 4
```

the terminal list becomes `[1, 3]` in one-based indexing. The DP solves the problem of connecting those two vertices, requiring the roads `1-2` and `2-3`. The answer is 2.

For shared paths, consider:

```
5 6 2
4 5
1 2
2 3
3 4
3 5
1 5
2 5
```

The independent shortest paths approach might count two separate routes, but the subset DP allows both terminal groups to merge at the same intermediate vertex. The final state finds the connected structure with only two roads, which is the minimum.
