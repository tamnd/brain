---
title: "CF 1352A - Sum of Round Numbers"
description: "We are asked to take a positive integer and break it into a sum of “round numbers,” which are numbers where all digits except the most significant are zero. For example, 4000, 10, 7, and 800 are round, while 110, 707, and 222 are not."
date: "2026-06-11T14:11:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1352
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 640 (Div. 4)"
rating: 800
weight: 1352
solve_time_s: 187
verified: false
draft: false
---

[CF 1352A - Sum of Round Numbers](https://codeforces.com/problemset/problem/1352/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 3m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to take a positive integer and break it into a sum of “round numbers,” which are numbers where all digits except the most significant are zero. For example, 4000, 10, 7, and 800 are round, while 110, 707, and 222 are not. Given a number `n`, the goal is to express it as a sum of round numbers using the fewest terms possible.

The input consists of multiple test cases. Each test case gives a number `n` between 1 and 10,000. The output for each test case must start with `k`, the number of round numbers in the sum, followed by the `k` numbers themselves. Any order is acceptable, as long as their sum is `n`.

The upper bound of `n` being 10,000 allows simple digit-wise operations without performance concerns, since we can at most have four non-zero digits. The number of test cases `t` is also at most 10,000, so the solution must handle tens of millions of basic operations efficiently.

A subtle edge case occurs when `n` itself is already a round number, like 1000 or 7. The correct output is just the number itself with `k = 1`. A careless solution might always try to split digits and end up with unnecessary zero terms, which are invalid because a round number must be positive. Another edge case is numbers like 1010, which need to be split into `1000` and `10`-a naive approach might try to include zero as a term.

## Approaches

The most obvious brute-force approach is to try every possible round number less than `n` and subtract it recursively until reaching zero. This is correct but unnecessary. The number of possible round numbers below 10,000 is small, but recursion or nested loops are overkill, and managing all combinations becomes tedious.

The key insight is that every positive integer can be decomposed into its non-zero digits multiplied by their place value. For example, 5072 can be seen as `5000 + 70 + 2`. Each of these components is by definition a round number. This works because a round number is just a non-zero digit followed by zeros, exactly what you get when you multiply a digit by its positional value.

Thus the optimal solution is to iterate through the digits of `n`, from least significant to most significant, and for each non-zero digit `d` at position `p` (0-based from the right), generate `d * 10^p` as a round number. Collect all such numbers and output them. This guarantees the minimum number of terms because each non-zero digit contributes exactly one term, and no term can be merged without introducing a non-round number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^d) | O(d) | Too slow |
| Optimal | O(log n) per test case | O(log n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the integer `n`.
3. Initialize an empty list to hold the round numbers for this `n`.
4. Initialize a multiplier `m = 1`, representing the current digit's place value (units, tens, hundreds, ...).
5. While `n > 0`, extract the least significant digit `digit = n % 10`.
6. If `digit` is not zero, append `digit * m` to the list of round numbers. This forms a valid round number corresponding to the current place.
7. Divide `n` by 10 using integer division to remove the processed digit.
8. Multiply `m` by 10 to move to the next higher place value.
9. After processing all digits, the list contains all the round numbers. Output the number of elements in the list, followed by the elements themselves.

Why it works: The loop guarantees we process every digit exactly once, and only non-zero digits are converted to round numbers. Each term is positive, and their sum reconstructs the original number. There is no redundancy because each non-zero digit contributes exactly one round number, ensuring the minimal number of summands.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    round_numbers = []
    m = 1
    temp = n
    while temp > 0:
        digit = temp % 10
        if digit != 0:
            round_numbers.append(digit * m)
        temp //= 10
        m *= 10
    print(len(round_numbers))
    print(*round_numbers)
```

The code reads the number of test cases, then for each `n` calculates its decomposition into round numbers. We use a temporary variable `temp` to iterate through digits without modifying the original `n`. The multiplier `m` handles the place value of each digit. Appending only non-zero terms avoids invalid zeros. Printing uses unpacking for brevity.

## Worked Examples

**Example 1: n = 5009**

| Step | temp | digit | m | round_numbers |
| --- | --- | --- | --- | --- |
| 1 | 5009 | 9 | 1 | [9] |
| 2 | 500 | 0 | 10 | [9] |
| 3 | 50 | 0 | 100 | [9] |
| 4 | 5 | 5 | 1000 | [9,5000] |
| 5 | 0 | - | 10000 | [9,5000] |

Output: `2` and `5000 9`

This confirms the algorithm correctly splits digits, ignores zeros, and generates round numbers in minimal quantity.

**Example 2: n = 1010**

| Step | temp | digit | m | round_numbers |
| --- | --- | --- | --- | --- |
| 1 | 1010 | 0 | 1 | [] |
| 2 | 101 | 1 | 10 | [10] |
| 3 | 10 | 0 | 100 | [10] |
| 4 | 1 | 1 | 1000 | [10,1000] |
| 5 | 0 | - | 10000 | [10,1000] |

Output: `2` and `10 1000`

This demonstrates handling of zeros in the middle of the number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * log n) | Each test case iterates through the digits of n, at most 5 iterations for n ≤ 10000. |
| Space | O(log n) | Storing non-zero digits as round numbers; maximum 5 elements for n ≤ 10000. |

With t ≤ 10,000 and n ≤ 10,000, the total operations are on the order of 50,000, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        round_numbers = []
        m = 1
        temp = n
        while temp > 0:
            digit = temp % 10
            if digit != 0:
                round_numbers.append(digit * m)
            temp //= 10
            m *= 10
        print(len(round_numbers))
        print(*round_numbers)
    return out.getvalue().strip()

# Provided samples
assert run("5\n5009\n7\n9876\n10000\n10\n") == "2\n9 5000\n1\n7\n4\n6 70 800 9000\n1\n10000\n1\n10", "sample 1"

# Custom cases
assert run("1\n1\n") == "1\n1", "minimum n"
assert run("1\n9999\n") == "4\n9 90 900 9000", "all 9s"
assert run("1\n1010\n") == "2\n10 1000", "zeros in middle"
assert run("1\n1001\n") == "2\n1 1000", "zeros in middle, edge digits"
assert run("1\n5000\n") == "1\n5000", "single round number"

| Test input | Expected output | What it validates |
|---|---|---|
| 1 | 1 1 | minimum n |
| 9999 | 4 9 90 900 9000 | multi-digit all non-zero |
| 1010 | 2 10 1000 | handling zeros |
| 1001 | 2 1 1000 | zeros at middle |
| 5000 | 1 5000 | input is already round |
```

## Edge Cases

For `n = 1`, the loop processes digit `1` with `m = 1` and outputs `[1]`, correctly returning `k = 1`. For `n = 1000`, the digits are 0,0,0,1, producing `[1000]`, skipping zeros. For `n = 1010`, zeros are ignored, producing `[10, 1000]
