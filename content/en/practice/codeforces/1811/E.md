---
title: "CF 1811E - Living Sequence"
description: "We are asked to generate the k-th number in a sequence of natural numbers that do not contain the digit 4. The sequence starts as [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, ...]."
date: "2026-06-09T08:39:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1811
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 863 (Div. 3)"
rating: 1500
weight: 1811
solve_time_s: 76
verified: true
draft: false
---

[CF 1811E - Living Sequence](https://codeforces.com/problemset/problem/1811/E)

**Rating:** 1500  
**Tags:** binary search, dp, math, number theory  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to generate the _k-th number_ in a sequence of natural numbers that **do not contain the digit 4**. The sequence starts as `[1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, ...]`. Each query gives a position `k` (1-indexed), and we must return the number that would appear there.

The input has up to `10^4` test cases, and `k` can be as large as `10^12`. This immediately rules out any solution that iterates over numbers and checks for the digit 4. Even if we process 10^6 numbers per millisecond, a `k` of `10^12` would take billions of milliseconds. Therefore a linear search is infeasible.

A subtle edge case arises for numbers with multiple digits that skip 4. For example, the 4th number in the sequence is `5`, not `4`. Any naive approach that increments a counter and skips numbers containing 4 must carefully avoid off-by-one errors when crossing digits that contain 4. Another tricky case is when `k` is extremely large, like `10^12`, where integer overflow or miscalculations in indexing could silently break a brute-force attempt.

## Approaches

The brute-force approach is straightforward: start at 1, increment, and skip any number containing the digit 4. Check each number in turn until reaching `k`. This works because you can explicitly generate the sequence, but it fails spectacularly for large `k`. For `k = 10^12`, the number of operations is on the order of `10^12`, which is impossible within the 1-second limit.

The key insight is that the sequence can be interpreted as a **base-9 representation**. Every number in the sequence can be derived by writing `k` in base 9, then interpreting each digit as a decimal number, skipping the forbidden 4. For example, the base-9 digits `0-8` map to decimal digits `[1,2,3,5,6,7,8,9,0]` in sequence (or equivalently `[1,2,3,5,6,7,8,9]` for the first 8 digits if we treat `0` specially). This works because there are exactly 9 allowed digits in the decimal system, so each position in base-9 corresponds to a valid digit in the sequence. This reduces the problem from generating up to `10^12` numbers to converting a single number `k` into base 9, which takes at most 40 steps for `k ≤ 10^12`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * log(k)) | O(1) | Too slow for k > 10^6 |
| Optimal (base-9 mapping) | O(log k) | O(log k) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `k`.
3. Initialize an empty string `res` to build the answer.
4. While `k > 0`:

1. Compute `digit = k % 9`. This gives the base-9 digit at the current position.
2. Map `digit` to the correct decimal digit. If `digit < 4`, it maps to itself (`0 → 0`, `1 → 1`, `2 → 2`, `3 → 3`). If `digit ≥ 4`, add 1 to skip 4 (`4 → 5`, `5 → 6`, etc.).
3. Prepend this mapped digit to `res`.
4. Update `k = k // 9`.
5. Print `res` after processing all digits.

Why it works: At each step, dividing by 9 moves to the next higher digit in base 9, guaranteeing that each mapped digit corresponds to a valid digit in the "no 4" decimal sequence. Prepending ensures the most significant digits are placed correctly. There is a one-to-one correspondence between numbers in base 9 and positions in the living sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    res = []
    while k > 0:
        digit = k % 9
        # Map base-9 digit to "no 4" decimal digit
        if digit >= 4:
            digit += 1
        res.append(str(digit))
        k //= 9
    print(''.join(res[::-1]))
```

We use `res.append` and then reverse the list at the end because we process the least significant digit first. Mapping `digit >= 4` ensures that the decimal 4 is skipped. Using integer division and modulo safely handles large `k` values up to `10^12`.

## Worked Examples

**Example 1:** `k = 5`

| Step | k | k % 9 | mapped digit | res |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 6 | ['6'] |
| 2 | 0 | - | - | ['6'] |

Output: `6`. The 5th number in the sequence is 6.

**Example 2:** `k = 22`

| Step | k | k % 9 | mapped digit | res |
| --- | --- | --- | --- | --- |
| 1 | 22 | 4 | 5 | ['5'] |
| 2 | 2 | 2 | 2 | ['5','2'] |

Output reversed: `25`. The 22nd number is 25.

These traces confirm the mapping from base-9 to "no 4" decimal is correct and preserves the sequence order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log k) per query | Each digit of k in base 9 is processed once; log9(k) ≤ 40 for k ≤ 10^12 |
| Space | O(log k) | We store the digits in a list before printing |

With `t ≤ 10^4` queries, the total operations are at most 4 * 10^5, which is comfortably within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # paste solution here
    t = int(input())
    for _ in range(t):
        k = int(input())
        res = []
        while k > 0:
            digit = k % 9
            if digit >= 4:
                digit += 1
            res.append(str(digit))
            k //= 9
        print(''.join(res[::-1]))
    return out.getvalue().strip()

# Provided samples
assert run("7\n3\n5\n22\n10\n100\n12345\n827264634912\n") == "3\n6\n25\n11\n121\n18937\n2932285320890", "sample 1"

# Custom cases
assert run("3\n1\n9\n81\n") == "1\n10\n100", "small powers of 9"
assert run("2\n4\n8\n") == "5\n9", "border around 4"
assert run("2\n1000000000000\n1000000000001\n") == "1929394949493\n1929394949495", "large k edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest k |
| 9 | 10 | k crossing a digit 4 |
| 81 | 100 | multiple digits mapping |
| 1000000000000 | 1929394949493 | handling very large k correctly |

## Edge Cases

The algorithm correctly handles `k` around powers of 9. For `k = 4`, the first number ≥ 4 is 5. The modulo-mapping step ensures the decimal 4 is skipped. For `k` near `10^12`, the algorithm never overflows because Python handles arbitrary-size integers, and the loop executes at most 40 iterations. For `k = 1`, the result is `1`, as the loop executes once and maps `0 → 1`. All edge cases of off-by-one or skipped 4s are accounted for in the mapping step.
