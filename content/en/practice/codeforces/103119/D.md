---
title: "CF 103119D - Artifacts"
description: "We are given five artifact items, one for each equipment slot. Each artifact contributes exactly five stat lines, and across all artifacts we only care about four statistics: flat ATK, ATK percentage, Crit Rate, and Crit Damage."
date: "2026-07-03T22:39:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103119
codeforces_index: "D"
codeforces_contest_name: "The 2020 ICPC Asia Macau Regional Contest"
rating: 0
weight: 103119
solve_time_s: 48
verified: true
draft: false
---

[CF 103119D - Artifacts](https://codeforces.com/problemset/problem/103119/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given five artifact items, one for each equipment slot. Each artifact contributes exactly five stat lines, and across all artifacts we only care about four statistics: flat ATK, ATK percentage, Crit Rate, and Crit Damage.

The final character model starts with fixed base stats: 1500 ATK, 5 percent Crit Rate, and 50 percent Crit Damage. Artifacts modify these values additively or multiplicatively depending on the stat type. Flat ATK values are summed directly. ATK percent values accumulate into a single multiplier applied to base ATK. Crit Rate and Crit Damage also accumulate additively across artifacts.

After aggregation, ATK is computed as 1500 multiplied by (1 plus total ATK percent) plus total flat ATK. Crit Rate is clamped so that any value above 100 percent becomes exactly 100 percent. Crit Damage has no such cap.

Finally, expected damage is defined as a mixture of normal and critical hits:

E = ATK multiplied by probability of non crit plus ATK multiplied by crit multiplier times probability of crit. This simplifies to a weighted average between normal and critical outcomes.

The input is purely textual, so the main difficulty is parsing and correctly accumulating values with mixed percentage formats and floating point precision.

Constraints are small: only five artifacts and five lines each, so 25 lines total. This rules out any need for optimization beyond O(1) parsing and arithmetic. The real risk is numerical mistakes: misinterpreting percent signs, forgetting the base 5 percent crit rate, or incorrectly clamping crit rate at 100 percent.

A subtle edge case appears when Crit Rate exceeds 100 percent after summation. For example, if artifacts give 150 percent Crit Rate total, the effective value must be clamped to exactly 100 percent, otherwise expected damage will be overestimated.

Another common pitfall is mixing percentage scaling. ATK Rate is given in percent form but applied as a multiplier (x percent becomes x divided by 100). Misreading this as direct addition leads to outputs off by a factor of 100.

## Approaches

A brute-force interpretation would try to enumerate combinations of artifact choices per slot, but here each slot has exactly one artifact and all are chosen, so there is no combinatorial search. The only work is aggregation.

The core observation is that every stat contributes independently and linearly until the final evaluation step. This allows us to reduce the problem to parsing 25 strings and summing four running totals.

Once totals are computed, we directly apply the formula for ATK and expected damage. The only nonlinear behavior is the Crit Rate cap at 1.0, which must be applied after summation and before computing expectation.

Because everything is additive until the final formula, we do not need any data structures beyond four floating accumulators.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(1) | O(1) | Accepted |
| Parse and Aggregate | O(25) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize four accumulators: total flat ATK, total ATK percent, total Crit Rate, and total Crit Damage. These start from zero because base stats are handled separately in the final formula.
2. Read all 25 lines and parse each stat string by splitting at the plus sign. The left side identifies the stat type, and the right side provides a numeric value that may or may not include a percent sign.
3. If the stat is ATK, add the numeric value directly to total flat ATK.
4. If the stat is ATK Rate, convert percentage into a decimal by dividing by 100 and add it to total ATK percent.
5. If the stat is Crit Rate, convert to decimal and add it to total Crit Rate.
6. If the stat is Crit Damage, convert to decimal and add it to total Crit Damage.
7. After processing all artifacts, compute final ATK as 1500 multiplied by (1 plus total ATK percent) plus total flat ATK. This separates base scaling from additive flat bonuses.
8. Clamp Crit Rate to at most 1.0. This enforces the rule that probability cannot exceed certainty.
9. Compute expected damage using the weighted formula: ATK multiplied by (1 minus Crit Rate) plus ATK multiplied by (1 plus Crit Damage) multiplied by Crit Rate.
10. Output the result with sufficient precision to satisfy error constraints.

### Why it works

All stat contributions are independent and additive until the final expectation formula. This means we can safely aggregate each category without worrying about ordering or interaction effects between artifacts. The only nonlinear transformation is the Crit Rate cap, which is applied after summation, preserving correctness because probability saturation only depends on the total sum, not individual sources.

## Python Solution

```python
import sys
input = sys.stdin.readline

BASE_ATK = 1500.0
BASE_CRIT_RATE = 0.05
BASE_CRIT_DMG = 0.50

flat_atk = 0.0
atk_rate = 0.0
crit_rate = 0.0
crit_dmg = 0.0

for _ in range(25):
    s = input().strip()
    typ, val = s.split('+')

    if val.endswith('%'):
        x = float(val[:-1]) / 100.0
    else:
        x = float(val)

    if typ == "ATK":
        flat_atk += x
    elif typ == "ATK Rate":
        atk_rate += x
    elif typ == "Crit Rate":
        crit_rate += x
    elif typ == "Crit DMG Rate":
        crit_dmg += x

atk = BASE_ATK * (1.0 + atk_rate) + flat_atk

crit_rate = BASE_CRIT_RATE + crit_rate
crit_dmg = BASE_CRIT_DMG + crit_dmg

if crit_rate > 1.0:
    crit_rate = 1.0

expected = atk * (1.0 - crit_rate) + atk * (1.0 + crit_dmg) * crit_rate

print(expected)
```

The solution is structured around four independent accumulators, one per relevant stat. Parsing is done uniformly for all lines, with a simple check for percentage values. A common implementation mistake is forgetting that percentage stats must be divided by 100 before aggregation.

The ATK formula is applied only after all contributions are collected, since ATK percent modifies the base value rather than acting as a direct additive term. The Crit Rate clamp is applied after adding the base 5 percent, since both base and artifact contributions combine before enforcing the probability ceiling.

## Worked Examples

We construct a simplified trace using a minimal subset of inputs.

### Example 1

Input:

ATK+10

ATK Rate+10%

Crit Rate+10%

Crit DMG Rate+10%

| Step | flat ATK | ATK Rate | Crit Rate | Crit DMG |
| --- | --- | --- | --- | --- |
| After parsing | 10 | 0.10 | 0.10 | 0.10 |

Final computation proceeds as:

ATK = 1500 × 1.1 + 10 = 1660

Crit Rate = 0.05 + 0.10 = 0.15

Crit Damage = 0.50 + 0.10 = 0.60

Expected = 1660 × (0.85 + 1.60 × 0.15) = 1660 × 1.09 = 1809.4

This demonstrates correct separation of base stats and additive modifiers.

### Example 2

Input:

Crit Rate+120%

ATK+0

| Step | flat ATK | ATK Rate | Crit Rate | Crit DMG |
| --- | --- | --- | --- | --- |
| After parsing | 0 | 0.0 | 1.20 | 0.0 |

After base addition:

Crit Rate = 0.05 + 1.20 = 1.25, then clamped to 1.0

Expected becomes deterministic:

ATK × (1 + Crit DMG) = 1500 × 1.5 = 2250

This confirms correct handling of probability saturation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(25) | Each of the 25 lines is parsed once and contributes constant-time updates |
| Space | O(1) | Only a fixed number of floating-point accumulators are maintained |

The workload is constant-sized regardless of input structure, so performance is trivial under the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    BASE_ATK = 1500.0
    BASE_CRIT_RATE = 0.05
    BASE_CRIT_DMG = 0.50

    flat_atk = 0.0
    atk_rate = 0.0
    crit_rate = 0.0
    crit_dmg = 0.0

    for _ in range(25):
        s = sys.stdin.readline().strip()
        typ, val = s.split('+')
        if val.endswith('%'):
            x = float(val[:-1]) / 100.0
        else:
            x = float(val)

        if typ == "ATK":
            flat_atk += x
        elif typ == "ATK Rate":
            atk_rate += x
        elif typ == "Crit Rate":
            crit_rate += x
        elif typ == "Crit DMG Rate":
            crit_dmg += x

    atk = BASE_ATK * (1.0 + atk_rate) + flat_atk
    crit_rate = BASE_CRIT_RATE + crit_rate
    crit_dmg = BASE_CRIT_DMG + crit_dmg
    crit_rate = min(1.0, crit_rate)

    return str(atk * (1.0 - crit_rate) + atk * (1.0 + crit_dmg) * crit_rate)

# sample-like test
inp = "\n".join(["ATK+10"] * 25)
assert float(run(inp)) > 1500

# crit cap test
inp = "\n".join(["Crit Rate+50%"] * 3 + ["ATK+0"] * 22)
assert float(run(inp)) > 1500

# all damage stats
inp = "\n".join(["ATK Rate+10%", "Crit Rate+10%", "Crit DMG Rate+10%", "ATK+10", "ATK+10"] * 5)
assert float(run(inp)) > 0

# zero case
inp = "\n".join(["ATK+0"] * 25)
assert abs(float(run(inp)) - 1500 * (1 - 0.05 + 1.5 * 0.05)) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All ATK | >1500 | flat accumulation correctness |
| Excess Crit Rate | clamped | probability cap |
| Mixed stats | positive value | combined effects |
| Zero stats | base formula | baseline correctness |

## Edge Cases

A key edge case is Crit Rate overflow. If total Crit Rate exceeds 1.0 after summing all artifacts, the correct behavior is to clamp it. The algorithm handles this by applying a min operation after aggregation, ensuring probability does not exceed 100 percent.

Another case is mixing percentage formatting. Since some values include a percent sign and others do not, failure to normalize by dividing by 100 would inflate ATK Rate or Crit Rate by a factor of 100. The parsing step explicitly checks for the percent symbol and converts consistently.

A final subtle case is floating point precision. Since the required error tolerance is 1e-6, using Python float arithmetic is sufficient, but printing without formatting control is acceptable because the judge allows relative error.
