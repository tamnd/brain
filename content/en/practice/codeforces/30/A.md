---
title: "CF 30A - Accounting"
description: "We are given three integers, A, B, and n. The task is to find an integer value X such that:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 30
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 30 (Codeforces format)"
rating: 1400
weight: 30
solve_time_s: 83
verified: true
draft: false
---
[CF 30A - Accounting](https://codeforces.com/problemset/problem/30/A)

**Rating:** 1400  
**Tags:** brute force, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers, `A`, `B`, and `n`. The task is to find an integer value `X` such that:

$A \cdot X^n = B$

`A` represents the kingdom's income in year `0`, `B` represents the income after `n` years, and `X` is the yearly growth coefficient. Every value must stay integer, including `X`. Negative values are allowed, and `X` may also be zero.

The constraints are very small. Both `A` and `B` are at most `1000` in absolute value, and `n` is at most `10`. That changes the nature of the problem completely. We do not need advanced number theory or logarithms. Even a direct brute-force over all reasonable integer candidates easily fits within the time limit.

The tricky part is not performance, but correctness around signs and zero.

One dangerous case is when `A = 0`.

For example:

```
0 0 5
```

The equation becomes:

$0 \cdot X^5 = 0$

Every integer `X` satisfies it. The problem allows printing any valid answer, so outputting `0` is fine.

But with:

```
0 10 3
```

we get:

$0 \cdot X^3 = 10$

No integer can satisfy this, because the left side is always `0`.

Another subtle case appears with negative answers and even powers.

Consider:

```
1 -8 2
```

We need:

$X^2 = -8$

An even power can never become negative, so the answer is `"No solution"`.

But with:

```
1 -8 3
```

we need:

$X^3 = -8$

Now `X = -2` works because odd powers preserve sign.

A careless implementation using floating-point roots can also fail. Computing something like `pow(64, 1/3)` may produce `3.999999999` instead of `4`, leading to rounding mistakes. Since the constraints are tiny, integer brute-force avoids all precision problems.

## Approaches

The most direct idea is to try every possible integer `X`, compute `A * X^n`, and check whether it equals `B`.

Why does this work? Because the search space is tiny. If `|B| ≤ 1000`, then any valid integer root must also stay reasonably small. For example, if `|X| ≥ 100`, then even `X²` already becomes at least `10000`, far outside the allowed range unless `A = 0`.

Trying every integer from `-1000` to `1000` gives only `2001` candidates. For each candidate we compute a power up to exponent `10`. That is only a few tens of thousands of arithmetic operations, essentially instantaneous.

A more mathematical approach would isolate:

$X^n = \frac{B}{A}$

and then attempt to compute an integer `n`-th root. The problem is that handling signs, divisibility, and floating-point precision becomes more annoying than the original problem itself. Because the constraints are so small, brute-force is actually the cleanest and safest solution.

The brute-force works because every valid answer must lie inside a very small range. Once we realize that, the problem reduces to a simple search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all integers | O(2000 × n) | O(1) | Accepted |
| Integer root math approach | O(n) | O(1) | Accepted but unnecessarily error-prone |

## Algorithm Walkthrough

1. Read integers `A`, `B`, and `n`.
2. Iterate through all integers `x` from `-1000` to `1000`.

This range is safely large enough because `|B| ≤ 1000`. Any larger magnitude would make `x^n` far exceed the target unless special zero cases occur.
3. For each candidate, compute:

$A \cdot x^n$

and compare it with `B`.
4. If equality holds, print `x` immediately and terminate.

The problem allows any valid solution, so the first one is enough.
5. If the loop finishes without finding a valid integer, print `"No solution"`.

### Why it works

The algorithm checks every integer candidate that could possibly satisfy the equation. If a solution exists, it must appear somewhere in the tested range, so the algorithm will eventually find it. If no candidate satisfies the equation, then no integer solution exists.

The correctness comes directly from exhaustive search over all feasible integer values.

## Python Solution

```python
import sys
input = sys.stdin.readline

A, B, n = map(int, input().split())

for x in range(-1000, 1001):
    if A * (x ** n) == B:
        print(x)
        break
else:
    print("No solution")
```

The loop tries every integer candidate in the allowed range. Python's integer arithmetic handles negative powers correctly when the exponent is integer and non-negative, so `(-2) ** 3` becomes `-8` and `(-2) ** 2` becomes `4` automatically.

The `for-else` structure is useful here. The `else` block executes only if the loop never hits a `break`, meaning no valid solution was found.

The range `[-1000, 1000]` is intentionally simple. We could derive tighter bounds mathematically, but there is no benefit. The current search size is already tiny.

Using integer arithmetic everywhere avoids floating-point precision issues entirely.

## Worked Examples

### Example 1

Input:

```
2 18 2
```

We need:

$2 \cdot X^2 = 18$

| x | x² | 2 × x² | Matches B? |
| --- | --- | --- | --- |
| -3 | 9 | 18 | Yes |
| -2 | 4 | 8 | No |
| -1 | 1 | 2 | No |
| 0 | 0 | 0 | No |
| 1 | 1 | 2 | No |
| 2 | 4 | 8 | No |
| 3 | 9 | 18 | Yes |

The algorithm stops at the first valid answer it encounters. Since iteration starts from negative numbers, it actually prints `-3`. That is completely valid because both `3²` and `(-3)²` equal `9`.

This example demonstrates that the problem accepts any valid solution.

### Example 2

Input:

```
1 -8 2
```

We need:

$X^2 = -8$

| x | x² | Matches -8? |
| --- | --- | --- |
| -3 | 9 | No |
| -2 | 4 | No |
| -1 | 1 | No |
| 0 | 0 | No |
| 1 | 1 | No |
| 2 | 4 | No |
| 3 | 9 | No |

Every square is non-negative, so the loop never finds a match.

Output:

```
No solution
```

This example shows why sign handling matters when `n` is even.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2000 × n) | At most 2001 candidates, each requiring exponentiation up to power `n` |
| Space | O(1) | Only a few integer variables are stored |

