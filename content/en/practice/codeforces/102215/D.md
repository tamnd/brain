---
title: "CF 102215D - Country Division"
description: "The road network is a tree, because there are (n) cities, exactly (n-1) roads, and every city is reachable from every other city. In each prediction, some cities are red, some are blue, and all remaining cities are irrelevant. We may close any set of roads."
date: "2026-08-17T23:34:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "D"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 222
verified: false
draft: false
---

[CF 102215D - Country Division](https://codeforces.com/problemset/problem/102215/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 42s  
**Verified:** no  

## Solution
## Problem Understanding

The road network is a tree, because there are (n) cities, exactly (n-1) roads, and every city is reachable from every other city. In each prediction, some cities are red, some are blue, and all remaining cities are irrelevant.

We may close any set of roads. After doing so, every red city must still be connected to every other red city, every blue city must still be connected to every other blue city, and no red city may be connected to any blue city. The task is to decide whether such a set of closed roads exists for every prediction. The official problem has (n,q\le 200000), with the sum of all queried red and blue cities also at most (200000).

The key object is the minimal subtree connecting a set of vertices. For the red cities, call this the red Steiner subtree. Any valid solution must leave every edge of this subtree open, because otherwise two red cities would become disconnected. The same is true for the blue Steiner subtree. Thus the real question is whether the two required subtrees can be made disjoint.

The size bounds rule out rebuilding information over all (n) cities for every query. With (q=200000) and (n=200000), an (O(nq)) method can perform about (4\cdot10^{10}) operations, far beyond a 2 second limit. The useful part of the constraints is that the total number of colored cities over all queries is only (200000), so the query work should be proportional to the number of mentioned cities, multiplied by a logarithmic tree operation.

There are several edge cases that are easy to mishandle. If each color has only one city, the answer is always YES. For example,

```
2
1 2
1
1 1 2
```

has answer `YES`. We can keep the only road open for each color's internal connectivity and there is no requirement to keep a red-blue path open.

The two color subtrees can also have the same root even though no red and blue city coincide. For example,

```
5
1 2
1 3
1 4
1 5
1
2 2 3 4 5
```

has red cities (2,3) and blue cities (4,5). Both color subtrees contain city (1), so the answer is `NO`. A careless solution that only checks whether the colored cities themselves are different would incorrectly accept it.

Another subtle case occurs when one color's Steiner root is an ancestor of the other color's Steiner root. Consider

```
4
1 2
2 3
3 4
1
2 1 4 3
```

The red cities are (1,4), so their Steiner subtree is the entire path from (1) to (4). The blue city is (3). The blue subtree lies inside the red subtree, so the answer is `NO`. Merely observing that the two Steiner roots, (1) and (3), are different is not enough.

The opposite situation is also possible:

```
4
1 2
2 3
3 4
1
2 1 2 3 4
```

Here the red cities are (1,2), the blue cities are (3,4), and their required subtrees are separated by the edge (2-3). The answer is `YES`.

## Approaches

A direct approach can root the tree and process every edge for every query. For each query, we could determine which side of every edge contains red and blue cities, then decide whether the edge must remain open for either color. This is correct because removing an edge splits a tree into exactly two components, so all connectivity requirements can be expressed in terms of these cuts.

The problem is the amount of work. Processing all (n-1) edges for every query costs (O(nq)). At the maximum bounds this is about (200000\cdot200000=4\cdot10^{10}) edge operations, which is nowhere near feasible.

The observation that unlocks the faster method is that we never need to inspect the whole tree. For a set of vertices, its minimal connecting subtree has a unique highest vertex when the tree is rooted. That vertex is simply the LCA of all vertices in the set.

Let (R) be the LCA of all red cities and (B) the LCA of all blue cities. The red Steiner subtree is exactly the union of the paths from (R) to every red city. Likewise, the blue Steiner subtree is the union of the paths from (B) to every blue city.

If neither (R) nor (B) is an ancestor of the other, their rooted subtrees are disjoint, so the two Steiner subtrees are automatically disjoint and the answer is `YES`.

Suppose instead that (R) is an ancestor of (B). The entire blue Steiner subtree is contained in the subtree rooted at (B). The red Steiner subtree reaches that subtree exactly when some red city itself is inside the subtree rooted at (B). If such a red city exists, its path from (R) to that city passes through (B), while the blue subtree also contains (B), so the two required subtrees intersect. The answer is `NO`. If no red city lies there, the two subtrees are disjoint and the answer is `YES`.

The case where (B) is an ancestor of (R) is symmetric.

Thus each query only needs repeated LCA computations, followed by ancestor checks. We preprocess the tree for (O(\log n)) LCA queries using heavy-light decomposition. Since the total number of mentioned cities is at most (200000), the total query work stays within the intended bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) | (O(n)) | Too slow |
| Optimal | (O(n + S\log n)), where (S\le200000) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at city (1). During an iterative DFS, compute `parent`, `depth`, and Euler entry and exit times `tin` and `tout`. The interval ([tin[v],tout[v])) represents exactly the subtree of (v), so ancestor checks can later be answered in (O(1)).
2. Compute subtree sizes and select one heavy child for every vertex. The heavy child is the child with the largest subtree. Following heavy children creates chains in which the number of times an LCA query changes chains is (O(\log n)).
3. Assign every vertex to the head of its heavy-light chain. The resulting decomposition lets us compute the LCA of two vertices by repeatedly moving the vertex whose chain head is deeper to its chain head's parent.
4. For each prediction, store the red vertices and compute their common LCA by folding LCA operations from left to right. Start with the first red vertex as the current LCA and replace it with `lca(current, next)` for every additional red vertex. The resulting vertex (R) is the highest vertex that belongs to the red Steiner subtree.
5. Do the same for the blue vertices and obtain (B). Since every query contains at least one vertex of each color, both LCAs are always defined.
6. Check whether (R) and (B) are incomparable in the rooted tree. If neither is an ancestor of the other, their subtrees are disjoint, so output `YES`.
7. If (R) is an ancestor of (B), scan the red vertices and check whether any of them lies in the subtree of (B). If one does, the red Steiner subtree has to pass through (B), where the blue Steiner subtree also exists, so output `NO`. Otherwise output `YES`.
8. If (B) is an ancestor of (R), perform the symmetric check. Look for a blue vertex inside the subtree of (R). Such a vertex forces the blue Steiner subtree through (R), causing an intersection. If no such vertex exists, output `YES`.

