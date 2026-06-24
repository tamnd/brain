---
title: "CF 105244I - Sum of Path Lengths"
description: "The input describes a tree with vertices numbered from 1 to n. Every vertex except the first has exactly one parent given, which implicitly defines an undirected edge between each node i and its parent pi."
date: "2026-06-24T07:03:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105244
codeforces_index: "I"
codeforces_contest_name: "Dynamic Programming, SPbSU 2024, Training 2"
rating: 0
weight: 105244
solve_time_s: 47
verified: true
draft: false
---

[CF 105244I - Sum of Path Lengths](https://codeforces.com/problemset/problem/105244/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a tree with vertices numbered from 1 to n. Every vertex except the first has exactly one parent given, which implicitly defines an undirected edge between each node i and its parent p_i. Because each node points to a smaller-indexed parent, the structure is guaranteed to be a valid tree rooted at 1.

The task is to consider every pair of vertices u and v, including pairs where u equals v, compute the distance between them in edges, and sum all those distances. A single pair contributes zero when both endpoints are the same vertex, and contributes the number of edges on the unique simple path otherwise.

The constraint n up to 300000 forces us away from any solution that attempts to compute distances pair by pair. A naive all-pairs shortest path style idea would implicitly examine O(n^2) pairs, which is already about 9e10 operations in the worst case, far beyond any feasible limit. Even storing or iterating over all pairs is impossible in both time and memory.

A more subtle issue arises with straightforward BFS or DFS from every node. Even though each traversal is linear, repeating it n times multiplies the cost to O(n^2), which again collapses under the constraints.

Edge cases are mostly structural rather than numeric. When n equals 1, there are no edges and thus no non-zero paths, so the answer must be zero. Another corner case is a highly skewed tree, which stresses naive recursive implementations due to depth up to 300000, requiring iterative traversal or careful recursion handling.

## Approaches

A brute-force method would explicitly compute the distance between every pair of vertices. For each starting vertex u, we run a BFS or DFS to compute distances to all other vertices v, then accumulate those distances. Each traversal costs O(n), repeated for n starting points yields O(n^2) total work. With n at 300000, this would require on the order of 10^10 operations, which is not remotely viable.

The key observation is that we do not actually need individual distances. We only need the total contribution of each edge across all paths. Every simple path between two vertices crosses a specific set of edges exactly once each. This allows us to shift perspective from pairs of vertices to edges.

If we fix an edge, say between a node and its parent, removing this edge splits the tree into two connected components. Any path that goes from a node in one component to a node in the other must traverse this edge exactly once. Therefore, the number of pairs whose shortest path uses this edge is exactly the product of the sizes of the two resulting components.

This transforms the problem into computing subtree sizes. Once we root the tree at node 1, every edge connects a node to its parent, and the size of the subtree rooted at a node directly tells us how many vertices lie on one side of that edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We start by interpreting the parent array as an adjacency list. Each node i from 2 to n is connected to p_i, forming an undirected tree.

1. Build an adjacency list from the parent representation by adding an edge between i and p_i for every i from 2 to n. This allows traversal in both directions, which is necessary for computing subtree sizes cleanly.
2. Root the tree at node 1 and compute subtree sizes using a depth-first traversal. We maintain a size array where size[v] represents how many nodes exist in the subtree of v, including v itself.
3. During DFS, we visit a node and recursively compute the sizes of all its children. After processing a child c, we add size[c] into size[v]. This aggregation step is what accumulates subtree information upward.
4. After computing all subtree sizes, we evaluate each edge in the original parent list. For the edge between i and p_i, assume the subtree rooted at i is the “child side” of that edge. The number of pairs whose path crosses this edge is size[i] multiplied by n minus size[i].
5. Sum these contributions across all i from 2 to n to obtain the final answer.

The subtle point is that we never explicitly compute distances. Each edge independently contributes to the total sum, and subtree sizes fully determine how many paths use that edge.

### Why it works

Every pair of vertices has a unique simple path in a tree. That path can be decomposed into edges, and each edge is counted exactly once per pair that uses it. When an edge is removed, the tree splits into two disjoint sets of vertices. A pair contributes to the total distance sum if and only if its endpoints lie in different components of that split. The DFS computation ensures we know the size of one component for every edge, which is sufficient to count all such pairs exactly once per edge.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input().strip())
    if n == 1:
        print(0)
        return

    p = list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        par = p[i - 2]
        g[i].append(par)
        g[par].append(i)

    size = [0] * (n + 1)

    def dfs(v, parent):
        size[v] = 1
        for to in g[v]:
            if to == parent:
                continue
            dfs(to, v)
            size[v] += size[to]

    dfs(1, -1)

    ans = 0
    for i in range(2, n + 1):
        s = size[i]
        ans += s * (n - s)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by constructing an adjacency list from the parent representation. This is essential because subtree computation requires bidirectional traversal, even though the input encodes a directed parent relation.

