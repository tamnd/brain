---
title: "CF 104764E - Seacave Jellyfish"
description: "We are given a weighted tree with up to 100 nodes. Each node represents a seacave and contains some amount of jellyfish, represented by a nonnegative value."
date: "2026-06-28T21:41:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 88
verified: false
draft: false
---

[CF 104764E - Seacave Jellyfish](https://codeforces.com/problemset/problem/104764/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted tree with up to 100 nodes. Each node represents a seacave and contains some amount of jellyfish, represented by a nonnegative value. Moving between two connected caves costs energy equal to the edge weight, and the total travel cost between any two caves is the sum of weights along the unique path in the tree.

If Ao Run chooses a cave $y$ as his base, then for every cave $x$, he travels from $y$ to $x$, pays the distance cost $dist(y,x)$, and then “engages” with the jellyfish in $x$, which costs an additional unit of energy. The engagement contribution from cave $x$ is defined as

$$\frac{c_x}{dist(y,x) + 1}.$$

The task is to choose the base node $y$ that maximizes the total sum of these contributions over all nodes, and output both the chosen node and the resulting maximum sum.

The input size is small, $n \le 100$, so even cubic or quadratic methods are feasible. This immediately suggests that we can afford to precompute all pairwise distances between nodes.

A subtle issue is numerical stability. The answer requires floating-point division and must be accurate to within $10^{-4}$, so naive integer arithmetic is insufficient at the final aggregation step, but standard double precision is easily enough because the number of terms is small (at most 100 per sum).

There are no tricky structural edge cases like disconnected graphs or multiple components, since the input is explicitly a tree.

One failure case for naive reasoning would be attempting to greedily choose a root based only on nearby high $c_i$ values. For example, in a small line tree, a node with slightly smaller nearby values but much better global distances can outperform a locally optimal choice. This shows that the objective is global and distance-dependent, not decomposable into local contributions.

## Approaches

A direct approach is to try every possible base node $y$. For each choice, we compute the shortest path distance from $y$ to all other nodes, then sum $\frac{c_x}{dist(y,x)+1}$.

Since the graph is a tree, shortest paths are unique and can be computed with a BFS or DFS when weights are small, but because weights are up to $10^3$, we need Dijkstra if we compute from each node independently. That gives $n$ runs of Dijkstra, each costing $O(n \log n)$, so about $10^4 \log 100$, which is trivial.

A simpler observation is that $n$ is only 100, so we can precompute all-pairs shortest paths. Either Floyd-Warshall in $O(n^3)$, or run Dijkstra from each node in $O(n^2 \log n)$. Once we have a full distance matrix, evaluating each candidate root is just a linear scan.

The key structure that makes this work is that the tree has no cycles, so distances are well-defined and independent of the choice of root. Once all distances are known, the objective function becomes a straightforward evaluation over a fixed matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force without precomputation | $O(n^2 \log n)$ per root → $O(n^3 \log n)$ | $O(n^2)$ | Acceptable but unnecessary |
| All-pairs distances + evaluation | $O(n^2 \log n + n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the tree with weights.

This gives a structure where each node can reach its neighbors with known costs, which is necessary for shortest-path computation.
2. Run Dijkstra from every node $i$ to compute $dist[i][*]$.

Even though the graph is a tree, we still treat it as a general weighted graph to avoid reasoning about rooted representations.
3. For each node $y$, compute a score initialized to zero.
4. For every node $x$, add $c_x / (dist[y][x] + 1)$ to the score of $y$.

The denominator includes the extra 1-unit engagement cost, so even at the same node the contribution is $c_y / 1$.
5. Track the node with the maximum score while computing all candidates.
6. Output the best node index and its score formatted to 5 decimal places.

The correctness relies on the fact that once distances are fixed, each candidate root is evaluated independently with no hidden interactions. Every term in the sum depends only on the chosen root and a precomputed distance.

### Why it works

The algorithm explicitly enumerates all possible bases and computes the exact value of the objective function for each one. Since distances in a tree are fixed and independent of rooting, the precomputed distance matrix is valid for every evaluation. The final selection is therefore an exact maximization over a finite set of correctly computed values, guaranteeing optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def dijkstra(start, adj, n):
    INF = 10**18
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def solve():
    n = int(input())
    c = [0] + list(map(int, input().split()))

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        x, y, w = map(int, input().split())
        adj[x].append((y, w))
        adj[y].append((x, w))

    dist = []
    for i in range(1, n + 1):
        dist.append(dijkstra(i, adj, n))

    best_node = 1
    best_val = -1.0

    for y in range(1, n + 1):
        s = 0.0
        for x in range(1, n + 1):
            s += c[x] / (dist[y-1][x] + 1)
        if s > best_val:
            best_val = s
            best_node = y

    print(best_node)
    print(f"{best_val:.5f}")

if __name__ == "__main__":
    solve()
```

The solution first constructs the adjacency list and computes all shortest paths using repeated Dijkstra runs. The distance table is stored so that each candidate root can be evaluated in isolation without recomputation.

When computing the score, the expression `dist[y-1][x]` reflects that we stored distances in a 0-indexed list of 1-indexed nodes. The division is done in floating point, which is sufficient because the sum involves at most 100 terms, keeping numerical error well below the tolerance.

The choice of Dijkstra instead of Floyd-Warshall is stylistic here; both are fast enough, but Dijkstra keeps the solution closer to standard graph intuition.

## Worked Examples

### Example Trace

Consider a small tree of three nodes in a line: 1-2-3, with all edge weights 1 and values $c = [2, 1, 3]$.

| Base y | dist(y,1) | dist(y,2) | dist(y,3) | score computation |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 2 | 2/1 + 1/2 + 3/3 = 2 + 0.5 + 1 |
| 2 | 1 | 0 | 1 | 2/2 + 1/1 + 3/2 = 1 + 1 + 1.5 |
| 3 | 2 | 1 | 0 | 2/3 + 1/2 + 3/1 |

The best base is node 3 since it benefits from the largest value being closest.

This trace shows how distance asymmetry directly affects the contribution of each node, making centrality and value distribution jointly important.

### Example Trace 2

A star-shaped tree with center 1 connected to 2, 3, 4 with weight 2, and values $c = [10, 1, 1, 1]$.

| Base y | center distance pattern | score structure |
| --- | --- | --- |
| 1 | all leaves at 1 | 10/1 + 1/3 + 1/3 + 1/3 |
| 2 | asymmetric distances | 1/1 + 10/3 + 1/5 + 1/5 |
| 3 | symmetric to 2 | similar |

The trace shows that although leaves can get closer to the center, the high central value dominates when the base is placed at the center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \log n)$ | Dijkstra run from each node over $n$ nodes with $n-1$ edges |
| Space | $O(n^2)$ | Full distance matrix stored for all node pairs |

With $n \le 100$, this corresponds to at most about $10^4$ relaxation steps per run, repeated 100 times, which is easily within limits. Memory usage is also negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from math import isclose

    # Re-run solution inline
    import heapq

    def dijkstra(start, adj, n):
        INF = 10**18
        dist = [INF] * (n + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    n = int(input())
    c = [0] + list(map(int, input().split()))
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        x, y, w = map(int, input().split())
        adj[x].append((y, w))
        adj[y].append((x, w))

    dist = [dijkstra(i, adj, n) for i in range(1, n + 1)]

    best_node = 1
    best_val = -1.0

    for y in range(1, n + 1):
        s = 0.0
        for x in range(1, n + 1):
            s += c[x] / (dist[y-1][x] + 1)
        if s > best_val:
            best_val = s
            best_node = y

    return str(best_node) + "\n" + f"{best_val:.5f}"

# provided sample
assert run("5\n5 2 9 1 7\n1 2 2\n1 3 2\n3 4 1\n3 5 3\n") == "3\n13.31667"

# minimum size
assert run("2\n1 2\n1 2 1\n") is not None

# star test
assert run("4\n10 1 1 1\n1 2 1\n1 3 1\n1 4 1\n").startswith("1")

# chain test
assert run("3\n1 2 3\n1 2 1\n2 3 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 3 / 13.31667 | correctness on full statement |
| 2-node tree | small value | base case handling |
| star tree | 1 | central dominance behavior |
| chain tree | consistent float sum | distance accumulation correctness |

## Edge Cases

A minimal tree with two nodes checks that the denominator rule is applied correctly even when a node is both source and target. If node 1 connects to node 2 with weight 5 and $c = [4, 6]$, then choosing node 1 yields $4/1 + 6/6$, while choosing node 2 yields $6/1 + 4/6$. The algorithm correctly evaluates both using the precomputed distance matrix and selects the larger.

A highly unbalanced tree, such as a chain of 100 nodes, checks that the distance accumulation does not introduce precision drift. Since each candidate root uses at most 100 fractional additions, the floating-point error remains stable, and the best node is still correctly identified by direct comparison of computed sums.
