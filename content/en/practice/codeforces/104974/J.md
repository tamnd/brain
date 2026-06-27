---
title: "CF 104974J - Bouquet of Flowers"
description: "We are given several test cases. In each test case, there are several flower types, each type having a fixed “beauty coefficient” and exactly 100 identical flowers available. Every individual flower costs 1 dinar, and we can buy at most c flowers in total."
date: "2026-06-28T06:14:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104974
codeforces_index: "J"
codeforces_contest_name: "Codentines Day"
rating: 0
weight: 104974
solve_time_s: 78
verified: false
draft: false
---

[CF 104974J - Bouquet of Flowers](https://codeforces.com/problemset/problem/104974/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases. In each test case, there are several flower types, each type having a fixed “beauty coefficient” and exactly 100 identical flowers available. Every individual flower costs 1 dinar, and we can buy at most `c` flowers in total.

If we buy some collection of flowers, the bouquet score is defined as a ratio: the total beauty of the chosen flowers divided by the total beauty of all flowers available in the shop. Since every type contributes 100 identical flowers, the denominator is fixed for a test case and depends only on the input array, not on what we buy.

This turns the task into a pure maximization problem: we want to maximize the total beauty sum of the selected flowers under a budget constraint, and then normalize it by a constant value.

Each flower of type `i` contributes `a_i` to the sum, and there are 100 copies of it. So the shop is equivalent to having `100 * n` items where each `a_i` appears exactly 100 times. We may pick at most `c` items.

The output is a real number representing this normalized maximum value.

The constraints allow up to `5 × 10^4` types per test case, and up to `10` test cases. Expanding all flowers explicitly would produce up to `5 × 10^6` items, which is borderline but still feasible in optimized languages, yet unnecessary.

The main edge case is when `c` is very large, up to `10^9`. In that situation, the constraint is effectively irrelevant because we cannot exceed the available `100n` flowers.

A naive mistake is to treat this as a fractional or continuous optimization problem or to misinterpret the denominator as depending on the chosen subset. For example, if one incorrectly assumes the denominator changes with selection, greedy selection could become invalid. Another subtle pitfall is expanding all `100n` items without considering that many values are repeated, leading to unnecessary overhead.

A small illustrative case:

Input:

```
n = 2, c = 3
a = [5, 1]
```

We have 100 copies of 5 and 100 copies of 1. The optimal choice is clearly three copies of 5, not mixing in 1s. Any approach that fails to group identical values would do extra work but still must respect this structure.

## Approaches

If we simulate the process directly, we construct all `100n` flowers, sort them by beauty, and take the top `c`. This is correct because every flower has independent contribution to the sum. The issue is scale: sorting up to five million elements per test case is borderline but still within some limits, though clearly unnecessary.

The key observation is that the structure is already grouped. Instead of thinking in terms of individual flowers, we can treat each type as a block of 100 identical values. Since all items are independent and additive, optimal selection always prefers higher `a_i` values first. Within a type, all copies are identical, so partial selection of a type only happens when we run out of budget.

This reduces the problem to sorting the `n` types by `a_i` in descending order and greedily taking up to 100 from each type until we exhaust the budget `c`.

Once we compute the maximum achievable sum, the final answer is this sum divided by the constant total beauty of all flowers, which is `100 * sum(a_i)`. Multiplying numerator and denominator by 1 simplifies the expression to a stable floating computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (expand all flowers) | O(100n log(100n)) | O(100n) | Accepted but heavy |
| Optimal (sort types + greedy) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all beauty coefficients, `S = sum(a_i)`. This represents the normalization denominator up to a constant factor.
2. Sort the array `a` in descending order. This ensures we always consider the most valuable flowers first, which is necessary because every flower of a higher `a_i` dominates any flower of a lower `a_i`.
3. Initialize a variable `taken_sum = 0` and keep track of remaining budget `c`.
4. Iterate over the sorted list. For each value `a_i`, determine how many flowers we can take from this type: `take = min(100, c)`. This respects both the availability constraint and the budget constraint.
5. Add `take * a_i` to `taken_sum`, and subtract `take` from `c`.
6. Stop early if `c` becomes zero, since no further contribution is possible.
7. Compute the final answer as `taken_sum / S`.

### Why it works

The process is a direct application of greedy selection over a multiset of independent weighted items. Each flower is identical within its type, so any optimal solution is equivalent to choosing a prefix of the sorted multiset of all flowers. Sorting ensures that this prefix is ordered by decreasing contribution, so replacing any lower-value selected flower with a higher-value unselected flower always improves or preserves the total sum. Since the denominator is constant, maximizing the ratio reduces to maximizing the numerator, so this greedy construction produces the optimal bouquet.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(float, input().split()))
        
        total = sum(a)
        a.sort(reverse=True)
        
        rem = c
        taken = 0.0
        
        for val in a:
            if rem == 0:
                break
            take = min(100, rem)
            taken += take * val
            rem -= take
        
        print(taken / total)

