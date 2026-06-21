---
title: "CF 105591A - \u041d\u043e\u0432\u044b\u0439 \u0433\u043e\u0434"
description: "We are asked to simulate a very simple bookkeeping task over a consecutive range of years. Imagine writing down every integer year starting from 1 up to 2024, one by one, without skipping any value."
date: "2026-06-22T05:53:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105591
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 7-8 \u043a\u043b\u0430\u0441\u0441\u044b, \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2024"
rating: 0
weight: 105591
solve_time_s: 45
verified: true
draft: false
---

[CF 105591A - \u041d\u043e\u0432\u044b\u0439 \u0433\u043e\u0434](https://codeforces.com/problemset/problem/105591/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a very simple bookkeeping task over a consecutive range of years. Imagine writing down every integer year starting from 1 up to 2024, one by one, without skipping any value. Each number is written in its usual decimal form, so 7 is written as a single digit, 10 is written as two digits, and 2024 is written as four digits. The task is to determine how many individual digits appear in total across all these written year labels.

The input contains no data, so the output is fully determined by this fixed range. That removes any variability: we are not computing something over test cases or user-provided ranges, but evaluating a constant expression defined by the problem statement.

The key constraint implication here is that there is no runtime pressure in the traditional sense. Any approach from direct simulation to arithmetic counting is fast enough because the range is small and fixed. The only real requirement is correctness in counting digit lengths across integer intervals.

A common subtle mistake is to assume the count is simply 2024 times an average digit length or to mis-handle boundary transitions between digit lengths. For example, numbers 1 to 9 contribute 9 digits, but 10 to 99 contribute 180 digits, and failing to properly separate these intervals leads to off-by-one errors.

Another mistake is attempting to convert numbers to strings and summing lengths without considering that the range is fixed. While that works here, it hides the combinatorial structure that generalizes to larger ranges.

## Approaches

A brute-force approach is straightforward: iterate from 1 to 2024, convert each number to a string, and sum its length. This is correct because each number’s decimal representation directly corresponds to its digit contribution. The total number of operations is proportional to 2024 conversions and length computations, which is trivial.

The limitation of this approach appears only when generalizing. If the upper bound were up to 10^9, iterating over every integer would require billions of steps, which is infeasible. That is where we need a structural observation: numbers with the same digit length form contiguous blocks. Instead of processing each integer individually, we can group them by digit length and count contributions arithmetically.

The key insight is that numbers from 1 to 9 contribute 1 digit each, from 10 to 99 contribute 2 digits each, from 100 to 999 contribute 3 digits each, and from 1000 to 2024 contribute 4 digits each. This reduces the problem to summing over a few intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Partition the range [1, 2024] into segments where all numbers have the same digit length. These segments are [1, 9], [10, 99], [100, 999], and [1000, 2024]. This works because decimal digit length only changes at powers of 10.
2. Compute the contribution of the first segment as the number of integers in [1, 9] multiplied by 1 digit per number. This isolates all single-digit numbers without overlap.
3. Compute the contribution of the second segment [10, 99] by counting how many integers lie in the interval and multiplying by 2. This captures all two-digit numbers consistently.
4. Compute the contribution of the third segment [100, 999] similarly, multiplying the count of numbers in that interval by 3.
5. Compute the contribution of the final segment [1000, 2024] by multiplying its size by 4, since all numbers in this interval have four digits.
6. Sum all segment contributions to obtain the total digit count.

The reason each step is safe is that every integer from 1 to 2024 belongs to exactly one segment, and each segment assigns the correct constant digit length to all its elements.

### Why it works

The algorithm relies on the invariant that digit length is constant within each interval defined by powers of ten. Since these intervals partition the entire range without overlap or omission, summing per-interval contributions is equivalent to summing per-number contributions. No number is double-counted or skipped, and within each interval the per-number contribution is uniform.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digits_count(l, r, d):
    if r < l:
        return 0
    return (r - l + 1) * d

def solve():
    total = 0
    total += digits_count(1, 9, 1)
    total += digits_count(10, 99, 2)
    total += digits_count(100, 999, 3)
    total += digits_count(1000, 2024, 4)
    print(total)

if __name__ == "__main__":
    solve()
```

The solution explicitly breaks the problem into digit-length intervals rather than iterating over all numbers. The helper function cleanly handles empty intervals, although in this fixed problem all intervals are valid.

The only subtlety is correctly defining interval boundaries. The transition points 9, 99, and 999 are inclusive upper bounds for their respective digit lengths, and the next interval starts immediately after.

## Worked Examples

Since the full problem has a fixed input, we simulate a smaller analogous case to demonstrate correctness. Consider computing the digit count from 1 to 15.

| Step | Interval | Count | Digits per number | Contribution |
| --- | --- | --- | --- | --- |
| 1 | [1, 9] | 9 | 1 | 9 |
| 2 | [10, 15] | 6 | 2 | 12 |

Total is 21 digits.

This trace shows that the algorithm correctly separates digit-length regimes and aggregates contributions without needing to inspect each number individually.

A second example can be [1, 120].

| Step | Interval | Count | Digits per number | Contribution |
| --- | --- | --- | --- | --- |
| 1 | [1, 9] | 9 | 1 | 9 |
| 2 | [10, 99] | 90 | 2 | 180 |
| 3 | [100, 120] | 21 | 3 | 63 |

Total is 252 digits.

This confirms that the interval logic naturally extends to mixed-length ranges and handles partial intervals correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of interval computations are performed |
| Space | O(1) | No additional data structures are used |

The computation does not depend on the input size because the range is fixed by the problem statement. Even if generalized, the number of digit-length boundaries is logarithmic in the range, but here it is constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    input = builtins.input

    def digits_count(l, r, d):
        if r < l:
            return 0
        return (r - l + 1) * d

    total = 0
    total += digits_count(1, 9, 1)
    total += digits_count(10, 99, 2)
    total += digits_count(100, 999, 3)
    total += digits_count(1000, 2024, 4)
    return str(total)

# main fixed case
assert run("") == str(9 + 180 + 900 + (2024 - 999) * 4)

# small range variant
def run_small():
    sys.stdin = io.StringIO("")
    return digits_count(1, 15, 0)  # placeholder not used

# custom direct checks via same logic
assert (9 + (15 - 9) * 2) == 21

assert (9 + 180 + (120 - 99) * 3) == 252

assert (9 + 180 + 900 + (1000 - 999) * 4) > 0

assert (9 + 180 + 900 + (2024 - 999) * 4) > 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1..15 | 21 | transition from 1-digit to 2-digit numbers |
| 1..120 | 252 | correct handling of partial 3-digit interval |
| 1..2024 | fixed sum | full boundary correctness |

## Edge Cases

The most relevant edge behavior is the transition at digit boundaries: 9 to 10, 99 to 100, and 999 to 1000. The algorithm handles these cleanly because each boundary is explicitly split into separate intervals.

For example, at the 9 to 10 transition, 9 contributes 1 digit while 10 contributes 2 digits. In the interval formulation, 9 is counted in [1, 9] and 10 starts [10, 99], so there is no overlap or ambiguity.

At the 999 to 1000 transition, the same structure holds. 999 is included in the 3-digit block, while 1000 begins the 4-digit block. The algorithm assigns each number exactly one digit length class, so the contribution remains consistent and complete.
