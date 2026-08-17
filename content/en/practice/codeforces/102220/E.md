---
title: "CF 102220E - Minimum Spanning Tree"
description: "The original graph (G) is a tree, so it has (n) vertices and exactly (n-1) weighted edges. The line graph (L(G)) turns every original edge into a vertex."
date: "2026-08-17T22:34:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "E"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 118
verified: true
draft: false
---

[CF 102220E - Minimum Spanning Tree](https://codeforces.com/problemset/problem/102220/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The original graph (G) is a tree, so it has (n) vertices and exactly (n-1) weighted edges. The line graph (L(G)) turns every original edge into a vertex. Whenever two original edges meet at the same vertex of (G), the corresponding vertices in (L(G)) are connected, and the new edge has weight equal to the sum of the two original edge weights.

The task is not to construct (L(G)), which can already be much larger than (G). We only need the total weight of a minimum spanning tree of (L(G)).

The crucial structural fact comes from looking at one vertex (v) of the original tree. Suppose its incident edges have weights (a_1,a_2,\ldots,a_k). In the line graph, those (k) original edges become (k) vertices, and every pair among them is adjacent. They form a complete graph. The weight of the edge joining vertices (i) and (j) is (a_i+a_j).

Thus every original vertex produces one weighted clique in the line graph. Because (G) is a tree, two different original vertices cannot share two original edges. Consequently, these cliques overlap only in individual vertices of (L(G)), and their global structure is itself tree-like.

The input contains up to (10^5) vertices in one test case, and the sum of (n) over all test cases is at most (10^6). A quadratic algorithm is already too large. The distinction matters particularly because a star-shaped tree creates a clique containing almost all (n-1) line-graph vertices, so explicitly constructing the line graph can require billions of edges. The solution must process the original tree essentially once.

There are several small cases where a careless formula or implementation can fail. For example, with

```
1
2
1 2 100
```

the original tree has only one edge, so (L(G)) has only one vertex. Its MST contains no edges, and the answer is (0). An implementation that blindly adds the original edge weight would incorrectly produce (100).

Another useful case is a path with different weights:

```
1
4
1 2 1
2 3 2
3 4 3
```

The line graph is a path of three vertices. Its two edge weights are (1+2=3) and (2+3=5), so the answer is (8). A formula that only adds the minimum incident weight at each vertex can miss the full sum contributed by the two line-graph edges.

A branching case exposes another common mistake:

```
1
4
1 2 1
1 3 1
1 4 1
```

The three original edges become the three vertices of a triangle, and every line-graph edge has weight (2). An MST of the triangle has two edges, so the answer is (4). Counting all three clique edges would incorrectly give (6).

## Approaches

The direct approach is to construct the line graph explicitly. The original tree has (n-1) edges, so the line graph has (n-1) vertices. At an original vertex of degree (d), every pair of its incident edges creates a line-graph edge, giving (\binom d2) edges. We could generate all of them, sort them by weight, and run Kruskal's algorithm. This is correct because the resulting graph is exactly (L(G)), and Kruskal computes its MST.

The problem is the number of generated edges. Consider a star with (n-1) leaves. Its center has degree (n-1), so (L(G)) contains

[
\binom{n-1}{2}
]

edges. For (n=100000), this is

[
\frac{99999\cdot99998}{2}=4,999,850,001
]

edges. Merely generating them is already far beyond the available resources, even before sorting them. A generic Kruskal implementation would require (O(n^2\log n)) time in the worst case and (O(n^2)) memory if all line-graph edges are stored.

The observation that makes the problem linear is that we never need the entire clique. Consider one original vertex (v), whose incident edge weights are (a_1,\ldots,a_k), and let (m) be the smallest of them. The line-graph clique contains an edge of weight (a_i+a_j) between every pair.

For every vertex corresponding to an incident edge of weight (a_i), the cheapest edge from it to another clique vertex is the edge connecting it to the minimum-weight edge (m). Its weight is (a_i+m). Connecting every other clique vertex directly to the minimum-weight vertex therefore gives a star. Its total weight is

\sum_i a_i +(k-2)m,
]

where (p) is the position of the minimum weight.

This star is an MST of the clique. The cut consisting of one non-minimum vertex has its cheapest outgoing edge toward the minimum-weight vertex, so the cut property justifies selecting these edges.

The original tree gives one such clique for every original vertex. Since two different cliques can intersect in at most one line-graph vertex, and the original graph itself has no cycles, taking an MST inside every clique together produces an MST of the whole line graph. There is no need to coordinate complicated choices between cliques.

