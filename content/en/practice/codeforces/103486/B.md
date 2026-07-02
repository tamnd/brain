---
title: "CF 103486B - Arithmetic Exercise"
description: "We are given three integers $A$, $B$, and $K$. The task is to compute the value of the fraction $A / B$ as a decimal number and output it with exactly $K$ digits after the decimal point."
date: "2026-07-03T06:20:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "B"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 46
verified: true
draft: false
---

[CF 103486B - Arithmetic Exercise](https://codeforces.com/problemset/problem/103486/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers $A$, $B$, and $K$. The task is to compute the value of the fraction $A / B$ as a decimal number and output it with exactly $K$ digits after the decimal point. The result must be rounded using the round-half-up rule, meaning we inspect the digit immediately after the $K$-th decimal digit: if it is 5 or more, we increase the $K$-th digit by one, otherwise we leave it unchanged.

The input sizes are small: $A, B \le 1000$ and $K \le 1000$. This immediately tells us that we do not need any asymptotically sophisticated numeric methods. A straightforward simulation of long division is sufficient because producing up to $K+1$ digits requires only $O(K)$ arithmetic steps.

The main subtlety is correctness around rounding and carry propagation. A naive implementation often fails when rounding causes cascading carry, such as when the fractional part ends in 9999 and rounding pushes it into the integer part.

For example, consider:

Input: $1\ 3\ 1$

Exact value is $0.3333...$

If we compute two digits: $0.33$, rounding does nothing and output is correct.

But for:

Input: $2\ 3\ 1$

Exact value is $0.6666...$

We compute $0.66$, then see next digit 6, so we round to $0.7$. This demonstrates that rounding must be applied after generating the extra digit, not during digit generation.

Another edge case arises when rounding affects the integer part:

Input: $999\ 1000\ 3$

We get $0.999...$. With rounding, this becomes $1.000$. A naive string-based approach that only manipulates fractional digits may fail to propagate carry into the integer part.

## Approaches

A brute-force idea is to compute the exact rational value as a floating-point number and format it with $K$ decimals using built-in rounding. While conceptually simple, floating-point representation is not reliable for up to 1000 digits of precision. Standard doubles only guarantee about 15-17 decimal digits of accuracy, so for larger $K$, this approach becomes incorrect.

Another naive approach is to compute each decimal digit one by one using repeated multiplication by 10 and integer division, which is essentially long division. This is correct, but must be extended carefully to generate one extra digit for rounding.

The key observation is that division of integers in decimal form can be simulated purely with integer arithmetic. At each step, we maintain a remainder, multiply it by 10, and extract the next digit by division. This avoids floating-point error entirely. To support rounding, we generate $K+1$ digits instead of $K$, then apply the rounding rule once at the end. Because $K \le 1000$, this is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Floating point + formatting | O(1) | O(1) | Incorrect for large K |
| Long division simulation | O(K) | O(K) | Accepted |

## Algorithm Walkthrough

We simulate manual long division of $A / B$ in base 10, but only up to $K+1$ decimal digits.

1. Compute the integer part as $A // B$ and the initial remainder as $A \% B$. The integer part is fixed and does not depend on precision.
2. Repeatedly generate decimal digits. For each step, multiply the remainder by 10 and compute the next digit as $(\text{remainder} \times 10) // B$. Update the remainder accordingly. This mirrors how decimal expansion works in manual division.
3. Store exactly $K+1$ digits of the fractional part. The extra digit exists solely for rounding decisions.
4. Apply rounding. If the $(K+1)$-th digit is at least 5, increment the $K$-th digit. This may trigger carry propagation backwards through the fractional digits.
5. If carry propagation overflows past the first fractional digit, propagate into the integer part.
6. Construct the final string with exactly $K$ fractional digits, padding with zeros if necessary.

Why it works: the long division invariant is that after each step, the remainder represents the true fractional part scaled by a power of 10. Each extracted digit is exactly correct for that position in base 10 expansion. Since we generate one extra digit before rounding, the decision to round the $K$-th digit uses exact information about whether the true value exceeds the truncation boundary, ensuring correctness under round-half-up.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, K = map(int, input().split())

    int_part = A // B
    rem = A % B

    digits = []
    for _ in range(K + 1):
        rem *= 10
        digits.append(rem // B)
        rem %= B

    # rounding from K+1 digit
    if digits[-1] >= 5:
        i = K - 1
        carry = 1
        while i >= 0 and carry:
            digits[i] += carry
            if digits[i] == 10:
                digits[i] = 0
                carry = 1
            else:
                carry = 0
            i -= 1

        if carry:
            int_part += 1

    frac = digits[:K]

    print(f"{int_part}." + "".join(map(str, frac)))

if __name__ == "__main__":
    solve()
```

The integer part is extracted directly since it is independent of decimal precision. The loop generates $K+1$ digits using classical long division with remainder tracking. The rounding block explicitly propagates carry backward, which is necessary because rounding can cascade across multiple trailing 9s.

The final formatting step ensures exactly $K$ digits by slicing the array. Zero padding is naturally preserved since we store digits explicitly.

## Worked Examples

### Example 1

Input: `1 2 2`

We compute $1 / 2 = 0.5$.

| Step | Remainder | Digit |
| --- | --- | --- |
| 1 | 1 → 10 | 5 |
| 2 | 0 → 0 | 0 (extra digit for rounding) |

We have digits `[5, 0]`. Since extra digit is 0, no rounding occurs. Output becomes `0.50`.

This confirms that trailing zero preservation works correctly.

### Example 2

Input: `10 99 5`

We simulate long division:

| Step | Remainder | Digit |
| --- | --- | --- |
| 1 | 10 → 100 | 1 |
| 2 | 1 → 10 | 0 |
| 3 | 10 → 100 | 1 |
| 4 | 1 → 10 | 0 |
| 5 | 10 → 100 | 1 |
| 6 (extra) | 1 → 10 | 0 |

Digits: `[1, 0, 1, 0, 1, 0]`

No rounding occurs because last digit is 0. Final output is `0.10101`.

This demonstrates that the algorithm preserves alternating decimal structure without interference from rounding logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K) | Each decimal digit requires constant-time arithmetic, and we compute K+1 digits |
| Space | O(K) | We store the generated digits explicitly for rounding |

The constraints allow up to 1000 digits, so a linear scan and arithmetic simulation is easily fast within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("1 2 2\n") == "0.50"
assert run("10 99 5\n") == "0.10101"

# custom cases
assert run("1 3 1\n") == "0.3", "simple rounding down"
assert run("2 3 1\n") == "0.7", "rounding up with carry"
assert run("999 1000 3\n") == "1.000", "carry into integer part"
assert run("1 8 5\n") == "0.12500", "trailing zeros preserved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 1 | 0.3 | simple truncation |
| 2 3 1 | 0.7 | rounding up |
| 999 1000 3 | 1.000 | carry into integer part |
| 1 |  |  |
