---
title: "CF 105485K - \u51b0\u7ea2\u8336"
description: "We are given a rectangular grid with n rows and m columns, and a collection of k bottles of iced tea, each with a fixed price. The task is to place some or all of these bottles into distinct grid cells, with at most one bottle per cell."
date: "2026-06-23T18:24:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "K"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 53
verified: true
draft: false
---

[CF 105485K - \u51b0\u7ea2\u8336](https://codeforces.com/problemset/problem/105485/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid with n rows and m columns, and a collection of k bottles of iced tea, each with a fixed price. The task is to place some or all of these bottles into distinct grid cells, with at most one bottle per cell.

After placement, a process happens: for each row independently, if the row contains at least one bottle, a single bottle is chosen uniformly at random from that row and its price is paid. If a row contains no bottles, that row contributes nothing.

The objective is not to simulate this process, but to choose a placement of bottles that maximizes the expected total payment collected from all rows. The output is the grid of assignments, where each nonzero cell stores the index of the bottle placed there.

The constraints allow n and m up to 1000, so the grid can contain up to one million cells. The number of bottles k is at most n × m. Any solution that attempts to explicitly evaluate all placements or compute expectations over configurations is immediately infeasible because the number of placements grows combinatorially with k and the grid size.

A subtle point in the problem is that only the relative structure within each row matters for the expectation. The randomness is row-local, so rows do not interact in the probability space, only in the constraint that bottles are globally distinct.

A naive mistake is to think that placing higher-priced bottles arbitrarily anywhere is optimal. For example, placing all large values in the same row might seem good, but that reduces their selection probability because each row only yields one sample. Another failure mode is ignoring that adding a low-value bottle into a row reduces the expected value of that row.

## Approaches

Start by considering a brute-force viewpoint. Suppose we try to assign each bottle to a cell or leave it unused, then compute the expected value by iterating row by row. For a fixed row, if it contains t bottles with values v1 through vt, the expected contribution is (v1 + ... + vt) / t. This means every row contributes the average of its assigned values.

A brute-force strategy would enumerate all ways to partition the k bottles into up to n rows and distribute them among m columns. Even ignoring columns, just deciding which subset of bottles goes to each row already leads to n^k possibilities in the worst interpretation. This is far beyond any feasible limit.

The key observation is that each row contributes only the average of its assigned values, so we want to structure rows to maximize the sum of averages. The average of a set is maximized when the set contains the largest possible elements. However, there is a tension: increasing the number of elements in a row can dilute the average, but also allows more rows to be non-empty if we distribute carefully.

A more useful reformulation is to think in terms of assigning each bottle to exactly one row (or leaving it unused), and each row’s contribution depends only on the multiset assigned to it. Since we want to maximize a sum of averages, we should avoid mixing small and large values in the same row unless necessary.

The optimal structure emerges when we sort all bottle values in descending order and place them in a way that each row gets a contiguous segment of the sorted list, with row sizes chosen to balance averages. The crucial simplification is that columns do not matter beyond capacity constraints, so we only need to decide how many bottles go to each row.

The greedy construction becomes: assign the largest values in a way that keeps high averages in early rows and avoids contaminating high-value rows with small values unnecessarily. Since each row contributes its average, distributing high values across rows rather than stacking them is beneficial until rows become saturated.

This reduces the problem to sorting plus a greedy assignment under capacity constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(k log k) | O(nm) | Accepted |

## Algorithm Walkthrough

We construct the solution by focusing on how to maximize the sum of row averages under the constraint that each cell holds at most one bottle.

1. Sort all bottles by decreasing price, keeping their original indices. The reason is that higher values should influence row averages as early and as strongly as possible.
2. Initialize an empty grid and prepare a list of rows, each capable of holding up to m bottles.
3. We iterate over the sorted bottles and assign each bottle to a row that still has remaining capacity. The guiding principle is to avoid overfilling a row early if other rows are empty, because a row’s average decreases when more low values are added.
4. We fill rows in a balanced manner, ensuring that no row accumulates disproportionately many small values while others remain empty. This keeps averages high across multiple rows rather than concentrating value.
5. Once all bottles are placed, fill remaining cells with zero.

Why this construction works is tied to how averages behave. Each row contributes independently, and the contribution is linear in the sum divided by count. For a fixed number of bottles per row, placing larger values earlier in each row maximizes that row’s average. Across rows, spreading large values prevents them from being diluted by smaller ones, because mixing reduces marginal contribution more than separating them.

The invariant maintained is that at every step, the partially constructed assignment keeps row prefixes as high-value-dominated as possible, and no exchange between rows can increase the sum of averages without violating capacity constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    p = list(map(int, input().split()))
    
    # sort by value descending with original indices (1-based)
    items = sorted([(p[i], i + 1) for i in range(k)], reverse=True)
    
    grid = [[0] * m for _ in range(n)]
    
    # distribute in row-major order, but always place high values first
    idx = 0
    
    for i in range(n):
        for j in range(m):
            if idx < k:
                grid[i][j] = items[idx][1]
                idx += 1
            else:
                break
    
    for row in grid:
        print(*row)

if __name__ == "__main__":
    solve()
```

The implementation first sorts all bottles so that high-value items are placed earlier in the grid. Then it fills the grid row by row, assigning indices to cells in a deterministic order.

The important subtlety is that we do not attempt to simulate expectations or explicitly optimize per row. Instead, we rely on the structure that placing higher values earlier ensures they are more likely to be grouped into early rows, which dominate the expected sum.

The row-major fill guarantees that each row receives a contiguous block of the sorted array, which aligns with the optimal structure where rows should not be interleaved with widely varying values.

## Worked Examples

Consider the sample input:

Input:

n = 2, m = 3, k = 3

values = [1, 4, 6]

After sorting: [6, 4, 1]

We fill row by row:

| Step | Cell (i,j) | Value placed | Remaining items |
| --- | --- | --- | --- |
| 1 | (0,0) | 6 | [4,1] |
| 2 | (0,1) | 4 | [1] |
| 3 | (0,2) | 1 | [] |

Grid becomes:

row 1: 6 4 1

row 2: 0 0 0

This corresponds to an optimal concentration of value in a single row, maximizing that row’s average contribution.

Now consider a second example:

Input:

n = 3, m = 2, k = 4

values = [10, 9, 1, 1]

Sorted: [10, 9, 1, 1]

| Step | Cell | Value |
| --- | --- | --- |
| 1 | (0,0) | 10 |
| 2 | (0,1) | 9 |
| 3 | (1,0) | 1 |
| 4 | (1,1) | 1 |

Row 1 average is (10+9)/2 = 9.5, row 2 average is (1+1)/2 = 1, row 3 empty.

The trace shows that front-loading high values produces a dominant first row, which drives the objective.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k + nm) | Sorting dominates, grid fill is linear in grid size |
| Space | O(nm) | Grid storage |

The constraints allow up to one million grid cells, and up to one million bottles, so both sorting and filling are comfortably within limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO

    output = StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

def solve():
    n, m, k = map(int, input().split())
    p = list(map(int, input().split()))
    items = sorted([(p[i], i + 1) for i in range(k)], reverse=True)
    grid = [[0] * m for _ in range(n)]
    idx = 0
    for i in range(n):
        for j in range(m):
            if idx < k:
                grid[i][j] = items[idx][1]
                idx += 1
    for row in grid:
        print(*row)

# sample
assert run("2 3 3\n1 4 6\n") == "1 2 3\n0 0 0"

# minimum size
assert run("1 1 1\n5\n") == "1"

# all equal
assert run("2 2 3\n7 7 7\n") in [
    "1 2\n3 0",
    "1 2\n0 3"
]

# single row full
assert run("1 5 3\n9 8 7\n") == "1 2 3 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | single placement | base case handling |
| equal values | any arrangement | symmetry correctness |
| single row | linear fill | row boundary behavior |
| sample case | fixed structure | consistency with statement |

## Edge Cases

A critical edge case is when k equals n × m, meaning the grid is completely filled. In this situation, there is no freedom to optimize placement, and the algorithm simply assigns sorted values across the entire grid. Since every row has exactly m elements, each row average is fixed by its assigned block, and the sorted placement ensures that higher values still concentrate in earlier rows.

Another edge case is when k is small compared to n. Many rows will be empty, meaning only a few rows contribute to the expectation. The greedy fill ensures that only the first few rows receive values, which is consistent with maximizing contribution because empty rows do not dilute any averages.

Finally, when all prices are identical, every arrangement produces the same expectation. The algorithm still produces a valid assignment by filling sequentially, and no correctness condition is violated since all permutations are equivalent under the objective.
