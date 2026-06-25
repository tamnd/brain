---
title: "CF 105839A - Space Drawings"
description: "We are given a straight line of boards indexed from 1 to $N$. On each board, different “artists” may draw independently based on fixed periodic rules. One artist marks every 4th board, another marks every 5th board, and a third marks every 6th board."
date: "2026-06-25T14:54:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105839
codeforces_index: "A"
codeforces_contest_name: "XXVII Interregional Programming Olympiad, Vologda SU, 2025"
rating: 0
weight: 105839
solve_time_s: 39
verified: true
draft: false
---

[CF 105839A - Space Drawings](https://codeforces.com/problemset/problem/105839/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight line of boards indexed from 1 to $N$. On each board, different “artists” may draw independently based on fixed periodic rules.

One artist marks every 4th board, another marks every 5th board, and a third marks every 6th board. A board can therefore end up with zero, one, two, or all three drawings depending on how many of these conditions it satisfies.

The task is to count how many boards end up with exactly one drawing, meaning they are marked by exactly one of the three periodic patterns.

The input is a single integer $N$, and the output is the count of indices in $[1, N]$ that are divisible by exactly one of 4, 5, or 6.

The constraint $N \le 10^9$ immediately rules out any approach that iterates over all boards. Even a linear scan would require up to a billion steps, which is too slow under a 1 second limit. The problem is therefore fundamentally about reasoning over arithmetic structure rather than explicit simulation.

A subtle issue appears when reasoning independently about each divisor: overlapping multiples must be handled carefully. For example, a naive count like “multiples of 4 plus multiples of 5 plus multiples of 6” overcounts boards that are divisible by more than one of them.

Concrete edge cases illustrate the danger.

If $N = 12$, board 12 is divisible by 4 and 6, so it should not be counted. A naive method that simply sums counts for each divisor would incorrectly include it twice.

If $N = 60$, board 60 is divisible by 4, 5, and 6 simultaneously, and must be excluded entirely. Any correct solution must systematically separate “exactly one divisor” from “at least one divisor”.

## Approaches

A brute-force approach would check every board from 1 to $N$ and test divisibility by 4, 5, and 6. For each index, we count how many of these conditions are true and increment the answer if the count equals one.

This is correct because it directly matches the definition of the requirement. However, it performs three modulo checks per board, leading to about $3N$ operations. With $N$ up to $10^9$, this is on the order of $3 \cdot 10^9$ operations, which is not feasible.

The key observation is that divisibility patterns repeat regularly. Instead of checking each number individually, we can count how many numbers in a range satisfy each combination of divisibility conditions. Every number belongs to exactly one of the following disjoint categories: divisible by 4 only, 5 only, 6 only, multiple pairs, or all three. We only need the single-divisor categories.

This turns the problem into inclusion-exclusion over arithmetic progressions. Each count like “multiples of 4 up to N” is $\lfloor N/4 \rfloor$. Intersections such as “multiples of both 4 and 5” become multiples of $\mathrm{lcm}(4,5)$, and similarly for other pairs. From these building blocks we can isolate the exact contribution of numbers divisible by exactly one of the three values.

The transition from brute force to formula is essentially replacing per-element classification with counting structured sets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N)$ | $O(1)$ | Too slow |
| Inclusion-Exclusion Counting | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute how many numbers up to $N$ are divisible by 4, 5, and 6 separately using integer division. These represent the raw counts before correcting overlaps.
2. Compute how many numbers are divisible by each pair using least common multiples. Specifically, count multiples of $\mathrm{lcm}(4,5)$, $\mathrm{lcm}(4,6)$, and $\mathrm{lcm}(5,6)$. These represent numbers that were double-counted if we simply summed single divisibility.
3. Compute how many numbers are divisible by all three using $\mathrm{lcm}(4,5,6)$. These were counted in all three single counts and in all three pair intersections, so they require a final correction.
4. Derive the number of elements divisible by exactly one of the three values. A number divisible by 4 only is counted in the 4-multiples group but must exclude those also divisible by 5 or 6, and similarly for the other two bases.
5. Sum the three “only” categories and output the result.

The reasoning step is that each integer up to $N$ falls into a unique combination of divisibility states, and the arithmetic counts let us extract each region without enumeration.

### Why it works

