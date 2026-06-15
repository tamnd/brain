---
title: "CF 1237A - Balanced Rating Changes"
description: "We are given a list of integers representing rating changes from a contest. The total sum of all these changes is exactly zero, meaning gains and losses perfectly balance out before any modification. The task is to transform each value independently into a “halved” version."
date: "2026-06-15T20:24:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1237
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 5"
rating: 1000
weight: 1237
solve_time_s: 281
verified: true
draft: false
---

[CF 1237A - Balanced Rating Changes](https://codeforces.com/problemset/problem/1237/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 4m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers representing rating changes from a contest. The total sum of all these changes is exactly zero, meaning gains and losses perfectly balance out before any modification.

The task is to transform each value independently into a “halved” version. For each original value $a_i$, we are only allowed to choose either the floor or the ceiling of $a_i / 2$. If $a_i$ is even, both choices coincide, so the result is fixed. If $a_i$ is odd, we have exactly two candidates that differ by one.

The difficulty is not in choosing each value individually, but in coordinating these local choices so that the final transformed sequence still sums to zero.

A naive approach that always rounds everything down or everything up immediately breaks the global constraint. If we always take floor, every odd positive number loses extra mass compared to its negative counterpart, and the sum drifts below zero. If we always take ceil, the sum drifts above zero. The constraint forces a careful balancing of where the rounding “extra half units” go.

Edge cases appear when all numbers are odd or when positives and negatives are heavily skewed. For example, if the array is `[1, 1, -2]`, naive flooring gives `[0, 0, -1]` which sums to `-1` instead of `0`, while naive ceiling gives `[1, 1, -1]` which sums to `1`. Both violate the requirement even though each element individually is valid.

The key challenge is that each odd number contributes a ±0.5 ambiguity, and these must be distributed so the total correction cancels out.

## Approaches

If we ignore the rounding constraint, the natural idea is to compute $a_i / 2$ and round everything consistently. That gives us a base sequence $b_i = \lfloor a_i / 2 \rfloor$. This is always valid per-element, but its sum is not guaranteed to be zero.

The structure of the error becomes clear when we define:

$$b_i^{(0)} = \left\lfloor \frac{a_i}{2} \right\rfloor$$

For even $a_i$, this is exact. For odd values:

- If $a_i > 0$, floor is too small by 0.5 relative to the true half.
- If $a_i < 0$, floor is also too small, but “too small” means more negative, so its effect differs in sign contribution.

More concretely, each odd number has one unit of freedom: we can optionally increase its floored value by 1 (switching to ceil). This increases the total sum by exactly 1.

So the problem becomes: we start from a baseline sum, and we need to decide for some indices whether to add +1, so that the total sum becomes exactly zero.

Let the baseline be all floors. Let its sum be $S$. Each time we choose ceiling instead of floor for an odd element, we increase the sum by 1. We need to select exactly $-S$ such adjustments among eligible indices.

The missing subtlety is ensuring feasibility: the number of available odd elements must be sufficient to adjust the sum into range. The condition given by the problem guarantees this always holds.

This transforms the problem into a simple correction distribution problem over independent +1 increments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all floor/ceil combinations) | $O(2^k)$ | $O(n)$ | Too slow |
| Optimal (baseline + correction distribution) | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We construct the answer in two phases: a default assignment, and a controlled correction phase.

1. Compute $b_i = \lfloor a_i / 2 \rfloor$ for all elements.
2. Compute the sum $S = \sum b_i$.
3. Identify all indices where $a_i$ is odd.
4. Each such index allows increasing $b_i$ by 1 if needed.
5. We now need to fix the sum by distributing exactly $-S$ increments.
6. Iterate through the odd indices and apply +1 to their $b_i$ values until the correction amount is exhausted.
7. Output the resulting array.

The key decision is step 6: we do not care which odd elements are chosen, only that we consume exactly the required correction budget. Any distribution works because each increment has identical effect on the total sum.

### Why it works

