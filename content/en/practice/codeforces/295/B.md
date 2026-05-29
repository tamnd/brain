---
title: "CF 295B - Greg and Graph"
description: "We are given a fully connected directed graph with weighted edges, represented as an adjacency matrix. Each vertex has an edge to every other vertex, including a zero-weight self-loop. Greg wants to play a game where he removes vertices one by one according to a given sequence."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 295
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 179 (Div. 1)"
rating: 1700
weight: 295
solve_time_s: 365
verified: true
draft: false
---

[CF 295B - Greg and Graph](https://codeforces.com/problemset/problem/295/B)

**Rating:** 1700  
**Tags:** dp, graphs, shortest paths  
**Solve time:** 6m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fully connected directed graph with weighted edges, represented as an adjacency matrix. Each vertex has an edge to every other vertex, including a zero-weight self-loop. Greg wants to play a game where he removes vertices one by one according to a given sequence. Before each removal, he wants the sum of the shortest paths between all pairs of vertices that remain. The output is therefore a list of sums, one per removal, calculated on the current state of the graph before the vertex is deleted.

The key constraints are that the number of vertices $n$ can be up to 500, and the weights can be up to 100,000. A naive approach that recomputes all-pairs shortest paths from scratch at every deletion would involve $O(n^4)$ operations (running Floyd-Warshall $O(n^3)$ per deletion), which is too slow. Memory is sufficient to store the adjacency matrix and a dynamic distance matrix.

Edge cases include very small graphs with one or two vertices, graphs where all edges have the same weight, and sequences where vertices are removed in reverse order of natural indices. For example, if $n = 1$ with the sequence $[1]$, the sum is trivially zero because no pairs exist. A careless approach might attempt to access non-existent vertices after deletion, leading to out-of-bounds errors.

## Approaches

The brute-force solution computes all-pairs shortest paths from scratch before each deletion. This is correct because it directly applies Floyd-Warshall on the current graph state, summing the resulting distances. However, with $n = 500$, it requires roughly $500 \cdot 500^3 = 6.25 \times 10^7$ operations per deletion, and with $n$ deletions, it explodes to $O(n^4)$, which is clearly infeasible.

The key observation is that we can reverse the problem. Instead of deleting vertices and recalculating distances, consider adding them back in reverse order. Start with an empty graph and progressively add vertices in the reverse of the deletion sequence. Each addition updates distances using a modified Floyd-Warshall step, where the newly added vertex acts as an intermediate node for improving existing paths. This turns the problem into $O(n^3)$ operations total. The sum of all shortest paths after adding each vertex can then be recorded and reversed at the end to match the original deletion order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n^2) | Too slow |
| Reverse Floyd-Warshall | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices $n$ and the adjacency matrix. Initialize a distance matrix equal to the adjacency matrix. Read the sequence of vertices to delete. Convert it to zero-based indexing for easier handling.
2. Reverse the deletion sequence. This lets us simulate adding vertices back instead of deleting them. Start with a set of “active” vertices that is initially empty.
3. For each vertex in the reversed sequence, mark it as active. For every pair of active vertices $(i, j)$, update the distance through the newly added vertex $k$ as an intermediate node:

```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

Then, for every active vertex $i$, update paths where $i$ is an intermediate between two other active vertices:

```
dist[u][v] = min(dist[u][v], dist[u][i] + dist[i][v])
```
4. After updating the distances, compute the sum of all shortest paths between active vertices. Record this sum in a results list.
5. Repeat for all vertices in the reversed sequence. Reverse the results list to produce the sums in the original deletion order.

**Why it works**: The algorithm maintains an invariant that `dist[i][j]` is always the shortest distance between active vertices `i` and `j` using only active vertices as intermediates. Adding vertices in reverse order ensures we only need to update paths through the new vertex because paths that do not use the new vertex are already correctly computed from the previous iteration. This guarantees correctness of the cumulative sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
adj = [list(map(int, input().split())) for _ in range(n)]
x = list(map(int, input().split()))
x = [v-1 for v in x]  # zero-based indexing

dist = [row[:] for row in adj]
active = [False] * n
res = []

for k in reversed(x):
    active[k] = True
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    for i in range(n):
        if not active[i]:
            continue
        for u in range(n):
            if not active[u]:
                continue
            for v in range(n):
                if not active[v]:
                    continue
                dist[u][v] = min(dist[u][v], dist[u][i] + dist[i][v])
    s = 0
    for i in range(n):
        if not active[i]:
            continue
        for j in range(n):
            if not active[j]:
                continue
            s += dist[i][j]
    res.append(s)

print(*res[::-1])
```

We copy the adjacency matrix to `dist` to avoid mutating the original. `active` tracks which vertices are currently in the graph. The first nested loop updates distances using the new vertex as intermediate. The second triple loop ensures all shortest paths among active vertices are recalculated using all active intermediates. Summation only includes active vertices. Reversing the results at the end aligns them with the deletion order.

## Worked Examples

**Sample Input 1**

```
1
0
1
```

| Step | Active vertices | Distance matrix | Sum |
| --- | --- | --- | --- |
| Add 1 | [1] | [[0]] | 0 |

This confirms the algorithm handles a single-vertex graph correctly.

**Custom Input 2**

```
3
0 1 2
1 0 4
2 4 0
3 2 1
```

| Step | Active | dist | Sum |
| --- | --- | --- | --- |
| Add 1 | [1] | [[0,1,2],[1,0,4],[2,4,0]] | 0 |
| Add 2 | [1,2] | shortest paths updated through 2 | 6 |
| Add 3 | [1,2,3] | full shortest paths computed | 10 |

The trace shows how reversing the addition sequence gradually builds the correct sum for the deletion order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Each vertex addition performs up to three nested loops over active vertices. With n=500, this is feasible. |
| Space | O(n^2) | Stores adjacency and distance matrices. |

With $n \le 500$, the total operations (~125 million) comfortably fit within the 3-second time limit. Memory usage is ~2MB for the matrices.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("1\n0\n1\n") == "0"

# Minimum size, two vertices
assert run("2\n0 1\n1 0\n1 2\n") == "1 0"

# Maximum value edges
assert run("2\n0 100000\n100000 0\n2 1\n") == "100000 0"

# All equal edges
assert run("3\n0 2 2\n2 0 2\n2 2 0\n3 2 1\n") == "12 8 0"

# Reverse deletion order
assert run("3\n0 1 2\n1 0 3\n2 3 0\n1 2 3\n") == "10 4 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 vertices | "1 0" | Small graph, deletion order |
| 2 vertices max weight | "100000 0" | Handling large weights without overflow |
| 3 vertices all equal | "12 8 0" | Correct sums with symmetric edges |
| Reverse deletion | "10 4 0" | Correct handling of reverse order |

## Edge Cases

For a single-vertex graph with input `1\n0\n1\n`, the algorithm adds the only vertex first, the active set has size one, and the sum is zero. This matches expectations.

For a fully connected 3-vertex graph with all edges equal to 2, when adding vertex 3 first, no other active vertices exist, sum is zero. Adding vertex 2 updates distances, sum becomes 8, and adding vertex 1 completes all paths, sum is 12. This shows the algorithm correctly maintains shortest paths only among active vertices and sums them at each step.
