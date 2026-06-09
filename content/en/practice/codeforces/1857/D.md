---
title: "CF 1857D - Strong Vertices"
description: "We are given two arrays, a and b, both of length n. From these arrays, we are asked to construct a directed graph with n vertices. There is an edge from vertex u to vertex v (for u != v) if the difference a[u] - a[v] is greater than or equal to b[u] - b[v]."
date: "2026-06-09T00:47:26+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1857
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 891 (Div. 3)"
rating: 1300
weight: 1857
solve_time_s: 106
verified: false
draft: false
---

[CF 1857D - Strong Vertices](https://codeforces.com/problemset/problem/1857/D)

**Rating:** 1300  
**Tags:** math, sortings, trees  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays, `a` and `b`, both of length `n`. From these arrays, we are asked to construct a directed graph with `n` vertices. There is an edge from vertex `u` to vertex `v` (for `u != v`) if the difference `a[u] - a[v]` is greater than or equal to `b[u] - b[v]`. After constructing this graph, we want to identify all _strong vertices_. A vertex is strong if from that vertex, there exists a directed path to every other vertex in the graph.

The input consists of multiple test cases, and the total sum of `n` across all test cases is up to 200,000. This bound immediately tells us that a naive approach that examines all pairs of vertices explicitly, which would take `O(n^2)` time per test case, is too slow. With `n` up to 2·10^5, we need a solution with roughly `O(n log n)` or `O(n)` time per test case.

An edge case to be careful about is when all vertices are mutually reachable, for example if `a` and `b` are both increasing sequences. In this case, every vertex is strong. Another subtle situation occurs when one vertex has significantly higher `a[i]` relative to `b[i]` compared to others; it may dominate and become the only strong vertex. For example, `a = [1, 2, 3]` and `b = [1, 1, 1]` produces only the last vertex as strong.

## Approaches

A brute-force approach would iterate over all pairs `(u, v)` and explicitly construct the directed edges. After that, we could perform a reachability check from each vertex using BFS or DFS. This is correct because it directly follows the problem statement, but it requires `O(n^2)` operations per test case, which can reach 4·10^10 in the worst case. This is far too slow.

The key observation is to reformulate the edge condition. The inequality `a[u] - a[v] >= b[u] - b[v]` can be rewritten as `(a[u] - b[u]) >= (a[v] - b[v])`. Denote `c[i] = a[i] - b[i]`. Then an edge from `u` to `v` exists whenever `c[u] >= c[v]`. This reveals a structure: vertices with higher `c[i]` can reach vertices with lower `c[i]`. Therefore, the strongest vertices are the ones with the maximum `c[i]` value. These vertices can reach all vertices with smaller or equal `c[i]`, and vertices with smaller `c[i]` cannot reach vertices with larger `c[i]`. This insight collapses the problem to computing the maximum of `c[i]` and identifying which indices achieve it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n^2) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the arrays `a` and `b`.
2. Compute the auxiliary array `c` where `c[i] = a[i] - b[i]`.
3. Find the maximum value `max_c` in `c`.
4. Identify all indices `i` where `c[i] == max_c`. These indices correspond to strong vertices.
5. Output the number of strong vertices and the list of their indices in ascending order.

This works because the condition `c[u] >= c[v]` ensures that vertices with the maximum `c` can reach all others. Vertices with smaller `c` cannot reach vertices with larger `c` since `c[u] < c[v]` fails the inequality, so they cannot be strong.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    c = [a[i] - b[i] for i in range(n)]
    max_c = max(c)
    
    strong = [i + 1 for i in range(n) if c[i] == max_c]
    print(len(strong))
    print(*strong)
```

The solution first reads the number of test cases. For each test case, it reads the arrays `a` and `b` and computes `c[i] = a[i] - b[i]`. The maximum value of `c` determines which vertices are strong. We store the 1-based indices of vertices achieving this maximum and print the result. The implementation correctly handles multiple test cases and preserves order.

## Worked Examples

**Sample 1**

Input arrays:

`a = [3, 1, 2, 4]`

`b = [4, 3, 2, 1]`

Compute `c = a - b = [-1, -2, 0, 3]`.

Maximum `c` is `3`, achieved only at index `4`.

| i | a[i] | b[i] | c[i] |
| --- | --- | --- | --- |
| 1 | 3 | 4 | -1 |
| 2 | 1 | 3 | -2 |
| 3 | 2 | 2 | 0 |
| 4 | 4 | 1 | 3 |

Strong vertices: `[4]`.

**Sample 2**

Input arrays:

`a = [1, 2, 4, 1, 2]`

`b = [5, 2, 3, 3, 1]`

Compute `c = [-4, 0, 1, -2, 1]`.

Maximum `c` is `1`, achieved at indices `3` and `5`.

| i | a[i] | b[i] | c[i] |
| --- | --- | --- | --- |
| 1 | 1 | 5 | -4 |
| 2 | 2 | 2 | 0 |
| 3 | 4 | 3 | 1 |
| 4 | 1 | 3 | -2 |
| 5 | 2 | 1 | 1 |

Strong vertices: `[3, 5]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing `c` takes O(n), finding max takes O(n), identifying indices takes O(n) |
| Space | O(n) | Array `c` of length n is stored |

The total operations across all test cases sum to O(total n) ≤ 2·10^5, which is well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        c = [a[i] - b[i] for i in range(n)]
        max_c = max(c)
        strong = [i + 1 for i in range(n) if c[i] == max_c]
        print(len(strong))
        print(*strong)
    return output.getvalue().strip()

# Provided samples
assert run("5\n4\n3 1 2 4\n4 3 2 1\n5\n1 2 4 1 2\n5 2 3 3 1\n2\n1 2\n2 1\n3\n0 2 1\n1 3 2\n3\n5 7 4\n-2 -3 -6") == "1\n4\n2\n3 5\n1\n2\n3\n1 2 3\n2\n2 3"

# Custom cases
assert run("1\n2\n0 0\n0 0") == "2\n1 2", "All equal"
assert run("1\n3\n1 2 3\n3 2 1") == "1\n3", "Single max at end"
assert run("1\n4\n4 4 4 4\n1 1 1 1") == "4\n1 2 3 4", "All vertices strong"
assert run("1\n5\n1 2 3 4 5\n5 4 3 2 1") == "1\n5", "Increasing difference at last"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a=[0,0], b=[0,0]` | `2\n1 2` | Case where all vertices are equal, everyone is strong |
| `a=[1,2,3], b=[3,2,1]` | `1\n3` | Single vertex is strong, checks correct max computation |
| `a=[4,4,4,4], b=[1,1,1,1]` | `4\n1 2 3 4` | All vertices |