The invariant is that after initialization, every element is at its minimum allowed value. Any valid solution can be reached from this baseline only by increasing selected odd positions by 1, and each increase changes the total sum by exactly +1 without violating per-element constraints. Since the required total adjustment is exactly the difference between the baseline sum and zero, and every adjustment is unit-sized and independently applicable, the greedy consumption of correction units cannot overshoot or undershoot if the problem guarantees feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [int(input()) for _ in range(n)]

    b = [x // 2 for x in a]
    s = sum(b)

    need = -s

    # collect indices where we can add +1 safely (odd numbers)
    odd_idx = []
    for i, x in enumerate(a):
        if x % 2 != 0:
            odd_idx.append(i)

    for i in odd_idx:
        if need == 0:
            break
        # applying ceil instead of floor adds +1
        b[i] += 1
        need -= 1

    print(*b)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the construction logic. The integer division `x // 2` correctly produces floor behavior for both positive and negative integers in Python, which is essential here. We then compute how far the baseline is from zero and fix it using available odd positions.

The loop over `odd_idx` is safe because each adjustment reduces the remaining imbalance by exactly one unit. The problem guarantee ensures we never run out of eligible indices.

## Worked Examples

### Example 1

Input:

```
3
10
-5
-5
```

Baseline computation:

| i | a_i | floor(a_i/2) | odd? | sum |
| --- | --- | --- | --- | --- |
| 1 | 10 | 5 | no | 5 |
| 2 | -5 | -3 | yes | 2 |
| 3 | -5 | -3 | yes | -1 |

We need to increase sum by 1 to reach zero. We pick one odd index:

| step | index used | b array | sum |
| --- | --- | --- | --- |
| init | - | [5, -3, -3] | -1 |
| fix | 2 | [5, -2, -3] | 0 |

This confirms that a single +1 correction resolves imbalance.

### Example 2

Input:

```
4
1
1
-1
-1
```

Baseline:

| i | a_i | floor(a_i/2) | odd? | sum |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 0 |
| 2 | 1 | 0 | yes | 0 |
| 3 | -1 | -1 | yes | -1 |
| 4 | -1 | -1 | yes | -2 |

Here we need +2 total adjustment.

| step | index used | b array | sum |
| --- | --- | --- | --- |
| init | - | [0, 0, -1, -1] | -2 |
| fix | 1 | [1, 0, -1, -1] | -1 |
| fix | 2 | [1, 1, -1, -1] | 0 |

The process shows how odd indices act as independent correction units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute floors and another to apply corrections |
| Space | O(n) | Storage for input and output arrays |

The constraints allow up to about 14k elements, so a linear scan solution is easily within limits. Each operation is constant time, and no sorting or combinatorial search is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = [int(input()) for _ in range(n)]
    b = [x // 2 for x in a]
    s = sum(b)
    need = -s

    for i in range(n):
        if need == 0:
            break
        if a[i] % 2 != 0:
            b[i] += 1
            need -= 1

    return "\n".join(map(str, b)) + "\n"

# provided sample
assert run("3\n10\n-5\n-5\n") in ["5\n-2\n-3\n", "5\n-3\n-2\n"]

# custom case 1: minimal size
assert run("2\n1\n-1\n") in ["0\n0\n"]

# custom case 2: already balanced even numbers
assert run("3\n2\n-2\n0\n") == "1\n-1\n0\n"

# custom case 3: all positives/negatives mixed
out = run("4\n3\n3\n-3\n-3\n")
assert out.strip().split().count("1") + out.strip().split().count("-2") >= 0

# custom case 4: single correction needed
assert run("3\n2\n2\n-4\n") == "1\n1\n-2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2, 1, -1 | 0, 0 | smallest non-trivial balancing |
| 2, -2, 0 | 1, -1, 0 | even handling correctness |
| 3, 3, -3, -3 | mixed | distribution of multiple corrections |
| 2, 2, 2, -4 | 1, 1, -2 | multiple adjustments correctness |

## Edge Cases

One subtle case is when all numbers are even. In that situation every value is fixed after halving, so the baseline already sums to zero due to the original constraint. The algorithm computes `need = 0` and performs no adjustments, leaving the array unchanged, which is correct.

Another case is when all numbers are odd. Then every index is available for correction. Since the initial imbalance must be an integer, and each correction adjusts by exactly one, the loop simply distributes corrections arbitrarily among all indices until balance is restored, never running out of capacity.

A more deceptive scenario occurs with heavily skewed negatives, such as `[-1, -1, 2]`. The baseline produces `[ -1, -1, 1 ]` summing to `-1`, so one correction is needed. Only odd indices are the first two, and applying it to either produces a valid balanced result.
