---
title: "CF 102361B - The Tree of Haruhi Suzumiya"
description: "We have a rooted tree whose root is vertex 1. Every vertex has an integer weight, and its depth is its distance from the root."
date: "2026-08-13T00:06:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "B"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 246
verified: true
draft: false
---

[CF 102361B - The Tree of Haruhi Suzumiya](https://codeforces.com/problemset/problem/102361/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree whose root is vertex 1. Every vertex has an integer weight, and its depth is its distance from the root. We split all vertices into group A and group B, and for every possible size of B, from 0 through n, we need the minimum possible value of the two groups' total dislike.

Group A pays for three kinds of things. An ancestor with a larger weight than its descendant creates a penalty, two incomparable vertices create a penalty, and every vertex in A contributes its depth. Group B has only one kind of pair penalty: an ancestor with a smaller weight than its descendant.

The subtle part is that a pair can be penalized in A, penalized in B, or penalized in neither group. When two vertices have equal weights and one is an ancestor of the other, neither group dislikes that pair. That exceptional case is the reason a simple "assign every vertex a score and sort" argument needs one extra structural observation.

The official constraints allow n up to 500,000, with a 2 second time limit and 1024 MB memory limit. A quadratic algorithm would already require around 250 billion pair operations for one full traversal of the vertices, so even O(n²) is far beyond the intended range. The solution needs to stay around O(n log n), with linear memory.

The first edge case is a single vertex.

```
1
7
```

There is no pair and the only vertex has depth zero, so the answer is

```
0
0
```

A solution that initializes the root depth to one would incorrectly report a positive cost.

The second edge case is equal weights along an ancestor chain.

```
3
1 1 1
1 2
2 3
```

The correct output is

```
3
1
0
0
```

With all three vertices in A, the depth contribution is 0 + 1 + 2 = 3. If only the deepest vertex moves to B, A contains the first two vertices and costs 1. If the deepest two move to B, A contains only the root and costs zero. Equal-weight ancestor pairs never contribute to either group. A solution that treats every pair as belonging to either the A-side or B-side will get this case wrong.

The third edge case is a branching tree with equal weights.

```
4
1 1 1 1
1 2
1 3
1 4
```

The correct output is

```
6
3
1
0
0
```

When one leaf is moved to B, the other three vertices remain in A. The three leaves have pairwise incomparable relations, so the remaining two leaves contribute one pair penalty, while their depths contribute two, giving 3. When two leaves are moved to B, A contains the root and one leaf, which are comparable, so the cost is only 1. This case catches implementations that handle equal-weight ancestor chains but forget that equal-weight vertices can branch.

## Approaches

The direct approach is to enumerate the set chosen by B. For each subset, its size tells us which output position it belongs to, and we can evaluate every pair of vertices and every depth contribution to obtain the exact cost. This is correct because it considers every possible partition.

The problem is the number of subsets. There are 2^n possible choices of B, and evaluating one choice naively takes Θ(n²) pair checks. In the worst case this is Θ(n²2^n), which is hopeless for n = 500,000. Even computing one answer by enumerating all subsets of a particular size requires binomially many choices.

The useful observation comes from looking at one pair at a time. Let x_i be 1 when vertex i belongs to B and 0 when it belongs to A. For an incomparable pair, the pair costs 1 exactly when both endpoints are in A, so its contribution is

[
(1-x_i)(1-x_j)=1-x_i-x_j+x_ix_j.
]

For an ancestor pair whose ancestor has larger weight, the same expression appears because the penalty belongs to A. For an ancestor pair whose ancestor has smaller weight, the penalty belongs to B, so the contribution is simply

[
x_ix_j.
]

The only pair with no contribution is an ancestor pair with equal weights.

This gives a common quadratic form. After fixing |B| = k, the sum of x_i x_j over all ordinary pairs contributes a fixed (\binom{k}{2}), except that equal-weight ancestor pairs have been omitted. The remaining vertex-dependent part can be represented by a score for every vertex.

Let b_i be the depth of i plus the number of A-type pair penalties involving i. If we ignored equal-weight ancestor pairs for a moment, moving i to B would improve the objective by b_i, while choosing two B vertices introduces the fixed (\binom{k}{2}) term.

Equal-weight ancestor pairs need special treatment. Suppose vertex u is an equal-weight ancestor of v. If u is selected for B but v is not, we can replace u by v without making the solution worse. Along an equal-weight parent-child edge, the score b strictly gains enough to compensate for every equal-weight descendant that can be lost from the pair reward. Repeating this transformation gives an optimal solution in which, for every equal-weight ancestor relation, selecting the ancestor implies selecting all equal-weight descendants.

For such a downward-closed set, the number of equal-weight ancestor pairs inside B is simply the sum, over selected vertices, of their number of equal-weight descendants. We can absorb this into the vertex score.

After the algebra is simplified, the final score has an especially compact form:

[
g_i =
n-\operatorname{subtreeSize}_i
+#{\text{ancestors of }i\text{ with weight}>w_i}
+#{\text{strict descendants of }i\text{ with weight}\le w_i}.
]

Once these scores are known, the best solution of size k is obtained by taking the k largest scores. Equal scores must be ordered by decreasing depth, which preserves the required downward-closed property for equal-weight ancestor relations.

The initial cost, when every vertex is in A, also simplifies. The number of incomparable pairs is

[
\binom n2-\sum_i d_i,
]

because vertex i has exactly d_i strict ancestors. Adding Mikuru's (\sum_i d_i) cancels that term. Thus the initial cost is simply

[
C=\binom n2+
#{(u,v)\text{ is an ancestor of }v,\ w_u>w_v}.
]

The latter count is exactly the sum of the ancestor-greater counts used in g_i.

The remaining task is to calculate subtree sizes, ancestor-greater counts, and descendant-less-or-equal counts efficiently. An Euler tour makes every subtree a contiguous interval. A Fenwick tree can then answer the required offline counting queries in O(log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex 1 with an iterative DFS. Store the parent, depth, preorder position, and the preorder list. Processing the vertices in reverse preorder then gives every subtree size. The subtree of vertex i occupies the Euler interval ([tin_i,tout_i]).
2. Sort all vertices by weight. We will use this one ordering for two offline Fenwick sweeps. Sorting once is enough because the two required counts use opposite directions of the same weight order.
3. Compute (a_i), the number of ancestors of i whose weight is strictly greater than (w_i). Process vertices in decreasing weight groups. Before inserting a group, query every vertex in that group. The Fenwick tree stores range additions over subtrees, so an already inserted vertex contributes 1 to every vertex in its subtree. Since only larger weights have been inserted, the query at i counts exactly its larger-weight ancestors. Vertices of the same weight are queried before insertion, which correctly enforces strict inequality.
4. Compute (c_i), the number of strict descendants of i whose weight is at most (w_i). Reset the Fenwick tree and process weight groups in increasing order. Insert every vertex of the current group at its Euler position, then query the whole subtree interval. The result counts vertices in the subtree with weight at most (w_i), including i itself, so subtract one.
5. Compute

[
g_i=n-\operatorname{subtreeSize}_i+a_i+c_i.
]

The first term represents vertices outside i's subtree. The second term accounts for larger-weight ancestors. The third term accounts for descendants whose weight is small enough to participate in the A-side score, including equal-weight descendants.

1. Compute the all-A baseline

[
C=\binom n2+\sum_i a_i.
]

The cancellation between incomparable-pair penalties and depth penalties is what makes this expression so short.

1. Sort vertices by decreasing (g_i), breaking ties by decreasing depth. For equal-weight ancestor and descendant vertices, the descendant has a score at least as large as the ancestor. When the scores tie, deeper first makes every prefix downward-closed with respect to equal-weight ancestry.
2. Let (P_k) be the sum of the first k scores. The answer for (|B|=k) is

[
\boxed{C+\binom{k}{2}-P_k}.
]

For k = 0, the prefix sum is zero and the formula gives the all-A cost. For k = n, it gives the cost of putting every vertex into B.

Why it works: For any fixed B, every non-equal ancestor or incomparable pair contributes a quadratic term (x_ix_j), while every A-side pair also contributes a linear (-x_i) term for each endpoint. Since exactly k vertices have x_i = 1, the ordinary quadratic terms contribute (\binom{k}{2}). Equal-weight ancestor pairs are the only missing quadratic terms, and their contribution is exactly the number of such selected pairs. The score (g_i) incorporates both the linear improvement and the equal-weight descendant reward. An optimal set can be transformed into one that is downward-closed among equal-weight descendants without decreasing its score. For every such set, the equal-weight pair reward is exactly the sum of the corresponding descendant counts, so maximizing the objective is precisely maximizing the sum of g_i. Taking the k largest g_i does that, and the depth tie-break makes the selected prefix downward-closed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    w = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    parent = [-2] * n
    depth = [0] * n
    tin = [0] * n
    order = []

    parent[0] = -1
    stack = [0]

    while stack:
        u = stack.pop()
        tin[u] = len(order) + 1
        order.append(u)

        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)

    size = [1] * n
    for u in reversed(order):
        p = parent[u]
        if p >= 0:
            size[p] += size[u]

    tout = [0] * n
    for u in range(n):
        tout[u] = tin[u] + size[u] - 1

    by_weight = list(range(n))
    by_weight.sort(key=w.__getitem__)

    bit = [0] * (n + 2)

    def add(pos, delta):
        while pos <= n:
            bit[pos] += delta
            pos += pos & -pos

    def prefix(pos):
        res = 0
        while pos:
            res += bit[pos]
            pos -= pos & -pos
        return res

    # Number of strictly larger-weight ancestors.
    anc_greater = [0] * n

    i = n - 1
    while i >= 0:
        j = i
        value = w[by_weight[i]]
        while j >= 0 and w[by_weight[j]] == value:
            j -= 1

        for p in range(j + 1, i + 1):
            u = by_weight[p]
            anc_greater[u] = prefix(tin[u])

        for p in range(j + 1, i + 1):
            u = by_weight[p]
            add(tin[u], 1)
            add(tout[u] + 1, -1)

        i = j

    # Reuse the Fenwick tree.
    bit = [0] * (n + 2)

    # Number of strict descendants with weight <= w[i].
    desc_le = [0] * n

    i = 0
    while i < n:
        j = i
        value = w[by_weight[i]]
        while j < n and w[by_weight[j]] == value:
            j += 1

        for p in range(i, j):
            u = by_weight[p]
            add(tin[u], 1)

        for p in range(i, j):
            u = by_weight[p]
            desc_le[u] = prefix(tout[u]) - prefix(tin[u] - 1) - 1

        i = j

    score = [0] * n
    base = n * (n - 1) // 2

    for u in range(n):
        score[u] = n - size[u] + anc_greater[u] + desc_le[u]
        base += anc_greater[u]

    # Equal-score equal-weight ancestors must come after descendants.
    vertices = list(range(n))
    scale = n + 1
    vertices.sort(
        key=lambda u: -(score[u] * scale + depth[u])
    )

    ans = [0] * (n + 1)
    prefix_score = 0

    for k, u in enumerate(vertices, 1):
        prefix_score += score[u]
        ans[k] = base + k * (k - 1) // 2 - prefix_score

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The first DFS is iterative rather than recursive because a tree can be a chain of 500,000 vertices, which would overflow Python's recursion limit and also make a recursive implementation fragile. The preorder position is one-based because Fenwick trees naturally use one-based indices.

The reverse traversal computes subtree sizes without needing a separate postorder traversal. Once the sizes are known, `tout[u] = tin[u] + size[u] - 1` follows directly from the Euler ordering.

The first Fenwick sweep uses range additions and point queries. Adding one to the entire subtree of a vertex means that a point query at i counts exactly the active ancestors of i. Processing strictly larger weights before the current weight group makes equal weights invisible to the query.

The second sweep uses point additions and range queries. At the end of weight group w, the Fenwick tree contains every vertex whose weight is at most w. A subtree range query counts such vertices inside the subtree. The vertex itself is included, so the final subtraction of one is necessary.

The formula for `score` already includes equal-weight descendants through `desc_le`. There is no separate equal-weight term in the implementation because

#(\text{descendants with weight}\le w_i).
]

