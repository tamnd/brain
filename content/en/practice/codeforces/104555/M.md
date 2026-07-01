---
title: "CF 104555M - Maximizing Flight Efficiency"
description: "We are given a complete weighted graph where each vertex represents a city and every pair of cities has a direct flight with a known cost. The cost matrix is symmetric, so traveling between two cities costs the same in both directions."
date: "2026-06-30T08:52:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104555
codeforces_index: "M"
codeforces_contest_name: "2023-2024 ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 104555
solve_time_s: 62
verified: true
draft: false
---

[CF 104555M - Maximizing Flight Efficiency](https://codeforces.com/problemset/problem/104555/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete weighted graph where each vertex represents a city and every pair of cities has a direct flight with a known cost. The cost matrix is symmetric, so traveling between two cities costs the same in both directions. The goal is to decide whether these direct flight prices are internally consistent with shortest-path reasoning, and if they are, to determine how many of the direct flights are unnecessary because an indirect route is never more expensive than them.

A table is considered consistent when, for every pair of cities, the direct flight cost is already the cheapest possible way to travel between them. In graph terms, this means the given adjacency matrix must already satisfy the all-pairs shortest path property.

If the table is not consistent, the presence of a cheaper indirect route invalidates the pricing model and we must output -1.

If it is consistent, we are allowed to remove as many direct edges as possible, but only those edges that are redundant in the sense that there exists an alternative route whose cost is exactly equal to the direct edge. The removal must not increase any shortest path cost between any pair of cities.

The constraints allow up to 100 cities, so we are dealing with up to 10,000 entries in the matrix. A cubic algorithm in N is acceptable. Anything worse than O(N^3) would be unnecessary, while O(N^4) is already close to the upper limit of comfort.

A subtle edge case arises when a direct edge is strictly worse than a two-hop path. For example, if we have:

```
0 5 10
5 0 4
10 4 0
```

Here the path 1 → 2 → 3 costs 9, which is cheaper than the direct 1 → 3 cost of 10. This means the table is incoherent and must return -1. A naive approach that only checks triangle inequality in one direction but misses intermediate comparisons can fail if not applied systematically over all triples.

Another edge case occurs when multiple equal-cost paths exist. For example:

```
0 2 2
2 0 2
2 2 0
```

All direct edges are already optimal, but none can be removed because removing any would increase shortest path cost. A naive “remove if there exists a path” approach would incorrectly remove edges even when the alternative path is not strictly shorter but equal, but still must preserve shortest path equality.

## Approaches

A brute-force approach would compute shortest paths between every pair of cities by repeatedly relaxing edges or running Dijkstra from each node, and then compare the computed shortest path distances with the given matrix. If any pair has a mismatch where the given edge is not equal to the computed shortest path, the table is incoherent.

This approach is correct because it directly checks whether the matrix already encodes the all-pairs shortest path solution. However, running Dijkstra from each node costs O(N^3 log N) or O(N^3) with optimizations, and Floyd-Warshall also costs O(N^3), so brute force is already borderline but still acceptable. The real inefficiency comes when we try to additionally test edge removals individually, which would multiply complexity by another factor of N^2.

The key observation is that we do not need to simulate removals. Once we compute all-pairs shortest paths using Floyd-Warshall, we can simultaneously validate coherence and count redundancy. An edge between i and j is removable if there exists some intermediate node k such that going i → k → j achieves exactly the same cost as the direct edge. If any intermediate path is strictly smaller than the direct edge, the table is invalid.

This reduces the problem to a single Floyd-Warshall run followed by a triple scan over all pairs and intermediates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (per-pair shortest paths + checks) | O(N^3) to O(N^4) | O(N^2) | Too slow |
| Floyd-Warshall optimized check | O(N^3) | O(N^2) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the matrix and store it as dist. This represents both the input direct edges and our working shortest path table. We keep it unchanged initially because we will progressively refine it using intermediate vertices.
2. Run Floyd-Warshall over all triples (k, i, j), updating dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]). This step computes the true shortest path between every pair using any intermediate cities. The reason this works is that any shortest path can be decomposed into subpaths whose intermediate vertices will eventually be considered as k increases.
3. After computing shortest paths, verify coherence by checking whether for every pair (i, j), the original direct cost equals the computed shortest path cost. If any direct edge is larger than the shortest path, the table is inconsistent and we immediately output -1. This ensures no indirect route is cheaper than a direct flight.
4. If coherence holds, we count removable edges. For each pair (i, j), we check whether there exists some intermediate node k different from i and j such that dist[i][j] equals dist[i][k] + dist[k][j]. If such a k exists, then the direct edge is redundant because an alternative path achieves the same optimal cost.
5. To avoid double counting, we only consider pairs i < j since the graph is undirected. Each removable edge contributes exactly one to the answer.
6. Output the total count of removable edges.

