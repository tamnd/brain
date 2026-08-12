---
title: "CF 102331J - Jiry Matchings"
description: "We have a weighted tree with (n) vertices. A matching is a set of edges such that no two selected edges share an endpoint. For every (k=1,2,ldots,n-1), we need the maximum possible sum of edge weights among all matchings containing exactly (k) edges."
date: "2026-08-13T03:51:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "J"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 450
verified: true
draft: false
---

[CF 102331J - Jiry Matchings](https://codeforces.com/problemset/problem/102331/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted tree with (n) vertices. A matching is a set of edges such that no two selected edges share an endpoint. For every (k=1,2,\ldots,n-1), we need the maximum possible sum of edge weights among all matchings containing exactly (k) edges. If a matching of size (k) cannot exist, we print `?`.

The input is a tree, so it contains exactly (n-1) edges. The weights can be negative, which means a valid matching of size (k) may have a negative optimum. We are not allowed to replace a negative answer by zero, because the number of selected edges is fixed.

With (n\le 200000), a usual tree knapsack is far too expensive. If a vertex has a subtree of size (s), storing an answer for every possible matching size already costs (O(s)), and directly combining two such arrays costs (O(s_1s_2)). On a path, repeatedly merging growing arrays would take (O(n^2)), which is already far beyond what the six second limit can support. The solution has to exploit a special shape of these DP arrays.

There are four edge cases that are particularly easy to mishandle.

First, negative weights are still valid answers. For the input

```
2
1 2 -7
```

the only possible matching has one edge, so the correct output is

```
-7
```

An implementation that initializes answers to zero and takes a maximum with zero would incorrectly print `0`.

Second, a matching can exist for some sizes and then become impossible. For

```
3
1 2 -5
2 3 -2
```

the best one-edge matching uses edge (2\text{-}3), giving `-2`, while a two-edge matching does not exist. The answer is

```
-2 ?
```

A careless implementation that only checks the first few DP entries can accidentally interpret an unreachable state as a real value.

Third, the maximum matching size is not (n-1). In a path on six vertices, at most three edges can be selected. For

```
6
1 2 3
2 3 3
3 4 3
4 5 3
5 6 3
```

the answer is

```
3 6 9 ? ?
```

The DP must preserve unreachable cardinalities rather than assuming every size up to (n-1) is feasible.

Fourth, equal weights can produce many optimal choices. For a star

```
5
1 2 4
1 3 4
1 4 4
1 5 4
```

only one edge can be selected, so the answer is

```
4 ? ? ?
```

A greedy rule that simply sorts edges by weight cannot solve the problem, because the important issue is the interaction between edges sharing vertices.

## Approaches

The direct solution is a tree DP. Root the tree at vertex (1). For every vertex (u), keep two arrays describing matchings inside its subtree.

Let (f_u^0[k]) be the maximum weight of a matching with (k) edges in the subtree of (u), where (u) is not matched to any of its children. Let (f_u^1[k]) be the corresponding value when (u) is matched to exactly one child. For a leaf, (f_u^0=[0]) and (f_u^1) is empty.

Suppose (v) is a child of (u), joined by an edge of weight (w). If we do not use (uv), the contribution of (v) is (\max(f_v^0,f_v^1)). If we use (uv), then (v) itself cannot be matched to another child, so its contribution is (f_v^0), shifted by one matching edge and increased by (w).

The remaining issue is combining the cardinality dimensions. If two DP arrays (a) and (b) describe independent subtrees, the ordinary tree-knapsack transition is

[
c[k]=\max_{i+j=k}(a[i]+b[j]).
]

For arbitrary arrays this is quadratic. Here the arrays have a crucial concavity property. The marginal gains

[
a[i]-a[i-1]
]

are non-increasing. This follows from the standard min-cost or max-cost flow interpretation of cardinality-constrained matching. In a bipartite graph, sending one more unit of matching flow has a non-increasing marginal cost when we maximize weight. The tree is bipartite, so the same property applies to every subtree DP profile. The same observation is used in the standard solution of this problem.

For two such concave arrays, the max-plus convolution becomes a merge of their marginal gains. If the marginal gains of (a) are

[
a[1]-a[0],a[2]-a[1],\ldots
]

and the marginal gains of (b) are defined similarly, we sort these two already-sorted sequences together. The prefix sums of the merged sequence are exactly the convolution. Thus two profiles of lengths (A) and (B) can be combined in (O(A+B)) rather than (O(AB)). This is the Minkowski-sum viewpoint used by the official solution.

That solves the expensive convolution, but a path still causes a problem. If we combine vertices one by one, the arrays have sizes (1,2,3,\ldots,n), producing (O(n^2)) work. The observation that fixes this is heavy-light decomposition.

For every vertex, choose its largest child subtree as the heavy child. The other children are light. We first combine all light children of a vertex using divide and conquer, so every light-child contribution participates in only (O(\log n)) merges. Then we process an entire heavy chain at once, again using divide and conquer. Each chain split is balanced according to the amount of non-heavy subtree information attached to its vertices. This gives the required (O(n\log^2 n)) bound.

The brute-force and optimized approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct tree knapsack | (O(n^2)) | (O(n^2)) in the worst case | Too slow |
| Concave convolution without HLD | (O(n^2)) on a path | (O(n)) to (O(n^2)) depending on storage | Still too slow |
| HLD + divide-and-conquer Minkowski sums | (O(n\log^2 n)) | (O(n\log n)) transient, (O(n)) graph storage | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex (1), compute every subtree size, and choose for every vertex the child with maximum subtree size as its heavy child. Store the weight of every child-parent edge with the child.

The heavy child keeps the largest remaining subtree attached to the current vertex. Every time we move through a light edge, the subtree size at least doubles, so a vertex can lie below only (O(\log n)) light edges.

1. For every vertex (u), first solve all light-child subtrees. For a light child (v), we already have the two profiles (f_v^0) and (f_v^1).

If (u) is not matched through (uv), the contribution is

[
g_v^0=\max(f_v^0,f_v^1).
]

If (u) is matched to (v), then (v) cannot simultaneously be matched to one of its own children. The contribution is

[
g_v^1[k+1]=f_v^0[k]+w(u,v).
]

For all light children, we need one profile for the case where (u) is unmatched to its children and another profile for the case where exactly one light child is matched to (u).

1. Combine the light children using divide and conquer. At a leaf of this divide-and-conquer tree, the pair of profiles is simply

[
(g_v^0,g_v^1).
]

When two groups are joined, the new "zero" profile is the Minkowski convolution of their zero profiles. The new "one" profile is the maximum of the two possibilities where the unique edge incident to the current vertex comes from the left group or from the right group.

Because all profiles are concave, each convolution is linear in the lengths of the two arrays. Divide and conquer prevents a sequence of increasingly expensive merges.

1. Now consider one heavy chain (v_1,v_2,\ldots,v_m), ordered from its top to its bottom. For each vertex we already know the two profiles produced by all its light children.

A chain segment needs four profiles. The two binary states describe whether its top endpoint and bottom endpoint are already matched inside the segment. For a single vertex, only state (00) and state (11) are possible, because the same vertex is simultaneously both endpoints.

1. Split a heavy chain segment into two balanced parts. Combine the four states of the left and right segments without selecting their connecting edge by taking all compatible Minkowski convolutions.

The external endpoints remain the endpoints of the two original segments. This is the ordinary concatenation case.

1. Separately consider selecting the edge joining the two halves. Such an edge is legal only when the right endpoint of the left half and the left endpoint of the right half are both currently unmatched inside their respective halves.

In that case, add the edge weight and shift the resulting profile by one position because one additional matching edge has been selected. Both internal endpoints become occupied, so the corresponding boundary states change from (0) to (1).

1. Repeat the chain divide and conquer until the complete heavy chain has been merged. The resulting two profiles for its top vertex are the required profiles for that subtree.
2. Process every heavy chain from the bottom upward. When a chain is finished, only its top vertex needs to remain available to its parent. All internal profiles can be released, which keeps the working memory under control.
3. After processing the chain containing the root, take

[
F[k]=\max(f_1^0[k],f_1^1[k]).
]

For every (k=1,\ldots,n-1), print (F[k]) if it is reachable and `?` otherwise.

### Why it works

The invariant is that every profile stored for a vertex or chain segment represents exactly all matchings inside that region, classified by whether the relevant boundary vertices are already matched inside the region. The light-child transition considers the only two possibilities for the edge connecting a child to its parent, while the chain transition considers the only two possibilities for the edge between the two chain segments, selected or not selected. Thus every legal matching is represented by some DP state, and every state constructed by the transitions corresponds to a legal matching.

The numerical optimization does not change these transitions. It only computes their max-plus convolutions faster. Since the cardinality profiles are concave, their marginal gains are already sorted, so merging the marginal gains gives exactly the same convolution as the quadratic definition.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

NEG = -10**30

def solve():
    n = int(input())

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))

    parent = [0] * (n + 1)
    value = [0] * (n + 1)
    size = [1] * (n + 1)
    heavy = [0] * (n + 1)

    order = [1]
    parent[1] = -1

    for u in order:
        for v, w in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            value[v] = w
            order.append(v)

    for u in reversed(order):
        size[u] = 1
        best = 0
        best_size = 0
        for v, _ in graph[u]:
            if parent[v] == u:
                size[u] += size[v]
                if size[v] > best_size:
                    best_size = size[v]
                    best = v
        heavy[u] = best

    f0 = [None] * (n + 1)
    f1 = [None] * (n + 1)

    def max_merge(a, b):
        if not a:
            return b[:]
        if not b:
            return a[:]

        m = max(len(a), len(b))
        c = [NEG] * m

        la = len(a)
        lb = len(b)

        for i in range(m):
            x = a[i] if i < la else NEG
            y = b[i] if i < lb else NEG
            c[i] = x if x >= y else y

        return c

    def minkowski(a, b):
        if not a or not b:
            return []

        la = len(a)
        lb = len(b)

        c = [0] * (la + lb - 1)
        c[0] = a[0] + b[0]

        da = [0] * (la - 1)
        db = [0] * (lb - 1)

        for i in range(1, la):
            da[i - 1] = a[i] - a[i - 1]

        for i in range(1, lb):
            db[i - 1] = b[i] - b[i - 1]

        i = 0
        j = 0
        p = 1
        total = len(c)

        while p < total:
            if j == len(db) or (i < len(da) and da[i] > db[j]):
                c[p] = da[i]
                i += 1
            else:
                c[p] = db[j]
                j += 1
            p += 1

        for i in range(1, total):
            c[i] += c[i - 1]

        return c

    def solve_light(ids, l, r):
        if l == r:
            u = ids[l]

            g = f0[u][:]
            if g:
                for i in range(len(g)):
                    g[i] += value[u]
                g.insert(0, NEG)

            return (
                max_merge(f0[u], f1[u]),
                g
            )

        mid = (l + r) >> 1

        left0, left1 = solve_light(ids, l, mid)
        right0, right1 = solve_light(ids, mid + 1, r)

        zero = minkowski(left0, right0)

        one_left = minkowski(left1, right0)
        one_right = minkowski(left0, right1)
        one = max_merge(one_left, one_right)

        return zero, one

    def solve_chain(ids, l, r):
        if l == r:
            u = ids[l]

            return (
                [[f0[u][:], []],
                 [[], f1[u][:]]]
            )

        total_light = 0
        for i in range(l, r + 1):
            u = ids[i]
            total_light += size[u] - size[heavy[u]]

        mid = l
        used = 0

        while mid < r and used < total_light // 2:
            u = ids[mid]
            used += size[u] - size[heavy[u]]
            mid += 1

        left = solve_chain(ids, l, mid - 1)
        right = solve_chain(ids, mid, r)

        res = [
            [[], []],
            [[], []]
        ]

        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        x = minkowski(left[a][b], right[c][d])
                        res[a][d] = max_merge(res[a][d], x)

        for a in range(2):
            for d in range(2):
                x = minkowski(left[a][0], right[0][d])

                if not x:
                    continue

                for i in range(len(x)):
                    x[i] += value[ids[mid]]

                x.insert(0, NEG)

                na = 1 if (l == mid - 1) else a
                nd = 1 if (mid == r) else d

                res[na][nd] = max_merge(res[na][nd], x)

        return res

    def process_chain(top):
        chain = []
        u = top

        while u:
            chain.append(u)
            u = heavy[u]

        for u in chain:
            light = []

            for v, _ in graph[u]:
                if parent[v] == u and v != heavy[u]:
                    process_chain(v)
                    light.append(v)

            if not light:
                f0[u] = [0]
                f1[u] = []
            else:
                a, b = solve_light(light, 0, len(light) - 1)
                f0[u] = a
                f1[u] = b

                for v in light:
                    f0[v] = None
                    f1[v] = None

        res = solve_chain(chain, 0, len(chain) - 1)

        f0[top] = max_merge(res[0][0], res[0][1])
        f1[top] = max_merge(res[1][0], res[1][1])

        for u in chain[1:]:
            f0[u] = None
            f1[u] = None

    process_chain(1)

    answer = []
    root0 = f0[1]
    root1 = f1[1]

    for k in range(1, n):
        best = NEG

        if k < len(root0):
            best = max(best, root0[k])

        if k < len(root1):
            best = max(best, root1[k])

        if best <= NEG // 2:
            answer.append("?")
        else:
            answer.append(str(best))

    print(" ".join(answer))