Python integers have arbitrary precision, which is useful here because the intermediate pair counts are Θ(n²), around 1.25 × 10¹¹ at the maximum input size.

The final sort uses `score * (n + 1) + depth` as a single integer key. This avoids allocating a two-element tuple for every vertex. The score is the primary key, while depth only resolves equal scores.

## Worked Examples

The official sample is

```
4
4 1 2 3
1 2
2 3
2 4
```

The DFS gives depths 0, 1, 2, 2 and subtree sizes 4, 3, 1, 1. The ancestor-greater counts and descendant-less-or-equal counts are:

| Vertex | Depth | Subtree Size | Larger Ancestors | Descendants ≤ Weight | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 0 | 3 | 3 |
| 2 | 1 | 3 | 1 | 0 | 2 |
| 3 | 2 | 1 | 1 | 0 | 4 |
| 4 | 2 | 1 | 1 | 0 | 4 |

The baseline is

[
\binom42 + (0+1+1+1)=6+3=9.
]

The sorted scores are 4, 4, 3, 2.

| k | Selected scores | Prefix Score | (\binom{k}{2}) | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | 0 | 0 | 9 |
| 1 | 4 | 4 | 0 | 5 |
| 2 | 4, 4 | 8 | 1 | 2 |
| 3 | 4, 4, 3 | 11 | 3 | 1 |
| 4 | 4, 4, 3, 2 | 13 | 6 | 2 |

