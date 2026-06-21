---
title: "CF 106456C - Crossing"
description: "We are given a grid where each cell contains a non-negative integer. A traveler starts at the top-left cell and must reach the bottom-right cell. Movement is allowed in four directions and cells may be revisited any number of times."
date: "2026-06-21T16:27:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106456
codeforces_index: "C"
codeforces_contest_name: "The 15th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 106456
solve_time_s: 72
verified: true
draft: false
---

[CF 106456C - Crossing](https://codeforces.com/problemset/problem/106456/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid where each cell contains a non-negative integer. A traveler starts at the top-left cell and must reach the bottom-right cell. Movement is allowed in four directions and cells may be revisited any number of times.

A path is not evaluated by its length or cost in the usual sense. Instead, we take the sequence of values encountered along the path, including repeats when a cell is revisited. From this sequence we compute two quantities: the bitwise OR over all visited values, and the bitwise AND over all visited values.

The goal is to choose any valid path from start to end that first minimizes the OR of all visited values. Among all paths that achieve this minimum OR, we then maximize the AND.

The key difficulty is that revisiting nodes does not change OR or AND in a beneficial way. Repeating a value in OR or AND is idempotent, so the only effect of revisits is to help connectivity without introducing new values. This means the problem is fundamentally about selecting a connected set of grid cells that contains both endpoints, where connectivity is in the grid sense.

Each chosen cell contributes its value into the OR and AND aggregates. The OR of the path is exactly the bitwise OR of all values in the chosen connected region, while the AND is the bitwise AND of all values in that region.

The constraints imply up to 2 × 10^5 cells total across test cases, and values fit within 30 bits. This rules out anything that explores all paths explicitly, since the number of paths in a grid grows exponentially. Even shortest path variants on expanded states would be too large if we encode bitmasks directly per state.

A subtle point appears in both objectives. The OR objective depends on the union of bits across all visited nodes, while the AND objective depends on intersection of bits across all visited nodes. These two objectives behave in opposite monotonic directions, which makes a direct single DP formulation difficult.

One failure case for naive reasoning is assuming a shortest path suffices. For example, a path that minimizes steps might include a high-value cell early, increasing OR unnecessarily.

Another failure case is treating OR minimization as independent per step. For instance, locally choosing the neighbor with smallest value can trap the path into needing high-bit cells later, increasing OR globally.

## Approaches

A brute-force approach would enumerate all possible simple paths from the start to the end and compute OR and AND for each. Even if we disallow revisits, the number of simple paths in a grid is exponential in n and m, making this immediately infeasible.

A more structured brute-force idea is to treat each path as a sequence of decisions and run a DFS or BFS over states defined by position and visited set. This still explodes because the visited set alone has size 2^(nm).

The key observation is that both OR and AND depend only on the set of visited cells, not on order or multiplicity. Any cycle in a path does not change the final OR or AND, so we can compress any valid walk into a spanning tree over the visited set. This reduces the problem to selecting a connected set of cells containing both endpoints.

We then separate the two objectives.

For the OR minimization, think of each bit independently. If we decide a candidate OR mask B, then we are restricting ourselves to using only cells whose values do not contain bits outside B. The question becomes whether (1,1) and (n,m) are connected in the subgraph induced by valid cells. The optimal OR is the smallest mask that still allows connectivity.

Since there are only 30 bits, we can greedily start with all bits set and try removing them one by one from high to low. After tentatively removing a bit, we check connectivity using BFS. If connectivity is preserved, the bit is truly unnecessary in the OR.

After fixing the minimal OR mask, we move to the AND objective. Now we only consider cells allowed by that OR mask. Among these, we want a path maximizing bitwise AND of all visited values. A bit can appear in the final AND only if every cell on the path contains that bit. So for a candidate AND mask C, we need a path where every visited cell contains all bits of C.

This again becomes a connectivity check in a filtered graph, so we can greedily build the AND mask bit by bit, testing feasibility each time using BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Paths | Exponential | Exponential | Too slow |
| Bitmask Greedy with BFS | O(60 × n × m × 30) | O(n × m) | Accepted |

## Algorithm Walkthrough

### OR minimization phase

1. Start with a mask B where all 30 bits are set. This guarantees every cell is initially allowed.
2. Process bits from high to low. For each bit, tentatively remove it from B, forming a candidate B'.
3. Run BFS from the start, only visiting cells whose value contains no bit outside B'. If the end is reachable, keep the bit removed; otherwise restore it.
4. After all bits are processed, B is the minimum OR mask that still allows a valid path.

The BFS step is checking a constrained connectivity problem: whether the grid remains connected when we delete all cells whose values are incompatible with the current mask.

### AND maximization phase

1. Restrict the grid to only cells compatible with B.
2. Initialize AND mask C as 0.
3. For each bit from high to low, tentatively set it in C to form C'.
4. Run BFS again, but now only allow traversal through cells whose value includes all bits in C'. If connectivity holds, keep the bit; otherwise discard it.
5. The final C is the maximum AND achievable among all paths respecting the minimal OR constraint.

### Why it works

The correctness relies on the fact that both objectives reduce to feasibility of connectivity under bitwise filters. For OR, feasibility depends on excluding forbidden bits from all visited nodes. For AND, feasibility depends on enforcing required bits in all visited nodes. Both constraints define a monotone property over bitsets: adding constraints only shrinks the set of usable cells, never expands it. This monotonicity makes greedy bit fixing valid because once a bit is proven unnecessary (or necessary), that decision remains consistent for all subsequent choices.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def bfs(n, m, grid, allowed_mask, require_mask):
    if (grid[0][0] & allowed_mask) != grid[0][0]:
        return False
    if (grid[0][0] & require_mask) != require_mask:
        return False
    if (grid[n-1][m-1] & allowed_mask) != grid[n-1][m-1]:
        return False
    if (grid[n-1][m-1] & require_mask) != require_mask:
        return False

    vis = [[False]*m for _ in range(n)]
    q = deque([(0,0)])
    vis[0][0] = True

    while q:
        x,y = q.popleft()
        if x == n-1 and y == m-1:
            return True
        for dx,dy in DIRS:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < m and not vis[nx][ny]:
                v = grid[nx][ny]
                if (v & allowed_mask) == v and (v & require_mask) == require_mask:
                    vis[nx][ny] = True
                    q.append((nx, ny))
    return vis[n-1][m-1]

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]

    full = (1 << 30) - 1

    # OR minimization
    B = full
    for b in range(29, -1, -1):
        if B & (1 << b):
            B2 = B ^ (1 << b)
            if bfs(n, m, grid, B2, 0):
                B = B2

    # AND maximization
    C = 0
    for b in range(29, -1, -1):
        C2 = C | (1 << b)
        if bfs(n, m, grid, B, C2):
            C = C2

    print(B, C)
