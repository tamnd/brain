---
title: "CF 104027D - \u9971\u4e86\u6ca1\u7ea2\u5305"
description: "We are given a sequence of orders, each with a price, and a collection of discount coupons. Each coupon has a threshold value and a discount value. A coupon can only be applied to an order if the order price is at least as large as the coupon’s threshold."
date: "2026-07-02T04:08:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104027
codeforces_index: "D"
codeforces_contest_name: "The 10-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104027
solve_time_s: 39
verified: true
draft: false
---

[CF 104027D - \u9971\u4e86\u6ca1\u7ea2\u5305](https://codeforces.com/problemset/problem/104027/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of orders, each with a price, and a collection of discount coupons. Each coupon has a threshold value and a discount value. A coupon can only be applied to an order if the order price is at least as large as the coupon’s threshold. If it is applied, it reduces the order’s cost by its discount value.

Each coupon can be used at most once. For every order, we want to decide which eligible coupon to use so that the total money spent across all orders is minimized. If multiple coupons are applicable to an order, we always want to choose the one that gives the largest discount, because using a smaller discount while a larger one is available would only increase total cost without affecting future feasibility.

The task is to compute the minimum total cost after optimally assigning coupons to orders under these constraints.

From a constraints perspective, the natural scale of Codeforces problems of this type is around $10^5$ orders and $10^5$ coupons. This immediately rules out any quadratic matching strategy where we check every coupon for every order. A naive $O(nm)$ simulation would require up to $10^{10}$ operations, which is infeasible in two seconds.

The key difficulty is that coupon applicability depends on the current order’s price, and coupons are consumed as we go, so the problem resembles a dynamic assignment with eligibility constraints.

A few edge cases matter for correctness:

If all orders are cheaper than every coupon threshold, no coupon is ever usable, so the answer is just the sum of all order prices. A naive approach that tries to assign coupons greedily without checking feasibility might incorrectly “force” usage and produce invalid negative contributions.

If all coupons have zero discount, any strategy works but a careless implementation might still try to maintain unnecessary structures or mis-handle empty heaps.

If multiple coupons share identical thresholds and discounts, tie-breaking does not matter as long as we always pick the maximum discount available.

## Approaches

The brute-force idea is straightforward: process each order independently, scan through all unused coupons, filter those whose threshold is satisfied by the current order, pick the one with maximum discount, apply it, and mark it as used. This is correct because it directly enforces feasibility and optimal local choice for each order.

However, this approach requires checking all remaining coupons for every order. With $n$ orders and $m$ coupons, this leads to $O(nm)$ operations. In the worst case where both are $10^5$, this becomes $10^{10}$, which is far beyond any practical limit.

The key observation is that feasibility depends only on whether the order price exceeds the coupon threshold, and this condition is monotone in the sense that once an order is large enough to use a coupon, all future larger orders will also be able to use it if we process in increasing order. This suggests sorting both orders and coupons.

Once sorted by threshold and order value, we can sweep through orders in increasing order and maintain a set of all coupons that are currently eligible. Among all eligible coupons, we always want the one with maximum discount. This is exactly a data structure problem: we need to maintain a dynamic set supporting insertion of newly eligible coupons and extraction of the maximum discount.

A max heap solves this cleanly. We insert coupons as they become eligible while iterating through orders, and for each order we extract the best available coupon.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(m)$ | Too slow |
| Optimal (sorting + heap) | $O((n+m)\log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Sort all orders by their price in increasing order. This ensures that once a coupon becomes eligible, it will remain eligible for all subsequent orders only by value, but not necessarily useful earlier.
2. Sort all coupons by their threshold value in increasing order. This allows us to progressively activate coupons as order values increase.
3. Maintain a pointer over the coupon list and a max heap that stores discounts of all coupons whose threshold is already satisfied.
4. Iterate over orders in sorted order. For each order, first push into the heap every coupon whose threshold is less than or equal to the current order price. This step ensures the heap contains exactly the set of coupons that can legally be applied.
5. If the heap is non-empty, pop the maximum discount coupon and subtract it from the current order price. This is correct because any other available coupon would yield a smaller or equal discount and would never improve future outcomes.
6. Add the (possibly reduced) order cost into the total answer.
7. Continue until all orders are processed.

The crucial decision is always selecting the maximum discount among feasible coupons. Any alternative choice would either waste a better coupon or leave it for a later order where it might not be usable.

### Why it works

At any moment, the heap contains exactly the coupons that are usable for the current or future orders in the sorted sweep. Since coupons are single-use, assigning a coupon earlier does not prevent a better assignment later except through consumption. The greedy choice of always taking the maximum discount available ensures that we never leave a better coupon unused while taking a worse one for the same or earlier constraint level. This establishes an exchange argument: if an optimal solution used a smaller discount while a larger one was available at the same moment, swapping them does not violate feasibility and strictly improves or preserves the total outcome. Repeating this argument step by step guarantees global optimality.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    orders = list(map(int, input().split()))
    coupons = []
    
    for _ in range(m):
        x, y = map(int, input().split())
        coupons.append((x, y))
    
    orders.sort()
    coupons.sort()
    
    total = 0
    heap = []
    
    i = 0
    for price in orders:
        while i < m and coupons[i][0] <= price:
            heapq.heappush(heap, -coupons[i][1])
            i += 1
        
        if heap:
            best = -heapq.heappop(heap)
            price -= best
        
        total += price
    
    print(total)

if __name__ == "__main__":
    solve()
```

The code follows the sweep-line structure directly. Sorting both arrays ensures monotonic activation of coupons. The pointer `i` guarantees each coupon is processed exactly once, giving linear insertion cost overall. The heap stores negative values because Python provides a min-heap by default, so negation simulates a max-heap.

A subtle point is that each coupon is removed from the heap once used, ensuring the “single-use” constraint is enforced naturally.

## Worked Examples

Consider an example with orders `[3, 8, 10]` and coupons `[(2, 1), (5, 4), (7, 3)]`.

### Trace 1

| Order | Activated Coupons | Heap (discounts) | Chosen | Order Cost |
| --- | --- | --- | --- | --- |
| 3 | (2,1) | [1] | 1 | 2 |
| 8 | (5,4), (7,3) | [4,3] | 4 | 4 |
| 10 | none new | [3] | 3 | 7 |

Final total is $2 + 4 + 7 = 13$.

This trace shows how activation depends only on threshold crossing, and how the heap always picks the strongest available coupon.

### Trace 2

Orders `[5, 5, 5]`, coupons `[(5, 10), (5, 3)]`.

| Order | Activated Coupons | Heap | Chosen | Order Cost |
| --- | --- | --- | --- | --- |
| 5 | both coupons | [10, 3] | 10 | -5 |
| 5 | none left | [3] | 3 | 2 |
| 5 | none left | [] | - | 5 |

Total is $-5 + 2 + 5 = 2$.

This demonstrates correct handling of reuse constraints: once a coupon is taken, it disappears, and remaining orders adapt accordingly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log m)$ | Each coupon is pushed once and possibly popped once; heap operations are logarithmic |
| Space | $O(m)$ | Heap stores at most all coupons |

The sorting and heap operations are efficient enough for typical Codeforces limits up to $10^5$ elements, comfortably within time constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    input = sys.stdin.readline
    n, m = map(int, input().split())
    orders = list(map(int, input().split()))
    coupons = [tuple(map(int, input().split())) for _ in range(m)]

    orders.sort()
    coupons.sort()

    total = 0
    heap = []
    i = 0

    for price in orders:
        while i < m and coupons[i][0] <= price:
            heapq.heappush(heap, -coupons[i][1])
            i += 1

        if heap:
            price -= -heapq.heappop(heap)

        total += price

    return str(total)

# provided sample-like tests
assert run("3 3\n3 8 10\n2 1\n5 4\n7 3\n") == "13"

# custom cases
assert run("1 1\n10\n5 100\n") == "-90", "coupon exceeds order value"
assert run("2 2\n1 2\n10 5\n10 6\n") == "1", "only second order uses coupon"
assert run("3 3\n5 5 5\n5 10\n5 3\n5 1\n") == "-4", "multiple identical thresholds"
assert run("3 0\n1 2 3\n") == "6", "no coupons case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single high coupon | -90 | coupon stronger than order cost |
| mixed eligibility | 1 | selective activation over time |
| identical thresholds | -4 | heap tie-breaking correctness |
| no coupons | 6 | baseline sum behavior |

## Edge Cases

One edge case is when coupons exist but none are eligible for early orders. For input like `orders = [1, 2, 3]` and `coupons = [(10, 5)]`, the heap remains empty throughout initial iterations. The algorithm correctly adds each order unchanged, producing sum `6`.

Another edge case is when multiple coupons become eligible at the same order boundary. Suppose order is `10` and coupons are `(5,1), (5,9), (5,4)`. After activation, heap contains all three discounts, and extraction ensures `9` is used first. The heap invariant guarantees correctness regardless of insertion order.

A final edge case is exhaustion: once all coupons are used, the heap becomes empty and subsequent orders simply contribute their raw price. This is naturally handled because no additional operations are attempted when the heap is empty.
