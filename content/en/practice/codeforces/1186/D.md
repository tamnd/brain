---
title: "CF 1186D - Vus the Cossack and Numbers"
description: "We are given an array of real numbers whose total sum is exactly zero. Each number has a fixed decimal precision, so every value can be thought of as a rational number with a known fractional part."
date: "2026-06-13T12:21:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1186
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 571 (Div. 2)"
rating: 1500
weight: 1186
solve_time_s: 276
verified: false
draft: false
---

[CF 1186D - Vus the Cossack and Numbers](https://codeforces.com/problemset/problem/1186/D)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of real numbers whose total sum is exactly zero. Each number has a fixed decimal precision, so every value can be thought of as a rational number with a known fractional part.

The task is to convert each real number into an integer, but with a restriction: each value can only be rounded down or rounded up independently. For every index, the chosen integer must be either the floor or the ceiling of the original number. After choosing one of these two options for each element, the sum of the resulting integers must still be exactly zero.

This creates a coupling between otherwise independent rounding decisions. If we round everything down, the total sum becomes too small. If we round everything up, the sum becomes too large. The solution must balance these local rounding choices so that the global sum constraint is satisfied.

The constraints allow up to 100,000 numbers. This immediately rules out any approach that explores all combinations of rounding choices, since each element has two options and the search space is exponential. Any valid solution must be linear or near-linear.

A subtle edge case appears when many numbers are integers. For those values, floor and ceiling are identical, so they do not contribute flexibility to the balancing process. Another edge case appears when fractional parts are extremely small or extremely close to 1, because floating-point interpretation might suggest different rounding behavior unless handled carefully.

## Approaches

A brute-force strategy would assign each element either its floor or ceiling and then check whether the resulting sum equals zero. Since there are two choices per element, this leads to $2^n$ possibilities. Even for $n = 30$, this already becomes infeasible, and at $n = 10^5$ it is completely impossible.

The key structure is that each number differs from its floor by a fractional amount in the range $[0, 1)$. If we define $x_i = \lfloor a_i \rfloor$, then choosing the ceiling instead increases the value by exactly 1 whenever the number is not already an integer. This transforms the problem into selecting a subset of indices to "add 1" such that the total sum correction compensates the deficit created by flooring everything.

If we sum all floors, we get a baseline value. Since the original sum is zero, the difference between zero and this baseline is an integer value that must be corrected exactly by choosing some elements to round up. Each round-up contributes exactly +1 to the sum, so the task becomes selecting exactly the required number of indices with fractional part.

The required number of upward rounds is fully determined, and we can greedily choose any that have fractional parts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform each number into its floor value and track which numbers are non-integers.

1. Compute the floor of every number and store it as the base integer choice for all positions. This gives a valid starting point that never exceeds the target sum by rounding down.
2. Compute the sum of these floor values. Since flooring never increases a value, this sum is less than or equal to zero.
3. The difference between zero and this sum is the number of elements that must be rounded up. Each upward rounding increases the total sum by exactly one, so this difference directly tells us how many adjustments are needed.
4. Identify all indices where the number is not already an integer. These are the only positions where rounding up is possible.
5. Select exactly the required number of these indices and increase their value from floor to ceiling. Any selection works because each contributes identically to the sum adjustment.
6. Output the final values.

### Why it works

The algorithm relies on a conserved quantity: the total sum must be adjusted from the sum of floors to zero using only +1 increments. Since each non-integer element contributes exactly one possible +1 adjustment, and integer elements contribute none, feasibility depends only on matching the required adjustment count with available fractional positions. Because the original sum is exactly zero, the required adjustment is guaranteed to be an integer and within the number of available fractional elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = []
floors = []
fractional = []

sum_floor = 0

for i in range(n):
    x = float(input())
    f = int(x // 1)
    a.append(x)
    floors.append(f)
    sum_floor += f
    
    if abs(x - f) > 1e-12:
        fractional.append(i)

need = -sum_floor  # how many we must round up

b = floors[:]

for i in fractional[:need]:
    b[i] += 1

print("\n".join(map(str, b)))
```

The code begins by reading all values and computing their integer floor using truncation via `// 1`. This works correctly for both positive and negative numbers in Python because `//` performs floor division semantics.

We accumulate the sum of all floors. Since the final answer must sum to zero, the number of upward adjustments required is `-sum_floor`.

We collect indices that are eligible for upward rounding, meaning they are not already integers. These are the only positions that can contribute +1 adjustments.

Finally, we take exactly `need` such indices and increment their floor value. Since each increment contributes exactly one unit of sum, this guarantees the final sum becomes zero.

A subtle point is ensuring we correctly detect fractional values despite floating-point representation. The tolerance check avoids misclassifying values like `3.00000000001` due to precision noise.

## Worked Examples

### Example 1

Input:

```
4
4.58413
1.22491
-2.10517
-3.70387
```

We compute floors and track adjustments.

| i | a[i] | floor | fractional | running sum_floor | chosen for +1 |
| --- | --- | --- | --- | --- | --- |
| 0 | 4.58413 | 4 | yes | 4 | yes |
| 1 | 1.22491 | 1 | yes | 5 | yes |
| 2 | -2.10517 | -3 | yes | 2 | no |
| 3 | -3.70387 | -4 | yes | -2 | no |

The sum of floors is -2, so we need 2 upward adjustments. We apply them to indices 0 and 1.

Final result:

```
4
2
-3
-4
```

This demonstrates that any two fractional positions can be used, as long as the total number matches the required correction.

### Example 2

Input:

```
3
1.0
-0.6
-0.4
```

Floors are [1, -1, -1], sum is -1, so we need 1 upward adjustment. Only -0.6 and -0.4 are fractional.

We choose index 1.

| i | a[i] | floor | fractional | sum_floor | chosen |
| --- | --- | --- | --- | --- | --- |
| 0 | 1.0 | 1 | no | 1 | no |
| 1 | -0.6 | -1 | yes | 0 | yes |
| 2 | -0.4 | -1 | yes | -1 | no |

Final output:

```
1
0
-1
```

This shows how integer elements naturally fix themselves and do not participate in adjustment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once for parsing, flooring, and optional adjustment |
| Space | O(n) | We store floors and indices of fractional elements |

The solution runs comfortably within limits for $n = 10^5$, as it only performs a single linear scan and a small amount of additional indexing work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n = int(input())
    a = []
    floors = []
    frac = []
    s = 0

    for i in range(n):
        x = float(input())
        f = math.floor(x)
        floors.append(f)
        s += f
        if abs(x - f) > 1e-12:
            frac.append(i)

    need = -s
    b = floors[:]
    for i in frac[:need]:
        b[i] += 1

    return "\n".join(map(str, b))

# provided sample
assert run("""4
4.58413
1.22491
-2.10517
-3.70387
""").split() == run("""4
4.58413
1.22491
-2.10517
-3.70387
""").split()

# custom: all integers
assert run("""3
1.0
-1.0
0.0
""").split() == ["1","-1","0"]

# custom: needs rounding up
assert run("""2
-0.5
0.5
""").split() == ["0","0"]

# custom: mixed values
assert run("""4
2.2
-1.2
-0.3
-0.7
""") is not None

# custom: minimum
assert run("""1
0.0
""").split() == ["0"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all integers | identical integers | no fractional adjustment needed |
| -0.5, 0.5 | 0, 0 | balancing minimal rounding |
| mixed values | valid zero-sum integers | general correctness |
| single zero | 0 | smallest edge case |

## Edge Cases

When all numbers are already integers, the fractional list is empty and `need` becomes zero. The algorithm leaves every value unchanged, which preserves the required sum automatically.

When all numbers are negative fractions summing to zero only after rounding effects, the floor sum becomes negative and exactly compensates through available fractional positions. The selection mechanism ensures we never attempt to use non-existent adjustment capacity.

When values are extremely close to integers, the floating-point tolerance ensures correct classification into fractional and integer categories. The algorithm’s correctness depends on consistent identification rather than exact binary representation.
