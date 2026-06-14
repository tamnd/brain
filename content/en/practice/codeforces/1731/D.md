---
title: "CF 1731D - Valiant's New Map"
description: "We are given several independent grids, each grid representing a city map where every cell contains a building height. From each grid, we must choose a square subgrid of size $l times l$ such that every cell inside that square has height at least $l$."
date: "2026-06-15T02:56:24+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1731
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 841 (Div. 2) and Divide by Zero 2022"
rating: 1700
weight: 1731
solve_time_s: 357
verified: true
draft: false
---

[CF 1731D - Valiant's New Map](https://codeforces.com/problemset/problem/1731/D)

**Rating:** 1700  
**Tags:** binary search, brute force, data structures, dp, two pointers  
**Solve time:** 5m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent grids, each grid representing a city map where every cell contains a building height. From each grid, we must choose a square subgrid of size $l \times l$ such that every cell inside that square has height at least $l$. The task is to find the maximum possible value of $l$ for each test case.

The key difficulty is that the constraint couples geometry with values: enlarging the square makes the requirement stricter because both the side length and the minimum allowed height increase together. This makes the problem fundamentally different from a standard “largest square of ones” type task where the threshold is fixed.

The constraints imply a total of at most $10^6$ cells across all test cases. This immediately rules out any approach that is superlinear per test case such as recomputing answers for every candidate square in a naive way with $O(n^3)$ or even $O(n^2 m)$ behavior. A solution that performs roughly $O(nm \log \min(n,m))$ or $O(nm)$ per test case aggregate is acceptable.

A few edge behaviors are easy to miss. If all values are small, for example a grid filled with 1s, then any square larger than $1 \times 1$ immediately fails because the requirement already forces values to be at least the side length. Conversely, if values are large but scattered, a large value in isolation does not help unless it forms a dense region.

A common mistake is treating the condition as if it only depends on square size or only on values. For instance, assuming “largest square where all values are at least 1” is always optimal ignores that increasing $l$ increases the threshold itself.

## Approaches

A brute-force solution tries every possible top-left corner and every possible square size. For each candidate square, it checks whether all cells satisfy the height condition. This involves up to $O(nm)$ checks per square, and there are $O(nm)$ squares, leading to a worst-case complexity around $O(n^2 m^2)$, which is far beyond feasible limits for $10^6$ total cells.

The key observation is that the condition for a fixed $l$ becomes a standard binary grid problem. If we decide a candidate side length $l$, we only care whether there exists an $l \times l$ submatrix where all values are at least $l$. This transforms the grid into a binary matrix where cells are valid or invalid depending on whether they meet the threshold.

For a fixed threshold, we can compute the largest all-ones square using a dynamic programming recurrence that tracks the largest square ending at each cell. If any cell achieves value at least $l$, then a valid square exists.

Since feasibility is monotonic in $l$ (if a square works for $l$, it also works for smaller values), we can binary search the answer over $l$. Each check runs in linear time over the grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3 m^3)$ | $O(1)$ | Too slow |
| Binary Search + DP | $O(nm \log \min(n,m))$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to checking whether a given side length $l$ is feasible.

1. For a fixed candidate $l$, convert the grid into a binary grid where a cell is 1 if its height is at least $l$, otherwise 0. This step encodes the constraint directly into structure, so geometry is all that remains.
2. Build a dynamic programming table where $dp[i][j]$ represents the size of the largest all-ones square ending at cell $(i,j)$. If the current cell is valid, we extend the smallest of the three neighboring squares. Otherwise it is zero. This works because any square ending at $(i,j)$ must extend valid squares from above, left, and diagonally up-left.
3. While filling the DP table, if any $dp[i][j]$ reaches at least $l$, we immediately know a valid $l \times l$ square exists and can stop early.
4. Wrap this feasibility check inside a binary search over $l$ from 1 to $\min(n,m)$. If a value $l$ is feasible, we try larger values; otherwise we reduce the range.
5. The final answer is the largest feasible $l$.

The DP recurrence is:

$dp[i][j] = \begin{cases} 1 + \min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) & \text{if } a_{i,j} \ge l \\ 0 & \text{otherwise} \end{cases}$

