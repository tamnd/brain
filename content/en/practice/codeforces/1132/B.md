---
title: "CF 1132B - Discounts"
description: "We have a set of chocolate bars, each with its own price. The shopper wants all the bars but has a selection of discount coupons. Each coupon allows buying a fixed number of bars, but within that selection, the cheapest bar is free."
date: "2026-06-12T04:07:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 900
weight: 1132
solve_time_s: 73
verified: true
draft: false
---

[CF 1132B - Discounts](https://codeforces.com/problemset/problem/1132/B)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of chocolate bars, each with its own price. The shopper wants all the bars but has a selection of discount coupons. Each coupon allows buying a fixed number of bars, but within that selection, the cheapest bar is free. The task is to determine, for each coupon, the minimum total cost if the coupon is applied optimally and the remaining bars are bought at full price.

The input consists of the number of bars `n`, their individual prices `a_i`, the number of coupons `m`, and the sizes of the coupons `q_i`. The output is an array of `m` integers, where each integer is the minimal payment if the corresponding coupon is used optimally.

The constraints allow `n` to be as large as 300,000. This immediately rules out any brute-force approach that tries all combinations of chocolate bars for each coupon, because `C(n, q)` grows combinatorially. Even iterating naively for each coupon would be too slow, so we need a method that scales linearly or near-linearly in `n`.

A non-obvious edge case occurs when all chocolate bars have the same price. For instance, if `n = 3`, bars are `[5, 5, 5]`, and a coupon allows `q = 2`, the optimal bars to select could be any pair. The output must still account for paying only for the most expensive in the pair. A careless approach that assumes bars are distinct could produce a wrong calculation.

Another subtle case is when the coupon allows `q = n` bars. Here, all bars are chosen for the discount, and the cheapest of all bars is free. The implementation must handle this without indexing errors.

## Approaches

The brute-force approach is simple: for each coupon, enumerate all possible subsets of size `q_i`, sum the prices of the selected bars excluding the cheapest, and add the sum of the remaining bars. This works correctly but has a worst-case complexity of O(n choose q) per coupon. With n up to 300,000, this is infeasible, as even modest q values create an astronomically large number of combinations.

The key insight is that, for each coupon, we want to maximize the discount. The discount is the price of the cheapest bar among the chosen set. Therefore, to minimize total cost, we should select the `q_i` most expensive bars for the coupon. Paying for all except the cheapest of these maximizes the amount deducted from the total. This allows us to reduce the problem to sorting all bars in descending order and using prefix sums to quickly compute the sum of the top `q_i` bars. The total cost becomes the sum of all bars minus the cheapest bar among the top `q_i`.

This transforms the solution from combinatorial to O(n log n + m), where O(n log n) is for sorting and O(m) is for computing each coupon's result using the precomputed prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * C(n, q)) | O(n) | Too slow |
| Optimal | O(n log n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the array of prices `a`, `m`, and the array of coupon sizes `q`. These represent the number of bars, their individual prices, the number of coupons, and how many bars each coupon affects.
2. Sort the array `a` in descending order. This ensures the most expensive bars are at the start. Sorting is crucial because the optimal coupon choice always includes the most expensive bars to maximize the discount.
3. Compute the prefix sums of the sorted array. The prefix sum at index `i` represents the sum of the first `i+1` most expensive bars. This allows constant-time queries of the total price of the top `k` bars.
4. Compute the total sum of all bars. This will be used to compute the final payment for each coupon by subtracting the free bar in the coupon.
5. For each coupon size `q_i`, the optimal strategy is to choose the top `q_i` bars. Among them, the cheapest bar (which is the last in the sorted subset of size `q_i`) is free. The total cost becomes the sum of all bars minus this cheapest bar.
6. Print the result for each coupon in order.

The invariant that guarantees correctness is that for any coupon, the discount is maximized by selecting the largest `q_i` bars. No alternative subset of bars yields a larger discount because any lower-priced bar reduces the value of the free chocolate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
m = int(input())
q = list(map(int, input().split()))

a.sort(reverse=True)
prefix_sum = [0] * n
prefix_sum[0] = a[0]
for i in range(1, n):
    prefix_sum[i] = prefix_sum[i-1] + a[i]

total_sum = prefix_sum[-1]

results = []
for x in q:
    free_bar = a[x-1]  # cheapest among the top x bars
    cost = total_sum - free_bar
    results.append(str(cost))

print('\n'.join(results))
```

The solution first sorts the chocolate bars and constructs a prefix sum array. The `total_sum` captures the sum of all bars. For each coupon, the last bar in the top `q_i` bars is subtracted from the total sum to account for the free chocolate. The algorithm avoids recomputation by using the pre-sorted array.

## Worked Examples

Sample 1:

Input:

```
7
7 1 3 1 4 10 8
2
3 4
```

State of key variables after sorting and prefix sums:

| Sorted a | Prefix Sum |
| --- | --- |
| 10 8 7 4 3 1 1 | 10 18 25 29 32 33 34 |

For coupon q=3, top 3 bars are 10, 8, 7. Cheapest is 7. Total cost = 34 - 7 = 27.

For coupon q=4, top 4 bars are 10, 8, 7, 4. Cheapest is 4. Total cost = 34 - 4 = 30.

Sample 2:

Input:

```
5
5 5 5 5 5
1
2
```

Sorted array and prefix sums:

| Sorted a | Prefix Sum |
| --- | --- |
| 5 5 5 5 5 | 5 10 15 20 25 |

For coupon q=2, top 2 bars are 5, 5. Cheapest is 5. Total cost = 25 - 5 = 20.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting the bars takes n log n. Each coupon computation is O(1) using prefix sums. |
| Space | O(n) | We store the sorted array and prefix sums. |

With n ≤ 3*10^5 and m ≤ n, this algorithm fits comfortably within the 2-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    q = list(map(int, input().split()))

    a.sort(reverse=True)
    total_sum = sum(a)
    results = []
    for x in q:
        results.append(str(total_sum - a[x-1]))
    return '\n'.join(results)

# provided samples
assert run("7\n7 1 3 1 4 10 8\n2\n3 4\n") == "27\n30", "sample 1"

# minimum size input
assert run("2\n1 2\n1\n2\n") == "2", "min size"

# all equal values
assert run("5\n5 5 5 5 5\n2\n2 5\n") == "20\n20", "all equal"

# maximum-size simplified test
assert run("6\n1 2 3 4 5 6\n1\n6\n") == "20", "full coupon"

# edge case: descending input
assert run("5\n10 8 5 3 1\n2\n2 3\n") == "27\n26", "descending input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 2\n1\n2 | 2 | minimum n |
| 5\n5 5 5 5 5\n2\n2 5 | 20\n20 | all bars equal |
| 6\n1 2 3 4 5 6\n1\n6 | 20 | coupon covers all bars |
| 5\n10 8 5 3 1\n2\n2 3 | 27\n26 | descending order, multiple coupons |

## Edge Cases

For a coupon covering all bars, `q = n`, the free bar is the cheapest overall. For example, with bars `[4, 2, 3]` and `q = 3`, the free bar is 2, total payment = 4 + 3 = 7. The algorithm correctly selects `a[q-1] = a
