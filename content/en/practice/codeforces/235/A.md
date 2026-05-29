---
title: "CF 235A - LCM Challenge"
description: "We need to choose three positive integers, each no larger than n, so that their least common multiple is as large as possible. The numbers may repeat, but repetition is usually not useful because equal numbers do not introduce new prime factors into the LCM."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 1600
weight: 235
solve_time_s: 210
verified: true
draft: false
---

[CF 235A - LCM Challenge](https://codeforces.com/problemset/problem/235/A)

**Rating:** 1600  
**Tags:** number theory  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to choose three positive integers, each no larger than `n`, so that their least common multiple is as large as possible. The numbers may repeat, but repetition is usually not useful because equal numbers do not introduce new prime factors into the LCM.

The input contains a single integer `n`. The output is the maximum LCM obtainable from any triple `(a, b, c)` where `1 ≤ a, b, c ≤ n`.

The limit is only `10^6`, which is small for arithmetic operations but enormous for brute force over triples. A naive search would examine roughly `n^3` combinations. For `n = 10^6`, that becomes `10^18` triples, which is completely impossible within two seconds.

The interesting part of the problem is that the optimal answer always comes from numbers very close to `n`. We do not need to search the whole range.

There are several edge cases that easily break careless solutions.

When `n = 1`, the only possible triple is `(1, 1, 1)`, so the answer is `1`. A formula like `n * (n - 1) * (n - 2)` would incorrectly produce `0`.

For `n = 2`, the best choice is `(2, 2, 1)` with LCM `2`. Using three distinct numbers is impossible here.

For even values of `n`, taking `(n, n - 1, n - 2)` is not always optimal because `n` and `n - 2` share a factor of `2`. For example:

Input:

```
4
```

A naive "largest three numbers" strategy gives:

`LCM(4, 3, 2) = 12`

But choosing `(4, 3, 1)` gives:

`LCM(4, 3, 1) = 12`

In this case they tie, but for larger even values the gap becomes real.

Input:

```
6
```

`LCM(6, 5, 4) = 60`

But:

`LCM(5, 4, 3) = 60`

Again equal here, but consider:

Input:

```
8
```

`LCM(8, 7, 6) = 168`

While:

`LCM(7, 6, 5) = 210`

The common factors inside `(8, 7, 6)` waste part of the product.

Another subtle case is when `n` is even but not divisible by `3`. Then the triple `(n, n - 1, n - 3)` often becomes optimal because it avoids both the shared factor `2` and unnecessary overlap with `3`.

## Approaches

The brute-force solution is straightforward. Enumerate every possible triple `(a, b, c)` with values from `1` to `n`, compute `LCM(a, b, c)`, and keep the maximum.

This works because it checks every valid combination. The problem is the running time. There are `n^3` triples. With `n = 10^6`, this becomes roughly `10^18` iterations. Even if each iteration took only one CPU instruction, it would still be hopelessly slow.

The key observation is that the maximum LCM must come from large numbers near `n`. If one of the chosen values is much smaller than `n`, replacing it with a larger nearby value usually increases the LCM or keeps it unchanged.

For odd `n`, the answer is especially clean. The numbers `n`, `n - 1`, and `n - 2` are consecutive, and since `n` is odd, these three numbers are pairwise "good enough" with respect to common divisors. Their LCM becomes exactly their product:

$$n(n-1)(n-2)$$

For even `n`, things become trickier because both `n` and `n - 2` are even. Their shared factor reduces the LCM. We need to avoid unnecessary overlap.

There are two important cases.

If `n` is even and not divisible by `3`, then:

$$LCM(n, n-1, n-3)$$

becomes optimal.

If `n` is divisible by `3`, then both `n` and `n - 3` share a factor of `3`, so it is better to skip `n` entirely and use:

$$(n-1)(n-2)(n-3)$$

This works because three consecutive numbers below an even multiple of `3` are pairwise favorable for the LCM.

The entire problem reduces to a few arithmetic formulas.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Handle very small values separately.

If `n = 1`, the only possible LCM is `1`.

If `n = 2`, the best achievable LCM is `2`.
3. If `n` is odd, return:

$$n(n-1)(n-2)$$

Consecutive numbers around an odd value avoid large common divisors, so the LCM equals their product.
4. If `n` is even and divisible by `3`, return:

$$(n-1)(n-2)(n-3)$$

Using `n` would introduce overlap with both `2` and `3`, reducing the LCM.
5. Otherwise, `n` is even but not divisible by `3`. Return:

$$n(n-1)(n-3)$$

This keeps the largest number `n` while avoiding the shared factor between `n` and `n-2`.

### Why it works

The maximum LCM comes from maximizing the product of distinct prime factors contributed by the chosen numbers. Large overlapping factors are harmful because the LCM only keeps the highest power of each prime once.

For odd `n`, the three largest consecutive numbers are already almost pairwise coprime, so their LCM equals their product.

For even `n`, choosing both `n` and `n-2` introduces a shared factor of `2`. If `n` is also divisible by `3`, then `n` and `n-3` share a factor of `3` as well. The optimal formulas are precisely the triples that keep the numbers large while minimizing duplicated prime factors.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n == 1:
    print(1)
elif n == 2:
    print(2)
elif n % 2 == 1:
    print(n * (n - 1) * (n - 2))
elif n % 3 == 0:
    print((n - 1) * (n - 2) * (n - 3))
else:
    print(n * (n - 1) * (n - 3))
```

The first two conditions handle the tiny inputs where the general formulas do not apply. Without these checks, expressions like `(n - 2)` would become zero or negative.

The odd case is the simplest one. Since consecutive numbers around an odd value do not create harmful overlap, the LCM becomes the direct product.

The even branch splits according to divisibility by `3`. When `n` is divisible by `3`, using `n` wastes part of the LCM because several factors are duplicated. Skipping `n` entirely produces a larger result.

Python integers automatically support arbitrary precision, so overflow is not a concern. In languages like C++ or Java, a 64-bit integer type is necessary because the result can exceed `2^31 - 1`.

## Worked Examples

### Example 1

Input:

```
9
```

Since `9` is odd, we use:

$$9 \times 8 \times 7$$

| Step | Value |
| --- | --- |
| n | 9 |
| n is odd | Yes |
| Formula used | n(n-1)(n-2) |
| Computation | 9 × 8 × 7 |
| Answer | 504 |

This example demonstrates the clean odd-number case where the maximum LCM equals the product of the three largest consecutive numbers.

### Example 2

Input:

```
8
```

Since `8` is even and not divisible by `3`, we use:

$$8 \times 7 \times 5$$

| Step | Value |
| --- | --- |
| n | 8 |
| n is odd | No |
| n divisible by 3 | No |
| Formula used | n(n-1)(n-3) |
| Computation | 8 × 7 × 5 |
| Answer | 280 |

This case shows why `(8,7,6)` is not optimal. The numbers `8` and `6` both contribute a factor of `2`, which lowers the LCM.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and condition checks |
| Space | O(1) | No extra memory proportional to input size |

The algorithm performs constant-time work regardless of `n`. This easily fits within the two-second time limit and the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    if n == 1:
        print(1)
    elif n == 2:
        print(2)
    elif n % 2 == 1:
        print(n * (n - 1) * (n - 2))
    elif n % 3 == 0:
        print((n - 1) * (n - 2) * (n - 3))
    else:
        print(n * (n - 1) * (n - 3))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("9\n") == "504\n", "sample 1"

# minimum input
assert run("1\n") == "1\n", "n = 1"

# small even input
assert run("2\n") == "2\n", "n = 2"

# even divisible by 3
assert run("6\n") == "60\n", "divisible by 3 case"

# even not divisible by 3
assert run("8\n") == "280\n", "general even case"

# large odd input
assert run("999999\n") == "999994000010999994\n", "large odd case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum boundary |
| `2` | `2` | Small even edge case |
| `6` | `60` | Even number divisible by 3 |
| `8` | `280` | Even number not divisible by 3 |
| `999999` | `999994000010999994` | Large-value arithmetic correctness |

## Edge Cases

When `n = 1`, the algorithm immediately returns `1`.

Input:

```
1
```

Execution trace:

| Check | Result |
| --- | --- |
| n == 1 | True |
| Output | 1 |

This prevents invalid expressions involving `n - 2`.

When `n = 2`, the algorithm returns `2`.

Input:

```
2
```

Execution trace:

| Check | Result |
| --- | --- |
| n == 1 | False |
| n == 2 | True |
| Output | 2 |

The best triple here is `(2,2,1)`.

When `n` is even and divisible by `3`, the algorithm skips `n`.

Input:

```
12
```

Execution trace:

| Check | Result |
| --- | --- |
| n odd | False |
| n % 3 == 0 | True |
| Formula | 11 × 10 × 9 |
| Output | 990 |

Using `(12,11,10)` would produce:

$$LCM(12,11,10)=660$$

The overlap from factors `2` and `3` makes it worse.

When `n` is even but not divisible by `3`, the algorithm keeps `n` but avoids `n-2`.

Input:

```
8
```

Execution trace:

| Check | Result |
| --- | --- |
| n odd | False |
| n % 3 == 0 | False |
| Formula | 8 × 7 × 5 |
| Output | 280 |

The naive choice `(8,7,6)` only gives:

$$168$$

because `8` and `6` share a factor of `2`.
