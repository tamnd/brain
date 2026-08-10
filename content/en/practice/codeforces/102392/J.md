---
title: "CF 102392J - Graph and Cycles"
description: "We have a complete undirected graph on an odd number (n) of vertices. Every one of its (frac{n(n-1)}2) edges has a positive weight. We must partition all edges into cycle-arrays."
date: "2026-08-10T19:37:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102392
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC Southeastern European Regional Programming Contest (SEERC 2019)"
rating: 0
weight: 102392
solve_time_s: 83
verified: true
draft: false
---

[CF 102392J - Graph and Cycles](https://codeforces.com/problemset/problem/102392/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete undirected graph on an odd number (n) of vertices. Every one of its (\frac{n(n-1)}2) edges has a positive weight.

We must partition all edges into cycle-arrays. Consecutive edges in one array must share a vertex, and the two transitions around every edge must use different endpoints, so the array describes a closed trail through the graph. A cycle-array is allowed to revisit a vertex. What matters is that its edges are arranged cyclically and each edge is adjacent to one edge through each of its endpoints.

For two consecutive edges (e_i,e_{i+1}), the contribution is the larger of their weights. The price of one cycle-array is the sum of these contributions around the whole array. The required output is the minimum possible total price over a partition of every graph edge into such arrays.

The oddness of (n) is the structural reason the problem becomes simple. Every vertex has degree (n-1), which is even. Since an edge entering a vertex in a cycle-array must be paired with exactly one edge leaving that vertex, all edges incident to a vertex can be divided into pairs.

There are at most (999) vertices, but the graph is dense. For (n=999), it contains

[
\frac{999\cdot998}{2}=498501
]

edges. This immediately rules out algorithms that enumerate cycles, cycle decompositions, or arbitrary pairings. Even a single cyclic ordering of all edges has roughly (498500!/2) possibilities. The intended solution needs to exploit the fact that the objective can be separated by vertices.

The weights can be as large as (10^9), so the answer does not fit in a 32-bit signed integer. In the largest all-equal instance the answer is (498501), and with larger individual weights it can be on the order of (10^{15}). Python integers handle this automatically, while a C++ implementation would need `long long`.

One small edge case is (n=3). Every vertex has exactly two incident edges, so there is only one possible pair at each vertex. For example,

```
3
1 2 1
2 3 1
1 3 1
```

has answer (3). A solution that assumes every vertex has at least four incident edges or that performs an incorrect pairing loop can miss this case.

Another important case is equal weights. For

```
3
1 2 5
2 3 5
1 3 5
```

the answer is (15). Every adjacency costs (5), and the triangle has three adjacencies. A careless implementation that tries to distinguish edges by weight can accidentally discard equal-weight edges or count only one of them.

A third case concerns large weights. For

```
3
1 2 1000000000
2 3 1000000000
1 3 1000000000
```

the answer is (3000000000). Using a 32-bit integer would overflow. The algorithm itself only performs additions, so the implementation should simply use an integer type capable of holding the final sum.

## Approaches

A direct approach would try to enumerate possible cycle-splits, calculate the price of each one, and keep the minimum. This is correct because every valid split would eventually be considered. The problem is the number of possibilities. If (m=\frac{n(n-1)}2), then even considering only one cycle containing all (m) edges gives ((m-1)!/2) distinct cyclic orderings in an undirected setting. For (n=999), (m=498501), so this is far beyond anything executable. Enumerating several cycles or trying all pairings at vertices is even worse.

The useful observation is that the price can be assigned locally to vertices.

Consider one edge (e=(u,v)). Inside its cycle-array, it is compared with exactly one neighboring edge through (u), and exactly one neighboring edge through (v). Thus, at vertex (u), the incident edges are divided into pairs, with each pair contributing the maximum of its two weights. Every price contribution in the entire cycle-split belongs to exactly one such vertex.

So the global problem becomes a collection of independent local problems: at every vertex, pair its (n-1) incident edges as cheaply as possible.

Suppose the incident weights at one vertex, sorted from largest to smallest, are

[
w_1\ge w_2\ge w_3\ge w_4\ge\cdots\ge w_{n-2}\ge w_{n-1}.
]

There are (\frac{n-1}{2}) pairs. To minimize the sum of pairwise maxima, the two largest values should be paired, then the next two largest, and so on:

[
(w_1,w_2),(w_3,w_4),\ldots
]

The contribution is consequently

[
w_1+w_3+w_5+\cdots+w_{n-2}.
]

Why is this pairing optimal? The largest element must be the maximum of some pair, so every pairing pays at least (w_1). After pairing it with the second largest value, the remaining problem has the same form on the remaining values. Equivalently, pairing a large value with a small value wastes that small value, because the large value already determines the pair's cost. Pairing the values consecutively from largest to smallest minimizes the number of large values that become pair maxima.

The remaining question is whether independently choosing these optimal pairs at every vertex can actually produce valid cycle-arrays. It can. Regard each chosen pair as a transition telling us which edge follows which at that vertex. Starting from any unused edge, follow the paired edge at its current endpoint. Every time we arrive at a vertex, exactly one pair there is partially used, so there is a unique edge that completes that pair. Continuing this process eventually returns to the starting point because there are finitely many edges and every edge has exactly two paired endpoints. The resulting closed trail is a valid cycle-array. Once it is finished, start again from another unused edge.

The resulting construction realizes every locally optimal pair, so the sum of the local minima is not merely a lower bound. It is achievable and is exactly the global optimum. This is the central reduction used by the official editorial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | At least (O(m!)), where (m=\frac{n(n-1)}2) | Exponential/factorial search state | Too slow |
| Optimal | (O(n^2\log n)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Read all (m=\frac{n(n-1)}2) edges and store each edge as its two endpoints and its weight. The graph is complete, so every vertex will eventually receive exactly (n-1) incident edges.
2. For every vertex, collect the weights of all incident edges. Since (n) is odd, (n-1) is even, so these weights can be divided into pairs.
3. Sort the incident weights in descending order. Pair positions (0) and (1), positions (2) and (3), positions (4) and (5), and so forth. The maximum of each pair is simply the first element of that pair.
4. Add the weights at positions (0,2,4,\ldots) to the answer. This computes the minimum possible contribution of that vertex independently of every other vertex.
5. Repeat this for every vertex. Every adjacency of two consecutive edges in every cycle-array occurs at exactly one vertex, so summing these local contributions counts every term of the global price exactly once.

The key invariant is that every valid cycle-split induces a pairing of the incident edges at every vertex, while our sorted pairing gives the minimum possible cost for that vertex. The independently chosen pairings can be followed as closed trails, so they correspond to a valid cycle-split. Thus no solution can cost less than our sum, and a solution achieving exactly that sum exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    edges = n * (n - 1) // 2

    incident = [[] for _ in range(n)]

    for _ in range(edges):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        incident[u].append(w)
        incident[v].append(w)

    ans = 0

    for v in range(n):
        incident[v].sort(reverse=True)
        ans += sum(incident[v][i] for i in range(0, n - 1, 2))

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop reads exactly (\frac{n(n-1)}2) edges, which is the number of edges in a complete graph. Each weight is appended to the lists of both endpoints because that edge participates in the local pairing at both vertices.

For every vertex, the list has exactly (n-1) elements. The range `range(0, n - 1, 2)` visits indices (0,2,4,\ldots,n-3). Each visited element is the larger element of one optimal pair, so adding these values gives that vertex's minimum contribution.

The sorting is done independently for every vertex. Since each vertex has at most (998) incident edges, this is easily fast enough. The input itself already contains (\Theta(n^2)) edges, so quadratic-scale processing is unavoidable.

No explicit cycle construction is needed. The proof shows that the optimal local pairings are simultaneously realizable as cycle-arrays, while the answer only asks for their total price. Avoiding the construction saves both time and implementation complexity.

Python's integer type also avoids overflow when the answer becomes larger than (2^{31}-1).

## Worked Examples

### Sample 1

The graph is a triangle and every edge has weight (1).

| Vertex | Sorted incident weights | Optimal pairs | Contribution |
| --- | --- | --- | --- |
| 1 | (1,1) | ((1,1)) | 1 |
| 2 | (1,1) | ((1,1)) | 1 |
| 3 | (1,1) | ((1,1)) | 1 |

The total is (1+1+1=3), matching the only possible cycle-array.

The trace demonstrates the (n=3) boundary case. Each vertex has exactly one pair, and the sum of the three local contributions is exactly the price of the triangle.

### Sample 2

For the ten edges, the incident weights become:

| Vertex | Sorted incident weights | Pair maxima | Contribution |
| --- | --- | --- | --- |
| 1 | (4,4,4,3) | (4,4) | 8 |
| 2 | (4,4,3,2) | (4,3) | 7 |
| 3 | (4,3,2,2) | (4,2) | 6 |
| 4 | (4,3,2,2) | (4,2) | 6 |
| 5 | (4,4,4,2) | (4,4) | 8 |

The final answer is

[
8+7+6+6+8=35.
]

The sample's optimal split has prices (12) and (23), giving the same total (35). The local calculation reaches that value without needing to discover those two cycles explicitly.

This trace demonstrates the central invariant: every transition between two consecutive edges is charged to their shared vertex, so adding the optimal pair maxima at all five vertices accounts for the entire cycle-split price.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2\log n)) | There are (n) incident lists, each of size (n-1), and each is sorted |
| Space | (O(n^2)) | All (n(n-1)/2) edge weights are stored twice, once for each endpoint |

