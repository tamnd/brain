---
title: "CF 1611B - Team Composition: Programmers and Mathematicians"
description: "We are given two groups of students: programmers and mathematicians. From these students, we want to form as many teams as possible, where every team contains exactly 4 students."
date: "2026-06-10T07:02:20+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1611
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 756 (Div. 3)"
rating: 800
weight: 1611
solve_time_s: 67
verified: true
draft: false
---

[CF 1611B - Team Composition: Programmers and Mathematicians](https://codeforces.com/problemset/problem/1611/B)

**Rating:** 800  
**Tags:** binary search, constructive algorithms, math  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two groups of students: programmers and mathematicians. From these students, we want to form as many teams as possible, where every team contains exactly 4 students.

There is a structural constraint on valid teams: a team is only acceptable if it contains at least one programmer and at least one mathematician. This immediately forbids “pure” teams made entirely of one type, even though they would still satisfy the size requirement.

The task is to maximize the number of disjoint valid teams. Each student can be used at most once, so once a person is assigned to a team, they cannot contribute to another.

The input size is large, with up to 10^4 test cases and values of a and b up to 10^9. This rules out any simulation that iterates over possible teams or individuals. Any approach must reduce each test case to O(1) reasoning.

A naive but important edge case arises when one group is very small. For example, if a = 10 and b = 1, we cannot even form a single valid team requiring both types in quantity, even though the total number of students is 11. A careless approach like floor((a + b) / 4) would incorrectly output 2, ignoring the composition constraint.

Another edge case is when one group is extremely dominant. If a = 100 and b = 1, we still cannot form more than one team because after using the single mathematician, no further valid team can be formed.

The key difficulty is balancing two constraints simultaneously: team size is fixed, but composition requires at least one from each group.

## Approaches

A brute-force way to think about the problem is to try constructing teams one by one. At each step, we pick 4 students and check whether the team contains both types. If not, we discard that selection and try another grouping. This quickly becomes infeasible because even deciding which subset of 4 to pick is combinatorial, and with up to 10^9 students per category, the state space is enormous.

A more structured brute-force is to simulate greedy construction: repeatedly take 1 programmer and 3 mathematicians or 2 and 2 or all valid splits, whichever is possible, until we cannot form a team. This still risks exploring multiple combinations per step and degenerates into linear time in the number of students, which is too slow given up to 10^4 test cases and potentially 10^9 elements per test case.

The key observation is that every team consumes exactly 4 students, and each team must consume at least one programmer and at least one mathematician. This means each team reduces both a and b by at least 1. So the number of teams is bounded above by min(a, b). At the same time, the total number of students bounds teams by (a + b) // 4.

These two constraints are independent and both must hold simultaneously. The maximum number of teams is therefore limited by whichever constraint is tighter: either we run out of one category, or we run out of total students in chunks of four.

The problem reduces to choosing the minimum of these two bottlenecks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(a + b) per test | O(1) | Too slow |
| Direct Formula | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the values a and b. These represent how many students of each type are available.
2. Compute the maximum number of teams limited purely by total students as (a + b) // 4. This assumes every team always uses exactly four people, regardless of type distribution.
3. Compute the maximum number of teams limited by the smaller group as min(a, b). Each team must include at least one student from each category, so after forming k teams, both a and b must still have been reduced by at least k.
4. The final answer is the smaller of these two values, since both constraints must be satisfied simultaneously.

### Why it works

Each valid team consumes at least one programmer and at least one mathematician, so after forming k teams we must have k ≤ a and k ≤ b, implying k ≤ min(a, b). Independently, each team consumes exactly 4 students, so k teams require 4k ≤ a + b, implying k ≤ (a + b) // 4. Any valid construction must respect both inequalities, so the true maximum is the tightest bound among them. Because both bounds are achievable in combination (by mixing team compositions appropriately whenever both sides have enough supply), the minimum of the two is the exact answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        print(min(min(a, b), (a + b) // 4))

if __name__ == "__main__":
    solve()
```

The code processes each test case independently in constant time. The expression min(a, b) captures the requirement that each team must include both types. The expression (a + b) // 4 captures the fixed size constraint of each team.

A subtle point is that we never explicitly construct teams. The reasoning relies entirely on global resource constraints, which avoids any ordering or greedy pitfalls.

## Worked Examples

We trace two cases to see how the formula behaves.

### Example 1: a = 5, b = 5

| Step | a | b | min(a,b) | (a+b)//4 | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | 5 | 5 | 5 | 2 | 2 |

Here the total pool allows at most 2 teams because 10 students form two groups of 4 with 2 left over. Even though both types are abundant, the total size constraint dominates.

This shows that having balanced groups does not automatically increase the answer beyond the packing limit imposed by group size 4.

### Example 2: a = 10, b = 1

| Step | a | b | min(a,b) | (a+b)//4 | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | 10 | 1 | 1 | 2 | 1 |

Here the mathematicians are the bottleneck. Even though there are enough total students for 2 teams, we only have one mathematician, so only one valid team can be formed.

This confirms that the composition constraint is independent of total capacity and can dominate the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with a constant number of arithmetic operations |
| Space | O(1) | No auxiliary structures are used beyond input variables |

The solution easily fits within limits because even for 10^4 test cases, the total work is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b = map(int, input().split())
        out.append(str(min(min(a, b), (a + b) // 4)))
    return "\n".join(out)

# provided samples
assert run("""6
5 5
10 1
2 3
0 0
17 2
1000000000 1000000000
""") == """2
1
1
0
2
500000000"""

# custom cases
assert run("""3
1 1
4 0
3 3
""") == """0
0
1"""

assert run("""2
8 1
7 7
""") == """1
3"""

assert run("""1
0 10
""") == """0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 4 0 / 3 3 | 0 / 0 / 1 | Minimum and extreme imbalance cases |
| 8 1 / 7 7 | 1 / 3 | Bottleneck vs balanced growth |
| 0 10 | 0 | Zero availability edge case |

## Edge Cases

For a = 0 and b = 10, the formula gives min(min(0, 10), 10 // 4) = 0. The algorithm correctly returns 0 because no team can satisfy the requirement of having at least one programmer.

For a = 4 and b = 0, we again get 0. Even though the total size is exactly 4, the absence of the second type prevents forming any valid team, showing that total divisibility alone is insufficient.

For highly imbalanced cases like a = 1000000000 and b = 1, the result becomes 1. The computation (a + b) // 4 would suggest a large number, but the min(a, b) constraint correctly caps it at 1, reflecting that only one valid mixed team is possible before the required diversity is exhausted.
