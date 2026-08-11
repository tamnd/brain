---
title: "CF 102397B - Calculate The Area"
description: "We need to reconstruct the dimensions of a rectangular piece of land from its area. The input contains a single integer n, representing the rectangle's area. We need to print two positive integers height and width whose product is exactly n."
date: "2026-08-11T15:47:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "B"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 95
verified: true
draft: false
---

[CF 102397B - Calculate The Area](https://codeforces.com/problemset/problem/102397/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to reconstruct the dimensions of a rectangular piece of land from its area. The input contains a single integer `n`, representing the rectangle's area. We need to print two positive integers `height` and `width` whose product is exactly `n`.

For example, if `n = 20`, both `4 5` and `2 10` describe valid rectangles because their products are 20. The problem explicitly allows any valid pair, so there is no requirement to find a unique rectangle or to optimize the dimensions.

The constraint `1 <= n <= 200` makes the problem extremely small. Even an algorithm that checks every integer from 1 through `n` performs at most 200 iterations, which is easily fast enough for a 1.5 second limit. Still, the mathematical structure gives us a cleaner `O(sqrt(n))` approach. This matters conceptually because factor-pair problems often have much larger limits, where checking every value up to `n` would become too expensive.

The main edge cases come from perfect squares and the smallest possible area. For `n = 1`, the only possible dimensions are `1 1`. A careless implementation that starts checking from 2 would never find a factor and could fail to print anything.

For a perfect square such as `n = 16`, the dimensions `4 4` are valid because the same factor can be used twice. An implementation that incorrectly searches only for two different factors could reject this case even though equal dimensions are perfectly valid.

For a prime area such as `n = 7`, there is no factor between 2 and `sqrt(7)`. The valid rectangle is simply `1 7`. An implementation that assumes every number has a non-trivial factor could fail here.

The sample formatting in the supplied statement omits the corresponding input lines, but the displayed output pairs clearly correspond to areas `20`, `16`, and `6`: `4 * 5 = 20`, `4 * 4 = 16`, and `2 * 3 = 6`.

## Approaches

The most direct approach is brute force. Try every possible height from 1 through `n`, and whenever `n` is divisible by that height, use `n / height` as the width. The first successful divisor immediately gives a valid pair because `height * (n / height) = n`. In the worst case, this performs `n` divisibility checks. With the actual constraint `n <= 200`, that means at most 200 checks, so brute force is fully accepted here. It would become too slow only if the constraint were increased dramatically, for example to values around `10^9` or larger, where performing up to `n` iterations is no longer realistic.

The useful observation is that factors come in pairs. If `a * b = n` and `a <= b`, then `a <= sqrt(n)`. Consequently, if we search downward from `floor(sqrt(n))`, the first value that divides `n` gives a factor pair immediately. There is no reason to inspect anything larger than `sqrt(n)`, because its matching factor would already be smaller than or equal to `sqrt(n)`.

This reduces the search from at most `n` checks to at most `sqrt(n)` checks. For this problem either method is fast enough, but the square-root approach captures the standard reasoning behind factor-pair problems and scales much better.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted for `n <= 200` |
| Search from `sqrt(n)` | O(sqrt(n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the area `n`. We need to find any positive divisor of `n` and use its complementary factor as the other dimension.
2. Compute `floor(sqrt(n))`. A factor pair can always be arranged so that the smaller factor is at most `sqrt(n)`, so searching beyond this boundary is unnecessary.
3. Start at `floor(sqrt(n))` and move downward to 1. Searching downward is convenient because it finds the factor pair with the largest possible smaller dimension, although the problem does not require this particular pair.
4. For each candidate `h`, check whether `n % h == 0`. If the remainder is zero, `h` divides the area exactly, so `n // h` is an integer and the pair `h, n // h` forms a valid rectangle.
5. Print `h` and `n // h` and stop. A divisor is guaranteed to be found because 1 divides every positive integer.

### Why it works

The invariant is that every candidate considered by the loop is at most `sqrt(n)`. For every valid factorization `n = a * b`, at least one of `a` and `b` is at most `sqrt(n)`. Since the loop checks every integer from `floor(sqrt(n))` down to 1, it must eventually encounter such a factor. When it does, the complementary value `n // a` satisfies `a * (n // a) = n`, so the printed dimensions always have exactly the required area.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

h = int(n ** 0.5)

while h >= 1:
    if n % h == 0:
        print(h, n // h)
        break
    h -= 1
```

The first line reads the single area value. There is only one test case, so no outer test-case loop is needed.

The expression `int(n ** 0.5)` gives the integer part of the square root for these very small constraints. We then inspect possible smaller dimensions from that value down to 1.

The divisibility test is the central operation. If `n % h` is zero, integer division gives the exact complementary dimension. We print immediately because any valid pair is accepted.

The loop condition uses `h >= 1` rather than `h > 1` because 1 is the fallback factor for every positive `n`. This handles both prime numbers and `n = 1` without special cases.

There is no integer overflow concern in Python, and the division is performed only after divisibility has been confirmed.

## Worked Examples

### Sample 1

For the first displayed sample, the area is `20`, and the expected displayed dimensions are `4 5`.

| `n` | `h` | `n % h` | Action |
| --- | --- | --- | --- |
| 20 | 4 | 0 | Print `4 5` |

The square root of 20 is approximately 4.47, so the loop starts at 4. Since 20 is divisible by 4, the algorithm immediately obtains the complementary factor 5. The invariant is satisfied because `4 * 5 = 20`.

### Sample 2

For the second displayed sample, the area is `16`, and the expected dimensions are `4 4`.

| `n` | `h` | `n % h` | Action |
| --- | --- | --- | --- |
| 16 | 4 | 0 | Print `4 4` |

Here `sqrt(16) = 4`, so the loop starts exactly at the square root. The square-root factor divides the number, producing two equal dimensions. This demonstrates why perfect squares need no special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n)) | At most `floor(sqrt(n))` divisibility checks are performed. |
| Space | O(1) | Only the area and one candidate factor are stored. |

With `n <= 200`, the loop performs fewer than 15 checks because `sqrt(200)` is about 14.14. The solution therefore has an enormous margin under the 1.5 second time limit and uses constant memory.

## Test Cases

Because the problem accepts any valid factor pair, the test helper below validates the mathematical property of the output rather than requiring one particular pair. The assertions for the samples accept the exact dimensions shown in the statement while also checking that the returned dimensions multiply to the requested area.

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    h = int(n ** 0.5)

    while h >= 1:
        if n % h == 0:
            print(h, n // h)
            break
        h -= 1

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

def check(inp: str, expected_area: int):
    out = run(inp)
    a, b = map(int, out.split())
    assert a * b == expected_area, (
        f"Invalid rectangle for area {expected_area}: {a} {b}"
    )
    assert a >= 1 and b >= 1

# Provided samples, whose input lines are omitted in the supplied statement.
assert run("20\n") == "4 5", "sample 1"
assert run("16\n") == "4 4", "sample 2"
assert run("6\n") == "2 3", "sample 3"

# Minimum-size input.
assert run("1\n") == "1 1", "minimum area"

# Maximum-size input.
check("200\n", 200)

# Another perfect square.
assert run("25\n") == "5 5", "perfect square"

# Prime number, where only 1 and n are factors.
check("197\n", 197)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1 1` | Minimum area and loop boundary at 1 |
| `200` | `10 20` | Maximum constraint and a non-square composite |
| `25` | `5 5` | Perfect-square handling |
| `197` | `1 197` | Prime input and fallback to factor 1 |

## Edge Cases

For `n = 1`, `floor(sqrt(1))` is 1. The first divisibility check is `1 % 1 == 0`, so the algorithm prints `1 1`. No separate special case is needed, and the lower loop boundary is handled correctly.

For the perfect square `n = 16`, the loop starts at 4. Since `16 % 4 == 0`, it prints `4 4`. Equal dimensions are allowed because a rectangle does not require its height and width to differ.

For the prime input `n = 7`, `floor(sqrt(7))` is 2. The algorithm checks `7 % 2`, which is nonzero, then reaches 1. Since `7 % 1 == 0`, it prints `1 7`. This works because every positive integer has 1 as a divisor.

For the maximum input `n = 200`, the loop starts at 14 and checks downward. The first divisor encountered is 10, because `200 % 10 == 0`. The complementary dimension is `200 // 10 = 20`, so the output is `10 20`. Their product is exactly 200, satisfying the required rectangle area.