With `n ≤ 10` and only `2001` tested values, the program performs very little work. The running time is far below the limit, and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    A, B, n = map(int, input().split())

    for x in range(-1000, 1001):
        if A * (x ** n) == B:
            print(x)
            break
    else:
        print("No solution")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("2 18 2\n") in ["3", "-3"], "sample 1"

# minimum values
assert run("0 0 1\n") == "-1000", "any integer works"

# impossible because A is zero
assert run("0 5 3\n") == "No solution", "zero times anything stays zero"

# negative root with odd exponent
assert run("1 -27 3\n") == "-3", "odd powers preserve sign"

# impossible with even exponent
assert run("1 -16 2\n") == "No solution", "even powers cannot be negative"

# maximum boundary style case
assert run("1 1000 1\n") == "1000", "largest positive root"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 1` | Any integer | Infinite valid solutions |
| `0 5 3` | `No solution` | Zero coefficient impossibility |
| `1 -27 3` | `-3` | Negative roots with odd powers |
| `1 -16 2` | `No solution` | Even powers cannot produce negatives |
| `1 1000 1` | `1000` | Large boundary answer |

## Edge Cases

Consider the input:

```
0 0 5
```

The algorithm starts checking from `x = -1000`.

We compute:

$0 \cdot (-1000)^5 = 0$

This already matches `B = 0`, so the algorithm immediately prints `-1000`.

That may look strange, but it is completely correct. Every integer satisfies the equation here, and the statement allows any valid answer.

Now consider:

```
0 10 3
```

For every candidate `x`, the left side becomes:

$0 \cdot x^3 = 0$

Since `0` never equals `10`, the loop finishes without success and prints `"No solution"`.

Another important edge case is:

```
1 -16 2
```

The algorithm tests all integers from `-1000` to `1000`.

For negative candidates:

$(-x)^2 > 0$

For positive candidates:

$x^2 > 0$

Squares are always non-negative, so the target `-16` can never appear. The exhaustive search correctly reports `"No solution"`.

Finally, consider:

```
2 18 2
```

Both `x = 3` and `x = -3` satisfy the equation because:

$3^2 = (-3)^2 = 9$

The algorithm returns the first valid value it encounters, which is `-3`. The problem explicitly allows any valid solution, so this behavior is correct.
