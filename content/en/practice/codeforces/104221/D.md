---
title: "CF 104221D - \u041a\u0430\u0440\u0438\u043c \u0438 \u0434\u043e\u0440\u043e\u0433\u0438"
description: "We are given an undirected simple graph with $n$ intersections and $m$ roads. Each road connects two distinct intersections, and between any pair of intersections there is at most one road."
date: "2026-07-01T23:46:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104221
codeforces_index: "D"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104221
solve_time_s: 74
verified: true
draft: false
---

[CF 104221D - \u041a\u0430\u0440\u0438\u043c \u0438 \u0434\u043e\u0440\u043e\u0433\u0438](https://codeforces.com/problemset/problem/104221/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected simple graph with $n$ intersections and $m$ roads. Each road connects two distinct intersections, and between any pair of intersections there is at most one road. The task is to assign a direction to every road so that after orientation, it becomes impossible to start at some intersection and follow directed roads forever in a cycle.

In graph terms, we must convert the undirected graph into a directed graph that has no directed cycles. We are free to choose the direction of each edge independently, but the final directed structure must be acyclic. If multiple valid orientations exist, any one of them can be printed.

The constraints are large: up to $2 \cdot 10^5$ vertices and edges. This immediately rules out anything quadratic such as trying all permutations of vertices or repeatedly simulating cycle formation. We need an $O(n + m)$ or $O(m \log n)$ construction.

A subtle point is that the input graph itself may contain cycles, and even many of them. A naive assumption that “we must first break cycles” leads to unnecessary complexity. The real task is not deleting edges or modifying structure, but purely assigning directions.

A typical failure case comes from attempting local greedy orientation without a global rule. For example, in a triangle $1-2-3-1$, if we orient $1 \to 2$, $2 \to 3$, and $3 \to 1$, we immediately create a directed cycle. A greedy rule based only on local consistency can easily fall into such contradictions if it does not enforce a global ordering.

Another pitfall is assuming we need to detect cycles in the undirected graph first. That is irrelevant, since even graphs full of cycles can still be oriented into a DAG.

## Approaches

The brute-force mindset would be to try to orient edges one by one and check whether a directed cycle appears after each assignment. Each check requires a cycle detection in a directed graph, which is $O(n + m)$, and we do it $m$ times, leading to $O(m(n + m))$. With $m$ up to $2 \cdot 10^5$, this is far too slow.

The key structural insight is that a directed graph is acyclic exactly when there exists a global ordering of vertices such that every edge points forward in that order. This converts the problem from “avoiding cycles dynamically” into “choosing a consistent ranking of vertices.”

Once we accept that we only need a total order, the construction becomes trivial. We assign any strict ordering to vertices, for example their labels $1 < 2 < \dots < n$. Then for every undirected edge $(u, v)$, we orient it from the smaller label to the larger label. Any directed cycle would imply a strictly increasing sequence of labels that eventually returns to the start, which is impossible.

This works regardless of how dense or cyclic the original graph is, because the orientation ignores structure and relies only on a global ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (incremental cycle checking) | $O(m(n+m))$ | $O(n+m)$ | Too slow |
| Global ordering orientation | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

We construct a directed acyclic graph by enforcing a consistent vertex ordering.

1. Assign each vertex a fixed rank equal to its index from $1$ to $n$. This creates a strict total order over all vertices. The reason for introducing this order is that any acyclic orientation must be compatible with some ordering, so we directly build one.
2. Iterate through all edges as they are given in the input. For each edge $(u, v)$, compare the ranks of $u$ and $v$.
3. If $u < v$, orient the edge as $u \to v$. Otherwise orient it as $v \to u$. This ensures every edge is directed from a smaller-ranked vertex to a larger-ranked one.
4. Output all oriented edges in the same order they were read.

### Why it works

Assume for contradiction that a directed cycle exists after orientation. Along this cycle, every edge must go from a smaller index to a larger index because of the construction rule. This implies that as we traverse the cycle, vertex indices strictly increase at every step. A strict increase cannot return to the starting vertex, since that would require the starting index to be both smallest and largest in the cycle simultaneously. Hence no directed cycle can exist, and the graph is a DAG.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        if u < v:
            edges.append((u, v))
        else:
            edges.append((v, u))

    out = []
    for u, v in edges:
        out.append(f"{u} {v}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation directly encodes the ordering idea. Each edge is normalized immediately so that its direction follows the natural numeric order of vertices. There is no need for adjacency lists, DFS, or cycle detection, since the construction itself guarantees acyclicity.

A common mistake would be storing edges and later deciding orientation inconsistently. The important property is that the same global ordering is applied uniformly to every edge, without exceptions.

## Worked Examples

### Example 1

Input:

```
4 4
1 2
3 2
2 4
4 3
```

We process edges in order and always orient from smaller to larger.

| Edge | Compare | Direction |
| --- | --- | --- |
| 1 2 | 1 < 2 | 1 → 2 |
| 3 2 | 2 < 3 | 2 → 3 |
| 2 4 | 2 < 4 | 2 → 4 |
| 4 3 | 3 < 4 | 3 → 4 |

Output:

```
1 2
2 3
2 4
3 4
```

This trace shows that even though the original graph contains cycles, the orientation eliminates all backward edges relative to the global order.

### Example 2

Input:

```
3 3
1 3
2 3
1 2
```

| Edge | Compare | Direction |
| --- | --- | --- |
| 1 3 | 1 < 3 | 1 → 3 |
| 2 3 | 2 < 3 | 2 → 3 |
| 1 2 | 1 < 2 | 1 → 2 |

Output:

```
1 3
2 3
1 2
```

This example highlights that the resulting directed graph is acyclic even though the original graph is a triangle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each edge is processed once with constant-time comparison and output formatting |
| Space | $O(m)$ | We store the list of edges before printing |

The solution fits easily within constraints since both $n$ and $m$ are at most $2 \cdot 10^5$, and the algorithm performs only linear work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        if u < v:
            edges.append((u, v))
        else:
            edges.append((v, u))
    return "\n".join(f"{u} {v}" for u, v in edges)

# provided sample
assert run("""4 4
1 2
3 2
2 4
4 3
""") == """1 2
2 3
2 4
3 4"""

# chain
assert run("""3 2
1 2
2 3
""") == """1 2
2 3"""

# reversed input order
assert run("""3 3
3 2
2 1
3 1
""") == """2 3
1 2
1 3"""

# complete triangle
assert run("""3 3
1 2
2 3
3 1
""") == """1 2
2 3
1 3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | linear orientation | basic correctness |
| reversed edges | consistent ordering | symmetry handling |
| triangle | acyclic result | cycle elimination |

## Edge Cases

A dense cyclic graph such as a complete graph is handled correctly because every edge is still oriented according to the same global numeric order. For instance, in a fully connected triple, every edge becomes consistent with $1 < 2 < 3$, producing a strict hierarchy rather than a cycle.

A single-edge graph trivially works because the comparison immediately assigns direction without any dependency on other edges. Even in this minimal case, the invariant that all edges respect the same ordering remains valid.

Graphs where input edges are given in arbitrary order do not affect correctness because orientation is independent of input sequence. Each edge is treated in isolation, but always under the same global rule.