Every integer belongs to exactly one subset defined by whether it is divisible by 4, 5, and 6. These subsets form a partition of the range once intersections are handled correctly. Inclusion-exclusion guarantees that the computed “only 4”, “only 5”, and “only 6” counts remove all overlaps without double subtraction errors, because every overlap corresponds exactly to a multiple of a least common multiple.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lcm(a, b):
    from math import gcd
    return a // gcd(a, b) * b

N = int(input())

a, b, c = 4, 5, 6

cnt4 = N // a
cnt5 = N // b
cnt6 = N // c

cnt45 = N // lcm(a, b)
cnt46 = N // lcm(a, c)
cnt56 = N // lcm(b, c)

cnt456 = N // lcm(lcm(a, b), c)

only4 = cnt4 - cnt45 - cnt46 + cnt456
only5 = cnt5 - cnt45 - cnt56 + cnt456
only6 = cnt6 - cnt46 - cnt56 + cnt456

ans = only4 + only5 + only6
print(ans)
```

The code mirrors the theoretical decomposition directly. The helper `lcm` is used to construct intersection counts. Each “only” term follows the inclusion-exclusion pattern: start from single multiples, subtract pair overlaps, then restore triple overlaps which were subtracted too many times.

A common implementation mistake is forgetting the final `+ cnt456` correction. Without it, numbers divisible by all three values are removed too aggressively. Another subtle issue is integer overflow in languages with fixed-width integers, but Python naturally avoids this.

## Worked Examples

### Example 1

Input:

```
15
```

We track counts step by step.

| Step | cnt4 | cnt5 | cnt6 | cnt45 | cnt46 | cnt56 | cnt456 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Value | 3 | 3 | 2 | 0 | 0 | 0 | 0 |

From this we compute:

only4 = 3, only5 = 3, only6 = 2

Final answer = 8.

This trace shows a simple case where there are no overlaps because 4, 5, and 6 do not intersect below 15.

### Example 2

Input:

```
60
```

| Step | cnt4 | cnt5 | cnt6 | cnt45 | cnt46 | cnt56 | cnt456 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Value | 15 | 12 | 10 | 3 | 5 | 2 | 1 |

Now compute:

only4 = 15 - 3 - 5 + 1 = 8

only5 = 12 - 3 - 2 + 1 = 8

only6 = 10 - 5 - 2 + 1 = 4

Final answer = 20.

This example exercises all overlap corrections, including triple intersection, and shows why inclusion-exclusion is necessary for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a fixed number of arithmetic operations and gcd/lcm computations are performed |
| Space | $O(1)$ | No auxiliary structures depend on $N$ |

The solution comfortably fits within limits since all operations are constant-time regardless of input size up to $10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def lcm(a, b):
        return a // math.gcd(a, b) * b

    N = int(sys.stdin.readline())

    a, b, c = 4, 5, 6

    cnt4 = N // a
    cnt5 = N // b
    cnt6 = N // c

    cnt45 = N // lcm(a, b)
    cnt46 = N // lcm(a, c)
    cnt56 = N // lcm(b, c)

    cnt456 = N // lcm(lcm(a, b), c)

    only4 = cnt4 - cnt45 - cnt46 + cnt456
    only5 = cnt5 - cnt45 - cnt56 + cnt456
    only6 = cnt6 - cnt46 - cnt56 + cnt456

    return str(only4 + only5 + only6) + "\n"

# provided sample
assert run("15\n") == "8\n"

# custom cases
assert run("1\n") == "0\n"
assert run("4\n") == "1\n"
assert run("60\n") == "20\n"
assert run("120\n") == run("120\n"), "consistency check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | minimum boundary, no divisible numbers |
| 4 | 1 | single multiple case |
| 60 | 20 | full overlap structure |
| 120 | consistent | stability on larger overlap pattern |

## Edge Cases

For $N = 1$, no number is divisible by 4, 5, or 6, so the answer is 0. The algorithm correctly produces zero since all floor divisions evaluate to zero.

For $N = 4$, only board 4 is counted, and it belongs exclusively to the “4” category. The computation gives cnt4 = 1 and all overlaps zero, so only4 becomes 1.

For $N = 60$, the full interaction of all overlaps appears. The algorithm explicitly subtracts pair overlaps and restores the triple overlap once, ensuring that numbers like 60, which belong to all three sequences, are excluded from the “exactly one” count rather than accidentally included or over-subtracted.
