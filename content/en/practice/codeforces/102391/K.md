---
title: "CF 102391K - Wind of Change"
description: "We have two weighted trees on the same set of vertices, with vertex labels (1) through (N). For two labels (i) and (j), their distance is not measured in either tree alone."
date: "2026-08-10T21:11:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "K"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 337
verified: true
draft: false
---

[CF 102391K - Wind of Change](https://codeforces.com/problemset/problem/102391/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two weighted trees on the same set of vertices, with vertex labels (1) through (N). For two labels (i) and (j), their distance is not measured in either tree alone. Instead, we add the path length between them in the first tree to the path length between them in the second tree. For every vertex (i), we need the smallest such sum over every other vertex (j).

The two trees can have completely different shapes and edge weights. A vertex that is close to (i) in the first tree may be very far away in the second tree, so independently finding a nearest vertex in either tree does not help. The answer is a nearest-neighbor query in the product metric of the two trees.

The largest instance has (250,000) vertices and each tree has (249,999) edges. A quadratic algorithm would inspect about (N(N-1)/2), roughly (31) billion, vertex pairs in the worst case. That is far beyond the practical range of a 12-second contest solution. The official problem limits are 12 seconds and 1024 MiB, so an (O(N\log^2N)) method is appropriate.

There are also two numerical details that matter. An individual tree distance can be as large as roughly (2.5\cdot10^{14}), so the combined distance needs 64-bit arithmetic in C++. Python integers handle this automatically. Also, (j=i) must never be used. Since its distance is zero, accidentally allowing it would immediately make every answer zero.

Consider the smallest possible tree:

```
2
1 2 1000000000
1 2 1000000000
```

The only possible other vertex is the other endpoint, so the correct output is

```
2000000000
2000000000
```

An implementation that includes the queried vertex itself would incorrectly print zero.

A second useful edge case is when both trees have the same simple shape and all weights are equal:

```
3
1 2 1
2 3 1
1 2 1
2 3 1
```

Every vertex has another vertex at combined distance (2), so the answer is

```
2
2
2
```

This catches implementations that confuse distance in one tree with the required sum of both distances.

Finally, the trees need not have similar shapes at all. For example,

```
3
1 2 1
2 3 100
1 2 100
2 3 1
```

has combined distance (101) between either adjacent pair and (202) between vertices (1) and (3). The correct output is

```
101
101
101
```

This is a useful check against accidentally reusing the geometry of the first tree for the second one.

## Approaches

The direct solution is straightforward. Compute the distance between every pair (i,j) in both trees and minimize the sum for every (i). Since a tree has unique paths, one can root each tree and obtain all distances from one source in linear time, but doing that from every source still costs (O(N^2)). Equivalently, explicitly considering every pair performs (N(N-1)/2) comparisons, which reaches about (31.25) billion pairs when (N=250,000).

The brute force is correct because it directly evaluates the quantity being minimized. Its failure is entirely computational. We need to exploit the fact that distances in a tree can be decomposed around a separator.

The useful separator is a centroid decomposition. Removing a centroid divides a tree into components of size at most half of the current component. Repeating this produces a centroid tree of logarithmic height. This standard balancing property is exactly what lets us replace an arbitrary pair of vertices by a pair of centroid ancestors.

Build a centroid decomposition independently for (T_1) and (T_2). For vertices (i) and (j), let (L_1) be their lowest common ancestor in the centroid tree of (T_1), and let (L_2) be their lowest common ancestor in the centroid tree of (T_2). By the way centroid decomposition separates components, the original path between (i) and (j) in (T_1) passes through (L_1), and similarly the path in (T_2) passes through (L_2). Hence

[d_1(L_1,i)+d_2(L_2,i)]
+
[d_1(L_1,j)+d_2(L_2,j)].
]

This is the key algebraic transformation. The contribution of (i) and (j) separates completely once (L_1,L_2) are fixed.

There is still an awkward condition: (L_1) and (L_2) must be the exact two centroid-tree LCAs. We can remove that condition. For a fixed (i,L_1,L_2), consider every vertex (j) that is simply a descendant of (L_1) in the first centroid tree and a descendant of (L_2) in the second centroid tree. This set is larger than the set having exactly those two LCAs.

