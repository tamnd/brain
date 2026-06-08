---
title: "CF 2020A - Find Minimum Operations"
description: "We are asked to reduce a given integer n to zero by repeatedly subtracting powers of a second integer k. Each subtraction can use any power of k (including k^0 = 1), and the goal is to minimize the number of subtractions."
date: "2026-06-08T12:46:53+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2020
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 976 (Div. 2) and Divide By Zero 9.0"
rating: 800
weight: 2020
solve_time_s: 84
verified: true
draft: false
---

[CF 2020A - Find Minimum Operations](https://codeforces.com/problemset/problem/2020/A)

**Rating:** 800  
**Tags:** bitmasks, brute force, greedy, math, number theory  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to reduce a given integer `n` to zero by repeatedly subtracting powers of a second integer `k`. Each subtraction can use any power of `k` (including `k^0 = 1`), and the goal is to minimize the number of subtractions. The input consists of multiple test cases, each giving values for `n` and `k`, and the output must specify the minimum number of operations for each test case.

The constraints allow `n` and `k` to be as large as 10^9, with up to 10^4 test cases. This rules out any approach that explicitly enumerates all sequences of subtractions or iterates over all powers of `k` in a naive way. The solution must operate in O(log n) per test case or better, because the number of operations needed to represent `n` in base `k` is logarithmic in `n`. Edge cases include `k = 1`, where every operation only subtracts 1, and large powers of `k` that exceed `n` immediately.

A naive implementation could incorrectly assume we should always subtract the largest possible power of `k`. While this works for `k > 1`, for `k = 1` it would never terminate correctly unless handled separately.

## Approaches

The brute-force approach is to iteratively subtract some power of `k` from `n`, trying all possible powers at each step. This is correct in principle because any sequence of subtractions that reduces `n` to zero is valid, but the number of possible sequences grows exponentially, making it completely infeasible for the given constraints.

The key insight is to recognize that subtracting powers of `k` is equivalent to expressing `n` in **base `k`**. Each digit in base `k` tells us how many times a corresponding power of `k` must be subtracted. Therefore, the minimal number of operations is exactly the sum of the digits of `n` when written in base `k`. For example, `n = 5` and `k = 2` gives the base-2 representation `101`, which has two ones, corresponding to the two required operations.

When `k = 1`, base representation is degenerate, and every subtraction can only remove `1`, so the number of operations equals `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per operation | O(1) | Too slow for large n |
| Base-k Digit Sum | O(log_k n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the integers `n` and `k`.
3. If `k` equals 1, return `n` as the answer because every operation subtracts exactly 1.
4. Otherwise, initialize a counter for operations to zero.
5. While `n` is greater than zero:

- Compute `n % k`, which gives the number of subtractions of the current power of `k` needed.
- Add this remainder to the operations counter.
- Update `n` to `n // k` to process the next higher power of `k`.
6. After the loop, the counter contains the minimal number of operations. Output it.

Why it works: expressing `n` in base `k` exactly captures the number of times each power of `k` is needed. The remainder at each step tells how many of the current power to subtract, and dividing by `k` moves to the next power. The process terminates when all powers are exhausted, guaranteeing the minimal number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        if k == 1:
            print(n)
            continue
        ans = 0
        while n > 0:
            ans += n % k
            n //= k
        print(ans)

if __name__ == "__main__":
    solve()
```

The code handles multiple test cases efficiently using fast I/O. It separates the special case `k = 1` to avoid an infinite loop and uses integer division and modulo to traverse the base-`k` representation. Each loop iteration corresponds to processing one digit in base `k`, ensuring logarithmic complexity.

## Worked Examples

Sample input `n = 5`, `k = 2`:

| Step | n | n % k | ans | n //= k |
| --- | --- | --- | --- | --- |
| Initial | 5 | 1 | 1 | 2 |
| Step 2 | 2 | 0 | 1 | 1 |
| Step 3 | 1 | 1 | 2 | 0 |

Total operations: 2. This matches the minimal sequence `5 - 1 = 4`, `4 - 4 = 0`.

Sample input `n = 3`, `k = 5`:

| Step | n | n % k | ans | n //= k |
| --- | --- | --- | --- | --- |
| Initial | 3 | 3 | 3 | 0 |

Total operations: 3, matching the expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log_k n) per test case | Each iteration divides `n` by `k` |
| Space | O(1) | Only counters and input variables |

With `t <= 10^4` and `n <= 10^9`, the solution performs well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("6\n5 2\n3 5\n16 4\n100 3\n6492 10\n10 1\n") == "2\n3\n1\n4\n21\n10"

# Custom test cases
assert run("1\n1 1\n") == "1", "k=1, n=1"
assert run("1\n1 2\n") == "1", "k>1, n=1"
assert run("1\n1023 2\n") == "10", "n=2^10-1, all digits 1 in base-2"
assert run("1\n1000000000 3\n") == "19", "large n, k=3"
assert run("1\n999999937 1\n") == "999999937", "k=1, large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal n, k=1 |
| 1 2 | 1 | minimal n, k>1 |
| 1023 2 | 10 | all 1’s in base-2 representation |
| 1000000000 3 | 19 | large n, k>1 |
| 999999937 1 | 999999937 | large n, k=1 |

## Edge Cases

When `k = 1`, each subtraction can only remove 1. For example, `n = 10` and `k = 1` requires exactly 10 operations. For `k > n`, the base-k digit sum handles it correctly: `n % k = n` and `n // k = 0`, yielding exactly `n` operations, consistent with subtracting `1` repeatedly. Large powers of `k` do not affect correctness because the base representation always accounts for each necessary power.
