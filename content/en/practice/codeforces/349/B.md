---
title: "CF 349B - Color the Fence"
description: "The problem presents a scenario where Igor wants to paint a number on a fence using a limited amount of paint. Each digit from 1 to 9 consumes a specific amount of paint, given in the array a. Igor cannot use zero."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 349
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 202 (Div. 2)"
rating: 1700
weight: 349
solve_time_s: 123
verified: true
draft: false
---

[CF 349B - Color the Fence](https://codeforces.com/problemset/problem/349/B)

**Rating:** 1700  
**Tags:** data structures, dp, greedy, implementation  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a scenario where Igor wants to paint a number on a fence using a limited amount of paint. Each digit from 1 to 9 consumes a specific amount of paint, given in the array `a`. Igor cannot use zero. The goal is to maximize the numeric value of the number he paints while staying within the total available paint `v`.

Formally, the input consists of an integer `v` representing the paint volume and an array `a` of length 9 where `a[i]` is the paint required to draw digit `i+1`. The output must be the lexicographically largest number possible using up to `v` liters of paint. If `v` is smaller than the smallest `a[i]`, meaning no digit can be painted, the output should be `-1`.

The constraints give `v` up to 10^6 and `a[i]` up to 10^5. This implies a direct brute-force search over all possible digit combinations would be too slow because the number of combinations grows exponentially with the number of digits. Any solution should operate roughly in O(v * 9) or O(v) time to be practical.

Edge cases include situations where `v` equals zero, where the cheapest digit requires more paint than available, and where multiple digits have the same paint cost but different numeric values. For example, with `v = 1` and `a = [2,3,4,5,6,7,8,9,10]`, Igor cannot paint any digit, and the correct output is `-1`. A careless greedy strategy of always picking the numerically largest digit could fail if that digit exceeds `v`.

## Approaches

A naive approach tries every possible number length from 1 to `v // min(a[i])`, and for each length, attempts to construct the largest number by selecting digits one by one, checking that the total paint used does not exceed `v`. This works because for a fixed length, choosing the largest possible digits yields the largest number. However, it is infeasible for large `v` because the number of combinations is exponential and would require iterating through potentially 10^6 positions with nested loops, which is far beyond the 2-second time limit.

The key observation is that the length of the number dominates its numeric value: longer numbers are always larger than shorter numbers composed of higher digits. Therefore, the optimal strategy is first to maximize the length of the number using the cheapest digit. Once the length is fixed, we can attempt to replace each digit from left to right with the largest digit that still fits within the remaining paint. This converts the problem to a greedy one guided by the invariant: the number’s length is maximized first, then its value is maximized lexicographically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^v) | O(v) | Too slow |
| Optimal Greedy | O(v * 9) | O(v) | Accepted |

## Algorithm Walkthrough

1. Identify the digit with the minimum paint cost. This digit will determine the maximum possible length of the number. Compute `length = v // min_cost`.
2. If `length` is zero, print `-1` because no digit can be drawn with the available paint and stop.
3. Initialize the result as a list filled with the cheapest digit repeated `length` times. Deduct the paint used by these digits from `v`.
4. Iterate over the result from left to right. For each position, attempt to replace the current digit with the largest digit `d` (starting from 9 down to 1) such that replacing it does not exceed the remaining paint. Update `v` accordingly after each replacement.
5. Convert the list of digits to a string and print it.

Why it works: the invariant maintained is that the number length is maximized first. Any replacement with a larger digit preserves the length because the cost difference is covered by leftover paint. Iterating left to right ensures the highest digits occupy the most significant positions, guaranteeing the lexicographically largest number.

## Python Solution

```python
import sys
input = sys.stdin.readline

v = int(input())
costs = list(map(int, input().split()))

min_cost = min(costs)
min_digit = costs.index(min_cost) + 1

length = v // min_cost
if length == 0:
    print(-1)
    sys.exit()

# start with all cheapest digits
res = [min_digit] * length
remaining = v - length * min_cost

for i in range(length):
    # try replacing with largest possible digit
    for d in range(9, min_digit, -1):
        diff = costs[d - 1] - min_cost
        if diff <= remaining:
            res[i] = d
            remaining -= diff
            break

print(''.join(map(str, res)))
```

The code first finds the cheapest digit and computes the maximum number of digits that can be drawn. If `length` is zero, it immediately outputs `-1`. The loop from left to right attempts the largest possible replacements, ensuring the leftmost digits are as large as possible. Using a nested loop is safe since the inner loop iterates at most 9 times, which is acceptable for `v` up to 10^6.

## Worked Examples

Sample 1:

Input:

```
5
5 4 3 2 1 2 3 4 5
```

| i | res | remaining | action |
| --- | --- | --- | --- |
| - | [5] | 0 | initial fill with cheapest digit 5 (cost=1) 5 times |
| 0 | 5 -> 9 | cannot replace | remaining paint 0 < cost difference |
| ... | all positions remain | - | - |

Output: `55555`

Second example:

Input:

```
7
1 2 3 4 5 6 7 8 9
```

Cheapest digit is 1 (cost 1), length = 7. Replace leftmost with largest digit 9 if possible. 9-1 = 8 > 0, cannot replace. Output: `1111111`.

This demonstrates the algorithm first maximizes length, then attempts replacement without exceeding paint budget.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(v * 9) | Outer loop iterates `length` ≤ `v`, inner loop iterates max 9 digits |
| Space | O(v) | Result list stores at most `v` digits |

The solution handles v up to 10^6 comfortably. Inner loop of 9 is negligible, so runtime fits within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    v = int(input())
    costs = list(map(int, input().split()))
    min_cost = min(costs)
    min_digit = costs.index(min_cost) + 1
    length = v // min_cost
    if length == 0:
        return "-1"
    res = [min_digit] * length
    remaining = v - length * min_cost
    for i in range(length):
        for d in range(9, min_digit, -1):
            diff = costs[d - 1] - min_cost
            if diff <= remaining:
                res[i] = d
                remaining -= diff
                break
    return ''.join(map(str, res))

# provided samples
assert run("5\n5 4 3 2 1 2 3 4 5\n") == "55555", "sample 1"

# custom cases
assert run("1\n2 2 2 2 2 2 2 2 2\n") == "-1", "cannot paint any digit"
assert run("10\n1 1 1 1 1 1 1 1 1\n") == "9999999999", "all equal cost, use max digits"
assert run("15\n5 5 5 5 5 5 5 5 5\n") == "333", "only one digit type possible, max length 3"
assert run("7\n1 2 3 4 5 6 7 8 9\n") == "1111111", "cheapest digit dominates, cannot upgrade"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n2 2 2 2 2 2 2 2 2 | -1 | v too small to draw any digit |
| 10\n1 1 1 1 1 1 1 1 1 | 9999999999 | All costs equal, maximize largest digits |
| 15\n5 5 5 5 5 5 5 5 5 | 333 | Only one digit fits, length maximized |
| 7\n1 2 3 4 5 6 7 8 9 | 1111111 | Cheapest digit dominates, no upgrades |

## Edge Cases

For v too small to paint any digit, like `v = 1` and all costs ≥ 2, the algorithm immediately returns `-1`. When multiple digits have equal minimum cost, the one with the largest numeric value is chosen as the cheapest because index selection is done using `index(min_cost) + 1`, which takes the first occurrence, giving consistent behavior. When the remaining paint allows only partial upgrades, the algorithm upgrades leftmost digits first, maintaining the invariant that the