For any such (j),

[
d_1(L_1,i)+d_1(L_1,j)\ge d_1(i,j)
]

and

[
d_2(L_2,i)+d_2(L_2,j)\ge d_2(i,j)
]

by the triangle inequality. Thus the relaxed candidate can never be smaller than the real distance. On the other hand, the true nearest vertex (j) has some exact pair (L_1,L_2), and that pair is included among the relaxed cases. Consequently, taking the minimum over all relaxed cases still gives exactly the true answer.

For a fixed centroid (L_2) in the second decomposition, we can visit every vertex in its centroid subtree. For each such vertex (v), we enumerate all centroid ancestors (L_1) of (v) in the first decomposition. For a fixed (L_1), we insert

[
d_1(L_1,v)+d_2(L_2,v)
]

into a two-element minimum structure. We only need the smallest and second-smallest values, because when querying for vertex (v), the smallest value may have come from (v) itself and must then be skipped.

Every vertex has only (O(\log N)) centroid ancestors in either decomposition. The nested enumeration consequently contains (O(N\log^2N)) combinations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(N)) | Too slow |
| Optimal | (O(N\log^2N)) | (O(N\log N)) | Accepted |

## Algorithm Walkthrough

1. Build the centroid decomposition of the first tree. Whenever a centroid (c) is selected, traverse its current component and record (d_1(c,v)) for every vertex (v) in that component. Since (c) becomes an ancestor of every such vertex in the centroid tree, this gives every vertex a list of its centroid ancestors together with their original-tree distances.
2. Build the centroid decomposition of the second tree as well, but we do not need to store its distance lists. During the later processing, whenever a centroid (c) is selected, we can traverse its current component and directly obtain (d_2(c,v)) for every descendant (v).
3. Initialize every answer to infinity. When processing a centroid (c=L_2) of the second tree, its current component is exactly the subtree of (c) in the second centroid tree. Thus every vertex visited in this component is a valid candidate for the relaxed condition (L_2) being an ancestor.
4. For every visited vertex (v), iterate through its stored centroid ancestors ((L_1,d_1(L_1,v))) from the first tree. For each (L_1), calculate
[
x=d_1(L_1,v)+d_2(c,v).
]
Maintain the two smallest values of (x) for every (L_1), together with the vertex producing each value.
5. After all vertices in the current second-tree component have been inserted, iterate through them again. For every vertex (v) and every first-tree ancestor (L_1), retrieve the smallest stored value belonging to a vertex other than (v). If the smallest value was produced by (v), use the second-smallest value instead.
6. Add the value for (v) itself:
[
d_1(L_1,v)+d_2(c,v)+
\min_{j\ne v}
[d_1(L_1,j)+d_2(c,j)].
]
Update the global answer of (v) with this candidate. This is exactly the relaxed expression derived above.
7. Mark the current second-tree centroid as removed and continue independently with every remaining component. Because every component has at most half the previous size, every vertex participates in only (O(\log N)) centroid levels.
8. Print the resulting minimum for every vertex. Self-pairs are excluded by selecting the second minimum whenever the first minimum belongs to the queried vertex.

### Why it works

Fix two vertices (i\ne j), and let (L_1,L_2) be their lowest common ancestors in the two centroid decompositions. Because those centroids separate (i) and (j), the original tree paths pass through the respective centroids. Hence their true combined distance equals

[
d_1(L_1,i)+d_2(L_2,i)+d_1(L_1,j)+d_2(L_2,j).
]

The algorithm considers this exact pair of ancestors because both are ancestors of (i), and (j) lies in both corresponding centroid subtrees. Thus the true optimum is among the candidates considered.

Every relaxed candidate has the form

[
d_1(L_1,i)+d_1(L_1,j)+d_2(L_2,i)+d_2(L_2,j).
]