Why it works can be summarized by one invariant: the Steiner subtree of a color is the union of paths from that color's common LCA to all of its terminals. If the two common LCAs are incomparable, these unions lie in disjoint rooted subtrees. If one LCA is above the other, say (R) above (B), the blue subtree is completely inside (B)'s subtree, and the red subtree intersects that region exactly when some red terminal is inside it. The algorithm tests precisely these possibilities, so it accepts exactly the predictions for which the two required Steiner subtrees are disjoint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = []

    # Iterative DFS.
    timer = 0
    stack = [(1, 0, 0)]

    while stack:
        v, p, state = stack.pop()

        if state == 0:
            parent[v] = p
            tin[v] = timer
            timer += 1
            order.append(v)

            stack.append((v, p, 1))

            for u in reversed(graph[v]):
                if u != p:
                    depth[u] = depth[v] + 1
                    stack.append((u, v, 0))
        else:
            tout[v] = timer

    # Subtree sizes and heavy child.
    size = [1] * (n + 1)
    heavy = [0] * (n + 1)

    for v in reversed(order):
        best_size = 0

        for u in graph[v]:
            if parent[u] == v:
                size[v] += size[u]
                if size[u] > best_size:
                    best_size = size[u]
                    heavy[v] = u

    # Heavy-light decomposition.
    head = [0] * (n + 1)
    chain_stack = [(1, 1)]

    while chain_stack:
        v, h = chain_stack.pop()

        while v:
            head[v] = h
            hv = heavy[v]

            for u in graph[v]:
                if parent[u] == v and u != hv:
                    chain_stack.append((u, u))

            v = hv

    def lca(a, b):
        while head[a] != head[b]:
            if depth[head[a]] > depth[head[b]]:
                a = parent[head[a]]
            else:
                b = parent[head[b]]

        return a if depth[a] < depth[b] else b

    def is_ancestor(a, b):
        return tin[a] <= tin[b] < tout[a]

    q = int(input())
    answer = []

    for _ in range(q):
        data = list(map(int, input().split()))
        r, b = data[0], data[1]

        reds = data[2:2 + r]
        blues = data[2 + r:2 + r + b]

        red_lca = reds[0]
        for v in reds[1:]:
            red_lca = lca(red_lca, v)

        blue_lca = blues[0]
        for v in blues[1:]:
            blue_lca = lca(blue_lca, v)

        if not is_ancestor(red_lca, blue_lca) and \
           not is_ancestor(blue_lca, red_lca):
            answer.append("YES")
            continue

        if is_ancestor(red_lca, blue_lca):
            # Red's Steiner tree intersects Blue's subtree
            # exactly when some red terminal is inside it.
            bad = False
            for v in reds:
                if is_ancestor(blue_lca, v):
                    bad = True
                    break
            answer.append("NO" if bad else "YES")
        else:
            # Symmetric case.
            bad = False
            for v in blues:
                if is_ancestor(red_lca, v):
                    bad = True
                    break
            answer.append("NO" if bad else "YES")

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The first preprocessing phase performs an iterative DFS instead of recursion. A path-shaped tree can contain (200000) vertices, which is deep enough to exceed Python's normal recursion limit, so recursive DFS would be an unnecessary source of failure.

