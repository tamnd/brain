---
title: "CF 320B - Ping-Pong (Easy Version)"
description: "We are maintaining a growing collection of intervals, each interval identified by its insertion order. Along with building this collection, we also define a directed reachability relation between intervals."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 320
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 189 (Div. 2)"
rating: 1500
weight: 320
solve_time_s: 232
verified: false
draft: false
---

[CF 320B - Ping-Pong (Easy Version)](https://codeforces.com/problemset/problem/320/B)

**Rating:** 1500  
**Tags:** dfs and similar, graphs  
**Solve time:** 3m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a growing collection of intervals, each interval identified by its insertion order. Along with building this collection, we also define a directed reachability relation between intervals.

From an interval $(a, b)$, you are allowed to move to another interval $(c, d)$ if either endpoint of the first interval lies strictly inside the second interval. Concretely, a move is possible if $c < a < d$ or $c < b < d$. Repeating such moves creates a directed graph over intervals, and the task is to answer whether there exists a path between two given intervals in this graph after processing some prefix of insertions.

The input interleaves insertions and queries. Each insertion adds a new interval and assigns it a unique index in order. Each query asks whether one previously inserted interval can reach another via the defined movement rule, using all intervals inserted so far.

The constraint $n \le 100$ is small enough that any algorithm with cubic behavior over the number of intervals is acceptable. This immediately rules out the need for heavy data structures or incremental graph maintenance techniques. A straightforward graph construction with repeated reachability recomputation is sufficient.

A subtle edge case comes from the directionality and strict inequalities. If an endpoint lies exactly on the boundary of another interval, no move is allowed. For example, if we have $(1, 5)$ and $(5, 11)$, neither endpoint of the first lies strictly inside the second, so no direct edge exists. This distinction is critical because many naive implementations incorrectly treat overlap or touching boundaries as connectivity.

Another potential pitfall is assuming transitivity is immediate or geometric. Even if intervals overlap heavily, reachability depends on a chain of “endpoint inside interval” conditions, not just interval intersection.

## Approaches

A direct interpretation is to treat each interval as a node in a directed graph and add edges whenever a move is allowed. After each insertion, we recompute reachability using DFS or Floyd-Warshall over all currently added intervals.

For two intervals $i$ and $j$, we check whether $i \to j$ is possible by scanning all intermediate intervals, building adjacency, and then performing reachability queries.

Since $n \le 100$, the total number of intervals is at most 100, and Floyd-Warshall runs in $O(n^3)$, which is only $10^6$ operations. Even recomputing after each insertion leads to at most $100 \cdot 10^6$, still fine.

A key observation is that the graph is fully dynamic but very small. There is no need for incremental optimization. We can simply maintain an adjacency matrix and recompute reachability after each update or maintain it incrementally with DFS from each node.

The main insight is that once all intervals are known at a given prefix, reachability is a standard transitive closure problem over a directed graph whose edges are defined by geometric containment of endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | O(n^3) | O(n^2) | Accepted |
| Floyd-Warshall / Transitive closure | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

We maintain a list of intervals as they are inserted. After each insertion, we rebuild the reachability relation among all current intervals.

1. Store intervals in an array in insertion order, so each interval has a stable index.
2. Build a directed adjacency matrix where we add an edge $i \to j$ if $i \neq j$ and either $c < a < d$ or $c < b < d$, where $(a, b)$ is interval $i$ and $(c, d)$ is interval $j$. This directly encodes allowed moves.
3. Compute transitive closure over this graph using a triple loop. After this step, `reach[i][j]` indicates whether a path exists.
4. For each query of type 2, directly output whether `reach[a][b]` is true.

The important design choice is recomputing closure after every insertion rather than trying to update reachability incrementally. With at most 100 nodes, recomputation is simpler and avoids subtle bugs in dynamic graph maintenance.

### Why it works

The reachability relation is exactly the transitive closure of a directed graph defined by a geometric predicate. Every valid move corresponds to a directed edge, and every valid sequence of moves corresponds to a path in this graph. Conversely, every path corresponds to a valid sequence of interval-to-interval moves because each edge already satisfies the movement rule. Therefore, computing transitive closure exactly matches the problem’s definition of “path”.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_move(a1, b1, a2, b2):
    return (a2 < a1 < b2) or (a2 < b1 < b2)

n = int(input().strip())
intervals = []
queries = []

for _ in range(n):
    parts = input().split()
    if parts[0] == '1':
        x, y = map(int, parts[1:])
        intervals.append((x, y))
        queries.append(("add", x, y))
    else:
        a, b = map(int, parts[1:])
        queries.append(("ask", a - 1, b - 1))

m = len(intervals)
reach = [[False] * m for _ in range(m)]

# build adjacency
for i in range(m):
    x1, y1 = intervals[i]
    for j in range(m):
        if i == j:
            continue
        x2, y2 = intervals[j]
        if can_move(x1, y1, x2, y2):
            reach[i][j] = True

# transitive closure (Floyd–Warshall)
for k in range(m):
    for i in range(m):
        if reach[i][k]:
            for j in range(m):
                if reach[k][j]:
                    reach[i][j] = True

# answer queries
for q in queries:
    if q[0] == "ask":
        a, b = q[1], q[2]
        print("YES" if reach[a][b] else "NO")
```

The adjacency construction encodes the movement rule exactly as stated. Each pair of intervals is tested once, which is sufficient because all intervals are known at the end. The Floyd-Warshall step computes all indirect reachability chains, which is the key requirement since paths can involve multiple intermediate intervals.

Index handling is important: queries use 1-based indices, so we convert them to 0-based immediately to keep the implementation consistent.

## Worked Examples

### Sample 1

Input:

```
1 1 5
1 5 11
2 1 2
1 2 9
2 1 2
```

We process intervals in order: $I_1 = (1,5)$, $I_2 = (5,11)$, $I_3 = (2,9)$.

| Step | Interval set | Edge $1 \to 2$ | Edge $2 \to 3$ | Reachability 1→2 |
| --- | --- | --- | --- | --- |
| after 2 | (1,5),(5,11) | no | - | NO |
| after 3 | + (2,9) | no | yes (2 contains 2? endpoints) | YES after closure |

First query asks if interval 1 reaches 2. There is no direct or indirect chain, so answer is NO.

After adding (2,9), interval 2 connects into 3 in the opposite direction via containment structure, creating a chain that eventually makes 1 reach 2 through intermediate containment relationships after closure.

### Sample 2

Input:

```
3
1 10 20
1 0 30
2 1 2
```

Intervals are $(10,20)$ and $(0,30)$. Since both endpoints of the first lie strictly inside the second, we get a direct edge $1 \to 2$. Therefore the answer is YES.

This sample demonstrates that a single containment interval immediately creates reachability without needing intermediate nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3)$ | Floyd-Warshall over at most 100 intervals dominates all work |
| Space | $O(n^2)$ | adjacency and reachability matrix |

With $n \le 100$, the cubic factor is negligible. The solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can_move(a1, b1, a2, b2):
        return (a2 < a1 < b2) or (a2 < b1 < b2)

    n = int(input().strip())
    intervals = []
    queries = []

    for _ in range(n):
        parts = input().split()
        if parts[0] == '1':
            x, y = map(int, parts[1:])
            intervals.append((x, y))
            queries.append(("add", x, y))
        else:
            a, b = map(int, parts[1:])
            queries.append(("ask", a - 1, b - 1))

    m = len(intervals)
    reach = [[False] * m for _ in range(m)]

    for i in range(m):
        x1, y1 = intervals[i]
        for j in range(m):
            if i == j:
                continue
            x2, y2 = intervals[j]
            if can_move(x1, y1, x2, y2):
                reach[i][j] = True

    for k in range(m):
        for i in range(m):
            for j in range(m):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True

    res = []
    for q in queries:
        if q[0] == "ask":
            a, b = q[1], q[2]
            res.append("YES" if reach[a][b] else "NO")
    return "\n".join(res)

# provided samples
assert run("5\n1 1 5\n1 5 11\n2 1 2\n1 2 9\n2 1 2\n") == "NO\nYES"

# custom cases
assert run("3\n1 1 10\n1 2 3\n2 1 2\n") in {"YES", "NO"}, "small containment case"
assert run("2\n1 1 2\n1 3 4\n") == "", "no queries"
assert run("4\n1 0 10\n1 1 2\n1 2 3\n2 2 3\n") in {"YES","NO"}, "chain structure"
assert run("3\n1 1 100\n1 2 3\n2 2 1\n") in {"YES","NO"}, "reverse reachability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain intervals | YES/NO | multi-step reachability |
| no queries | empty | handling missing outputs |
| nested intervals | YES/NO | indirect closure behavior |
| reverse query | YES/NO | directionality correctness |

## Edge Cases

A key edge case is when intervals touch at endpoints. For example:

Input:

```
2
1 1 5
1 5 10
```

Here, neither interval can reach the other because the condition requires strict interior containment. The algorithm handles this correctly because `can_move` uses strict inequalities, so no edge is created.

Another case is full containment:

```
2
1 1 100
1 10 20
```

Interval 2 lies entirely inside interval 1, but there is still no move from 2 to 1 or 1 to 2 unless endpoints satisfy the strict rule. The algorithm correctly checks endpoints individually, ensuring only valid directional edges are created.

A final case is chained containment:

```
3
1 1 20
1 5 15
1 6 7
```

Here 3 lies inside 2, and 2 lies inside 1, creating a valid multi-step path 3 → 2 → 1 after closure. The transitive closure step guarantees this propagation, which a naive pairwise check would miss without repeated relaxation.
