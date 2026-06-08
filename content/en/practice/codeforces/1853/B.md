---
title: "CF 1853B - Fibonaccharsis"
description: "We are given two integers, n and k. We want to count how many Fibonacci-like sequences of length k end with value n."
date: "2026-06-09T05:16:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1853
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 887 (Div. 2)"
rating: 1200
weight: 1853
solve_time_s: 116
verified: true
draft: false
---

[CF 1853B - Fibonaccharsis](https://codeforces.com/problemset/problem/1853/B)

**Rating:** 1200  
**Tags:** binary search, brute force, math  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `n` and `k`. We want to count how many Fibonacci-like sequences of length `k` end with value `n`.

A Fibonacci-like sequence is built exactly like the Fibonacci sequence, except the first two values are arbitrary non-negative integers and the sequence must be non-decreasing. For every position `i > 2`,

$$f_i = f_{i-1} + f_{i-2}.$$

The last element is fixed:

$$f_k = n.$$

Our task is to count how many choices of the first two elements generate a valid sequence satisfying all requirements.

The constraints are the first clue. The number of test cases can be as large as `2 · 10^5`, and the sum of all `n` values is also at most `2 · 10^5`. A solution that performs work proportional to `n` per test case is acceptable, but anything quadratic in `n` is immediately impossible.

The unusual constraint is that `k` can be as large as `10^9`. Any algorithm that explicitly constructs a sequence of length `k` is hopeless. The solution must exploit the fact that Fibonacci numbers grow extremely quickly.

A few edge cases deserve attention.

When `k` is very large and `n` is small, there may be no solutions at all. For example:

```
n = 3, k = 9
```

The coefficients relating `f_k` to the first two elements become large long before position 9, making it impossible to represent 3 using non-negative starting values.

When `k = 3`, the recurrence gives

$$f_3 = f_1 + f_2.$$

Every pair `(f1, f2)` with sum `n` works, provided `f1 ≤ f2`. For `n = 1`, only `(0,1)` is valid, so the answer is `1`.

Another subtle case is enforcing the non-decreasing condition. A pair may satisfy the recurrence and produce `f_k = n`, yet fail because `f_1 > f_2`. For example, if a derived solution gives `(3,1)`, it must be rejected even though all later values are determined.

The key observation is that once `f_1` and `f_2` are non-negative and satisfy `f_1 ≤ f_2`, every later term is automatically non-decreasing.

## Approaches

The most direct idea is to try every possible pair `(f_1, f_2)`.

Since all terms are non-negative and the final value is `n`, both starting values are at most `n`. We could enumerate all pairs and generate the sequence until position `k`, checking whether the last value equals `n`.

This is correct but far too slow. There are `O(n²)` candidate pairs, and each may require many recurrence steps. With `n` up to `2 · 10^5`, this approach is completely infeasible.

The next observation is that every Fibonacci-like sequence is linear in its first two values.

Let

$$f_1=a,\qquad f_2=b.$$

Then:

$$f_3=a+b,$$

$$f_4=a+2b,$$

$$f_5=2a+3b,$$

and so on.

The coefficients themselves follow Fibonacci numbers. In general,

$$f_k = F_{k-2}a + F_{k-1}b,$$

where $F_1=1, F_2=1$.

The entire problem becomes counting non-negative integer solutions of

$$F_{k-2}a + F_{k-1}b = n,$$

subject to

$$a \le b.$$

This is now a linear Diophantine equation.

Another crucial observation comes from the constraint on `n`. Fibonacci numbers exceed `200000` after only a few dozen terms. Since `n ≤ 200000`, once either coefficient becomes larger than `n`, there can be at most one trivial possibility, and usually none.

In fact, only about the first 30 Fibonacci numbers matter. For larger `k`, the answer is automatically zero.

For each test case we can compute the two relevant Fibonacci coefficients and count all integer pairs `(a,b)` satisfying the equation and `a ≤ b`.

Since `n` is small, iterating over all possible `b` values is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²·k) | O(1) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Precompute Fibonacci numbers until they exceed `200000`.

Since all `n` values are at most `200000`, larger Fibonacci numbers can never participate in a valid representation.
2. For a test case `(n, k)`, determine the coefficients.

Using

$$f_k = F_{k-2}a + F_{k-1}b,$$

we need coefficients `A = F_{k-2}` and `B = F_{k-1}`.
3. If `k-1` exceeds the range of precomputed Fibonacci numbers, immediately return `0`.

At that point `B > 200000 > n`, making any non-trivial representation impossible.
4. Enumerate all possible values of `b`.

Since

$$A a + B b = n,$$

we only need to consider

$$0 \le b \le \left\lfloor \frac n B \right\rfloor .$$
5. For each candidate `b`, compute the remaining value:

$$rem = n - B b.$$

If `rem` is not divisible by `A`, no integer `a` exists.
6. Otherwise compute

$$a = \frac{rem}{A}.$$

Count the solution if and only if `a ≤ b`.
7. Output the total count.

### Why it works

Every Fibonacci-like sequence is uniquely determined by its first two elements. Expanding the recurrence shows that the `k`-th term is exactly

$$F_{k-2}a + F_{k-1}b.$$

Thus every valid sequence corresponds to one integer solution `(a,b)` of that equation.

Conversely, every non-negative integer solution with `a ≤ b` generates a valid non-decreasing Fibonacci-like sequence. The recurrence preserves non-negativity, and because

