---
title: "CF 105911A - Nezha Naohai"
description: "We are given three independent events that represent how long Nezha spends causing disturbances in the sea. Each event has a duration measured in hours, and during every hour of disturbance, a fixed number of complaints is generated."
date: "2026-06-21T12:11:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105911
codeforces_index: "A"
codeforces_contest_name: "2025 ICPC Nanchang Invitational and Jiangxi Provincial Collegiate Programming Contest"
rating: 0
weight: 105911
solve_time_s: 48
verified: true
draft: false
---

[CF 105911A - Nezha Naohai](https://codeforces.com/problemset/problem/105911/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three independent events that represent how long Nezha spends causing disturbances in the sea. Each event has a duration measured in hours, and during every hour of disturbance, a fixed number of complaints is generated.

Concretely, there are three durations, corresponding to three separate incidents. The first lasts A hours, the second lasts B hours, and the third lasts C hours. Every single hour spent in any of these incidents contributes exactly D complaints. The task is to compute the total number of complaints generated across all three incidents.

The structure of the problem implies that the total time spent disturbing the sea is simply the sum of the three durations. Since each hour independently contributes the same fixed cost, the final answer is just the total time multiplied by the per-hour complaint rate.

The constraints are extremely small, with all values bounded between 1 and 100. This immediately rules out any concern about overflow in typical integer types and confirms that even the most straightforward arithmetic approach is sufficient within the time limit.

There are no hidden edge cases involving ordering, overlap, or partial contributions. Each incident is fully independent and contributes linearly to the result.

A common mistake would be to accidentally multiply instead of summing durations, for example computing A × B × C × D, which has no meaningful interpretation in the problem context. Another mistake would be to apply D per incident rather than per hour, leading to (A + B + C) × D being misinterpreted as A × D + B × D + C × D but incorrectly implemented with missing parentheses or incorrect grouping in more complex languages. In Python, this is less risky but still worth being explicit.

## Approaches

The most direct way to think about the problem is to simulate what happens during each incident. We could conceptually iterate over each hour of each of the three events and add D complaints per hour. This would look like looping A times, then B times, then C times, incrementing a counter each time. This is correct because it mirrors the definition exactly.

However, this approach is unnecessary because it performs repeated identical operations. The total number of iterations would be A + B + C, which is at most 300. Even though this is already small, it reveals the underlying structure: every iteration does exactly the same work, adding D.

Once we recognize that each hour contributes independently and uniformly, we can collapse the simulation into a single arithmetic expression. Instead of iterating, we compute the total time first and multiply once by D. This reduces the entire computation to constant time.

The key observation is linearity: the complaint generation process is additive over time and uniform per unit hour. This allows aggregation of all time intervals before applying the rate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(A + B + C) | O(1) | Accepted |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We want to compute total complaints generated across all disturbances.

1. Read four integers A, B, C, and D from input. These represent three independent durations and a uniform complaint rate per hour.
2. Compute the total time spent in the sea disturbances by summing the three durations: total_time = A + B + C. This aggregation works because each incident contributes independently to the total complaint count.
3. Multiply the total time by D to obtain the final number of complaints: answer = total_time × D. This step applies the uniform per-hour cost to the combined duration.
4. Output the computed result.

### Why it works

Each hour of activity is indistinguishable in terms of its contribution to complaints. Since the rate D is constant across all hours and all incidents, the total complaint count depends only on the total number of hours spent. Because addition distributes over multiplication, (A × D) + (B × D) + (C × D) is exactly equal to (A + B + C) × D, which guarantees the correctness of aggregating first and multiplying once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    A, B, C, D = map(int, input().split())
    total_time = A + B + C
    print(total_time * D)

if __name__ == "__main__":
    main()
```

The implementation directly follows the derived formula. The input is read in one line and unpacked into four integers. The sum of A, B, and C is stored explicitly to make the structure of the computation clear, and then multiplied by D.

Using an intermediate variable for total_time is not required for correctness, but it reduces the chance of misreading the expression and mirrors the logical decomposition used in the derivation.

All arithmetic is done using Python integers, which safely handle the maximum possible value (300 × 100 = 30000).

## Worked Examples

### Example 1

Input:

A = 1, B = 2, C = 3, D = 4

| Step | A | B | C | total_time | D | result |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 1 | 2 | 3 | - | 4 | - |
| Sum durations | 1 | 2 | 3 | 6 | 4 | - |
| Multiply rate | 1 | 2 | 3 | 6 | 4 | 24 |

The total number of hours is 6. Each hour produces 4 complaints, giving 24 complaints overall.

### Example 2

Input:

A = 5, B = 5, C = 5, D = 2

| Step | A | B | C | total_time | D | result |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 5 | 5 | 5 | - | 2 | - |
| Sum durations | 5 | 5 | 5 | 15 | 2 | - |
| Multiply rate | 5 | 5 | 5 | 15 | 2 | 30 |

All three incidents contribute equally. The combined time is 15 hours, and at 2 complaints per hour the result is 30.

These examples confirm that the computation is purely additive over time and linear in the rate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed regardless of input values |
| Space | O(1) | No additional data structures are used |

The constraints are small enough that even a loop-based solution would pass easily, but the constant-time formula is cleaner and avoids unnecessary iteration entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import prod

    A, B, C, D = map(int, sys.stdin.readline().split())
    return str((A + B + C) * D)

# provided sample
assert run("1 2 3 4") == "24", "sample 1"

# minimum values
assert run("1 1 1 1") == "3", "all ones"

# asymmetric case
assert run("10 1 1 2") == "24", "skewed distribution"

# equal durations
assert run("5 5 5 5") == "75", "uniform case"

# max values
assert run("100 100 100 100") == "30000", "boundary max case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 3 | minimum boundary correctness |
| 10 1 1 2 | 24 | uneven distribution handling |
| 100 100 100 100 | 30000 | upper bound safety |

## Edge Cases

### Minimum values

Input:

A = B = C = D = 1

The algorithm computes total_time = 3 and output = 3. There is no special handling required for small values, since the arithmetic expression remains valid even at the lowest bounds.

### Maximum values

Input:

A = B = C = D = 100

Execution:

total_time = 300

result = 300 × 100 = 30000

Even at the upper bound, the multiplication stays well within integer range and no overflow or precision issues arise in Python.

### Uneven distribution

Input:

A = 10, B = 1, C = 1, D = 2

Execution:

total_time = 12

result = 24

This confirms that only the sum matters, not how the hours are distributed across incidents. Each hour contributes identically, so partitioning is irrelevant.
