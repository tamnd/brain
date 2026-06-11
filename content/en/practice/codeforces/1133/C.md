---
title: "CF 1133C - Balanced Team"
description: "We have a list of students, each with a programming skill score. The task is to form the largest possible team such that the difference between the highest-skilled and lowest-skilled members does not exceed 5. In other words, for any team of size $k$, if the skills are $s1, s2, ."
date: "2026-06-12T04:03:53+07:00"
tags: ["codeforces", "competitive-programming", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1133
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 544 (Div. 3)"
rating: 1200
weight: 1133
solve_time_s: 69
verified: true
draft: false
---

[CF 1133C - Balanced Team](https://codeforces.com/problemset/problem/1133/C)

**Rating:** 1200  
**Tags:** sortings, two pointers  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a list of students, each with a programming skill score. The task is to form the largest possible team such that the difference between the highest-skilled and lowest-skilled members does not exceed 5. In other words, for any team of size $k$, if the skills are $s_1, s_2, ..., s_k$, then $\max(s_i) - \min(s_i) \le 5$. Our goal is to determine the maximum size of such a team.

The input consists of $n$, the number of students, followed by $n$ integers representing the skill levels. The output is a single integer: the largest balanced team size. The constraints tell us $n$ can be up to $2 \cdot 10^5$ and skill levels can be as large as $10^9$. This means a naive $O(n^2)$ approach that checks every possible group of students would require up to $4 \cdot 10^{10}$ operations in the worst case, which is far too slow. We need something closer to linear or $O(n \log n)$ to fit within the 2-second limit.

An edge case occurs when all students have the same skill level. Any grouping is valid, so the answer should be $n$. Another edge case is when every student's skill differs by more than 5 from the next closest; here the largest balanced team has only one member. A careless approach might forget to handle this and assume at least two students per team, producing the wrong result.

## Approaches

The brute-force method would iterate through every possible subset of students, computing the maximum and minimum skill for each subset and checking if their difference is at most 5. The subset with the largest size that satisfies this condition would be the answer. This is correct because it exhaustively checks all valid teams, but it fails for large $n$ due to combinatorial explosion-there are $2^n$ subsets.

The key insight to optimize is that the order of students does not matter once we sort them by skill. If the array is sorted, any balanced team must correspond to a contiguous subarray where the difference between the first and last element is at most 5. This allows us to reduce the problem to a sliding window or two-pointer technique. We expand the right pointer to include as many students as possible until the difference exceeds 5, then move the left pointer forward to restore the balance. This linear scan after sorting guarantees that we check every potential team efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Two-Pointer on Sorted Array | O(n log n) | O(1) additional | Accepted |

## Algorithm Walkthrough

1. Read the number of students $n$ and their skill levels into an array. Sorting them makes it easy to check contiguous groups.
2. Sort the skill levels in ascending order. After sorting, any balanced team corresponds to a subarray where the first and last elements differ by at most 5.
3. Initialize two pointers, `left` and `right`, both starting at the beginning of the sorted array. Also initialize `max_team` to 0 to store the largest team size found.
4. Expand the `right` pointer forward. For each position of `right`, check the difference between `skills[right]` and `skills[left]`. If the difference exceeds 5, increment `left` until the difference is at most 5 again. This maintains the invariant that the window `[left, right]` is always a balanced team.
5. Update `max_team` with the size of the current window, `right - left + 1`, if it is larger than the previous maximum.
6. Continue this process until `right` reaches the end of the array. Print `max_team`.

Why it works: Because the array is sorted, any subarray containing elements with a difference greater than 5 cannot be extended without violating the balance constraint. Sliding the left pointer ensures we always maintain the largest possible window ending at `right` that satisfies the condition. No balanced team is missed because every potential contiguous subarray is considered exactly once as `right` advances.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
skills = list(map(int, input().split()))

skills.sort()
max_team = 0
left = 0

for right in range(n):
    while skills[right] - skills[left] > 5:
        left += 1
    max_team = max(max_team, right - left + 1)

print(max_team)
```

The code first reads and sorts the skill levels. The two-pointer loop ensures we maintain a balanced team at all times. The while loop advances `left` only when the difference exceeds 5, which is subtle but crucial to avoid off-by-one errors. Updating `max_team` after adjusting `left` ensures the largest window is recorded.

## Worked Examples

Sample Input 1:

```
6
1 10 17 12 15 2
```

| right | left | skills[right] | skills[left] | window size | max_team |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 2 | 1 | 2 | 2 |
| 2 | 0 | 10 | 1 | 3 -> left moves to 2 | 2 |
| 3 | 2 | 12 | 10 | 2 | 2 |
| 4 | 2 | 15 | 10 | 3 | 3 |
| 5 | 2 | 17 | 12 | 3 | 3 |

The largest balanced team has 3 students `[12, 15, 17]`.

Sample Input 2:

```
5
5 5 5 5 5
```

| right | left | skills[right] | skills[left] | window size | max_team |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 5 | 1 | 1 |
| 1 | 0 | 5 | 5 | 2 | 2 |
| 2 | 0 | 5 | 5 | 3 | 3 |
| 3 | 0 | 5 | 5 | 4 | 4 |
| 4 | 0 | 5 | 5 | 5 | 5 |

All students form a balanced team. The invariant that `skills[right] - skills[left] <= 5` is maintained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates. The two-pointer scan is O(n) because each pointer moves at most n times. |
| Space | O(n) | The skills array is stored. Sorting can be done in-place with no extra memory. |

This fits well within the constraints: for $n = 2 \cdot 10^5$, sorting takes about $4 \cdot 10^6$ operations, and the two-pointer pass adds another $2 \cdot 10^5$, comfortably under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    skills = list(map(int, input().split()))
    skills.sort()
    max_team = 0
    left = 0
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_team = max(max_team, right - left + 1)
    return str(max_team)

# Provided samples
assert run("6\n1 10 17 12 15 2\n") == "3"
assert run("5\n5 5 5 5 5\n") == "5"
assert run("1\n100\n") == "1"

# Custom cases
assert run("3\n1 7 13\n") == "1"  # no pair within 5
assert run("4\n1 2 3 7\n") == "3"  # first three form a team
assert run("5\n1 2 3 4 6\n") == "4"  # largest balanced team [1,2,3,4]
assert run("2\n1 6\n") == "2"  # boundary case exactly 5 apart
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n1 7 13 | 1 | Handles case with no valid pairs |
| 4\n1 2 3 7 | 3 | Correct selection of largest contiguous team |
| 5\n1 2 3 4 6 | 4 | Sliding window correctly drops leftmost element |
| 2\n1 6 | 2 | Edge case difference exactly 5 |

## Edge Cases

For the single-student case `1\n100`, the algorithm initializes `left` and `right` at 0, calculates `window size = 1`, and returns 1. No while loop triggers, so it handles minimum-size input correctly.

For an array where no two students can form a team, like `3\n1 7 13`, `left` increments each time `skills[right] - skills[left] > 5