The DFS computes subtree sizes in a single pass starting from node 1. Each node initializes its size to 1 and accumulates sizes from its children. The parent parameter prevents revisiting the previous node.

The final accumulation loop uses the fact that each edge (i, p_i) is uniquely associated with node i as the child side, so size[i] is exactly one component of that edge split.

A common implementation pitfall is using recursion without increasing the recursion limit, which will fail for a chain-like tree. Another subtlety is ensuring the parent array is indexed correctly, since it starts from p2.

## Worked Examples

Consider a simple chain of four nodes: 1 connected to 2, 2 to 3, and 3 to 4.

For this input, the parent array is `1 2 3`. The subtree sizes computed from node 1 are shown below.

| Node | Parent | Subtree size |
| --- | --- | --- |
| 1 | - | 4 |
| 2 | 1 | 3 |
| 3 | 2 | 2 |
| 4 | 3 | 1 |

Each edge contribution is computed as size[i] times n minus size[i].

For i=2, contribution is 3 × 1 = 3. For i=3, contribution is 2 × 2 = 4. For i=4, contribution is 1 × 3 = 3. The total is 10.

This matches the direct enumeration of all pairwise distances in a chain, where distances naturally accumulate across intermediate edges.

Now consider a star centered at node 1 with nodes 2, 3, 4 all directly connected to 1.

| Node | Subtree size |
| --- | --- |
| 1 | 4 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Each leaf contributes 1 × 3 = 3, so total answer is 9. This corresponds to every pair of leaves having distance 2 and every leaf-to-center pair having distance 1, matching the computed sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node and edge is processed a constant number of times during DFS and final accumulation |
| Space | O(n) | Adjacency list and subtree arrays store linear-sized structures |

The linear complexity comfortably fits within constraints for n up to 300000. The memory usage is also linear and dominated by the adjacency list, which is acceptable under a 512 MiB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

assert run("1\n") == "0", "single node"

assert run("4\n1 2 3\n") == "10", "chain of 4 nodes"

assert run("4\n1 1 1\n") == "9", "star centered at 1"

assert run("5\n1 2 3 4\n") == "20", "long chain check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | minimum size tree |
| chain of 4 | 10 | correctness of path accumulation |
| star tree | 9 | correctness of component splitting |
| chain of 5 | 20 | linear structure consistency |

## Edge Cases

For n equal to 1, the algorithm immediately returns zero before building any structure. This matches the fact that there are no pairs of distinct vertices.

In a linear chain, recursion depth reaches n. The DFS is written recursively, so increasing the recursion limit is necessary to avoid stack overflow. On the input `1 2 3 ... n-1`, subtree sizes become strictly decreasing from root to leaf, and each edge contribution is still correctly captured as size[i] times n minus size[i].

In a star-shaped tree, every node except the center has subtree size 1. Each such edge contributes n minus 1, and summing over all leaves produces the correct total without double counting, since each edge is uniquely identified by its child node in the parent representation.
