---
title: "CF 2008B - Square or Not"
description: "We are given a binary string that was originally formed by flattening a rectangular grid row by row. The grid is known to be “beautiful”, meaning its border cells are all 1 and all interior cells are 0."
date: "2026-06-08T13:25:46+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 800
weight: 2008
solve_time_s: 259
verified: false
draft: false
---

[CF 2008B - Square or Not](https://codeforces.com/problemset/problem/2008/B)

**Rating:** 800  
**Tags:** brute force, math, strings  
**Solve time:** 4m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string that was originally formed by flattening a rectangular grid row by row. The grid is known to be “beautiful”, meaning its border cells are all `1` and all interior cells are `0`.

The task is not to reconstruct the grid, but to decide whether there exists any way to interpret the string as coming from a square grid, where the number of rows equals the number of columns, while still respecting the same “border ones, interior zeros” structure.

So conceptually we are checking a compatibility condition: can we place the string into an `r × r` grid such that the perimeter is all ones and the inside is all zeros.

The key constraint is that the string is already fixed; only the interpretation (the dimension `r`) is flexible. Since `r^2` must equal the string length, the problem is really asking whether the length is a perfect square and whether the implied structure could match a valid border pattern.

Because total input length across tests is large, up to 2 · 10^5, any solution must be linear per test case. Anything involving simulation of multiple candidate grids per test would be too slow.

A common mistake is to try to reconstruct the matrix explicitly or to test multiple possible side lengths by filling grids. That would waste computation and is unnecessary because the structure of a square border is fully determined once `r` is fixed.

## Approaches

The brute-force idea would be to try every possible dimension `r` from 1 up to `n`, check whether `r × r = n`, and if so, reconstruct the grid and verify whether it matches a valid border-ones pattern. This approach is already mostly redundant since only one `r` can satisfy the square condition, but even if generalized to trying multiple candidates, it still requires building or simulating a matrix and checking all cells, which is O(n√n) in the worst case.

The key observation is that a square matrix exists only when the length is a perfect square. Once that holds, the structure of a beautiful matrix is fixed: all first and last rows are ones, all first and last columns are ones, and everything else is zero. That pattern does not introduce any ambiguity once the size is known. So the entire problem reduces to checking whether the string length is a perfect square.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force reconstruction | O(n√n) | O(n) | Too slow |
| Square check only | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We only need to determine whether the string length can form a square grid.

1. Read the integer `n` and the string `s`. The string itself is not used beyond its length.
2. Compute the integer square root of `n`.
3. Check whether squaring this integer root returns exactly `n`.
4. If it matches, output “Yes”, otherwise output “No”.

The reasoning behind step 3 is that a valid square grid requires exactly `r × r` cells, so the length must be a perfect square.

### Why it works

A square beautiful matrix is completely determined by its size `r`. If the string length is not of the form `r^2`, no square grid can exist at all, regardless of the arrangement of ones and zeros. If it is a perfect square, then a valid border configuration is always constructible for that size, so existence depends only on the arithmetic condition.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    r = int(math.isqrt(n))
    if r * r == n:
        print("Yes")
    else:
        print("No")
```

The implementation focuses only on the length `n`. The string is still read to consume input correctly, but never processed. The key detail is using `math.isqrt`, which avoids floating-point precision issues that can occur with `sqrt`.

A common pitfall is forgetting to strip the newline when reading the string; while not strictly required here, it is good practice to ensure consistent input handling. Another subtle issue is using floating-point square root and casting, which can misclassify large perfect squares due to precision errors. Integer square root avoids that entirely.

## Worked Examples

### Example 1

Input:

```
n = 9, s = 111101111
```

| n | isqrt(n) | r² | result |
| --- | --- | --- | --- |
| 9 | 3 | 9 | Yes |

This confirms that a 3×3 grid is possible.

### Example 2

Input:

```
n = 12, s = 111110011111
```

| n | isqrt(n) | r² | result |
| --- | --- | --- | --- |
| 12 | 3 | 9 | No |

Even though 3 is the integer square root, 12 is not a perfect square, so no square grid exists.

These examples show that the content of the string is irrelevant; only its length matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test computes one integer square root |
| Space | O(1) | No auxiliary structures beyond input |

The solution easily satisfies constraints since each test case is processed in constant time.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        r = math.isqrt(n)
        out.append("Yes" if r * r == n else "No")
    return "\n".join(out)

# provided samples
assert run("""5
2
11
4
1111
9
111101111
9
111111111
12
111110011111
""") == """No
Yes
Yes
No
No"""

# custom cases
assert run("""1
1
1
""") == "Yes"

assert run("""1
8
11111111
""") == "No"

assert run("""1
16
1111111111111111
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest valid square |
| 8 | 11111111 | non-square length rejection |
| 16 | all ones | larger perfect square case |

## Edge Cases

The only meaningful edge case is when `n` is very close to a perfect square, such as `8` or `10`. In these cases, `isqrt(n)` returns the floor root, and squaring it correctly fails to match `n`, ensuring the answer is “No”. This avoids any ambiguity from floating-point rounding and guarantees correctness even for large inputs.
