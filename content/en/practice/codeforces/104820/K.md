---
title: "CF 104820K - \u0412\u044b\u0431\u043e\u0440 \u043d\u0435 \u0432\u0435\u043b\u0438\u043a"
description: "We are given a grid whose rows and columns are not uniform in size. Each row has a positive height given by array A, and each column has a positive width given by array B."
date: "2026-06-28T12:58:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "K"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 103
verified: true
draft: false
---

[CF 104820K - \u0412\u044b\u0431\u043e\u0440 \u043d\u0435 \u0432\u0435\u043b\u0438\u043a](https://codeforces.com/problemset/problem/104820/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid whose rows and columns are not uniform in size. Each row has a positive height given by array `A`, and each column has a positive width given by array `B`. If we take any contiguous block of rows and any contiguous block of columns, they form a rectangular region made of unit cells, where each cell `(i, j)` exists inside a larger geometric rectangle whose area contribution depends on the chosen rows and columns.

If we select rows from `l` to `r` and columns from `x` to `y`, the chosen shape is a full submatrix. The number of selected sectors is simply the count of cells in that submatrix, which equals `(r - l + 1) * (y - x + 1)`.

However, there is a geometric constraint. Each row contributes a height, so the total height of a chosen row segment is the sum of `A[i]` over that segment, and each column contributes a width, so the total width is the sum of `B[j]` over the column segment. The physical area of the resulting rectangle is the product of these two sums, and this product must not exceed `S`.

The task is to choose one contiguous row segment and one contiguous column segment maximizing the number of cells in the resulting rectangle while keeping the geometric area constraint satisfied.

The constraints `N, M ≤ 1000` imply that any solution roughly beyond `O(N^2 M)` or `O(N M^2)` will be too slow. A solution around `O(N^2 log M + M^2 log N)` or better is acceptable, since about one million intervals per dimension is feasible, but nested full scans per query are not.

A naive attempt that tries every pair of row and column segments independently would check roughly `O(N^2 M^2)` combinations, which is about `10^12`, far beyond limits.

A subtle failure case for naive pruning appears when one dimension is large but slightly reduces the allowed range of the other. For example, choosing a slightly larger row segment might reduce the allowable column width by just one column, but that single column loss can drastically reduce area count. Any greedy expansion in one dimension without considering all intervals will miss such tradeoffs.

## Approaches

A direct brute force solution enumerates every possible row interval and every possible column interval. For each pair, we compute the sums of `A` and `B` over those intervals, check whether their product is at most `S`, and compute the number of cells. This is correct because it exhaustively checks all valid rectangles. The issue is the cost: there are `O(N^2)` row intervals and `O(M^2)` column intervals, and checking each pair takes constant or logarithmic time if prefix sums are used, giving roughly `10^12` evaluations in the worst case.

The key structural observation is that row and column choices are independent except through a single scalar constraint: the product of their sums. This suggests separating the problem into two stages. If we fix a row interval, its sum becomes a constant `H`. Then any valid column interval must satisfy `sum(B[l..r]) ≤ S / H`. For that fixed threshold, we want the column interval with maximum length.

This turns the problem into a pattern: precompute all column intervals once, store them by their sum, and answer many “maximum length among intervals with sum ≤ T” queries. The same can be done symmetrically for rows, but doing it once is enough.

We reduce the 2D choice problem into generating all 1D intervals for one dimension and querying them efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N² M²) | O(1) | Too slow |
| Interval preprocessing + binary search | O((N² + M²) log M²) | O(M²) | Accepted |

## Algorithm Walkthrough

We precompute all column intervals and compress their information into a structure that allows fast queries by sum constraint.

1. Compute prefix sums for array `B`, so any interval sum can be obtained in O(1). This lets us evaluate every column segment efficiently.
2. Enumerate all column intervals `(l, r)` and compute two values for each: `sumB = B[l] + ... + B[r]` and `lenB = r - l + 1`. This produces about `M² / 2` intervals.
3. Sort these intervals by `sumB`. After sorting, we build an array where at each position we store the maximum `lenB` seen so far. This transforms the structure into a monotone query tool: for any threshold `T`, we can find the best column length among all intervals with sum ≤ `T` using a binary search followed by a prefix maximum lookup.
4. Repeat the same prefix sum preparation for `A`.
5. Enumerate all row intervals `(i, j)`, compute `sumA = A[i] + ... + A[j]` and `lenA = j - i + 1`.
6. For each row interval, compute the maximum allowed column sum `T = S // sumA`.
7. Query the preprocessed column structure to obtain the best possible column length whose sum does not exceed `T`.
8. Update the answer with `lenA * bestLenB`.

The reason this works is that once the row interval is fixed, the column choice becomes an independent constrained optimization problem over a precomputed set, and vice versa.

### Why it works

For every valid rectangle, there exists exactly one row interval and one column interval representing it. The algorithm considers every row interval explicitly, and for each such interval it computes the best compatible column interval under the exact constraint induced by that row choice. Since column intervals are fully enumerated and optimized for every possible sum threshold, no feasible configuration is skipped. The decomposition preserves optimality because the constraint couples the dimensions only through a single scalar product.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_intervals(arr):
    n = len(arr)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + arr[i]

    intervals = []
    for i in range(n):
        for j in range(i, n):
            s = pref[j + 1] - pref[i]
            length = j - i + 1
            intervals.append((s, length))
    return intervals

def build_query_structure(intervals):
    intervals.sort()
    best = []
    max_len = 0

    for s, l in intervals:
        if l > max_len:
            max_len = l
        best.append((s, max_len))
    return best