With (n\le999), there are at most (498501) graph edges and each incident list contains at most (998) values. The total sorting work is comfortably within the limits, while the memory usage is proportional to the dense input itself.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    edges = n * (n - 1) // 2

    incident = [[] for _ in range(n)]

    for _ in range(edges):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        incident[u].append(w)
        incident[v].append(w)

    ans = 0

    for v in range(n):
        incident[v].sort(reverse=True)
        ans += sum(incident[v][i] for i in range(0, n - 1, 2))

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        old_input = globals()["input"]
        globals()["input"] = sys.stdin.readline

        # solve() uses its own local input binding, so changing stdin is enough.
        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        try:
            solve()
        finally:
            sys.stdout = old_stdout

        return output.getvalue().strip()
    finally:
        globals()["input"] = old_input
        sys.stdin = old_stdin

# Sample 1
assert run(
    """3
1 2 1
2 3 1
1 3 1
"""
) == "3", "sample 1"

# Sample 2
assert run(
    """5
4 5 4
1 3 4
1 2 4
3 2 3
3 5 2
1 4 3
4 2 2
1 5 4
5 2 4
3 4 2
"""
) == "35", "sample 2"

# Minimum size, with different weights.
assert run(
    """3
1 2 1
2 3 2
1 3 3
"""
) == "8", "n=3 with non-equal weights"

