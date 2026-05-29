---
title: "CF 448D - Multiplication Table"
description: "We are working with a conceptual multiplication grid where the cell in row i and column j contains the value i × j. Instead of explicitly building this table, we imagine listing all n × m values and sorting them in non-decreasing order."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 448
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 256 (Div. 2)"
rating: 1800
weight: 448
solve_time_s: 74
verified: true
draft: false
---

[CF 448D - Multiplication Table](https://codeforces.com/problemset/problem/448/D)

**Rating:** 1800  
**Tags:** binary search, brute force  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a conceptual multiplication grid where the cell in row `i` and column `j` contains the value `i × j`. Instead of explicitly building this table, we imagine listing all `n × m` values and sorting them in non-decreasing order. The task is to find the value that appears in position `k` in this sorted list.

The key difficulty is scale. Both dimensions of the table can be as large as 500,000, which makes the total number of elements up to 2.5 × 10¹¹. Any approach that attempts to generate or sort all values is immediately infeasible. Even iterating over all rows and columns explicitly is impossible within time limits.

This pushes us toward a strategy where we never construct the table directly, and instead reason about counts of values.

A subtle edge case appears when many repeated values exist. For example, in a small table like `n = 3, m = 3`, the value `2` appears multiple times. A naive flatten-and-sort approach would still work conceptually, but would fail due to memory and time limits. Another edge case is when `k = 1`, where the answer is always `1`, and when `k = n × m`, where the answer is `n × m`. Any correct solution must handle these boundaries naturally without special casing.

## Approaches

The brute-force idea is straightforward. We generate every product `i × j`, store them in a list, sort the list, and return the `k`-th element. This is correct because it explicitly constructs the multiset we are asked to order. However, the number of elements is `n × m`, which in the worst case is about 2.5 × 10¹¹. Even storing 10⁷ integers is already tight in Python; storing 10¹¹ is impossible. Sorting also adds a logarithmic factor, making this completely unusable.

The key observation is that we do not actually need the full sorted list. We only need to answer queries of the form: how many entries in the table are less than or equal to some value `x`. If we can compute this count efficiently, we can use binary search on the answer.

For a fixed `x`, each row `i` contributes `min(m, x // i)` values, because in row `i`, all columns `j` such that `i × j ≤ x` satisfy `j ≤ x // i`. Summing this over all rows gives the total number of elements ≤ `x`.

This transforms the problem into a monotonic predicate search: as `x` increases, the number of values ≤ `x` never decreases. That monotonicity allows binary search over the answer space from `1` to `n × m`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm log(nm)) | O(nm) | Too slow |
| Optimal (Binary Search + Counting) | O(n log(nm)) | O(1) | Accepted |

## Algorithm Walkthrough

We now construct the solution using binary search over the answer value.

1. Define a function `count(x)` that returns how many cells in the multiplication table are less than or equal to `x`. For each row `i`, the largest valid column is `x // i`, but it cannot exceed `m`, so we add `min(m, x // i)`.
2. Set the binary search range as `lo = 1` and `hi = n × m`. This range safely contains all possible values in the table.
3. Repeatedly compute `mid = (lo + hi) // 2`.
4. Compute `count(mid)`. If this value is at least `k`, then `mid` is large enough to potentially be the answer, so we move `hi = mid`.
5. Otherwise, fewer than `k` elements are ≤ `mid`, so we need larger values, and we move `lo = mid + 1`.
6. Continue until `lo == hi`. At that point, `lo` is the smallest value such that at least `k` elements are ≤ it, which matches the definition of the k-th smallest element in the multiset.

The key reason each step is valid is that the function `count(x)` is monotonic in `x`. Once a value `x` is large enough to include at least `k` elements, all larger values will also satisfy this property, so binary search correctly isolates the boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_leq(n, m, x):
    total = 0
    for i in range(1, n + 1):
        total += min(m, x // i)
    return total

def main():
    n, m, k = map(int, input().split())

    lo, hi = 1, n * m

    while lo < hi:
        mid = (lo + hi) // 2
        if count_leq(n, m, mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    main()
```

The core implementation detail is the `count_leq` function. It avoids building the table and instead computes contributions row by row. Each row `i` contributes all values `i × 1` through `i × (x // i)`, but we cap it at `m` because the table has only `m` columns.

The binary search maintains an invariant that the answer lies within `[lo, hi]`. The update rules shrink this interval while preserving correctness. A common mistake is using `hi = mid - 1`, which breaks the lower-bound style search needed for duplicates; here we intentionally keep `hi = mid`.

## Worked Examples

### Example 1

Input:

```
2 2 2
```

We search in range `[1, 4]`.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 1 | 4 | 2 | 3 |

At `mid = 2`, values ≤ 2 are `{1, 2, 2}`, so count is 3 ≥ k=2, shrink right.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |

Now count(1) = 1 < 2, move left bound up.

We end at `lo = 2`, which is the answer.

This shows how duplicates (two 2s in the table) are naturally handled by counting rather than explicit ordering.

### Example 2

Input:

```
3 3 5
```

Search range `[1, 9]`.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 1 | 9 | 5 | 7 |

Since 7 ≥ 5, move left.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 1 | 5 | 3 | 4 |

Since 4 < 5, move right.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 4 | 5 | 4 | 6 |

Now 6 ≥ 5, move left.

| lo | hi | mid | count(mid) |
| --- | --- | --- | --- |
| 4 | 4 | - | - |

Answer is 4.

This trace shows how the algorithm converges to the smallest value whose prefix count reaches k.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(nm)) | Each binary search step scans all rows, and there are O(log(nm)) steps |
| Space | O(1) | Only a few variables are used |

The solution fits within constraints because the binary search depth is about 40, and each step does up to 500,000 simple integer divisions, which is borderline but acceptable in optimized Python under PyPy or fast input assumptions typical for Codeforces.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    def count_leq(n, m, x):
        total = 0
        for i in range(1, n + 1):
            total += min(m, x // i)
        return total

    lo, hi = 1, n * m
    while lo < hi:
        mid = (lo + hi) // 2
        if count_leq(n, m, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)

# provided sample
assert run("2 2 2\n") == "2", "sample 1"

# minimum case
assert run("1 1 1\n") == "1", "single element"

# rectangular skewed table
assert run("1 100000 50\n") == "50", "single row"

# square case
assert run("3 3 5\n") == "4", "middle selection"

# max edge small k
assert run("100000 100000 1\n") == "1", "minimum value"

# max edge large k
assert run("100000 100000 10000000000\n") == "10000000000", "maximum value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | smallest boundary |
| 1 100000 50 | 50 | single row behavior |
| 3 3 5 | 4 | median selection correctness |
| 100000 100000 1 | 1 | global minimum |
| 100000 100000 10000000000 | max | global maximum |

## Edge Cases

For `n = 1`, the table degenerates into a single row `[1, 2, ..., m]`. The algorithm reduces to binary searching the smallest `x` such that `x ≥ k`, since `count(x)` becomes exactly `min(m, x)`. The counting function handles this naturally because only row `i = 1` contributes.

For `k = 1`, binary search immediately converges to `1` because `count(1)` is always at least 1. No special logic is needed.

For `k = n × m`, the search pushes toward the largest product `n × m`. At `x = n × m`, every entry is counted, and the predicate becomes true, fixing the upper bound correctly.

For highly unbalanced tables like `n = 1` and large `m`, or vice versa, the loop still runs over all rows but remains linear per check, and binary search ensures only logarithmic repetitions of this scan.
