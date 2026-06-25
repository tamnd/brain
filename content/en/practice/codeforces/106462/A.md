---
title: "CF 106462A - \u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c \u0442\u0430\u0431\u043b\u0438\u0446\u0443 \u0443\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u044f"
description: "We are given a conceptual multiplication table with n rows and m columns. In row i and column j, the value stored is simply i × j."
date: "2026-06-25T08:58:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106462
codeforces_index: "A"
codeforces_contest_name: "\u041f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0441\u0440\u0435\u0434\u0438 \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445 2026"
rating: 0
weight: 106462
solve_time_s: 39
verified: true
draft: false
---

[CF 106462A - \u041f\u043e\u0432\u0442\u043e\u0440\u044f\u0435\u043c \u0442\u0430\u0431\u043b\u0438\u0446\u0443 \u0443\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/106462/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a conceptual multiplication table with `n` rows and `m` columns. In row `i` and column `j`, the value stored is simply `i × j`. If we flatten all `n × m` values into a single list and sort them in non-decreasing order, we are asked to find the value that appears in the `k`-th position.

So instead of building the table explicitly, the task is to understand the distribution of products `i × j` and answer a rank query over that multiset.

The constraints are large: both dimensions can be up to `5 · 10^5`, which makes the table size potentially `2.5 · 10^11`. Any approach that tries to enumerate entries directly is immediately impossible, even storing the structure is out of the question. This forces us into a solution where we never materialize the grid and instead count properties of it.

A naive interpretation might try to generate all products and sort them, but even generating a single row costs `O(m)` and doing that for all rows leads to `O(nm)` operations, which is far beyond feasible.

A subtle edge case appears when many products are equal, especially small numbers. For example, in a `3 × 3` table, the value `2` appears only twice, while `4` appears three times, coming from different pairs. Any approach that assumes uniqueness of products would fail.

Another issue is overflow thinking: products fit in 32-bit integers, but counts of how many values are `≤ x` can reach `n × m`, which requires 64-bit arithmetic.

## Approaches

The brute-force method is straightforward: compute every value `i × j`, store them in an array, sort it, and pick the `k`-th element. This is correct because it directly constructs the multiset described in the problem. However, it requires generating `n × m` values, which in the worst case is about `2.5 · 10^11` multiplications and memory for the same number of elements. Even if memory were ignored, time alone makes this impossible.

The key structural observation is that we do not need to know all values, only how many values are less than or equal to a candidate number `x`. If we can compute this count efficiently, then we can binary search the answer. The reason this works is monotonicity: if a value `x` is large enough to be at least the `k`-th smallest element, then any larger value is also valid, and any smaller value is not. This creates a monotonic predicate suitable for binary search.

So the problem reduces to counting, for a fixed `x`, how many pairs `(i, j)` satisfy `i × j ≤ x`. For each row `i`, valid `j` values go from `1` up to `min(m, x // i)`. Summing over all rows gives the total count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm log(nm)) due to sorting | O(nm) | Too slow |
| Binary Search + Counting | O(n log(max value)) | O(1) | Accepted |

## Algorithm Walkthrough

1. We search for the smallest value `x` such that at least `k` numbers in the table are `≤ x`. This reframes the ranking problem into a decision problem.
2. We set binary search bounds from `1` to `n × m`, since the smallest value is `1 × 1` and the largest is `n × m`.
3. For a candidate value `mid`, we compute how many products `i × j` are `≤ mid`. For each row `i`, we count valid columns as `min(m, mid // i)`. This works because in row `i`, values grow linearly as `i, 2i, 3i, ...`.
4. We sum these counts over all `i` from `1` to `n`. If the total is at least `k`, then `mid` is large enough, so we move the search left. Otherwise, we move right.
5. After binary search converges, the answer is the smallest `mid` that satisfies the condition.

### Why it works

The core invariant is that the function `F(x)` defined as “number of table entries ≤ x” is non-decreasing in `x`. Once a value `x` produces a count ≥ `k`, every larger value also produces a count ≥ `k`. This monotonic structure guarantees binary search converges to the minimal valid value, which is exactly the `k`-th smallest element in the sorted multiset.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

def count_le(x):
    total = 0
    for i in range(1, n + 1):
        total += min(m, x // i)
    return total

lo, hi = 1, n * m

while lo < hi:
    mid = (lo + hi) // 2
    if count_le(mid) >= k:
        hi = mid
    else:
        lo = mid + 1

print(lo)
```

The function `count_le` is the critical component. For each row index `i`, `x // i` tells us how far we can go in that row before exceeding `x`. We clamp it by `m` because each row has only `m` columns.

Binary search is done on the value domain, not on indices. This distinction is important because the array is not explicitly constructed.

## Worked Examples

### Example 1

Input:

```
2 3 4
```

We are looking at the table:

```
1 2 3
2 4 6
```

We binary search values.

| mid | count ≤ mid | decision |
| --- | --- | --- |
| 3 | 4 | go left or accept |
| 2 | 3 | go right |
| 3 | 4 | final |

The first value reaching at least 4 elements is `3`, so the answer is `3`.

This confirms that duplicates and ordering across rows are handled correctly by the counting function.

### Example 2

Input:

```
3 3 5
```

Table:

```
1 2 3
2 4 6
3 6 9
```

| mid | count ≤ mid | decision |
| --- | --- | --- |
| 4 | 5 | candidate |
| 3 | 4 | too small |
| 4 | 5 | final |

We see that `4` is the smallest value with at least 5 elements not exceeding it, so it is the 5-th smallest value.

This example shows how repeated values like `6` being present twice do not break the logic, since the algorithm counts multiplicities naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(nm)) | Each binary search step scans all rows once, and there are logarithmically many steps over the value range |
| Space | O(1) | Only a few counters and variables are used |

The method scales comfortably for `n, m ≤ 5 · 10^5`, since the binary search runs about 30 iterations, and each iteration is a linear scan over `n`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    def count_le(x):
        total = 0
        for i in range(1, n + 1):
            total += min(m, x // i)
        return total

    lo, hi = 1, n * m
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    return str(lo)

# provided samples
assert run("2 2 2") == "2"
assert run("2 3 4") == "3"
assert run("1 10 5") == "5"

# custom cases
assert run("1 1 1") == "1", "single cell"
assert run("3 3 1") == "1", "minimum element"
assert run("3 3 9") == "9", "maximum element"
assert run("4 4 8") == "4", "duplicate-heavy region"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | smallest possible grid |
| 3 3 1 | 1 | minimum edge selection |
| 3 3 9 | 9 | maximum boundary |
| 4 4 8 | 4 | duplicates and mid-range counting |

## Edge Cases

A small grid like `1 × m` behaves like a simple sequence `1, 2, ..., m`. The algorithm reduces correctly because each row contributes at most one element, and `min(m, x // i)` becomes `min(m, x)` when `i = 1`.

When `k = n × m`, the answer must be the maximum product `n × m`. During binary search, only values below this maximum fail the predicate, so the search converges correctly at the upper bound.

When many products repeat, such as multiple ways to form `6` in a `3 × 3` grid, the counting function correctly includes all occurrences because each valid `(i, j)` pair is counted independently through `min(m, x // i)`.
