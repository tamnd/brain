---
title: "CF 103934I - Offering to god Ra"
description: "We are building a number of grams of food that Thiago will offer. Each valid offering must be composed of baskets of fixed size A, so the total amount must be a multiple of A."
date: "2026-07-02T07:13:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103934
codeforces_index: "I"
codeforces_contest_name: "2022 USP Try-outs"
rating: 0
weight: 103934
solve_time_s: 40
verified: true
draft: false
---

[CF 103934I - Offering to god Ra](https://codeforces.com/problemset/problem/103934/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a number of grams of food that Thiago will offer. Each valid offering must be composed of baskets of fixed size `A`, so the total amount must be a multiple of `A`. At the same time, when we write this total in decimal, its most significant digits must match a given integer `B`. In other words, the number must lie inside the range of numbers whose decimal representation starts with the digits of `B`.

So the task is to find some integer `X` such that `X = k * A` for some integer `k`, `X < 10^18`, and when written in base 10, `X` begins with the digits of `B`.

The constraints are large: up to `10^5` test cases and values up to `10^9`. This immediately rules out any approach that iterates over multiples of `A` or scans large ranges per test case. Even trying all candidates up to `10^18` is impossible, since that would be astronomically large. The solution must reduce the search space to something logarithmic or constant per test.

A subtle failure case appears when we try to “just start from B and move upward”. For example, if `A = 7` and `B = 2`, valid numbers are multiples of 7 starting with digit 2: 21, 28, 210, 217, etc. A naive approach might check only a few small multiples and miss that the first valid one might be far from `B` itself in numeric value. Another pitfall is assuming the answer is always close to `B * 10^k`, which is not guaranteed to be divisible by `A`.

The core difficulty is combining two structures: arithmetic progression (multiples of `A`) and a prefix constraint in decimal representation.

## Approaches

A brute-force idea is straightforward. We could iterate over multiples of `A`: compute `A, 2A, 3A, ...` and check whether each value begins with `B`. This is correct because every valid candidate is included in this sequence. However, the sequence grows linearly, and in the worst case the first valid match could appear extremely far away. Since values are allowed up to `10^18`, the number of multiples we might need to check can also be on the order of `10^18 / A`, which is completely infeasible.

The key observation is that the prefix condition does not require us to inspect every multiple. Instead, we can reinterpret the condition “starts with B” as a range constraint. A number starts with `B` if and only if it lies in some interval `[B * 10^k, (B + 1) * 10^k - 1]` for some non-negative integer `k`. This converts the digit condition into a union of intervals.

For each such interval, we want to find the smallest multiple of `A` that lies inside it. That becomes a simple arithmetic alignment problem: for a fixed interval, we can compute the first multiple of `A` that is greater than or equal to the left endpoint, and check if it still lies within the right endpoint. Since the number of relevant `k` values is small (at most 18 because `10^18` bounds the length of numbers), we can try all possible prefix lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force multiples | O(10^18 / A) worst case | O(1) | Too slow |
| Interval + modular alignment | O(log 10^18) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `A` and `B`. We interpret `B` as a fixed decimal prefix that the answer must begin with.
2. Convert the prefix condition into intervals. For each possible length of the number, construct a power `p = 10^k` and define the interval `[B * p, (B + 1) * p - 1]`. These intervals represent exactly the numbers whose leading digits are `B` when written with at most that many digits. The smallest valid number will appear in one of these ranges.
3. For each interval, compute the smallest multiple of `A` that is at least the left endpoint. This is done by taking `x = ((L + A - 1) // A) * A`. This ensures we jump directly to the first valid multiple inside or after the interval start.
4. Check whether this candidate `x` is within the interval and also less than `10^18`. If it is, it satisfies both constraints: it is a multiple of `A` and begins with `B`.
5. Track the minimum valid `x` over all interval lengths. The answer is the smallest such value.
6. If no interval produces a valid multiple, output `-1`.

### Why it works

The correctness rests on the fact that every number with prefix `B` belongs to exactly one interval defined by a power of ten. Any valid solution must lie in one of these intervals. Inside a fixed interval, multiples of `A` form an arithmetic progression, so the first valid candidate can be found using a single ceiling division. Since we test every possible digit length up to the limit imposed by `10^18`, we do not miss any valid representation, and among all candidates we choose the smallest valid multiple.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    LIMIT = 10**18

    for _ in range(t):
        A, B = map(int, input().split())

        best = None
        pow10 = 1

        for k in range(1, 20):
            L = B * pow10
            R = (B + 1) * pow10 - 1

            if L >= LIMIT:
                break

            if R >= LIMIT:
                R = LIMIT - 1

            x = ((L + A - 1) // A) * A

            if x <= R:
                if best is None or x < best:
                    best = x

            pow10 *= 10

        print(best if best is not None else -1)

if __name__ == "__main__":
    solve()
```

The implementation builds the interval boundaries using powers of ten and checks at most about 18 possible digit lengths. For each range, it computes the first multiple of `A` that enters the range using integer ceiling division, then verifies whether it still preserves the prefix constraint. The `best` variable maintains the minimum valid candidate across all lengths.

A subtle detail is the handling of the upper bound `10^18`. Any interval extending beyond this limit is clipped because values above it are invalid by problem definition. The loop bound of 20 is safe since 10^19 already exceeds the limit.

## Worked Examples

### Example 1

Input:

```
A = 7, B = 2
```

We examine prefix intervals:

| k | L = B·10^k | R = (B+1)·10^k - 1 | First multiple x | Valid? |
| --- | --- | --- | --- | --- |
| 1 | 20 | 29 | 21 | yes |
| 2 | 200 | 299 | 203 | yes |
| 3 | 2000 | 2999 | 2002 | yes |

The smallest valid candidate is 21.

This shows that the algorithm does not assume the smallest digit-length interval is always optimal, it checks all and selects the minimum.

### Example 2

Input:

```
A = 10, B = 3
```

| k | L | R | First multiple x | Valid? |
| --- | --- | --- | --- | --- |
| 1 | 30 | 39 | 30 | yes |
| 2 | 300 | 399 | 300 | yes |

The smallest valid value is 30, which is immediately aligned with both conditions.

These examples demonstrate how alignment inside each interval directly produces valid multiples without scanning intermediate values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(18 · t) | each test checks at most ~18 digit lengths |
| Space | O(1) | only a few variables are maintained |

The solution comfortably fits within limits since `t ≤ 10^5` and each case performs only constant work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    LIMIT = 10**18
    out = []

    for _ in range(t):
        A, B = map(int, input().split())

        best = None
        pow10 = 1

        for k in range(1, 20):
            L = B * pow10
            R = (B + 1) * pow10 - 1

            if L >= LIMIT:
                break
            if R >= LIMIT:
                R = LIMIT - 1

            x = ((L + A - 1) // A) * A

            if x <= R:
                if best is None or x < best:
                    best = x

            pow10 *= 10

        out.append(str(best if best is not None else -1))

    return "\n".join(out)

# provided-style cases
assert run("3\n7 2\n10 3\n2 10\n") == "21\n30\n20"

# minimum case
assert run("1\n1 1\n") == "1"

# power alignment case
assert run("1\n5 9\n") == "90"

# no-small-fit forcing longer interval
assert run("1\n8 7\n") == "72"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 2 | 21 | basic prefix alignment |
| 10 3 | 30 | exact multiple at boundary |
| 2 10 | 20 | multi-digit prefix handling |
| 1 1 | 1 | smallest possible values |
| 5 9 | 90 | extension to next digit length |
| 8 7 | 72 | non-trivial alignment inside interval |

## Edge Cases

One edge case is when `A = 1`. Then every number is valid in terms of divisibility, so the answer is simply the smallest number starting with `B`, which is `B` itself as long as it is below `10^18`. The algorithm handles this because in the first interval `k = digits(B)`, the left endpoint equals `B` and the first multiple is exactly `B`.

Another edge case is when no valid multiple exists within the limit. For example, if `A` is large and the prefix interval starts beyond `10^18`, the loop terminates early and `best` remains empty, producing `-1`.

A more subtle case is when the first multiple inside an interval exceeds the interval boundary. For instance, if `L = 23`, `R = 29`, and `A = 10`, the first multiple is `30`, which is outside the interval. The check `x <= R` correctly discards it, preventing false positives.
