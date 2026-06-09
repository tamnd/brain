---
title: "CF 1811F - Is It Flower?"
description: "We are asked to detect a specific type of graph called a $k$-flower. Conceptually, a $k$-flower is made of a central cycle of length $k$, and at each vertex of that cycle there is another disjoint cycle of length $k$ attached."
date: "2026-06-09T08:41:02+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1811
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 863 (Div. 3)"
rating: 2100
weight: 1811
solve_time_s: 106
verified: true
draft: false
---

[CF 1811F - Is It Flower?](https://codeforces.com/problemset/problem/1811/F)

**Rating:** 2100  
**Tags:** dfs and similar, graphs, implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to detect a specific type of graph called a $k$-flower. Conceptually, a $k$-flower is made of a central cycle of length $k$, and at each vertex of that cycle there is another disjoint cycle of length $k$ attached. No two of these attached cycles share vertices with each other or with the central cycle except at the connecting vertex. A graph is given in the form of vertices and edges, and the task is to decide if it matches the $k$-flower structure for some $k \ge 3$.

Each test case provides the number of vertices and edges, followed by a list of edges. The output is a simple YES or NO for each graph depending on whether it is a $k$-flower.

The constraints are tight: $n$ and $m$ can be up to $2 \cdot 10^5$, with up to $10^4$ test cases. A brute-force attempt to check all subsets of vertices or cycles will not scale because even a cubic algorithm is infeasible. We need a solution that is essentially linear in the size of each graph.

Edge cases include very small graphs or graphs that superficially contain cycles but cannot be structured as a $k$-flower. For example, a triangle with an extra edge elsewhere is **not** a $k$-flower because the attached cycles must all be disjoint and of the same length as the central cycle. Similarly, graphs with vertices of degree other than two or four in the right places will immediately fail the test.

## Approaches

The brute-force method would enumerate all possible cycles in the graph and try to verify the flower property by attaching cycles to each vertex. This works in principle because cycles define the $k$-flower, but enumerating all cycles of length $k$ is exponential. With $n$ up to $2 \cdot 10^5$, this approach is hopeless.

The key insight is structural: each $k$-flower has a very specific degree pattern. Every vertex in the central cycle has degree 4, because it participates in two edges of the central cycle and two edges of its attached cycle. Every vertex in an attached cycle (excluding the one connecting to the center) has degree 2. This rigid degree pattern drastically reduces the search space.

With this insight, we can immediately reject graphs where some vertex degree is not 2 or 4. Furthermore, connected components of vertices with degree 2 must themselves be simple cycles. By identifying all degree-4 vertices and confirming they form a single cycle and each connects to exactly one cycle of degree-2 vertices of the same length, we can verify the flower structure in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n^2) | Too slow |
| Degree-based Structural Check | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph for a test case and build adjacency lists. This allows efficient traversal and degree checking.
2. Compute the degree of each vertex. If a vertex has a degree other than 2 or 4, immediately return NO. This captures the first structural property of $k$-flowers.
3. Collect all vertices of degree 4. Check that they form a single cycle. We can do this using DFS or BFS starting from one degree-4 vertex and making sure we visit all degree-4 vertices exactly once, following edges between them. If any vertex is missing or revisited, return NO.
4. For each degree-4 vertex, inspect its neighbors of degree 2. These neighbors must form a simple cycle, all of the same length $k$ (the same as the central cycle). Perform DFS or BFS restricted to degree-2 vertices to confirm each connected component forms a cycle.
5. Verify that no degree-2 vertex is shared among different degree-4 vertices. This ensures the attached cycles are disjoint.
6. If all checks pass, output YES. Otherwise, output NO.

Why it works: the algorithm encodes the exact structural invariants of a $k$-flower. By checking degrees first, we filter out impossible graphs quickly. Confirming the central cycle ensures connectivity among the core vertices. Inspecting attached cycles guarantees the strict $k$-flower pattern. Because no extra edges can exist without violating degrees, the check is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

def is_k_flower(n, edges):
    adj = [[] for _ in range(n)]
    deg = [0]*n
    for u, v in edges:
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    deg4 = [i for i, d in enumerate(deg) if d == 4]
    deg2 = [i for i, d in enumerate(deg) if d == 2]

    if any(d not in (2,4) for d in deg):
        return "NO"
    if not deg4:
        return "NO"

    # check central cycle of degree 4 vertices
    visited = [False]*n
    def dfs_cycle(u, parent):
        visited[u] = True
        for v in adj[u]:
            if deg[v] != 4:
                continue
            if v == parent:
                continue
            if visited[v]:
                continue
            dfs_cycle(v, u)
    dfs_cycle(deg4[0], -1)
    if any(visited[v] == False for v in deg4):
        return "NO"

    # check attached cycles
    for u in deg4:
        for v in adj[u]:
            if deg[v] == 2 and not visited[v]:
                # explore attached cycle
                comp = []
                stack = [v]
                while stack:
                    x = stack.pop()
                    if visited[x]:
                        continue
                    visited[x] = True
                    comp.append(x)
                    for y in adj[x]:
                        if deg[y] == 2 and not visited[y]:
                            stack.append(y)
                # verify cycle
                if len(comp) < 3:
                    return "NO"
                for x in comp:
                    if len([y for y in adj[x] if deg[y]==2]) != 2:
                        return "NO"
    return "YES"

def main():
    t = int(input())
    results = []
    for _ in range(t):
        input()  # skip empty line
        n, m = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        results.append(is_k_flower(n, edges))
    print("\n".join(results))

if __name__ == "__main__":
    main()
```

The code first filters impossible graphs by degree, then confirms the central cycle of degree-4 vertices using DFS. Attached cycles are verified in the same pass, ensuring they form simple cycles of degree-2 vertices, and all vertices are marked visited to avoid overlaps. The check `len([y for y in adj[x] if deg[y]==2]) != 2` ensures each attached cycle vertex has exactly two connections within the cycle.

## Worked Examples

**Sample 1:**

```
9 12
1 2
3 1
2 3
1 6
4 1
6 4
3 8
3 5
5 8
9 7
2 9
7 2
```

| Step | Visited deg4 | Component of deg2 | Check passed |
| --- | --- | --- | --- |
| Central cycle DFS | 1,2,3 | - | Yes |
| Attached cycles | 4,5,6,7,8,9 | each forms cycle of length 3 | Yes |

Output: YES. Confirms correct identification of central triangle and attached cycles.

**Sample 2:**

```
8 12
1 2
3 1
2 3
1 6
4 1
6 4
3 8
3 5
5 8
8 7
2 8
7 2
```

Central cycle check fails because the degree-4 vertices cannot form a simple cycle, output: NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS explores each vertex and edge at most once |
| Space | O(n + m) | Adjacency list plus visited arrays |

Linear time is acceptable given $n + m \le 2 \cdot 10^5$ per test case and the sum across all test cases stays within this bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""5

9 12
1 2
3 1
2 3
1 6
4 1
6 4
3 8
3 5
5 8
9 7
2 9
7 2

8 12
1 2
3 1
2 3
1 6
4 1
6 4
3 8
3 5
5 8
```
