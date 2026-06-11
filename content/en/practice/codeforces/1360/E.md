---
title: "CF 1360E - Polygon"
description: "We are given an $n times n$ square matrix that starts entirely filled with zeros. Along the top edge, there are $n$ cannons, one above each column, and along the left edge, there are $n$ cannons, one to the left of each row."
date: "2026-06-11T12:51:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1360
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 644 (Div. 3)"
rating: 1300
weight: 1360
solve_time_s: 129
verified: true
draft: false
---

[CF 1360E - Polygon](https://codeforces.com/problemset/problem/1360/E)

**Rating:** 1300  
**Tags:** dp, graphs, implementation, shortest paths  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ square matrix that starts entirely filled with zeros. Along the top edge, there are $n$ cannons, one above each column, and along the left edge, there are $n$ cannons, one to the left of each row. Each cannon shoots a "1" in a straight line either rightward (row cannons) or downward (column cannons) until it hits another 1 or the edge of the matrix. Once a 1 stops, it stays permanently in that cell.

The task is to determine whether a given final configuration of 0s and 1s could have been produced by some sequence of shots from these cannons. The input is a series of test cases, each consisting of the size $n$ and the $n \times n$ matrix, and the output should be "YES" if the configuration is possible and "NO" otherwise.

The constraints $1 \le n \le 50$ and total cells across all test cases $\le 10^5$ suggest that an $O(n^2)$ approach per matrix is acceptable. The non-obvious cases are those where a 1 is in a position that, if no other 1 blocks its path, would continue moving past the edge. For example, a 1 at the bottom-right corner is always fine, but a 1 at position $(1,1)$ in a 2x2 matrix without any 1s in the first row or column is impossible because nothing can stop a shot there early. A naive implementation that does not account for this "blocking by neighbors" rule would falsely accept such configurations.

## Approaches

The brute-force approach would try to simulate every possible sequence of shots and see if it matches the final matrix. Each cannon could shoot multiple times, and there are $2n$ cannons. Trying all sequences is combinatorial in nature and infeasible, even for $n=10$.

The key insight is to work backward. A 1 in the matrix must either be on the bottom edge, right edge, or have a 1 immediately to its right or below. If a 1 does not satisfy this property, no sequence of cannon shots could have placed it there without violating the collision rule. This observation allows us to check each cell independently in $O(n^2)$ time: for each 1 not in the last row or column, we ensure that either the cell below or to the right is also a 1. This captures the essential constraint that a 1 stops either when it reaches the matrix boundary or another 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)^k) for k shots | O(n^2) | Too slow |
| Optimal | O(n^2) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Iterate over each test case and read the size $n$ and the matrix.
2. For each cell $(i, j)$ in the matrix, check if it contains a 1.
3. If the cell contains a 1, and it is **not** in the last row or last column, check the two cells that could block its shot: $(i+1, j)$ (below) and $(i, j+1)$ (right).
4. If both the cell below and the cell to the right are 0, the configuration is impossible. Immediately mark this test case as "NO" and move to the next test case.
5. If all 1s pass the check, the configuration is possible, so mark the test case as "YES".
6. Output the results for all test cases.

Why it works: By construction, any 1 in a non-boundary position must have a blocker either directly below or directly to the right to be able to stop there. This invariant ensures that every 1 could have originated from a cannon shot and stopped appropriately. If any 1 violates this property, no sequence of shots could produce it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
results = []

for _ in range(t):
    n = int(input())
    grid = [input().strip() for _ in range(n)]
    possible = True
    for i in range(n):
        for j in range(n):
            if grid[i][j] == '1':
                if i < n - 1 and j < n - 1:
                    if grid[i+1][j] != '1' and grid[i][j+1] != '1':
                        possible = False
                        break
        if not possible:
            break
    results.append("YES" if possible else "NO")

print("\n".join(results))
```

This solution iterates over each cell. The nested loop checks only the cells that are not on the last row or last column. The early break avoids unnecessary checks once a violation is found. The grid is stored as a list of strings to simplify indexing and comparison with `'1'`.

## Worked Examples

Sample Input 1:

```
4
0010
0011
0000
0000
```

| i | j | grid[i][j] | i<n-1 & j<n-1? | grid[i+1][j] | grid[i][j+1] | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | True | 0 | 1 | OK |
| 1 | 2 | 1 | True | 0 | 1 | OK |
| 1 | 3 | 1 | False | - | - | OK |

All 1s satisfy the blocking rule, output is YES.

Sample Input 2:

```
2
10
01
```

| i | j | grid[i][j] | i<n-1 & j<n-1? | grid[i+1][j] | grid[i][j+1] | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | True | 0 | 0 | Fail |

A 1 at (0,0) has no right or bottom neighbor as 1, impossible configuration, output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test case | Each cell is checked at most once, total cells ≤ 10^5 |
| Space | O(n^2) | Stores the grid for each test case, no additional structures |

Given the constraints, this solution runs comfortably within the 2-second limit and uses memory well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    results = []
    for _ in range(t):
        n = int(input())
        grid = [input().strip() for _ in range(n)]
        possible = True
        for i in range(n):
            for j in range(n):
                if grid[i][j] == '1':
                    if i < n - 1 and j < n - 1:
                        if grid[i+1][j] != '1' and grid[i][j+1] != '1':
                            possible = False
                            break
            if not possible:
                break
        results.append("YES" if possible else "NO")
    return "\n".join(results)

# Provided samples
assert run("5\n4\n0010\n0011\n0000\n0000\n2\n10\n01\n2\n00\n00\n4\n0101\n1111\n0101\n0111\n4\n0100\n1110\n0101\n0111\n") == "YES\nNO\nYES\nYES\nNO"

# Custom cases
assert run("1\n1\n1\n") == "YES"  # single-cell 1
assert run("1\n2\n11\n11\n") == "YES"  # full 2x2 grid
assert run("1\n3\n100\n010\n001\n") == "NO"  # diagonal without blockers
assert run("1\n3\n110\n111\n011\n") == "YES"  # complex valid pattern
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid with 1 | YES | Single-cell trivial case |
| 2x2 full 1s | YES | Small complete grid |
| 3x3 diagonal 1s | NO | Impossible placement without blockers |
| 3x3 complex | YES | Multiple 1s with correct blockers |

## Edge Cases

For a single-cell matrix, any 1 is always valid since it is both on the last row and column.

For a 2x2 matrix where a 1 is at (0,0) and (1,1) but (0,1) and (1,0) are 0, the algorithm identifies that the 1 at (0,0) has no blockers to stop it, producing NO.

For a matrix entirely filled with 1s, every 1 either has a neighbor to the right or below or is on the boundary, producing YES.

The algorithm naturally handles all these scenarios without extra conditional logic, confirming correctness.
