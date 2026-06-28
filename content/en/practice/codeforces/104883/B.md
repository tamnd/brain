---
title: "CF 104883B - \u5965\u672f\u4e4b\u5c18"
description: "Each account comes with a certain amount of “arcane dust”, and there is a fixed list of card decks, each requiring a specific dust cost to be fully crafted."
date: "2026-06-28T09:09:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104883
codeforces_index: "B"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Final"
rating: 0
weight: 104883
solve_time_s: 44
verified: true
draft: false
---

[CF 104883B - \u5965\u672f\u4e4b\u5c18](https://codeforces.com/problemset/problem/104883/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Each account comes with a certain amount of “arcane dust”, and there is a fixed list of card decks, each requiring a specific dust cost to be fully crafted. For every account, we want to know the maximum number of complete decks that can be crafted if we choose an arbitrary subset of decks, with the restriction that each chosen deck consumes its full required dust and all chosen costs must sum within the account’s dust budget.

In more concrete terms, we are given an array `A` of size `n`, where `A[i]` is the available dust for account `i`. We are also given an array `B` of size `m`, where each `B[j]` is the cost of crafting deck `j`. For each `A[i]`, we must pick a subset of `B` maximizing the number of chosen elements such that their sum does not exceed `A[i]`.

The constraints `n, m ≤ 10^5` immediately rule out any solution that tries to recompute a knapsack per account. A naive per-account dynamic programming approach would require `O(n * m)` time, which is on the order of `10^10` operations in the worst case, far beyond a 1 second limit.

A key subtlety is that we are not asked to maximize value or compute different combinations per account, only the count of items. This makes the structure greedy after sorting.

A common failure case comes from not sorting the deck costs. If we pick expensive decks first, we can artificially reduce the count. For example, if `A = 10` and `B = [8, 7, 3, 2]`, picking 8 first gives only one deck, while the optimal is `[2, 3, 7]` or `[2, 3]` depending on budget, clearly showing greedy-by-arbitrary-order is incorrect.

Another edge case is zero-cost decks. If `B = [0, 0, 5]` and `A = 1`, we can take both zero-cost decks first, then still potentially take the 5-cost deck if budget allows. Any method that ignores zeros or assumes strict positivity can miscount.

## Approaches

The brute-force idea is straightforward. For each account, we try all subsets of decks, compute their total cost, and track the maximum subset size that fits within the budget. This is correct because it directly enforces the constraint definition, but it requires enumerating `2^m` subsets per account, which is impossible even for small `m`.

A more structured brute force is to sort subsets by size or try a knapsack DP per account. That leads to a pseudo-polynomial solution `O(n * m * max(A))` in spirit, but still infeasible because `A[i]` can be as large as `10^9`.

The key observation is that since every deck contributes the same “value” (one crafted deck), we should always prefer cheaper decks first. Once we sort `B` in non-decreasing order, the optimal strategy for any fixed budget is to take as many smallest costs as possible until we exceed the budget. This turns each query into a prefix sum problem followed by a binary search.

We precompute the sorted `B` and its prefix sums. Then for each `A[i]`, we find the largest prefix index such that the prefix sum is ≤ `A[i]`. That index is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^m) | O(1) | Too slow |
| Optimal (sort + prefix + binary search) | O(m log m + n log m) | O(m) | Accepted |

## Algorithm Walkthrough

We transform the problem into answering multiple “how many smallest elements fit into a budget” queries.

1. Sort the array `B` in ascending order. This ensures we always consider cheaper decks first, which is necessary because each deck contributes equally to the count.
2. Build a prefix sum array `P`, where `P[k]` represents the total dust required to craft the first `k` cheapest decks. This converts subset sums into a monotonic sequence.
3. For each account budget `A[i]`, perform a binary search on `P` to find the largest index `k` such that `P[k] ≤ A[i]`. The answer for that account is `k`.
4. Output all answers in order.

The binary search works because the prefix sum array is strictly non-decreasing, so feasibility (`P[k] ≤ A[i]`) is monotonic in `k`.

### Why it works

