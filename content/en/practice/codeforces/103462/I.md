---
title: "CF 103462I - Iaom and Chicken feet"
description: "We are given a tree, meaning a connected acyclic graph on $n$ nodes with $n-1$ edges. The task is to count how many distinct subgraphs of a specific shape appear inside this tree."
date: "2026-07-03T07:02:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103462
codeforces_index: "I"
codeforces_contest_name: "The Hangzhou Normal U Qualification Trials for ZJPSC 2021"
rating: 0
weight: 103462
solve_time_s: 45
verified: true
draft: false
---

[CF 103462I - Iaom and Chicken feet](https://codeforces.com/problemset/problem/103462/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree, meaning a connected acyclic graph on $n$ nodes with $n-1$ edges. The task is to count how many distinct subgraphs of a specific shape appear inside this tree. Two subgraphs are considered identical if they consist of exactly the same set of edges, so we are effectively counting distinct edge-sets that form the required pattern.

The pattern, described informally as a “chicken feet”, corresponds to a small connected structure centered at a node and branching out into three separate edges, like a Y-shaped or three-pronged star. Each valid instance is determined entirely by choosing a central node and selecting three of its incident edges, because in a tree any such choice uniquely determines the three neighboring nodes and the edges connecting them.

The constraint $n \le 5 \cdot 10^5$ immediately rules out any approach that enumerates subgraphs or tries combinations of nodes or edges explicitly. Even iterating over all triples of edges would be far too slow, since the number of edges is linear in $n$ and combinations would explode to cubic behavior in the worst case. The solution must therefore reduce the problem to something that can be computed in linear or near-linear time, ideally by aggregating local structural information at each node.

A subtle edge case appears when the tree is small or has low-degree nodes. If $n < 4$, no node can possibly have three incident edges, so the answer must be zero. Another common pitfall is misunderstanding what constitutes a distinct subgraph: even if two stars are centered at different nodes but happen to look structurally similar, they are different if their edge sets differ.

## Approaches

A direct way to think about the problem is to attempt enumerating every possible connected subgraph and checking whether it forms the required three-pronged structure. In a tree with $n$ nodes, the number of connected subgraphs is already exponential in the worst case, since each subset of edges that keeps connectivity is a candidate. Even if we restrict ourselves only to small subgraphs of size 4 nodes, we would still need to explore combinations of edges and verify structure, which leads to at least $O(n^2)$ or worse behavior in dense-degree regions. This quickly becomes infeasible for $5 \cdot 10^5$ nodes.

The key observation is that the “chicken feet” structure is completely determined by a single central node. Once the center is fixed, the only freedom is choosing which three neighbors participate. In a tree, any three distinct edges incident to a node automatically form a valid subgraph of the required shape, because there are no cycles and each edge leads to a unique subtree. This collapses the global counting problem into a purely local combinatorial one.

For each node $v$ with degree $\deg(v)$, the number of ways to choose three incident edges is $\binom{\deg(v)}{3}$. Summing this over all nodes gives the total number of valid “chicken feet” subgraphs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of subgraphs | $O(n^2)$ to $O(2^n)$ | $O(n)$ | Too slow |
| Degree combination counting | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

The computation becomes a single pass over the tree structure.

1. Read the tree and compute the degree of every node by counting how many edges are incident to it. This is sufficient because the structure we are counting depends only on local adjacency, not on global topology.
2. Initialize an accumulator for the answer to zero. This variable will store the sum of contributions from each node.
3. For each node $v$, examine its degree $d$. If $d \ge 3$, compute the number of ways to choose three neighbors from its adjacency list, which is $d(d-1)(d-2)/6$, and add this value to the answer. Nodes with degree less than 3 contribute nothing because they cannot form the required branching structure.
4. Output the accumulated sum modulo $998244353$.

The reason this works cleanly is that every valid configuration has exactly one center. A star-shaped subgraph cannot be centered at more than one node in a tree, because the center is the only vertex with degree three inside that subgraph, while the other vertices have degree one. This uniqueness ensures that every valid structure is counted exactly once when processing its center node.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def nC3(x):
    if x < 3:
        return 0
    return x * (x - 1) * (x - 2) // 6

def main():
    n = int(input())
    deg = [0] * (n + 1)

    for _ in range(n - 1):
        u, v = map(int, input().split())
        deg[u] += 1
        deg[v] += 1

    ans = 0
    for i in range(1, n + 1):
        ans += nC3(deg[i])

    print(ans % MOD)

if __name__ == "__main__":
    main()
```

The core of the implementation is the degree array, which tracks local structure while reading edges. Each edge increments two degrees, one for each endpoint, ensuring the final array fully captures adjacency information.

The combination function uses integer arithmetic directly. Since Python handles big integers safely, there is no overflow concern, but the final result is reduced modulo $998244353$ as required.

A subtle detail is that the division by 6 is done after multiplication in integer space. This is safe because the product of three consecutive integers is always divisible by 6, so no precision issues arise.

## Worked Examples

Consider a small tree shaped like a central node connected to four leaves. Let the edges be $(1-2), (1-3), (1-4), (1-5)$.

| Node | Degree | Contribution $\binom{d}{3}$ |
| --- | --- | --- |
| 1 | 4 | 4 |
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 4 | 1 | 0 |
| 5 | 1 | 0 |

The answer is 4, corresponding to choosing any 3 of the 4 edges incident to node 1. This confirms that each selection of three leaves produces a distinct subgraph.

Now consider a path of five nodes: $1-2-3-4-5$.

| Node | Degree | Contribution |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 0 |
| 4 | 2 | 0 |
| 5 | 1 | 0 |

Every node has degree less than 3, so no valid “chicken feet” exists. The answer is zero, which matches the intuition that a path has no branching points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each edge is processed once to compute degrees, and each node is visited once to compute combinations |
| Space | $O(n)$ | The degree array stores one integer per node |

The linear structure of the solution fits comfortably within the constraints of $5 \cdot 10^5$ nodes. Both memory and time usage are proportional to the size of the input graph.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    MOD = 998244353

    n = int(input())
    deg = [0] * (n + 1)

    for _ in range(n - 1):
        u, v = map(int, input().split())
        deg[u] += 1
        deg[v] += 1

    ans = 0
    for i in range(1, n + 1):
        d = deg[i]
        if d >= 3:
            ans += d * (d - 1) * (d - 2) // 6

    return str(ans % MOD)

# sample-like case: star
assert run("""5
1 2
1 3
1 4
1 5
""") == "4"

# path case
assert run("""5
1 2
2 3
3 4
4 5
""") == "0"

# minimum n
assert run("""3
1 2
2 3
""") == "0"

# two centers
assert run("""7
1 2
1 3
1 4
2 5
2 6
2 7
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Star graph | 4 | multiple combinations at single high-degree node |
| Path graph | 0 | no valid branching nodes |
| n = 3 chain | 0 | minimum edge case |
| Two branching centers | 5 | contributions from multiple nodes |

## Edge Cases

In a star-shaped input, the algorithm assigns all structure to the center node. For example, with center node 1 connected to four others, the degree of node 1 becomes 4 and all others remain 1. The computation $\binom{4}{3} = 4$ correctly counts all distinct selections of three edges, and each corresponds to a unique edge set, so no overcounting occurs.

In a simple path, every node has degree at most 2, so the combinatorial formula never triggers. The algorithm naturally produces zero without any special casing, matching the fact that no node can serve as a branching point.

In a tree with multiple branching nodes, such as two adjacent nodes both having high degree in different subtrees, each node contributes independently. Since a valid “chicken feet” must have a unique center, there is no overlap between contributions, and summing locally remains correct.