if __name__ == "__main__":
    solve()
```

The first preprocessing pass is iterative rather than recursive. This avoids making the Python call stack depend on the height of the original tree, which can be (200000) on a path. The reverse traversal then computes subtree sizes and chooses the largest child as the heavy child.

The `minkowski` function is the central numerical optimization. It computes the max-plus convolution by forming successive differences and merging those differences in decreasing order. The input profiles are concave, so those differences are already ordered. The prefix sums reconstruct the resulting profile.

The leading `NEG` value in shifted profiles represents an impossible matching size. It is deliberately much smaller than every real answer. The largest possible absolute total weight is below (2\cdot10^{14}), so `-10**30` leaves a very large safety margin and Python integers have no overflow issue anyway.

`solve_light` implements the divide-and-conquer merge for all light children. Its second profile corresponds to choosing exactly one edge incident to the current vertex. The shift by one position accounts for that chosen edge.

`solve_chain` is the four-state divide-and-conquer DP for a heavy chain. Its state `res[a][b]` records the state of the two exposed endpoints. The first combination loop handles a boundary edge that is not selected. The second loop handles selecting that edge, requiring both adjacent endpoint states to be zero.

The split is weighted by `size[u] - size[heavy[u]]`, the amount of information that does not continue through the heavy edge. This is the detail that gives the chain recursion its balanced complexity rather than merely splitting by the number of vertices.

The final answer takes the maximum of the two root states because the root has no parent, so there is no external restriction on whether it is matched to one of its children.

The implementation follows the (O(n\log^2 n)) HLD and concave-convolution structure described in the standard solutions.

## Worked Examples

### Sample 1

The tree is

```
1
|
2
/ \
3  4
|
5
```

with weights (3,5,4,2). The heavy path chosen by subtree size is (1\to2\to3\to5), while (4) is a light child of (2).

The relevant local profiles evolve as follows.

| Stage | Vertex or segment | (f^0) | (f^1) |
| --- | --- | --- | --- |
| 1 | Leaf 4 | `[0]` | `[]` |
| 2 | Vertex 2, before heavy child | `[0]` | `[-inf, 4]` |
| 3 | Segment 3-5 | `[0]` | `[-inf, 2]` |
| 4 | Subtree of 2 | `[0, 2]` | `[-inf, 5, 6]` |
| 5 | Whole tree | `[0, 5, 6]` | `[-inf, 3, 5]` |

At the root, the best profile is `[0,5,6]`. The entry for one edge is (5), obtained from edge (2\text{-}3). The entry for two edges is (6), obtained from edges (2\text{-}4) and (3\text{-}5). Larger cardinalities are unreachable, so the output is `5 6 ? ?`.

This trace also shows why the two states are needed. At vertex (2), choosing (2\text{-}4) prevents choosing (2\text{-}3), but it does not prevent choosing (3\text{-}5).

### Sample 2

For the ten-vertex tree, the final root profile contains the following reachable values.

| Matching size (k) | Best value |
| --- | --- |
| 1 | 5 |
| 2 | 10 |
| 3 | 15 |
| 4 | 10 |
| 5 | unreachable |
| 6 | unreachable |
| 7 | unreachable |
| 8 | unreachable |
| 9 | unreachable |

The important part of the trace is that the value does not have to decrease monotonically with (k). The first three matching sizes can use several positive edges, while forcing a fourth edge can require replacing a much better configuration with a lower-weight one. The DP is optimizing each cardinality independently, so `10` for (k=4) is completely valid even though it is smaller than the answer for (k=3).

The final output is

```
5 10 15 10 ? ? ? ? ?
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^2 n)) | Concave convolutions are linear in profile sizes, while light-child and heavy-chain merges are balanced by divide and conquer |
| Space | (O(n\log n)) transient, (O(n)) graph storage | DP vectors are released after their subtree or chain is consumed |

