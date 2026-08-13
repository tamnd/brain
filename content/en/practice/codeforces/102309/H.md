---
title: "CF 102309H - Horton and Orz Pandas"
description: "We have an undirected graph whose vertices are the Orz Pandas and whose edges are possible data links. Every edge has two positive values, a and b. For a chosen set of edges S, the communication requirement says that the chosen edges must form a connected spanning subgraph."
date: "2026-08-13T23:47:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "H"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 127
verified: true
draft: false
---

[CF 102309H - Horton and Orz Pandas](https://codeforces.com/problemset/problem/102309/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph whose vertices are the Orz Pandas and whose edges are possible data links. Every edge has two positive values, `a` and `b`. For a chosen set of edges `S`, the communication requirement says that the chosen edges must form a connected spanning subgraph. The score of such a set is

[
f(S)=\frac{\sum_{e\in S} b_e}{\sum_{e\in S} a_e}.
]

The task is to maximize this ratio.

The denominator is always positive because every `a_e` is positive and a connected graph with `n > 1` needs at least one edge. The graph is guaranteed to contain at least one connected spanning subgraph, so the optimization problem always has a feasible solution.

The constraints are large enough that enumerating edge subsets is completely impossible. With up to (10^5) edges, even (O(m^2)) is already around (10^{10}) operations, while the graph algorithms we need should be close to (O(m\log m)) per optimization step. The number of vertices is at most (10^4), so a disjoint set union structure is a natural fit for repeatedly maintaining connected components. The values of `a` and `b` can reach (10^7), so sums can reach roughly (10^{12}). Python integers handle this safely, while floating point is needed only for the ratio parameter.

There are several cases where an apparently reasonable simplification fails.

First, the answer does not have to be represented by a spanning tree. Consider

```
3 3
1 2 1 10
2 3 1 1
1 3 10 10
```

Choosing edges `1-2` and `2-3` gives (11/2=5.5), while choosing all three gives (21/12=1.75). The optimal solution happens to be a tree here, but this example shows that simply choosing every edge with a large individual ratio is not enough. Connectivity and the accumulated numerator and denominator have to be considered together.

Second, a transformed edge can have negative value and still be necessary. For example,

```
3 2
1 2 1 10
2 3 100 1
```

The only connected solution contains both edges, so the answer is

[
\frac{10+1}{1+100}=\frac{11}{101}.
]

A method that simply keeps edges with positive transformed weight would discard the second edge and leave the graph disconnected.

Third, several edges can have exactly the same ratio. For

```
3 3
1 2 7 7
2 3 7 7
1 3 14 14
```

every feasible choice has score (1). The algorithm must handle zero transformed weights without treating them as a reason to terminate prematurely.

## Approaches

The brute-force solution is conceptually straightforward. Enumerate every subset of the `m` possible links, test whether the selected edges connect all `n` vertices, and, for every connected subset, compute the ratio of its total `b` value to its total `a` value. There are (2^m) subsets, and checking connectivity costs (O(n+m)) with DFS or DSU. The worst-case operation count is therefore (O(2^m(n+m))), which is already hopeless for even a few dozen edges, let alone (10^5).

A more tempting idea is to search for a spanning tree with the best ratio. That is not enough, because the original problem permits extra edges. An extra edge can improve the ratio if its own `b/a` ratio is above the current ratio, even when it creates a cycle. The optimization is over connected subgraphs, not only trees.

The key observation is to temporarily replace the ratio objective by a linear objective. Suppose we guess that the answer is some value (\lambda). For a connected edge set `S`, define

[
W_\lambda(S)=\sum_{e\in S}(b_e-\lambda a_e).
]

If the true optimum is (R), then

[
R=\max_S\frac{B(S)}{A(S)}
]

is equivalent to saying

[
\max_S \left(B(S)-R A(S)\right)=0.
]

For a candidate (\lambda), an edge has transformed weight

[
w_e=b_e-\lambda a_e.
]

Now we need to find the maximum total transformed weight among all connected spanning subgraphs.

This auxiliary problem has a simple greedy structure. Every edge with positive transformed weight should be included, because adding it cannot hurt connectivity and strictly increases the transformed objective. Every zero-weight edge can also be included because it costs nothing in the transformed objective and may help connectivity. After all nonnegative edges have been included, their endpoints form some connected components. The only remaining task is to connect those components. Since every edge still being considered has negative transformed weight, we want the least harmful edges that connect the components. That is exactly a maximum spanning tree problem on the remaining components, which Kruskal's algorithm solves by processing transformed weights from largest to smallest.

This gives an exact oracle for a fixed (\lambda).

We then use Dinkelbach's fractional programming method. Start with any feasible connected edge set and let its ratio be (\lambda). Find the connected subgraph maximizing (B-\lambda A). If its transformed value is zero, (\lambda) is the optimum. Otherwise, the newly selected subgraph has a strictly better ratio, so replace (\lambda) by its ratio and repeat.

The brute-force works because it directly evaluates every feasible subgraph, but fails because the number of subgraphs is exponential. The observation that a ratio can be converted into a linear expression gives us a maximum-weight connected-subgraph oracle, and Dinkelbach's method turns repeated calls to that oracle into the desired optimum.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^m(n+m))) | (O(n+m)) | Too slow |
| Binary search + transformed connected-subgraph oracle | (O(Km\log m)) | (O(n+m)) | Correct, but many oracle calls |
| Dinkelbach + transformed connected-subgraph oracle | (O(Im\log m)) | (O(n+m)) | Accepted |

Here `K` is the number of binary-search iterations and `I` is the number of Dinkelbach iterations. For this finite combinatorial problem, Dinkelbach reaches an optimal ratio after finitely many changes of the selected solution, and in practice the number of iterations is small. The accepted contest approach uses this property rather than paying for dozens of fixed-precision binary-search rounds.

## Algorithm Walkthrough

1. Read all edges and compute the ratio of the entire edge set, (\lambda=B_{\text{all}}/A_{\text{all}}). Since the input graph itself is connected, the complete edge set is a feasible solution, so this gives a valid starting ratio.
2. For the current value of (\lambda), assign every edge the transformed weight

[
w_e=b_e-\lambda a_e.
]

Maximizing the original ratio at this parameter is equivalent to maximizing the sum of these transformed weights.
3. Sort all edges by decreasing transformed weight. Use a DSU structure to maintain the connected components formed by edges already accepted.
4. Whenever an edge has nonnegative transformed weight, include it in the selected subgraph. Its endpoints are united in the DSU as well. A positive edge increases the transformed objective, while a zero edge can only help connectivity.
5. For a negative transformed edge, include it only if its endpoints currently belong to different DSU components. Such an edge is necessary to connect those components, and Kruskal's ordering guarantees that among all ways of connecting the components, the chosen negative edges maximize the transformed sum.
6. While selecting edges, accumulate both the original numerator and denominator, namely `sum_b` and `sum_a`. The transformed objective is also equal to `sum_b - lambda * sum_a`.
7. After all edges have been processed, compute

[
\lambda_{\text{new}}=\frac{\text{sum_b}}{\text{sum_a}}.
]

If the new value is unchanged from the current value, the transformed optimum is zero and the current ratio is optimal. Otherwise, set `lambda = lambda_new` and repeat.
8. Print the final ratio with enough decimal digits. Twelve digits after the decimal point are more than sufficient for the required (10^{-9}) absolute or relative error.

The reason the transformed subproblem works is captured by its invariant: after processing any prefix of the edges in decreasing transformed weight, the DSU represents exactly the connectivity that can be obtained using the already considered edges, while the selected set has maximum possible transformed value subject to that partial processing. All nonnegative edges are mandatory in an optimum of the transformed problem, and the negative edges that remain necessary form a maximum spanning forest between the resulting components.

For Dinkelbach's part, let (F(\lambda)) be the maximum value of (B(S)-\lambda A(S)) over connected spanning subgraphs. If (\lambda<R), some feasible solution has ratio larger than (\lambda), so (F(\lambda)>0). If (\lambda>R), every feasible solution has ratio at most (\lambda), so (F(\lambda)<0). At the optimum (R), (F(R)=0). When the oracle returns a solution with positive transformed value, its ratio is strictly larger than the current (\lambda), so the sequence moves monotonically toward the optimum. When the oracle returns zero, the current value is exactly an optimal ratio.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    __slots__ = ("parent", "size")

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a, b):
        parent = self.parent
        size = self.size

        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        return True

