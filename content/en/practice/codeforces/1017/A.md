---
title: "CF 1017A - The Rank"
description: "We are given a class of students, each identified by a unique integer id starting from 1. Every student has four exam scores corresponding to different subjects. The task is to rank all students by their total score across the four subjects."
date: "2026-06-16T22:09:13+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1017
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 502 (in memory of Leopoldo Taravilse, Div. 1 + Div. 2)"
rating: 800
weight: 1017
solve_time_s: 90
verified: true
draft: false
---

[CF 1017A - The Rank](https://codeforces.com/problemset/problem/1017/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a class of students, each identified by a unique integer id starting from 1. Every student has four exam scores corresponding to different subjects. The task is to rank all students by their total score across the four subjects. Higher total score means a better rank. When two students have the same total score, the tie is broken by giving the student with the smaller id a better rank.

The output we need is the rank of the student with id 1, Thomas. Rank is defined as position in this sorted order starting from 1.

The constraints are small, with at most 1000 students. This immediately tells us that an O(n²) approach is perfectly fine, and even a straightforward sorting-based O(n log n) solution is overkill but clean and safe. There is no need for optimization beyond simple aggregation and ordering.

The main subtlety in this problem is the tie-breaking rule. If we forget that smaller id wins when sums are equal, we may incorrectly place Thomas behind someone with the same score. Another subtle point is that rank depends on position in the final sorted list, not on counting how many people have strictly greater scores only after sorting incorrectly. A naive implementation that only counts strictly higher totals without handling ties correctly would fail.

A concrete failure case arises when Thomas has the same score as multiple students. Suppose Thomas and student 5 both have total 400, and student 2 has 401. The correct ranking places student 2 first, then Thomas before student 5 because of smaller id. If we ignore id tie-breaking, Thomas’s rank could be miscomputed as 3 instead of 2.

## Approaches

The simplest way to think about the problem is to compute each student’s total score and then sort all students according to the rules described. After sorting, we locate Thomas and read off his position.

A brute-force approach would be to repeatedly scan all students and pick the next best candidate not yet chosen. This mimics selection sort behavior. Each selection step requires O(n) scanning, and we do it n times, resulting in O(n²) operations. With n up to 1000, this is about one million comparisons, which is still acceptable but unnecessary.

A more direct approach is to compute all totals, store them with ids, and sort using Python’s built-in sorting. The key insight is that the ranking order is fully determined by a single key: negative total score (for descending order), and then id (for ascending order). This converts the problem into a standard sorting task.

Once sorted, Thomas’s rank is simply his index in the sorted list plus one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Selection | O(n²) | O(n) | Accepted |
| Sort by key | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of students and store their scores.
2. For each student, compute the sum of the four subject scores. This reduces each student to a single comparable value.
3. Store each student as a pair consisting of negative sum and id. The negative is used so that sorting in ascending order produces descending score order.
4. Sort the list of students. The sorting automatically applies the secondary rule because id is included in the tuple.
5. Scan the sorted list and find the entry corresponding to id 1.
6. Output its 1-based position as the rank.

Why it works is based on the fact that sorting by a tuple enforces lexicographic ordering. The tuple (-sum, id) ensures that higher sums come first, and among equal sums, smaller ids come first. Since every student is represented exactly once and the ordering is total and consistent, the sorted list is exactly the required ranking. The position of Thomas in this list is therefore his correct rank.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    students = []

    for i in range(1, n + 1):
        a, b, c, d = map(int, input().split())
        total = a + b + c + d
        students.append((-total, i))

    students.sort()

    for idx, (_, sid) in enumerate(students, start=1):
        if sid == 1:
            print(idx)
            return

if __name__ == "__main__":
    main()
```

The solution builds a list of tuples where each tuple encodes both ranking criteria. The sorting step handles all ordering logic, which avoids manual comparison mistakes. The final loop only searches for id 1, which is safe given the small constraints.

A common mistake is forgetting to include the id in the sort key. Without it, equal scores could appear in arbitrary order, which would break the rank definition.

## Worked Examples

### Sample 1

Input:

```
5
100 98 100 100
100 100 100 100
100 100 99 99
90 99 90 100
100 98 60 99
```

Computed totals:

| id | sum |
| --- | --- |
| 1 | 398 |
| 2 | 400 |
| 3 | 398 |
| 4 | 379 |
| 5 | 357 |

Sorted order by (-sum, id):

| position | id | sum |
| --- | --- | --- |
| 1 | 2 | 400 |
| 2 | 1 | 398 |
| 3 | 3 | 398 |
| 4 | 4 | 379 |
| 5 | 5 | 357 |

Thomas (id 1) appears at position 2, so output is 2.

This trace confirms that tie-breaking by id is essential, since ids 1 and 3 share the same score but are ordered correctly.

### Sample 2

Input:

```
6
100 100 100 69
60 60 60 60
80 80 80 70
75 75 75 75
75 75 75 75
0 0 0 0
```

Totals:

| id | sum |
| --- | --- |
| 1 | 369 |
| 2 | 240 |
| 3 | 310 |
| 4 | 300 |
| 5 | 300 |
| 6 | 0 |

Sorted order:

| position | id | sum |
| --- | --- | --- |
| 1 | 1 | 369 |
| 2 | 3 | 310 |
| 3 | 4 | 300 |
| 4 | 5 | 300 |
| 5 | 2 | 240 |
| 6 | 6 | 0 |

Thomas is first, so rank is 1. The trace shows that even when multiple ties exist (ids 4 and 5), ordering remains stable due to id-based tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates after computing sums |
| Space | O(n) | Each student stored once as a tuple |

The constraints allow up to 1000 students, so sorting at most 1000 elements is trivial. The memory usage is constant-scale and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue() if (main() or True) else ""

# sample tests
assert run("""5
100 98 100 100
100 100 100 100
100 100 99 99
90 99 90 100
100 98 60 99
""").strip() == "2"

assert run("""6
100 100 100 69
60 60 60 60
80 80 80 70
75 75 75 75
75 75 75 75
0 0 0 0
""").strip() == "1"

# custom: minimum case
assert run("""1
10 10 10 10
""").strip() == "1"

# custom: all equal scores
assert run("""3
10 10 10 10
10 10 10 10
10 10 10 10
""").strip() == "1"

# custom: Thomas is worst
assert run("""3
0 0 0 0
10 0 0 0
0 0 0 1
""").strip() == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | 1 | minimum boundary |
| all equal | 1 | tie-breaking by id |
| Thomas worst | 3 | correct ranking order |

## Edge Cases

When all students have identical total scores, the ranking depends entirely on id ordering. For example, with three students all scoring 40, the sorted order must be ids 1, 2, 3. Thomas is always first among equals, so his rank is 1. The algorithm handles this correctly because id is the secondary key in the tuple.

When Thomas has the lowest score, he should appear at the end of the sorted list. For instance, if Thomas has total 10 and others have 20 and 30, the sorted order becomes 30, 20, 10, placing him at rank 3. The sorting key ensures this naturally without special handling, since -10 is larger than -30 and -20, pushing him later in the order.
