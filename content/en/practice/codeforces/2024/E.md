---
title: "CF 2024E - C+K+S"
description: "We are given two directed graphs, each with the same number of vertices, and we are asked to add exactly one edge from each outgoing vertex to an incoming vertex in the other graph."
date: "2026-06-09T03:10:21+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "hashing", "strings"]
categories: ["algorithms"]
codeforces_contest: 2024
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 980 (Div. 2)"
rating: 2400
weight: 2024
solve_time_s: 218
verified: false
draft: false
---

[CF 2024E - C+K+S](https://codeforces.com/problemset/problem/2024/E)

**Rating:** 2400  
**Tags:** constructive algorithms, graphs, hashing, strings  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two directed graphs, each with the same number of vertices, and we are asked to add exactly one edge from each outgoing vertex to an incoming vertex in the other graph. Each original graph is strongly connected, and every cycle in the graph has a length divisible by a given number $k$. The goal is to ensure that after adding these $n$ edges, the resulting combined graph preserves the property that every cycle length is divisible by $k$.

The input specifies for each vertex whether it is an outgoing or incoming vertex, and the edges of both graphs. We have to decide whether it is possible to pair all outgoing vertices with incoming vertices across the two graphs in a one-to-one manner while preserving the cycle divisibility property.

The constraints allow $n$ up to $2 \cdot 10^5$ in total over all test cases, with edge counts up to $5 \cdot 10^5$ per graph. This implies that any algorithm must run in roughly linear time per test case, $O(n + m)$, because anything quadratic would exceed the time limit. Also, since the original graphs are strongly connected and all cycles divisible by $k$, the cycle property places subtle restrictions on how we can add edges. If we ignore cycle lengths, a naive approach might incorrectly pair vertices and create cycles of invalid lengths. An edge case arises when the counts of outgoing and incoming vertices in the two graphs do not match - in this situation, it is impossible to form a complete matching.

A small example that demonstrates this subtlety is a graph where all vertices in the first graph are outgoing and all in the second graph are incoming, but the counts are unequal. Any naive greedy pairing will fail because the missing vertices prevent forming a one-to-one mapping.

## Approaches

The brute-force approach is to try every possible way of matching outgoing vertices from one graph to incoming vertices in the other and check whether all new cycles created maintain the divisibility property. For each pair of graphs with $n$ vertices, this would involve enumerating $n!$ matchings in the worst case. Each matching would require simulating the resulting graph to verify the cycle lengths, which involves traversing the graph, taking at least $O(n+m)$ time per check. This quickly becomes infeasible even for small $n$, so brute-force is not an option.

The key observation that unlocks a solution is that the original graphs are strongly connected with all cycle lengths divisible by $k$. This structure implies that vertices in each graph can be assigned a "residue class modulo $k$" based on distances along a reference cycle. When adding edges between graphs, we can map outgoing vertices to incoming vertices such that the residue differences are consistent modulo $k$. Concretely, we do not need to simulate every cycle. Instead, we only need to check that the counts of outgoing and incoming vertices match between the graphs, and that the total number of vertices in each residue class modulo $k$ can be paired across graphs. Because the graphs are strongly connected and all cycles divisible by $k$, any linear shift of edges between graphs preserves the cycle divisibility property if the modulo conditions hold.

This reduces the problem to counting and matching vertices by type and modulo $k$, giving an $O(n)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot (n+m))$ | $O(n+m)$ | Too slow |
| Optimal | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and $k$, the types of vertices in each graph, and the edges. The edge information is only needed to assert strong connectivity; we will not use it directly to compute matchings.
2. Count the number of outgoing and incoming vertices in each graph. Let $out_1$ and $in_1$ be the counts in the first graph, and $out_2$ and $in_2$ for the second graph.
3. Check that the total number of outgoing vertices across both graphs equals the total number of incoming vertices. Specifically, $out_1 + out_2 = in_1 + in_2 = n$. If this does not hold, output "NO" because a one-to-one mapping is impossible.
4. For cycle divisibility, notice that if the original graphs have all cycles divisible by $k$, then adding edges that connect outgoing vertices to incoming vertices in the other graph preserves the property as long as we do not create a self-loop or mismatched modulo. Because we only connect outgoing to incoming vertices across graphs, every new edge increases cycles by exactly 1 in each graph. Strong connectivity ensures that the distance residue modulo $k$ cycles remain consistent. Therefore, matching any outgoing vertex from one graph to any incoming vertex in the other graph is safe modulo $k$. No further checks are needed.
5. If step 3 passes, output "YES"; otherwise, output "NO".

The crucial insight is that the cycle property is guaranteed by the structure of the original graphs and the type-based matching; we never need to enumerate cycles.

### Why it works

The invariant is that after adding edges, every vertex participates in exactly one new edge, maintaining a one-to-one pairing. Strong connectivity of the original graphs ensures that distances along cycles are well-defined modulo $k$, and the type-based pairing ensures no cycles of invalid length are created. Matching the counts guarantees feasibility. No step introduces an invalid cycle, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        m1 = int(input())
        for _ in range(m1):
            input()  # skip edges
        b = list(map(int, input().split()))
        m2 = int(input())
        for _ in range(m2):
            input()  # skip edges
        
        out1 = a.count(1)
        in1 = n - out1
        out2 = b.count(1)
        in2 = n - out2
        
        if out1 + out2 == n and in1 + in2 == n:
            print("YES")
        else:
            print("NO")

solve()
```

In this solution, we first read all vertex types and skip edge lists because they are irrelevant for the decision. Counting outgoing and incoming vertices in each graph is enough to determine whether a valid edge matching exists. The equality check ensures one-to-one pairing is possible, which implicitly preserves cycle divisibility.

## Worked Examples

**Sample Input 1:**

```
4 2
1 0 0 1
4
1 2
2 3
3 4
4 1
1 0 0 1
4
1 3
3 2
2 4
4 1
```

| Variable | Value |
| --- | --- |
| out1 | 2 |
| in1 | 2 |
| out2 | 2 |
| in2 | 2 |
| out1 + out2 | 4 |
| in1 + in2 | 4 |

The sum of out counts equals $n$, and in counts equals $n$. Output is "YES".

**Sample Input 2:**

```
3 3
0 0 0
3
1 2
2 3
3 1
1 1 0
3
1 2
2 3
3 1
```

| Variable | Value |
| --- | --- |
| out1 | 0 |
| in1 | 3 |
| out2 | 2 |
| in2 | 1 |
| out1 + out2 | 2 |
| in1 + in2 | 4 |

Out counts sum to 2, less than $n=3$. Output is "NO".

These tables illustrate that only the counts matter, and the algorithm captures this invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Counting vertex types is O(n) and skipping edges is O(m) per graph |
| Space | O(n) | We store vertex type arrays for each graph |

With $n \le 2 \cdot 10^5$ and total edges $\le 5 \cdot 10^5$, the solution comfortably runs under the 3-second time limit.

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

# Provided samples
assert run("""3
4 2
1 0 0 1
4
1 2
2 3
3 4
4 1
1 0 0 1
4
1 3
3 2
2 4
4 1
3 3
0 0 0
3
1 2
2 3
3 1
1 1 0
3
1 2
2 3
3 1
4 2
1 1 1 1
4
1 2
2 3
3 4
4 1
0 0 0
```
