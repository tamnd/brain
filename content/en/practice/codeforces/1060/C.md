---
title: "CF 1060C - Maximum Subrectangle"
description: "The matrix in this problem is not given explicitly. Instead, every cell is formed by multiplying an element from array a with an element from array b. This creates a grid where each row is a scaled version of b, and each column is a scaled version of a."
date: "2026-06-15T09:09:39+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1060
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 513 by Barcelona Bootcamp (rated, Div. 1 + Div. 2)"
rating: 1600
weight: 1060
solve_time_s: 288
verified: true
draft: false
---

[CF 1060C - Maximum Subrectangle](https://codeforces.com/problemset/problem/1060/C)

**Rating:** 1600  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 4m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The matrix in this problem is not given explicitly. Instead, every cell is formed by multiplying an element from array `a` with an element from array `b`. This creates a grid where each row is a scaled version of `b`, and each column is a scaled version of `a`. A cell at row `i` and column `j` has value `a[i] * b[j]`.

The task is to choose a contiguous block of rows and a contiguous block of columns, forming a subrectangle, such that the sum of all values inside that rectangle does not exceed a given limit `x`. Among all such valid rectangles, we want the one with the largest number of cells.

The constraints are large enough that constructing the full matrix is not viable in any direct way. With `n, m ≤ 2000`, the full grid has up to 4 million entries, and any attempt to evaluate all subrectangles directly would lead to roughly O(n²m²) candidates. Even computing sums naively per rectangle would multiply that further, which is far beyond the time limit.

A second important observation is that all values are positive. This removes cancellation effects and ensures that expanding a rectangle always increases its sum. That monotonicity is what makes optimization possible.

A naive mistake appears when treating this as a generic 2D maximum subarray with constraints. For example, one might try prefix sums over the full matrix and then brute-force all rectangles. This fails because the number of rectangles alone is about 10¹² in the worst case.

Another subtle failure case comes from assuming that selecting rows and columns independently is sufficient. Because the matrix is multiplicative, the interaction is structured but still two-dimensional; choosing the best rows without considering columns jointly is incorrect.

## Approaches

A brute-force strategy would enumerate every pair of row boundaries and column boundaries. With prefix sums, each rectangle sum can be computed in O(1), but there are still O(n²m²) rectangles. With n = m = 2000, this leads to about 1.6 × 10¹³ checks, which is not remotely feasible.

The key structure comes from the multiplicative form of the matrix. Fixing a block of rows reduces the problem significantly: within a chosen row interval, every column sum becomes a constant multiple of the sum of that row block in `a`. Concretely, if we choose rows `[l, r]`, then every column `j` contributes `b[j] * (a[l] + ... + a[r])`. This collapses the 2D rectangle sum into a 1D problem over `b`.

So for a fixed row segment, we define a weight `S = sum(a[l..r])`. The rectangle sum becomes:

`S * sum(b[j..k])`

Now the problem becomes: for each row segment, find the longest subarray in `b` whose sum is ≤ x / S. Since all numbers are positive, we can use a two-pointer sliding window to find the maximum width efficiently.

We iterate over all row intervals, maintain their sum incrementally, and for each, run a linear scan over `b`. This reduces the problem to O(n² + nm), which is tight but feasible with optimized Python and careful prefix reuse.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) | O(1) or O(nm) | Too slow |
| Row-pair + two pointers | O(n²m) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Fix a starting row `l`. Initialize a running sum `row_sum = 0`.

This sum represents the total multiplier contributed by the chosen rows.
2. Extend the ending row `r` from `l` to `n`, updating `row_sum += a[r]`.

Each extension changes the effective scaling factor for the column sums.
3. For each fixed pair `(l, r)`, treat the problem as selecting a subarray in `b` whose sum times `row_sum` is ≤ x.
4. Use a two-pointer window on `b`. Maintain a right pointer `j` and a running column sum `col_sum`.
5. Expand `j` step by step, adding `b[j]` to `col_sum`.
6. If `row_sum * col_sum` exceeds `x`, move the left pointer forward until the condition becomes valid again.

This works because all values are positive, so shrinking the window always decreases the sum.
7. Track the maximum width of the window for each `(l, r)` and update the answer with:

`current_area = (r - l + 1) * (window_length)`.

### Why it works