By the triangle inequality in each tree, this is at least (d_1(i,j)+d_2(i,j)). So the algorithm can never produce a value below the real optimum. Since the real optimal pair is considered as well, the minimum produced by the algorithm is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def get_component_centroid(adj, root, removed, parent, size):
    nodes = []
    stack = [root]
    parent[root] = -1

    while stack:
        u = stack.pop()
        nodes.append(u)
        pu = parent[u]

        for v, _ in adj[u]:
            if removed[v] or v == pu:
                continue
            parent[v] = u
            stack.append(v)

    for u in reversed(nodes):
        s = 1
        for v, _ in adj[u]:
            if removed[v]:
                continue
            if parent[v] == u:
                s += size[v]
        size[u] = s

    total = len(nodes)
    centroid = nodes[0]
    best_balance = total + 1

    for u in nodes:
        largest = total - size[u]

        for v, _ in adj[u]:
            if removed[v]:
                continue
            if parent[v] == u and size[v] > largest:
                largest = size[v]

        if largest < best_balance:
            best_balance = largest
            centroid = u

    return nodes, centroid

def build_ancestors(adj, n):
    removed = bytearray(n)
    parent = [-1] * n
    size = [0] * n
    ancestors = [[] for _ in range(n)]

    tasks = [0]

    while tasks:
        root = tasks.pop()

        _, centroid = get_component_centroid(
            adj, root, removed, parent, size
        )

        stack = [(centroid, -1, 0)]

        while stack:
            u, p, d = stack.pop()
            ancestors[u].append((centroid, d))

            for v, w in adj[u]:
                if removed[v] or v == p:
                    continue
                stack.append((v, u, d + w))

        removed[centroid] = 1

        for v, _ in adj[centroid]:
            if not removed[v]:
                tasks.append(v)

    return ancestors

def solve():
    input = sys.stdin.readline
    n = int(input())

    adj1 = [[] for _ in range(n)]
    adj2 = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        adj1[u].append((v, w))
        adj1[v].append((u, w))

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        adj2[u].append((v, w))
        adj2[v].append((u, w))

    ancestors = build_ancestors(adj1, n)

    removed = bytearray(n)
    parent = [-1] * n
    size = [0] * n

    best1 = [INF] * n
    best2 = [INF] * n
    id1 = [-1] * n
    id2 = [-1] * n
    seen = [0] * n
    token = 0

    ans = [INF] * n
    tasks = [0]

    while tasks:
        root = tasks.pop()

        _, centroid = get_component_centroid(
            adj2, root, removed, parent, size
        )

        nodes_dist = []
        stack = [(centroid, -1, 0)]

        while stack:
            u, p, d = stack.pop()
            nodes_dist.append((u, d))

            for v, w in adj2[u]:
                if removed[v] or v == p:
                    continue
                stack.append((v, u, d + w))

        token += 1

        for v, d2 in nodes_dist:
            for a, d1 in ancestors[v]:
                if seen[a] != token:
                    seen[a] = token
                    best1[a] = INF
                    best2[a] = INF
                    id1[a] = -1
                    id2[a] = -1

                value = d1 + d2

                if value < best1[a]:
                    best2[a] = best1[a]
                    id2[a] = id1[a]
                    best1[a] = value
                    id1[a] = v
                elif value < best2[a]:
                    best2[a] = value
                    id2[a] = v

        for v, d2 in nodes_dist:
            for a, d1 in ancestors[v]:
                if id1[a] == v:
                    other = best2[a]
                else:
                    other = best1[a]

                if other < INF:
                    candidate = d1 + d2 + other
                    if candidate < ans[v]:
                        ans[v] = candidate

        removed[centroid] = 1

        for v, _ in adj2[centroid]:
            if not removed[v]:
                tasks.append(v)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The first helper, `get_component_centroid`, performs an entirely iterative traversal. This avoids Python recursion depth problems on a path containing (250,000) vertices. It first records the current component and parent relation, then computes subtree sizes in reverse order, and finally selects a vertex whose largest remaining piece is as small as possible.

`build_ancestors` constructs the first centroid decomposition. The original weighted edges are never changed. For every centroid, the traversal records the actual weighted distance from that centroid to every vertex in its current component. This is exactly the information required later, so there is no need to explicitly construct the centroid tree itself.

