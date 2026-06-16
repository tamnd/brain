---
title: "CF 991A - If at first you don't succeed..."
description: "We are given summary statistics about how students in a group behaved after an exam. Every student belongs to exactly one of four categories: they either visited only BugDonalds, only BeaverKing, both restaurants, or stayed at home because they failed the exam."
date: "2026-06-17T00:27:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 991
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 491 (Div. 2)"
rating: 1000
weight: 991
solve_time_s: 74
verified: true
draft: false
---

[CF 991A - If at first you don't succeed...](https://codeforces.com/problemset/problem/991/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given summary statistics about how students in a group behaved after an exam. Every student belongs to exactly one of four categories: they either visited only BugDonalds, only BeaverKing, both restaurants, or stayed at home because they failed the exam.

From the input, we are told how many students visited BugDonalds in total, how many visited BeaverKing in total, how many visited both places, and the total number of students in the group. The task is to check whether these statistics can come from some valid distribution of students, and if they can, compute how many students failed the exam and stayed at home.

The key hidden structure is that the restaurant counts are not disjoint. The value representing “both restaurants” is counted inside both totals, so the actual number of distinct visitors must be reconstructed carefully. Once we know how many students visited at least one restaurant, everyone else must be the ones who stayed home.

The constraints are tiny, all values are at most 100, which immediately tells us that any solution running in constant time per test case is sufficient. Even a brute-force enumeration over all distributions of four categories bounded by 100 would be feasible, but unnecessary.

The subtle failure cases come from inconsistencies between overlap and totals. One common mistake is forgetting that the overlap is included in both A and B, leading to impossible negative counts or overcounting.

A few concrete invalid scenarios help clarify:

If A = 1, B = 1, C = 1, N = 1, then both A and B already imply at least one student exists in each restaurant, but the overlap forces a contradiction because a single student cannot simultaneously satisfy all counts unless carefully aligned.

If C is greater than either A or B, such as A = 2, B = 2, C = 3, this is immediately impossible because “both” cannot exceed “either total”.

If A + B − C exceeds N, then even before accounting for overlap, we already need more students than exist in the group.

These inconsistencies are what the algorithm must detect.

## Approaches

A brute-force interpretation would try to assign each of the N students to one of four states and check whether we can match the required counts A, B, and C exactly. This would involve iterating over all possible splits of N into four groups and verifying constraints. The number of ways to partition N into four non-negative integers is on the order of N³, since fixing three automatically determines the fourth. Even though N ≤ 100 makes this barely acceptable, it is unnecessary complexity for what is fundamentally a direct arithmetic reconstruction problem.

The key observation is that the overlap structure completely determines the partition. Let x be only BugDonalds, y only BeaverKing, z both restaurants, and w stayed home. Then A = x + z, B = y + z, and C = z. This immediately gives x = A − C and y = B − C. Once these are fixed, the total number of students who visited at least one restaurant is x + y + z = A + B − C. The remaining students are w = N − (A + B − C).

The entire problem reduces to checking whether these derived values are all non-negative integers and whether they sum consistently to N. Any violation signals impossible input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N³) | O(1) | Too slow / unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reconstruct the four categories from the given totals using algebra and then validate feasibility.

1. Compute the number of students who visited both restaurants, denoted z = C. This is directly given, so no inference is needed.
2. Compute x = A − C, the number of students who visited only BugDonalds. This removes those counted in both from the total BugDonalds visitors.
3. Compute y = B − C, the number of students who visited only BeaverKing. This is symmetric reasoning applied to the second restaurant.
4. Compute the number of students who visited at least one restaurant as x + y + z. This simplifies to A + B − C, since z cancels correctly.
5. Compute the number of students who stayed home as w = N − (A + B − C). This represents those who failed the exam.
6. Check validity conditions: x, y, z, and w must all be non-negative. If any is negative, the counts contradict reality and we output −1.
7. If valid, output w as the number of students who failed.

Why it works: the decomposition into four disjoint groups is forced by inclusion-exclusion. Every student is uniquely classified, and the formulas are the only way to satisfy both restaurant totals simultaneously. Any violation of non-negativity corresponds to an impossible overlap structure or a mismatch between total group size and reconstructed participation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C, N = map(int, input().split())

    x = A - C
    y = B - C
    z = C

    if x < 0 or y < 0:
        print(-1)
        return

    total_attended = x + y + z  # equals A + B - C
    w = N - total_attended

    if w < 0:
        print(-1)
        return

    print(w)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reconstructed variables. The only subtle point is ensuring that subtraction does not silently produce invalid negative counts. We explicitly guard x and y before proceeding, since they represent physical student counts and cannot be negative. The final check ensures that the reconstructed attending students do not exceed the group size.

## Worked Examples

### Example 1

Input:

A = 10, B = 10, C = 5, N = 20

We compute:

| Step | x | y | z | total_attended | w |
| --- | --- | --- | --- | --- | --- |
| Start | - | - | - | - | - |
| Compute overlap | - | - | 5 | - | - |
| Only BugDonalds | 10−5 = 5 | - | 5 | - | - |
| Only BeaverKing | 5 | 10−5 = 5 | 5 | - | - |
| Total visited | 5 | 5 | 5 | 15 | - |
| Home | 5 | 5 | 5 | 15 | 20−15 = 5 |

The result is valid because all reconstructed groups are non-negative and the total matches the group size. The output is 5, meaning five students stayed home.

### Example 2

Input:

A = 2, B = 2, C = 2, N = 3

| Step | x | y | z | total_attended | w |
| --- | --- | --- | --- | --- | --- |
| Overlap | - | - | 2 | - | - |
| Only BugDonalds | 2−2 = 0 | - | 2 | - | - |
| Only BeaverKing | 0 | 2−2 = 0 | 2 | - | - |
| Total visited | 0 | 0 | 2 | 2 | - |
| Home | 0 | 0 | 2 | 2 | 3−2 = 1 |

This is valid and yields one student at home. If instead N were 1, we would get a negative w, immediately proving inconsistency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow any constant-time arithmetic solution, and this reconstruction fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A, B, C, N = map(int, sys.stdin.readline().split())

    x = A - C
    y = B - C
    z = C

    if x < 0 or y < 0:
        return "-1"

    total_attended = x + y + z
    w = N - total_attended

    if w < 0:
        return "-1"

    return str(w)

# provided sample
assert run("10 10 5 20\n") == "5"

# all stayed home
assert run("0 0 0 5\n") == "5"

# impossible overlap
assert run("2 2 3 5\n") == "-1"

# impossible due to group size
assert run("10 10 0 5\n") == "-1"

# exact full attendance
assert run("3 3 3 3\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 5 | 5 | all students failed |
| 2 2 3 5 | -1 | invalid overlap (C > A,B) |
| 10 10 0 5 | -1 | attendance exceeds group size |
| 3 3 3 3 | 0 | everyone attended, no one at home |

## Edge Cases

When A, B, and C are all zero with a positive N, the algorithm computes x = 0, y = 0, z = 0 and total_attended = 0, so w = N. This corresponds to all students staying home, which is valid and handled correctly because no negative checks trigger.

When C exceeds either A or B, such as A = 2, B = 1, C = 3, the computation produces x = −1 or y = −2. The algorithm immediately rejects this case before computing totals, correctly identifying that an overlap cannot exceed a total category.

When A + B − C exceeds N, such as A = 10, B = 10, C = 0, N = 15, we get total_attended = 20 and w = −5. This negative result directly signals impossibility, reflecting that the reconstructed attendance exceeds the group size.