def solve_case(n, edges):
    total_a = 0
    total_b = 0

    for u, v, a, b in edges:
        total_a += a
        total_b += b

    # The complete graph is connected, so this is a feasible starting point.
    lam = total_b / total_a

    # Dinkelbach iterations.
    while True:
        # Reordering the edge list is intentional. Timsort can reuse existing
        # order between iterations in many instances.
        edges.sort(key=lambda e: e[3] - lam * e[2], reverse=True)

        dsu = DSU(n)

        sum_a = 0
        sum_b = 0

        for u, v, a, b in edges:
            w = b - lam * a

            if w >= 0.0:
                # Every nonnegative transformed edge belongs to an optimum.
                sum_a += a
                sum_b += b
                dsu.union(u, v)
            else:
                # Negative edges are used only when they are necessary for
                # connecting two currently different components.
                if dsu.union(u, v):
                    sum_a += a
                    sum_b += b

        new_lam = sum_b / sum_a

        # At the exact optimum, the maximizing transformed solution has
        # ratio equal to the current parameter.
        if new_lam == lam:
            return lam

        lam = new_lam

def main():
    out = []

    while True:
        line = input()
        if not line:
            break

        n, m = map(int, line.split())
        edges = []

        for _ in range(m):
            x, y, a, b = map(int, input().split())
            edges.append((x - 1, y - 1, a, b))

        ans = solve_case(n, edges)
        out.append(f"{ans:.12f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The DSU uses path compression together with union by size, so each union or find operation is effectively constant time for the problem sizes involved. The graph vertices are converted from one-based input indices to zero-based indices immediately, which keeps all internal array accesses consistent.

The first pass computes the ratio of all edges. The full edge set is connected by the input guarantee, so this is a valid feasible ratio. Starting from a feasible ratio is useful because every Dinkelbach update can only improve it toward the optimum.

Inside each iteration, the transformed weight is evaluated as `b - lam * a`. The sorting order is descending because we are solving a maximum-weight problem. The code treats `w >= 0` as an unconditional inclusion. This includes zero-weight edges, which can connect components without changing the transformed objective.

For negative edges, the DSU check is the Kruskal condition. If the endpoints are already connected, adding the edge would only decrease the transformed objective. If they are in different components, the edge is necessary to make progress toward a connected graph, so it is accepted.

The original `a` and `b` sums are accumulated rather than the floating-point transformed sum. This avoids unnecessary numerical error when calculating the next ratio. All input sums fit comfortably in Python integers, and the only floating-point operations are the transformed comparisons and the ratio updates.

The termination test uses equality of the floating-point ratio rather than an arbitrary epsilon. Every update is itself a quotient of two integer sums, and once the same optimal combinatorial solution is selected again, the computed quotient is represented by the same Python floating-point value. This avoids stopping too early merely because a chosen epsilon is larger than the remaining gap.

## Worked Examples

Only one official sample is provided, so the second trace below uses a small constructed case that exercises the need for a negative connecting edge.

### Sample 1

The graph is

```
4 4
1 2 20 10
2 3 30 10
3 4 40 10
4 1 50 10
```

The initial ratio of all four edges is (40/140=2/7).

| Iteration | Current (\lambda) | Selected edges | Sum A | Sum B | New ratio |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.285714285714 | 1-2, 2-3, 3-4 | 90 | 30 | 0.333333333333 |
| 2 | 0.333333333333 | 1-2, 2-3, 3-4 | 90 | 30 | 0.333333333333 |

At the first iteration, the transformed weights are approximately (4.286), (1.429), (-1.429), and (-4.286). The first two edges are positive and connect vertices 1, 2, and 3. Among the negative edges, `3-4` is less harmful than `4-1`, so it is chosen to connect vertex 4.

The resulting ratio is (30/90=1/3). At (\lambda=1/3), the first edge is positive, the second is exactly zero, the third is negative but needed to connect vertex 4, and the fourth is even more negative. The same set is selected, so the ratio has reached the fixed point. The output is `0.333333333333`.

### Constructed Example 2

Consider

```
3 2
1 2 1 10
2 3 100 1
```

There is only one connected spanning edge set, so both edges must be selected.

| Iteration | Current (\lambda) | Edge 1-2 | Edge 2-3 | Selected A | Selected B | New ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 11/101 | positive | negative | 101 | 11 | 11/101 |
| 2 | 11/101 | positive | zero | 101 | 11 | 11/101 |

The second edge is negative during the first transformed optimization, but it joins vertex 3 to the existing component, so DSU accepts it. This demonstrates why the transformed solution cannot simply discard every negative edge.

At the second iteration, the transformed weight of the second edge becomes exactly zero because its ratio is (1/100), while the current global ratio is (11/101). The edge is still included because connectivity requires it. The final answer is (11/101).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(Im\log m)) | Each Dinkelbach iteration sorts `m` transformed edge weights and performs (O(m\alpha(n))) DSU work |
| Space | (O(n+m)) | The edge list, DSU arrays, and sorting metadata require linear memory |