This reproduces the official output `9 5 2 1 2`. The selected vertices for k = 1, 2, 3 can be vertices 3, then 3 and 4, then 1, 3 and 4, matching the schemes described in the statement.

For the second example, consider an equal-weight chain.

```
3
1 1 1
1 2
2 3
```

Every ancestor pair has equal weights, so neither Haruhi nor Kyon dislikes any ancestor pair. The only cost when everything is in A is the depth sum.

| Vertex | Depth | Subtree Size | Larger Ancestors | Descendants ≤ Weight | Score |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 0 | 2 | 2 |
| 2 | 1 | 2 | 0 | 1 | 2 |
| 3 | 2 | 1 | 0 | 0 | 2 |

All scores tie, so decreasing depth chooses vertex 3 first, then vertex 2, then vertex 1.

| k | Selected vertices | Prefix Score | (\binom{k}{2}) | Answer |
| --- | --- | --- | --- | --- |
| 0 | none | 0 | 0 | 3 |
| 1 | 3 | 2 | 0 | 1 |
| 2 | 3, 2 | 4 | 1 | 0 |
| 3 | 3, 2, 1 | 6 | 3 | 0 |

The tie-breaking is essential here. If vertex 1 were selected before vertex 3, the selected set would not be downward-closed among equal weights, and the simplified score formula would no longer represent the equal-weight pair reward correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | One tree traversal, one weight sort, two Fenwick sweeps, and one final sort |
| Space | O(n) | Tree storage, Euler data, scores, sorting arrays, and Fenwick tree |

