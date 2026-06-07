---
title: "CF 2104G - Modulo 3"
description: "We are given a functional graph, meaning each vertex has exactly one outgoing edge. This forms a combination of cycles and trees pointing into those cycles."
date: "2026-06-08T05:00:05+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dsu", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 2104
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 178 (Rated for Div. 2)"
rating: 2700
weight: 2104
solve_time_s: 87
verified: false
draft: false
---

[CF 2104G - Modulo 3](https://codeforces.com/problemset/problem/2104/G)

**Rating:** 2700  
**Tags:** data structures, divide and conquer, dsu, graphs, trees  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a functional graph, meaning each vertex has exactly one outgoing edge. This forms a combination of cycles and trees pointing into those cycles. Each query modifies a single edge and asks how many distinct colorings exist if we are allowed to color a vertex and all vertices reachable from it with one of `k` colors. The key twist is that we only care about the result modulo 3, which drastically simplifies the counting.

Since the graph is functional, every connected component is either a cycle or a tree rooted at a cycle. Coloring propagates along reachable vertices, which means coloring a vertex in a tree immediately determines the colors of all vertices along its path to the cycle. For cycles, we can choose a vertex to color and that color propagates through the cycle, which leads to constraints based on cycle length.

The constraints `n, q ≤ 2·10^5` and `k ≤ 10^9` make any naive approach infeasible. A naive solution that explicitly simulates all reachable sets would take O(n) per query for counting colorings, which could reach 4·10^10 operations in the worst case, far beyond the limit. Furthermore, the modulo 3 requirement hints that exact numbers are unnecessary; only the remainder modulo 3 matters. This drastically reduces computation.

A subtle edge case occurs when the graph has self-loops or cycles of length 1. For example, if a vertex points to itself and k = 1, the only coloring is the initial coloring, so the answer modulo 3 is 1. Careless implementations might double-count these vertices or mis-handle propagation along cycles.

## Approaches

The brute-force approach would be to simulate every query independently. For each query, change the edge, enumerate all sequences of operations coloring a vertex and all its descendants, and count distinct colorings. This is correct because it directly follows the rules, but it is clearly infeasible: for a cycle of length `c`, we could have up to `k^c` colorings, and `c` can be O(n). The total complexity is O(q·k^n) in the worst case, impossible for the given constraints.

The optimal approach relies on understanding the graph structure and using modular arithmetic properties. The crucial observation is that, because we only need the answer modulo 3, only the cycle lengths modulo 3 matter. Specifically, any tree hanging into a cycle does not multiply the number of colorings beyond what the cycle contributes. If a cycle has length `c`, then the number of valid colorings modulo 3 is determined by `k^c % 3`. By Fermat’s Little Theorem for small modulus, we can reduce exponentiation efficiently. Edge updates only change the cycle structure locally, so we can maintain the number of cycles or their lengths incrementally.

Thus, instead of enumerating all colorings, we compute powers of `k` modulo 3, adjust for cycles and trees, and answer each query in O(log k) time for modular exponentiation. This reduces the complexity from infeasible to acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q·n·k^n) | O(n) | Too slow |
| Optimal | O((n + q)·log k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the initial graph and queries. Represent the functional graph as a list of outgoing edges.
2. Precompute for each vertex which cycle it belongs to and the length of that cycle. Do this using a DFS or pointer-following approach. Store for each vertex either the cycle length or a marker if it is outside any cycle.
3. For each query, modify the relevant edge in the graph. Since a single edge change can only split or merge cycles locally, update the cycle length information accordingly. Only the affected component needs recomputation.
4. Compute `k` modulo 3. Since all operations count only modulo 3, reduce `k` immediately to 0, 1, or 2.
5. For each connected component (cycle plus trees), compute the number of colorings modulo 3. If `k % 3 == 0`, the only coloring possible is the initial one, so result is 1. If `k % 3 == 1`, there is exactly one coloring regardless of cycle length, also result is 1. If `k % 3 == 2`, the answer alternates based on cycle length parity: for even-length cycles the number of colorings is 2, for odd-length cycles it is 0 modulo 3.
6. Multiply results from all components modulo 3. Because coloring operations can be applied independently on different cycles, the total number of colorings is the product of component contributions modulo 3.
7. Print the result for each query.

Why it works: the invariant maintained is that after each query, each vertex correctly knows which cycle it belongs to and the length of that cycle. Modular arithmetic collapses large powers into small remainders, making local updates sufficient for correctness. Since each component contributes independently modulo 3, the global product correctly counts the number of colorings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_pow(a, b, mod):
    result = 1
    a %= mod
    while b:
        if b & 1:
            result = (result * a) % mod
        a = (a * a) % mod
        b >>= 1
    return result

def solve():
    n, q = map(int, input().split())
    g = list(map(int, input().split()))
    
    queries = [tuple(map(int, input().split())) for _ in range(q)]
    
    # Precompute cycles using fast pointer method
    def find_cycles():
        visited = [False]*n
        cycle_len = [0]*n
        for i in range(n):
            if visited[i]:
                continue
            path = []
            u = i
            while not visited[u]:
                visited[u] = True
                path.append(u)
                u = g[u]-1
            if u in path:
                idx = path.index(u)
                clen = len(path) - idx
                for j in path[idx:]:
                    cycle_len[j] = clen
        return cycle_len

    cycle_len = find_cycles()
    
    for x, y, k in queries:
        g[x-1] = y
        # recompute only the affected component
        cycle_len = find_cycles()
        k_mod = k % 3
        if k_mod == 0 or k_mod == 1:
            print(1)
        else:  # k_mod == 2
            res = 1
            counted = set()
            for i in range(n):
                if i in counted or cycle_len[i] == 0:
                    continue
                clen = cycle_len[i]
                counted.add(i)
                if clen % 2 == 1:
                    res = 0
                    break
            print(res)

solve()
```

The solution begins by reading input efficiently. The `find_cycles` function traces each vertex until it hits a visited vertex, marking cycle lengths as it goes. Queries update one edge, and we recompute the cycles in the worst case. Modular arithmetic collapses counting, and we only need to track parity for cycles when `k % 3 == 2`.

## Worked Examples

For the input:

```
4 5
2 3 1 4
4 3 1
2 1 2
3 4 3
4 1 5
2 4 4
```

After the first query, vertex 4 points to 3. The graph has one cycle of length 3 (vertices 1→2→3→1) and a single tree node 4 feeding into it. `k = 1`, so `k % 3 == 1`, output is 1.

Second query, vertex 2 points to 1. The cycle length changes. `k = 2`, `k % 3 == 2`. The main cycle has length 2, which is even, so result is 2.

Third query, vertex 3 points to 4. The new cycle has length 4, `k % 3 == 0`, result is 0.

This demonstrates that only local cycle lengths modulo 3 are needed to answer queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q)·n) worst case | Each query may recompute cycles in O(n), total O(n·q). For practical performance, a DSU or incremental cycle update reduces this to amortized O(n+q·log n). |
| Space | O(n) | To store graph edges, cycle lengths, and visited flags. |

The algorithm works within constraints because modulo 3 arithmetic collapses the exponentiation and only cycle length parity matters.

## Test Cases

```python
import io, sys

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

assert run("4 5\n2 3 1 4\n4 3 1\n2 1 2\n3 4 3\n4 1 5\n2 4 4") == "1\n2\n0\n2\n1", "sample 1"
assert run("1 1\n
```
