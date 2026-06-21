---
title: "CF 106192I - \u041d\u0430\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u0436\u0443\u043a\u043e\u0432"
description: "The city is modeled as an $n times n$ grid of intersections. Each intersection $(x, y)$ lies on a vertical street $x$ and a horizontal street $y$."
date: "2026-06-21T09:48:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106192
codeforces_index: "I"
codeforces_contest_name: "\u041f\u0435\u0440\u043c\u0441\u043a\u0430\u044f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2025"
rating: 0
weight: 106192
solve_time_s: 47
verified: true
draft: false
---

[CF 106192I - \u041d\u0430\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u0436\u0443\u043a\u043e\u0432](https://codeforces.com/problemset/problem/106192/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is modeled as an $n \times n$ grid of intersections. Each intersection $(x, y)$ lies on a vertical street $x$ and a horizontal street $y$. We need to place guards on some intersections, and each guard “covers” exactly one vertical street and one horizontal street, meaning every guard contributes once to the row $x$ and once to the column $y$.

The requirement is that every row and every column must have exactly $k$ guards placed on intersections belonging to it. Each intersection can host at most one guard, so we are effectively selecting cells of an $n \times n$ matrix such that every row sum and every column sum is exactly $k$.

The output also asks for the minimum possible number of guards. Since every guard contributes to exactly one row and one column, counting row contributions gives $n \cdot k$ total contributions, and each guard contributes exactly one to a row count. This already pins the answer to $m = n \cdot k$, so the task is not optimization in the usual sense but construction of a valid configuration with that many selected cells.

The constraints $n \le 1000$ and $k \le n$ imply we need an $O(nk)$ or $O(n^2)$ construction at worst. Anything involving flow or matching would be overkill but still technically feasible. The structure strongly suggests a direct combinational pattern.

A subtle failure case appears when $k = 0$. Then no guards should be placed and the output must be empty after printing zero. Another boundary case is $k = n$, where every row and column must contain all $n$ columns, forcing the full grid.

## Approaches

A brute-force way to think about the problem is to treat it as a bipartite graph construction: rows on one side, columns on the other, and each guard is an edge. We need a bipartite graph where every vertex on both sides has degree exactly $k$. One could attempt to search for such a graph by repeatedly adding edges and checking constraints, or run a maximum flow construction where each row and column has capacity $k$. This works because each valid solution corresponds to a perfect degree-constrained bipartite multigraph.

However, a flow-based construction builds a network with $O(n^2)$ potential edges and runs at least $O(n^3)$ or similar depending on implementation. This is unnecessary because the structure is symmetric and regular.

The key observation is that we only need a $k$-regular bipartite graph between two equal partitions of size $n$. Such graphs have a simple cyclic construction: connect each row $i$ to $k$ consecutive columns, wrapping around modulo $n$. This automatically ensures every row has exactly $k$ edges by construction, and every column also receives exactly $k$ edges because the shift distributes endpoints uniformly.

This reduces the problem from a constraint satisfaction problem to a deterministic pattern generation task.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Flow / brute constraint building | $O(n^3)$ | $O(n^2)$ | Too slow |
| Cyclic construction | $O(nk)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We interpret rows as left vertices and columns as right vertices in a bipartite graph. We construct exactly $k$ edges per row using a sliding window over columns.

1. Fix a row index $i$. We assign it exactly $k$ columns.
2. For each row $i$, connect it to columns $i, i+1, \dots, i+k-1$, using modulo $n$ wrapping.
3. Every such pair $(i, j)$ corresponds to placing a guard at intersection $(i, j)$.
4. Output all constructed pairs.

The wrapping is essential because without modulo arithmetic, rows near the end would run out of columns. The cyclic shift ensures uniformity across all rows.

### Why it works

Each row produces exactly $k$ distinct columns by construction, so row constraints are satisfied immediately. For column constraints, observe that column $j$ is included in row $i$ exactly when $j \in [i, i+k-1]$ modulo $n$. Over all rows, this interval pattern shifts uniformly, so every column is covered exactly $k$ times. This is equivalent to saying the construction is invariant under cyclic shifts of indices, which forces uniform degree distribution on both sides.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    
    res = []
    
    for i in range(n):
        for t in range(k):
            j = (i + t) % n
            res.append((i + 1, j + 1))
    
    out = [str(len(res))]
    for x, y in res:
        out.append(f"{x} {y}")
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the cyclic construction. Rows and columns are converted to 1-based indexing at output time. The nested loop over $n$ rows and $k$ offsets generates exactly $n \cdot k$ guards.

A common implementation mistake is forgetting modulo $n$, which breaks correctness for rows near the boundary. Another is off-by-one indexing when switching between 0-based internal logic and 1-based output format.

## Worked Examples

### Example 1

Input:

```
3 1
```

We build one guard per row.

| Row $i$ | Chosen column $j$ | Output pair |
| --- | --- | --- |
| 1 | 1 | (1, 1) |
| 2 | 2 | (2, 2) |
| 3 | 3 | (3, 3) |

Output:

```
3
1 1
2 2
3 3
```

This satisfies each row and column having exactly one guard.

### Example 2

Input:

```
4 2
```

| Row $i$ | Columns selected | Output pairs |
| --- | --- | --- |
| 1 | 1, 2 | (1,1), (1,2) |
| 2 | 2, 3 | (2,2), (2,3) |
| 3 | 3, 4 | (3,3), (3,4) |
| 4 | 4, 1 | (4,4), (4,1) |

Output:

```
8
1 1
1 2
2 2
2 3
3 3
3 4
4 4
4 1
```

The second example shows how wrapping preserves uniformity across boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk)$ | We generate exactly one output entry per guard |
| Space | $O(nk)$ | Storage for all guard positions before printing |

The constraint $n \le 1000$ ensures $n^2 \le 10^6$, so even the worst case $k = n$ produces about one million pairs, which is easily within limits in Python when using buffered output.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, k = map(int, sys.stdin.readline().split())
    
    res = []
    for i in range(n):
        for t in range(k):
            j = (i + t) % n
            res.append((i + 1, j + 1))
    
    out = [str(len(res))]
    for x, y in res:
        out.append(f"{x} {y}")
    return "\n".join(out)

# provided sample
assert run("3 1\n") == "3\n1 1\n2 2\n3 3"

# k = 0 edge case
assert run("5 0\n") == "0"

# full grid case
out = run("2 2\n").splitlines()
assert out[0] == "4"

# uniform small case
assert run("1 1\n") == "1\n1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 | diagonal selection | basic correctness |
| 5 0 | 0 | empty construction |
| 2 2 | full grid | maximal density |
| 1 1 | single cell | minimal non-zero case |

## Edge Cases

For $k = 0$, the loops generate no pairs. The output list remains empty, and the program correctly prints zero. This case ensures that the construction does not accidentally emit invalid coordinates when the inner loop is skipped.

For $k = n$, each row connects to all columns. The modulo operation still works, but it becomes redundant since no wrapping is needed. The algorithm produces the full $n^2$ grid, and every row and column has exactly $n$ guards as required.