The second decomposition is processed after the first one has been stored. For each second-tree centroid, `nodes_dist` contains every vertex in that centroid subtree and its distance to the centroid. Each such vertex already knows all its first-tree centroid ancestors, so iterating the two lists enumerates every required ((L_1,L_2,v)) combination.

The four arrays `best1`, `best2`, `id1`, and `id2` represent the two smallest values for each (L_1). The `seen` array gives lazy clearing. Instead of resetting all (N) entries every time a centroid is processed, only the (L_1) values actually encountered in that component are initialized.

The strict exclusion of the current vertex is handled by the stored vertex IDs. If `id1[a] == v`, the smallest candidate is the self-pair and `best2[a]` must be used. If the first candidate belongs to another vertex, it is immediately valid.

All arithmetic is performed using Python integers. In C++, the corresponding implementation needs `long long`, since the sum of the two tree distances can exceed (2^{31}-1).

## Worked Examples

### Sample 1

For the first tree, vertex (4) is a natural top-level centroid. One of its descendant centroid relationships is (2), which separates vertices (1) and (2). In the second tree, vertex (1) is the top-level centroid.

For the pair (L_1=2,L_2=1), the relevant vertices are (1) and (2). Their values before excluding the query vertex are

[
d_1(2,1)+d_2(1,1)=10,
]

and

[
d_1(2,2)+d_2(1,2)=15.
]

The two smallest values are thus (10) from vertex (1) and (15) from vertex (2).

| Query vertex | (L_1) | (L_2) | Own value | Other minimum | Candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 10 | 15 | 25 |
| 2 | 2 | 1 | 15 | 10 | 25 |

For vertex (1), the candidate uses vertex (2), giving (10+15=25). For vertex (2), the same pair is used in the opposite direction, giving (15+10=25).

The other centroid combinations produce the remaining answers.

| Vertex | Best witness | First-tree distance | Second-tree distance | Answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 10 | 15 | 25 |
| 2 | 1 | 10 | 15 | 25 |
| 3 | 1 | 60 | 25 | 85 |
| 4 | 1 | 30 | 35 | 65 |
| 5 | 1 | 80 | 25 | 105 |

This demonstrates the self-exclusion rule as well as the central decomposition identity. The final output is

```
25
25
85
65
105
```

### Sample 2

The second sample is useful because the two trees have very different structures. The optimal pair for each vertex is not simply an adjacent pair in one fixed tree.

The final minimizing witnesses can be checked directly from the two original trees.

| Query vertex | Witness | (d_1(i,j)) | (d_2(i,j)) | Sum |
| --- | --- | --- | --- | --- |
| 1 | 8 | 8278 | 9806 | 18084 |
| 2 | 6 | 410 | 8959 | 9369 |
| 3 | 8 | 9078 | 504 | 9582 |
| 4 | 7 | 15446 | 7984 | 23430 |
| 5 | 2 | 21833 | 4861 | 26694 |
| 6 | 2 | 410 | 8959 | 9369 |
| 7 | 4 | 15446 | 7984 | 23430 |
| 8 | 3 | 9078 | 504 | 9582 |
| 9 | 3 | 22225 | 763 | 22988 |

For example, vertex (3) is closest to vertex (8). The first-tree path from (3) to (8) costs (4268+4810=9078), while their second-tree edge costs (504), giving (9582). The decomposition will encounter the centroid-ancestor pair corresponding to these paths, and the stored minimum for that pair recovers exactly this value.

The official sample has the output shown below.

```
18084
9369
9582
23430
26694
9369
23430
9582
22988
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log^2N)) | Each vertex has (O(\log N)) ancestors in each centroid decomposition, and every second-tree centroid level processes the corresponding ancestor combinations. |
| Space | (O(N\log N)) | The first decomposition stores one distance for every vertex and every first-tree centroid ancestor. The two original trees and working arrays require (O(N)) additional space. |

A centroid decomposition has logarithmic height because every removal leaves components of size at most half the current component. Each vertex consequently has only (O(\log N)) stored ancestors. The nested first-tree and second-tree ancestor enumeration gives the (O(N\log^2N)) running time described by the intended solution.

For (N=250,000), this is the asymptotic range required by the problem's 12-second and 1024 MiB limits. The Python implementation uses iterative traversals because a recursive DFS on a long tree would otherwise exceed Python's recursion limit.

## Test Cases

The following test harness assumes the solution above is saved as `solution.py`. The helper replaces standard input and output, then calls the actual `solve()` function.

```python
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """\
5
1 2 10
2 4 20
3 4 30
4 5 50
1 2 15
1 3 25
1 4 35
1 5 25
"""