### Why it works

Every valid square ending at a cell must contain a smaller square ending at each of its three predecessor directions. If any of those directions breaks the condition, the square cannot be extended. The recurrence captures exactly the largest possible square anchored at each position, and any valid $l \times l$ square must appear as a DP value reaching at least $l$. This makes the check both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(l, n, m, a):
    dp = [0] * (m + 1)
    prev = [0] * (m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1][j-1] >= l:
                dp[j] = min(prev[j], dp[j-1], prev[j-1]) + 1
                if dp[j] >= l:
                    return True
            else:
                dp[j] = 0
        prev, dp = dp, prev
    return False

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        
        lo, hi = 1, min(n, m)
        ans = 1
        
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, n, m, a):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates feasibility checking from optimization. The `can` function encodes the DP logic while scanning row by row, using only two rolling arrays to keep memory linear in the number of columns.

The binary search drives the final answer because feasibility is monotonic in $l$: once a square of size $l$ exists, all smaller sizes are automatically possible since both the size requirement and height threshold decrease together.

A subtle implementation detail is early exit inside the DP loop. Once any cell achieves a square of size at least $l$, further computation is unnecessary for that test, which significantly improves performance in dense cases.

## Worked Examples

### Example 1

Consider a small grid:

```
3 3
5 5 5
5 5 5
5 5 5
```

We check candidate values of $l$.

| l | DP outcome (key idea) | feasible |
| --- | --- | --- |
| 1 | all cells valid | yes |
| 2 | 2x2 squares exist | yes |
| 3 | 3x3 square exists | yes |

The binary search will converge to 3, which matches the full grid size.

This demonstrates the case where structure is uniform and the answer is limited only by geometry.

### Example 2

```
2 3
1 2 3
2 3 4
```

For $l=2$, we require all cells in a 2x2 square to be at least 2. Only one such region partially satisfies this, but one cell fails the threshold constraint, so no 2x2 square works.

| l | feasible |
| --- | --- |
| 1 | yes |
| 2 | no |

The answer is 1, showing the interaction between increasing size and increasing threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm \log \min(n,m))$ | each binary search step runs a full DP scan |
| Space | $O(m)$ | rolling arrays store only previous row states |

The total number of cells across all test cases is bounded by $10^6$, so even with about 20 iterations of binary search, the total operations remain comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def can(l, n, m, a):
        dp = [0] * (m + 1)
        prev = [0] * (m + 1)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if a[i-1][j-1] >= l:
                    dp[j] = min(prev[j], dp[j-1], prev[j-1]) + 1
                    if dp[j] >= l:
                        return True
                else:
                    dp[j] = 0
            prev, dp = dp, prev
        return False

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        lo, hi = 1, min(n, m)
        ans = 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, n, m, a):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""4
2 2
2 3
4 5
1 3
1 2 3
2 3
4 4 3
2 1 4
5 6
1 9 4 6 5 8
10 9 5 8 11 6
24 42 32 8 11 1
23 1 9 69 13 3
13 22 60 12 14 17
""") == """2
1
1
3"""

# custom cases
assert run("""1
1 1
5
""") == "1", "min case"

assert run("""1
2 2
1 1
1 1
""") == "1", "all small values"

assert run("""1
3 3
9 9 9
9 9 9
9 9 9
""") == "3", "all large values"

assert run("""1
3 3
1 2 3
4 5 6
7 8 9
""") == "2", "mixed grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single cell | 1 | minimal boundary |
| all ones 2x2 | 1 | threshold restriction |
| all high 3x3 | 3 | full feasibility |
| increasing grid | 2 | non-uniform structure |

## Edge Cases

A single-cell grid behaves trivially because the only possible square has size 1, and the threshold requirement is always satisfied when the value is at least 1.

A uniform low grid such as all ones ensures that any attempt to form squares larger than 1 fails immediately since the height constraint scales with the square size, forcing rejection regardless of geometry.

A uniform high grid such as all nines makes the answer purely geometric, and the DP will propagate maximum square sizes until limited by the grid boundary rather than values.
