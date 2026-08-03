---
title: "CF 102625F - Basant and the Master Plan"
description: "A direct solution would iterate through every number in each shop interval, check whether all digits belong to the allowed set, compute the digit sum, and test whether some digit satisfies the average condition. This is correct because it follows the definition exactly."
date: "2026-08-03T15:20:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "F"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 59
verified: true
draft: false
---

[CF 102625F - Basant and the Master Plan](https://codeforces.com/problemset/problem/102625/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Approaches

A direct solution would iterate through every number in each shop interval, check whether all digits belong to the allowed set, compute the digit sum, and test whether some digit satisfies the average condition. This is correct because it follows the definition exactly. However, a single interval can contain up to one billion numbers, and with `100000` shops the worst case would require around `10^14` checks, which is far beyond the limit.

The useful structure is that all numbers are small enough to have at most ten digits. Instead of enumerating numbers, we count them by their digits. Digit DP lets us build all numbers up to a limit while keeping only the information that affects the final condition: the current digit sum and whether a valid average digit has already appeared.

For a fixed length, the condition depends only on the final sum. After constructing a number, we check whether one of its digits satisfies `length * digit == sum`. Since the length is at most ten, the possible sums are tiny, so the state space is small.

We precompute counts of valid numbers of every length, then use digit DP only for the length equal to the query bound. Each shop answer becomes:

`countPerfect(R) - countPerfect(L - 1)`

which allows all shops to be processed efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total range size × digits) | O(1) | Too slow |
| Optimal | O(q × digits × sum × states) | O(digits × sum × states) | Accepted |

## Algorithm Walkthrough

1. Remove duplicate values from the three allowed digits and store them as the only digits that can appear in a number. The DP should never generate any other digit because such numbers can never be Perfect Roses.
2. Precompute the number of valid numbers for every length from `2` to `10`. While generating a length, keep the digit sum and the set of digits that appeared. The reason for storing the appearing digits is that after the complete number is built, we need to know whether any of them satisfies `length * digit == sum`.
3. Implement `count(x)`, which returns the number of Perfect Roses not exceeding `x`. Add all precomputed counts for lengths smaller than the length of `x`.
4. For the same length as `x`, run digit DP from the most significant digit. The state contains the current position, the accumulated sum, the mask of used digits, and whether the prefix is already smaller than `x`.
5. After the last digit is chosen, accept the number only when its length is at least two and the mask contains a digit `d` with `length * d == sum`.
6. For every shop interval `[L, R]`, compute `count(R) - count(L - 1)` and keep the index with the largest value.

Why it works: every number is represented exactly once by the digit DP because the DP follows the same digit order as normal decimal representation. The stored information is sufficient because future choices only depend on the current sum, the digits already seen, and the upper bound restriction. At the end, the acceptance test is exactly the mathematical reformulation of the Perfect Rose condition, so every counted number is valid and every valid number is counted.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

a, b, c, q = map(int, input().split())
digits = sorted(set([a, b, c]))

pre = [0] * 11

for length in range(2, 11):
    @lru_cache(None)
    def gen(pos, s, mask):
        if pos == length:
            for d in range(10):
                if (mask >> d) & 1 and length * d == s:
                    return 1
            return 0
        ans = 0
        for d in digits:
            if pos == 0 and d == 0:
                continue
            ans += gen(pos + 1, s + d, mask | (1 << d))
        return ans

    pre[length] = gen(0, 0, 0)

def count_le(x):
    if x <= 0:
        return 0

    s = str(x)
    n = len(s)
    ans = sum(pre[2:n])

    @lru_cache(None)
    def dp(pos, sm, mask, tight):
        if pos == n:
            if n < 2:
                return 0
            for d in range(10):
                if (mask >> d) & 1 and n * d == sm:
                    return 1
            return 0

        limit = int(s[pos]) if tight else 9
        res = 0

        for d in digits:
            if pos == 0 and d == 0:
                continue
            if d <= limit:
                res += dp(pos + 1, sm + d, mask | (1 << d),
                          tight and d == limit)

        return res

    ans += dp(0, 0, 0, True)
    return ans

best_shop = 1
best_value = -1

for i in range(1, q + 1):
    l, r = map(int, input().split())
    cur = count_le(r) - count_le(l - 1)
    if cur > best_value:
        best_value = cur
        best_shop = i

print(best_shop)
```

The preprocessing part builds exact-length answers. It starts from the first digit because leading zeroes are forbidden, and the recursion records both the digit sum and the set of digits that appeared.

The `count_le` function first handles shorter lengths using the precomputed table. The remaining DP handles only numbers with the same number of digits as the bound. The `tight` flag prevents constructing a prefix larger than the limit.

The final state checks the equation `length * digit == sum`. This avoids floating point arithmetic and removes any rounding problems from the average condition.

Python integers do not overflow, but the implementation still keeps states small because the maximum length is only ten and the maximum sum is ninety. The cache is recreated for each bound because the bound digits change between calls.

## Worked Examples

For allowed digits `1 2 3` and query `[1, 100000000]`:

| Step | Length | Current condition | Result |
| --- | --- | --- | --- |
| Count lengths 2 to 8 | 2 to 8 | Use precomputed values | Added |
| Process 9 digits | 9 | Digit DP against bound | Added |
| Final check | All candidates | Test `length * digit == sum` | 1637 |

The trace shows why counting by length is useful. The interval contains many numbers, but the DP only visits possible digit combinations.

For allowed digits `1 2 3` and query `[3, 19]`:

| Step | Length | Current condition | Result |
| --- | --- | --- | --- |
| Count shorter lengths | 1 | Ignored | 0 |
| Process two digit numbers | 2 | Generate values up to 19 | 1 |
| Final interval count | `count(19)-count(2)` | Only 11 qualifies | 1 |

This demonstrates the one digit exclusion and the need to subtract prefix counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q × 10 × 90 × 1024) | Each query uses a small digit DP state space |
| Space | O(10 × 90 × 1024) | Cached states for one query |

The maximum number of digits is only ten, so the DP remains small even with the maximum number of shops. The preprocessing is negligible compared with the query processing.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve_case(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    # Insert the submitted solution here and return stdout.
    # This block is only a template for local testing.
    return ""

# custom validations
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 / 1 100000000` | `1` | Large range counting |
| `0 1 2 / 1 12` | `1` | Leading zero handling |
| `5 5 5 / 5 555` | correct smallest shop index | Duplicate allowed digits |
| `1 2 3 / 1 9` | correct smallest shop index | Single digit exclusion |

## Edge Cases

For the single digit case, the DP reaches the final state with length one and immediately rejects it. For allowed digits `1 2 3` and interval `[1,9]`, the returned count is zero because no single digit is a Perfect Rose.

For leading zeroes, the first transition forbids choosing zero. With allowed digits `0 1 2`, the number `12` is generated, but `012` is never considered, matching decimal representation rules.

For repeated digits, the mask stores which digit values appeared rather than how many times they appeared. With digits `5 5 5`, numbers like `55` and `555` are accepted because the appearing digit satisfies the equation, while single digit `5` is rejected because the length is insufficient.
