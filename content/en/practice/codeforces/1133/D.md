---
title: "CF 1133D - Zero Quantity Maximization"
description: "We are given two arrays of integers, a and b, each with n elements. We are asked to construct a new array c using a single real number d such that each element ci equals d ai + bi. Our goal is to choose d to maximize the number of zeros in c."
date: "2026-06-12T04:05:05+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1133
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 544 (Div. 3)"
rating: 1500
weight: 1133
solve_time_s: 73
verified: true
draft: false
---

[CF 1133D - Zero Quantity Maximization](https://codeforces.com/problemset/problem/1133/D)

**Rating:** 1500  
**Tags:** hashing, math, number theory  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of integers, `a` and `b`, each with `n` elements. We are asked to construct a new array `c` using a single real number `d` such that each element `c_i` equals `d * a_i + b_i`. Our goal is to choose `d` to maximize the number of zeros in `c`. The output is the maximum number of zero elements achievable in `c`.

The constraints are significant. `n` can be up to 200,000, and `a_i` and `b_i` can each be as large as 10^9 in absolute value. This rules out any solution that examines all possible `d` values explicitly or tries all pairs in a nested loop. The algorithm must run in roughly linear or linearithmic time relative to `n`.

A subtle edge case arises when some `a_i` values are zero. In that case, `c_i = b_i` is independent of `d`, so we can only get a zero for that position if `b_i` itself is zero. Another important case is when multiple pairs `(a_i, b_i)` yield the same ratio `-b_i / a_i`. These will contribute to the same optimal `d`. A careless implementation that ignores precision or reduces fractions incorrectly could miscount these.

Small example: `a = [0, 2], b = [0, 4]`. Here, the first element is already zero regardless of `d`. The second element becomes zero when `d = -2`. The optimal `d` is `-2` and we get two zeros. A naive approach that ignores zeros where `a_i = 0` would count only one zero.

## Approaches

The brute-force approach is to consider every real `d` that could possibly make some `c_i` zero, then count zeros for that `d`. Observing that `c_i = 0` implies `d = -b_i / a_i` (when `a_i ≠ 0`), a naive algorithm might attempt to test all these candidate `d` values and count zeros in `O(n^2)` time. This is correct in principle but far too slow: for `n = 2 * 10^5`, it could require 4 * 10^10 operations.

The key observation is that `d` is determined uniquely by the ratio `-b_i / a_i`. If multiple indices produce the same ratio, choosing that `d` makes all corresponding `c_i` zero simultaneously. Therefore, we only need to count how many times each unique ratio occurs. Fractions must be stored in reduced form to avoid floating-point inaccuracies. Zero pairs `(a_i = 0, b_i = 0)` can be counted separately since they are zeros for any `d`.

This reduces the problem to hashing these fractions and counting occurrences. Each fraction can be represented as `(numerator, denominator)` in reduced form using the greatest common divisor, while ensuring the denominator is positive for consistency. Once we have the counts, the maximum frequency plus the number of `a_i = 0, b_i = 0` gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log(max( | a_i | , |

## Algorithm Walkthrough

1. Initialize a counter `ratio_count` to store the frequency of each reduced fraction representing `-b_i / a_i`. Also initialize `zero_count` to count positions where `a_i = 0` and `b_i = 0`.
2. Iterate over each pair `(a_i, b_i)`. If `a_i` is zero and `b_i` is zero, increment `zero_count`. If `a_i` is zero and `b_i` is not zero, skip it because no `d` can make this zero.
3. For nonzero `a_i`, compute the fraction `-b_i / a_i`. Reduce this fraction to its simplest form using the greatest common divisor. Normalize signs so the denominator is positive, ensuring consistent hashing.
4. Use the tuple `(numerator, denominator)` as a key in the counter `ratio_count` and increment the count for that key.
5. The final answer is the maximum count in `ratio_count` plus `zero_count`. If `ratio_count` is empty (all `a_i = 0`), the answer is `zero_count`.

Why it works: each fraction represents exactly one candidate `d` that makes the corresponding `c_i` zero. By counting how many times each candidate `d` occurs, we find the `d` that maximizes zeros. Zero elements independent of `d` are added separately. No candidate is missed, and no fraction is double-counted due to normalization.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd
from collections import Counter

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

ratio_count = Counter()
zero_count = 0

for ai, bi in zip(a, b):
    if ai == 0:
        if bi == 0:
            zero_count += 1
        continue
    num = -bi
    den = ai
    g = gcd(num, den)
    num //= g
    den //= g
    if den < 0:
        num = -num
        den = -den
    ratio_count[(num, den)] += 1

max_ratio = max(ratio_count.values(), default=0)
print(max_ratio + zero_count)
```

This solution first handles zeros where `a_i = 0`. Then it carefully reduces fractions and normalizes signs to ensure consistent keys. Using a `Counter` efficiently tracks frequencies. The final `max` call finds the optimal candidate `d`.

## Worked Examples

Sample 1:

Input:

```
5
1 2 3 4 5
2 4 7 11 3
```

| i | a_i | b_i | num=-b_i | den=a_i | reduced | ratio_count |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | -2 | 1 | (-2,1) | 1 |
| 2 | 2 | 4 | -4 | 2 | (-2,1) | 2 |
| 3 | 3 | 7 | -7 | 3 | (-7,3) | 1 |
| 4 | 4 | 11 | -11 | 4 | (-11,4) | 1 |
| 5 | 5 | 3 | -3 | 5 | (-3,5) | 1 |

`zero_count = 0`, `max_ratio = 2`, output `2`. This confirms that choosing `d = -2` zeros the first two positions.

Sample 2:

Input:

```
3
0 1 2
0 3 6
```

| i | a_i | b_i | zero_count | ratio_count |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | - |
| 2 | 1 | 3 | 0 | (-3,1)=1 |
| 3 | 2 | 6 | 0 | (-3,1)=2 |

`zero_count=1`, `max_ratio=2`, output `3`. The fraction counting plus zero handling works correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max( | a_i |
| Space | O(n) | We store at most n unique fractions in the counter. |

With `n ≤ 2 * 10^5`, the time complexity is acceptable within 2 seconds. Memory usage is linear, well within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    from math import gcd
    from collections import Counter
    ratio_count = Counter()
    zero_count = 0
    for ai, bi in zip(a, b):
        if ai == 0:
            if bi == 0:
                zero_count += 1
            continue
        num, den = -bi, ai
        g = gcd(num, den)
        num //= g
        den //= g
        if den < 0:
            num = -num
            den = -den
        ratio_count[(num, den)] += 1
    max_ratio = max(ratio_count.values(), default=0)
    return str(max_ratio + zero_count)

# provided samples
assert run("5\n1 2 3 4 5\n2 4 7 11 3\n") == "2", "sample 1"
assert run("3\n0 1 2\n0 3 6\n") == "3", "custom zero + fraction overlap"
# minimum-size input
assert run("1\n0\n0\n") == "1", "single zero"
assert run("1\n1\n2\n") == "1", "single non
```