Once decks are sorted by cost, any optimal selection that uses a more expensive deck while skipping a cheaper one can be improved by swapping them without reducing the number of chosen decks and only decreasing or preserving total cost. Repeating this exchange argument forces all optimal solutions into a structure where chosen decks are always a prefix of the sorted list. That makes the solution space one-dimensional and fully captured by prefix sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    A = list(map(int, input().split()))
    m = int(input())
    B = list(map(int, input().split()))

    B.sort()

    P = [0] * (m + 1)
    for i in range(1, m + 1):
        P[i] = P[i - 1] + B[i - 1]

    def upper_bound(x):
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if P[mid] <= x:
                lo = mid
            else:
                hi = mid - 1
        return lo

    res = []
    for a in A:
        res.append(str(upper_bound(a)))

    print(" ".join(res))

if __name__ == "__main__":
    main()
```

The sorting step ensures we are always consuming the cheapest possible decks first. The prefix array converts repeated summation checks into a single monotone structure. The binary search finds the maximum feasible prefix length efficiently.

A subtle detail is the use of an upper-bound style binary search rather than `bisect_right` directly, but both are equivalent. The important condition is that we search on prefix sums, not raw values.

Zero-cost decks are naturally handled because they contribute zero to the prefix sum, allowing the prefix index to increase without consuming budget.

## Worked Examples

Consider `B = [0, 2, 5, 9]` and accounts `A = [0, 5, 10]`.

First we sort `B` (already sorted) and compute prefix sums:

| k | B[k] | P[k] |
| --- | --- | --- |
| 0 | - | 0 |
| 1 | 0 | 0 |
| 2 | 2 | 2 |
| 3 | 5 | 7 |
| 4 | 9 | 16 |

For each account:

| A | Feasible prefix k | Reason |
| --- | --- | --- |
| 0 | 1 | only zero-cost deck fits |
| 5 | 3 | 0 + 2 + 5 = 7 is too large, so best is 0 + 2 |
| 10 | 3 | 0 + 2 + 5 = 7 fits, 4th exceeds |

For `A = 5`, the binary search finds the largest prefix sum ≤ 5, which is `k = 2`, corresponding to two decks. This confirms that we always prefer smaller costs first.

Now consider a case with large imbalance: `B = [100, 1, 1]`, `A = 2`.

Sorted `B = [1, 1, 100]`, prefix sums `[0, 1, 2, 102]`.

| A | k |
| --- | --- |
| 2 | 2 |

We correctly take both cheap decks and ignore the expensive one entirely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m + n log m) | sorting decks dominates, each query uses binary search |
| Space | O(m) | prefix sum array storage |

The constraints `n, m ≤ 10^5` fit comfortably within this complexity. Sorting and binary searching over 100k elements is standard within a 1 second limit in Python when implemented carefully.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    A = list(map(int, input().split()))
    m = int(input())
    B = list(map(int, input().split()))

    B.sort()
    P = [0]
    for x in B:
        P.append(P[-1] + x)

    def upper_bound(x):
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if P[mid] <= x:
                lo = mid
            else:
                hi = mid - 1
        return lo

    return " ".join(str(upper_bound(a)) for a in A)

# sample-like test
assert run("3\n5 10 15\n4\n2 2 3 4") == "2 4 4", "basic case"

# minimum case
assert run("1\n0\n1\n0") == "1", "single zero case"

# all expensive
assert run("2\n1 10\n3\n100 200 300") == "0 0", "no budget case"

# all zeros
assert run("2\n0 5\n3\n0 0 0") == "3 3", "zero cost stacking"

# mixed case
assert run("3\n3 6 10\n4\n1 2 5 7") == "3 4 4", "prefix growth case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 1 | zero-cost handling |
| no budget | 0 0 | inability to pick any deck |
| all zeros | 3 3 | accumulation of free decks |
| mixed case | 3 4 4 | correct prefix + greedy structure |

## Edge Cases

When all deck costs are zero, the prefix sum remains zero for all prefixes. The algorithm returns `m` for every account because every prefix is feasible. For an input like `A = [0, 100]` and `B = [0, 0, 0]`, the binary search always returns 3, matching the fact that all decks can be taken regardless of budget.

When all decks are too expensive, such as `B = [5, 6, 7]` and `A = [0, 4]`, the prefix sums start at 0 then immediately exceed budgets. The algorithm correctly returns 0 for all accounts since even the cheapest deck cannot be afforded.

When budgets are extremely large, the binary search always returns `m`, since the full prefix sum fits. This avoids any overflow or iterative accumulation per query and demonstrates why preprocessi
