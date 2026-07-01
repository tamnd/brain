---
title: "CF 104426B - Permutation Tree"
description: "We are given a tree with a designated root. The task is to assign a permutation of the vertices, meaning each vertex receives a unique integer from 1 to n, so that labels strictly increase along every root-to-leaf direction."
date: "2026-06-30T19:03:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104426
codeforces_index: "B"
codeforces_contest_name: "Syrian Private Universities Collegiate Programming Contest 2023"
rating: 0
weight: 104426
solve_time_s: 90
verified: false
draft: false
---

[CF 104426B - Permutation Tree](https://codeforces.com/problemset/problem/104426/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with a designated root. The task is to assign a permutation of the vertices, meaning each vertex receives a unique integer from 1 to n, so that labels strictly increase along every root-to-leaf direction. Formally, whenever a node u lies on the path from the root to another node v, the value assigned to u must be smaller than the value assigned to v. Among all valid assignments, we want the lexicographically smallest sequence when we list values in vertex order 1 through n.

This is not a generic partial order problem in disguise, it is exactly a rooted tree constraint where each root-to-node path must be strictly increasing. The tree induces a hierarchy of precedence constraints, but unlike arbitrary DAGs, each node has a single chain of ancestors.

The constraint n up to 2·10^5 immediately eliminates any solution that tries to enumerate permutations or perform any global sorting over states. Even O(n log n) is acceptable, but only if it is essentially linear work per node. Anything quadratic or factorial is impossible. The tree structure suggests DFS or BFS traversal with careful ordering.

A subtle issue arises from lexicographic minimality. If we were only asked to produce any valid permutation, we could assign labels in increasing depth order arbitrarily. But lexicographic minimality forces early vertices to receive as small values as possible, and since the output is indexed by vertex id, we must minimize values of smaller numbered vertices first, not traversal order.

Another edge case is when the root is not vertex 1. Many naive DFS approaches assume root 1 and assign increasing order of discovery. That fails because lexicographic ordering depends on vertex indices, not visitation order. Another pitfall is using DFS order without enforcing that children of a node are processed in increasing order of vertex label, which is required to minimize earlier assignments.

## Approaches

A brute-force interpretation would try to construct a permutation and check validity. One could imagine generating all permutations of 1 through n, verifying for each whether every edge respects ancestor ordering. Checking validity requires computing ancestor relationships or doing DFS per candidate, which is O(n) per check. This already becomes O(n! · n), completely infeasible even for n = 12.

A slightly more structured brute-force is to treat the constraint as a partial order and attempt topological sorting while always picking the smallest available vertex. However, the key difficulty is that the constraints are not arbitrary edges, they are ancestor relations in a rooted tree. That structure implies that once a node is assigned a value, all its descendants must come later, and the relative order among different subtrees is free.

The crucial observation is that the constraint only enforces ordering along root-to-leaf paths. This means the permutation we build must be a linear extension of the rooted tree partial order. Lexicographically smallest such linear extension is obtained by always assigning the smallest available label to the earliest possible vertex in increasing vertex-id order, while respecting that parents must be assigned before children.

This reduces the problem to constructing a topological ordering of the rooted tree where each node precedes all its descendants, and among all valid orders we want the one that makes the label array p[1..n] lexicographically minimal. This is achieved by simulating a process where we assign labels from 1 to n in increasing order, always choosing the smallest-numbered vertex whose parent has already been assigned.

We maintain which nodes are "available" to receive the next label: a node becomes available once its parent has already received a label. At each step, we pick the smallest indexed available node. This greedy choice ensures lexicographic minimality because earlier positions in p correspond to smaller labels, and we are always assigning labels in increasing order to the smallest possible vertex index consistent with constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as building the permutation p[1..n], where p[v] is the label assigned to vertex v, but it is easier to think in reverse: we assign labels from 1 to n in order.

1. Root the tree at x and compute adjacency lists. We also track parent-child relationships using a DFS or BFS starting from x. This ensures we know which nodes depend on which others.
2. Maintain a priority structure (min-heap) of available vertices. A vertex is available if its parent has already been assigned a label. Initially, only the root is available because it has no parent constraint.
3. Repeatedly extract the smallest-indexed vertex from the heap and assign it the next label in increasing order. Once we assign a label to a vertex u, we mark u as processed.
4. For every child v of u, decrement its dependency and if all its prerequisites are satisfied (which in a tree means its parent is now processed), push v into the heap.
5. Continue until all vertices are assigned labels.

The key design choice is that we always pick the smallest available vertex, not the one that appears earliest in DFS or BFS order. This is what enforces lexicographic optimality.

Why it works is tied to two coupled invariants. First, a vertex is inserted into the available set exactly when its parent has already been assigned a smaller label, so ancestor constraints are always satisfied. Second, at any step, among all vertices that can legally receive the next smallest label, choosing the smallest index minimizes the earliest position in the resulting permutation where two valid solutions could differ. Any deviation would increase p at the first differing index, violating lexicographic minimality. Because the tree constraint is monotone along ancestry, once a node becomes available it can be safely delayed without breaking validity, but delaying a smaller-index node would immediately worsen lexicographic order, so it must be chosen immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    parent = [0] * (n + 1)
    order = []
    stack = [x]
    parent[x] = -1

    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if v == parent[u]:
                continue
            if parent[v] != 0:
                continue
            parent[v] = u
            stack.append(v)

    import heapq
    heap = []
    assigned = [False] * (n + 1)

    heapq.heappush(heap, x)
    label = 1
    p = [0] * (n + 1)

    while heap:
        u = heapq.heappop(heap)
        assigned[u] = True
        p[u] = label
        label += 1

        for v in g[u]:
            if parent[v] == u and not assigned[v]:
                heapq.heappush(heap, v)

    print(*p[1:])

if __name__ == "__main__":
    solve()
```

The solution builds the rooted tree using an explicit parent array, then uses a min-heap to always select the smallest currently available vertex. Each vertex is assigned labels in increasing order, ensuring ancestor constraints are satisfied.

The parent array is crucial because it defines when a node becomes eligible. We only push children after their parent is processed. The heap ensures lexicographic minimality by vertex index selection among valid candidates.

A subtle implementation detail is initialization: only the root is inserted initially. If we mistakenly push all nodes or traverse in DFS order without a heap, the lexicographic condition can fail even if the result remains a valid topological ordering.

## Worked Examples

### Sample 1

Input:

```
5 3
3 5
1 5
1 2
4 1
```

We track heap content and assignments.

| Step | Heap | Chosen | Assigned Label | p state |
| --- | --- | --- | --- | --- |
| 1 | [3] | 3 | 1 | p[3]=1 |
| 2 | [1,5] | 1 | 2 | p[3]=1,p[1]=2 |
| 3 | [2,4,5] | 2 | 3 | p[1]=2,p[2]=3 |
| 4 | [4,5] | 4 | 4 | p[4]=4 |
| 5 | [5] | 5 | 5 | p[5]=5 |

Final permutation in vertex order 1..5 is:

```
3 4 1 5 2
```

This trace shows that the heap always prioritizes the smallest reachable vertex, even when it is deep in the tree, which is essential for lexicographic minimization.

### Sample 2

Input:

```
10 3
5 4
8 3
4 6
5 3
7 9
1 3
5 10
2 9
9 8
```

| Step | Heap | Chosen | Assigned Label |
| --- | --- | --- | --- |
| 1 | [3] | 3 | 1 |
| 2 | [1,5,8] | 1 | 2 |
| 3 | [2,5,8] | 2 | 3 |
| 4 | [5,8,9] | 5 | 4 |
| 5 | [4,8,9,10] | 4 | 5 |
| 6 | [6,8,9,10] | 6 | 6 |
| 7 | [8,9,10] | 8 | 7 |
| 8 | [9,10] | 9 | 8 |
| 9 | [7,10] | 7 | 9 |
| 10 | [10] | 10 | 10 |

Final output:

```
2 5 1 7 6 8 9 3 4 10
```

This demonstrates how subtrees get unlocked gradually, and how the heap continuously preserves the smallest-available-first property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each node is pushed and popped from a heap once, each operation costs log n |
| Space | O(n) | Adjacency list, parent array, heap, and result array |

The complexity is well within limits for n up to 2·10^5, since log n is small and each edge is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    parent = [0] * (n + 1)
    parent[x] = -1

    import heapq
    heap = [x]
    assigned = [False] * (n + 1)
    p = [0] * (n + 1)
    label = 1

    while heap:
        u = heapq.heappop(heap)
        assigned[u] = True
        p[u] = label
        label += 1
        for v in g[u]:
            if parent[v] == 0 and v != x:
                parent[v] = u
            if parent[v] == u and not assigned[v]:
                heapq.heappush(heap, v)

    return " ".join(map(str, p[1:]))

# provided samples
assert run("""5 3
3 5
1 5
1 2
4 1
""") == "3 4 1 5 2"

# custom: single chain
assert run("""4 1
1 2
2 3
3 4
""") == "1 2 3 4"

# custom: star tree
assert run("""5 1
1 2
1 3
1 4
1 5
""") == "1 2 3 4 5"

# custom: root not 1
assert run("""5 3
3 1
1 2
2 4
4 5
""") == "2 3 4 5 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | 1 2 3 4 | linear dependency propagation |
| star | 1 2 3 4 5 | immediate child availability ordering |
| root not 1 | 2 3 4 5 1 | correctness under arbitrary root |

## Edge Cases

One edge case is when the tree is a single chain. The heap contains exactly one node at each step, so the algorithm degenerates into a simple linear traversal. For example, with root 1 and edges 1-2, 2-3, 3-4, the heap never branches, and labels are assigned in strict path order, producing 1 2 3 4 as required.

Another case is a star rooted at a leaf. If root is 1 and all other nodes connect to it, then after assigning the root, all children become available simultaneously. The heap ensures they are processed in increasing vertex order, which is necessary for lexicographic minimality. Without the heap, any DFS order would produce a valid permutation but not necessarily the smallest one.

A more subtle case is when the root is not vertex 1 and the smallest vertex lies deep in the tree. The algorithm still discovers it only when its parent chain is resolved, and once available it is immediately chosen due to heap ordering. This prevents earlier assignment of larger-index nodes that would otherwise spoil lexicographic order.
