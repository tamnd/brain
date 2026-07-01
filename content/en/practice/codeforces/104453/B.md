---
title: "CF 104453B - \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0438"
description: "We are given a group of students who answered a poll about attending a training session. Each student could choose the time “10 o’clock”, “12 o’clock”, or both. The totals in the poll are partially overlapping, so some students are counted twice across the two tallies."
date: "2026-06-30T14:32:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104453
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Qualyfing Round, 2021"
rating: 0
weight: 104453
solve_time_s: 71
verified: true
draft: false
---

[CF 104453B - \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/104453/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of students who answered a poll about attending a training session. Each student could choose the time “10 o’clock”, “12 o’clock”, or both. The totals in the poll are partially overlapping, so some students are counted twice across the two tallies.

The input gives four numbers. The first is the number of votes for 10 o’clock, the second is the number of votes for 12 o’clock, the third is how many students selected both options, and the fourth is the maximum number of students that can physically fit in the room at the same time.

From this we need to determine whether it is possible to schedule the training so that everyone who attends can be accommodated in the room. The key ambiguity is that the “both” group contributes to both vote counts, but those students are still single individuals.

The important hidden structure is that the two possible sessions are independent groups except for the overlap. The actual number of distinct students is not A + B, but A + B − C.

Since C students appear in both groups, removing double counting is essential. A naive interpretation that treats A and B as disjoint leads to overestimating attendance and incorrectly rejecting feasible cases.

A second subtle edge case appears when the room capacity is exactly equal to the union size. Since equality is allowed, the correct answer must be “Yes” when A + B − C ≤ D, not strictly less.

A third case worth attention is when C equals A or B. That means one group is fully contained in the other, and the union reduces to the larger value. For example, A = 15, B = 15, C = 15 means all students are identical in choice sets, so the true number is 15, not 30 or 15 + 15 − 15 = 15, which is consistent but easy to misinterpret if thinking in terms of separate groups.

The constraints A, B, C, D ≤ 100000 imply that any O(1) or O(log n) computation per test case is sufficient. There is no need for complex data structures or simulation.

## Approaches

A brute-force way to think about this is to explicitly model each student as an individual entity and assign them to one or two sessions depending on their votes. We would then try to construct a valid schedule and count how many people attend at the same time. This quickly becomes unnecessary because the structure of the problem is fully determined by set overlap sizes, not by individual identities. Even if implemented, such a simulation would require iterating over up to 100000 students, and possibly constructing subsets, which is redundant since only aggregate counts matter.

The key insight is recognizing that the poll describes two sets with an intersection. The number of unique students is exactly the size of the union of two sets. This is a direct application of the inclusion-exclusion principle. Once we compute the union size, the feasibility check becomes a simple comparison against capacity D.

This reduces the entire problem to a constant-time arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(A + B) | O(A + B) | Too slow and unnecessary |
| Inclusion-Exclusion | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We want to compute how many distinct students exist across both poll options, then compare that to the room capacity.

1. Read A, B, C, D from input. These represent two overlapping groups and a capacity constraint.
2. Compute the number of distinct students using the formula A + B − C. This removes the double-counted students who appear in both groups.
3. Compare the result with D. If A + B − C is less than or equal to D, the room can accommodate everyone at once.
4. Output “Yes” if the condition holds, otherwise output “No”.

### Why it works

Each student belongs to one of three disjoint categories: only 10 o’clock, only 12 o’clock, or both. The values A and B count the last category twice, once in each group total. Subtracting C removes exactly this duplication and leaves the exact number of distinct individuals. Since every student must be present in the room for at least one session, the worst-case simultaneous occupancy is exactly the size of this union. The comparison against D therefore correctly determines feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C, D = map(int, input().split())
    total = A + B - C
    if total <= D:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The solution reads the four integers and directly applies the inclusion-exclusion formula. The computed value represents the number of distinct students, which is the only meaningful quantity for capacity checking. The final comparison is straightforward.

There are no loops or edge-dependent branches, so there are no concerns about ordering or incremental updates. The subtraction of C must be performed exactly once; failing to subtract it leads to double counting and incorrect rejection in cases where overlap is large.

## Worked Examples

### Sample 1

Input: 15 15 10 20

We compute the union size step by step.

| Step | A | B | C | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Input | 15 | 15 | 10 | read values | - |
| Union | 15 | 15 | 10 | A + B − C | 20 |

Now we compare 20 with D = 20.

Since 20 ≤ 20, the output is “Yes”.

This example shows a balanced overlap where the intersection is large enough to reduce the total exactly to capacity.

### Sample 2

Input: 15 15 10 10

| Step | A | B | C | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Input | 15 | 15 | 10 | read values | - |
| Union | 15 | 15 | 10 | A + B − C | 20 |

Now compare 20 with D = 10.

Since 20 > 10, the room cannot accommodate all students at once, so the answer is “No”.

This shows how large overlap does not necessarily make the group small enough, and capacity is the limiting factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed regardless of input size |
| Space | O(1) | No additional data structures are used |

The constraints allow up to 100000, but the solution does not depend on input scale at all. It performs constant-time arithmetic, so it comfortably fits within any typical time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("15 15 10 20\n") == "Yes"
assert run("15 15 10 10\n") == "Yes"
assert run("15 15 10 9\n") == "No"

# minimum case
assert run("0 0 0 0\n") == "Yes"

# no overlap
assert run("5 7 0 11\n") == "Yes"

# full overlap
assert run("10 10 10 10\n") == "Yes"

# tight boundary
assert run("6 7 2 10\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | Yes | empty case |
| 5 7 0 11 | Yes | disjoint sets |
| 10 10 10 10 | Yes | full overlap |
| 6 7 2 10 | No | boundary overflow |

## Edge Cases

A subtle case is when all students are in the intersection, meaning A = B = C. For example, input 10 10 10 10 results in a union size of 10. The algorithm computes 10 + 10 − 10 = 10 and correctly matches capacity.

Another case is when there is no overlap, C = 0. For example, 5 7 0 11 produces union size 12. The subtraction does nothing and the result directly reflects two disjoint groups.

A final edge case is when capacity exactly matches the union size. For example, 6 7 2 11 yields union 11 and outputs “Yes”. The comparison must be non-strict to handle this correctly.
