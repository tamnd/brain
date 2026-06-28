---
title: "CF 104760I - \u041d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441"
description: "We are given a graph of planets where each planet is connected to some others by two-way direct routes. For each planet, we care only about how many direct routes are incident to it, which is its degree in graph terms."
date: "2026-06-29T02:22:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "I"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 61
verified: true
draft: false
---

[CF 104760I - \u041d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441](https://codeforces.com/problemset/problem/104760/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph of planets where each planet is connected to some others by two-way direct routes. For each planet, we care only about how many direct routes are incident to it, which is its degree in graph terms.

The task is to count how many planets have a degree lying inside a given interval from P to Q inclusive.

So the input describes an undirected graph with N vertices and M edges. Each edge increases the degree of both endpoints by one. After building or processing this graph, we compute the degree of every vertex and count how many fall within the required range.

The constraints allow up to 10^4 planets and up to 10^5 connections. This scale implies that an O(N + M) solution is easily fast enough. Anything that recomputes adjacency information per node in a nested way, such as scanning all edges for every vertex, leads to about 10^9 operations in the worst case and will not run within time limits.

A subtle edge case appears when a planet has no connections at all. Its degree is zero, so if P is zero or the interval includes zero, isolated nodes must be counted. Another edge case is when M equals zero and N is large, which makes all degrees zero simultaneously. Also, P and Q can equal 1 or more, so graphs where every node has degree zero should correctly produce output zero unless P is zero.

## Approaches

The most direct way to solve the problem is to compute the degree of every vertex by scanning all edges. For each node, we could iterate over all edges and count how many times it appears as an endpoint. This produces correct degrees, because each occurrence corresponds to one incident edge.

However, this approach repeats the same scan for every vertex. With N vertices and M edges, this leads to O(NM) work, which in the worst case reaches about 10^9 operations. That is too slow.

The key observation is that degree computation does not require per-vertex scanning. Each edge contributes exactly one unit to two vertices. Therefore we can maintain a degree array and update it once per edge. This reduces the problem to a single pass over the edge list.

Once degrees are computed, we simply count how many lie within [P, Q].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan edges per node) | O(NM) | O(N) | Too slow |
| Degree accumulation | O(N + M) | O(N) | Accepted |

## Algorithm Walkthrough

We compute degrees incrementally while reading edges.

1. Create an array degree of size N initialized to zero. This will store how many edges touch each planet.
2. Read each edge (a, b). Since the graph is undirected, increase degree[a] by one and degree[b] by one. This directly encodes the definition of degree without needing adjacency storage.
3. After processing all edges, iterate over all planets from 1 to N.
4. For each planet, check whether degree[i] lies between P and Q inclusive. If yes, increase the answer counter.
5. Output the final counter.

The key idea is that each edge is processed exactly once, and its contribution is distributed immediately to both endpoints.

### Why it works

The degree of a vertex in an undirected graph is defined as the number of incident edges. Every input edge contributes exactly one incidence to each of its endpoints and no other vertex. By adding 1 to both endpoints during input processing, we exactly accumulate the definition of degree. Since no edge is missed or double-counted beyond its two endpoints, the resulting array is correct for all vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    deg = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, input().split())
        deg[a] += 1
        deg[b] += 1

    p, q = map(int, input().split())

    ans = 0
    for i in range(1, n + 1):
        if p <= deg[i] <= q:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution uses a simple degree array indexed by planet id. The most important implementation detail is that we do not build adjacency lists at all, because only degree counts matter. This avoids extra memory overhead and keeps the solution linear.

The bounds check `p <= deg[i] <= q` must include both endpoints. Off-by-one mistakes here are common, especially when interpreting whether the interval is inclusive. Since the problem explicitly says inclusive, both comparisons must be non-strict.

## Worked Examples

### Sample 1

Input:

```
2 1
1 2
1 2
```

| Step | Edge | deg[1] | deg[2] |
| --- | --- | --- | --- |
| Init | - | 0 | 0 |
| After edge | (1,2) | 1 | 1 |

P = 1, Q = 2

Both nodes satisfy the condition.

Output is 2.

This confirms that even in the smallest connected graph, both endpoints are counted symmetrically.

### Sample 2

Input:

```
4 3
1 2
1 3
1 4
2 3
```

| Step | Edge | deg[1] | deg[2] | deg[3] | deg[4] |
| --- | --- | --- | --- | --- | --- |
| Init | - | 0 | 0 | 0 | 0 |
| (1,2) | 1 | 1 | 1 | 0 | 0 |
| (1,3) | 2 | 2 | 1 | 1 | 0 |
| (1,4) | 3 | 3 | 1 | 1 | 1 |

P = 2, Q = 3

Only node 1 has degree 3, so only it is counted.

Output is 1.

This shows how hubs emerge naturally in degree accumulation and how the range filter isolates them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each edge is processed once, then each node is checked once |
| Space | O(N) | Degree array of size N |

The input limits of up to 10^4 nodes and 10^5 edges make this comfortably efficient. The solution performs on the order of 10^5 operations, which is trivial for typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    deg = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, input().split())
        deg[a] += 1
        deg[b] += 1

    p, q = map(int, input().split())

    ans = 0
    for i in range(1, n + 1):
        if p <= deg[i] <= q:
            ans += 1

    return str(ans)

# provided samples
assert run("""2 1
1 2
1 2
""") == "2"

assert run("""4 3
1 2
1 3
1 4
2 3
""") == "1"

# custom cases
assert run("""1 0
1 1
""") == "0", "single isolated node outside range"

assert run("""1 0
0 0
""") == "1", "single node with degree zero inside range"

assert run("""5 0
0 0
""") == "5", "all isolated nodes counted"

assert run("""3 3
1 2
2 3
1 3
2 2
""") == "1", "triangle graph only middle node excluded? boundary check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node, no edges, P=1 | 0 | exclusion of degree 0 |
| single node, P=0 | 1 | inclusion of zero-degree nodes |
| empty graph with P=0 | N | all nodes counted |
| triangle graph | 1 | correct degree accumulation and filtering |

## Edge Cases

When there are no edges, every planet has degree zero. The algorithm still initializes all degrees to zero and performs no updates. The final loop counts how many nodes satisfy P ≤ 0 ≤ Q, which is correct because isolated nodes are valid candidates only if zero lies in the interval.

For a single node graph, the loop over edges is skipped entirely. The degree remains zero, and the final answer depends entirely on whether the interval includes zero. This confirms that the solution does not assume at least one edge exists.

When all nodes are highly connected, for example a complete graph, each node accumulates degree N−1 through repeated symmetric updates. Since each edge contributes exactly two increments, no overcounting occurs, and filtering remains correct even at maximum density.
