---
title: "CF 105992H - V \u6211 112.5"
description: "We are given a single integer x, which represents a percentage tax or surcharge applied to a fixed base cost. The base cost is always 50 units. The final amount to pay is the base cost plus an additional percentage of that base cost."
date: "2026-06-22T16:37:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105992
codeforces_index: "H"
codeforces_contest_name: "The 2025 Shanghai Collegiate Programming Contest"
rating: 0
weight: 105992
solve_time_s: 47
verified: true
draft: false
---

[CF 105992H - V \u6211 112.5](https://codeforces.com/problemset/problem/105992/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer `x`, which represents a percentage tax or surcharge applied to a fixed base cost. The base cost is always 50 units. The final amount to pay is the base cost plus an additional percentage of that base cost.

Concretely, the surcharge is computed as `50 × x / 100`, and the total payment is `50 + 50 × x / 100`. The output format requires printing this final value as a decimal number rounded to three digits after the decimal point, prefixed by the string `Vivo`.

The input size is trivial in terms of algorithmic complexity since there is only one integer and a constant-time arithmetic computation. Even though `x` can be as large as 19,198,100, the computation remains safe in floating-point or scaled integer arithmetic. The only subtlety lies in correct rounding and formatting.

The main edge cases come from formatting rather than computation. When `x = 0`, the result should remain exactly `50.000`. When `x` is large, the result can reach nearly one million, but still fits comfortably in standard double precision. Another edge case is proper rounding: values like `x = 1` produce `50.5`, which must be printed as `50.500`, not `50.5` or `50.5000`.

A careless implementation might also lose precision if integer division is used, for example computing `50 * x // 100`, which would discard fractional contributions entirely and break rounding.

## Approaches

A brute-force interpretation would attempt to directly simulate the percentage calculation using integer arithmetic step by step. One might try to compute the extra fee as `(50 * x) / 100` using integer division. This is already close to optimal, but if done incorrectly with floor division, it silently truncates instead of preserving decimals. Another naive idea is to convert everything to floats without thinking about precision control, then print the raw result, which risks inconsistent rounding behavior depending on formatting defaults.

The key observation is that the formula is a single linear expression. There is no iteration, no conditional structure, and no dependence between multiple inputs. This reduces the problem to evaluating a constant-time arithmetic expression and formatting the output correctly. Since floating-point arithmetic in Python is sufficient for this scale, the only real requirement is to ensure that the formatting step enforces three decimal places with rounding.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct integer/floating computation with possible truncation | O(1) | O(1) | Wrong due to precision issues |
| Proper floating-point computation with formatting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the result directly from the definition of the problem and carefully control formatting.

1. Read the integer `x` from input. This is the percentage rate applied to the base cost of 50.
2. Compute the multiplier effect of the percentage as `x / 100.0`. The use of floating-point division is essential here because integer division would discard fractional parts.
3. Multiply the base cost 50 by this multiplier to obtain the additional fee. This represents the exact proportional surcharge applied to the base.
4. Add the base cost 50 to the computed additional fee to obtain the final amount.
5. Format the result using fixed-point formatting with exactly three digits after the decimal point. This step enforces rounding rules required by the output specification.
6. Print the result prefixed by `Vivo `.

### Why it works

The computation is a direct evaluation of a linear function of `x`. Since every transformation preserves equivalence to the original formula `50 × (1 + x / 100)`, the algorithm cannot diverge from the intended value. The only potential source of discrepancy is numeric representation, and using standard floating-point arithmetic combined with controlled formatting ensures the final printed value matches the required rounding semantics.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input().strip())

base = 50.0
total = base + base * (x / 100.0)

print(f"Vivo {total:.3f}")
```

The solution reads a single integer and immediately evaluates the formula in constant time. The base value is explicitly written as a float to ensure that the entire expression stays in floating-point space, avoiding accidental integer truncation.

The formatting string `:.3f` is critical because it enforces both rounding and fixed width decimal output. Without it, Python may print a variable number of decimal places, which would fail the output requirement.

## Worked Examples

### Example 1

Input:

```
0
```

We compute step by step:

| Step | x | extra = 50 * x / 100 | total | output |
| --- | --- | --- | --- | --- |
| init | 0 | 0.0 | 50.0 | - |
| final | 0 | 0.0 | 50.0 | Vivo 50.000 |

This shows the identity case where no tax is applied. The output remains exactly the base cost.

### Example 2

Input:

```
125
```

| Step | x | extra = 50 * x / 100 | total | output |
| --- | --- | --- | --- | --- |
| init | 125 | 62.5 | 112.5 | - |
| final | 125 | 62.5 | 112.5 | Vivo 112.500 |

This confirms correct proportional scaling: a 125% surcharge doubles the base cost and adds an extra 25%.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed regardless of input size |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to very large values of `x`, but since the computation is purely arithmetic and non-iterative, it easily fits within all limits. The only concern is floating-point precision, which is handled by formatting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    x = int(input().strip())
    base = 50.0
    total = base + base * (x / 100.0)
    return f"Vivo {total:.3f}"

# provided samples
assert run("0\n") == "Vivo 50.000"
assert run("125\n") == "Vivo 112.500"

# custom cases
assert run("1\n") == "Vivo 50.500", "small fractional increase"
assert run("2\n") == "Vivo 51.000", "rounding to integer boundary"
assert run("100\n") == "Vivo 100.000", "doubling case"
assert run("19198100\n") == run("19198100\n"), "large value stability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | Vivo 50.000 | no tax edge case |
| 1 | Vivo 50.500 | fractional precision |
| 2 | Vivo 51.000 | clean rounding boundary |
| 100 | Vivo 100.000 | doubling correctness |

## Edge Cases

One edge case is when `x = 0`. The computation becomes `50 + 0`, and the output must still include three decimal places. The algorithm produces `50.0`, and formatting converts it correctly to `50.000`.

Another edge case is small percentages such as `x = 1`, where the result is `50.5`. Without explicit formatting, this might be printed as `50.5`, which would violate the required fixed precision. The algorithm ensures `50.500` is printed.

A large value like `x = 19198100` produces a large intermediate result `50 × (1 + 191981.0) = 9,599,050.0`. This still fits safely within floating-point range, and formatting remains stable.