The dominant operations are the two Fenwick sweeps and the sorting operations. With n = 500,000, O(n log n) is the intended scale for the 2 second C++ limit, while the large 1024 MB memory allowance leaves room for the linear auxiliary arrays used by the Python implementation.

## Test Cases

```python
# The solution code above should be placed in the same file before these tests.
# The test harness calls solve() with redirected stdin/stdout.

import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return out.getvalue() + ("\n" if out.getvalue() and not out.getvalue().endswith("\n") else "")

# Official sample
sample = """\
4
4 1 2 3
1 2
2 3
2 4
"""
assert run(sample) == "9\n5\n2\n1\n2\n", "official sample"

# Minimum-size input
minimum = """\
1
7
"""
assert run(minimum) == "0\n0\n", "single vertex"

# Equal weights on a chain
equal_chain = """\
3
1 1 1
1 2
2 3
"""
assert run(equal_chain) == "3\n1\n0\n0\n", "equal-weight chain"

# Equal weights on a branching tree
equal_star = """\
4
1 1 1 1
1 2
1 3
1 4
"""
assert run(equal_star) == "6\n3\n1\n0\n0\n", "equal-weight branching tree"

# Boundary weights and strict inequalities
boundary = """\
2
500000 1
1 2
"""
assert run(boundary) == "2\n0\n0\n", "maximum and minimum weights"

# Maximum-size test, all weights equal, chain.
# For an equal-weight chain, the answer for k B-vertices is
# C(n-k, 2), so the expected output can be generated directly.
n = 500000
weights = " ".join(["1"] * n)
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
maximum_input = f"{n}\n{weights}\n{edges}\n"

expected = "\n".join(
    str((n - k) * (n - k - 1) // 2)
    for k in range(n + 1)
) + "\n"

assert run(maximum_input) == expected, "maximum-size all-equal chain"
```

