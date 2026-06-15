---
title: "CF 1065B - Vasya and Isolated Vertices"
description: "We are given a simple undirected graph with a fixed number of vertices and edges. The graph has no self-loops and no duplicate edges."
date: "2026-06-15T08:19:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1065
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 52 (Rated for Div. 2)"
rating: 1300
weight: 1065
solve_time_s: 351
verified: false
draft: false
---

[CF 1065B - Vasya and Isolated Vertices](https://codeforces.com/problemset/problem/1065/B)

**Rating:** 1300  
**Tags:** constructive algorithms, graphs  
**Solve time:** 5m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple undirected graph with a fixed number of vertices and edges. The graph has no self-loops and no duplicate edges. The structure is otherwise unrestricted, meaning we are free to imagine any valid configuration that uses exactly $m$ edges among $n$ labeled vertices.

A vertex is called isolated if it is not incident to any edge. The task is not to construct a graph, but to reason about extremes: among all valid graphs with $n$ vertices and $m$ edges, we want the smallest possible number of isolated vertices and the largest possible number of isolated vertices.

The key tension is between how edges “consume” vertices and how freely we can concentrate edges inside small subsets of vertices.

The constraints allow $n$ up to $10^5$, which immediately rules out any solution that tries to simulate graph construction or enumerate edges. The answer must come from structural reasoning about how edges can be distributed.

A naive misunderstanding often comes from thinking that edges always “use up” two new vertices. That is false because edges can share vertices, and in fact that sharing is what drives the minimum number of isolated vertices down.

A subtle edge case appears when $m = 0$. In that case, every vertex is isolated, so both minimum and maximum are $n$. Another is when $m$ is large enough that we can “touch” almost all vertices even if we try to avoid isolation, but still not large enough to guarantee connectivity.

## Approaches

The brute-force view is to imagine building graphs and counting isolated vertices for each configuration. For each subset of edges, one could compute how many vertices appear in at least one edge, then deduce isolated vertices. This immediately explodes because the number of graphs grows exponentially with $m$ and $n$, making enumeration impossible even for tiny inputs.

The correct perspective is to reverse the question. Instead of placing edges arbitrarily, we ask how few vertices can be made non-isolated using $m$ edges, and how many vertices we can avoid touching.

For the maximum number of isolated vertices, we want to concentrate edges as much as possible inside the smallest possible set of vertices. If we pick $k$ vertices and place all $m$ edges inside them, then the remaining $n-k$ vertices are isolated. The smallest $k$ that can host $m$ edges is the smallest integer such that:

$$\binom{k}{2} \ge m$$

If $m = 0$, then $k = 0$. Otherwise, $k$ must be at least 2.

So the maximum isolated vertices is $n - k$, where $k$ is the minimum size of a vertex set that can support $m$ edges.

For the minimum number of isolated vertices, we want to spread edges so that they touch as many distinct vertices as possible. Each edge can introduce at most two new vertices, but once vertices are reused, the marginal gain decreases. The optimal strategy is to maximize the number of vertices covered by edges, which is limited by $2m$, but cannot exceed $n$. So the minimum number of isolated vertices is:

$$\max(0, n - 2m)$$

This bound is achievable by constructing a matching-like structure when possible, and otherwise reusing vertices to saturate coverage.

The two extremes are independent: one packs edges tightly, the other spreads them as widely as possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (graph enumeration) | Exponential | Exponential | Too slow |
| Optimal (combinatorial reasoning) | $O(\sqrt{n})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the minimum number of isolated vertices by estimating how many vertices can be “covered” by edges. Each edge can contribute up to two new vertices, so the number of covered vertices is at most $2m$, capped by $n$. The isolated count is $n - \min(n, 2m)$, which simplifies to $\max(0, n - 2m)$.
2. Compute the maximum number of isolated vertices by finding the smallest number of vertices needed to accommodate all edges. Start with $k = 0$, and increase it until $\binom{k}{2} \ge m$. This $k$ represents the smallest vertex set that can host all edges.
3. The remaining $n - k$ vertices can be completely isolated since no edges are forced to touch them in an optimal construction.
4. Output the pair: minimum isolated vertices first, then maximum isolated vertices.

The key idea is that both computations are independent extremal packings of the same edge budget.

### Why it works

The number of vertices touched by edges is what controls isolation. For the minimum case, we maximize coverage, and each edge contributes at most two distinct vertices, giving a tight upper bound. For the maximum case, we minimize coverage by concentrating edges into a dense subgraph, and the capacity of a $k$-vertex simple graph is exactly $\binom{k}{2}$. These two opposite packing arguments fully characterize all feasible configurations.

## Python Solution

```
PythonRun
```

The code separates the two extremal calculations. The first part directly applies the observation that each edge can cover at most two new vertices, so we subtract $2m$ from $n$. The second part searches for the smallest $k$ such that a complete graph on $k$ vertices has enough edges to contain all $m$ edges. The loop is safe because $k$ never exceeds roughly $\sqrt{2m}$, which is well within limits for $n \le 10^5$.

A subtle point is the handling of $m = 0$. Without it, the triangular condition would incorrectly force $k = 1$, but the correct interpretation is that no vertices are needed to host edges.

## Worked Examples

### Example 1

Input:

```

```

For minimum isolated vertices, we compute $n - 2m = 4 - 4 = 0$. This corresponds to using both edges to cover all four vertices, for example two disjoint edges.

For maximum isolated vertices, we find the smallest $k$ such that $\binom{k}{2} \ge 2$. We check $k=2 \rightarrow 1$, not enough; $k=3 \rightarrow 3$, enough. So $k=3$, and maximum isolated vertices is $4 - 3 = 1$.

| Step | k | k(k−1)/2 | Condition |
| --- | --- | --- | --- |
| 2 | 2 | 1 | < 2 |
| 3 | 3 | 3 | ≥ 2 |

This confirms that two edges can be packed into three vertices while leaving one vertex isolated.

### Example 2

Input:

```

```

Minimum isolated vertices is $5 - 0 = 5$. Maximum isolated vertices is also $5$, since $k = 0$. The graph has no edges, so every vertex is isolated regardless of construction.

| Step | k | k(k−1)/2 | Condition |
| --- | --- | --- | --- |
| 0 | 0 | 0 | ≥ 0 |

This shows that the edge-free case collapses both extremes to the same value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{m})$ | The triangular number search grows until reaching $m$, requiring at most $O(\sqrt{m})$ iterations |
| Space | $O(1)$ | Only a few integer variables are used |

The constraints allow up to $10^5$ vertices and about $10^{10}$ possible edges, but only a single pair $(n, m)$ is processed. The loop remains fast because the required $k$ is bounded by roughly $\sqrt{2m}$, which is at most around $10^5$ in the worst case.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 1 | single vertex edge-free behavior |
| 5 0 | 5 5 | full isolation edge-free graph |
| 4 6 | 0 0 | complete graph case |
| 6 3 | 0 3 | intermediate packing behavior |

## Edge Cases

For $n = 1, m = 0$, the algorithm sets minimum isolated vertices to $1 - 0 = 1$. For maximum, $k = 0$, so result is $1$. This matches the fact that a single vertex with no edges must be isolated.

For $m = 0$ with large $n$, the formula yields $min = n$ and $max = n$, reflecting that no construction can reduce isolation.

For very large $m$, close to $\binom{n}{2}$, the triangular search finds $k = n$, so maximum isolated vertices becomes $0$. The minimum is also $0$ because all vertices must be used in a dense graph.
