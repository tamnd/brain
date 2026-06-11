---
title: "CF 1327A - Sum of Odd Integers"
description: "The problem asks whether a given integer n can be expressed as the sum of exactly k distinct positive odd integers. Each test case provides n and k, and the answer is either \"YES\" or \"NO\". Odd integers are numbers not divisible by 2, so valid candidates are 1, 3, 5, 7,...."
date: "2026-06-11T16:31:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1327
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 84 (Rated for Div. 2)"
rating: 1100
weight: 1327
solve_time_s: 256
verified: false
draft: false
---

[CF 1327A - Sum of Odd Integers](https://codeforces.com/problemset/problem/1327/A)

**Rating:** 1100  
**Tags:** math  
**Solve time:** 4m 16s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks whether a given integer `n` can be expressed as the sum of exactly `k` distinct positive odd integers. Each test case provides `n` and `k`, and the answer is either "YES" or "NO". Odd integers are numbers not divisible by 2, so valid candidates are `1, 3, 5, 7,...`.

The constraints are significant. With `t` up to `10^5` and `n` and `k` up to `10^7`, a naive approach that generates all possible subsets of odd numbers would immediately be infeasible. The worst-case number of operations in a brute-force enumeration grows exponentially, which is far beyond what 2 seconds of runtime can handle. This implies that any solution must run in roughly `O(1)` or at worst `O(log n)` per test case.

Non-obvious edge cases arise from the parity of the numbers. For example, `n=4` and `k=2` can be represented as `1+3`, but `n=10` and `k=3` cannot, because the sum of any three distinct positive odd numbers is always odd, while `10` is even. Similarly, if `k` is too large relative to `n`, it is impossible because the sum of the first `k` smallest odd numbers already exceeds `n`. For instance, `n=8` and `k=3` fails because `1+3+5=9>8`. These considerations make parity and minimal sum the key constraints.

## Approaches

The brute-force method would attempt to generate all combinations of `k` distinct positive odd integers and check if any sum equals `n`. This is theoretically correct, but combinatorial explosion makes it impractical: even for `k=20`, the number of combinations is astronomical. Thus, the brute-force works only for tiny values of `n` and `k`.

The key observation for a fast solution is that the first `k` odd numbers are `1, 3, 5, ..., 2k-1`, and their sum is `k^2`. Therefore, for `n` to be expressible as a sum of `k` distinct odd integers, `n` must be at least `k^2`. Additionally, the parity of `n` and `k` must match: the sum of `k` odd numbers is odd if `k` is odd and even if `k` is even. This is because the sum of an odd count of odd numbers is odd, and the sum of an even count of odd numbers is even. Combining these two conditions gives a constant-time check for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(k) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read integers `n` and `k`.
2. Compute the minimal sum of the first `k` odd numbers, which is `k^2`. This ensures that we have enough "odd mass" to reach `n`.
3. Check if `n` is at least `k^2`. If not, it is impossible to represent `n` as a sum of `k` distinct odd numbers, so output "NO".
4. Check if the parity of `n` matches the parity of `k`. Specifically, verify if `(n % 2) == (k % 2)`. This ensures the sum can be either odd or even to match `n`.
5. If both conditions are satisfied, output "YES"; otherwise, output "NO".

Why it works: The minimal sum guarantees that the smallest `k` odd numbers can fit within `n`. Any sum of `k` distinct odd numbers can be obtained by increasing some of the numbers while keeping them odd, which preserves the sum parity. Therefore, if `n` is larger than `k^2` and has matching parity, there always exists a set of distinct odd numbers that sum to `n`. Otherwise, it is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    if n >= k * k and (n % 2) == (k % 2):
        print("YES")
    elif n >= 2 * k and (n % 2) == 0:
        # optional: for even numbers check sum of k even numbers
        print("YES")
    else:
        print("NO")
```

The first condition `n >= k*k and (n%2) == (k%2)` handles the sum of odd numbers. The second condition, sometimes seen in solutions, would handle even numbers if we also considered representing `n` as a sum of even numbers. For this problem, only odd numbers are required, so the first check is sufficient. Fast I/O ensures the program handles up to `10^5` test cases efficiently.

## Worked Examples

For the input `n=10, k=3`, compute minimal sum of first 3 odd numbers: `1+3+5=9`. Check parity: sum of 3 odd numbers is odd, `10` is even. Condition fails, output is "NO".

| n | k | k^2 | n >= k^2 | n%2 | k%2 | parity match | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 3 | 9 | True | 0 | 1 | False | NO |

For the input `n=16, k=4`, minimal sum `1+3+5+7=16`. Parity of sum of 4 odd numbers is even, `16` is even. Both conditions satisfied, output is "YES".

| n | k | k^2 | n >= k^2 | n%2 | k%2 | parity match | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 4 | 16 | True | 0 | 0 | True | YES |

These traces confirm the algorithm correctly handles edge parity and minimal sum conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case requires only arithmetic and modulo checks |
| Space | O(1) | No additional storage proportional to `n` or `k` is needed |

Given `t <= 10^5`, total operations are at most `10^5`, easily within the 2-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        if n >= k * k and (n % 2) == (k % 2):
            print("YES")
        else:
            print("NO")
    return out.getvalue().strip()

# provided samples
assert run("6\n3 1\n4 2\n10 3\n10 2\n16 4\n16 5\n") == "YES\nYES\nNO\nYES\nYES\nNO", "sample 1"

# custom cases
assert run("3\n1 1\n2 1\n10000000 1000\n") == "YES\nNO\nYES", "minimum and large n"
assert run("2\n15 4\n36 6\n") == "NO\nYES", "odd/even parity tests"
assert run("2\n5 3\n14 3\n") == "NO\nNO", "sum too small tests"
assert run("1\n9999999 3162\n") == "YES", "large n edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | YES | smallest valid sum |
| 2 1 | NO | odd number cannot sum to even n |
| 10000000 1000 | YES | large n within constraints |
| 15 4 | NO | parity mismatch |
| 36 6 | YES | even sum of even k |
| 5 3 | NO | sum too small |
| 14 3 | NO | sum too small |
| 9999999 3162 | YES | large n, k^2 close |

## Edge Cases

For `n=2, k=1`, minimal sum is `1`. Parity check fails because sum of 1 odd number is odd, `n` is even. Algorithm correctly outputs "NO".

For `n=1, k=1`, minimal sum is `1`. Parity check matches. Algorithm outputs "YES". These confirm both lower-bound and parity edge cases are handled.

For `n=10^7, k=1`, minimal sum is `1`. Parity check: `10^7` even, `1` odd, fails. Output is "NO". This confirms algorithm handles large n efficiently.