The custom tests exercise different parts of the derivation. The single-vertex case checks the root depth convention and all empty-pair boundaries. The equal-weight chain checks the exceptional pair type and the depth-based tie-breaking. The equal-weight star checks branching among equal-weight descendants. The boundary-weight case checks strict versus non-strict comparisons. The maximum-size chain checks both scalability and the formula over the full range of k.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0 0` | Minimum n and root depth |
| Equal-weight chain of 3 vertices | `3 1 0 0` | Equal ancestor weights and tie-breaking |
| Equal-weight star of 4 vertices | `6 3 1 0 0` | Branching equal-weight descendants |
| Two vertices with weights `500000 1` | `2 0 0` | Strict weight comparisons and boundary values |
| Equal-weight chain with n = 500000 | (\binom{500000-k}{2}) | Maximum n and linear-memory implementation |

## Edge Cases

For the single-vertex input

```
1
7
```

the DFS assigns depth zero and subtree size one. There are no ancestors and no descendants, so both `anc_greater` and `desc_le` are zero. The score is (1-1=0), and the baseline is (\binom12=0). Both k = 0 and k = 1 produce zero.

For the equal-weight chain

```
3
1 1 1
1 2
2 3
```

every ancestor comparison has equal weights, so the larger-ancestor counts are all zero. The scores are all 2 because the first vertex has two qualifying descendants, the second has one descendant plus one vertex outside its subtree, and the third has two vertices outside its subtree. All three scores tie. Sorting by decreasing depth gives the order 3, 2, 1, so every prefix is downward-closed. The resulting answers are 3, 1, 0, 0.

For the equal-weight star

```
4
1 1 1 1
1 2
1 3
1 4
```

the root has score 3 because it has three equal-weight descendants, and every leaf also has score 3 because three vertices lie outside its subtree. The depth tie-break puts all leaves before the root. With two vertices in B, two leaves are selected, leaving the root and one leaf in A, so the cost is exactly the remaining leaf's depth, 1. With three vertices in B, all leaves are selected and A contains only the root, giving zero.

For the strict boundary case

```
2
500000 1
1 2
```

the root has a larger weight than its child, so the pair is an A-side penalty when both vertices are in A. The baseline is (\binom22+1=2). The child has score 2, so selecting it for B reduces the cost to zero. Selecting both vertices for B also costs zero because Kyon only dislikes an ancestor with a smaller weight than its descendant, which is false here.

For the maximum-size equal-weight chain, every pair of vertices is an ancestor pair and hence receives no pair penalty. The only cost is the sum of depths of vertices left in A. The optimal B set consists of the deepest k vertices, leaving the first n-k vertices in A. Their depths sum to

\frac{(n-k)(n-k-1)}2.
]

The implementation's formula produces exactly the same expression, confirming that the quadratic correction and the equal-weight tie-breaking behave correctly even at the maximum input size.
