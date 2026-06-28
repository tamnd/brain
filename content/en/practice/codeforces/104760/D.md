---
title: "CF 104760D - \u0412\u0435\u0441\u0435\u043b\u044b\u0435 \u0444\u043e\u043d\u0430\u0440\u0438"
description: "We are given a graph where vertices represent lamps and edges represent streets connecting pairs of lamps. Each street imposes a constraint: the two lamps at its ends must not share the same color after repainting."
date: "2026-06-28T22:02:05+07:00"
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

We are given a graph where vertices represent lamps and edges represent streets connecting pairs of lamps. Each street imposes a constraint: the two lamps at its ends must not share the same color after repainting. Each lamp can be painted using one of two available colors, so the task is equivalent to deciding whether we can assign one of two colors to every vertex such that every edge connects vertices of different colors.

The graph may contain self-loops and multiple edges between the same pair of vertices. A self-loop immediately creates a contradiction because it requires a vertex to differ from itself. Multiple edges between the same pair do not change the constraint, they only repeat it.

The number of vertices per test is up to 400, and there can be up to 50 tests. Even though the number of edges can reach about 80,000 in the worst case, this is still small enough that an $O(N + M)$ or $O(N^2)$ per test solution is easily sufficient. Anything relying on exponential search over colorings is infeasible since $2^{400}$ is far beyond any limit.

A few corner situations matter.

A graph with no edges is always valid because there are no constraints at all. For example, $N=5, M=0$ should output YES.

A graph containing a self-loop is always invalid. For example, $N=1, M=1, (1,1)$ must output NO because the single vertex cannot be colored differently from itself.

A disconnected graph must be checked component by component. One bad component makes the entire graph invalid.

## Approaches

The brute-force idea is to try every possible assignment of two colors to the $N$ vertices and check whether all edges satisfy the constraint. Each assignment requires scanning all edges, which costs $O(M)$, and there are $2^N$ assignments, giving $O(2^N \cdot M)$. With $N=400$, this is completely unusable.

The key observation is that the condition on edges is exactly the definition of a bipartite graph. We do not need to search over all assignments; we only need to check whether such a coloring exists. Bipartite checking can be done by BFS or DFS: we pick an uncolored vertex, assign it a color, and propagate alternating colors along edges. If we ever see a contradiction, the graph is not bipartite.

Self-loops can be handled immediately as failure, since they force a vertex to differ from itself. Parallel edges do not affect correctness because they impose identical constraints repeatedly.

This reduces the problem to a standard graph traversal over all components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N \cdot M)$ | $O(N)$ | Too slow |
| BFS/DFS Bipartite Check | $O(N + M)$ | $O(N + M)$ | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph. If an edge connects a vertex to itself, immediately mark the test as impossible. This is because a self-loop enforces a contradiction regardless of coloring.
2. Maintain an array `color` initialized to -1 for all vertices, meaning uncolored. We will use two colors, 0 and 1.
3. Iterate through all vertices from 1 to N. Whenever we find an uncolored vertex, we start a BFS from it and assign it color 0.
4. In BFS, remove a vertex `v` from the queue and examine all neighbors `u`. If `u` is uncolored, assign it the opposite color of `v` and push it into the queue.
5. If `u` is already colored and has the same color as `v`, we immediately conclude the graph is not bipartite and stop.
6. Repeat this process for every disconnected component. If no contradictions are found, the graph is valid.

The key idea is that BFS enforces constraints locally while propagating decisions globally. Each edge acts as a parity constraint between two vertices.

### Why it works

The BFS process maintains an invariant: whenever a vertex is colored, its color is consistent with all already-processed paths from the BFS source. Each edge enforces a parity relation, and BFS ensures that parity assignments remain consistent along all discovered paths. If a contradiction arises, it means there are two different parity requirements for the same vertex, which implies an odd cycle or a self-loop exists in that component, making a two-coloring impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        parts = list(map(int, input().split()))
        n, m = parts[0], parts[1]
        edges = parts[2:]

        adj = [[] for _ in range(n + 1)]
        bad = False

        idx = 0
        for _ in range(m):
            a = edges[idx]
            b = edges[idx + 1]
            idx += 2

            if a == b:
                bad = True
            else:
                adj[a].append(b)
                adj[b].append(a)

        if bad:
            out.append("NO")
            continue

        color = [-1] * (n + 1)

        def bfs(start):
            q = deque([start])
            color[start] = 0

            while q:
                v = q.popleft()
                for u in adj[v]:
                    if color[u] == -1:
                        color[u] = color[v] ^ 1
                        q.append(u)
                    elif color[u] == color[v]:
                        return False
            return True

        ok = True
        for i in range(1, n + 1):
            if color[i] == -1:
                if not bfs(i):
                    ok = False
                    break

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The adjacency list construction ensures we can traverse neighbors efficiently. The early check for self-loops avoids unnecessary traversal. The BFS function enforces alternating colors and detects conflicts immediately. The XOR operation `color[v] ^ 1` is a compact way to flip between the two colors.

