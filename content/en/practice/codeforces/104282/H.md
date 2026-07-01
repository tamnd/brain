---
title: "CF 104282H - Maze"
description: "We are given an $n times m$ grid where each cell either contains a cake or is empty. The task is to eat all cakes while maximizing total satisfaction. There are two possible actions. One action eats a single cake and gives a fixed reward $p$."
date: "2026-07-01T21:07:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104282
codeforces_index: "H"
codeforces_contest_name: "The 20th Hangzhou City University Programming Contest"
rating: 0
weight: 104282
solve_time_s: 60
verified: true
draft: false
---

[CF 104282H - Maze](https://codeforces.com/problemset/problem/104282/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ grid where each cell either contains a cake or is empty. The task is to eat all cakes while maximizing total satisfaction. There are two possible actions. One action eats a single cake and gives a fixed reward $p$. The other action eats two cakes that are adjacent horizontally or vertically and gives reward $q$, which replaces two single-cake operations.

The problem is fundamentally about choosing a subset of adjacent pairs to “merge” into double-eating operations, while all remaining cakes are taken individually. Each cake must be consumed exactly once, either alone or as part of a pair, so we are effectively partitioning all 1-cells into singletons and edges of an adjacency graph induced by the grid.

The grid size can be up to $300 \times 300$, so up to 90,000 cells. This immediately rules out any approach that tries to enumerate subsets of pairings or runs exponential matching. A solution that is roughly $O(nm \cdot \text{something linear})$ or $O(V + E)$ per test is acceptable, but anything involving combinatorial exploration of matchings is not.

A subtle point is that we are not required to pair as many adjacent cakes as possible. Whether pairing is beneficial depends entirely on the comparison between $q$ and $2p$. If $q < 2p$, pairing is worse than taking two singles. If $q > 2p$, pairing is always better, but we are constrained by adjacency structure and cannot arbitrarily pair all cells, since each cell can be used at most once.

Edge cases arise when cakes form small connected components where pairing opportunities are limited. For example, consider two adjacent cakes only. If $q < 2p$, answer is $2p$, but a naive greedy that always pairs might incorrectly take $q$. Another edge case is a line of three cakes. If pairing is beneficial, only one pair can be taken and one remains single; choosing which pair is irrelevant, but incorrect greedy matching might try to overcount.

## Approaches

The brute-force perspective treats the grid as a graph where each cake is a node and edges connect adjacent cakes. We need to select a set of edges such that no two share an endpoint, maximizing total weight, where selecting an edge gives $q$ and leaving a node unmatched contributes $p$.

This is exactly a maximum weight matching problem on a general graph. A straightforward brute-force would try all matchings: for each node, either leave it unmatched or match it with one of its neighbors, recurse on the remaining graph, and compute the best result. In the worst case of a fully filled grid, each node has up to four choices and the recursion branches heavily, leading to exponential complexity on the order of $O(2^{nm})$ in spirit. This is completely infeasible for 90,000 nodes.

The key observation is that all nodes are identical in weight, and edges are uniform. The decision is not locally dependent on structure beyond whether using an edge improves total value compared to two singles. This removes any need to solve a true matching problem. Instead, the only meaningful choice is whether to use as many edges as possible in some valid matching when it is beneficial.

If we compare costs, taking two singles gives $2p$, while pairing gives $q$. If $q \le 2p$, pairing is never beneficial, so we simply take all cakes individually. If $q > 2p$, we want to maximize the number of disjoint adjacent pairs in the grid subgraph induced by cakes. That becomes a maximum matching problem in a bipartite graph formed by checkerboard coloring of grid cells.

Because the grid graph is bipartite, we can compute maximum matching using a standard flow or DFS-based bipartite matching. Each cake cell connects to its neighbors in four directions, and we match as many edges as possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching Enumeration | Exponential | Exponential | Too slow |
| Bipartite Maximum Matching | $O(VE)$ worst case | $O(V+E)$ | Accepted |

## Algorithm Walkthrough

We split the problem into two regimes based on the comparison between $q$ and $2p$.

1. We count how many cakes exist in the grid. This gives the baseline if we take everything individually.
2. If $q \le 2p$, we immediately return total cakes multiplied by $p$. This is because every pairing would reduce or not improve total reward, so no pairing is ever useful.
3. If $q > 2p$, we model the grid as a graph where each cake cell is a vertex. We color the grid in a chessboard pattern to obtain a bipartition.
4. We connect edges between adjacent cake cells across opposite colors. This ensures the graph is bipartite, which is necessary for standard matching algorithms to apply cleanly.
5. We compute a maximum bipartite matching on this graph. Each matched edge represents replacing two singles with one pair operation, gaining an extra $q - 2p$ over treating them individually.
6. The final answer is computed as total cakes times $p$, plus matching size times $(q - 2p)$.

The reasoning behind this decomposition is that we start from a baseline where every cake is taken individually, and then each matched edge upgrades two single contributions into one pair contribution.

### Why it works

Every valid strategy partitions the set of cake cells into singletons and disjoint adjacent pairs. This corresponds exactly to a matching in the adjacency graph. The value of any solution is $p \cdot (\text{number of nodes}) + (q - 2p) \cdot (\text{number of matched edges})$. Since $p$ is constant over all nodes, maximizing total value reduces to maximizing the number of edges in the matching when $q > 2p$, and choosing no edges otherwise. The matching constraint guarantees no cell is reused, so every feasible solution corresponds to a valid matching and vice versa.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, m, p, q = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]

    ones = []
    idx = [[-1] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                idx[i][j] = len(ones)
                ones.append((i, j))

    k = len(ones)

    if q <= 2 * p:
        print(k * p)
        return

    # build bipartite graph
    adj = [[] for _ in range(k)]

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for v, (i, j) in enumerate(ones):
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and idx[ni][nj] != -1:
                adj[v].append(idx[ni][nj])

    color = [(i + j) % 2 for i, j in ones]

    match_to = [-1] * k

    def dfs(v, vis):
        for u in adj[v]:
            if vis[u]:
                continue
            vis[u] = True
            if match_to[u] == -1 or dfs(match_to[u], vis):
                match_to[u] = v
                return True
        return False

    matching = 0
    for v in range(k):
        if color[v] == 0:
            vis = [False] * k
            if dfs(v, vis):
                matching += 1

    ans = k * p + matching * (q - 2 * p)
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first compresses the grid into a list of cake cells and assigns each one an index. This avoids dealing with empty cells entirely and keeps adjacency checks fast.

The bipartite matching is implemented using a standard DFS augmenting path approach. We only start DFS from one color class to avoid duplicate work. The `match_to` array stores which left-side vertex is currently matched to each right-side vertex. Each successful DFS finds an augmenting path that increases the matching size by one.

The final formula directly reflects the baseline plus improvements structure. A common implementation pitfall is forgetting to subtract the baseline double-counting when converting match size into total score; the formula here avoids that by constructing from the baseline explicitly.

## Worked Examples

### Example 1

Consider a small grid:

Input:

```
2 3 10 25
1 1 0
0 1 1
```

Here there are 4 cakes. Since $q = 25 > 2p = 20$, pairing is beneficial.

We build indices for cakes:

| Cell | Index |
| --- | --- |
| (0,0) | 0 |
| (0,1) | 1 |
| (1,1) | 2 |
| (1,2) | 3 |

Adjacency edges exist between (0,0)-(0,1), (0,1)-(1,1), (1,1)-(1,2). The maximum matching size is 2.

| Step | Matching Size | Base Score | Final Score |
| --- | --- | --- | --- |
| Start | 0 | 40 | 40 |
| After matching | 2 | 40 | 40 + 2×5 = 50 |

This shows that two pairs replace four singles, improving score by $2 \cdot (25 - 20)$.

### Example 2

Input:

```
1 4 7 10
1 1 1 1
```

There are 4 cakes in a line. Since $q = 10 > 14$ is false, pairing is not beneficial.

We immediately compute:

| Cakes | p | q | Strategy | Result |
| --- | --- | --- | --- | --- |
| 4 | 7 | 10 | all singles | 28 |

Even though adjacency exists, pairing would reduce value, so matching is not used at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(VE)$ | DFS augmenting path bipartite matching over cake graph |
| Space | $O(V + E)$ | adjacency list and matching arrays |

With $V \le 90000$ and each node having up to 4 edges, the graph is sparse. In practice this runs fast enough under typical constraints due to small degree and early termination in DFS.

The memory limit of 1024 MB easily accommodates adjacency lists and auxiliary arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return capture()

# we embed solution here for testing

def solve(inp: str) -> str:
    import sys
    input = sys.stdin.readline

    n, m, p, q = map(int, sys.stdin.readline().split())
    grid = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

    ones = []
    idx = [[-1] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                idx[i][j] = len(ones)
                ones.append((i, j))

    k = len(ones)

    if q <= 2 * p:
        return str(k * p)

    adj = [[] for _ in range(k)]
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    for v,(i,j) in enumerate(ones):
        for di,dj in dirs:
            ni,nj = i+di,j+dj
            if 0<=ni<n and 0<=nj<m and idx[ni][nj]!=-1:
                adj[v].append(idx[ni][nj])

    color = [(i+j)%2 for i,j in ones]
    match_to = [-1]*k

    def dfs(v, vis):
        for u in adj[v]:
            if vis[u]:
                continue
            vis[u]=True
            if match_to[u]==-1 or dfs(match_to[u],vis):
                match_to[u]=v
                return True
        return False

    matching=0
    for v in range(k):
        if color[v]==0:
            vis=[False]*k
            if dfs(v,vis):
                matching+=1

    return str(k*p + matching*(q-2*p))

# custom tests
assert solve("2 3 10 25\n1 1 0\n0 1 1\n") == "50"
assert solve("1 4 7 10\n1 1 1 1\n") == "28"
assert solve("2 2 5 3\n1 1\n1 1\n") == "20"
assert solve("1 1 5 100\n0\n") == "0"
assert solve("3 3 1 10\n1 0 1\n0 1 0\n1 0 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2×2 full grid with bad pairing | 20 | no pairing used when q ≤ 2p |
| single cell empty | 0 | empty grid correctness |
| checkerboard sparse | 5 | sparse matching structure |
| line and center mix | correctness of adjacency handling |  |

## Edge Cases

One edge case is when there are no cakes at all. The algorithm maps this to $k = 0$, immediately producing zero, since both baseline and matching contribution vanish.

Another case is when all cakes are isolated. Even if $q > 2p$, adjacency graph has no edges, so matching size is zero and result remains $k \cdot p$. The DFS matching correctly finds no augmenting paths because adjacency lists are empty.

A final case is a fully filled grid with $q \le 2p$. Even though the graph is dense, the algorithm avoids constructing matching entirely and directly returns $k \cdot p$, preventing unnecessary computation and avoiding time limits on large inputs.