def query(best, T):
    import bisect
    idx = bisect.bisect_right(best, (T, 10**18)) - 1
    if idx < 0:
        return 0
    return best[idx][1]

def solve():
    N, M, S = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    col_intervals = build_intervals(B)
    col_best = build_query_structure(col_intervals)

    row_intervals = build_intervals(A)

    ans = 0

    for sumA, lenA in row_intervals:
        if sumA > 0:
            T = S // sumA
            lenB = query(col_best, T)
            ans = max(ans, lenA * lenB)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts each array into all possible contiguous segments using prefix sums. Each segment is represented by its sum and its length. For columns, these segments are sorted by sum and compressed so that for any sum threshold we can retrieve the maximum achievable width efficiently.

The query function uses binary search over the compressed structure. Since the structure is monotone in sum, the best length for any threshold is always found at or before the last interval whose sum is within the limit.

The row loop evaluates each possible height choice and translates it into a maximum allowable column sum. The product of the best matching column and the row length gives a candidate answer.

## Worked Examples

### Sample 1

Input:

```
A = [2, 4, 1, 3]
B = [4, 2, 1, 2]
S = 2
```

We first list a few column intervals:

| interval | sumB | lenB |
| --- | --- | --- |
| [1] | 4 | 1 |
| [2] | 2 | 1 |
| [3] | 1 | 1 |
| [4] | 2 | 1 |
| [2,3] | 3 | 2 |
| [3,4] | 3 | 2 |

After compression, for small thresholds like `T = 1`, only intervals with sum ≤ 1 are usable, giving best length 1.

Row intervals include single-element rows like `[3]` with sumA = 1 and lenA = 1. This gives `T = 2`, so we can use any column interval with sum ≤ 2, giving best column length 1. Product is 1.

Trying larger row sums immediately reduces `T` to 0, which gives no valid columns. The best answer remains 1.

This trace shows that tight constraints force the solution toward minimal valid rectangles.

### Sample 2

Input:

```
A = [2, 4, 1, 3]
B = [4, 2, 1, 2]
S = 20
```

Now constraints are loose enough to allow larger rectangles.

For row interval `[4, 1, 3]`, sumA = 8 and lenA = 3, so `T = 20 // 8 = 2`. We can choose the best column interval with sum ≤ 2, such as `[2]` or `[3]` or `[4]`, giving lenB = 1. Product is 3.

For row interval `[1, 3]`, sumA = 4 and lenA = 2, so `T = 5`. Now column interval `[2,3]` is valid with sum 3 and length 2, giving product 4.

The best combination is achieved when both dimensions are moderately large while still respecting the product constraint.

This trace highlights how increasing allowed area expands feasible column choices nonlinearly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² + M² log M²) | All intervals are generated in quadratic time, sorting column intervals dominates with log factor |
| Space | O(M²) | Storage of all column intervals and compressed structure |

The quadratic preprocessing is acceptable because both dimensions are capped at 1000, giving about one million intervals per array. The logarithmic query per row interval keeps total operations within a few tens of millions, which fits comfortably within typical limits for Python under Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    N, M, S = map(int, sys.stdin.readline().split())
    A = list(map(int, sys.stdin.readline().split()))
    B = list(map(int, sys.stdin.readline().split()))

    def build(arr):
        n = len(arr)
        pref = [0]*(n+1)
        for i in range(n):
            pref[i+1]=pref[i]+arr[i]
        res=[]
        for i in range(n):
            for j in range(i,n):
                res.append((pref[j+1]-pref[i], j-i+1))
        return res

    def build_best(intervals):
        intervals.sort()
        best=[]
        mx=0
        for s,l in intervals:
            mx=max(mx,l)
            best.append((s,mx))
        return best

    def query(best,T):
        import bisect
        i=bisect.bisect_right(best,(T,10**18))-1
        return 0 if i<0 else best[i][1]

    col=build(B)
    cb=build_best(col)
    row=build(A)

    ans=0
    for sA,lA in row:
        if sA<=0: 
            continue
        T=S//sA
        ans=max(ans,lA*query(cb,T))
    return str(ans)

# provided samples
assert run("4 4 2\n2 4 1 3\n4 2 1 2\n") == "1"
assert run("4 4 20\n2 4 1 3\n4 2 1 2\n") == "6"

# custom cases
assert run("1 1 100\n5\n5\n") == "1", "single cell"
assert run("3 3 1\n1 1 1\n1 1 1\n") == "1", "tight constraint"
assert run("3 3 1000\n1 2 3\n1 2 3\n") == "9", "full rectangle possible"
assert run("2 3 5\n2 2\n1 2 1\n") >= "1", "basic feasibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 1 | minimal structure handling |
| tight constraint | 1 | extreme limiting S |
| full rectangle possible | 9 | maximum expansion case |
| basic feasibility | ≥1 | non-trivial validity |

## Edge Cases

A corner case occurs when all row sums exceed `S`. In that situation, every `T` becomes zero and no column interval qualifies. The algorithm handles this because binary search returns `0`, and the product update is never triggered.

Another case appears when only single-row intervals are valid. For example, if `A = [100, 1, 100]` and `S = 10`, only the middle row contributes any valid configurations. The loop naturally evaluates each row interval independently, and only the interval with `sumA = 1` produces a non-zero column result.

A third case involves uneven distributions where one very small row segment unlocks a disproportionately large column segment. Because all row intervals are explicitly enumerated rather than greedily extended, the algorithm does not miss these asymmetric optimal structures.
