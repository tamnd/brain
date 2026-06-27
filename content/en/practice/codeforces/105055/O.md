---
title: "CF 105055O - Another Trip"
description: "The situation is a simple road trip with a mistake in direction. Two distances are relevant: the first is how far the travelers went after taking the wrong direction, and the second is the remaining distance from their starting point to the destination along the correct route."
date: "2026-06-28T00:27:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "O"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 53
verified: true
draft: false
---

[CF 105055O - Another Trip](https://codeforces.com/problemset/problem/105055/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The situation is a simple road trip with a mistake in direction. Two distances are relevant: the first is how far the travelers went after taking the wrong direction, and the second is the remaining distance from their starting point to the destination along the correct route.

After realizing the mistake, they effectively undo part of their journey by turning around, then continue along the correct path. The total distance they actually travel is the sum of the wrong-direction segment and the corrected route to the destination.

So the task reduces to computing how many kilometers are traveled in total when combining the detour and the final correct trip.

The input provides two integers, A and B. A is the distance traveled in the wrong direction before turning around. B is the correct distance from the start to the destination. The output is the total distance traveled, including both the wrong path and the correct route.

The constraints are small, with each value up to 10^6. This immediately rules out any need for advanced data structures or optimization. A constant-time arithmetic expression is sufficient.

There are no subtle edge cases involving ordering, parity, or structure. The only meaningful edge case is when A or B equals 1, but even then the computation remains a direct arithmetic sum. The key is understanding that the wrong-direction segment is not canceled out, it is physically traveled twice: once going forward incorrectly, and once returning to the correct path.

## Approaches

A brute-force interpretation would simulate the journey step by step. One could imagine moving A kilometers forward in the wrong direction, then A kilometers back to the starting point, and finally B kilometers toward the destination. This produces a total travel distance of A + A + B. While this is conceptually valid, it introduces unnecessary simulation.

The structure of the problem makes the simulation redundant. The wrong direction travel is exactly mirrored when turning around, meaning the detour contributes twice its length to the final distance. The correct path is then added once. This collapses the process into a direct formula without any iteration.

The key observation is that the journey consists of three linear segments whose lengths are fully determined by the input values. There is no dependency between steps that would require simulation or state tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(A + B) | O(1) | Too slow conceptually, unnecessary |
| Direct Formula (2A + B) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer A representing the distance traveled in the wrong direction. This segment will be traversed twice in total, once forward and once when returning.
2. Read the integer B representing the correct distance from the starting point to the destination. This segment is traversed exactly once at the end of the trip.
3. Compute the total distance as 2 × A + B. The factor of two accounts for the round trip caused by the mistaken direction.
4. Output the computed value directly.

### Why it works

The travel path decomposes into three disjoint segments: an initial forward mistake of length A, a return of length A, and a final correct traversal of length B. These segments are independent and sequential, so total distance is additive. There is no overlap or cancellation because distance measures physical travel, not net displacement. This guarantees that summing the segment lengths produces the exact total distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input().strip())
b = int(input().strip())

print(2 * a + b)
```

The solution reads two integers and applies the derived expression directly. The use of `strip()` ensures safe parsing even if trailing newlines are present. The multiplication is done before addition in a single expression, avoiding intermediate variables but keeping the logic explicit.

The only subtle point is recognizing that the wrong-direction travel is not discarded but counted twice. This is encoded directly in `2 * a`.

## Worked Examples

### Sample 1

Input:

```
A = 4
B = 2
```

| Step | A | B | Computation | Result |
| --- | --- | --- | --- | --- |
| Read input | 4 | 2 | - | - |
| Apply formula | 4 | 2 | 2×4 + 2 | 10 |

The journey goes 4 km in the wrong direction, returns 4 km, then proceeds 2 km correctly. The table confirms the decomposition into three segments.

### Sample 2

Input:

```
A = 5
B = 7
```

| Step | A | B | Computation | Result |
| --- | --- | --- | --- | --- |
| Read input | 5 | 7 | - | - |
| Apply formula | 5 | 7 | 2×5 + 7 | 17 |

This case shows that when the correct path is longer, the structure still holds. The detour contribution remains independent of B.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two arithmetic operations are performed |
| Space | O(1) | No auxiliary storage beyond input variables |

The constraints allow up to 10^6, but the computation does not depend on input size at all. The solution runs instantly within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = int(input().strip())
    b = int(input().strip())
    return str(2 * a + b)

# provided samples
assert run("4\n2\n") == "10", "sample 1"
assert run("5\n7\n") == "17", "sample 2"
assert run("2\n4\n") == "8", "sample 3"

# minimum values
assert run("1\n1\n") == "3", "min case"

# asymmetric small values
assert run("1\n10\n") == "12", "small A, large B"

# large values
assert run("1000000\n1000000\n") == "3000000", "max case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | 3 | minimum boundary correctness |
| 1, 10 | 12 | imbalance between segments |
| 10^6, 10^6 | 3×10^6 | overflow-safe arithmetic |

## Edge Cases

The smallest possible input occurs when both distances are 1. In that case, the traveler goes 1 km wrong, returns 1 km, then proceeds 1 km correctly, totaling 3. The formula 2A + B correctly produces 3, confirming that even minimal paths preserve the structure.

When A is large and B is small, such as A = 10^6 and B = 1, the detour dominates the result. The computation still reduces to a single expression, and no overflow issues arise in Python due to arbitrary precision integers.

When B is large and A is minimal, the detour becomes negligible relative to the final segment, but it still contributes exactly twice its value. This confirms that the detour is independent of the final route length, and the additive decomposition remains valid in all regimes.
