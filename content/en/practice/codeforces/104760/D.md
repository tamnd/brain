---
title: "CF 104760D - \u0412\u0435\u0441\u0435\u043b\u044b\u0435 \u0444\u043e\u043d\u0430\u0440\u0438"
description: "The city can be modeled as a graph where each lamp is a vertex and each street connects two lamps. The task is to assign one of two colors to every lamp so that every street connects lamps of different colors."
date: "2026-06-28T22:36:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 85
verified: false
draft: false
---

[CF 104760D - \u0412\u0435\u0441\u0435\u043b\u044b\u0435 \u0444\u043e\u043d\u0430\u0440\u0438](https://codeforces.com/problemset/problem/104760/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

The city can be modeled as a graph where each lamp is a vertex and each street connects two lamps. The task is to assign one of two colors to every lamp so that every street connects lamps of different colors. In graph terms, this is asking whether the graph can be 2-colored so that no edge is monochromatic.

There is an additional structural detail that matters: a street may connect a lamp to itself, and there may be multiple streets between the same pair of lamps. Multiple streets do not change any constraint because they all enforce the same condition between the same two endpoints. A self-loop, however, creates a direct contradiction because it demands a vertex to have a color different from itself.

The constraints allow up to 400 vertices per test case and up to 50 test cases. Even in the densest case this is a small graph, so an O(NM) or O(N + M) per test solution is easily fast enough. Anything involving exponential search over colorings would fail immediately since 2^400 is astronomically large.

A naive implementation pitfall appears when self-loops or disconnected components are mishandled. For example, if a vertex has an edge to itself like input `1 1`, the correct answer is always NO, even though a naive BFS might never explicitly detect a contradiction unless it checks edges carefully.

Another subtle case is multiple components. A graph can be bipartite component-wise even if not connected, so a solution that only starts BFS from node 1 can incorrectly miss other components that violate bipartiteness.

## Approaches

A brute-force strategy would try all assignments of two colors to N vertices and verify whether every edge connects differently colored endpoints. This directly encodes the condition but requires checking 2^N assignments, and for each assignment scanning all edges, leading to O(2^N · M). With N up to 400, this is infeasible.

The key observation is that the constraint is exactly the definition of a bipartite graph. Instead of exploring all assignments globally, we propagate constraints locally: once a node is assigned a color, all its neighbors are forced to take the opposite color. If a contradiction appears during propagation, no valid coloring exists. This converts an exponential search into a linear traversal per component.

The presence of self-loops simplifies detection further, because any self-loop immediately violates bipartiteness without needing traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N · M) | O(N) | Too slow |
| BFS/DFS Bipartite Check | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the number of vertices and edges, then build an adjacency list for the graph. This representation allows efficient traversal of neighbors during coloring.
2. While reading edges, immediately check whether an edge connects a vertex to itself. If such an edge exists, the graph cannot be properly colored, because it forces two different colors on the same node. In this case, we can immediately conclude the answer is NO for the test case.
3. Initialize an array `color` of size N with all values unset. This array stores one of two states for each vertex, representing its assigned color in the attempted bipartition.
4. Iterate through every vertex from 1 to N. If a vertex is uncolored, it starts a new BFS or DFS traversal. This step is necessary because the graph may be disconnected, and each connected component must satisfy bipartiteness independently.
5. Assign the starting vertex a color, for example 0, and push it into a queue.
6. While the queue is not empty, extract a vertex and inspect all its neighbors. If a neighbor is uncolored, assign it the opposite color and enqueue it. If it is already colored and has the same color as the current vertex, a contradiction is found and the graph is not bipartite.
7. If all components can be processed without contradiction, output YES.

The critical idea is that coloring is not guessed but forced. Each edge enforces a constraint, and BFS ensures all constraints propagate consistently.

### Why it works

