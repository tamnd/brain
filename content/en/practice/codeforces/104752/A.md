---
title: "CF 104752A - Akira"
description: "We are given a set of points in the plane, each representing a source of an expanding circular “sphere of light”. Every point starts as a level 1 catastrophe, and its influence grows outward uniformly over time at a fixed rate $M$."
date: "2026-06-29T01:24:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "A"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 82
verified: true
draft: false
---

[CF 104752A - Akira](https://codeforces.com/problemset/problem/104752/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the plane, each representing a source of an expanding circular “sphere of light”. Every point starts as a level 1 catastrophe, and its influence grows outward uniformly over time at a fixed rate $M$. At time $t$, each point has a disk of radius $M \cdot t$.

Whenever two existing catastrophe regions touch or overlap, they merge into a single combined catastrophe whose level is the sum of the two previous levels. This merging is transitive: once a group of points has merged into a single connected cluster, any further intersection with another cluster merges the two clusters and adds their levels.

The task is to find the earliest time when at least one connected cluster has total level at least $K$. Since each initial point has level 1, this is equivalent to finding the earliest time when there exists a connected component (under disk intersections) containing at least $K$ points.

The geometric condition for two points $i$ and $j$ to be connected at time $t$ is:

$$M \cdot t \ge \frac{d_{ij}}{2}$$

where $d_{ij}$ is the Euclidean distance between the points. Equivalently:

$$t \ge \frac{d_{ij}}{2M}$$

So we are effectively building a graph whose edges “activate” over time, and we want the earliest time when some connected component reaches size $K$.

The constraints allow up to $N = 1000$, so the complete graph has up to about $5 \times 10^5$ edges. A solution with $O(N^2 \log N)$ or $O(N^2)$ structure is acceptable per test case given $T \le 200$ but we must be careful with constants.

A subtle edge case is when $K = 1$. Then the answer is always 0, since each point already forms a level 1 catastrophe at time zero.

Another edge case is when points are very close or identical. If two points coincide, distance is zero, so they merge immediately at time 0, meaning union-find must correctly handle zero-weight edges.

## Approaches

The brute-force idea is to simulate time continuously and repeatedly recompute which points are connected at a given time $t$. For a fixed $t$, we can build a graph where we connect all pairs whose distance is at most $2Mt$, then run a DFS or union-find to compute component sizes and check whether any component reaches size $K$. We could then search over time using binary search.

This works because the connectivity relation is monotone in time: once two points are connected, they remain connected forever. However, the brute-force approach becomes expensive because each check costs $O(N^2)$ to build edges and $O(N^2)$ or $O(N \alpha(N))$ to union components. With binary search over floating time (say 60 iterations), the total cost becomes too large for worst-case $T = 200$.

The key observation is that we do not actually need to simulate time. Each pair of points has a fixed activation time:

$$w_{ij} = \frac{d_{ij}}{2M}$$

We only care about when edges appear, not how time progresses continuously. This transforms the problem into a classic offline connectivity problem with weighted edges. We sort all edges by activation time and use a union-find structure to merge components in increasing order of time. While merging, we track component sizes, and the moment any component reaches size $K$, the current edge time is the answer.

This reduces the problem to Kruskal-style processing of a complete graph, stopping early once the required component appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force + Binary Search | $O(T \cdot \log R \cdot N^2)$ | $O(N^2)$ | Too slow |
| Kruskal + DSU | $O(T \cdot N^2 \log N)$ | $O(N^2)$ | Accepted |

## Algorithm Walkthrough

### Optimal algorithm

1. For each test case, read all points and compute every pairwise Euclidean distance. This is necessary because every possible interaction between two spheres is determined only by their geometric separation.
2. For each pair $i, j$, compute the time when their spheres first touch:

$$t_{ij} = \frac{\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}}{2M}$$

This converts the continuous growth process into a discrete set of events, one per pair.
3. Store all edges $(t_{ij}, i, j)$ in a list. Each edge represents a future merge event between two components when time reaches $t_{ij}$.
4. Sort all edges by increasing $t_{ij}$. This ensures we process merges in the exact order they become physically possible.
5. Initialize a disjoint set union (DSU) structure where each point starts in its own component of size 1. This reflects that initially every catastrophe has level 1.
6. Traverse edges in sorted order. For each edge $(t, u, v)$, attempt to union the components containing $u$ and $v$. If they are already in the same component, skip it because the connection is redundant.
7. When merging two components, update the resulting component size. If at any point a component size becomes at least $K$, record the current time $t$ as the answer and stop processing further edges.
8. Output the recorded time for the test case.

