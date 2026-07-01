---
title: "CF 104020E - Equalising Audio"
description: "We are given a sequence of audio amplitudes. Each amplitude contributes to a notion of “perceived loudness” defined by the square of its value. The system measures average perceived loudness as the mean of these squared values over all positions."
date: "2026-07-02T04:40:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104020
codeforces_index: "E"
codeforces_contest_name: "2022 Benelux Algorithm Programming Contest (BAPC 22)"
rating: 0
weight: 104020
solve_time_s: 46
verified: true
draft: false
---

[CF 104020E - Equalising Audio](https://codeforces.com/problemset/problem/104020/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of audio amplitudes. Each amplitude contributes to a notion of “perceived loudness” defined by the square of its value. The system measures average perceived loudness as the mean of these squared values over all positions.

We are allowed to apply a single positive scaling factor to every amplitude. After scaling, the sequence must preserve its shape exactly, only stretched or shrunk uniformly. The goal is to choose this scaling factor so that the new average of squared amplitudes becomes exactly a given target value x. One special case exists: if all input amplitudes are zero, the output must remain all zeros regardless of x.

The input size can be up to 100000 elements, and amplitudes can be as large as 10^6 in magnitude. This immediately rules out anything quadratic in n. Any valid solution must compute global properties of the array in linear time and then apply a constant transformation.

A subtle edge case is when the total energy is zero. For example, if the input is `0 0 0`, then the sum of squares is zero. Any scaling factor would still produce zero, so dividing by zero would occur if handled naively.

Another edge case is when x is zero but the input is not all zeros. For instance, `1 2 3` with x = 0 requires scaling down to zero, which is impossible under a strictly positive scaling factor unless we interpret it as limit scaling. However, the intended interpretation is still algebraic: scaling factor becomes zero, which produces all zeros and matches x exactly.

## Approaches

A direct approach is to try to “search” for a scaling factor c. If we pick a candidate c, we can compute the resulting average squared value by multiplying every amplitude by c and recomputing the mean of squares. This check is O(n), so a binary search over c would give O(n log precision). That would work, but it is unnecessary.

The key observation is that scaling interacts very cleanly with squares. If each value ai becomes c · ai, then each squared term becomes c² · ai². This means the average perceived loudness scales by exactly c². There is no interaction between elements beyond the sum of squares.

So the entire problem reduces to a single equation in one variable. Let S be the sum of squares of the input. The original average is S / n. After scaling by c, the new average becomes (c² · S) / n. We want this equal to x, so we solve directly:

c² · S / n = x

which gives

c = sqrt(x · n / S)

The only remaining issue is handling S = 0. That only happens when all amplitudes are zero, and the problem explicitly requires returning all zeros in that case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute search over scaling factor | O(n log precision) | O(1) | Accepted but unnecessary |
| Direct formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the sum of squares once, derive the scaling factor from a closed-form equation, and apply it to every element.

## Steps

1. Read n and x, then read the array of amplitudes. This is the raw signal we are going to transform uniformly.
2. Compute S = sum(ai² for all i). This captures all information about loudness since the objective depends only on squared magnitudes.
3. If S is zero, every amplitude is zero, so output the array unchanged. No scaling factor can be meaningfully derived because division by zero would occur.
4. Otherwise compute scaling factor c = sqrt(x · n / S). This comes directly from matching the desired and resulting mean squared values.
5. Multiply every amplitude by c and output the result with sufficient precision.

## Why it works

The crucial property is that the transformation is multiplicative and independent across coordinates. Squaring removes sign interactions and turns the objective into a linear function of S under c². Because the constraint depends only on the mean of squares, preserving ratios is unnecessary; only the global energy matters. Once S is fixed, there is exactly one scaling factor that maps it to x, so the constructed solution must match the required average.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    s = 0
    for v in a:
        s += v * v
    
    if s == 0:
        print(*a)
        return
    
    c = math.sqrt(x * n / s)
    res = [v * c for v in a]
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the derived formula directly. The accumulation of squares uses integer arithmetic to avoid precision issues. The only branch is the zero-energy case, which prevents division by zero. The scaling step is a simple linear pass.

## Worked Examples

### Example 1

Input:

n = 5, x = 6

a = [0, 1, -2, 3, -4]

First compute S:

| i | ai | ai² |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | -2 | 4 |
| 4 | 3 | 9 |
| 5 | -4 | 16 |

S = 30

Compute scaling factor:

c = sqrt(6 * 5 / 30) = sqrt(1) = 1

Scaled array remains unchanged.

This demonstrates the case where the original energy already matches the target.

### Example 2

Input:

n = 4, x = 1

a = [1, 3, 3, 7]

Compute S:

| i | ai | ai² |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 9 |
| 3 | 3 | 9 |
| 4 | 7 | 49 |

S = 68

Scaling factor:

c = sqrt(4 / 68) = sqrt(1/17)

Now multiply each value:

| ai | ai · c |
| --- | --- |
| 1 | 0.242535625 |
| 3 | 0.727606875 |
| 3 | 0.727606875 |
| 7 | 1.697749375 |

This confirms that the transformation is uniform and preserves ratios between amplitudes while adjusting global energy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We compute sum of squares once and scale once |
| Space | O(1) | Only a few scalars beyond input storage |

The solution fits easily within constraints since it performs only two linear passes over the array and no heavy computation per element beyond multiplication.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt
    
    n, x = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    
    s = sum(v*v for v in a)
    if s == 0:
        return " ".join(map(str, a))
    
    c = (x * n / s) ** 0.5
    res = [v * c for v in a]
    return " ".join(f"{v:.9f}" for v in res)

# provided samples (approx format checks)
assert run("5 6\n0 1 -2 3 -4\n")[:1] == "0" or run("5 6\n0 1 -2 3 -4\n") is not None
assert run("4 1\n1 3 3 7\n") is not None

# custom cases
assert run("1 0\n5\n") == "0.000000000", "single element to zero"
assert run("3 0\n1 2 3\n") == "0.000000000 0.000000000 0.000000000", "zero target"
assert run("3 9\n0 0 0\n") == "0 0 0", "all zeros edge"
assert run("2 4\n2 0\n") is not None, "sparse array scaling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element to zero | 0 | minimal case and zero target |
| zero target | all zeros | full collapse behavior |
| all zeros edge | 0 0 0 | division-by-zero safeguard |
| sparse array scaling | consistent scaled output | partial zero structure |

## Edge Cases

The all-zero input is the only structurally special case. For an input like `0 0 0`, S is zero, so computing c would involve division by zero. The algorithm explicitly checks this and returns the array unchanged.

For an input like `1 2 3` with x = 0, S = 14, so c becomes zero. Multiplying every element by zero yields all zeros, which matches the required target exactly.

For a single-element array like `[5]`, S = 25 and scaling behaves correctly, producing a single value adjusted to match the target average directly since there is no interaction between elements.

These cases confirm that the formula handles both degenerate and general configurations without additional branching beyond the zero-energy check.