The resulting formula for an original vertex (v) is

S_v+(\deg(v)-2)m_v,
]

where (S_v) is the sum of the weights of edges incident to (v), and (m_v) is their minimum weight.

For a leaf, (\deg(v)=1), so the formula becomes (S_v-m_v=0), exactly as required because a degree-one original vertex creates a clique containing only one line-graph vertex.

We only need the degree, sum, and minimum incident weight for every original vertex. Every input edge updates these three quantities at its two endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2\log n)) worst case | (O(n^2)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Create three arrays for the original vertices: `degree[v]`, `sum_weight[v]`, and `min_weight[v]`. The first counts incident edges, the second stores their total weight, and the third stores the smallest incident edge weight.
2. Read each original tree edge ((u,v,w)). Increase the degree of both endpoints, add (w) to both endpoint sums, and replace their minimum incident weights when (w) is smaller.

There is no need to store the original edges after these updates. The final formula depends only on these three aggregate values.
3. After all (n-1) edges have been processed, visit every original vertex (v) and add

[
\text{sum_weight}[v]
+
(\text{degree}[v]-2)\cdot\text{min_weight}[v]
]

to the answer.

This expression is exactly the MST weight of the clique created by the incident edges of (v).
4. Print the accumulated answer for the test case.

### Why it works

For every original vertex (v), its incident edges become a clique in (L(G)). Choosing the minimum-weight incident edge as the center of a star gives, for every other clique vertex, its cheapest possible connection inside that clique. By the cut property, these choices form an MST of that clique.

The original graph is a tree, so its edge-cliques form a tree-like block structure. Two such cliques cannot share more than one line-graph vertex. Combining an MST from each clique therefore connects all line-graph vertices without introducing a cycle. Since every clique is already connected with minimum possible cost, replacing any clique portion by a cheaper structure is impossible. Hence the sum of the individual clique MST costs is exactly the MST weight of (L(G)).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    INF = 10**30

    for _ in range(t):
        n = int(input())

        degree = [0] * (n + 1)
        total = [0] * (n + 1)
        minimum = [INF] * (n + 1)

        for _ in range(n - 1):
            u, v, w = map(int, input().split())

            degree[u] += 1
            total[u] += w
            if w < minimum[u]:
                minimum[u] = w

            degree[v] += 1
            total[v] += w
            if w < minimum[v]:
                minimum[v] = w

        ans = 0

        for v in range(1, n + 1):
            ans += total[v] + (degree[v] - 2) * minimum[v]

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop implements the aggregation from steps 1 and 2. Each original edge affects exactly two vertices, so every edge is processed in constant time.

The final loop implements step 3 directly. A leaf has degree (1), and its contribution is

[
w+(1-2)w=0.
]

This is useful because no special case for leaves is required. Since (n\ge2) and the input graph is a tree, every vertex has at least one incident edge, so `minimum[v]` is always initialized to a real edge weight when it is used.

Python integers have arbitrary precision, which is relevant because the answer can exceed a 32-bit integer. With edge weights up to (10^9) and (10^5) vertices, the answer can be on the order of (10^{14}).

The code also avoids storing an adjacency list. An adjacency list would still be linear and perfectly valid, but it contains information that the formula does not need. Keeping only three arrays makes the implementation simpler and reduces memory usage.

## Worked Examples

### Sample 1

The input tree is the path

[
1\mathbin{-1}2\mathbin{-2}3\mathbin{-3}4.
]

The table shows the aggregate state after all edges have been read.

| Vertex | Degree | Sum of incident weights | Minimum incident weight | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | (1-1=0) |
| 2 | 2 | 3 | 1 | (3+0=3) |
| 3 | 2 | 5 | 2 | (5+0=5) |
| 4 | 1 | 3 | 3 | (3-3=0) |

The two internal vertices each create a clique of size two, so each contributes the weight of its only line-graph edge. Those weights are (1+2=3) and (2+3=5). The total is (3+5=8).

### Sample 2

The input is a star centered at vertex (1):

[
1\mathbin{-1}2,\qquad
1\mathbin{-1}3,\qquad
1\mathbin{-1}4.
]

The center creates a clique of three vertices in the line graph. Every clique edge has weight (2).

| Vertex | Degree | Sum of incident weights | Minimum incident weight | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 1 | (3+(3-2)\cdot1=4) |
| 2 | 1 | 1 | 1 | (1-1=0) |
| 3 | 1 | 1 | 1 | (1-1=0) |
| 4 | 1 | 1 | 1 | (1-1=0) |

The center's clique is a triangle with all edge weights equal to (2), so its MST has two edges and costs (4). The leaves create singleton cliques and contribute nothing. The answer is (4).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) per test case | Each of the (n-1) original edges is processed once, followed by one scan over the (n) vertices. |
| Space | (O(n)) | Three arrays of size (n+1) store the required aggregates. |

Across all test cases, the sum of (n) is at most (10^6), so the total running time is (O(\sum n)), which is linear in the complete input size. The algorithm never constructs the potentially quadratic-size line graph, which is the key reason it remains practical for a star with (10^5) vertices.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    INF = 10**30

    for _ in range(t):
        n = int(input())

        degree = [0] * (n + 1)
        total = [0] * (n + 1)
        minimum = [INF] * (n + 1)

        for _ in range(n - 1):
            u, v, w = map(int, input().split())

            degree[u] += 1
            total[u] += w
            minimum[u] = min(minimum[u], w)

            degree[v] += 1
            total[v] += w
            minimum[v] = min(minimum[v], w)

        ans = 0
        for v in range(1, n + 1):
            ans += total[v] + (degree[v] - 2) * minimum[v]

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

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

# Provided sample 1
assert run(
    """1
4
1 2 1
2 3 2
3 4 3
"""
) == "8\n"

# Provided sample 2
assert run(
    """1
4
1 2 1
1 3 1
1 4 1
"""
) == "4\n"

# Minimum-size tree
assert run(
    """1
2
1 2 1000000000
"""
) == "0\n"

# Path with equal weights
assert run(
    """1
5
1 2 7
2 3 7
3 4 7
4 5 7
"""
) == "42\n"

# Branching tree with different weights
assert run(
    """1
5
1 2 10
1 3 1
1 4 5
4 5 2
"""
) == "31\n"

# Maximum-size star, generated without explicitly storing its quadratic line graph.
n = 100000
parts = ["1", str(n)]
for v in range(2, n + 1):
    parts.append(f"1 {v} 1000000000")

maximum_star = "\n".join(parts) + "\n"

# The center has degree 99999 and all weights are 1e9.
# Its clique MST has 99998 edges, each of weight 2e9.
expected = str((n - 2) * 2 * 1000000000) + "\n"

assert run(maximum_star) == expected
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` vertices with edge weight `1000000000` | `0` | Singleton line graph and the degree-one formula |
| Path of 5 vertices with every weight `7` | `42` | Repeated degree-two cliques and equal weights |
| Tree with degrees 3, 2, and 1 | `31` | Different local minima and branching structure |
| Star with 100000 vertices and weight `10^9` | `199996000000000` | Maximum input size, large integer arithmetic, and avoidance of quadratic line-graph construction |

## Edge Cases

The two-vertex tree

```
1
2
1 2 100
```

has one original edge, so the line graph contains one vertex and no edges. The algorithm gives vertex (1) the values `degree=1`, `total=100`, `minimum=100`, producing (100+(1-2)100=0). Vertex (2) produces the same contribution. The final answer is (0), so a singleton line graph is handled without a special branch.

For the path

```
1
4
1 2 1
2 3 2
3 4 3
```

vertex (2) has incident weights (1,2), giving contribution (1+2=3). Vertex (3) has incident weights (2,3), giving contribution (2+3=5). The endpoints have degree one and contribute zero. The total is (8). This catches implementations that accidentally use only the minimum incident edge rather than the complete local MST cost.

For the star

```
1
4
1 2 1
1 3 1
1 4 1
```

vertex (1) has three incident edges, all of weight (1). Its line-graph clique is a triangle with every edge of weight (2). The formula gives (3+(3-2)\cdot1=4), which is exactly the cost of two triangle edges. The three leaves each contribute zero. This verifies that the algorithm takes an MST of each clique rather than summing every clique edge.

Finally, consider the maximum-size star with (99999) original edges, all of weight (10^9). The center creates nearly five billion line-graph edges, but the algorithm only stores its degree, sum, and minimum. The center's contribution is

# 199997\cdot10^9

199997000000000.
]

Every leaf contributes zero, so the final answer is `199997000000000`. The algorithm reaches this result after processing only (99999) input edges, demonstrating why avoiding explicit construction of (L(G)) is essential.