### Why it works

The Floyd-Warshall step ensures dist contains the true shortest path distances under all possible routes. If any direct edge is larger than this value, it cannot be part of any optimal structure and the input is inconsistent. If equality holds, then the direct edge is already optimal, but it may or may not be unique. Checking for an intermediate k that preserves equality identifies exactly when the edge is not uniquely required. Because any shortest path with equal cost suffices to preserve all-pairs distances, removing such an edge does not change any shortest path value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    dist = [list(map(int, input().split())) for _ in range(n)]

    # Floyd–Warshall
    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == 10**18:
                continue
            for j in range(n):
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd

    # Check coherence
    for i in range(n):
        for j in range(n):
            if dist[i][j] != dist[i][j]:
                pass
    # Actually we need original matrix, so recompute carefully
    # Store original
    # (Fix approach: re-read logic cleanly)

def solve():
    n = int(input())
    orig = [list(map(int, input().split())) for _ in range(n)]
    dist = [row[:] for row in orig]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # coherence check
    for i in range(n):
        for j in range(n):
            if dist[i][j] != orig[i][j]:
                print(-1)
                return

    removable = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(n):
                if k != i and k != j:
                    if dist[i][j] == dist[i][k] + dist[k][j]:
                        removable += 1
                        break

    print(removable)

if __name__ == "__main__":
    solve()
```

The solution begins by copying the input matrix so we preserve the original direct flight costs while computing shortest paths separately. Floyd-Warshall then transforms `dist` into the true all-pairs shortest path matrix.

The coherence check compares each pair against the original matrix. Any mismatch means the input contained a strictly suboptimal direct flight, so the structure is invalid.

The final loop counts edges that have an alternative equal-cost decomposition through some intermediate node. The `break` ensures each edge is counted only once, since we only need existence of one such witness node.

## Worked Examples

### Example 1

Input:

```
3
0 1 2
1 0 1
2 1 0
```

After Floyd-Warshall, shortest paths remain identical:

| i | j | original | shortest |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 0 | 2 | 2 | 2 |
| 1 | 2 | 1 | 1 |

No pair has a strictly better indirect route. However, edge (0,2) is redundant because 0 → 1 → 2 has cost 1 + 1 = 2, matching the direct edge.

So we can remove exactly one edge.

Output:

```
1
```

### Example 2

Input:

```
3
0 2 2
2 0 2
2 2 0
```

Floyd-Warshall does not improve any value. Every pair already has its direct edge as the unique shortest path cost.

Checking removability:

For (0,1), any path through 2 gives 2 + 2 = 4, which is worse than 2. Same for all pairs.

No edges are removable.

Output:

```
0
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^3) | Floyd-Warshall dominates with three nested loops over cities |
| Space | O(N^2) | Two matrices store original and shortest path distances |

With N ≤ 100, 10^6 iterations per loop level is acceptable. The constant factors are small and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp)).strip()

# Re-define safe runner since solve prints
def solve_output(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)

    out = StringIO()
    backup_out = sys.stdout
    sys.stdout = out

    solve()

    sys.stdin = backup
    sys.stdout = backup_out
    return out.getvalue()

# provided samples
assert solve_output("""3
0 1 2
1 0 1
2 1 0
""") == "1\n"

assert solve_output("""3
0 2 2
2 0 2
2 2 0
""") == "0\n"

# custom cases
assert solve_output("""2
0 5
5 0
""") == "0\n", "minimum non-trivial graph"

assert solve_output("""3
0 1 10
1 0 1
10 1 0
""") == "-1\n", "incoherent triangle violation"

assert solve_output("""4
0 1 2 3
1 0 1 2
2 1 0 1
3 2 1 0
""") == "3\n", "chain redundancy"

assert solve_output("""1
0
""") == "0\n", "single node"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node symmetric | 0 | minimal structure, no removals |
| triangle violation | -1 | incoherent detection |
| chain graph | 3 | maximal redundancy cases |
| single node | 0 | boundary condition |

## Edge Cases

For a single city, there are no edges to validate or remove, and the algorithm immediately produces zero after skipping both Floyd-Warshall improvement and pair checks.

For a triangle where one edge is strictly worse than a two-step path, the Floyd-Warshall step strictly reduces that entry, causing an immediate mismatch with the original matrix and returning -1. This prevents any attempt at counting removable edges on invalid data.

For fully equal-cost complete graphs, every edge is directly equal to all alternative two-hop paths, so every edge is marked removable once. The algorithm correctly counts each undirected pair exactly once because the inner loop only increments when at least one intermediate equality exists.
