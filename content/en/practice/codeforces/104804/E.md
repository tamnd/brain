---
title: "CF 104804E - \u0412\u044b\u043f\u0430\u0432\u0448\u0438\u0435 \u043c\u0435\u0448\u043a\u0438"
description: "We are given a network of cities connected by undirected roads. Each road can be used repeatedly, and each road initially contains a single collectible item with a value between 0 and 10. If the value is zero, the item is already gone and the road yields nothing."
date: "2026-06-28T13:25:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "E"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 86
verified: false
draft: false
---

[CF 104804E - \u0412\u044b\u043f\u0430\u0432\u0448\u0438\u0435 \u043c\u0435\u0448\u043a\u0438](https://codeforces.com/problemset/problem/104804/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a network of cities connected by undirected roads. Each road can be used repeatedly, and each road initially contains a single collectible item with a value between 0 and 10. If the value is zero, the item is already gone and the road yields nothing.

A traveler starts at city 1 and must make exactly $k$ moves along roads. Every time he traverses a road, he collects the value of that road, but only the first time it is used, because afterwards the item is no longer available.

The goal is to maximize the total collected value after exactly $k$ traversals, while freely choosing routes in the graph.

The graph is sparse in a very strong sense. Each city has at most 10 outgoing roads, so the branching factor is small. The number of moves is extremely small as well, bounded by 6. This combination is the key: the search depth is tiny even though the graph itself can be large.

If we tried to reason in terms of general graph DP over paths, we would immediately run into exponential explosion in $k$ and potentially in branching. However, $k \le 6$ changes the structure completely. Any method that explores states up to depth 6 is already feasible if each state expansion is constant or logarithmic.

The subtle difficulty is that roads can be reused but only pay once, which introduces a global “used edge” state. A naive path search that ignores this would overcount. On the other hand, explicitly tracking used edges is impossible because there are up to $10^4$ edges.

A few concrete pitfalls:

A naive DFS that simply sums edge weights along depth $k$ paths would incorrectly allow re-collecting the same road multiple times. For example, in a triangle 1-2-1 with value 10 on both edges, a 2-step walk 1→2→1 would incorrectly collect 20 if reuse is allowed in the code logic, but in reality the second traversal of the same edge should give 0.

Another failure mode is attempting shortest-path or longest-path style DP over nodes alone. That ignores whether a high-value edge was already consumed earlier in the route.

The correct solution must combine two facts: we only care about paths of length at most 6, and edge reuse only matters locally along a single traversal sequence.

## Approaches

A brute-force idea is to simulate all possible walks of length $k$ starting from node 1. At each step we choose one of the incident edges, and maintain a set of used edges to ensure we do not double count their values.

However, the number of states is disastrous. Each step branches up to 10 times, so we have up to $10^6$ paths for $k=6$, which is borderline but manageable in isolation. The real issue is that tracking used edges introduces combinatorial explosion: the same node reached via different edge-use histories is a different state, and the number of subsets of used edges grows exponentially.

The key observation is that $k$ is extremely small, so we can treat the solution as a layered expansion over time, but we must avoid storing edge subsets explicitly.

Instead, we observe that each edge can contribute at most once, and only if it is traversed the first time we use it. Since $k \le 6$, any walk uses at most 6 edges total. That means at most 6 distinct edges can ever matter in a single trajectory. This allows us to encode the “used edge set” implicitly along a single path rather than globally.

We perform a depth-limited search from node 1 up to depth $k$, and maintain a local visited-edge state only for the current recursion path. Since depth is at most 6, the number of edges stored is at most 6 as well. This keeps state management linear in $k$, not exponential in $m$.

The structure is essentially a DFS over states $(v, d)$, where $v$ is the current node and $d$ is how many moves have been used, with backtracking to mark edges as used/un-used along the path.

Because each step branches at most 10 ways, total work is bounded by $10^6$, and each transition is $O(1)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with edge-set tracking | O(10^k · 2^k) | O(2^k) | Too slow |
| Depth-limited DFS with local edge marking | O(10^k) | O(k) | Accepted |

## Algorithm Walkthrough

We solve the problem by enumerating all possible walks of exactly $k$ steps and accumulating rewards only the first time each edge is used along a path.

1. Build an adjacency list storing for each city its incident edges, including both endpoints and the value of the resource on that road. Since the graph is undirected, each edge is stored twice with a shared identifier. This allows us to mark an edge as used consistently regardless of direction.
2. Run a recursive DFS starting from node 1 with depth 0 and accumulated score 0.
3. At each recursive call, if the current depth equals $k$, update a global answer with the current score. This corresponds to completing one full itinerary.
4. Otherwise, iterate over all outgoing edges from the current node. For each edge, check whether it has already been used in the current path. If not used, traversing it yields its value; if used, it yields zero.
5. Temporarily mark the edge as used and recurse into the neighboring city with depth increased by 1 and updated score.
6. After returning from recursion, unmark the edge to restore the state for other branches. This backtracking is essential because each path must have an independent notion of which edges were already taken.
7. Continue until all depth-k paths have been explored, and return the maximum score observed.

### Why it works

The algorithm maintains a consistent invariant: at every recursion state, the set of marked edges exactly corresponds to the edges used along the current partial walk. This ensures that each path is evaluated with correct one-time edge rewards.

Because every possible sequence of $k$ edge traversals is explored exactly once, and each sequence is evaluated with correct edge usage semantics, the maximum over all explored states equals the optimal answer. No valid walk is omitted, and no invalid reuse is counted, so correctness follows from exhaustive enumeration over a correctly modeled state space.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, m, k = map(int, input().split())

g = [[] for _ in range(n + 1)]

edges = []
for i in range(m):
    a, b, c = map(int, input().split())
    g[a].append((b, c, i))
    g[b].append((a, c, i))
    edges.append(c)

used = [False] * m
ans = 0

def dfs(v, depth, score):
    global ans
    if depth == k:
        ans = max(ans, score)
        return

    for to, val, idx in g[v]:
        if not used[idx]:
            used[idx] = True
            dfs(to, depth + 1, score + val)
            used[idx] = False
        else:
            dfs(to, depth + 1, score)

dfs(1, 0, 0)
print(ans)
```

The adjacency list stores each undirected road with an index so that both directions share the same usage flag. This is crucial because treating directions independently would allow double counting the same road.

The recursion depth is explicitly bounded by $k$, and the score is threaded through the call stack rather than recomputed. The backtracking of the `used` array guarantees correctness of the local state.

One subtle point is that edges with value 0 still need to be explored, because they may lead to higher-value edges later. The algorithm naturally handles this since zero-value edges are included in the traversal but do not contribute to the score.

## Worked Examples

### Sample 1

Input:

```
5 4 3
1 2 1
2 3 2
3 4 3
4 5 1
```

This is a simple chain graph. Starting from 1, each move forces progress along the line.

| Step | Node | Depth | Score | Action |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | start |
| 1 | 2 | 1 | 1 | take 1-2 |
| 2 | 3 | 2 | 3 | take 2-3 |
| 3 | 4 | 3 | 6 | take 3-4 |

The DFS explores all paths of length 3, but all are equivalent due to the linear structure. The best achievable sum is 6.

This confirms the algorithm correctly accumulates edge values only once per traversal.

### Sample 2

Input:

```
6 6 6
1 2 3
2 3 3
3 4 5
4 5 1
5 6 7
6 1 3
```

This graph forms a cycle, allowing repeated circulation.

| Step | Node | Depth | Score | Action |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | start |
| 1 | 2 | 1 | 3 | 1-2 |
| 2 | 3 | 2 | 6 | 2-3 |
| 3 | 4 | 3 | 11 | 3-4 |
| 4 | 5 | 4 | 12 | 4-5 |
| 5 | 6 | 5 | 19 | 5-6 |
| 6 | 1 | 6 | 22 | 6-1 |

The DFS correctly recognizes that each edge contributes only once per path traversal, and the cycle is fully exploited.

This demonstrates that revisiting nodes is allowed, but edge reuse is carefully controlled, which is the core constraint of the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(10^k)$ | Each step branches into at most 10 edges, and depth is at most 6 |
| Space | $O(k)$ | recursion depth and at most k active edge marks |

The bound $k \le 6$ makes exponential enumeration over walks feasible. Even in the worst case, $10^6$ states is small enough for Python when each transition is constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.setrecursionlimit(10**7)

    n, m, k = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(n + 1)]
    edges = []

    for i in range(m):
        a, b, c = map(int, sys.stdin.readline().split())
        g[a].append((b, c, i))
        g[b].append((a, c, i))
        edges.append(c)

    used = [False] * m
    ans = 0

    def dfs(v, depth, score):
        nonlocal ans
        if depth == k:
            ans = max(ans, score)
            return
        for to, val, idx in g[v]:
            if not used[idx]:
                used[idx] = True
                dfs(to, depth + 1, score + val)
                used[idx] = False
            else:
                dfs(to, depth + 1, score)

    dfs(1, 0, 0)
    return str(ans)

# provided samples
assert run("""5 4 3
1 2 1
2 3 2
3 4 3
4 5 1
""") == "6"

assert run("""6 6 6
1 2 3
2 3 3
3 4 5
4 5 1
5 6 7
6 1 3
""") == "22"

# custom cases
assert run("""1 0 0
""") == "0", "no moves"

assert run("""2 1 1
1 2 5
""") == "5", "single edge"

assert run("""3 2 2
1 2 10
2 3 10
""") == "20", "simple chain"

assert run("""4 4 2
1 2 1
2 1 1
1 3 5
3 4 5
""") == "10", "choice of edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 | 0 | zero-move base case |
| 1-2 single edge | 5 | single traversal correctness |
| chain of 3 nodes | 20 | additive path accumulation |
| branching choice | 10 | correct selection of best path |

## Edge Cases

One edge case is when the graph contains cycles that allow revisiting nodes but reusing edges incorrectly if state is not tracked. For example, in a triangle 1-2-3-1 with all weights 10 and $k=3$, the correct answer is 30. The DFS marks each edge as used once per path, so the cycle contributes fully once per traversal sequence.

Another case is when multiple edges exist between the same pair of nodes. Since each edge has its own index, the algorithm correctly distinguishes them. Without indexing, one would incorrectly merge their usage state and lose valid paths.

A final case is when all edge weights are zero. The algorithm still explores all paths of length $k$, but every transition yields zero score. The maximum remains zero, which is correctly produced because updates only depend on accumulated score, not structure alone.