```

The BFS function is shared between both phases, but it enforces different constraints depending on the phase. In the OR phase, require_mask is zero and only forbidden bits matter. In the AND phase, allowed_mask is fixed and require_mask enforces mandatory bits that every visited node must contain.

A subtle implementation detail is the early rejection of start and end nodes before BFS. This avoids unnecessary traversal when either endpoint already violates constraints. Another important detail is that both constraints must hold simultaneously inside the BFS transition check, otherwise we would accidentally allow invalid intermediate nodes.

## Worked Examples

Consider a small grid where different paths force inclusion of different bits. The algorithm does not care about geometry directly; it only cares about whether filtering by bits preserves connectivity.

For the OR phase, suppose removing a bit disconnects start and end. The BFS will fail to reach the target, and the bit is restored. This directly demonstrates that every kept bit is structurally necessary for connectivity.

For the AND phase, suppose a bit is present in start but missing in some intermediate region required for connectivity. Even if endpoints satisfy the bit, BFS will fail because every step must maintain the bit constraint. This demonstrates why AND is determined by a global intersection constraint rather than endpoint values alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(60 × n × m) per test case | Each of up to 30 bits is checked twice with BFS, each BFS visits each cell once |
| Space | O(n × m) | Visited array and queue for BFS |

The total number of cells across all test cases is bounded by 2 × 10^5, so the BFS operations remain comfortably within limits. The constant factor from two greedy passes over 30 bits is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

    def bfs(n, m, grid, allowed_mask, require_mask):
        if (grid[0][0] & allowed_mask) != grid[0][0]:
            return False
        if (grid[0][0] & require_mask) != require_mask:
            return False
        if (grid[n-1][m-1] & allowed_mask) != grid[n-1][m-1]:
            return False
        if (grid[n-1][m-1] & require_mask) != require_mask:
            return False

        vis = [[False]*m for _ in range(n)]
        q = deque([(0,0)])
        vis[0][0] = True

        while q:
            x,y = q.popleft()
            if x == n-1 and y == m-1:
                return True
            for dx,dy in DIRS:
                nx, ny = x+dx, y+dy
                if 0 <= nx < n and 0 <= ny < m and not vis[nx][ny]:
                    v = grid[nx][ny]
                    if (v & allowed_mask) == v and (v & require_mask) == require_mask:
                        vis[nx][ny] = True
                        q.append((nx, ny))
        return vis[n-1][m-1]

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(n)]

        full = (1 << 30) - 1

        B = full
        for b in range(29, -1, -1):
            if B & (1 << b):
                B2 = B ^ (1 << b)
                if bfs(n, m, grid, B2, 0):
                    B = B2

        C = 0
        for b in range(29, -1, -1):
            C2 = C | (1 << b)
            if bfs(n, m, grid, B, C2):
                C = C2

        out.append(f"{B} {C}")

    return "\n".join(out)

# provided sample placeholders
# assert run("...") == "..."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid single value | value value | trivial connectivity and both phases |
| all equal grid | value value | AND remains maximal and OR minimal trivial |
| forced corridor | computed mask | connectivity sensitivity to bit removal |
| split by high-bit obstacle | computed | OR phase correctness |

## Edge Cases

A key edge case is when the only valid path requires a high-bit cell. In that case, attempts to remove that bit during OR minimization will fail BFS, forcing the algorithm to keep it. The BFS directly encodes this failure because the endpoint becomes unreachable once the cell is removed.

Another edge case occurs in AND maximization when the optimal AND is zero. This happens when every valid path must include at least one cell that misses a given bit. The greedy construction naturally converges to zero because every attempt to set a bit fails the connectivity check, leaving C unchanged.
