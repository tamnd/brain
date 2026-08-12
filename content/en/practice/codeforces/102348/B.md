---
title: "CF 102348B - Interesting Vertices"
description: "We have a tree whose vertices are numbered from 1 to (n), and exactly (k) of those vertices are colored. For an uncolored vertex (x), imagine cutting (x) away from the tree. Every neighbor of (x) becomes the root of one connected component."
date: "2026-08-13T00:50:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "B"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 114
verified: true
draft: false
---

[CF 102348B - Interesting Vertices](https://codeforces.com/problemset/problem/102348/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree whose vertices are numbered from 1 to (n), and exactly (k) of those vertices are colored. For an uncolored vertex (x), imagine cutting (x) away from the tree. Every neighbor of (x) becomes the root of one connected component. The vertex (x) is interesting precisely when every one of those components contains at least one colored vertex.

The task is to find every uncolored vertex satisfying that condition and print their indices in increasing order.

The central difficulty is that the definition temporarily roots the tree at every possible (x). A direct implementation would seem to require a separate tree traversal for every uncolored vertex. With (n) as large as (2\cdot10^5), that is too expensive for a two-second limit. An (O(n^2)) algorithm can perform roughly (4\cdot10^{10}) vertex visits in the worst case, far beyond what is practical. We need to extract information about all possible roots from a single traversal.

There are several edge cases that can make a seemingly reasonable implementation wrong. First, an uncolored leaf is always interesting, because after removing the leaf there is only one remaining component, and that component contains all (k) colored vertices. For example,

```
2 1
1
1 2
```

has output

```
1
2
```

A solution that requires a vertex to have at least two colored directions would incorrectly reject vertex 2.

A second edge case occurs when the candidate itself is colored. Such a vertex may have colored vertices in every direction, but it is not eligible because only uncolored vertices can be answers. For example,

```
3 1
2
1 2
2 3
```

has output

```
2
1 3
```

The colored vertex 2 must be excluded even though both components obtained by removing it contain no colored vertices, which already makes it fail here. More generally, the implementation should explicitly exclude colored vertices rather than relying on the directional test to do so.

A third edge case is a single colored vertex. If (k=1), an uncolored vertex with degree at least two cannot be interesting, because only one of its incident components can contain the unique colored vertex. Every uncolored leaf is interesting. For example,

```
5 1
3
1 2
2 3
3 4
4 5
```

has output

```
2
1 5
```

A careless implementation that only checks whether the whole subtree contains a color can accidentally accept internal vertices, even though one of their directions is colorless.

Finally, the colored vertices are guaranteed to be distinct, so a test case where all colored values are equal is invalid under the problem constraints. The closest meaningful boundary case is (k=1), which is covered separately.

## Approaches

The brute-force solution starts by choosing every uncolored vertex (x) as a root. Once the tree is rooted at (x), we can traverse it and determine, for every child of (x), whether its subtree contains a colored vertex. If every child subtree contains one, we add (x) to the answer.

This is correct because those child subtrees are exactly the connected components produced when (x) is removed. The problem is the amount of repeated work. In the worst case there can be (n-1) uncolored candidates, and checking one candidate requires (O(n)) work. With (k=1), for example, this can reach

[
(n-1)(n-1)=O(n^2),
]

which is about (4\cdot10^{10}) operations when (n=2\cdot10^5).

The key observation is that we do not actually need to root the tree at every candidate. Fix an arbitrary root, say vertex 1. For every vertex (v), compute the number of colored vertices in its ordinary rooted subtree.

Consider an edge between a parent (u) and a child (v). Removing this edge splits the tree into exactly two components. One is the subtree of (v), containing `sub[v]` colored vertices. The other contains all remaining colored vertices, so it contains

[
k-\text{sub}[v]
]

colored vertices.

That completely determines whether the edge is a bad direction for either endpoint. If `sub[v] == 0`, the component on the (v) side contains no colored vertex, so (u) cannot be interesting. If `sub[v] == k`, every colored vertex is inside (v)'s subtree, so the component on the (u) side contains no colored vertex, and (v) cannot be interesting.

Every other value of `sub[v]` means both sides of the edge contain at least one colored vertex, so this edge is safe for both endpoints.

The brute-force works because it checks each component around a candidate explicitly, but fails when the same components are recomputed for many candidates. The observation that every edge has only two possible sides lets us classify all directions at once. After computing subtree color counts, every edge contributes at most one failure to one endpoint, so the entire tree can be processed in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the tree and mark every colored vertex. We keep a boolean array because the final answer must exclude colored vertices even if their structural properties would otherwise qualify them.
2. Root the tree arbitrarily at vertex 1. Build a `parent` array and an `order` array using an iterative DFS. The `order` array stores vertices in parent-before-child order, which will later let us process them in reverse without recursion.
3. Initialize `sub[v]` to 1 for every colored vertex and to 0 for every uncolored vertex. Thus `sub[v]` will eventually represent the number of colored vertices in the rooted subtree of (v).
4. Process the vertices in reverse DFS order. For every non-root vertex (v), add `sub[v]` to `sub[parent[v]]`. By the time a vertex is processed, all of its children have already contributed their colored counts.
5. Create `bad[v]`, initially zero. For every non-root vertex (v), consider the edge from its parent (p) to (v). If `sub[v] == 0`, the entire (v)-side of that edge is colorless, so this edge is a bad direction for (p), and we increment `bad[p]`.
6. If `sub[v] == k`, all colored vertices lie inside the (v)-side. Consequently, the parent-side component is colorless, so the same edge is a bad direction for (v), and we increment `bad[v]`.
7. Finally, scan every vertex. A vertex is interesting exactly when it is uncolored and `bad[v] == 0`. Sort these indices before printing them. Sorting takes (O(n\log n)), but because the vertices are already numbered from 1 through (n), we can instead scan them in numerical order and obtain sorted output directly, preserving the overall (O(n)) complexity.

### Why it works

For every edge (p-v), the two components formed by removing that edge contain exactly `sub[v]` and (k-\text{sub[v]}) colored vertices. The edge is bad for (p) exactly when `sub[v] == 0`, and it is bad for (v) exactly when `sub[v] == k`. Thus `bad[x]` counts precisely the incident components of (x) that contain no colored vertex.

For an uncolored vertex (x), the original definition says that every component around (x) must contain a colored vertex. This is equivalent to saying that none of its incident edges is bad, which is exactly `bad[x] == 0`. Since colored vertices are explicitly excluded, every reported vertex satisfies the definition, and every interesting vertex is reported.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    colored = [False] * (n + 1)
    for x in map(int, input().split()):
        colored[x] = True

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at vertex 1.
    parent = [0] * (n + 1)
    order = [1]
    parent[1] = -1

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # sub[v] = number of colored vertices in v's rooted subtree.
    sub = [0] * (n + 1)
    for v in range(1, n + 1):
        if colored[v]:
            sub[v] = 1

    for v in reversed(order[1:]):
        sub[parent[v]] += sub[v]

    # bad[v] = number of incident components of v containing no color.
    bad = [0] * (n + 1)

    for v in order[1:]:
        p = parent[v]

        if sub[v] == 0:
            bad[p] += 1

        if sub[v] == k:
            bad[v] += 1

    answer = []
    for v in range(1, n + 1):
        if not colored[v] and bad[v] == 0:
            answer.append(v)

    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The first part stores the colored vertices in `colored`. Using a boolean array gives constant-time membership checks and avoids any need to search through the list of colored indices later.

The adjacency list represents the tree with (O(n)) memory. Since a tree has exactly (n-1) edges, the total number of entries across all adjacency lists is (2(n-1)).

The DFS is deliberately iterative. A recursive DFS on a path of (2\cdot10^5) vertices would exceed Python's normal recursion depth and could fail even though the algorithm itself is correct. The `order` array gives us a convenient postorder simply by iterating through it backwards.

The initialization of `sub` puts one unit at each colored vertex. Processing `order` backwards then accumulates those units toward the root, so `sub[v]` becomes the number of colored vertices in the entire subtree of (v).

The edge classification is the most important implementation detail. For an edge from `p` to `v`, `sub[v] == 0` means the child-side component has no colors, so only `p` is disqualified by that edge. Conversely, `sub[v] == k` means all colors are on the child side, so only `v` is disqualified. These two cases must not be swapped.

No special handling is needed for the root. Every edge incident to the root appears as a parent-child edge in the rooted tree, and its child-side count completely determines whether that edge is bad for the root.

The final loop goes from 1 to (n), so the output is already sorted. There is no need for a separate sort and the running time remains linear.

## Worked Examples

### Sample 1

The tree is

```
1 - 2 - 3
    |
    4
```

Vertex 3 is colored. We root the tree at vertex 1.

| Vertex | Parent | Colored in subtree | Bad directions |
| --- | --- | --- | --- |
| 1 | none | 1 | 0 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 1 | 1 |
| 4 | 2 | 0 | 0 |

For edge (1-2), the subtree of 2 contains the only colored vertex, so `sub[2] == k`. This makes the parent-side component empty of colors and marks vertex 2 as bad.

For edge (2-3), the child side contains the colored vertex, so vertex 3 has no bad direction from this edge. For edge (2-4), the subtree of 4 contains no colored vertex, so vertex 2 gets another bad direction.

Vertices 1 and 4 are uncolored and have zero bad directions. Vertex 3 is colored and is excluded, while vertex 2 has bad directions. The output is therefore `1 4`.

This example shows why a leaf can be interesting even when there is only one colored vertex. Removing leaf 4 leaves one component containing vertex 3.

### Sample 2

Rooting at vertex 1 gives the following parent-child structure:

```
        1
     / /|\ \
    5 6 2 8
   / \   |
  4   3  7
```

Vertices 6, 5, and 7 are colored.

| Vertex | Parent | Colored in subtree | Bad directions |
| --- | --- | --- | --- |
| 1 | none | 3 | 1 |
| 2 | 1 | 1 | 0 |
| 3 | 5 | 0 | 0 |
| 4 | 5 | 0 | 0 |
| 5 | 1 | 1 | 2 |
| 6 | 1 | 1 | 0 |
| 7 | 2 | 1 | 0 |
| 8 | 1 | 0 | 0 |

The subtree of vertex 8 has zero colored vertices, so edge (1-8) makes vertex 1 fail. The subtrees of 3 and 4 are also colorless, so both edges make vertex 5 fail.

For vertex 2, its child subtree containing 7 has one colored vertex, while the rest of the tree contains the other two colored vertices. Both directions therefore contain a color, making 2 interesting.

Vertices 3, 4, and 8 are leaves, so their only remaining component contains all colored vertices. They are also interesting. Vertex 5 is rejected because its two leaf directions toward 3 and 4 contain no colors. The colored vertices 6 and 7 are excluded.

The resulting answer is `2 3 4 8`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Building the tree, rooting it, computing subtree counts, classifying edges, and scanning the vertices each take linear time. |
| Space | (O(n)) | The adjacency list, parent array, traversal order, subtree counts, bad counts, and color flags all use linear memory. |

The largest tree has (2\cdot10^5) vertices and only (2\cdot10^5-1) edges. The algorithm performs a constant amount of work per vertex and per edge, so it comfortably fits the two-second limit. The iterative traversal also avoids recursion-depth failures on highly unbalanced trees such as a path.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py`, with the `solve()` function shown above.

```python
import sys
import io
from contextlib import redirect_stdout

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()

    try:
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue().strip()

# Provided sample 1
assert run("""\
4 1
3
1 2
2 3
2 4
""") == """\
2
1 4
""", "sample 1"

# Provided sample 2
assert run("""\
8 3
6 5 7
1 5
5 4
5 3
1 6
2 7
1 2
1 8
""") == """\
4
2 3 4 8
""", "sample 2"

# Minimum-size tree. The only uncolored vertex is a leaf.
assert run("""\
2 1
1
1 2
""") == """\
1
2
""", "minimum size"

# One colored vertex on a path. Only the two uncolored leaves are interesting.
assert run("""\
5 1
3
1 2
2 3
3 4
4 5
""") == """\
2
1 5
""", "single colored vertex"

# Two colored vertices split the path. Vertex 3 sees one color in each direction.
assert run("""\
5 2
2 4
1 2
2 3
3 4
4 5
""") == """\
3
1 3 5
""", "two colored directions"

# Boundary case with many colored vertices. The uncolored center has a
# colored vertex in every incident component.
assert run("""\
4 3
2 3 4
1 2
1 3
1 4
""") == """\
1
1
""", "every branch contains a color")

