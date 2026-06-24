---
title: "CF 105229M - \u4e0d\u5171\u6234\u5929"
description: "We are given a line of $n$ water lilies labeled from left to right. We need to design two independent directed systems of connections on these positions. The first system belongs to a frog."
date: "2026-06-24T16:12:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105229
codeforces_index: "M"
codeforces_contest_name: "The 2024 Shanghai Collegiate Programming Contest"
rating: 0
weight: 105229
solve_time_s: 63
verified: true
draft: false
---

[CF 105229M - \u4e0d\u5171\u6234\u5929](https://codeforces.com/problemset/problem/105229/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of $n$ water lilies labeled from left to right. We need to design two independent directed systems of connections on these positions.

The first system belongs to a frog. It consists of directed jumps from some positions $a_i$ to $b_i$, always with $a_i < b_i$, and every position is used at most once as a start and at most once as an end. Because of this restriction, the frog’s moves form a collection of disjoint directed edges on the line.

The second system belongs to a bird. It is defined in the same way using pairs $x_i \to y_i$, also with all starts distinct and all ends distinct.

Once these two systems are fixed, movement is allowed by following directed edges repeatedly, so both frog and bird can travel along paths in their respective directed graphs.

A pair of positions $(i, j)$ becomes dangerous if the frog can reach $j$ from $i$ using its jump system and simultaneously the bird can also reach $j$ from $i$ using its flight system. If even one such pair exists, the bird will eventually be able to catch the frog.

The task is to construct both systems in such a way that no such overlapping reachability pair exists, while maximizing the total number of edges across both systems.

The key constraint is that each system has very limited structure: because all sources are distinct and all targets are distinct, each system is a partial matching directed from left to right. However, reachability is transitive, so even if edges look simple locally, chaining could create long-range reachability and potentially create forbidden overlaps.

With $n \le 10^4$, we can afford an $O(n)$ or $O(n \log n)$ construction. Anything involving global pairwise reasoning over all $O(n^2)$ pairs is impossible.

A subtle failure case appears when one system forms a chain. For example, if we build frog edges as $1 \to 2, 2 \to 3, 3 \to 4$, then the frog can reach every later node from every earlier node. In that situation, the bird must avoid every reachable pair entirely, which collapses its structure to almost nothing. This shows that long chains are dangerous because they explode reachability through transitivity.

## Approaches

A brute-force idea is to try all possible ways to assign directed edges to the frog and bird under the uniqueness constraints, compute reachability in both graphs, and check whether any pair is reachable in both. This quickly becomes infeasible because even building reachability for one graph is $O(n^2)$ in the worst case, and the number of configurations is combinatorial.

The structural insight is that reachability only becomes large when chains form. If a graph contains no directed path of length greater than one, then its reachability relation is exactly its edge set. This happens when every node appears in at most one edge as a source and at most one as a destination, and importantly, no vertex is used as both an intermediate bridge between two edges. In other words, we keep each system as a matching, so transitive closure does not expand anything.

Once both systems are matchings, the condition simplifies dramatically: a pair is reachable if and only if it is directly an edge. The constraint “no pair is reachable in both systems” becomes “no directed edge is shared between the two systems.”

This reduces the task to packing as many disjoint directed edges as possible into two matchings on the line. Since each matching can use each vertex at most once as a start and at most once as an end, each matching can contain at most $\lfloor n/2 \rfloor$ edges, and we can construct both simultaneously in an interleaving pattern so that together they use almost all adjacent pairs without conflict.

A clean construction achieves total $n-1$ edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over graphs + reachability | Exponential / $O(n^3)$ | $O(n^2)$ | Too slow |
| Interleaving matching construction | $O(n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We build two directed matchings on the path $1, 2, \dots, n$, carefully staggered so that no directed pair is reused.

1. Construct frog edges by pairing consecutive nodes starting from 1: $1 \to 2, 3 \to 4, 5 \to 6,$ and so on.

This ensures the frog graph is a set of independent edges with no paths longer than one step, so reachability is identical to the edge set.
2. Construct bird edges by shifting the pairing by one: $2 \to 3, 4 \to 5, 6 \to 7,$ and so on.

This also forms a matching, again preventing any multi-step reachability.
3. Stop each system when running out of valid pairs. If $n$ is odd, the last node remains unused in one or both systems, which is unavoidable due to the matching constraint.
4. Output all frog edges first, then all bird edges.

The construction guarantees that every edge is unique across systems because frog edges always connect odd-even pairs, while bird edges connect even-odd pairs shifted by one. This structural offset prevents overlap.

Why it works comes down to reachability collapse. Since both graphs are matchings, no vertex acts as a junction connecting two edges, so every reachable pair is exactly one edge. Therefore, the only way the forbidden condition could happen is if both systems contain the same directed pair. The alternating construction prevents this entirely while maximizing the number of edges each system can hold.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    frog = []
    bird = []
    
    # frog: (1,2), (3,4), ...
    for i in range(1, n, 2):
        if i + 1 <= n:
            frog.append((i, i + 1))
    
    # bird: (2,3), (4,5), ...
    for i in range(2, n, 2):
        if i + 1 <= n:
            bird.append((i, i + 1))
    
    m = len(frog) + len(bird)
    print(m)
    
    for a, b in frog:
        print(a, b)
    
    for a, b in bird:
        print(a, b)

if __name__ == "__main__":
    solve()
```

The frog edges are generated by stepping through odd indices, ensuring every edge starts at an odd position and ends at the next even position. The bird edges are generated symmetrically but shifted, starting from even indices. This guarantees that no directed pair appears in both lists.

A common pitfall is trying to maximize edges without controlling structure, which accidentally creates chains like $1 \to 2 \to 3$ and causes large transitive closures. Here we explicitly avoid that by ensuring each node participates in at most one edge per graph, eliminating all multi-step reachability.

## Worked Examples

### Example 1

Let $n = 6$.

Frog edges are:

$1 \to 2, 3 \to 4, 5 \to 6$

Bird edges are:

$2 \to 3, 4 \to 5$

| Step | Frog edges | Bird edges | Total |
| --- | --- | --- | --- |
| 1 | (1,2) | - | 1 |
| 2 | (1,2),(3,4) | - | 2 |
| 3 | (1,2),(3,4),(5,6) | - | 3 |
| 4 | same | (2,3) | 4 |
| 5 | same | (2,3),(4,5) | 5 |

This shows the alternating pattern fills almost all adjacent pairs without overlap.

The invariant observed is that frog edges always start from odd indices, while bird edges always start from even indices, so no edge coincides.

### Example 2

Let $n = 5$.

Frog edges:

$1 \to 2, 3 \to 4$

Bird edges:

$2 \to 3, 4 \to 5$

| Step | Frog | Bird | Total |
| --- | --- | --- | --- |
| 1 | (1,2) | - | 1 |
| 2 | (1,2),(3,4) | - | 2 |
| 3 | same | (2,3) | 3 |
| 4 | same | (2,3),(4,5) | 4 |

Again, no overlap occurs and all edges are direct, so reachability does not extend beyond single edges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is processed once to build at most one edge per graph |
| Space | $O(1)$ extra | Only storing output edges |

The construction is linear and easily fits within the constraints $n \le 10^4$, with negligible memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal
assert run("2") == "1\n1 2", "n=2 simplest"

# provided-like small even
assert run("6") == "5\n1 2\n3 4\n5 6\n2 3\n4 5"

# odd case
assert run("5") == "4\n1 2\n3 4\n2 3\n4 5"

# single chain boundary
assert run("3") == "2\n1 2\n2 3"

# larger structure sanity
assert run("8").splitlines()[0] == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | single edge only | minimal boundary |
| 6 | interleaving pattern | correctness of construction |
| 5 | odd-length handling | leftover node behavior |
| 3 | smallest non-trivial overlap case | avoids chain formation |

## Edge Cases

For $n = 2$, the construction produces a single frog edge $1 \to 2$ and no bird edges. There is no possibility of overlap because only one pair exists.

For $n = 3$, frog gets $1 \to 2$, bird gets $2 \to 3$. There is no transitive reachability beyond these edges, so no hidden overlap appears.

For larger odd $n$, the last node is unused in one or both systems. This is unavoidable due to the matching constraint, and the algorithm naturally leaves it isolated without affecting correctness.
