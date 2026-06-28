---
title: "CF 104760I - \u041d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441"
description: "We are given a network of planets connected by bidirectional direct routes. Each planet can be viewed as a node in an undirected graph, and each route is an edge."
date: "2026-06-28T22:04:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "I"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 70
verified: false
draft: false
---

[CF 104760I - \u041d\u0430\u043b\u043e\u0433\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441](https://codeforces.com/problemset/problem/104760/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a network of planets connected by bidirectional direct routes. Each planet can be viewed as a node in an undirected graph, and each route is an edge. For every planet, we look at how many other planets it can reach in exactly one direct move, which is simply its degree in the graph.

The task is to count how many planets have a degree that lies within a given inclusive interval $[P, Q]$.

So the problem reduces to: build the graph, compute the degree of each node, and count how many degrees fall in the required range.

The constraints are small enough that a linear scan over all edges is sufficient. With $N \le 10^4$ and $M \le 10^5$, any algorithm that is $O(N + M)$ will easily run within limits. Even a naive adjacency list construction is safe, but anything like recomputing connectivity or running graph searches per node would be unnecessary overhead.

A few edge cases deserve attention.

One is when there are no edges at all. In this case every planet has degree zero, and we simply check whether zero lies in $[P, Q]$.

Another is when the graph is dense around a single node. For example, if one planet is connected to all others, its degree is $N-1$, while the rest have degree one. The solution must correctly count each degree independently.

Finally, duplicate edges are not present by problem guarantee, but self-loops are also excluded. So degree is always just the number of input edges incident to a node.

## Approaches

A brute-force interpretation would be to compute, for each planet, how many distinct nodes are reachable via direct transition. One could build adjacency lists and for each node count its neighbors. This is already sufficient, but it helps to see why anything more complex is unnecessary.

A more naive thought might be to, for each planet, scan all edges and count how many involve it. That would be $O(NM)$, which in the worst case becomes $10^9$ operations, too slow.

The key observation is that “number of direct transitions” is exactly the degree of a node in an undirected graph. Degrees can be accumulated in a single pass over the edges: every edge $(a, b)$ increases the degree of both $a$ and $b$ by one. After processing all edges, each node already has its final value.

This reduces the problem to a simple counting task over an array of size $N$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Edge scanning per node | $O(NM)$ | $O(1)$ | Too slow |
| Degree accumulation | $O(N + M)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an array `deg` of size $N$ with zeros. This array will store the number of direct connections for each planet. We use zero-based or one-based indexing consistently, but must be careful with input indices.
2. Read each edge $(a, b)$. For every edge, increment `deg[a]` and `deg[b]` by one. This works because each direct route contributes exactly one neighbor to both endpoints.
3. After processing all edges, iterate over all planets from 1 to $N$. For each planet, check whether its degree lies between $P$ and $Q$, inclusive.
4. Maintain a counter that increases whenever a planet satisfies the condition.
5. Output the final counter.

### Why it works

Each edge contributes exactly one unit of adjacency to both endpoints, so after processing all edges, `deg[i]` equals the number of distinct direct transitions from planet $i$. Since the graph is undirected and has no parallel edges, this count is exact. The final loop simply filters nodes by a fixed interval condition, so no structural property beyond degree is required.

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

The solution uses a direct degree accumulation array. The only subtle point is maintaining correct indexing: since planets are numbered from 1, the degree array is allocated with size $N+1$, and index 0 is unused.

The final scan is necessary because we must evaluate each node individually against the threshold range.

## Worked Examples

### Sample 1

Input:

```
2 1
1 2
1 2
```

We have two planets and one bidirectional connection.

| Step | Edge | deg[1] | deg[2] | Action |
| --- | --- | --- | --- | --- |
| 1 | (1,2) | 1 | 1 | increment both endpoints |

Now degrees are $[1, 1]$. With $P = 1, Q = 2$, both planets satisfy the condition.

The algorithm counts both nodes, producing output 2, which matches the expected result. This confirms that single-edge graphs are handled correctly and that both endpoints are counted symmetrically.

### Sample 2

Input:

```
4 3
1 2
1 3
1 4
2 3
```

We process edges one by one.

| Step | Edge | deg[1] | deg[2] | deg[3] | deg[4] |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,2) | 1 | 1 | 0 | 0 |
| 2 | (1,3) | 2 | 1 | 1 | 0 |
| 3 | (1,4) | 3 | 1 | 1 | 1 |

Final degrees are $[3,1,1,1]$. With $P = 2, Q = 3$, only node 1 qualifies.

The trace shows that repeated accumulation at node 1 correctly captures its higher connectivity, while leaves remain low-degree nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + M)$ | Each edge is processed once, then each node is checked once |
| Space | $O(N)$ | Degree array of size $N$ |

The constraints allow up to $10^5$ edges, so a single linear pass over edges and nodes is well within limits. Memory usage is minimal and fixed per node.

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

# provided samples
assert run("2 1\n1 2\n1 2\n") == "2", "sample 1"
assert run("4 3\n1 2\n1 3\n1 4\n2 3\n") == "1", "sample 2"

# custom cases
assert run("1 0\n1 1\n0 0") == "1", "single node always valid range"
assert run("3 0\n1 2\n1 1") == "3", "all degrees zero"
assert run("5 4\n1 2\n1 3\n1 4\n1 5\n3 0 2") == "4", "star graph boundary"
assert run("4 2\n1 2\n3 4\n1 1") == "4", "all degrees equal 1 in range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node graph | 1 | handles empty edge set |
| all isolated nodes | 3 | zero-degree correctness |
| star graph | 4 | high-degree center + boundary |
| two disjoint edges | 4 | uniform degree handling |

## Edge Cases

One important edge case is when there are no edges. For example:

Input:

```
3 0
1 1
```

Here all planets have degree zero. The algorithm initializes `deg = [0, 0, 0]` and skips the edge loop. The final check compares each zero against $[1,1]$. Since zero is not in the range, the answer is 0. This shows that absence of input edges does not require special handling.

Another case is a fully star-shaped graph:

Input:

```
5 4
1 2
1 3
1 4
1 5
2 4
```

Degrees become `[4,1,1,1,1]`. If the range is $[2,4]$, only node 1 qualifies. The algorithm correctly aggregates contributions from multiple edges into a single high-degree node without double counting or missing contributions.

A final subtle case is when $P = Q = 0$. Then only isolated nodes count. Since degrees are computed purely from edges, nodes with no incident edges remain zero, and the final scan naturally captures them without any extra logic.
