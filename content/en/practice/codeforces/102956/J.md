---
title: "CF 102956J - Burnished Security Updates"
description: "We are given a network of computers connected by undirected cables, and we need to choose a subset of computers to “activate” under two simultaneous rules. First, no two chosen computers are directly connected by a cable, so the chosen set must be independent in graph terms."
date: "2026-07-04T07:09:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102956
codeforces_index: "J"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Belarusian SU Contest (XXI Open Cup, Grand Prix of Belarus)"
rating: 0
weight: 102956
solve_time_s: 53
verified: true
draft: false
---

[CF 102956J - Burnished Security Updates](https://codeforces.com/problemset/problem/102956/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a network of computers connected by undirected cables, and we need to choose a subset of computers to “activate” under two simultaneous rules. First, no two chosen computers are directly connected by a cable, so the chosen set must be independent in graph terms. Second, every cable must touch at least one chosen endpoint, so every edge must be covered by the chosen vertices. Among all sets that satisfy both constraints, we want the one with the smallest possible number of chosen computers, and we must output its size. If no such set exists, the answer is impossible.

The constraints reach up to three hundred thousand vertices and edges, which immediately rules out anything quadratic or even close. Any solution must be essentially linear in the size of the graph, since even a small factor like n log n is acceptable but anything that repeatedly explores edges in a nested way would time out.

A subtle issue hides in the definition itself: it is not obvious that such a set always exists, or that when it exists it has a simple structure. Another potential pitfall is assuming the set can be chosen greedily without considering global consistency across edges.

A few edge cases clarify the structure:

If the graph has a triangle, such as 1-2-3-1, then any independent set can contain at most one vertex, but any single vertex fails to cover all edges. For example, choosing vertex 1 leaves edge 2-3 uncovered. This input must return -1.

If the graph has no edges at all, then every set is both independent and a vertex cover vacuously. However, the problem requires the chosen set to be non-empty, so the correct answer becomes 1, not 0.

If the graph is a simple chain like 1-2-3-4, then choosing vertices {1, 3} or {2, 4} both satisfy the conditions, and the minimal size depends on how we partition the graph.

These examples already suggest that the structure is closely tied to bipartiteness.

## Approaches

A brute-force attempt would try all subsets of vertices and check both conditions. For each subset, we would verify independence by checking all edges and also verify coverage by scanning all edges again. This leads to roughly O(2^n · m), which is completely infeasible for n up to 300,000.

A more structured observation comes from rewriting the two conditions. If a set S is independent, then no edge has both endpoints in S. If S is also a vertex cover, then every edge has at least one endpoint in S. Combining both statements forces every edge to have exactly one endpoint in S. This means that every edge must go between S and its complement V \ S.

This immediately implies that the graph is bipartite, with S forming one color class and V \ S forming the other. Conversely, in any bipartite graph, either side of the bipartition is independent and also covers all edges. So the problem reduces to checking whether the graph is bipartite, and if so, choosing the smaller side in each connected component.

Each connected component can be colored with two colors. Within a component, we can either pick all vertices of color 0 or all vertices of color 1. To minimize the total size, we choose the smaller color class independently per component. The only remaining complication is that the problem forbids an empty set, so if the graph has no edges at all, we must still return 1 instead of 0.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · m) | O(n) | Too slow |
| Bipartite coloring | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We process each connected component separately using BFS or DFS while assigning two colors.

1. We iterate over all vertices. If a vertex has not been visited, we start a BFS from it.
2. During BFS, we assign the starting vertex color 0 and propagate alternating colors along edges. If we ever see a neighbor already colored with the same color, the graph is not bipartite and we immediately return -1. This is necessary because such a conflict means some edge forces both endpoints into the same side, which breaks the required structure.
3. For each connected component, we maintain counts of how many vertices are colored 0 and how many are colored 1.
4. After finishing a component, we add min(count0, count1) to the answer, since we are free to choose the cheaper side as the selected set for that component.
5. After processing all components, if the total answer is zero, we replace it with 1 because the problem requires a non-empty chosen set.

### Why it works

