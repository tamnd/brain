---
title: "CF 102439F - Prime or number"
description: "We are given one non-negative integer n, with 1 <= n <= 10^18. Instead of ordinary multiplication, we are asked to use bitwise OR as the operation that combines two numbers."
date: "2026-08-12T08:12:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "F"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 66
verified: true
draft: false
---

[CF 102439F - Prime or number](https://codeforces.com/problemset/problem/102439/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one non-negative integer `n`, with `1 <= n <= 10^18`. Instead of ordinary multiplication, we are asked to use bitwise OR as the operation that combines two numbers.

The number `n` is considered prime under this operation when `n > 1` and there do not exist integers `x` and `y` satisfying `1 < x <= y < n` and

```
x OR y = n
```

The task is to print `Yes` when `n` has this special prime property and `No` otherwise.

The upper bound of `10^18` immediately rules out anything that iterates through all possible values up to `n`. Even an `O(n)` solution would require up to `10^18` iterations, far beyond the one-second limit. A brute-force search over pairs is roughly quadratic, around `5 * 10^35` pairs in the worst case. The useful structure has to come from the binary representation of `n`, which contains only about 60 bits.

There are three edge cases that deserve attention. First, `n = 1` must produce `No`, because the definition requires a prime candidate to be greater than `1`; there is no valid prime under this definition at `1`. Second, a power of two such as `8` produces `Yes`. A careless implementation might look for an ordinary divisor and conclude something based on conventional primality, but ordinary multiplication has nothing to do with the operation here. Finally, a number with exactly two set bits, such as `6 = 110₂`, produces `No`: we can choose `x = 2` and `y = 4`, and `2 OR 4 = 6`, with both operands strictly between `1` and `6`.

The crucial distinction is thus not whether `n` is an ordinary prime. It is how many `1` bits occur in its binary representation.

## Approaches

The direct approach follows the definition literally. We could enumerate every `x` from `2` through `n - 1`, every `y` from `x` through `n - 1`, and check whether `x OR y` equals `n`. If such a pair exists, the answer is `No`; if every pair fails, the answer is `Yes`. This is correct because it examines exactly the pairs forbidden by the definition.

The problem is the size of the search space. For a value close to `10^18`, there are approximately

```
(n - 2)(n - 1) / 2
```

candidate pairs. At `n = 10^18`, this is approximately `5 * 10^35` pairs, which is completely infeasible.

The observation that unlocks the problem comes directly from the behavior of bitwise OR. Every `1` bit of `x` or `y` must also be a `1` bit of `n` when `x OR y = n`. Conversely, every `1` bit of `n` must occur in at least one of `x` or `y`.

Suppose `n` has at least two set bits. Pick one set bit and put it into `x`, while putting all the remaining set bits into `y`. Both numbers are proper submasks of `n`, so both are strictly smaller than `n`, and their OR is exactly `n`.

For example,

```
n = 10 = 1010₂

x = 2  = 0010₂
y = 8  = 1000₂

x OR y = 1010₂ = 10
```

Both operands are greater than `1`, so `10` is not prime under the OR operation.

The only exception is when `n` has exactly one set bit. Then `n` is a power of two. Every positive number whose bits are contained in `n` is either `0` or `n` itself. There is no valid operand strictly between `1` and `n`, so no pair can satisfy the definition. Thus every power of two greater than `1` is prime under OR.

We have reduced the entire problem to checking whether `n` is a power of two, with the additional requirement that `n > 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and first check whether `n <= 1`. Such a value cannot satisfy the definition of a prime candidate, so print `No`.
2. Check whether `n` has exactly one set bit. The standard bitwise test for this is

```
n & (n - 1) == 0
```

For a positive integer with exactly one `1` bit, subtracting one changes that bit to `0` and changes every lower bit to `1`. Their AND is consequently zero. If there are at least two set bits, the AND remains nonzero.

1. Print `Yes` if the test succeeds and `No` otherwise. A successful test means that `n` is a power of two greater than `1`, which is exactly the set of OR-prime numbers.

### Why it works

The invariant is that every valid decomposition `x OR y = n` must distribute the set bits of `n` between the two operands. If `n` has at least two set bits, one can always construct such a decomposition by putting one set bit into `x` and all other set bits into `y`. Both operands are greater than `1` and smaller than `n`, so `n` is composite under OR.

If `n` has exactly one set bit, every submask of `n` is either `0` or `n`. There is no integer strictly between `1` and `n` that can be used as either operand, so no forbidden decomposition exists. Hence, among values greater than `1`, the OR-prime numbers are exactly the powers of two.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n > 1 and (n & (n - 1)) == 0:
        print("Yes")
    else:
        print("No")

solve()
```

The first condition, `n > 1`, handles the boundary required by the definition. Without it, `n = 1` would incorrectly pass the power-of-two test because `1 & 0` is zero.

The second condition checks whether exactly one bit is set. Python integers have arbitrary precision, so there is no overflow concern even though the input can be as large as `10^18`.

The expression uses `n - 1` before the AND operation. For example, `8` is `1000₂`, while `7` is `0111₂`, so `8 & 7` is zero. For `10 = 1010₂`, `9 = 1001₂`, and `10 & 9 = 1000₂`, which is nonzero.

No iteration over the value of `n` is needed. The entire decision consists of a constant number of integer operations.

## Worked Examples

Since the statement formatting provided here omits the numeric values from the displayed sample inputs, we can trace representative values corresponding to the two sample outcomes.

For `n = 8`, the number is `1000₂`.

| `n` | `n > 1` | `n - 1` | `n & (n - 1)` | Output |
| --- | --- | --- | --- | --- |
| 8 | true | 7 (`0111₂`) | 0 | Yes |

The zero result confirms that `8` has exactly one set bit. There is no valid operand strictly between `1` and `8` whose bits are contained in `8`, so `8` cannot be represented as the OR of two allowed smaller operands.

For `n = 6`, the binary representation is `110₂`.

| `n` | `n > 1` | `n - 1` | `n & (n - 1)` | Output |
| --- | --- | --- | --- | --- |
| 6 | true | 5 (`101₂`) | 4 (`100₂`) | No |

The nonzero result means that `6` has more than one set bit. Indeed, `2 OR 4 = 6`, and both `2` and `4` satisfy `1 < x <= y < 6`. The required decomposition exists, so `6` is not prime under OR.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | The bitwise operations work on the approximately `log₂ n` bits of `n`. |
| Space | O(1) | Only a constant number of integer variables are stored. |

With `n <= 10^18`, the binary representation has at most 60 bits. The solution therefore performs only a constant amount of work on a very small integer representation, easily fitting the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())

    if n > 1 and (n & (n - 1)) == 0:
        print("Yes")
    else:
        print("No")

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if False else ""
    finally:
        sys.stdin = old_stdin
        input = old_input
