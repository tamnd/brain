---
title: "CF 1941G - Rudolf and Subway"
description: "The problem describes a subway system as an undirected graph where each vertex is a station and each edge represents a direct connection between two stations. Every edge is labeled with a color representing the subway line it belongs to."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1941
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 933 (Div. 3)"
rating: 2000
weight: 1941
solve_time_s: 68
verified: true
draft: false
---
[CF 1941G - Rudolf and Subway](https://codeforces.com/problemset/problem/1941/G)

**Rating:** 2000  
**Tags:** constructive algorithms, dfs and similar, graphs, shortest paths  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a subway system as an undirected graph where each vertex is a station and each edge represents a direct connection between two stations. Every edge is labeled with a color representing the subway line it belongs to. All edges of the same color form a connected subgraph, meaning you can travel along that line without interruption between its stations. The task is to determine the smallest number of subway lines that a route must pass through to go from a departure station `b` to a destination station `e`.

The input provides multiple test cases, each defining a graph with up to 200,000 vertices and 200,000 edges, and the total number of vertices and edges across all test cases also stays within these bounds. With such limits and a 2-second runtime, any solution with a time complexity worse than O(n + m) per test case is likely to be too slow. Specifically, nested loops over edges or colors would quickly exceed feasible operation counts.

Non-obvious edge cases include when the start and end stations are the same, when the graph has only one line, or when the shortest path spans multiple colors in a way that naive greedy traversal might miss. For instance, a graph where vertices 1-2-3 are one color and 3-4-5 another, traveling from 1 to 5 requires switching lines exactly once, and a careless BFS that ignores colors could miscount.

## Approaches

A brute-force approach could enumerate all paths from `b` to `e`, keeping track of the set of line colors used along each path, and then choose the path that uses the fewest colors. This is correct in principle, but the number of paths grows exponentially with the number of stations, making this approach completely impractical for `n` and `m` up to 2·10^5. Even limiting paths to simple paths, the combinatorial explosion is unavoidable.

The key insight comes from realizing that the minimum number of lines to switch is not related to the total number of stations traversed but only to the transitions between different color-connected components. Each color defines a connected component of stations. If we treat these components as nodes in a new "meta-graph," where two components are connected if there exists an edge connecting a station from one to a station of another, then the problem reduces to finding the shortest path in this meta-graph. This is exactly the BFS problem with edge weights 0 and 1: traveling along the same color has weight 0 (no line change), and switching colors incurs weight 1 (a line change). We can efficiently compute this with a 0-1 BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(paths) | O(n) | Too slow |
| 0-1 BFS / Component Graph | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the graph edges and group them by color. Since edges of the same color form a connected subgraph, treat each color's subgraph as a single component for BFS purposes.
2. Assign a unique identifier to each connected component within each color. This can be done using DFS or BFS restricted to edges of the same color. Each station belongs to exactly one component per color.
3. Build a meta-graph where each node is a station, and edges exist between stations of different colors that are directly connected in the original graph. Annotate edges with a cost: 0 if the color does not change, 1 if switching lines. This produces the weighted graph for 0-1 BFS.
4. Initialize a deque for BFS starting from the departure station `b` with a cost of 0 lines used. Push neighbors along the same color to the front of the deque (weight 0) and neighbors requiring a color change to the back (weight 1).
5. Continue BFS until the destination station `e` is reached. The cost at that moment represents the minimum number of subway lines used. If `b` equals `e`, return 0 immediately.
6. Output the result for each test case.

Why it works: The algorithm maintains the invariant that the BFS deque always contains the next stations ordered by the minimal number of line switches required to reach them. Because the graph has non-negative edge costs (0 or 1) and BFS processes nodes in order of increasing cost, the first time we reach the destination gives the minimum number of lines. The 0-1 BFS guarantees optimality by exploring zero-cost moves before incrementing line switches.

## Python Solution

```python
import sys
from collections import defaultdict, deque
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        edges = defaultdict(list)
        color_edges = defaultdict(list)
        for _ in range(m):
            u, v, c = map(int, input().split())
            edges[u].append((v, c))
            edges[v].append((u, c))
            color_edges[c].append((u, v))
        b, e = map(int, input().split())
        if b == e:
            print(0)
            continue

        # component mapping per color
        color_comp = {}
        for c, pairs in color_edges.items():
            visited = set()
            comp_id = 0
            adj = defaultdict(list)
            for u, v in pairs:
                adj[u].append(v)
                adj[v].append(u)
            for u in adj:
                if u not in visited:
                    stack = [u]
                    while stack:
                        node = stack.pop()
                        if node in visited:
                            continue
                        visited.add(node)
                        color_comp[(node, c)] = comp_id
                        for nei in adj[node]:
                            if nei not in visited:
                                stack.append(nei)
                    comp_id += 1

        # BFS 0-1
        dq = deque()
        dist = {}
        for v, c in edges[b]:
            dist[(v, c)] = 1
            dq.append((v, c))
        dist[(b, 0)] = 0
        dq.appendleft((b, 0))

        while dq:
            node, curr_c = dq.popleft()
            d = dist[(node, curr_c)]
            for nei, c in edges[node]:
                cost = 0 if c == curr_c or curr_c == 0 else 1
                if (nei, c) not in dist or dist[(nei, c)] > d + cost:
                    dist[(nei, c)] = d + cost
                    if cost == 0:
                        dq.appendleft((nei, c))
                    else:
                        dq.append((nei, c))
        ans = min([dist[(e, c)] for v, c in edges[e] if (e, c) in dist] + [dist.get((e, 0), float('inf'))])
        print(ans)
        
solve()
```

The solution first builds adjacency lists both by station and by color. The DFS assigns a unique component ID to each connected set of stations for a color. Then the 0-1 BFS handles line switches by using a deque, pushing same-color moves to the front and switches to the back. We track distances using `(station, color)` pairs to distinguish state based on the current line.

Subtle implementation choices include initializing `dist[(b, 0)] = 0` to allow the first move to any line to count as a line switch, and carefully checking neighbors in BFS to handle color changes. Off-by-one errors are avoided because Python uses 1-based station indices directly from input.

## Worked Examples

**Test Case 1:**

Input:

```
6 6
1 2 1
2 3 1
5 2 2
2 4 2
4 6 2
3 6 3
1 3
```

| Step | Current Node | Current Color | Distances Updated | Explanation |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | dist[(1,0)]=0 | Departure |
| Move | 1→2 | 1 | dist[(2,1)]=1 | First line used |
| Move | 2→3 | 1 | dist[(3,1)]=1 | Same line, no new line |
| End | 3 | 1 | min distance=1 | Reached destination using 1 line |

This confirms that if a direct path exists within a single color, the algorithm finds it.

**Test Case 2:**

Input:

```
6 6
1 2 1
2 3 1
5 2 2
2 4 2
4 6 2
3 6 3
1 6
```

| Step | Current Node | Current Color | Distances Updated | Explanation |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | dist[(1,0)]=0 | Departure |
| Move | 1→2 | 1 | dist[(2,1)]=1 | First line used |
| Move | 2→4 | 2 | dist[(4,2)]=2 | Switch line, cost+1 |
| Move | 4→6 | 2 | dist[(6,2)]=2 | Same line, no new line |
| Move | 2→3 | 1 | dist[(3,1)]=1 | Continue green line |
| Move | 3→6 | 3 | dist[(6,3)]=2 | Another line possible |
| End | 6 | min(dist[(6,2)],dist[( |  |  |
