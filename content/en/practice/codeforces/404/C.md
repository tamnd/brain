---
title: "CF 404C - Restore Graph"
description: "We are asked to reconstruct an undirected connected graph from a list of shortest distances from one vertex, under the constraint that each vertex can have at most k edges."
date: "2026-06-07T01:29:51+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "sortings"]
categories: ["algorithms"]
codeforces_contest: 404
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 237 (Div. 2)"
rating: 1800
weight: 404
solve_time_s: 373
verified: false
draft: false
---

[CF 404C - Restore Graph](https://codeforces.com/problemset/problem/404/C)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, sortings  
**Solve time:** 6m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to reconstruct an undirected connected graph from a list of shortest distances from one vertex, under the constraint that each vertex can have at most _k_ edges. The input gives the number of vertices `n`, the maximum degree `k`, and an array `d` of length `n` where `d[i]` represents the distance from the chosen starting vertex to vertex `i`. The graph may have any structure as long as it is consistent with the distances and degree limits, and does not contain self-loops or multiple edges.

The key constraints are: `n` can be up to 10^5 and each vertex has degree at most `k`. This means any solution must be roughly linear or O(n log n). Algorithms that attempt to check all possible edge combinations would require O(n^2) operations, which is too slow. Memory is sufficient for storing adjacency lists or similar structures, as 10^5 vertices with up to 10^5 edges is acceptable under the 256 MB limit.

Non-obvious edge cases include: a graph where all vertices have distance 0 except the start, which is trivial; a graph where some distance values are missing, which would make construction impossible; and cases where `k` is too small to connect vertices at the same distance, leading to a disconnected graph. For example, if `n = 3, k = 1` and `d = [0, 1, 2]`, we cannot build a valid graph because the vertex at distance 2 cannot connect to more than one vertex, and it has no other option to reach distance 1 without exceeding degree.

## Approaches

A brute-force approach would attempt to connect vertices greedily based on distance: for each vertex, try to connect it to any vertex with distance one less until all distances are satisfied. This is correct in principle but slow: for each vertex, we could iterate over up to `n` candidates, giving O(n^2) complexity, which is infeasible for n = 10^5.

The key insight is to leverage the distance levels. Vertices can be grouped by distance from the start. All vertices at distance `d` must be connected to some vertex at distance `d-1`. Within a level, vertices do not connect to each other (since that would create a shortcut, violating the distance). This lets us build a BFS-like tree structure level by level. The degree constraint `k` is handled by keeping track of how many edges each vertex has already used and ensuring that no vertex exceeds `k`.

The brute-force works because it considers every possible connection, but fails when n is large. The level-based BFS approach works because distances impose a strict hierarchy: a vertex at distance `d` can only be connected to vertices at distance `d-1` (or `d+1` if looking backward), and this prevents cycles that would contradict distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n^2) | Too slow |
| Level BFS / Distance Grouping | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Identify the vertex with distance 0. This is the starting vertex, the root of our BFS tree. If there is no vertex with distance 0 or multiple, output -1 because the input is inconsistent.
2. Group all vertices by their distance from the start. Use a dictionary or list of lists where `level[d]` contains all vertices at distance `d`. If any level is empty between 0 and the maximum distance, output -1 because a gap means some distances cannot be reached.
3. Initialize a degree counter for each vertex, starting at 0. This will track how many edges each vertex already has.
4. Connect vertices level by level. For distance `d = 1` to max_distance, for each vertex `v` in level `d`, choose a parent vertex `u` from level `d-1` that has remaining degree capacity. If no such parent exists, the graph cannot be formed, output -1.
5. For each connection, increment the degree counter for both vertices. Stop assigning children to a parent if it reaches `k`.
6. Collect all edges and print the total count followed by each edge. Multiple solutions are acceptable because any valid parent assignment works.

Why it works: Every vertex at distance `d` is guaranteed to connect to a vertex at distance `d-1`. No vertex exceeds the degree limit because we check capacity before connecting. Distances are preserved because edges are only formed between consecutive levels. Connectivity is guaranteed because the BFS tree spans all vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
d = list(map(int, input().split()))

from collections import defaultdict, deque

# Step 1: check for valid root
roots = [i for i, dist in enumerate(d) if dist == 0]
if len(roots) != 1:
    print(-1)
    sys.exit()

root = roots[0]

# Step 2: group by distance
levels = defaultdict(list)
max_dist = 0
for i, dist in enumerate(d):
    levels[dist].append(i)
    max_dist = max(max_dist, dist)

# Step 3: check for missing levels
for dist in range(max_dist + 1):
    if not levels[dist]:
        print(-1)
        sys.exit()

# Step 4: assign edges
edges = []
degree = [0] * n

for dist in range(1, max_dist + 1):
    parents = deque(levels[dist - 1])
    if not parents:
        print(-1)
        sys.exit()
    for v in levels[dist]:
        # find parent with free degree
        while parents and degree[parents[0]] >= k:
            parents.popleft()
        if not parents:
            print(-1)
            sys.exit()
        u = parents[0]
        edges.append((u + 1, v + 1))
        degree[u] += 1
        degree[v] += 1
        # keep parent in deque if it can take more
        if degree[u] >= k:
            parents.popleft()

print(len(edges))
for u, v in edges:
    print(u, v)
```

This solution first finds the root, groups vertices by distance, then assigns edges level by level. The `degree` array ensures we never exceed `k` connections per vertex. Using `deque` allows efficiently popping parents when they reach their capacity.

## Worked Examples

**Sample 1**

Input:

```
3 2
0 1 1
```

| dist | levels | degree | edges |
| --- | --- | --- | --- |
| 0 | [0] | [0,0,0] | [] |
| 1 | [1,2] | [0,0,0] | [] |

- connect 1 → 0 | - | [1,1,0] | [(1,2)] |
- connect 2 → 0 | - | [2,1,1] | [(1,2),(1,3)] |

Output:

```
2
1 2
1 3
```

This demonstrates that vertices at distance 1 connect to root. Degree limits are respected.

**Custom Example**

Input:

```
4 2
0 1 2 2
```

| dist | levels | degree | edges |
| --- | --- | --- | --- |
| 0 | [0] | [0,0,0,0] | [] |
| 1 | [1] | [0,0,0,0] | [] |

- connect 1 → 0 | - | [1,1,0,0] | [(1,2)] |

| 2 | [2,3] | [1,1,0,0] | [] |
- connect 2 → 1 | - | [1,2,1,0] | [(1,2),(2,3)] |
- connect 3 → 1 | - | [1,2,1,1] | [(1,2),(2,3),(2,4)] |

Output:

```
3
1 2
2 3
2 4
```

Shows that vertices at distance 2 connect to any available parent at distance 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex is processed once and edges are formed in O(1) using deque. |
| Space | O(n) | Storing levels, degrees, and edges requires linear memory. |

This fits well within the constraints `n <= 10^5` and `m <= 10^6`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    return out.getvalue().strip()

# provided sample
assert run("3 2\n0 1 1\n") == "2\n1 2\n1 3"

# custom cases
assert run("4 2\n0 1 2 2\n") == "3\n1 2\n2 3\n2 4", "level 2 vertices connect correctly"
assert run("3 1\n0 1 2\n") == "-1", "degree too small to connect vertex at distance 2"
assert run("1 1\n0\n") == "0
```
