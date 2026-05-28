---
title: "CF 44C - Holidays"
description: "We are asked to verify a watering schedule for flowers over a set of consecutive holiday days. Each day must be watered exactly once. The schedule specifies, for each of several people, the range of days they are assigned to water the flowers."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 44
codeforces_index: "C"
codeforces_contest_name: "School Team Contest 2 (Winter Computer School 2010/11)"
rating: 1300
weight: 44
solve_time_s: 84
verified: true
draft: false
---

[CF 44C - Holidays](https://codeforces.com/problemset/problem/44/C)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to verify a watering schedule for flowers over a set of consecutive holiday days. Each day must be watered exactly once. The schedule specifies, for each of several people, the range of days they are assigned to water the flowers. The goal is to detect whether there is any mistake: either a day where no one waters the flowers or a day where multiple people water the flowers. If there is a mistake, we must report the earliest day with the incorrect watering count and how many times the flowers are watered that day. Otherwise, we simply report "OK".

The input consists of two integers, _n_ and _m_, representing the number of days and the number of people. Then follow _m_ pairs of integers indicating the start and end day of each person's watering assignment. Each assignment range is within the total number of days. The constraints are small: _n_ and _m_ are both at most 100. This allows algorithms with time complexity up to O(n·m) to run efficiently within the time limits.

A naive implementation might simply check each day individually and count how many assignments cover it. A subtle edge case arises when two people have consecutive or overlapping ranges. For instance, if two people are assigned [2, 4] and [4, 6], day 4 is covered twice. Another edge case is when there is a gap in the schedule, e.g., assignments [1, 2] and [4, 5], leaving day 3 unwatered. A careless solution that only looks at start or end days could miss these issues.

## Approaches

The brute-force method is straightforward: for each day from 1 to _n_, count how many assignments cover it by iterating through all _m_ people. This works because for each day we check _m_ intervals, resulting in O(n·m) operations. With n and m up to 100, this is at most 10,000 operations, which is acceptable. The drawback is conceptual: we are repeatedly checking overlaps, which is unnecessary if we track watering counts directly.

A more efficient approach uses an array of size _n_, initialized to zeros, to store the number of waterings per day. For each assignment range [a_i, b_i], we increment all days in that range. After processing all assignments, we scan the array to find any day where the value is not 1. This guarantees correctness because we explicitly count waterings per day and allows immediate identification of mistakes. The efficiency is acceptable given the constraints, and the implementation is simpler and less error-prone than repeatedly checking each day individually.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(1) | Accepted |
| Range Count Array | O(n·m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `watered` of length _n_ filled with zeros. Each element will represent the number of times that day is watered. This explicitly models the key invariant: `watered[i]` equals the number of assignments covering day i+1.
2. Iterate over each person's assignment. For each range [a_i, b_i], increment `watered[j]` for all j from a_i-1 to b_i-1 inclusive. The reason for subtracting 1 is to convert 1-based days in the input to 0-based array indices in Python.
3. After all assignments are processed, iterate through `watered` from the first day to the last. For each day, check if the value is exactly 1. If it is, continue. If it is not, this day is the first with a mistake. Print the day number (index+1) and the value in `watered` for that day, then terminate. This ensures we report the minimal day with an incorrect watering count.
4. If the loop completes without finding any incorrect day, print "OK".

This algorithm works because we maintain an invariant: at the end of step 2, `watered[i]` exactly counts how many times day i+1 is scheduled for watering. Step 3 guarantees we detect the first violation of the rule that each day should be watered exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
watered = [0] * n

for _ in range(m):
    a, b = map(int, input().split())
    for day in range(a - 1, b):
        watered[day] += 1

for i in range(n):
    if watered[i] != 1:
        print(i + 1, watered[i])
        break
else:
    print("OK")
```

The array `watered` models the exact number of waterings per day. We carefully convert 1-based input indices to 0-based Python array indices to avoid off-by-one errors. The loop over `i` ensures the minimal day with a mistake is found. Using `else` on the loop ensures that if no mistakes exist, "OK" is printed.

## Worked Examples

**Sample 1:**

Input:

```
10 5
1 2
3 3
4 6
7 7
8 10
```

| Day | watered |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |
| 6 | 1 |
| 7 | 1 |
| 8 | 1 |
| 9 | 1 |
| 10 | 1 |

All days are watered exactly once, so the output is "OK".

**Sample 2:**

Input:

```
5 2
1 2
4 5
```

| Day | watered |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 0 |
| 4 | 1 |
| 5 | 1 |

Day 3 is not watered, so the first mistake occurs on day 3, output "3 0".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | For each of the m people, we increment up to n days in their range. With n, m ≤ 100, total operations ≤ 10,000. |
| Space | O(n) | The array `watered` of length n stores counts for each day. |

Given the constraints, the solution easily runs within the 2-second time limit and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n, m = map(int, input().split())
    watered = [0] * n
    for _ in range(m):
        a, b = map(int, input().split())
        for day in range(a - 1, b):
            watered[day] += 1
    for i in range(n):
        if watered[i] != 1:
            print(i + 1, watered[i])
            break
    else:
        print("OK")
    return output.getvalue().strip()

# provided samples
assert run("10 5\n1 2\n3 3\n4 6\n7 7\n8 10\n") == "OK", "sample 1"
assert run("5 2\n1 2\n4 5\n") == "3 0", "sample 2"

# custom cases
assert run("1 1\n1 1\n") == "OK", "single day watered correctly"
assert run("2 1\n1 2\n") == "OK", "two days watered by one person"
assert run("3 2\n1 2\n2 3\n") == "2 2", "overlapping day"
assert run("4 1\n2 3\n") == "1 0", "first day not watered"
assert run("5 3\n1 1\n3 3\n5 5\n") == "2 0", "middle day not watered"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 1 | OK | Minimum input size works |
| 2 1\n1 2 | OK | Single person covers multiple days |
| 3 2\n1 2\n2 3 | 2 2 | Detect overlapping day |
| 4 1\n2 3 | 1 0 | First day not watered |
| 5 3\n1 1\n3 3\n5 5 | 2 0 | Detect unwatered day in middle |

## Edge Cases

The case of overlapping assignments, e.g., [1, 2] and [2, 3], is handled because the array increments counts for all covered days. Day 2 will have `watered[1] = 2`, and the algorithm outputs "2 2" correctly. If the first day is missing from assignments, e.g., assignment [2, 3], day 1 remains 0, and the algorithm outputs "1 0". In all cases, the array accurately counts waterings and ensures the earliest mistake is reported.