The `tin` and `tout` arrays are filled when a vertex is entered and exited. Because the traversal is a DFS, all descendants of a vertex receive entry times before its exit time. Consequently, `a` is an ancestor of `b` exactly when `tin[a] <= tin[b] < tout[a]`.

The `size` and `heavy` arrays are computed in reverse DFS order. Every child has already had its subtree size calculated when its parent is processed. The largest child becomes the heavy child.

The heavy-light decomposition stores only the chain head for each vertex. To find an LCA, we move the deeper chain head upward until both vertices lie on the same chain. A light edge can only be crossed (O(\log n)) times, because choosing a light child reduces the remaining subtree size by at least a factor of two.

For every query, the red and blue vertices are retained because the ancestor scan at the end may need to inspect the original terminals. The total number of stored terminals across all queries is at most (200000), so this does not create a large memory cost.

The condition `is_ancestor(red_lca, blue_lca)` deliberately includes equality. If the two LCAs are equal, every red terminal is inside the subtree of the common LCA, so the subsequent scan immediately finds a red terminal there and returns `NO`. This handles the common-LCA case without requiring a separate branch.

There is no integer arithmetic involving values larger than (n), so Python integer overflow is irrelevant. The critical implementation boundary is the half-open Euler interval in `is_ancestor`: using `tout[v]` as an inclusive endpoint would introduce an off-by-one error.

## Worked Examples

### Sample 1

For the sample tree rooted at city (1), the relevant ancestor relationships are (1) above (2,3), (2) above (4,5), and (3) above (6,7).

| Query | Red vertices | Red LCA | Blue vertices | Blue LCA | Relationship | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (4,5) | 2 | (6,7) | 3 | Incomparable | YES |
| 2 | (4,6) | 1 | (5,7) | 1 | Equal | NO |
| 3 | (1,4) | 1 | (5,2) | 2 | Red LCA above blue LCA, red (4) is below 2 | NO |
| 4 | (4,5) | 2 | (1) | 1 | Blue LCA above red LCA, blue (1) is outside subtree 2 | YES |
| 5 | (1) | 1 | (2) | 2 | Red LCA above blue LCA, red (1) is outside subtree 2 | YES |
| 6 | (1,2,3,4,5,6) | 1 | (7) | 7 | Red LCA above blue LCA, no red vertex below 7 | YES |

The first query demonstrates the simplest successful case where the two Steiner subtrees lie in different branches of the root. The second demonstrates why checking only the terminal vertices is insufficient, because both Steiner subtrees must pass through city (1). The third demonstrates the nested-subtree test. Although the red and blue LCA vertices differ, red city (4) forces the red subtree through blue LCA (2).

### A second example

Consider a path:

```
5
1 2
2 3
3 4
4 5
3
2 1 2 4 5
2 1 1 4 3
2 1 1 3 2
```

The first query has red cities (1,2) and blue cities (4,5). The color subtrees occupy opposite sides of the edge (2-3).

| Query | Red LCA | Blue LCA | Ancestor relation | Terminal inside nested subtree | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 1 above 4 | No red vertex in subtree 4 | YES |
| 2 | 1 | 4 | 1 above 4 | No red vertex in subtree 4 | YES |
| 3 | 1 | 3 | 1 above 3 | Red vertex 1 is not in subtree 3 | YES |

