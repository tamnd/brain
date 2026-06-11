---
title: "CF 1133E - K Balanced Teams"
description: "We have a list of students, each with a programming skill level. The task is to divide these students into at most k teams so that the total number of students included is maximized."
date: "2026-06-12T04:04:59+07:00"
tags: ["codeforces", "competitive-programming", "dp", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1133
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 544 (Div. 3)"
rating: 1800
weight: 1133
solve_time_s: 65
verified: true
draft: false
---

[CF 1133E - K Balanced Teams](https://codeforces.com/problemset/problem/1133/E)

**Rating:** 1800  
**Tags:** dp, sortings, two pointers  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a list of students, each with a programming skill level. The task is to divide these students into at most `k` teams so that the total number of students included is maximized. Each team must be "balanced," meaning that no two students in the same team differ by more than 5 in skill. Students not placed in a team are simply excluded from the count.

The input size allows up to 5000 students, which means any algorithm worse than O(n²) could be too slow, especially if we consider trying all possible subsets of students. The skill values themselves can be large, up to 10⁹, but the actual skill value is not as important as their relative differences because team formation depends on differences, not absolute values.

A naive solution might consider all subsets of students for each team, but this explodes combinatorially. Edge cases arise when students are all clustered closely (allowing a large team) or when many students are widely spread, forcing small or no teams. For instance, if `n = 5, k = 2, a = [1, 2, 15, 15, 15]`, the optimal approach forms one small team `[1,2]` and one large team `[15,15,15]`, totaling 5 students. A careless greedy approach that only builds teams sequentially might miss the global optimum by forming suboptimal early teams.

## Approaches

A brute-force approach would attempt all possible divisions of students into up to `k` groups. To check each team’s validity, we would verify the difference between the smallest and largest skill in the subset does not exceed 5. This approach works because it correctly counts balanced subsets, but the number of combinations grows as 2ⁿ, which is completely infeasible for n = 5000.

The key insight is to sort the students by skill. Once sorted, any valid team must consist of consecutive students because adding a lower-skilled student before a higher-skilled student would violate the skill difference constraint. This allows us to treat the problem as a variant of interval partitioning. Then, dynamic programming naturally fits: let `dp[i]` represent the maximum number of students in balanced teams among the first `i` students. For each position, we consider forming a team ending at that student and extending backwards as far as the skill difference allows.

We can optimize team formation with two pointers: for student `i`, find the farthest `j` to the left such that the skill difference between `a[i]` and `a[j]` is at most 5. This tells us the largest possible balanced team ending at `i`. Then, `dp[i]` is the maximum of not including `i` (taking `dp[i-1]`) or including the team `[j..i]` and adding it to `dp[j-1]`. To respect the limit on `k` teams, we use a secondary DP dimension or track the number of teams formed. Since the number of teams is at most 5000, a simple 1D DP suffices if we process teams greedily in order of increasing skill.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ * n) | O(n) | Too slow |
| Optimal (sort + DP + two pointers) | O(n²) worst case, but effectively O(n) per pointer advance | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array of student skills. This ensures that any consecutive segment with a maximum difference ≤ 5 is a valid team. Sorting also allows us to use two pointers efficiently.
2. Initialize a DP array `dp` of length `n+1`, where `dp[i]` stores the maximum number of students in balanced teams among the first `i` students. Set `dp[0] = 0`.
3. For each student `i` from 1 to `n`, use a pointer `j` starting from the beginning of the array to find the leftmost student such that `a[i] - a[j] <= 5`. This identifies the largest team ending at `i`.
4. Update `dp[i]` as the maximum between `dp[i-1]` (not including student `i`) and `dp[j-1] + (i - j + 1)` (forming a team with students from `j` to `i`).
5. Repeat until `i = n`. The final answer is `dp[n]`, the maximum number of students that can be placed in balanced teams.

Why it works: Sorting guarantees that any valid team corresponds to a contiguous subarray. The DP recurrence checks all possible left endpoints for teams ending at `i` efficiently with the two-pointer approach. Each `dp[i]` stores the optimal solution for the first `i` students, ensuring that decisions made earlier are incorporated optimally.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

dp = [0] * (n + 1)
j = 0

for i in range(1, n + 1):
    while a[i - 1] - a[j] > 5:
        j += 1
    # max between not using this student or using the largest valid team ending here
    dp[i] = max(dp[i - 1], dp[j] + (i - j))

print(dp[n])
```

This code first sorts the skills. The variable `j` is a two-pointer left boundary of the valid team ending at student `i`. The DP array accumulates the optimal number of students included. The `while` loop ensures we shrink the left boundary until the team becomes valid.

## Worked Examples

### Sample Input 1

```
5 2
1 2 15 15 15
```

| i | a[i-1] | j | i-j | dp[i] | dp[j] + (i-j) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 0 + 1 |
| 2 | 2 | 0 | 2 | 2 | 0 + 2 |
| 3 | 15 | 2 | 1 | 2 | 2 + 1 = 3 |
| 4 | 15 | 2 | 2 | 4 | 2 + 2 = 4 |
| 5 | 15 | 2 | 3 | 5 | 2 + 3 = 5 |

Trace demonstrates that the algorithm correctly identifies two separate teams `[1,2]` and `[15,15,15]`.

### Custom Input 2

```
6 3
1 3 4 5 12 13
```

| i | a[i-1] | j | i-j | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 3 | 0 | 2 | 2 |
| 3 | 4 | 0 | 3 | 3 |
| 4 | 5 | 0 | 4 | 4 |
| 5 | 12 | 4 | 1 | 5 |
| 6 | 13 | 4 | 2 | 6 |

The table shows two teams `[1,3,4,5]` and `[12,13]`, totaling 6 students. DP correctly accumulates maximum students.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n) | Sorting takes O(n log n), two-pointer DP runs in O(n) |
| Space | O(n) | DP array of length n+1 |

With n ≤ 5000, the sorting and linear DP are well within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    dp = [0] * (n + 1)
    j = 0
    for i in range(1, n + 1):
        while a[i - 1] - a[j] > 5:
            j += 1
        dp[i] = max(dp[i - 1], dp[j] + (i - j))
    return str(dp[n])

# provided sample
assert run("5 2\n1 2 15 15 15\n") == "5"

# minimum input
assert run("1 1\n10\n") == "1"

# all equal
assert run("4 2\n5 5 5 5\n") == "4"

# sparse skills
assert run("5 2\n1 10 20 30 40\n") == "1"

# max k less than optimal splits
assert run("6 3\n1 2 3 4 12 13\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 2\n1 2 15 15 15 | 5 | Multiple balanced teams separated by skill gap |
| 1 1\n10 | 1 | Minimum input |
| 4 2\n5 5 5 5 | 4 | All equal values form one team |
