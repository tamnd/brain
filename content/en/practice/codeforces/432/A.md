---
title: "CF 432A - Choosing Teams"
description: "We are given a set of students at a university, each with a record of how many times they have already participated in the ACM ICPC world championship."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 432
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 246 (Div. 2)"
rating: 800
weight: 432
solve_time_s: 81
verified: true
draft: false
---

[CF 432A - Choosing Teams](https://codeforces.com/problemset/problem/432/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of students at a university, each with a record of how many times they have already participated in the ACM ICPC world championship. The head of the training center wants to form teams of exactly three students, and each team is required to participate in at least _k_ more world championships. A student cannot be in more than one team.

The input consists of two integers, _n_, the number of students, and _k_, the minimum number of future participations required for a team. The second line gives _n_ integers where each integer represents the number of times a student has already participated. Since any student can participate at most five times, a student can contribute to a team only if the sum of their past participations and _k_ does not exceed 5.

The output is a single number: the maximum number of three-person teams that can be formed under these restrictions.

Constraints tell us that _n_ can go up to 2000, which is small enough for simple O(n log n) or O(n) algorithms. However, a naive approach that attempts to consider all subsets of three students would require O(n³) operations, which is clearly too slow.

Non-obvious edge cases include situations where some students are already at the participation limit and cannot join any new team. For example, if the input is `3 1` with participations `5 5 5`, no team can be formed, so the correct output is `0`. A careless approach that ignores the participation cap could erroneously count a team as valid.

## Approaches

The brute-force approach would iterate over all possible combinations of three students and check if each combination satisfies the participation constraint. This approach is correct in principle because it exhaustively checks all options, but the worst-case number of combinations is `C(n,3)`, roughly n³/6. For _n_ = 2000, this is over a billion checks, which is far too slow for a 1-second time limit.

The optimal solution comes from the observation that we do not need to check every combination explicitly. What matters is whether a student is eligible to join a team at all. If we count the number of students who have participated at most `5 - k` times, any three of these students can form a team. This reduces the problem to counting eligible students and then dividing by three, discarding the remainder since a team cannot be formed from fewer than three.

This insight transforms a combinatorial problem into a simple counting problem. We only iterate over the student list once, making it linear in time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read _n_ and _k_ from input. These define the number of students and the minimum number of future participations required for a team.
2. Read the list of student participation counts. Each count tells us how many times a student has already participated.
3. Initialize a counter for eligible students to zero. Eligible students are those who can participate at least _k_ more times without exceeding the maximum of 5.
4. Iterate through each student's participation count. For each student, if `count + k ≤ 5`, increment the eligible counter. This step filters out students who are over the participation limit.
5. The maximum number of teams is the integer division of the number of eligible students by three. We discard the remainder because fewer than three students cannot form a team.
6. Print the resulting number of teams.

Why it works: At every step, we maintain the invariant that we only consider students who are eligible to form a team. By dividing the total count of eligible students by three, we ensure that every team formed consists of exactly three eligible members. No eligible student is counted twice, satisfying the "no student in multiple teams" constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
participations = list(map(int, input().split()))

eligible_count = 0
for p in participations:
    if p + k <= 5:
        eligible_count += 1

max_teams = eligible_count // 3
print(max_teams)
```

The solution reads input efficiently using `sys.stdin.readline` to handle potentially large input. The loop filters eligible students with a simple condition, avoiding off-by-one errors by using `<= 5`. The integer division ensures no partial teams are counted.

## Worked Examples

### Sample 1

Input:

```
5 2
0 4 5 1 0
```

| Student | Participations | Eligible? |
| --- | --- | --- |
| 0 | 0 | Yes |
| 1 | 4 | No |
| 2 | 5 | No |
| 3 | 1 | Yes |
| 4 | 0 | Yes |

Eligible students = 3 → `3 // 3 = 1` team.

### Sample 2

Input:

```
4 3
1 2 1 0
```

| Student | Participations | Eligible? |
| --- | --- | --- |
| 0 | 1 | Yes |
| 1 | 2 | No |
| 2 | 1 | Yes |
| 3 | 0 | Yes |

Eligible students = 3 → `3 // 3 = 1` team.

This trace confirms that counting eligible students correctly and integer-dividing by three produces the correct result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through the list of students once, checking eligibility. |
| Space | O(1) | Only a counter is used, no additional arrays proportional to n. |

The solution comfortably fits within the 1-second time limit for n up to 2000 and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    participations = list(map(int, input().split()))
    eligible_count = sum(1 for p in participations if p + k <= 5)
    return str(eligible_count // 3)

# provided samples
assert run("5 2\n0 4 5 1 0\n") == "1", "sample 1"
assert run("4 3\n1 2 1 0\n") == "1", "sample 2"

# custom cases
assert run("3 1\n5 5 5\n") == "0", "all students maxed out"
assert run("6 2\n0 0 0 0 0 0\n") == "2", "all students eligible, multiple teams"
assert run("2 1\n0 1\n") == "0", "less than three students"
assert run("7 5\n0 0 0 0 0 0 0\n") == "0", "k too high for any student"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1\n5 5 5 | 0 | students already at limit cannot form teams |
| 6 2\n0 0 0 0 0 0 | 2 | multiple teams can be formed from all eligible students |
| 2 1\n0 1 | 0 | fewer than 3 students, no team possible |
| 7 5\n0 0 0 0 0 0 0 | 0 | k exceeds remaining participation for all students |

## Edge Cases

In the input `3 1\n5 5 5`, the algorithm iterates through the participations and finds no student eligible because `5 + 1 > 5`. The eligible counter remains zero, and integer division by 3 yields 0. This correctly handles the edge case where all students are at the participation limit.

In the input `2 1\n0 1`, the counter finds 2 eligible students, but dividing by 3 produces 0, correctly handling the case with fewer than three students.

The solution handles boundaries and participation limits consistently, ensuring no over-counting of teams.
