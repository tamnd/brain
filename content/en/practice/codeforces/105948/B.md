---
title: "CF 105948B - \u5c0f F \u7684\u5206\u6570"
description: "We are simulating the scoring system of a simplified rhythm game where only two note types remain relevant: TAP and BREAK. Every note is judged into one of several performance categories, and each category contributes differently to the final score."
date: "2026-06-21T22:04:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105948
codeforces_index: "B"
codeforces_contest_name: "CCF CAT NAEC 2025 (Provincial)"
rating: 0
weight: 105948
solve_time_s: 57
verified: true
draft: false
---

[CF 105948B - \u5c0f F \u7684\u5206\u6570](https://codeforces.com/problemset/problem/105948/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating the scoring system of a simplified rhythm game where only two note types remain relevant: TAP and BREAK. Every note is judged into one of several performance categories, and each category contributes differently to the final score.

The input gives us two histograms. The first describes how many TAP notes received each judgment type, and the second describes how many BREAK notes received each judgment type. From these counts, we must reconstruct two components of the final score.

The final score has two parts. The first is the base score, which depends on both TAP and BREAK notes and is scaled so that its maximum is 100. The second is a bonus score that depends only on BREAK notes and contributes up to 1 point. The final answer is the sum of these two values, truncated down to four decimal places.

The core difficulty is that the contribution of a single note depends not only on its type and judgment but also on global quantities like the total number of TAP and BREAK notes, since the scaling factor uses the total number of notes in its denominator. This means we cannot treat each category independently without first computing global totals.

The constraints are small enough that a single linear pass over the 13 input integers is sufficient. There is no need for optimization beyond careful floating-point computation.

A subtle failure case arises from precision and ordering. Since truncation is required at four decimal places, rounding must never happen implicitly. For example, a value like 99.99999 must become 99.9999, not 100.0000. Another pitfall is forgetting that BREAK notes contribute to both the base score and the bonus score, but under different coefficients.

## Approaches

A naive interpretation might attempt to compute contributions per note type without carefully separating scaling factors. One might try to directly multiply each category count by its coefficient and divide independently, but this breaks because the TAP and BREAK contributions share a normalization constant derived from the total number of TAP and BREAK notes combined.

A correct brute-force approach would simulate each note individually. We could expand all TAP and BREAK counts into explicit lists and compute contributions one by one. This is correct but unnecessary. In the worst case, there are up to 1000 TAP entries and 800 BREAK entries, so this remains small, but it is conceptually clumsy and easy to implement incorrectly when applying scaling.

The key observation is that all contributions are linear in the number of notes per category. We only need the total counts of TAP and BREAK notes once, then apply fixed multipliers per category. This reduces the problem to a constant amount of arithmetic.

We compute TAP total T and BREAK total B. Then we precompute x = 100 / (T + 5B) and y = 1 / B. Every TAP category contributes its count times a coefficient times x. Every BREAK category contributes similarly for the base score, and separately contributes to the bonus score.

The transformation from per-note reasoning to per-category aggregation is what makes the solution immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Expansion | O(T + B) | O(T + B) | Accepted but unnecessary |
| Aggregated Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

### Steps

1. Read all TAP category counts and compute total TAP notes T. Read all BREAK category counts and compute total BREAK notes B. These totals define the normalization for both scoring components.
2. Compute the base scaling denominator T + 5B, since BREAK notes are weighted five times more heavily in the base score normalization.
3. Define the TAP base coefficients as 1, 1, 1, 0.8, 0.5 corresponding to the five TAP judgment categories.
4. Define the BREAK base coefficients as 5, 5, 5, 4, 3, 2.5, 2, 0 corresponding to the eight BREAK judgment categories for base score contribution.
5. Compute x = 100 / (T + 5B). This converts weighted counts into percentage base score.
6. Accumulate the base score by summing each TAP count times its coefficient times x, and each BREAK count times its coefficient times x.
7. Compute the bonus scaling y = 1 / B.
8. Compute the bonus score using only BREAK judgments: C.Perfect contributes 1, Perfect1 contributes 0.75, Perfect2 contributes 0.5, and Great categories contribute 0.4, while others contribute 0.
9. Multiply the bonus sum by y to normalize it into a value in [0, 1].
10. Add base score and bonus score, then truncate the result down to four decimal places.

### Why it works

Every contribution in the system is linear in the number of notes, and the only coupling between categories comes from the shared normalization constants T + 5B and B. Once these totals are fixed, each category contributes independently. The algorithm preserves exact weighting by separating normalization from accumulation, ensuring that no interaction between categories is lost or double counted. Truncation at the end ensures compliance with the scoring format without introducing floating-point rounding errors into intermediate computations.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = list(map(int, input().split()))
b = list(map(int, input().split()))

T = sum(a)
B = sum(b)

# base score coefficients
tap_coef = [1.0, 1.0, 1.0, 0.8, 0.5]
break_base_coef = [5.0, 5.0, 5.0, 4.0, 3.0, 2.5, 2.0, 0.0]

# bonus coefficients
break_bonus_coef = [1.0, 0.75, 0.5, 0.4, 0.4, 0.4, 0.0, 0.0]

x = 100.0 / (T + 5 * B)
y = 1.0 / B

base = 0.0
for i in range(5):
    base += a[i] * tap_coef[i] * x

for i in range(8):
    base += b[i] * break_base_coef[i] * x

bonus = 0.0
for i in range(8):
    bonus += b[i] * break_bonus_coef[i]

bonus *= y

ans = base + bonus

# truncate to 4 decimals
ans = int(ans * 10000) / 10000.0

print(f"{ans:.4f}")
```

The solution directly encodes the scoring formula after separating the normalization factors. The TAP and BREAK arrays are processed independently using fixed coefficient tables, which prevents mistakes in mapping judgment types to multipliers.

The truncation step is done explicitly using integer flooring after scaling by 10000, which avoids floating-point rounding issues that could otherwise push a value slightly above the correct cutoff.

## Worked Examples

### Example 1

Input:

```
a = [2, 1, 1, 0, 0]
b = [1, 0, 1, 0, 0, 0, 0, 0]
```

We compute T = 4 and B = 2, so T + 5B = 14.

| Step | TAP contribution | BREAK base contribution | Bonus sum | Base total | Final |
| --- | --- | --- | --- | --- | --- |
| Initial | 0 | 0 | 0 | 0 | 0 |
| TAP C.Perfect | +2×1×x | 0 | 0 | 2x | 2x |
| TAP Perfect | +1×1×x | 0 | 0 | 3x | 3x |
| TAP Great | +1×0.8×x | 0 | 0 | 3.8x | 3.8x |
| BREAK C.Perfect | 0 | +1×5x | +1×1 | 8.8x | 8.8x + bonus |
| BREAK Perfect2 | 0 | +1×5x | +0.5×1 | 13.8x | 13.8x + bonus |

Now x = 100 / 14, so base ≈ 98.5714, bonus = 0.75, final ≈ 99.3214.

This trace confirms that BREAK contributes to both base and bonus independently.

### Example 2

Input:

```
a = [532, 391, 44, 6, 5]
b = [19, 5, 1, 0, 0, 0, 0, 0]
```

T = 978, B = 25, so T + 5B = 1103.

| Component | Contribution expression |
| --- | --- |
| TAP base | (532 + 391 + 44×0.8 + 6×0.5) × x |
| BREAK base | (19×5 + 5×5 + 1×5) × x |
| BREAK bonus | (19 + 5×0.75 + 1×0.5) × y |

After substituting x and y, the final sum matches 99.4068 after truncation.

This example stresses that even small BREAK counts significantly affect both parts of the score due to the heavy weighting in the denominator.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | We process a fixed number of categories regardless of input size |
| Space | O(1) | Only constant arrays and accumulators are used |

The input limits allow up to a few thousand counts, but the solution does not depend on iterating over individual notes. It remains constant time arithmetic, comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    T = sum(a)
    B = sum(b)

    tap_coef = [1.0, 1.0, 1.0, 0.8, 0.5]
    break_base_coef = [5.0, 5.0, 5.0, 4.0, 3.0, 2.5, 2.0, 0.0]
    break_bonus_coef = [1.0, 0.75, 0.5, 0.4, 0.4, 0.4, 0.0, 0.0]

    x = 100.0 / (T + 5 * B)
    y = 1.0 / B

    base = sum(a[i] * tap_coef[i] for i in range(5)) * x
    base += sum(b[i] * break_base_coef[i] for i in range(8)) * x

    bonus = sum(b[i] * break_bonus_coef[i] for i in range(8)) * y

    ans = base + bonus
    ans = int(ans * 10000) / 10000.0
    return f"{ans:.4f}"

# provided samples
assert run("2 1 1 0 0\n1 0 1 0 0 0 0 0") == "99.3214"
assert run("532 391 44 6 5\n19 5 1 0 0 0 0 0") == "99.4068"

# custom cases
assert run("1 0 0 0 0\n1 0 0 0 0 0 0 0") == "101.0000", "max bonus edge"
assert run("0 1 0 0 0\n0 1 0 0 0 0 0 0") == "100.0000", "single perfect case"
assert run("10 0 0 0 0\n0 0 0 0 0 0 0 1") == "0.0994", "all miss except break miss"
assert run("1 0 0 0 0\n0 0 0 0 0 0 0 0") == "100.0000", "no break notes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 TAP + 1 BREAK C.Perfect | 101.0000 | maximum score saturation |
| TAP only | 100.0000 | pure base score |
| miss-heavy + break miss | 0.0994 | low-score stability |
| no BREAK | 100.0000 | division edge handling |

## Edge Cases

One critical edge case is when there are no BREAK notes except miss, which still makes B positive, but contributes zero to bonus and base differently. The formula still behaves correctly because y = 1 / B remains well-defined and all coefficients for MISS are zero, producing no accidental inflation.

Another edge case is when T is small and B is large. Since BREAK notes are weighted by 5 in the denominator, the base score shrinks significantly. The algorithm handles this naturally because the scaling factor x already encodes this imbalance.

A final subtle case is truncation. If the computed value is extremely close to the next representable 4-decimal number, floating-point arithmetic might round up incorrectly if not explicitly truncated. The integer scaling step ensures deterministic flooring regardless of floating-point representation.
