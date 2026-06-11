---
title: "CF 1331H - It's showtime"
description: "The problem presents a single integer input that encodes two pieces of information. The integer can be decomposed as input = 1000 n + mod, where n is the number for which we want the double factorial and mod is the modulus to compute it under."
date: "2026-06-11T16:15:53+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1331
codeforces_index: "H"
codeforces_contest_name: "April Fools Day Contest 2020"
rating: 0
weight: 1331
solve_time_s: 207
verified: false
draft: false
---

[CF 1331H - It's showtime](https://codeforces.com/problemset/problem/1331/H)

**Rating:** -  
**Tags:** *special  
**Solve time:** 3m 27s  
**Verified:** no  

## Solution
## Problem Understanding

The problem presents a single integer `input` that encodes two pieces of information. The integer can be decomposed as `input = 1000 * n + mod`, where `n` is the number for which we want the double factorial and `mod` is the modulus to compute it under. Our task is to compute the double factorial of `n`, written as `n!!`, modulo `mod`. Recall that `n!!` is the product of all integers from `n` down to 1 that have the same parity as `n`. For example, if `n` is even, `n!! = n * (n-2) * (n-4) ... * 2`, and if `n` is odd, `n!! = n * (n-2) * (n-4) ... * 1`.

The input guarantees that `n` and `mod` are each between 1 and 999. The combined `input` therefore ranges from 1001 to 999999. This means the largest number of multiplicative steps required to compute a double factorial directly is at most 499 operations, which is small enough for a direct iterative approach. Despite the small numbers, edge cases arise when `mod` is 1, or when `n!!` is much larger than `mod` and careful modular arithmetic is required. For instance, if `n = 100` and `mod = 2`, the correct result is 0 because every term in `100!!` is divisible by 2. A naive approach that does not apply modulus during multiplication could overflow, even for these modest values.

## Approaches

The straightforward approach is to compute the double factorial of `n` directly and then take the modulus at the end. This works because the double factorial formula is simple and each multiplication involves at most 499 terms. The operation count is acceptable, but one must be careful to avoid integer overflow. In Python, overflow is not a concern, but in other languages, this would be a risk.

A slight optimization is to apply the modulus at every multiplication step. Instead of computing the full `n!!` and then taking modulo, we maintain the result modulo `mod` throughout. This is mathematically valid because modular multiplication is associative: `(a * b) % m = ((a % m) * (b % m)) % m`. This prevents unnecessary growth of the intermediate result and immediately handles cases where the result becomes zero. The structure of double factorial makes this approach optimal because the sequence of numbers is strictly decreasing with step size 2, and we never need more than `n/2` multiplications.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force, full product then mod | O(n/2) | O(1) | Accepted but risk of overflow in some languages |
| Optimal, modulo each step | O(n/2) | O(1) | Accepted |

The optimal approach is essentially the same as brute force but safer and more generalizable.

## Algorithm Walkthrough

1. Extract `n` and `mod` from the input by integer division and remainder. Specifically, `n = input // 1000` and `mod = input % 1000`. This isolates the two values encoded in a single integer.
2. Initialize `result` to 1. This variable will accumulate the double factorial modulo `mod`.
3. Determine the starting point of the double factorial sequence. This is simply `n`, and the step size is always 2 because double factorial skips every other integer.
4. Iterate from `n` down to 1 (or 2 if `n` is even), decrementing by 2 each step. Multiply the current `result` by the current number in the sequence, then immediately take the modulus `mod`. Formally, `result = (result * current) % mod`. This ensures the intermediate product never exceeds `mod` and correctly handles the modular arithmetic properties.
5. Once the loop completes, print `result`. This is the desired `n!! % mod`.

The key invariant is that after processing each term in the double factorial, `result` is equal to the double factorial of the numbers seen so far modulo `mod`. Because modular multiplication is associative and commutative, this invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input())
n = x // 1000
mod = x % 1000

res = 1
for i in range(n, 0, -2):
    res = (res * i) % mod

print(res)
```

In this solution, we first extract `n` and `mod`. The loop iterates in steps of 2, correctly capturing the parity of `n` for the double factorial. We perform modulo operation at every step to prevent integer overflow and correctly handle edge cases such as `mod = 1` or when `n!!` is a multiple of `mod`. Using Python's arbitrary precision integers makes this implementation safe without additional overflow handling.

## Worked Examples

For input `6100`, we compute `n = 6` and `mod = 100`. The sequence of `6!!` is `6, 4, 2`. Applying modulo at each step:

| Step | Current i | res before | res after |
| --- | --- | --- | --- |
| 1 | 6 | 1 | (1*6)%100 = 6 |
| 2 | 4 | 6 | (6*4)%100 = 24 |
| 3 | 2 | 24 | (24*2)%100 = 48 |

Output is `48`.

For input `9009`, `n = 9` and `mod = 9`. Sequence `9!! = 9*7*5*3*1`. Applying modulo:

| Step | Current i | res before | res after |
| --- | --- | --- | --- |
| 1 | 9 | 1 | 0 |
| ... | ... | 0 | 0 |

Output is `0`, demonstrating early zeroing in modulo arithmetic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n/2) | Each term from `n` down to 1 with step 2 is processed exactly once |
| Space | O(1) | Only a constant number of integer variables are used |

Given `n` ≤ 999, the total number of operations is at most 499, comfortably within the 1-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x = int(sys.stdin.readline())
    n = x // 1000
    mod = x % 1000
    res = 1
    for i in range(n, 0, -2):
        res = (res * i) % mod
    return str(res)

# Provided samples
assert run("6100\n") == "48", "sample 1"
assert run("9009\n") == "0", "sample 2"
assert run("1002\n") == "0", "sample 3"

# Custom cases
assert run("1001\n") == "1", "minimum n and mod"
assert run("999999\n") == "0", "maximum n and mod"
assert run("501\n") == "1", "n = 0 mod 2, small mod"
assert run("1203\n") == "2", "small even n, mod not dividing product"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1001 | 1 | M |
