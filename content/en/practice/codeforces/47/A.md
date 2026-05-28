---
title: "CF 47A - Triangular numbers"
description: "We are asked to determine if a given positive integer can be represented as a triangular number. Triangular numbers are formed by arranging dots into an equilateral triangle, so the _n_-th triangular number is the sum of the first _n_ positive integers."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 47
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 44 (Div. 2)"
rating: 800
weight: 47
solve_time_s: 70
verified: true
draft: false
---
[CF 47A - Triangular numbers](https://codeforces.com/problemset/problem/47/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine if a given positive integer can be represented as a triangular number. Triangular numbers are formed by arranging dots into an equilateral triangle, so the _n_-th triangular number is the sum of the first _n_ positive integers. For example, the first few triangular numbers are 1, 3, 6, 10, 15, and so on. The input is a single integer `n` between 1 and 500, and the output should be `YES` if `n` matches any triangular number, otherwise `NO`.

Since `n` is at most 500, we can reason about computational limits. Calculating each triangular number sequentially is feasible because the 32nd triangular number is already 528, slightly above our maximum bound. This tells us the problem is small enough for a straightforward iteration. A careless approach might try to invert the triangular number formula using floating-point division, which could produce off-by-one errors for small integers like 1, 3, or 6. For example, if we miscalculate the discriminant of the quadratic formula, we might incorrectly conclude that 1 is not triangular.

Edge cases include `n = 1`, `n = 500`, and numbers just below or above a triangular number, such as 5 (between 3 and 6).

## Approaches

The naive approach is to generate triangular numbers sequentially and compare each to `n`. Start with 1, then 1 + 2 = 3, then 1 + 2 + 3 = 6, and so on, until you either match `n` or exceed it. This works because triangular numbers increase monotonically, so once we surpass `n` there is no chance of finding a match.

This naive method is actually sufficient here because the maximum `n` is 500. The number of iterations in the worst case is around 32, since the triangular numbers grow roughly quadratically (`k(k+1)/2 ≤ 500`). This is far below any reasonable limit for a 2-second time constraint.

An alternative is to use the closed-form formula `k(k+1)/2 = n` and solve for `k` using the quadratic formula. This requires checking if the solution is a positive integer. While mathematically elegant, this introduces floating-point operations or careful integer checks and risks rounding issues, so for this problem the iterative approach is simpler, safer, and completely adequate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(√n) | O(1) | Accepted |
| Quadratic formula | O(1) | O(1) | Accepted, but overkill |

## Algorithm Walkthrough

1. Initialize a variable `current` to 1, representing the current triangular number, and a variable `increment` to 2. The variable `increment` tracks the next number to add to form the next triangular number.
2. Loop while `current` is less than or equal to `n`. On each iteration, check if `current` equals `n`. If it does, print `YES` and terminate the program.
3. If `current` does not equal `n`, add `increment` to `current` to get the next triangular number, and increment `increment` by 1. This simulates forming the sequence 1, 3, 6, 10, etc., without computing sums from scratch.
4. If the loop exits without finding a match, print `NO`.

The reason this works is that triangular numbers grow strictly monotonically. By iteratively constructing them, we guarantee that if `n` is triangular we will hit it exactly; if we overshoot, no triangular number equals `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

current = 1
increment = 2

while current <= n:
    if current == n:
        print("YES")
        break
    current += increment
    increment += 1
else:
    print("NO")
```

The code follows the algorithm directly. `current` starts at 1, the first triangular number, and `increment` starts at 2. The loop adds `increment` to `current` each time, generating successive triangular numbers. The `else` clause on the `while` loop triggers only if the loop exits naturally without a `break`, which ensures `NO` is printed if no match is found. This avoids off-by-one errors and unnecessary checks.

## Worked Examples

Consider `n = 1`:

| current | increment | condition current == n? |
| --- | --- | --- |
| 1 | 2 | YES |

The first triangular number matches immediately.

Consider `n = 5`:

| current | increment | condition current == n? |
| --- | --- | --- |
| 1 | 2 | NO |
| 3 | 3 | NO |
| 6 | 4 | loop ends |

The loop ends because `current` exceeds `n`. The program prints `NO`, correctly identifying that 5 is not triangular.

These traces confirm the loop invariant: `current` always equals the sum of the first `increment-1` numbers, and we check every triangular number up to `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | The largest triangular number ≤ n is roughly √(2n), so the loop runs approximately √(2n) iterations. |
| Space | O(1) | Only two integer variables are used, independent of input size. |

With `n ≤ 500`, the loop executes at most 32 times, far below the 2-second limit. Memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n = int(input())
        current = 1
        increment = 2
        while current <= n:
            if current == n:
                print("YES")
                break
            current += increment
            increment += 1
        else:
            print("NO")
    return out.getvalue().strip()

# provided samples
assert run("1\n") == "YES", "sample 1"
assert run("3\n") == "YES", "sample 2"

# custom cases
assert run("5\n") == "NO", "between triangular numbers"
assert run("6\n") == "YES", "triangular number"
assert run("500\n") == "NO", "upper bound non-triangular"
assert run("36\n") == "YES", "exact triangular number"
assert run("37\n") == "NO", "just above a triangular number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES | minimum input |
| 5 | NO | between triangular numbers |
| 500 | NO | upper bound |
| 36 | YES | typical triangular number |
| 37 | NO | off-by-one above triangular number |

## Edge Cases

For `n = 1`, the loop immediately detects `current == n` and prints `YES`. This ensures that the algorithm handles the smallest triangular number correctly. For `n = 500`, the sequence of triangular numbers exceeds 500 at `current = 528`. The loop exits naturally and prints `NO`, correctly identifying that 500 is not triangular. Cases just below or just above triangular numbers confirm the loop invariant: each triangular number is visited exactly once, and overshoot guarantees `NO` is returned without error.