Here `I` denotes the number of Dinkelbach iterations. Each iteration is dominated by sorting the edges, while DSU operations are effectively linear. With (m\le 10^5), the graph itself is easily representable within the memory limit. The practical number of Dinkelbach iterations is small because each nonterminal iteration replaces the current ratio with the ratio of a strictly better transformed solution.

The use of Dinkelbach rather than a fixed 60 or 100 step binary search is particularly useful here because every oracle invocation requires sorting up to (10^5) edges. Reducing the number of such invocations is the main performance consideration.

## Test Cases

```python
# The test harness below mirrors the submitted algorithm.
import sys
import io

class DSU:
    __slots__ = ("parent", "size")

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a, b):
        parent = self.parent
        size = self.size

        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        return True

def solve_case(n, edges):
    total_a = sum(e[2] for e in edges)
    total_b = sum(e[3] for e in edges)

    lam = total_b / total_a

    while True:
        edges.sort(key=lambda e: e[3] - lam * e[2], reverse=True)

        dsu = DSU(n)
        sa = 0
        sb = 0

        for u, v, a, b in edges:
            w = b - lam * a

            if w >= 0.0:
                sa += a
                sb += b
                dsu.union(u, v)
            elif dsu.union(u, v):
                sa += a
                sb += b

        new_lam = sb / sa

        if new_lam == lam:
            return lam

        lam = new_lam

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    out = []

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        n, m = map(int, line.split())
        edges = []

        for _ in range(m):
            x, y, a, b = map(int, sys.stdin.readline().split())
            edges.append((x - 1, y - 1, a, b))

        out.append(f"{solve_case(n, edges):.12f}")

    sys.stdin = old_stdin
    return "\n".join(out)

# Provided sample
assert run(
    """\
4 4
1 2 20 10
2 3 30 10
3 4 40 10
4 1 50 10
"""
) == "0.333333333333", "sample 1"

# Minimum-size graph. The only edge has ratio 8/2 = 4.
assert run(
    """\
2 1
1 2 2 8
"""
) == "4.000000000000", "minimum-size case"

# A negative transformed edge is unavoidable because it is the only bridge.
assert run(
    """\
3 2
1 2 1 10
2 3 100 1
"""
) == "0.108910891089", "required negative edge"

# All edges have exactly the same ratio.
assert run(
    """\
3 3
1 2 7 7
2 3 7 7
1 3 14 14
"""
) == "1.000000000000", "equal ratios"

# Maximum n and m. All edges have ratio 1, so every connected solution has
# the same ratio. The graph contains a chain plus many parallel edges.
n = 10000
m = 100000
lines = [f"{n} {m}"]

for i in range(1, n):
    lines.append(f"{i} {i + 1} 10000000 10000000")

for _ in range(m - (n - 1)):
    lines.append("1 2 10000000 10000000")

assert run("\n".join(lines) + "\n") == "1.000000000000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2 2 8` | `4.000000000000` | Minimum number of vertices and the simplest possible connected graph |
| `3 2 / 1 2 1 10 / 2 3 100 1` | `0.108910891089` | A negative transformed edge that is mandatory for connectivity |
| Three edges with `b/a = 1` | `1.000000000000` | Equal ratios and zero transformed weights |
| `n=10000, m=100000`, all `a=b=10000000` | `1.000000000000` | Maximum stated dimensions, large integer sums, and DSU scalability |

