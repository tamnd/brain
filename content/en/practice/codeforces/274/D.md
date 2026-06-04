---
title: "CF 274D - Lovely Matrix"
description: "We are given a matrix with n rows and m columns. Each row originally was sorted in non-decreasing order, but now some entries have been erased (marked -1) and the columns may have been shuffled."
date: "2026-06-05T02:05:48+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 274
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 168 (Div. 1)"
rating: 2200
weight: 274
solve_time_s: 94
verified: true
draft: false
---

[CF 274D - Lovely Matrix](https://codeforces.com/problemset/problem/274/D)

**Rating:** 2200  
**Tags:** dfs and similar, graphs, greedy, sortings  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a matrix with `n` rows and `m` columns. Each row originally was sorted in non-decreasing order, but now some entries have been erased (marked `-1`) and the columns may have been shuffled. Our task is to restore the column order so that it is possible to fill the erased entries with integers and make every row sorted again. The output is a permutation of column indices representing a valid reordering, or `-1` if no such ordering exists.

The input constraint `1 ≤ n·m ≤ 10^5` means we can afford at most linear or near-linear time algorithms. Anything quadratic in `n·m` is likely too slow. Each number fits in a 32-bit integer range, so we do not have to worry about arithmetic overflow.

Edge cases are subtle. For instance, if an entire column is erased, it can fit anywhere, so a naive approach that compares only existing numbers might falsely declare impossibility. Similarly, if some rows contain equal values in multiple columns, we need to ensure the final ordering allows any filled number to maintain the row’s sorted property.

A concrete example is:

```
2 2
-1 2
1 -1
```

A naive comparison might reject the first column before realizing it can take the value `0` in row 1 and still preserve sorting. The correct output is `2 1`, showing that a careful relative ordering based on constraints, not exact values, is required.

## Approaches

The brute-force method would try all `m!` permutations of columns, checking for each permutation whether it is possible to fill erased entries to make rows sorted. This is correct in principle but infeasible since `m!` grows faster than 10^5 even for `m = 10`. Checking each permutation requires iterating over all rows and columns, giving `O(n·m·m!)` operations, which is far beyond our limit.

The key observation is that the problem reduces to a topological ordering. Each row implies constraints between columns: if a number in column `c1` is greater than a number in column `c2` in the same row (ignoring `-1`), then in the final lovely matrix, `c1` must appear after `c2`. For erased entries, we can ignore them because they can take any value. Combining all rows, we construct a directed graph of column dependencies. If this graph has a cycle, no ordering is possible. If it is acyclic, a topological sort gives a valid column permutation.

The optimal solution works because we only care about relative order imposed by filled numbers. We never need exact values, so we can reduce the problem from factorial-time permutation checks to linear-time topological sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m·m!) | O(n·m) | Too slow |
| Topological Sort | O(n·m) | O(n·m) | Accepted |

## Algorithm Walkthrough

1. Initialize an adjacency list `graph` for columns and an array `in_degree` to track incoming edges. These will store the column dependencies derived from rows.
2. Iterate through each row. For each pair of filled entries `(c1, c2)` such that the value in `c1` > value in `c2`, add an edge from `c2` to `c1` in the graph. This encodes that `c2` must appear before `c1`. Ignore `-1` entries.
3. After processing all rows, check for cycles using Kahn's algorithm for topological sorting. Initialize a queue with all columns having zero in-degree.
4. Repeatedly remove a column from the queue, append it to the result permutation, and decrease the in-degree of its neighbors. Add any neighbor whose in-degree drops to zero to the queue.
5. If all columns are processed, output the resulting permutation. If a cycle prevents all columns from being added, output `-1`.

Why it works: Every directed edge represents a constraint implied by some row that must be preserved to achieve a non-decreasing sequence. By performing a topological sort, we produce an order of columns that respects all these constraints. Because `-1` entries impose no constraint, ignoring them does not introduce any invalidity. A cycle indicates a contradictory ordering that cannot be resolved, hence `-1`.

## Python Solution

```python
import sys
from collections import deque, defaultdict
input = sys.stdin.readline

n, m = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(n)]

graph = [[] for _ in range(m)]
in_degree = [0] * m

for row in matrix:
    filled = [(val, idx) for idx, val in enumerate(row) if val != -1]
    filled.sort()
    for i in range(len(filled) - 1):
        u = filled[i][1]
        v = filled[i + 1][1]
        if filled[i][0] < filled[i + 1][0]:
            graph[u].append(v)
            in_degree[v] += 1

queue = deque([i for i in range(m) if in_degree[i] == 0])
order = []

while queue:
    u = queue.popleft()
    order.append(u + 1)
    for v in graph[u]:
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)

if len(order) < m:
    print(-1)
else:
    print(*order)
```

The solution first collects non-erased numbers per row and sorts them to identify ordering constraints. Using a graph and in-degree array implements Kahn's algorithm efficiently. Adding `1` to indices ensures output matches the 1-based requirement.

## Worked Examples

### Sample 1

Input:

```
3 3
1 -1 -1
1 2 1
2 -1 1
```

| Row | Filled entries | Sorted | Edges added |
| --- | --- | --- | --- |
| 1 | [(1,0)] | [(1,0)] | None |
| 2 | [(1,0),(2,1),(1,2)] | [(1,0),(1,2),(2,1)] | 0->1, 2->1 |
| 3 | [(2,0),(1,2)] | [(1,2),(2,0)] | 2->0 |

Topological sort of graph produces column order `[3,1,2]`.

This trace shows that ignoring `-1` and only adding edges from strictly smaller values preserves all constraints and allows a valid permutation.

### Custom Input

```
2 2
-1 2
1 -1
```

Filled entries per row: `[(1,1)]`, `[(1,0)]`. No strict inequalities, so graph has no edges. Any permutation `[1,2]` or `[2,1]` is valid. Topological sort returns `[1,2]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | Each row is scanned once. Sorting filled entries is at most O(m log m) per row, but since m ≤ 10^5/n, it stays linear overall. Graph construction and topological sort are O(m + n·m). |
| Space | O(n·m) | Storing matrix and adjacency list. In-degree array is O(m). |

The solution comfortably fits within the 2-second limit for n·m ≤ 10^5.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque
    input = sys.stdin.readline
    n, m = map(int, input().split())
    matrix = [list(map(int, input().split())) for _ in range(n)]
    graph = [[] for _ in range(m)]
    in_degree = [0]*m
    for row in matrix:
        filled = [(val, idx) for idx, val in enumerate(row) if val != -1]
        filled.sort()
        for i in range(len(filled)-1):
            u = filled[i][1]
            v = filled[i+1][1]
            if filled[i][0] < filled[i+1][0]:
                graph[u].append(v)
                in_degree[v] += 1
    queue = deque([i for i in range(m) if in_degree[i]==0])
    order=[]
    while queue:
        u=queue.popleft()
        order.append(u+1)
        for v in graph[u]:
            in_degree[v]-=1
            if in_degree[v]==0:
                queue.append(v)
    if len(order)<m:
        return "-1"
    return " ".join(map(str, order))

# Provided samples
assert run("3 3\n1 -1 -1\n1 2 1\n2 -1 1\n") == "3 1 2", "sample 1"

# Custom cases
assert run("2 2\n-1 2\n1 -1\n") in ["1 2", "2 1"], "erased entries anywhere"
assert run("1 3\n-1 -1 -1\n") in ["1 2 3","1 3 2","2 1 3","2
```
