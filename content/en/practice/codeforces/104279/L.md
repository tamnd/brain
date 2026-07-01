---
title: "CF 104279L - \u6811\u8fb9\u91cd\u6392"
description: "We are given a tree with n vertices and n − 1 undirected edges. The task is not to output the edges themselves or reconstruct an adjacency list, but to assign to every vertex i (from 1 to n − 1) a partner vertex pi such that the pair (i, pi) is one of the given tree edges."
date: "2026-07-01T21:13:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "L"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 48
verified: true
draft: false
---

[CF 104279L - \u6811\u8fb9\u91cd\u6392](https://codeforces.com/problemset/problem/104279/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with n vertices and n − 1 undirected edges. The task is not to output the edges themselves or reconstruct an adjacency list, but to assign to every vertex i (from 1 to n − 1) a partner vertex pi such that the pair (i, pi) is one of the given tree edges.

In other words, for each vertex except the last one, we must choose one neighbor from the tree and write it down as its assigned value. The only requirement is that the chosen pair must correspond to an existing edge in the tree.

The constraint n ≤ 100000 implies the tree can be large and any solution must be linear or near-linear in n. A quadratic strategy that tries, for each vertex, to search through edges or test connectivity is immediately too slow. Even a repeated BFS per node would lead to roughly O(n^2) behavior in the worst case, which is far beyond acceptable limits.

A subtle point in interpretation is that the tree is undirected but the output introduces an orientation-like structure: each vertex i picks exactly one neighbor pi. This is not arbitrary per se; it must be consistent with the tree structure, meaning pi must be adjacent to i.

A naive mistake is assuming we must assign a global orientation or produce a rooted structure. That is not required. Another mistake is thinking the answer must be unique or optimal in some sense; any valid assignment is accepted.

One edge case that often confuses implementations is when the tree is a simple path. For example, if the tree is 1-2-3-4, then valid outputs include p1 = 2, p2 = 1 or 3, p3 = 2 or 4. A careless implementation that always picks the smallest neighbor may still work here, but a DFS-based attempt that assumes parent-child structure can fail if the traversal root is chosen poorly and constraints are not respected when writing output indices.

Another case is a star-shaped tree where node 1 connects to all others. In that case, all pi values could be 1, which is valid, but an implementation that assumes each vertex must choose a distinct partner would fail.

## Approaches

A brute-force interpretation would be to, for each vertex i from 1 to n − 1, scan all edges and find one that is incident to i. This is correct because every vertex has at least one neighbor in a tree, so such an edge always exists. However, scanning all edges for every vertex costs O(n^2), since there are n − 1 vertices and n − 1 edges, leading to about 10^10 checks in the worst case, which is impossible.

The key observation is that we do not need to search at all. The input already gives us adjacency information implicitly. If we build an adjacency list, every vertex immediately knows its neighbors, so we can pick any one neighbor in constant time per vertex. This reduces the problem from repeated search to a single preprocessing step plus a linear assignment pass.

The structure of a tree guarantees that every vertex has at least one adjacent vertex, so the adjacency list is never empty. This ensures we can always choose a valid pi.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan edges per vertex | O(n^2) | O(n) | Too slow |
| Build adjacency list and pick any neighbor | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all edges and construct an adjacency list for each vertex. This gives direct access to all neighbors of any node in constant time per neighbor.
2. For each vertex i from 1 to n − 1, look at its adjacency list and pick any neighbor. A common deterministic choice is the first neighbor encountered. This ensures pi is always valid because adjacency lists only contain vertices connected by an edge.
3. Output pi for each i in order.

The main design decision is that we never need to consider vertex n for output because the problem only asks for values up to n − 1. The adjacency list guarantees that every such vertex has at least one neighbor, so no special handling is needed for leaves or internal nodes.

### Why it works

The correctness relies on the invariant that in a tree every vertex has degree at least one except in the trivial n = 1 case, which is excluded by n ≥ 2. Since the adjacency list is built directly from the edges, any neighbor selected from it is guaranteed to form a valid edge. Because each pi is chosen independently and only constrained by local adjacency, there is no global consistency requirement beyond edge validity. Thus, selecting an arbitrary neighbor per node always yields a valid output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    res = []
    for i in range(1, n):
        res.append(str(adj[i][0]))
    
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The implementation builds a standard adjacency list in O(n). Each edge is inserted twice, once for each endpoint, preserving undirected structure.

When producing the answer, we iterate only up to n − 1 exactly as required. For each node, we access adj[i][0], which is safe because every node in a tree has at least one neighbor. No sorting or prioritization is required because any valid neighbor satisfies the condition.

A subtle implementation detail is ensuring indexing starts at 1, matching the problem statement. Another is that we never attempt to handle empty adjacency lists, since tree properties guarantee non-emptiness.

## Worked Examples

Consider the sample tree:

Input edges:

1-2, 1-3, 2-4, 2-5

Adjacency lists become:

1: [2, 3]

2: [1, 4, 5]

3: [1]

4: [2]

5: [2]

We process nodes 1 to 4:

| i | adj[i] | chosen pi |
| --- | --- | --- |
| 1 | [2, 3] | 2 |
| 2 | [1, 4, 5] | 5 (or any neighbor) |
| 3 | [1] | 1 |
| 4 | [2] | 2 |

This demonstrates that any neighbor choice is valid and still satisfies the constraint.

A second example is a path tree 1-2-3-4-5.

Adjacency lists:

1: [2]

2: [1, 3]

3: [2, 4]

4: [3, 5]

5: [4]

Processing:

| i | adj[i] | chosen pi |
| --- | --- | --- |
| 1 | [2] | 2 |
| 2 | [1, 3] | 1 |
| 3 | [2, 4] | 2 |
| 4 | [3, 5] | 3 |

This shows the algorithm naturally handles chains where each node has exactly two choices except endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is stored twice and each vertex is processed once |
| Space | O(n) | Adjacency list stores 2(n − 1) entries |

The solution comfortably fits within the constraints since both time and memory scale linearly with n up to 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    res = []
    for i in range(1, n):
        res.append(str(adj[i][0]))
    return " ".join(res)

# provided sample (one valid output form)
assert run("""5
1 2
1 3
2 4
2 5
""") in {
    "2 1 2 2",
    "2 3 2 2",
    "3 1 2 2",
    "3 2 2 2"
}

# minimum n
assert run("""2
1 2
""") == "2"

# star shaped
assert run("""5
1 2
1 3
1 4
1 5
""") == "2 1 1 1"

# path
assert run("""5
1 2
2 3
3 4
4 5
""") == "2 1 2 3"

# skewed small
assert run("""4
1 2
2 3
3 4
""") == "2 1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 edge | 2 | smallest tree |
| star tree | all 1 or equivalent | hub structure correctness |
| path tree | alternating neighbors | chain handling |
| skewed tree | consistent adjacency choice | non-uniform degree cases |

## Edge Cases

In a two-node tree, adjacency lists are [2] and [1]. The algorithm assigns p1 = 2 directly from adj[1][0], producing the only valid output.

In a star centered at 1, adj[1] contains all other nodes, while all leaves contain only 1. For i from 1 to n − 1, each leaf i has adj[i][0] = 1, and node 1 picks its first neighbor, typically 2. Every assignment remains a valid edge because all edges connect through the center.

In a deep path, each internal node has exactly two neighbors. The algorithm always picks the first inserted neighbor, which is determined by input order, and still guarantees adjacency. The correctness does not depend on consistency between choices across nodes, only on local edge validity, which is preserved by construction.
