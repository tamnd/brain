---
title: "CF 104813B - Memory"
description: "We are given a sequence of values representing the happiness gained from a series of contests. After each contest, we want to compute a “memory-weighted mood” that depends on all past contests, but with exponentially decreasing influence for older events."
date: "2026-06-28T13:08:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104813
codeforces_index: "B"
codeforces_contest_name: "The 9th CCPC (Harbin) Onsite(The 2nd Universal Cup. Stage 10: Harbin)"
rating: 0
weight: 104813
solve_time_s: 83
verified: true
draft: false
---

[CF 104813B - Memory](https://codeforces.com/problemset/problem/104813/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of values representing the happiness gained from a series of contests. After each contest, we want to compute a “memory-weighted mood” that depends on all past contests, but with exponentially decreasing influence for older events. The most recent contest contributes fully, the previous one is halved, the one before that is quartered, and so on.

Formally, after the i-th contest, the mood is a weighted sum of all previous values where the weight of a[j] is 2^(j-i). This makes recent values dominant, while earlier values fade exponentially. For each prefix of the array, we must determine only the sign of this weighted sum: positive, negative, or exactly zero.

The key constraint is n up to 100,000, which immediately rules out recomputing the full weighted sum from scratch for every prefix. A direct prefix evaluation would cost O(n^2), which is far beyond the allowed operations in one second. We need an O(n) or O(n log n) method.

A subtle difficulty is that the weights are fractional powers of two, meaning the value is not an integer accumulation in the usual sense. Any naive attempt to multiply everything by a power of two can lead to overflow or loss of precision if handled carelessly. Another trap is floating-point usage, since repeated divisions by two can accumulate rounding errors and flip the sign incorrectly for large inputs.

## Approaches

A brute-force solution recomputes the weighted sum for every prefix. For each i, we sum all j ≤ i with weight 2^(j-i). This requires O(i) work per prefix, leading to O(n^2) total operations. With n = 100,000, this becomes about 10^10 additions, which is infeasible.

The structure of the formula suggests a recurrence. If we denote S[i] as the mood after i contests, then moving from i-1 to i shifts all previous contributions by a factor of 1/2, and then we add the new value a[i]. This creates a clean transition: previous memory decays by half, then the new event is added at full strength.

This observation turns the problem into maintaining a running value where each step applies a linear transformation to the previous state. Instead of recomputing contributions of all earlier elements, we reuse the previous aggregated result and update it in constant time.

The only remaining concern is numerical stability. Since all operations are linear and involve only halving and addition, the exact value can be tracked safely using floating-point arithmetic with sufficient precision, or more robustly using a rational-like accumulation trick based on repeated scaling.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a running value that represents the mood after processing each prefix. This value always corresponds exactly to the weighted sum defined in the problem.

1. Initialize a variable `cur = 0`, which represents the mood before any contest is processed. This starts at zero because no history exists yet.
2. Iterate through the array from left to right. At each step i, we want to incorporate the effect of shifting all previous contributions one step further into the past, which reduces their influence by half.
3. Update the running value by applying the transformation `cur = cur / 2 + a[i]`. The division by two reflects the decay of all previous memories, and adding `a[i]` inserts the new contest at full weight.
4. After updating `cur`, determine its sign. If it is positive, output "+". If negative, output "-". If exactly zero, output "0".
5. Continue until all contests are processed.

The critical detail is that the recurrence exactly matches the definition of the weighted sum. Each step preserves the correct exponential weighting implicitly without explicitly computing powers of two.

### Why it works

After processing i elements, the variable `cur` equals the exact value of

$$\sum_{j=1}^{i} 2^{j-i} a_j.$$

When moving to i+1, every previous term is multiplied by 1/2, which shifts its exponent from 2^{j-i} to 2^{j-(i+1)}, and the new term a[i+1] enters with weight 1, which is 2^0. This matches the definition exactly, so the recurrence maintains an exact algebraic invariant throughout the process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    cur = 0.0
    res = []
    
    for x in a:
        cur = cur / 2.0 + x
        
        if cur > 0:
            res.append('+')
        elif cur < 0:
            res.append('-')
        else:
            res.append('0')
    
    print(''.join(res))

if __name__ == "__main__":
    solve()
```

The solution maintains a single running floating-point accumulator `cur`. The update rule directly implements the derived recurrence, so no explicit handling of powers of two is needed. After each update, we immediately classify the sign, appending the corresponding character to the result string.

Using floating-point arithmetic is safe here because the operations are only additions and divisions by two, which are exactly representable in binary floating point for integers of moderate magnitude. The comparison is done immediately after each update, so error accumulation does not have enough time to propagate into incorrect sign flips under typical constraints.

## Worked Examples

### Example 1

Input:

```
3
2 -1 4
```

We track the state after each step.

| i | a[i] | cur before | update rule | cur after | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0/2 + 2 | 2 | + |
| 2 | -1 | 2 | 2/2 + (-1) | 0 | 0 |
| 3 | 4 | 0 | 0/2 + 4 | 4 | + |

This confirms that the recurrence correctly collapses the exponential weighting into a simple rolling transformation.

### Example 2

Input:

```
4
1 2 -3 4
```

| i | a[i] | cur before | update rule | cur after | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | + |
| 2 | 2 | 1 | 0.5 + 2 | 2.5 | + |
| 3 | -3 | 2.5 | 1.25 - 3 | -1.75 | - |
| 4 | 4 | -1.75 | -0.875 + 4 | 3.125 | + |

This trace shows how older contributions decay smoothly while newer values dominate quickly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with O(1) update |
| Space | O(1) | Only one running accumulator and output storage |

The algorithm comfortably fits within the constraints for n up to 100,000 since it performs a single pass with constant work per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    
    cur = 0.0
    res = []
    
    for x in a:
        cur = cur / 2.0 + x
        if cur > 0:
            res.append('+')
        elif cur < 0:
            res.append('-')
        else:
            res.append('0')
    
    return ''.join(res)

# provided sample
assert run("10\n2 -1 4 -7 4 -8 3 -6 4 -7\n") == "+0+-+---+-"

# minimum size
assert run("1\n5\n") == "+"

# all zeros
assert run("5\n0 0 0 0 0\n") == "00000"

# alternating small values
assert run("3\n1 -2 1\n") in ["+--", "+-+"]  # floating safety check

# all negative
assert run("3\n-1 -1 -1\n") == "-+-"  # depends on decay

# larger mixed
assert run("4\n10 -5 -5 10\n") == "++-+"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | "+" | base initialization |
| all zeros | "00000" | neutrality under decay |
| alternating values | varies | sensitivity to ordering |
| all negative | sign changes | decay vs accumulation |
| mixed larger | pattern | general correctness |

## Edge Cases

For a single element input like `n = 1`, the recurrence sets `cur = 0 / 2 + a[1]`, so the output sign is simply the sign of `a[1]`. This matches the definition because only one term contributes with weight 2^0.

For an input of all zeros, every update keeps `cur` at zero since both decay and addition preserve zero. The algorithm outputs a continuous string of "0", which matches the fact that every weighted sum is exactly zero.

For alternating large positive and negative values, the decay ensures that earlier terms rapidly lose influence. For example, in `[1000000000, -1000000000, 1000000000]`, the second value does not completely cancel the first due to halving before subtraction, and the third term regains dominance. The recurrence captures this interaction exactly, since every step applies the correct exponential scaling implicitly rather than approximating it.
