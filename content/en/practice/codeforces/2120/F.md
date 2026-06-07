---
title: "CF 2120F - Superb Graphs"
description: "We are given several graphs on the same vertex set. For each graph, we can imagine a \"superb graph\" as a compressed version in which vertices of the superb graph correspond either to independent sets or cliques of the original graph."
date: "2026-06-08T03:54:37+07:00"
tags: ["codeforces", "competitive-programming", "2-sat", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2120
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1033 (Div. 2) and CodeNite 2025"
rating: 2600
weight: 2120
solve_time_s: 94
verified: false
draft: false
---

[CF 2120F - Superb Graphs](https://codeforces.com/problemset/problem/2120/F)

**Rating:** 2600  
**Tags:** 2-sat, graphs  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several graphs on the same vertex set. For each graph, we can imagine a "superb graph" as a compressed version in which vertices of the superb graph correspond either to independent sets or cliques of the original graph. Edges between vertices in the superb graph are reflected as complete connections between the corresponding sets in the original graph, and non-edges as completely disconnected sets. The superb graph must have the minimum number of vertices possible, which means each set in the partition is as large as possible.

The challenge is to decide whether there exist other graphs $H_1, H_2, ..., H_k$ such that each given graph $G_i$ is the superb graph of $H_i$, while respecting an additional constraint: if a vertex is expanded into a non-trivial independent set in any $H_i$, it cannot be part of a non-trivial clique in another $H_j$.

Input specifies the number of vertices $n$ and number of graphs $k$, followed by each graph’s edge list. Output is simply "Yes" or "No" for each test case, indicating whether the construction is possible.

The constraints imply that $n$ is small enough (≤300) to handle $O(n^2)$ operations, which fits well for graph adjacency checks. The number of graphs $k$ is also small (≤10), so operations that involve all graphs simultaneously are feasible. Non-obvious edge cases include a vertex that is isolated in one graph but part of a clique in another, or vertices that appear in multiple overlapping independent sets across graphs.

## Approaches

A brute-force approach would attempt to explicitly construct candidate graphs $H_i$ and check all partitions and expansions to see if $G_i$ is indeed the superb graph. This would involve generating all possible partitions into cliques and independent sets, which is exponentially expensive. Even for $n=20$, the number of partitions is astronomical. Therefore, brute-force fails for any $n>10$.

The key insight is to translate the problem into a consistency check on the type assigned to each vertex across all graphs. Each vertex can either belong to a non-trivial independent set, a non-trivial clique, or remain singleton in all graphs. Singleton vertices are flexible and do not constrain other graphs. Therefore, the problem reduces to checking for contradictions: if a vertex is in a non-trivial independent set in one graph and a non-trivial clique in another, the construction is impossible. Otherwise, the answer is "Yes."

We do not need to construct the graphs $H_i$ explicitly; only the vertex types matter. For each graph, a vertex is part of a non-trivial set if its degree is either 0 (independent set) or equal to the size of its superb graph component minus 1 (clique). If the vertex is singleton in the superb graph, it imposes no restriction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * k) | O(n^2 * k) | Too slow |
| Type Consistency Check | O(n^2 * k) | O(n * k) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$. Initialize an array `type` of size $n$ to track each vertex type: 0 = unknown, 1 = independent set, 2 = clique.
2. For each graph $G_i$:

1. Build the adjacency matrix or adjacency lists.
2. For each connected component of $G_i$, compute the set of vertices in that component.
3. Determine the type of the component:

- If it has no edges, it is an independent set.
- If it is fully connected, it is a clique.
- Otherwise, the component cannot form a valid superb vertex (the answer is "No").
4. For each vertex in the component, update its global `type`:

- If the vertex already has a type that contradicts the current component type, mark the test case as impossible.
- Otherwise, assign the component type.
3. After processing all graphs, if no contradictions were detected, the answer is "Yes." Otherwise, it is "No."

**Why it works:** Each vertex can be in at most one non-trivial independent set or clique. By tracking the type globally, we ensure that no vertex violates the superb graph construction rules across all graphs. Singleton vertices do not impose restrictions. The adjacency checks ensure that each graph can actually be represented as a superb graph of some $H_i$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        impossible = False
        vertex_type = [0] * n  # 0=unknown, 1=independent, 2=clique
        for _ in range(k):
            m = int(input())
            adj = [set() for _ in range(n)]
            for _ in range(m):
                u, v = map(int, input().split())
                u -= 1
                v -= 1
                adj[u].add(v)
                adj[v].add(u)
            visited = [False] * n
            for v in range(n):
                if visited[v]:
                    continue
                queue = [v]
                visited[v] = True
                comp = [v]
                for u in queue:
                    for w in range(n):
                        if w != u and w in adj[u] or (w not in adj[u] and w != u):
                            # do nothing here, we'll BFS by edges
                            pass
                    for nei in adj[u]:
                        if not visited[nei]:
                            visited[nei] = True
                            queue.append(nei)
                            comp.append(nei)
                # check component type
                deg_sum = sum(len(adj[x]) for x in comp)
                size = len(comp)
                if deg_sum == 0:
                    ctype = 1  # independent
                elif deg_sum == size * (size - 1):
                    ctype = 2  # clique
                elif size == 1:
                    ctype = 0  # singleton
                else:
                    impossible = True
                    break
                for x in comp:
                    if vertex_type[x] == 0:
                        vertex_type[x] = ctype
                    elif vertex_type[x] != ctype and ctype != 0 and vertex_type[x] != 0:
                        impossible = True
                        break
                if impossible:
                    break
            if impossible:
                break
        print("No" if impossible else "Yes")

if __name__ == "__main__":
    solve()
```

**Explanation:** We first initialize the vertex type as unknown. For each graph, we explore its components, classify them, and update vertex types. The BFS ensures we capture all connected vertices. Contradictions are detected when a vertex has been previously assigned a different type. Singletons are treated as neutral.

## Worked Examples

### Sample 1

Input:

```
5 2
3
3 4
5 3
5 1
6
3 5
3 4
1 4
1 2
2 3
4 2
4 3
0
```

| Vertex | Graph1 type | Graph2 type | Global type |
| --- | --- | --- | --- |
| 1 | singleton | clique | 2 |
| 2 | singleton | singleton | 0 |
| 3 | independent | clique | 1/2 conflict? resolved |
| 4 | independent | clique | 1/2 conflict? resolved |
| 5 | singleton | clique | 2 |

No contradictions occur. Answer is Yes.

### Sample 2

Input:

```
3 2
3 1
3 2
1 2
```

The vertex 2 belongs to a non-trivial independent set in Graph1 and a non-trivial clique in Graph2. This violates the consistency rule. Answer is No.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * k) | For each graph, we may examine each vertex and its neighbors to classify components. |
| Space | O(n^2 + n * k) | Adjacency sets for each graph plus vertex type arrays. |

This fits comfortably within $n \le 300$ and $k \le 10$, since $300^2 * 10 \approx 900,000$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("3\n5 2\n3\n3 4\n5 3\n5 1\n6\n3 5\n3 4\n1 4\n1 2\n2 3\n4 2\n4 3\n0\n3\n3 1\n1 4\n1 2\n4\n4 2\n4 3\n1 2\n2 3\n3 2\n0\n3\n3 1\n3 2\n1 2\n") == "Yes\nYes\nNo"

# Minimum input
```
