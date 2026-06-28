---
title: "CF 104720C - Cooking Class"
description: "We are given a fixed pool of competitors, each with a known skill value, and Autumn with her own initial skill. She can choose exactly one upgrade from a list of possible boosts, and each boost simply adds a fixed amount to her base skill."
date: "2026-06-29T06:11:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 77
verified: false
draft: false
---

[CF 104720C - Cooking Class](https://codeforces.com/problemset/problem/104720/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed pool of competitors, each with a known skill value, and Autumn with her own initial skill. She can choose exactly one upgrade from a list of possible boosts, and each boost simply adds a fixed amount to her base skill. After choosing one boost, all competitors are ranked purely by skill, with ties sharing the same rank and skipping ranks accordingly.

The task is to determine which single boost Autumn should pick in order to achieve the best possible final rank.

A key detail is that rank depends only on how many competitors strictly exceed Autumn’s final skill. If we know Autumn’s final skill value $X$, then her rank is simply $1 + \#\{S_i > X\}$. Equal skills do not affect rank beyond tying.

The constraints are large: up to $2 \cdot 10^5$ competitors and $2 \cdot 10^5$ boosts. This immediately rules out any solution that recomputes comparisons against all competitors for each boost in a naive way. A double loop over boosts and competitors would require up to $4 \cdot 10^{10}$ comparisons, which is far beyond feasible limits.

The main computational task is therefore: for many candidate values $X = S_A + P_i$, quickly compute how many array elements exceed $X$, and take the minimum resulting rank.

A few edge cases matter:

If all boosts are very small, Autumn may still rank poorly, and the answer is not always 1. For example, if competitors are $[10, 20, 30]$, Autumn is $S_A = 1$, and boosts are $[0, 0]$, then every final score is 1, and everyone outranks her, so rank is 4.

If boosts are large enough, she can surpass all competitors and get rank 1.

If many competitors have the same skill as the final value, they tie below or equal, but do not increase rank unless strictly greater.

## Approaches

A brute-force solution would try each boost $P_i$, compute Autumn’s final skill $X_i = S_A + P_i$, then scan all competitors to count how many have skill greater than $X_i$. This correctly computes the rank for each choice, and then we take the minimum. The correctness is immediate since it directly follows the ranking definition.

However, each evaluation costs $O(N)$, and there are $M$ boosts, giving $O(NM)$. With $2 \cdot 10^5$ in both dimensions, this is too large.

The key observation is that the competitor list is static, and for each candidate $X_i$ we only need a count of elements greater than it. If we sort the competitor skills once, then for any threshold $X$, the number of elements greater than $X$ can be found by binary search. Specifically, if we sort in increasing order, we can find the first position where value exceeds $X$, and subtract from $N$.

This reduces each query from linear time to logarithmic time. We then evaluate all boosts in $O(M \log N)$, which is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NM)$ | $O(1)$ extra | Too slow |
| Sorting + Binary Search | $O(N \log N + M \log N)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read all competitor skills and Autumn’s initial skill. Keep competitors separate from Autumn’s value.
2. Sort the competitor skill list in increasing order. This enables fast threshold counting.
3. For each boost $P_i$, compute Autumn’s final skill $X = S_A + P_i$.
4. For each $X$, compute how many competitors have strictly greater skill using binary search on the sorted array.

The first index where value is greater than $X$ gives the boundary between ≤X and >X.
5. Convert that count into rank using $rank = 1 + count\_greater$.
6. Track the minimum rank over all boosts and output it.

The binary search step is the only non-trivial part: we are effectively finding the upper bound of $X$ and measuring the suffix length of the array.

### Why it works

Sorting preserves all relative comparisons among competitors. For any candidate final skill $X$, the set of competitors who outrank Autumn is exactly the suffix of the sorted array consisting of values strictly greater than $X$. Since sorting guarantees all such elements are contiguous at the end, a single binary search correctly identifies the split point. Because rank depends only on the count of strictly greater elements, minimizing rank is equivalent to minimizing this suffix size over all boosts.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, M = map(int, input().split())
arr = list(map(int, input().split()))
S_A = arr[-1]
competitors = arr[:-1]

