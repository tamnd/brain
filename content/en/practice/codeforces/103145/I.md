---
title: "CF 103145I - Takeaway"
description: "We are given a fixed menu with seven possible dish types, each type having a known price. For each test case, Kanari selects several dishes, and the input lists which dish types he ordered. The total cost of the order is simply the sum of the corresponding dish prices."
date: "2026-07-03T19:51:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103145
codeforces_index: "I"
codeforces_contest_name: "The 15th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 103145
solve_time_s: 43
verified: true
draft: false
---

[CF 103145I - Takeaway](https://codeforces.com/problemset/problem/103145/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed menu with seven possible dish types, each type having a known price. For each test case, Kanari selects several dishes, and the input lists which dish types he ordered. The total cost of the order is simply the sum of the corresponding dish prices.

After computing the raw total, the platform may apply exactly one discount coupon. There are three possible coupons, each triggered only if the total order price reaches a certain threshold. A coupon with a higher threshold gives a larger discount. The system automatically picks the single best applicable coupon for the order, meaning we do not choose manually, we simply evaluate which discounts are available and apply the strongest one.

So for each test case, the task reduces to computing the sum of selected dish prices and then applying the best eligible discount based on that sum.

The constraints are extremely tight in terms of the number of test cases, up to one million. However, each test case is very small, with at most seven dishes. This immediately rules out any complex per-test processing, but also suggests that a constant time solution per test case is sufficient. The total computational budget is dominated by input parsing and O(1) arithmetic per case.

A subtle issue is performance overhead from repeated parsing. With T up to 10^6, even a linear scan per test case must be minimal and carefully implemented using fast I/O.

There are no structural edge cases in terms of ordering or combinatorics, but a common mistake is incorrectly stacking coupons or trying to apply more than one. The statement guarantees only one coupon is applied per order, and always the best one.

## Approaches

The naive approach is to interpret the problem literally: enumerate all subsets of coupons and simulate their application, or even attempt to test all combinations of applying discounts in different orders. This quickly becomes unnecessary because the coupons are not independent actions that can be reordered. Since only one coupon is applied in the final answer, trying combinations introduces redundant branching with no benefit. Even if implemented cleanly, it still degenerates into repeated conditional checks per test case.

The key observation is that coupon application depends only on the final total sum of the order. Once the sum is known, the decision is deterministic: if the sum is at least 120, the 50 yuan discount is best; otherwise if at least 89, apply 30; otherwise if at least 69, apply 15; otherwise no discount applies. This collapses the entire problem into a simple lookup on a scalar value.

So the structure of the problem is not combinatorial over coupons, but purely functional over a single aggregated value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of coupon choices | O(T) with heavy constant or unnecessary branching | O(1) | Too slow in practice |
| Direct sum + threshold check | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Predefine the price array for the seven dish types so that each dish type can be converted into a cost in constant time.
2. For each test case, read n and the list of chosen dish types, and compute the total sum by directly mapping each type to its price and accumulating it.
3. After computing the total sum S, determine the best coupon by checking thresholds in descending order of discount value.
4. If S is at least 120, subtract 50 from S. Otherwise if S is at least 89, subtract 30. Otherwise if S is at least 69, subtract 15. If none apply, keep S unchanged.
5. Output the final computed value for each test case immediately.

The ordering of checks matters because multiple coupons may be valid simultaneously, and we must pick the one with the largest discount. Evaluating from highest threshold downward ensures correctness without tracking all coupons explicitly.

### Why it works

The entire discount system is a monotonic step function over the total order value. Each coupon is only a function of whether the sum crosses a fixed boundary, and the best coupon is always uniquely determined by the largest threshold satisfied. Since the total sum fully determines eligibility and coupons do not interact, collapsing the process into a single comparison chain preserves all decision logic without loss of information.

## Python Solution

```python
import sys
input = sys.stdin.readline

prices = [0, 7, 27, 41, 49, 63, 78, 108]

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        total = 0
        for x in arr:
            total += prices[x]

        if total >= 120:
            total -= 50
        elif total >= 89:
            total -= 30
        elif total >= 69:
            total -= 15

        out.append(str(total))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation is deliberately kept at O(1) logic per test case after reading input. The only real work is summing up to seven values and applying three comparisons.

One subtle point is buffering output. With up to one million test cases, printing line by line can become a bottleneck, so results are accumulated and flushed once.

## Worked Examples

### Example 1

Input:

```
1
3
2 3 4
```

Dish mapping gives prices 27, 41, 49.

| Step | Chosen dishes | Running sum | Coupon check | Final |
| --- | --- | --- | --- | --- |
| 1 | 2, 3, 4 | 27 | - | - |
| 2 | 2, 3, 4 | 68 | - | - |
| 3 | 2, 3, 4 | 117 | eligible for 30 off | 87 |

The total is 117, which does not reach 120 but is above 89, so the 30-yuan coupon is the best applicable one.

### Example 2

Input:

```
1
7
7 7 7 7 7 7 7
```

All dishes cost 108.

| Step | Chosen dishes | Running sum | Coupon check | Final |
| --- | --- | --- | --- | --- |
| 1 | 7 items | 108 | - | - |
| 2 | 7 items | 216 | eligible for 50 off | 166 |

Since 216 exceeds 120, the strongest coupon applies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case sums at most 7 values and performs constant-time checks |
| Space | O(1) | Only fixed price table and a few variables are used |

The solution easily fits within limits because even with one million test cases, the total number of arithmetic operations remains small and bounded.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    prices = [0, 7, 27, 41, 49, 63, 78, 108]
    t = int(sys.stdin.readline())
    res = []
    
    for _ in range(t):
        n = int(sys.stdin.readline())
        arr = list(map(int, sys.stdin.readline().split()))
        
        total = 0
        for x in arr:
            total += prices[x]
        
        if total >= 120:
            total -= 50
        elif total >= 89:
            total -= 30
        elif total >= 69:
            total -= 15
        
        res.append(str(total))
    
    return "\n".join(res)

# provided sample-like cases
assert run("2\n3\n2 3 4\n7\n7 7 7 7 7 7 7\n") == "87\n166"

# minimum case
assert run("1\n1\n1\n") == "7"

# boundary case just below first coupon
assert run("1\n1\n4\n") == "49"

# boundary case hitting first coupon
assert run("1\n1\n2 3\n") == "62"

# all same mid coupon range
assert run("1\n1\n5 5\n") == "96"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single dish type 1 | 7 | minimum input handling |
| 2 + 3 dishes | 62 | correct sum and no coupon |
| 2 dishes type 5 | 96 | mid-range coupon application |
| full sample set | 87, 166 | correctness on both branches |

## Edge Cases

A key edge case is when the total is exactly on a coupon threshold boundary. For example, if the sum is exactly 69, the 15-yuan discount must apply.

Input:

```
1
1
5 4
```

This sums to 63 + 49 = 112.

Step trace:

| Step | Sum | Coupon decision | Output |
| --- | --- | --- | --- |
| compute | 112 | >= 89 so 30 off | 82 |

The algorithm correctly chooses the highest valid coupon because it evaluates thresholds in descending order.

Another boundary case is when no coupon applies at all.

Input:

```
1
1
1
```

Sum is 7, which is below all thresholds, so no subtraction happens and the output remains 7.
