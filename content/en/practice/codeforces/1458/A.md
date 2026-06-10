---
title: "CF 1458A - Row GCD"
description: "The problem presents us with two sequences of integers: the first sequence a contains n elements, and the second sequence b contains m elements."
date: "2026-06-11T02:33:38+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1458
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 691 (Div. 1)"
rating: 1600
weight: 1458
solve_time_s: 264
verified: true
draft: false
---

[CF 1458A - Row GCD](https://codeforces.com/problemset/problem/1458/A)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 4m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents us with two sequences of integers: the first sequence `a` contains `n` elements, and the second sequence `b` contains `m` elements. For each element `b_j` in `b`, we are asked to compute the greatest common divisor (GCD) of the sequence formed by adding `b_j` to every element in `a`. In other words, we must compute the GCD of `a_1 + b_j, a_2 + b_j, ..., a_n + b_j` for each `b_j`.

The constraints are large: `n` and `m` can each be up to 2 × 10^5, and individual elements can be up to 10^18. This rules out any approach that explicitly computes the GCD of all elements for each `b_j` in a naive nested loop, because that would require O(n × m) GCD computations, which could be up to 4 × 10^10 operations. Any such approach would exceed reasonable time limits.

A subtle point is that all numbers are positive and potentially very large. This means that integer overflow is a concern in languages with fixed-width integers, but in Python we can rely on arbitrary precision arithmetic. Another edge case is when `n = 1`, in which case the GCD of a single number is the number itself. A careless implementation might attempt to compute differences between elements without handling this properly.

## Approaches

A naive approach would be to iterate over every `b_j` and then compute the GCD of `a_i + b_j` for all `i` in `a`. This would be correct, because the GCD of a set of numbers can be computed iteratively, but its complexity is O(n × m), which is too slow for the given constraints.

The key insight is that for any sequence `x_1, x_2, ..., x_n`, the GCD of the sequence is the same as the GCD of the first element plus the differences from the first element. Formally,

```

```

Applying this to our problem:

```

```

The differences `a_i - a_1` do not depend on `b_j`, so we can precompute their GCD once, which we call `g = GCD(a_2 - a_1, a_3 - a_1, ..., a_n - a_1)`. Then for each `b_j`, the answer is simply `GCD(a_1 + b_j, g)`. This reduces the complexity to O(n + m), which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × m) | O(1) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`, then read sequences `a` and `b`.
2. If `n == 1`, the GCD for each `b_j` is just `a[0] + b_j`, because a single number's GCD is itself.
3. Otherwise, compute the GCD of the differences from the first element:

```

```

This gives the GCD of all differences `a_i - a_1`.
4. For each `b_j` in `b`, compute `GCD(a[0] + b_j, g)` and store the result.
5. Output the results in order.

Why it works: The invariant is that adding a constant `b_j` to all elements shifts all numbers by the same amount. The differences between elements remain the same, so the GCD can be factored using the first element and the precomputed GCD of differences. This guarantees correctness for all `b_j` without recomputing differences each time.

## Python Solution

```
PythonRun
```

### Explanation

The first section handles the special case `n = 1`, where the answer is trivial. The differences `a[i] - a[0]` are precomputed for all `i > 0` and their GCD is stored in `g`. This step ensures that the sequence's structure relative to the first element is captured. Then for each element `b_j` in the second sequence, we compute `gcd(a[0] + b_j, g)`, which is sufficient because all differences have already been factored in.

## Worked Examples

Input:

```

```

Compute differences from first element:

```

```

GCD of differences: `gcd(24, 120) = 24`, `gcd(24, 168) = 24` → `g = 24`

Compute answers:

| b_j | a[0] + b_j | gcd(a[0] + b_j, g) | Result |
| --- | --- | --- | --- |
| 1 | 2 | gcd(2, 24) | 2 |
| 2 | 3 | gcd(3, 24) | 3 |
| 7 | 8 | gcd(8, 24) | 8 |
| 23 | 24 | gcd(24, 24) | 24 |

Output: `2 3 8 24` → matches sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Precompute GCD of differences in O(n), then compute GCD for each `b_j` in O(1) × m |
| Space | O(n + m) | Store sequences `a` and `b`, output list |

This fits within the limits because n + m ≤ 4 × 10^5, which is well below the 2-second time limit.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3\n7\n2 3 5\n` | `9 10 12` | Single element sequence a |
| `3 2\n5 5 5\n1 2\n` | `6 7` | All equal elements in a |
| `2 2\n10^18 10^18+12\n10^18 10^18-1\n` | `12 13` | Handling of very large numbers |
| `1 1\n42\n58\n` | `100` | Minimal |