## Edge Cases

A graph with only two vertices has exactly one required connection in the smallest valid instance. For

```
2 1
1 2 2 8
```

the only feasible set contains the single edge, so the answer is (8/2=4). The initial ratio is already 4, and the transformed weight is zero, so the algorithm immediately reaches its fixed point.

A mandatory low-ratio bridge is handled by the Kruskal part of the transformed oracle. In

```
3 2
1 2 1 10
2 3 100 1
```

the first edge has a high transformed value, while the second is negative. After accepting the first edge, vertices 1 and 2 form one component and vertex 3 is isolated. The negative edge joins those components, so DSU accepts it despite its negative contribution. The final ratio is (11/101), approximately `0.108910891089`.

Equal ratios are another useful boundary case. In

```
3 3
1 2 7 7
2 3 7 7
1 3 14 14
```

every edge has ratio 1. At (\lambda=1), every transformed weight is exactly zero. The oracle can include the edges, and the resulting ratio remains 1. The equality handling in `w >= 0.0` allows zero-weight edges to provide connectivity.

The maximum-size test contains (10^4) vertices and (10^5) edges, with every edge satisfying `a=b=10000000`. The total sums are large, but Python integers represent them exactly. Since every edge has ratio 1, the transformed weights vanish at (\lambda=1), and the answer remains exactly 1. This case also exercises the DSU and sorting code at the largest stated input dimensions.