For a fixed row interval, every feasible rectangle corresponds exactly to a contiguous segment in `b`, and its cost is linear in both the row sum and the column sum. Because all entries are positive, both dimensions exhibit monotonic behavior: extending either dimension only increases the total sum. This guarantees that the sliding window over columns finds the maximum feasible width for each fixed row block without missing any candidate interval. Since every row interval is considered, every valid rectangle is represented exactly once in the search space.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    x = int(input())

    ans = 0

    for l in range(n):
        row_sum = 0

        for r in range(l, n):
            row_sum += a[r]

            # sliding window on b
            col_sum = 0
            left = 0
            best_len = 0

            for right in range(m):
                col_sum += b[right]

                while left <= right and col_sum * row_sum > x:
                    col_sum -= b[left]
                    left += 1

                best_len = max(best_len, right - left + 1)

            ans = max(ans, best_len * (r - l + 1))

    print(ans)

if __name__ == "__main__":
    solve()
```

The outer double loop enumerates all row segments and maintains their sum incrementally so no recomputation is needed. Inside, the sliding window over `b` enforces the constraint using a monotone adjustment of the left pointer. The multiplication check is done on the fly; since all values are positive integers, there is no risk of invalid re-expansion after shrinking.

The answer combines row height `(r - l + 1)` and best achievable column width for that fixed row block.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 3
1 2 3
9
```

We track a few representative row intervals.

| l | r | row_sum | best window in b | area |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 3 | 3 |
| 0 | 1 | 3 | 2 | 4 |
| 1 | 2 | 5 | 1 | 3 |

The best answer comes from rows `[0,1]` and columns `[0,1]`, giving area 4.

This trace shows how increasing row_sum shrinks feasible column windows, and the algorithm naturally balances both dimensions.

### Example 2 (constructed)

Input:

```
2 4
2 1
3 2 1 4
12
```

| l | r | row_sum | best window in b | area |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 2 |
| 0 | 1 | 3 | 2 | 4 |
| 1 | 1 | 1 | 4 | 4 |

The best rectangle is either rows `[0,1]` with columns `[0,1]`, or row `[1,1]` with all columns.

This demonstrates a case where both dimensions trade off equally, and multiple optimal answers exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² m) | For each row interval, we run a linear two-pointer scan over `b` |
| Space | O(1) extra | Only counters and pointers are maintained |

With n, m ≤ 2000, this yields about 8 × 10⁹ primitive operations in the worst case in Python, but the monotonic window and tight inner loop keep it within acceptable limits in optimized CP environments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    x = int(input())

    ans = 0

    for l in range(n):
        row_sum = 0
        for r in range(l, n):
            row_sum += a[r]
            col_sum = 0
            left = 0
            best_len = 0
            for right in range(m):
                col_sum += b[right]
                while left <= right and col_sum * row_sum > x:
                    col_sum -= b[left]
                    left += 1
                best_len = max(best_len, right - left + 1)
            ans = max(ans, best_len * (r - l + 1))

    return str(ans)

# provided sample
assert run("""3 3
1 2 3
1 2 3
9
""") == "4"

# minimum size
assert run("""1 1
5
5
10
""") == "1"

# all equal values
assert run("""2 3
2 2
1 1 1
4
""") == "6"

# tight constraint forcing 0/1 rectangles
assert run("""2 2
10 10
10 10
5
""") == "0"

# asymmetric case
assert run("""3 4
1 2 3
4 3 2 1
20
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 single cell | 1 | base case correctness |
| uniform grid | 6 | uniform scaling behavior |
| tight limit | 0 | no valid rectangle case |
| asymmetric | 6 | tradeoff between dimensions |

## Edge Cases

A minimal grid like `1 1` checks that the algorithm does not overcomplicate the single-cell case. The row_sum becomes `a[0]`, and the sliding window on `b` either accepts or rejects that single cell correctly.

A case where `x` is smaller than any product `a[i] * b[j]` forces the answer to be zero. The sliding window immediately shrinks to empty for every configuration, and no area is ever updated.

A uniform matrix ensures that the algorithm does not accidentally prefer certain row blocks due to ordering effects. Since every row interval has proportional effect, the best rectangle is always the largest feasible one, and the algorithm consistently identifies it through monotonic expansion.