# Maximum-size stress case: a star with all leaves colored.
n = 200000
colored = " ".join(map(str, range(2, n + 1)))
edges = "\n".join(f"1 {v}" for v in range(2, n + 1))
maximum_case = f"{n} {n - 1}\n{colored}\n{edges}\n"

assert run(maximum_case) == """\
1
1
""", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=2,\ k=1), edge (1-2), color 1 | `1 / 2` | Minimum size and the fact that an uncolored leaf is interesting |
| Path of 5 vertices with only vertex 3 colored | `2 / 1 5` | The (k=1) case and rejection of internal vertices |
| Path of 5 vertices with colors 2 and 4 | `3 / 1 3 5` | A vertex whose two different directions contain colors |
| Star with center 1 and colored leaves 2, 3, 4 | `1 / 1` | Every incident component of the center contains a colored vertex |
| Star with 200000 vertices and all leaves colored | `1 / 1` | Maximum input size, large (k), and linear-time behavior |

The maximum-size test intentionally uses a generated input rather than embedding hundreds of thousands of lines directly into the editorial. It still constructs exactly the maximum permitted tree and runs the same assertion against the actual solution.

## Edge Cases

### A single colored vertex

Consider

```
5 1
3
1 2
2 3
3 4
4 5
```

After rooting at 1, the subtree counts are `1, 1, 1, 0, 0` from vertices 1 through 5 except for the appropriate accumulation around vertex 3. More directly, for any internal uncolored vertex there are at least two incident components, but only one can contain vertex 3. Thus every internal vertex has a bad direction. Vertices 1 and 5 are leaves, so after removing either one there is a single component containing vertex 3. The algorithm gives `bad[1] = 0` and `bad[5] = 0`, while internal candidates receive at least one bad count, producing `1 5`.