# All weights equal.
assert run(
    """5
1 2 7
1 3 7
1 4 7
1 5 7
2 3 7
2 4 7
2 5 7
3 4 7
3 5 7
4 5 7
"""
) == "70", "all weights equal"

# Maximum edge weight boundary.
assert run(
    """3
1 2 1000000000
2 3 1000000000
1 3 1000000000
"""
) == "3000000000", "maximum weight"

# Maximum n, generated compactly.
n = 999
parts = [str(n)]
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        parts.append(f"{u} {v} 1")

max_case = "\n".join(parts) + "\n"
assert run(max_case) == "498501", "maximum n, all weights equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=3), weights (1,2,3) | 8 | Minimum graph size and unequal weights |
| (K_5), every weight 7 | 70 | Equal values and repeated pair maxima |
| (K_3), every weight (10^9) | 3000000000 | Integer-size boundary |
| (K_{999}), every weight 1 | 498501 | Maximum input size and quadratic processing |

## Edge Cases

For (n=3), every vertex has degree (2). Consider

```
3
1 2 1
2 3 2
1 3 3
```

At vertex (1), the weights are (3,1), contributing (3). At vertex (2), they are (2,1), contributing (2). At vertex (3), they are (3,2), contributing (3). The answer is (8). The algorithm handles this naturally because the only processed index is (0) at every vertex.

For equal weights, consider the complete graph on five vertices with every edge equal to (7). Each vertex has four incident edges, so it forms two pairs and each pair contributes (7). Every vertex contributes (14), giving (5\cdot14=70). The identity of the edges inside each pair does not matter because all weights are equal.

For the maximum weight boundary,

```
3
1 2 1000000000
2 3 1000000000
1 3 1000000000
```

each of the three vertices contributes (10^9), so the answer is (3\cdot10^9=3000000000). There is no overflow in Python, and the calculation does not depend on the magnitude of the weights except for the final integer sum.

For the largest graph, (n=999), every vertex has (998) incident edges. If every weight is (1), every one of the (499) local pairs contributes (1), so one vertex contributes (499). Across (999) vertices the answer is (999\cdot499=498501), which is also exactly the number of graph edges. The implementation processes all (498501) input edges and performs the required local sorts without attempting to construct or enumerate the enormous set of possible cycle-splits.