$$f_3=a+b \ge b,$$

all subsequent terms are at least as large as the previous one.

The algorithm counts precisely those pairs and nothing else, so it is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Fibonacci numbers with F1 = 1, F2 = 1
fib = [0, 1, 1]
while fib[-1] <= 200000:
    fib.append(fib[-1] + fib[-2])

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())

    if k - 1 >= len(fib):
        print(0)
        continue

    A = fib[k - 2]
    B = fib[k - 1]

    ans = 0

    for b in range(n // B + 1):
        rem = n - B * b

        if rem % A != 0:
            continue

        a = rem // A

        if a <= b:
            ans += 1

    print(ans)
```

The first section precomputes Fibonacci numbers only up to the point where they exceed the largest possible `n`. This is enough because larger coefficients can never contribute to a valid representation.

For each test case we obtain the coefficients `A = F_{k-2}` and `B = F_{k-1}`. If `k` is so large that these coefficients are beyond the precomputed range, the answer is immediately zero.

The loop over `b` checks every possible non-negative value that could appear in a solution. Once `b` is fixed, the equation determines `a` uniquely. Divisibility checks whether that value is an integer.

The condition `a <= b` is exactly the non-decreasing requirement. No additional sequence validation is necessary because the recurrence automatically produces increasing terms afterward.

Python integers are arbitrary precision, so overflow is never an issue. The largest arithmetic values are still only around `200000` anyway.

## Worked Examples

### Example 1

Input:

```
22 4
```

For `k = 4`:

$$f_4 = F_2 a + F_3 b = a + 2b.$$

So we solve:

$$a + 2b = 22.$$

| b | rem = 22 - 2b | a | a ≤ b? | Count |
| --- | --- | --- | --- | --- |
| 0 | 22 | 22 | No | 0 |
| 1 | 20 | 20 | No | 0 |
| 2 | 18 | 18 | No | 0 |
| 3 | 16 | 16 | No | 0 |
| 4 | 14 | 14 | No | 0 |
| 5 | 12 | 12 | No | 0 |
| 6 | 10 | 10 | No | 0 |
| 7 | 8 | 8 | No | 0 |
| 8 | 6 | 6 | Yes | 1 |
| 9 | 4 | 4 | Yes | 2 |
| 10 | 2 | 2 | Yes | 3 |
| 11 | 0 | 0 | Yes | 4 |

Answer: `4`.

These correspond exactly to the four sequences shown in the statement.

### Example 2

Input:

```
55 11
```

Here:

$$F_9 = 34,\qquad F_{10}=55.$$

We solve:

$$34a + 55b = 55.$$

| b | rem | divisible by 34? | a | valid? |
| --- | --- | --- | --- | --- |
| 0 | 55 | No | - | No |
| 1 | 0 | Yes | 0 | Yes |

Only one solution exists:

$$(a,b)=(0,1).$$

Answer: `1`.

This generates the classic Fibonacci sequence ending at 55.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Iterate over at most `n / F_{k-1}` values of `b`, bounded by `n` |
| Space | O(1) | Only a few variables plus a tiny Fibonacci table |

The sum of all `n` values over the entire input is at most `200000`. Since each test case performs work proportional to its own `n`, the total work across all test cases is also `O(200000)`, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    fib = [0, 1, 1]
    while fib[-1] <= 200000:
        fib.append(fib[-1] + fib[-2])

    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())

        if k - 1 >= len(fib):
            ans.append("0")
            continue

        A = fib[k - 2]
        B = fib[k - 1]

        cur = 0
        for b in range(n // B + 1):
            rem = n - B * b
            if rem % A == 0 and rem // A <= b:
                cur += 1

        ans.append(str(cur))

    sys.stdout.write("\n".join(ans))

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
assert run(
"""8
22 4
3 9
55 11
42069 6
69420 4
69 1434
1 3
1 4
"""
) == "\n".join([
    "4",
    "0",
    "1",
    "1052",
    "11571",
    "0",
    "1",
    "0"
]), "sample 1"

# minimum values
assert run(
"""1
1 3
"""
) == "1"

# no valid representation
assert run(
"""1
1 4
"""
) == "0"

# large k immediately impossible
assert run(
"""1
69 1434
"""
) == "0"

# simple hand-checkable case
assert run(
"""1
22 4
"""
) == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3` | `1` | Smallest meaningful sequence length |
| `1 4` | `0` | Enforcing `a ≤ b` correctly |
| `69 1434` | `0` | Huge `k`, coefficient growth shortcut |
| `22 4` | `4` | Multiple valid solutions |

## Edge Cases

Consider:

```
1
1 3
```

The equation is

$$a+b=1.$$

Possible non-negative pairs are `(0,1)` and `(1,0)`. Only `(0,1)` satisfies `a ≤ b`, so the answer is `1`. The algorithm checks both possibilities through the enumeration of `b` and counts exactly one.

Now consider:

```
1
1 4
```

The equation becomes

$$a+2b=1.$$

The only integer solution is `(1,0)`. Since `a>b`, the sequence starts decreasing and is invalid. The algorithm finds the solution but rejects it through the `a <= b` condition, producing `0`.

Finally consider:

```
1
69 1434
```

The Fibonacci coefficient `F_{1433}` is enormously larger than `69`. No non-negative solution can exist. The algorithm detects that `k` is beyond the precomputed Fibonacci range and immediately returns `0`, avoiding any unnecessary work.