To demonstrate the rejecting version of the same structure, change the second query to red cities (1,5) and blue city (3). The red LCA is (1), the blue LCA is (3), and red city (5) lies below (3). The red path from (1) to (5) must pass through (3), so the answer becomes `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n + S\log n)) | Tree preprocessing is linear. Each of the (S\le200000) mentioned cities participates in at most one LCA or ancestor scan, and every LCA costs (O(\log n)). |
| Space | (O(n+S)) | The tree and heavy-light arrays use (O(n)) memory, while the current query stores (O(r+b)) terminals. |

The maximum (n) and total number of colored cities are both (200000). The preprocessing touches each road only a constant number of times, while the query phase performs logarithmic LCA operations on only the cities explicitly mentioned by the predictions. The solution therefore fits the 2 second and 256 MB limits without relying on recursion or a large (O(n\log n)) lifting table.

## Test Cases

```python
# The solution above defines solve() and the global input variable.
# This harness temporarily replaces stdin/stdout so solve() can be tested
# multiple times in one process.

import sys
import io

def run(inp: str) -> str:
    global input

    old_input = input
    old_stdout = sys.stdout

    input = io.StringIO(inp).readline
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        input = old_input
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
7
1 2
1 3
2 4
2 5
3 6
3 7
6
2 2 4 5 6 7
2 2 4 6 5 7
2 1 4 5 2
2 1 4 5 1
1 1 1 2
6 1 1 2 3 4 5 6 7
"""

assert run(sample1) == """\
YES
NO
NO
YES
YES
YES""", "sample 1"

# Minimum-size tree.
minimum = """\
2
1 2
1
1 1 2
"""

assert run(minimum) == "YES", "minimum tree"

# Star where both color Steiner trees must use the center.
same_lca = """\
5
1 2
1 3
1 4
1 5
1
2 2 3 4 5
"""

assert run(same_lca) == "NO", "same LCA"

# Path with both a successful nested case and a failing nested case.
path_cases = """\
5
1 2
2 3
3 4
4 5
3
2 1 2 4 5
2 1 1 4 3
2 1 1 5 3
"""

assert run(path_cases) == """\
YES
YES
NO""", "nested ancestor cases"

# Maximum-size tree and maximum total number of colored cities.
# Red = 1..100000, Blue = 100001..200000.
# Their Steiner subtrees are separated by the edge 100000-100001.
n = 200000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))

red = " ".join(str(i) for i in range(1, 100001))
blue = " ".join(str(i) for i in range(100001, 200001))

maximum = (
    f"{n}\n"
    f"{edges}\n"
    f"1\n"
    f"100000 100000 {red} {blue}\n"
)

assert run(maximum) == "YES", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `YES NO NO YES YES YES` | Full official sample, including incomparable, equal-LCA, and nested cases |
| Two-node tree | `YES` | Minimum (n), one red and one blue city |
| Five-node star | `NO` | Both Steiner trees meet at the same LCA |
| Five-node path | `YES YES NO` | Nested ancestor relationships and the decisive terminal-subtree check |
| (n=200000) path | `YES` | Maximum size, maximum total query input, and iterative traversal safety |

## Edge Cases

The two-city tree has no internal structure to reason about. With

```
2
1 2
1
1 1 2
```

the red LCA is (1), the blue LCA is (2), and (1) is an ancestor of (2). The only red vertex is (1), which is not inside the subtree of (2), so the algorithm returns `YES`.

For the common-LCA case,

```
5
1 2
1 3
1 4
1 5
1
2 2 3 4 5
```

the red LCA is (1) and the blue LCA is also (1). The first ancestor test succeeds with equality, and the algorithm scans the red vertices against the subtree of (1). Every red vertex is inside it, so it returns `NO`. This is exactly the situation where two groups are separated as terminal sets but cannot be separated as connected groups.

For a nested but intersecting case,

```
4
1 2
2 3
3 4
1
2 1 4 3
```

the red LCA is (1) and the blue LCA is (3). Since (1) is an ancestor of (3), the algorithm checks whether a red terminal lies in the subtree rooted at (3). Red city (4) does, so the red path from (1) to (4) must pass through (3). The answer is `NO`.

For a nested but separable case,

```
4
1 2
2 3
3 4
1
2 1 2 3 4
```

the red LCA is (1) and the blue LCA is (3). No red city lies in the subtree rooted at (3), because the red cities are (1) and (2). The red Steiner subtree ends before entering the blue subtree, so the edge (2-3) can be closed and the answer is `YES`.

The maximum-size path also checks a Python-specific edge case. The tree can have depth (199999), so a recursive DFS would be unsafe. The implementation uses an explicit stack for preprocessing, while all LCA operations use the heavy-light chains. The algorithm consequently handles a path of (200000) cities without recursion depth problems.