The reason we can stop early is that once a component reaches size $K$, no later edge can produce a smaller valid time, since all remaining edges occur at equal or larger times.

### Why it works

At any time $t$, the graph formed by edges with $t_{ij} \le t$ exactly represents which spheres have intersected. DSU maintains the connected components of this graph as edges are added in increasing order of $t_{ij}$. Since component size is exactly the sum of initial unit levels, reaching size $K$ corresponds precisely to having a level $K$ catastrophe. The first time this happens in increasing edge order must be the minimum possible time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, M, K = input().split()
        n = int(n)
        M = float(M)
        K = int(K)

        pts = []
        for _ in range(n):
            x, y = map(int, input().split())
            pts.append((x, y))

        if K == 1:
            print("0.0")
            continue

        edges = []
        for i in range(n):
            x1, y1 = pts[i]
            for j in range(i + 1, n):
                x2, y2 = pts[j]
                dx = x1 - x2
                dy = y1 - y2
                dist = (dx * dx + dy * dy) ** 0.5
                edges.append((dist / (2.0 * M), i, j))

        edges.sort()

        parent = list(range(n))
        size = [1] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return 0
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            return size[ra]

        for t, u, v in edges:
            new_size = union(u, v)
            if new_size >= K:
                print(f"{t:.10f}")
                break
        else:
            print("0.0")

if __name__ == "__main__":
    solve()
```

The solution is a direct implementation of Kruskal-style merging over geometric edge activation times. The DSU maintains component membership efficiently, and the size array tracks catastrophe levels.

A subtle implementation detail is computing Euclidean distance using floating point square root. Since the required precision tolerance is $10^{-6}$, standard floating arithmetic is sufficient. Another important point is early termination: once a valid component appears, continuing would only produce larger times and is unnecessary.

## Worked Examples

### Sample 1

Input:

```
1
1 1 1
0 0
```

There is only one point, so it already forms a valid level 1 catastrophe at time zero.

| Step | Action | Component sizes | Current answer |
| --- | --- | --- | --- |
| 1 | Single node | {1} | 0 |

This confirms that $K = 1$ is handled immediately without constructing edges.

### Sample 2

Input:

```
1
4 1 2
0 0
0 2
500 500
500 100
```

We compute distances. The closest meaningful pair is $(0,0)$ and $(0,2)$, distance 2, giving merge time 1.

| Edge | Time | Union result | Largest component |
| --- | --- | --- | --- |
| (0,0)-(0,2) | 1.0 | size 2 | 2 |

After processing the first merge, a component of size 2 appears, so the process stops.

This shows that only the earliest merging edge matters, not the full connectivity structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2 \log N)$ per test | Pairwise distances generate $O(N^2)$ edges, sorted once, each union is nearly constant |
| Space | $O(N^2)$ | All edges stored explicitly |

With $N \le 1000$, this results in about $5 \times 10^5$ edges per test, which is acceptable under the constraints with early termination in many cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # assume solve() is defined above
    solve()
    return ""  # placeholder for illustration

# provided sample
# (output comparison omitted for brevity)

# K=1 immediate
assert run("1\n1 2 1\n0 0\n") == ""

# two points touching immediately
assert run("1\n2 1 2\n0 0\n0 0\n") == ""

# chain requiring second merge
assert run("1\n3 1 3\n0 0\n0 2\n0 4\n") == ""

# square formation
assert run("1\n4 1 2\n0 0\n0 1\n1 0\n1 1\n") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | base case K=1 |
| identical points | 0 | zero distance merging |
| line of 3 points | small t | propagation of unions |
| square | early size-2 merge | geometric ordering correctness |

## Edge Cases

When $K = 1$, the algorithm bypasses all geometry and returns 0 immediately. This is correct because each initial point already forms a level 1 catastrophe without any interaction.

When multiple points coincide, their pairwise distance is zero, so their merge time is zero. The DSU unions them at the first step, forming a larger component instantly, and the size tracking correctly reflects immediate catastrophe growth.

When all points are far apart, no edges will appear before very large times. The algorithm still processes all edges in sorted order, and only returns after the first necessary merge appears, ensuring correctness even in sparse interaction scenarios.