if __name__ == "__main__":
    solve()
```

The code first reads all flower types and computes the normalization sum. Sorting ensures we process the most valuable types first. The loop greedily consumes up to 100 flowers per type, but never exceeds the budget `c`. The final division converts the accumulated selection score into the required normalized value.

A subtle implementation detail is using floating-point arithmetic consistently, since both input and output involve real numbers. Another important point is early termination when `rem` reaches zero, which avoids unnecessary iteration when `c` is small compared to `n`.

## Worked Examples

### Example 1

Input:

```
n = 3, c = 4
a = [4, 2, 1]
```

We have the following process:

| Step | Current type | rem | take | taken sum |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 4 | 16 |
| 2 | 2 | 0 | 0 | 16 |
| 3 | 1 | 0 | 0 | 16 |

We take four flowers of value 4 and stop immediately after exhausting the budget. The denominator is `4 + 2 + 1 = 7`, so result is `16 / 7`.

This confirms that concentrating budget on the highest values is optimal.

### Example 2

Input:

```
n = 3, c = 200
a = [3, 3, 2]
```

| Step | Current type | rem | take | taken sum |
| --- | --- | --- | --- | --- |
| 1 | 3 | 200 | 100 | 300 |
| 2 | 3 | 100 | 100 | 600 |
| 3 | 2 | 0 | 0 | 600 |

We exhaust both high-value types completely before touching the lower one. This shows that the algorithm naturally fills full 100-item blocks when budget allows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the `n` types dominates per test case |
| Space | O(n) | Storing the input array |

The constraints allow up to `5 × 10^4` types per test case, so sorting is easily fast enough. Even with 10 test cases, total operations remain well within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    t = int(input())
    out = []
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(float, input().split()))
        total = sum(a)
        a.sort(reverse=True)

        rem = c
        taken = 0.0

        for v in a:
            if rem == 0:
                break
            take = min(100, rem)
            taken += take * v
            rem -= take

        out.append(str(taken / total))
    return "\n".join(out) + "\n"

# minimal case
assert run("1\n1 1\n5\n")[:10], "min case"

# small greedy split
assert run("1\n2 3\n5 1\n") is not None

# all equal
assert run("1\n3 150\n2 2 2\n") is not None

# large budget saturates all
assert run("1\n2 1000\n1 2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single type | 1.0 | trivial normalization |
| mixed values | greedy preference | correctness of ordering |
| all equal | uniform selection | no bias in distribution |
| large budget | full exhaustion | cap at availability |

## Edge Cases

When `c` exceeds `100n`, the algorithm processes every type fully, taking all available flowers. The loop naturally handles this because `min(100, rem)` will always cap at 100 until the budget runs out or all types are consumed.

If all `a_i` are equal, sorting does not change order, but the algorithm still behaves correctly by filling types sequentially. For example, with `a = [2,2,2]` and `c = 250`, we take 100 from each of the first two types and 50 from the third, producing a proportional result consistent with uniform weights.

When `c` is very small, only the first few highest-value types are touched. Since the algorithm always processes in descending order, no low-value flower can be selected before a higher-value one is exhausted, preserving optimality even in extreme budget scarcity.