competitors.sort()

def count_greater(x):
    lo, hi = 0, len(competitors)
    while lo < hi:
        mid = (lo + hi) // 2
        if competitors[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return len(competitors) - lo

P = list(map(int, input().split()))

best = float('inf')

for p in P:
    x = S_A + p
    greater = count_greater(x)
    rank = 1 + greater
    if rank < best:
        best = rank

print(best)
```

The code separates Autumn’s skill from the competitors and sorts the competitor array once. The helper function `count_greater` performs a standard upper-bound binary search, returning how many elements exceed the threshold.

A subtle point is the strict inequality: only values strictly greater than $X$ affect rank. That is why the binary search advances past values `<= x`, not `>= x`.

We maintain the minimum rank across all boosts and output it at the end.

## Worked Examples

### Example 1

Input:

```
N = 3, M = 2
competitors = [10, 20, 30], S_A = 5
P = [1, 20]
```

Sorted competitors: [10, 20, 30]

| Boost | X = S_A + P | First > X index | Greater count | Rank |
| --- | --- | --- | --- | --- |
| 1 | 6 | 0 | 3 | 4 |
| 20 | 25 | 2 | 1 | 2 |

Best rank is 2.

This demonstrates that even large boosts do not always guarantee rank 1; only exceeding the maximum competitor value does.

### Example 2

Input:

```
N = 4, M = 3
competitors = [3, 3, 3, 3], S_A = 3
P = [0, 1, 5]
```

Sorted competitors: [3, 3, 3, 3]

| Boost | X | First > X index | Greater count | Rank |
| --- | --- | --- | --- | --- |
| 0 | 3 | 4 | 0 | 1 |
| 1 | 4 | 4 | 0 | 1 |
| 5 | 8 | 4 | 0 | 1 |

This shows tie behavior: equal skills do not increase rank, since rank depends only on strictly greater values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + M \log N)$ | Sorting once plus binary search per boost |
| Space | $O(1)$ auxiliary | Only sorting and input storage |

The complexity is comfortably within limits since both $N$ and $M$ are at most $2 \cdot 10^5$, and logarithmic factors are small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    N, M = map(int, input().split())
    arr = list(map(int, input().split()))
    S_A = arr[-1]
    competitors = arr[:-1]
    competitors.sort()

    def count_greater(x):
        lo, hi = 0, len(competitors)
        while lo < hi:
            mid = (lo + hi) // 2
            if competitors[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        return len(competitors) - lo

    P = list(map(int, input().split()))

    best = 10**18
    for p in P:
        x = S_A + p
        best = min(best, 1 + count_greater(x))

    return str(best)

# sample
assert run("3 2\n10 20 30 5\n1 20\n") == "2"

# minimum size
assert run("1 1\n5 3\n10\n") == "1"

# all equal
assert run("4 2\n5 5 5 5 5\n0 1\n") == "1"

# no boost advantage
assert run("3 2\n10 20 30 1\n0 0\n") == "4"

# already strongest possible
assert run("3 2\n1 2 3 10\n1 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal size | 1 | single competitor edge |
| all equal values | 1 | tie handling |
| zero boost case | 4 | worst rank behavior |
| already dominant | 1 | maximum threshold correctness |

## Edge Cases

A critical edge case is when Autumn’s final score equals many competitors. For input:

```
3 1
5 5 5 5
0
```

sorting yields [5, 5, 5]. With $X = 5$, the binary search finds no element strictly greater, so rank is 1. The algorithm correctly ignores equal values.

Another edge case is when boosts are very large but not necessary to compute all comparisons. For:

```
3 2
100 200 300 10
1 1000
```

the second boost produces $X = 1010$, binary search returns 0 greater elements immediately, giving rank 1 without scanning the array.

A final edge case is when all competitors are strictly greater than every possible $X$. Then every query returns rank $N+1$, and the algorithm consistently returns that value since every binary search yields full suffix size.
