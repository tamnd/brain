---
title: "CF 103411A - \u0414\u0438\u0441\u0442\u0430\u043d\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u0435"
description: "We are organizing online classes using a fixed number of video conferences. Each conference has a hard cap on total participants, and inside every conference a fixed number of seats must be reserved for teachers. The remaining seats, if any, can be filled by students."
date: "2026-07-03T10:55:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103411
codeforces_index: "A"
codeforces_contest_name: "2020-2021, ICPC, East Siberian Regional Contest"
rating: 0
weight: 103411
solve_time_s: 44
verified: true
draft: false
---

[CF 103411A - \u0414\u0438\u0441\u0442\u0430\u043d\u0446\u0438\u043e\u043d\u043d\u043e\u0435 \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/103411/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are organizing online classes using a fixed number of video conferences. Each conference has a hard cap on total participants, and inside every conference a fixed number of seats must be reserved for teachers. The remaining seats, if any, can be filled by students. A student is allowed to attend at most one conference, so we cannot reuse students across sessions.

The task is to determine how many students can be accommodated in total across all available conferences under these constraints.

The input gives the number of conferences available, the maximum capacity of each conference, and how many of those slots are already reserved for teachers. The output is the total number of student slots across all conferences.

The constraints are small: up to 1000 conferences, and each conference supports at most 100 participants. This immediately suggests that any solution running in linear time over these values is sufficient, since even a direct computation involves at most a few thousand arithmetic operations.

A naive mistake comes from misinterpreting whether students are distributed independently or globally constrained. The key constraint is that each conference independently reserves teacher slots, so student capacity is per conference, not shared.

Another potential pitfall is forgetting that teacher slots reduce student capacity even if the conference is not fully utilized. For example, if there are 10 conferences, each with capacity 10 and 9 teachers, then only 1 student fits per conference, giving 10 total students, not 100.

## Approaches

A brute-force interpretation would simulate assigning students conference by conference, filling teacher slots first and then adding students until either the conference is full or students run out. This would require tracking each conference and potentially iterating through students one by one. While correct, this is unnecessary overhead since the structure is uniform.

The crucial observation is that every conference is identical in structure: each one always contributes exactly `n - c` student slots, independent of the others. There is no interaction between conferences except the global count of available conferences `k`.

This collapses the problem into a simple multiplication: each conference contributes a fixed number of student seats, and we have `k` such conferences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute simulation | O(k · n) | O(1) | Accepted but unnecessary |
| Direct formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of conferences `k`, the maximum capacity `n`, and the number of teachers `c`. These define how many student slots exist per conference and how many conferences are available.
2. Compute the number of student slots in a single conference as `n - c`. This reflects the fact that teacher seats are mandatory and occupy part of the capacity before students can be placed.
3. Multiply the per-conference student capacity by `k`. This aggregates identical independent conferences into a single total.
4. Output the result as the maximum number of students that can be accommodated.

### Why it works

Each conference operates independently and has identical structure. Since every conference always reserves exactly `c` teacher slots, the remaining capacity for students is fixed at `n - c`. There is no coupling between conferences, so maximizing students globally reduces to maximizing them locally and summing across all conferences. Any deviation from `n - c` per conference would violate either the teacher requirement or the capacity constraint, so this value is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())
n = int(input())
c = int(input())

print(k * (n - c))
```

The solution reads three integers and directly applies the derived formula. The multiplication captures aggregation across all conferences. The subtraction ensures that teacher reservations are excluded from student capacity.

There are no boundary conditions beyond ensuring `c < n`, which guarantees the result is always positive.

## Worked Examples

Consider an input where there are 3 conferences, each allowing 5 participants, with 2 reserved for teachers.

| k | n | c | students per conference | total students |
| --- | --- | --- | --- | --- |
| 3 | 5 | 2 | 3 | 9 |

Each conference contributes 3 student slots, so across 3 conferences we get 9 students.

Now consider a second case with a single large conference.

| k | n | c | students per conference | total students |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1 | 9 | 9 |

Here the result is directly the available student capacity in one conference.

These examples confirm that the computation is purely additive across identical independent units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to 1000 conferences, but the solution does not iterate over them. Instead, it uses constant-time arithmetic, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(sys.stdin.readline())
    n = int(sys.stdin.readline())
    c = int(sys.stdin.readline())
    return str(k * (n - c))

# provided sample-style checks
assert run("3\n5\n2\n") == "9"
assert run("1\n10\n1\n") == "9"

# custom cases
assert run("1\n2\n1\n") == "1", "minimum student capacity"
assert run("1000\n100\n1\n") == str(1000 * 99), "maximum k and near-maximum n"
assert run("5\n10\n9\n") == "5", "only one student per conference"
assert run("10\n100\n0\n") == "1000", "no teachers edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,2,1 | 1 | minimal non-zero capacity |
| 1000,100,1 | 99000 | large-scale multiplication |
| 5,10,9 | 5 | extreme teacher dominance |
| 10,100,0 | 1000 | absence of teachers |

## Edge Cases

One edge case is when the number of teachers is just one less than capacity. For input `k=5, n=10, c=9`, each conference only allows one student. The algorithm computes `10 - 9 = 1`, then multiplies by 5, yielding 5. This matches the intended constraint that teacher slots are mandatory and always consume capacity before students.

Another case is when there are no teachers, conceptually `c = 0` (even though the problem states `c ≥ 1`, this is useful to reason about correctness). For `k=10, n=100, c=0`, each conference fully contributes 100 student slots, and the algorithm returns `1000`, correctly treating all capacity as available for students.

A final boundary situation is the smallest configuration `k=1, n=2, c=1`. Only one student can be placed, and the formula gives `1`, matching the expected outcome without requiring any special handling.