assert run(sample1) == """\
25
25
85
65
105
""", "sample 1"

sample2 = """\
9
5 7 6577
4 5 8869
5 9 9088
2 1 124
6 2 410
2 8 8154
4 8 4810
3 4 4268
3 9 763
6 2 8959
7 4 7984
3 8 504
8 6 9085
5 2 4861
1 9 8539
1 7 7834
"""

assert run(sample2) == """\
18084
9369
9582
23430
26694
9369
23430
9582
22988
""", "sample 2"

case_minimum = """\
2
1 2 1000000000
1 2 1000000000
"""

assert run(case_minimum) == """\
2000000000
2000000000
""", "minimum size and maximum edge weight"

case_equal = """\
4
1 2 1
1 3 1
1 4 1
1 2 1
1 3 1
1 4 1
"""

assert run(case_equal) == """\
2
2
2
2
""", "all equal weights"

case_different_shapes = """\
3
1 2 1
2 3 100
1 2 100
2 3 1
"""

assert run(case_different_shapes) == """\
101
101
101
""", "different tree weights"

def make_max_case():
    n = 250000
    lines = [str(n)]

    for i in range(1, n):
        lines.append(f"{i} {i + 1} 1")

    for i in range(1, n):
        lines.append(f"{i} {i + 1} 1")

    return "\n".join(lines) + "\n"

maximum_case = make_max_case()
assert run(maximum_case) == "2\n" * 250000, "maximum size stress case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `25 25 85 65 105` | Basic centroid-pair processing and self-exclusion |
| Sample 2 | `18084 9369 9582 23430 26694 9369 23430 9582 22988` | Different tree structures and weighted paths |
| (N=2), weights (10^9) | `2000000000 2000000000` | Minimum size, large integer arithmetic, and mandatory exclusion of self |
| (N=4), identical unit stars | `2 2 2 2` | Equal weights and many tied nearest candidates |
| (N=3), opposite weights | `101 101 101` | The two tree metrics must both contribute |
| (N=250000), identical unit paths | `2` repeated 250000 times | Maximum input size and iterative traversal safety |

## Edge Cases

The (N=2) case has only one valid pair. For

```
2
1 2 1000000000
1 2 1000000000
```

the first centroid decomposition stores the two vertices at distances (0) and (10^9), and the second decomposition does the same. When processing either vertex, the first minimum belongs to the vertex itself, so the algorithm selects the second minimum. The resulting value is (10^9+10^9=2,000,000,000).

The self-pair issue is particularly visible when a centroid subtree contains only one vertex for a particular ancestor pair. The two-minimum structure then has only one finite value. The implementation checks for `INF` before updating the answer, so a nonexistent second vertex cannot become a fake candidate.

Equal distances are also handled correctly. In the four-vertex unit star, several other vertices have exactly the same combined distance. The two-minimum structure stores vertex IDs in addition to values, so tied values from distinct vertices remain distinct candidates. For every vertex, at least one other vertex has value (2), giving four answers equal to (2).

Large edge weights do not affect the decomposition itself. Centroid selection depends only on component sizes, while the actual edge weights are carried unchanged when computing distances from a centroid. This separation is useful because the structural decomposition and the metric calculation do not interfere with each other.

A path of (250,000) vertices is the worst shape for recursive DFS in Python, because its ordinary depth is (250,000). The implementation uses explicit stacks for component traversal, centroid distance traversal, and decomposition tasks, so its Python call stack remains constant-depth even on this adversarial shape.

The two trees may also have completely unrelated topologies. The algorithm never assumes that a centroid in one tree corresponds to a centroid with the same label in the other. It only uses the labels to identify the same point across the two trees, while (L_1) and (L_2) are selected independently. This independence is what makes the method work for arbitrary pairs of weighted trees.
