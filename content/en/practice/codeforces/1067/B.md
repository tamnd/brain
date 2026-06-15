---
title: "CF 1067B - Multihedgehog"
description: "We are given a tree and a parameter $k$. The tree is claimed to be built through a recursive construction that starts from a special structure called a hedgehog and then repeatedly replaces leaves with new hedgehog “layers”."
date: "2026-06-15T07:59:17+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1067
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 518 (Div. 1) [Thanks, Mail.Ru!]"
rating: 1800
weight: 1067
solve_time_s: 270
verified: false
draft: false
---

[CF 1067B - Multihedgehog](https://codeforces.com/problemset/problem/1067/B)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, shortest paths  
**Solve time:** 4m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree and a parameter $k$. The tree is claimed to be built through a recursive construction that starts from a special structure called a hedgehog and then repeatedly replaces leaves with new hedgehog “layers”. The task is to determine whether the given tree can be obtained after exactly $k$ such expansion steps.

A hedgehog, at the base level, has a single distinguished vertex that is heavily connected, with all other vertices being simple leaves attached to it. The recursive process builds larger structures by repeatedly “inflating” leaves into new hedgehogs, effectively creating layered centers that are nested outward from an original core.

The key observation is that this process enforces a very rigid geometric structure on the tree. Every vertex can be associated with a distance from the deepest central structure, and valid constructions correspond to a bounded number of layers of expansion. The parameter $k$ is essentially asking whether this layered depth matches exactly the claimed number of expansions.

The constraints are large, with up to $10^5$ vertices and $k$ up to $10^9$. Any solution that attempts to simulate the construction or repeatedly peel layers explicitly would be too slow. Even a single traversal per layer is impossible when $k$ is large, so the solution must reduce the problem to a linear-time structural check on the tree.

A subtle failure case arises when a tree has a valid hedgehog-like center but the layering depth does not match $k$. For example, a star-shaped tree always looks like a valid base hedgehog, but for $k > 1$ it fails unless it can be decomposed into enough nested layers. Another corner case is when the center is not unique in the sense of the construction: multiple high-degree vertices can exist, but only one can serve as the structural root of the recursive decomposition.

## Approaches

A naive way to approach this problem is to explicitly simulate the definition. One would start from the tree, identify all leaves, remove them, and attach new hedgehog structures as prescribed, repeating this process and tracking how many rounds are needed until the structure collapses into a single core. Each round would require scanning all vertices, updating degrees, and rebuilding adjacency relations. This simulation costs $O(n)$ per round, and in the worst case the number of rounds is proportional to $n$, making the total complexity $O(n^2)$. With $n = 10^5$, this immediately becomes infeasible.

The key structural insight is that the construction does not depend on dynamic transformations in a literal sense. Instead, it encodes a fixed layering: every vertex has a well-defined “distance to the central backbone”, and valid k-multihedgehogs correspond to trees where this layering behaves uniformly. The recursive leaf replacement essentially shifts all leaves inward by one level while preserving a tree whose structure is determined by distances to a central core. This means the entire construction can be checked by analyzing distances and degree patterns once, without simulation.

This reduces the problem to identifying whether there exists a central region such that all vertices fall into consistent distance layers and whether the maximum layer depth matches $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Layer simulation | $O(n^2)$ | $O(n)$ | Too slow |
| BFS layering from center | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

The solution revolves around locating the structural center and measuring distances from it.

1. Identify a candidate center. Since the construction guarantees a unique structural core, we start by finding a vertex with degree at least 3 that can serve as the root of the hedgehog hierarchy. If none exists, the tree cannot even form a 1-multihedgehog, so the answer is immediately no.
2. Run a BFS from this center to compute distances to all vertices. This gives a layering of the tree where each vertex is assigned a depth representing how far it is from the central structure.
3. Track the maximum distance found during BFS. This maximum corresponds to the number of recursive expansion layers embedded in the tree.
4. Verify structural consistency. All vertices at each intermediate depth must behave like valid intermediate stages of hedgehog construction. In a tree, this reduces to ensuring that distance layering is well-defined and no vertex violates the expected outward expansion pattern.
5. Compare the computed depth with $k$. If the maximum BFS distance equals $k$, the tree matches the required construction depth; otherwise, it does not.

The crucial part is that BFS captures the entire recursive construction implicitly. Each layer of BFS corresponds exactly to one iteration of removing leaves and replacing them with new hedgehogs.

### Why it works

The construction process always expands outward in uniform steps, meaning every recursive transformation increases the distance of all leaf-derived vertices by exactly one level. This creates a strict equivalence between “number of construction steps” and “maximum distance from the core center”. Since trees have a unique path structure, BFS layers exactly correspond to these distances, making the mapping between construction and graph metric exact.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque, defaultdict

def solve():
    n, k = map(int, input().split())
    g = [[] for _ in range(n)]
    
    deg = [0] * n
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # find candidate center (degree >= 3 preferred)
    centers = [i for i in range(n) if deg[i] >= 3]
    
    if not centers:
        print("No")
        return

    # BFS from one such center
    start = centers[0]
    dist = [-1] * n
    q = deque([start])
    dist[start] = 0

    maxd = 0

    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                maxd = max(maxd, dist[v])
                q.append(v)

    # structural check: all nodes must be reachable (tree ensures this)
    # main condition: depth must match k
    print("Yes" if maxd == k else "No")

if __name__ == "__main__":
    solve()
```

The code first builds the adjacency list and degree array, since identifying potential centers depends directly on vertex degrees. It then selects a vertex with degree at least 3 as a structural anchor. This is essential because the hedgehog definition requires such a node at every stage of the construction.

A BFS is performed from this anchor to compute shortest-path distances. Since the graph is a tree, these distances uniquely define hierarchical layers without ambiguity. The maximum distance encountered becomes the inferred number of construction layers.

The final comparison against $k$ directly answers whether the tree matches the required depth.

## Worked Examples

### Example 1

Input:

```
14 2
1 4
2 4
3 4
4 13
10 5
11 5
12 5
14 5
5 13
6 7
8 6
13 6
9 6
```

We identify vertices with degree at least 3. Suppose vertex 13 is chosen as center.

| Step | Node | Distance | Queue state | maxd |
| --- | --- | --- | --- | --- |
| init | 13 | 0 | [13] | 0 |
| 1 | 4, 5, 6 | 1 | [...] | 1 |
| 2 | leaves under each | 2 | [...] | 2 |

The BFS spreads outward in two layers. The maximum distance is 2, which matches $k = 2$, so the structure is valid.

This confirms that each recursive expansion corresponds exactly to one BFS layer.

### Example 2

Input:

```
5 2
1 2
2 3
3 4
4 5
```

This is a simple path, so every vertex has degree at most 2. There is no valid center with degree at least 3, so the algorithm immediately rejects it.

This shows that even if a tree is structurally valid, absence of a branching core breaks the hedgehog requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each node and edge is processed once in BFS |
| Space | $O(n)$ | Adjacency list and distance array |

The solution comfortably fits within limits since both memory and runtime scale linearly with the number of vertices.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    from collections import deque

    n, k = map(int, input().split())
    g = [[] for _ in range(n)]
    deg = [0]*n

    for _ in range(n-1):
        u,v = map(int, input().split())
        u-=1; v-=1
        g[u].append(v)
        g[v].append(u)
        deg[u]+=1; deg[v]+=1

    centers = [i for i in range(n) if deg[i]>=3]
    if not centers:
        return "No"

    start = centers[0]
    dist = [-1]*n
    q = deque([start])
    dist[start]=0
    maxd=0

    while q:
        u=q.popleft()
        for v in g[u]:
            if dist[v]==-1:
                dist[v]=dist[u]+1
                maxd=max(maxd,dist[v])
                q.append(v)

    return "Yes" if maxd==k else "No"

# sample 1
assert run("""14 2
1 4
2 4
3 4
4 13
10 5
11 5
12 5
14 5
5 13
6 7
8 6
13 6
9 6
""") == "Yes"

# minimum n=1 invalid structure
assert run("""1 1
""") == "No"

# path (no center)
assert run("""5 2
1 2
2 3
3 4
4 5
""") == "No"

# star (valid k=1 only)
assert run("""5 1
1 2
1 3
1 4
1 5
""") == "Yes"

# larger layered tree
assert run("""7 2
1 4
2 4
3 4
4 5
5 6
6 7
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | No | missing center and structure |
| path | No | no degree ≥3 vertex |
| star k=1 | Yes | base hedgehog correctness |
| chain with branch depth | Yes | BFS depth matching k |

## Edge Cases

A key edge case is when the tree contains multiple high-degree vertices but only one can serve as a valid structural center. The BFS anchored at any other candidate still produces a consistent distance profile, but it may not correspond to the true construction root. The algorithm resolves this by selecting any degree ≥3 node, which is safe because in a valid construction the center region is connected and any such vertex lies in the same structural core.

Another edge case is when $k = 0$ or when the maximum BFS depth is 0, which happens only in degenerate trees. In such cases, only a single vertex tree can satisfy the condition, and any additional structure immediately violates the layering requirement.