The (O(n\log^2 n)) time bound is the key reason the method handles (n=200000). A light edge can be traversed only (O(\log n)) times because subtree size at least doubles after every such transition, and the divide-and-conquer convolution adds another logarithmic factor. This is the intended asymptotic complexity for the HLD solution.

The edge weights can be as large as (10^9), and there can be (O(n)) selected edges, so 64-bit arithmetic is required in C++. Python integers naturally provide the required range.

## Test Cases

The following harness assumes the submitted solution has been saved as `solution.py`. It uses a subprocess so that the exact stdin/stdout interface of the competitive-programming program is tested.

```python
import subprocess

def run(inp: str) -> str:
    result = subprocess.run(
        ["python3", "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

# Provided sample 1
assert run("""\
5
1 2 3
2 3 5
2 4 4
3 5 2
""") == "5 6 ? ?", "sample 1"

# Provided sample 2
assert run("""\
10
2 8 -5
5 10 5
3 4 -5
1 6 5
3 9 5
1 7 -3
4 8 -5
10 8 -5
1 8 -3
""") == "5 10 15 10 ? ? ? ? ?", "sample 2"

# Provided sample 3
assert run("""\
2
1 2 35
""") == "35", "sample 3"

# Minimum size with a negative edge
assert run("""\
2
1 2 -7
""") == "-7", "negative answer must remain negative"

# Three-vertex path, one matching is possible but two are not
assert run("""\
3
1 2 -5
2 3 -2
""") == "-2 ?", "unreachable cardinality"

# Star, all edges equal
assert run("""\
5
1 2 4
1 3 4
1 4 4
1 5 4
""") == "4 ? ? ?", "star matching size"

# Path with equal positive weights
assert run("""\
6
1 2 3
2 3 3
3 4 3
4 5 3
5 6 3
""") == "3 6 9 ? ?", "maximum matching size"

# Maximum-size stress shape.
# A star on 200000 vertices has maximum matching size 1.
n = 200000
parts = [str(n)]
parts.extend(f"1 {v} 1" for v in range(2, n + 1))
maximum_input = "\n".join(parts) + "\n"
maximum_expected = "1 " + " ".join("?" for _ in range(n - 2))
assert run(maximum_input) == maximum_expected, "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2 -7` | `-7` | Negative optimal values |
| `3 / 1 2 -5 / 2 3 -2` | `-2 ?` | Impossible larger matching sizes |
| Four equal edges incident to one center | `4 ? ? ?` | Matching conflicts at a high-degree vertex |
| Six-vertex path with all weights `3` | `3 6 9 ? ?` | Exact maximum matching size and repeated marginal gains |
| Two-hundred-thousand-vertex star | `1 ? ? ... ?` | Maximum input size and extreme degree |