The coloring enforces that adjacent vertices always lie in opposite sets. This guarantees independence for each color class. The moment both endpoints of an edge would require the same color, the graph cannot be partitioned so that every edge has endpoints on opposite sides, meaning no valid set exists. Once a valid bipartition is found, every edge automatically has one endpoint in each color class, so selecting an entire color class ensures vertex cover property while preserving independence. Minimizing per component is sufficient because components are disconnected, so decisions do not interact.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    color = [-1] * n
    ans = 0

    for i in range(n):
        if color[i] != -1:
            continue

        q = deque([i])
        color[i] = 0
        cnt = [1, 0]

        while q:
            u = q.popleft()
            for v in g[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    cnt[color[v]] += 1
                    q.append(v)
                elif color[v] == color[u]:
                    print(-1)
                    return

        ans += min(cnt[0], cnt[1])

    if ans == 0:
        ans = 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the graph efficiently to support linear traversal. The BFS assigns colors and simultaneously counts the size of each partition in a component. The conflict check inside the BFS is the key correctness gate, since it detects non-bipartite structure immediately.

The final adjustment for the empty answer handles the degenerate case where there are no edges, since in that situation every vertex is isolated and all components contribute zero to the minimum.

## Worked Examples

### Example 1

Input:

```
4 2
1 2
3 4
```

We have two independent edges forming two components.

| Component | Nodes | Color 0 | Color 1 | Chosen |
| --- | --- | --- | --- | --- |
| 1 | {1,2} | 1 | 1 | 1 |
| 2 | {3,4} | 1 | 1 | 1 |

Total answer becomes 2.

This demonstrates that each component is optimized independently, and both partitions are balanced.

### Example 2

Input:

```
4 3
1 2
2 3
1 3
```

This is a triangle.

During BFS coloring, vertex 1 is 0, vertex 2 becomes 1, vertex 3 becomes 0, but edge 1-3 forces both endpoints to have color 0 while also requiring opposite colors, creating a conflict.

The algorithm detects this and returns -1 immediately, matching the fact that no bipartition exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed once during BFS traversal |
| Space | O(n + m) | Adjacency list plus color array |

The constraints allow up to 300,000 vertices and edges, and a single linear traversal fits comfortably within the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    color = [-1] * n
    ans = 0

    for i in range(n):
        if color[i] != -1:
            continue
        q = deque([i])
        color[i] = 0
        cnt = [1, 0]

        ok = True
        while q:
            u = q.popleft()
            for v in g[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    cnt[color[v]] += 1
                    q.append(v)
                elif color[v] == color[u]:
                    ok = False
        if not ok:
            return "-1"
        ans += min(cnt)

    if ans == 0:
        ans = 1

    return str(ans)

# provided sample-like cases
assert run("4 2\n1 2\n3 4\n") == "2"
assert run("4 3\n1 2\n2 3\n1 3\n") == "-1"

# custom cases
assert run("2 0\n") == "1"
assert run("3 2\n1 2\n2 3\n") == "1"
assert run("5 4\n1 2\n2 3\n3 4\n4 5\n") == "2"
assert run("6 3\n1 2\n3 4\n5 6\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes, no edges | 1 | Empty graph requires non-empty set |
| path graph | 1 | Single component bipartite handling |
| chain of 5 | 2 | Optimal split on bipartite path |
| three disjoint edges | 3 | Independent component aggregation |

## Edge Cases

For an empty-edge graph, the algorithm produces all components as isolated vertices, each contributing zero to the answer. Since the accumulated value becomes zero, the final adjustment forces the output to one, matching the requirement that the chosen set cannot be empty even when no edges exist.

For a single odd cycle such as a triangle, BFS coloring inevitably assigns two adjacent vertices the same color at some point in the traversal. The conflict is detected immediately when visiting the closing edge of the cycle, and the algorithm returns -1 without needing to process the rest of the graph.

For disconnected bipartite graphs, each component is handled independently. Even if one component is large and another is a single edge, the decision in one does not affect the other because edges do not cross components, so local minimization is globally optimal.