The outer loop ensures disconnected components are also validated.

## Worked Examples

### Example 1

Input:

```
3 1
1 2
1 3
```

This graph has edges (1,2) and (1,3). We expect YES.

| Step | Queue | Coloring | Action |
| --- | --- | --- | --- |
| Start | [1] | 1=0 | initialize |
| Pop 1 | [] | 2=1, 3=1 | assign neighbors |
| Push neighbors | [2,3] | consistent | continue |
| Process rest | [] | no conflicts | finish |

No contradiction appears, so the graph is bipartite.

### Example 2

Input:

```
3 3
1 2
2 3
1 3
```

This is a triangle, so it is impossible.

| Step | Queue | Coloring | Action |
| --- | --- | --- | --- |
| Start | [1] | 1=0 | initialize |
| Pop 1 | [] | 2=1, 3=1 | assign |
| Pop 2 | [3] | check 3 | conflict (3 already 1, expected 0) |

A contradiction occurs on edge (2,3), confirming the odd cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + M)$ | each vertex and edge processed once during BFS |
| Space | $O(N + M)$ | adjacency list plus color array |

The constraints allow up to 400 vertices and about 80,000 edges per test, so this linear traversal easily fits within limits even for 50 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            parts = list(map(int, input().split()))
            n, m = parts[0], parts[1]
            edges = parts[2:]

            adj = [[] for _ in range(n + 1)]
            bad = False

            idx = 0
            for _ in range(m):
                a = edges[idx]
                b = edges[idx + 1]
                idx += 2
                if a == b:
                    bad = True
                else:
                    adj[a].append(b)
                    adj[b].append(a)

            if bad:
                out.append("NO")
                continue

            color = [-1] * (n + 1)

            def bfs(s):
                q = deque([s])
                color[s] = 0
                while q:
                    v = q.popleft()
                    for u in adj[v]:
                        if color[u] == -1:
                            color[u] = color[v] ^ 1
                            q.append(u)
                        elif color[u] == color[v]:
                            return False
                return True

            for i in range(1, n + 1):
                if color[i] == -1:
                    if not bfs(i):
                        out.append("NO")
                        break
            else:
                out.append("YES")

        return "\n".join(out)

    return solve()

# provided sample (interpreted)
assert run("3\n3 1 1 2 1 3\n3 3 1 2 2 3 1 3\n1 0\n") == "YES\nNO\nYES"

# custom: no edges
assert run("1\n5 0\n") == "YES"

# custom: self loop
assert run("1\n2 1 1 1\n") == "NO"

# custom: disconnected bipartite
assert run("1\n4 2 1 2 3 4\n") == "YES"

# custom: odd cycle
assert run("1\n3 3 1 2 2 3 3 1\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 isolated nodes | YES | empty graph validity |
| self-loop | NO | immediate contradiction |
| two edges in disjoint pairs | YES | disconnected components |
| triangle cycle | NO | odd cycle detection |

## Edge Cases

A self-loop is the most direct failure case. If we take input `1 1 1 1`, the adjacency construction flags it immediately and returns NO without even attempting BFS. This is correct because any coloring would require a vertex to differ from itself.

Disconnected components are handled by restarting BFS whenever a new uncolored vertex is found. For a graph like `1-2` and `3-4`, the BFS from 1 colors only its component, then BFS from 3 handles the second component independently. Since both are bipartite, the final result is YES.

Odd cycles produce a contradiction during traversal. In a triangle, BFS assigns alternating colors but eventually encounters an edge forcing equality between two vertices already constrained to differ, exposing inconsistency and correctly rejecting the graph.