The algorithm maintains the invariant that whenever a vertex is colored, its color is consistent with all previously processed edges within its connected component. BFS ensures that every edge is checked exactly once for consistency, and any violation of bipartiteness appears as a direct conflict between two adjacent vertices with identical assigned colors. Because every vertex is eventually reached from some starting point, all components are validated independently, ensuring global correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        a, b = map(int, input().split())
        if a == b:
            print("NO")
            # consume remaining edges
            for __ in range(_ + 1, m):
                input()
            return
        adj[a].append(b)
        adj[b].append(a)
    
    color = [-1] * (n + 1)
    
    for start in range(1, n + 1):
        if color[start] != -1:
            continue
        
        color[start] = 0
        q = deque([start])
        
        while q:
            v = q.popleft()
            for to in adj[v]:
                if color[to] == -1:
                    color[to] = 1 - color[v]
                    q.append(to)
                elif color[to] == color[v]:
                    print("NO")
                    return
    
    print("YES")

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The solution builds an adjacency list per test case and immediately rejects any self-loop. The BFS uses a queue to propagate alternating colors across edges. The `color` array starts at -1 to represent unvisited vertices, which is essential for distinguishing unprocessed nodes from valid color assignments.

A subtle implementation detail is handling multiple test cases efficiently by rebuilding the graph each time, since N is small but input size can still accumulate. Another important point is ensuring that disconnected components are all checked, which is why the outer loop scans every vertex.

## Worked Examples

Consider a simple bipartite graph with two components:

Input:

```
1
4 2
1 2
3 4
```

| Step | Vertex | Action | Color State | Queue |
| --- | --- | --- | --- | --- |
| 1 | 1 | start BFS, assign 0 | [0, -1, -1, -1] | [1] |
| 2 | 1 | visit neighbors, set 2=1 | [0, 1, -1, -1] | [2] |
| 3 | 2 | done | [0, 1, -1, -1] | [] |
| 4 | 3 | start new BFS, assign 0 | [0, 1, 0, -1] | [3] |
| 5 | 3 | set 4=1 | [0, 1, 0, 1] | [4] |

This confirms that disconnected components are handled independently while preserving bipartite structure.

Now consider a non-bipartite triangle:

Input:

```
1
3 3
1 2
2 3
3 1
```

| Step | Vertex | Action | Color State | Queue |
| --- | --- | --- | --- | --- |
| 1 | 1 | assign 0 | [0, -1, -1] | [1] |
| 2 | 2 | assign 1 | [0, 1, -1] | [2] |
| 3 | 3 | assign 0 | [0, 1, 0] | [3] |
| 4 | 3 | conflict with 1 | contradiction | stop |

The conflict arises when edge (3,1) forces two vertices of the same color to be adjacent, proving the graph is not bipartite.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each vertex is enqueued once and each edge is checked at most twice |
| Space | O(N + M) | Adjacency list plus color array |

Given N ≤ 400 and M up to about 1e5, this is comfortably within limits even for 50 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n, m = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        
        for _ in range(m):
            a, b = map(int, input().split())
            if a == b:
                return "NO"
            adj[a].append(b)
            adj[b].append(a)
        
        color = [-1] * (n + 1)
        
        for i in range(1, n + 1):
            if color[i] != -1:
                continue
            color[i] = 0
            q = deque([i])
            while q:
                v = q.popleft()
                for to in adj[v]:
                    if color[to] == -1:
                        color[to] = 1 - color[v]
                        q.append(to)
                    elif color[to] == color[v]:
                        return "NO"
        return "YES"

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided sample (interpreted cleanly)
assert run("1\n3 2\n1 2\n1 3\n") == "YES"

# self-loop case
assert run("1\n1 1\n1 1\n") == "NO"

# triangle (odd cycle)
assert run("1\n3 3\n1 2\n2 3\n3 1\n") == "NO"

# disconnected bipartite
assert run("1\n4 2\n1 2\n3 4\n") == "YES"

# fully connected bipartite square
assert run("1\n4 4\n1 2\n2 3\n3 4\n4 1\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| self-loop | NO | immediate contradiction detection |
| triangle | NO | odd cycle rejection |
| disconnected edges | YES | component-wise processing |
| square cycle | YES | even cycle bipartiteness |

## Edge Cases

A self-loop is the most direct failure mode. For input `1 1 / 1 1`, the algorithm returns NO immediately before any traversal. This is correct because a node cannot have a different color from itself, and BFS would otherwise never explicitly detect this unless special-cased.

Disconnected graphs are handled by restarting BFS from every unvisited node. Without this, a component containing an odd cycle could be ignored if BFS started elsewhere.

Multiple edges between the same nodes do not affect correctness. Each duplicate edge simply rechecks the same color constraint, but since colors remain consistent, no contradiction arises.
