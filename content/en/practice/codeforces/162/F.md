---
title: "CF 162F - Factorial zeros"
description: "The task is to determine how many trailing zeros appear at the end of the factorial of a given integer n. A factorial, denoted n!, is the product of all integers from 1 up to n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "F"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 63
verified: true
draft: false
---

[CF 162F - Factorial zeros](https://codeforces.com/problemset/problem/162/F)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to determine how many trailing zeros appear at the end of the factorial of a given integer _n_. A factorial, denoted _n!_, is the product of all integers from 1 up to _n_. Trailing zeros are the consecutive zeros at the rightmost end of this number, which occur whenever the number is divisible by 10. Since 10 is the product of 2 and 5, each trailing zero corresponds to a pair of factors 2 and 5 in the factorial product.

The input is a single integer _n_ with an upper bound of 1,000,000. This limit rules out naive approaches that attempt to compute the factorial explicitly, because _n!_ grows extremely fast and cannot be stored in standard numeric types for large _n_. Even with arbitrary-precision arithmetic, directly multiplying numbers up to 1,000,000 would be far too slow, on the order of millions of multiplications.

The subtlety comes from recognizing that factors of 2 are far more abundant than factors of 5 in a factorial. For example, in 10!, the factors of 2 occur in 2, 4, 6, 8, 10, while factors of 5 occur only in 5 and 10. This means the number of trailing zeros is determined entirely by the count of factors of 5. A naive approach that attempts to divide the factorial by 10 repeatedly or count 10s explicitly would fail for large _n_ due to both performance and numeric overflow.

Edge cases include very small numbers such as 1 or 4, where the factorial has no trailing zeros. For example, 1! = 1 and 4! = 24 both produce zero trailing zeros. Another edge case is exact powers of 5, like 5 or 25, which add more than one zero when multiples of 25, 125, etc., are included.

## Approaches

The brute-force solution would attempt to compute _n!_ explicitly, either storing it or counting trailing zeros as we multiply. While this approach is conceptually simple, it requires O(n) multiplications and results in numbers with hundreds of thousands of digits for _n_ near 1,000,000, making it infeasible in practice.

The key insight is that a trailing zero is produced by a factor of 10, which in turn requires a factor of 5 paired with a factor of 2. Factors of 2 are abundant, so the count of 5s directly determines the number of trailing zeros. To count the number of 5s in _n!_, we need to sum the integer divisions of _n_ by powers of 5: n//5 counts numbers divisible by 5, n//25 counts numbers divisible by 25 (which contribute an extra factor of 5), n//125 counts numbers divisible by 125, and so on. This continues until 5^k exceeds _n_. This approach reduces the problem to O(log_5 n) operations, which is extremely fast for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) multiplications, very large intermediate numbers | O(1) or O(n) depending on storage | Too slow |
| Optimal | O(log_5 n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `zeros` to 0. This will accumulate the total number of trailing zeros.
2. Set a variable `power_of_5` to 5, representing the current power of 5 being considered.
3. While `power_of_5` is less than or equal to `n`, compute `n // power_of_5` and add it to `zeros`. This counts the numbers divisible by this power of 5, each contributing additional factors of 5 to the factorial.
4. Multiply `power_of_5` by 5 to move to the next higher power.
5. Repeat step 3 until `power_of_5` exceeds `n`.
6. Output the value of `zeros`.

Why it works: Each number divisible by 5 contributes at least one factor of 5. Numbers divisible by 25 contribute an additional factor, those divisible by 125 contribute yet another, and so on. Summing these counts ensures every factor of 5 is counted exactly once, which pairs with the abundant factors of 2 to determine the exact number of trailing zeros.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
zeros = 0
power_of_5 = 5
while power_of_5 <= n:
    zeros += n // power_of_5
    power_of_5 *= 5
print(zeros)
```

The solution first reads the integer input. The loop iteratively sums contributions from each power of 5, starting with 5 itself and increasing exponentially. Multiplying `power_of_5` by 5 ensures we only consider higher powers that contribute extra factors of 5. The result is printed directly. Care is taken to avoid off-by-one errors by using `<=` in the loop condition, ensuring that powers of 5 exactly equal to `n` are counted.

## Worked Examples

Sample 1: n = 6

| power_of_5 | n // power_of_5 | zeros |
| --- | --- | --- |
| 5 | 6 // 5 = 1 | 1 |
| 25 | 6 // 25 = 0 | 1 |

The algorithm adds 1 from the numbers divisible by 5, then stops because 25 > 6. The result is 1 trailing zero.

Sample 2: n = 24

| power_of_5 | n // power_of_5 | zeros |
| --- | --- | --- |
| 5 | 24 // 5 = 4 | 4 |
| 25 | 24 // 25 = 0 | 4 |

Numbers divisible by 5 contribute 4 factors of 5. There are no higher powers of 5 within 24. The factorial 24! has 4 trailing zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log_5 n) | Each iteration multiplies `power_of_5` by 5, producing logarithmic number of steps in base 5 |
| Space | O(1) | Only a few integer variables are stored, independent of n |

Given n ≤ 10^6, log_5(n) ≈ 10, so the algorithm performs at most 10 iterations. This easily fits in the 3-second time limit with negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    zeros = 0
    power_of_5 = 5
    while power_of_5 <= n:
        zeros += n // power_of_5
        power_of_5 *= 5
    return str(zeros)

# provided samples
assert run("6\n") == "1", "sample 1"
assert run("24\n") == "4", "sample 2"

# custom cases
assert run("1\n") == "0", "minimum input"
assert run("5\n") == "1", "exactly one factor of 5"
assert run("25\n") == "6", "includes power of 25"
assert run("1000000\n") == "249998", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | Handles minimum input, no trailing zeros |
| 5 | 1 | Correctly counts a single factor of 5 |
| 25 | 6 | Correctly sums factors from 5 and 25 |
| 1000000 | 249998 | Ensures algorithm handles large n efficiently |

## Edge Cases

For n = 1, the loop condition `5 <= 1` fails immediately, and `zeros` remains 0. The output is correctly 0, confirming the algorithm does not falsely detect trailing zeros for small numbers.

For n = 25, the first iteration adds 25 // 5 = 5, the second iteration adds 25 // 25 = 1, resulting in 6. There are exactly 6 factors of 5 in 25!, correctly producing 6 trailing zeros. The algorithm correctly handles numbers that are exact powers of 5.