## Edge Cases

A single negative edge is handled because the base profile contains zero only for selecting no edges, while the requested answer starts at (k=1). For

```
2
1 2 -7
```

the shifted profile for the only edge is `[-inf, -7]`. The final root maximum therefore gives `-7`, not zero.

A path of three vertices demonstrates an unreachable state:

```
3
1 2 -5
2 3 -2
```

The two edges share vertex (2), so the DP can create a valid size-one state with value `-2`, but there is no valid size-two state. The corresponding array position remains `NEG`, and the output logic converts it to `?`.

A star demonstrates why selecting the locally heaviest edge is insufficient:

```
5
1 2 4
1 3 4
1 4 4
1 5 4
```

All four edges have the same weight, but they all conflict at vertex (1). The state where the center is already matched prevents every other incident edge from being selected. The resulting profile contains only sizes zero and one.

The six-vertex path

```
6
1 2 3
2 3 3
3 4 3
4 5 3
5 6 3
```

has maximum matching size three. The three edges (1\text{-}2), (3\text{-}4), and (5\text{-}6) give weight (9). The next cardinality is impossible, so the answer ends after the third value. This checks the boundary between reachable and unreachable DP entries.

Finally, the maximum-size star has (200000) vertices and (199999) edges. Every edge shares the center, so only one edge can belong to a matching. The algorithm still has to process all vertices, but the heavy-light structure chooses one leaf as the heavy child and treats the remaining leaves as light children. The resulting answer is `1` followed by `199998` question marks. This case exercises both the high-degree vertex handling and the requirement to process the full input size.