```

For a directly executable assert-based test harness, it is cleaner to capture standard output explicitly:

```python
import sys
import io

def solve():
    n = int(input())

    if n > 1 and (n & (n - 1)) == 0:
        print("Yes")
    else:
        print("No")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Representative sample 1
assert run("8\n") == "Yes\n", "power of two"

# Representative sample 2
assert run("6\n") == "No\n", "two set bits"

# Minimum-size input
assert run("1\n") == "No\n", "1 is not greater than 1"

# Smallest valid OR-prime
assert run("2\n") == "Yes\n", "2 is a power of two"

# Maximum input
assert run("1000000000000000000\n") == "No\n", "maximum bound"

# Power of two near the maximum
assert run("576460752303423488\n") == "Yes\n", "2^59"

# Boundary between one and two set bits
assert run("3\n") == "No\n", "1 OR 2 = 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `No` | Minimum input and the `n > 1` boundary |
| `2` | `Yes` | Smallest valid OR-prime |
| `3` | `No` | Smallest number with two set bits |
| `576460752303423488` | `Yes` | Large power of two, testing the upper range |
| `1000000000000000000` | `No` | Maximum allowed input |
| `6` | `No` | Explicit decomposition into `2 OR 4` |

The first harness shown above illustrates the intended `run` structure but does not capture output, so the second harness is the one to use when actually running the assertions. The competitive-programming submission itself only needs the much shorter solution from the previous section.

## Edge Cases

For `n = 1`, the input is `1`, and the algorithm first evaluates `n > 1`, which is false. It immediately prints `No`. This prevents the expression `n & (n - 1)` from incorrectly classifying `1` as a valid prime under OR simply because `1` has one set bit.

For `n = 2`, the binary representation is `10₂`. The expression `2 & 1` equals zero, and `2 > 1`, so the algorithm prints `Yes`. There is no integer `x` with `1 < x < 2`, which makes a decomposition impossible.

For `n = 6`, the binary representation is `110₂`. The expression `6 & 5` gives `4`, so the number has multiple set bits and the algorithm prints `No`. The actual witness is `x = 2`, `y = 4`, since `2 OR 4 = 6`.

For a large power of two such as `576460752303423488 = 2^59`, exactly one bit is set. Subtracting one produces a number with the lower 59 bits set, so their AND is zero. The algorithm prints `Yes`, demonstrating that the method does not depend on small values.

For `n = 10^18`, the binary representation contains multiple set bits, so `n & (n - 1)` is nonzero and the answer is `No`. This case also demonstrates why an approach based on enumerating possible operands cannot work: even a linear scan would require an infeasible number of operations, while the bitwise characterization handles the value immediately.
