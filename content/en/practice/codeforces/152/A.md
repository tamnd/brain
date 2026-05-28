---
title: "CF 152A - Marks"
description: "We are asked to find the number of students in a class who are the best in at least one subject. Each student has grades for multiple subjects, with each grade being a single-digit number between 1 and 9."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 152
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 108 (Div. 2)"
rating: 900
weight: 152
solve_time_s: 68
verified: true
draft: false
---

[CF 152A - Marks](https://codeforces.com/problemset/problem/152/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the number of students in a class who are the best in at least one subject. Each student has grades for multiple subjects, with each grade being a single-digit number between 1 and 9. The input represents the grades as a grid of size _n_ by _m_, where each row corresponds to a student and each column corresponds to a subject. A student is considered successful if, in at least one column, their grade matches the maximum grade among all students for that subject.

The constraints are modest: both the number of students and the number of subjects are at most 100. This means a solution with a double loop over students and subjects, which amounts to at most 10,000 operations, will run comfortably under the 1-second time limit. Edge cases we must watch for include situations where all students have the same grades, where only one student is the top in every subject, or where the maximum grade in a subject appears multiple times. A careless approach might count a student only if they are the unique maximum in a subject, which would produce the wrong answer.

## Approaches

A straightforward brute-force approach is to check each student for every subject, keeping track of the maximum grade in that subject. Once we have the maximum, we mark all students who achieved it. This involves iterating over each column to find the maximum grade, then iterating over each student again to check if they match that maximum. The correctness is guaranteed because we explicitly compare every student in every subject.

This brute-force is already optimal for these constraints. The key insight is that we do not need to sort or use additional data structures. We can simply maintain a set of indices of students who are successful, updating it whenever a student matches the maximum grade for a subject. The problem structure makes this feasible because the grid is small and the maximum calculation per column is cheap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Accepted |
| Optimal | O(n * m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values for the number of students _n_ and the number of subjects _m_, and then read the next _n_ lines as strings representing student grades. Each line is converted into a list for easier indexing.
2. Initialize a set to keep track of successful students. Using a set avoids double-counting and allows efficient insertion.
3. Iterate over each subject index from 0 to _m-1_. For each subject, find the maximum grade among all students by iterating over the rows for that column.
4. Once the maximum grade for the current subject is determined, iterate again over all students and add to the successful set any student whose grade matches the maximum for that subject.
5. After processing all subjects, the size of the successful set represents the total number of successful students. Print this value.

Why it works: By iterating column by column, we guarantee that every subject is checked for its top performer(s). The set ensures that each student is counted only once regardless of how many subjects they are top in. The algorithm cannot miss any successful student because every student-grade comparison occurs explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grades = [list(input().strip()) for _ in range(n)]
successful = set()

for col in range(m):
    max_grade = max(grades[row][col] for row in range(n))
    for row in range(n):
        if grades[row][col] == max_grade:
            successful.add(row)

print(len(successful))
```

The code first reads the dimensions and the grade grid. Each student’s grades are stored as a list of characters. The main loop iterates over each subject (column). For each column, the maximum grade is computed using a generator expression, then another loop marks all students who achieved that grade. Finally, the length of the set gives the number of successful students. The subtlety is handling grades as strings because they are single-digit characters; this works because character comparison for digits gives the same ordering as integer comparison. Using a set avoids duplicates without additional bookkeeping.

## Worked Examples

**Sample 1**

Input:

```
3 3
223
232
112
```

Trace table:

| col | max_grade | successful set |
| --- | --- | --- |
| 0 | 2 | {0, 1} |
| 1 | 3 | {0, 1} |
| 2 | 3 | {0, 1} |

Explanation: Student 0 has top grade in subject 0, student 1 has top grade in subject 1, both are added to the successful set. Student 2 never matches a maximum.

**Sample 2**

Input:

```
2 2
99
99
```

Trace table:

| col | max_grade | successful set |
| --- | --- | --- |
| 0 | 9 | {0, 1} |
| 1 | 9 | {0, 1} |

Both students are successful in both subjects. The algorithm correctly counts each only once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Each subject iteration requires scanning all students to find max and again to mark successful ones |
| Space | O(n) | The set stores indices of at most n students |

With n and m up to 100, the total operations are at most 10,000, which fits easily within the 1-second limit. The memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    grades = [list(input().strip()) for _ in range(n)]
    successful = set()
    for col in range(m):
        max_grade = max(grades[row][col] for row in range(n))
        for row in range(n):
            if grades[row][col] == max_grade:
                successful.add(row)
    return str(len(successful))

# Provided samples
assert run("3 3\n223\n232\n112\n") == "2", "sample 1"
assert run("2 2\n99\n99\n") == "2", "sample 2"

# Custom cases
assert run("1 1\n5\n") == "1", "single student and subject"
assert run("3 3\n111\n111\n111\n") == "3", "all equal values"
assert run("2 5\n12345\n54321\n") == "2", "top in multiple subjects"
assert run("4 4\n9123\n1294\n2912\n3219\n") == "4", "multiple winners"
assert run("100 1\n" + "\n".join("9" for _ in range(100)) + "\n") == "100", "maximum n edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n5\n | 1 | Minimum-size input |
| 3 3\n111\n111\n111\n | 3 | All-equal values |
| 2 5\n12345\n54321\n | 2 | Multiple subjects with different winners |
| 4 4\n9123\n1294\n2912\n3219\n | 4 | Complex mix of winners |
| 100 1\n9 repeated | 100 | Maximum number of students |

## Edge Cases

When all students have the same grades, every student should be counted as successful. For input:

```
3 3
111
111
111
```

The maximum in each subject is 1. Iterating over each column, every student matches the maximum and is added to the set. The final count is 3, as expected. This confirms the algorithm handles tie cases correctly.

For a single student with multiple subjects:

```
1 5
12345
```

The student is trivially successful in all subjects. The set ensures the student is counted once, yielding output 1. This confirms the algorithm correctly handles minimum-size edge cases.