### An uncolored leaf

Consider

```
2 1
1
1 2
```

Rooting at 1 gives `sub[2] = 0`, because vertex 2 is uncolored. The condition `sub[2] == 0` increments `bad[1]`, not `bad[2]`. Vertex 2 has no child edges and therefore receives no bad direction. Since it is uncolored, it is accepted. This assignment of the bad edge to the correct endpoint is an easy place to introduce an off-by-one conceptual error.

### A colored vertex must never be reported

Consider

```
3 1
2
1 2
2 3
```

The colored array marks vertex 2. The algorithm may compute structural information for it just like every other vertex, but the final condition explicitly requires `not colored[v]`. Thus only vertices 1 and 3 can enter the answer, and both are leaves. The output is

```
2
1 3
```

This explicit exclusion is preferable to trying to prove that every colored vertex will automatically receive a bad count, because the definition itself is the cleanest authority on eligibility.

### A vertex with several colorless branches

In the first sample,

```
4 1
3
1 2
2 3
2 4
```

vertex 2 has three incident directions. The direction toward vertex 3 contains the only color, while the directions toward vertices 1 and 4 contain none. The subtree rooted at 4 has `sub[4] = 0`, which increments `bad[2]`. The edge toward the parent 1 has all colors on the 2-side, so `sub[2] == k` increments `bad[2]` again. Vertex 2 consequently has two bad directions and is rejected.

The same edge-based accounting handles this case without separately reasoning about the degree of the candidate. Every incident component is represented by exactly one directed side of an edge, so checking whether each such side contains a color is reduced to the two subtree-count boundary cases `0` and `k`.
