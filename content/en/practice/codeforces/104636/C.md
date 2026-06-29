---
title: "CF 104636C - The Rank"
description: "We are given a list of students, each identified by an integer id from 1 to n. Student 1 is Thomas. Every student has four exam scores, and their overall performance is measured by the sum of these four scores."
date: "2026-06-29T17:05:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 83
verified: false
draft: false
---

[CF 104636C - The Rank](https://codeforces.com/problemset/problem/104636/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of students, each identified by an integer id from 1 to n. Student 1 is Thomas. Every student has four exam scores, and their overall performance is measured by the sum of these four scores.

All students are ranked by sorting them in decreasing order of this total score. If two students have the same total score, the tie is broken by choosing the student with the smaller id first. The task is to determine Thomas’s final position in this ordering.

The constraints n ≤ 1000 and score values up to 100 mean each total score is bounded by 400. This immediately suggests that any O(n^2) or O(n log n) solution is comfortably fast, since even 10^6 comparisons is trivial in 1 second.

The main subtlety is the tie-breaking rule. A common mistake is to only count strictly higher scores and forget that equal scores still require comparing ids. Another failure case is sorting only by score without encoding the id ordering correctly, which leads to incorrect placement when duplicates exist.

A concrete edge case is when multiple students share the same total score as Thomas. For example, if Thomas has total 390 and two other students also have 390, only students with strictly greater scores should be ahead of him, and among equal scores Thomas should come first due to id = 1. A careless implementation that counts “score ≥ Thomas score” as higher rank would incorrectly push Thomas down.

## Approaches

A direct approach is to compute each student’s total score, then sort the students using the required ordering rule, and finally locate the position of student 1 in the sorted list.

This works because the ranking definition is exactly a global ordering problem: once all totals are computed, the task reduces to sorting pairs of (score, id) with a lexicographic order where score is descending and id is ascending.

A brute-force alternative is to compare Thomas against every other student and count how many are ranked ahead of him. A student is ahead if their score is strictly larger than Thomas’s score, or if the score is equal and their id is smaller. Since Thomas has the smallest id, no equal-score student can outrank him, so only strictly larger scores matter. This observation reduces the logic significantly.

The brute-force idea already runs in O(n), but generalizing it for any student would require O(n^2) comparisons. The sorting-based approach is more uniform and closer to how ranking systems are typically implemented.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Accepted but unnecessary |
| Sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Optimal approach

1. Read all students and compute their total score by summing the four subjects.

This transforms the problem into working with a single comparable value per student.
2. Store each student as a pair containing their total score and their id.

We keep id because tie-breaking depends on it.
3. Sort the list of students by two keys: first by decreasing total score, then by increasing id.

This directly encodes the ranking rule into the sorting comparator.
4. Scan through the sorted list and find the position where id equals 1.

The index in this sorted order is the answer, adjusted to 1-based indexing.

### Why it works

After computing totals, every comparison between students depends only on two values: score and id. The sorting order exactly matches the problem’s ranking rule, meaning the sorted array is a valid final ranking. Since sorting produces a total order consistent with the required comparison function, the position of student 1 is guaranteed to match their rank. No later adjustment is needed because all tie-breaking is already resolved during sorting.

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
        students.append(( -total, i ))  # negative for descending sort
    
    students.sort()
    
    for idx, (_, sid) in enumerate(students, start=1):
        if sid == 1:
            print(idx)
            return

if __name__ == "__main__":
    main()
```

The implementation uses a negated score to avoid writing a custom comparator: Python sorts ascending by default, so flipping the sign achieves descending order. The id is left as-is so that ties naturally resolve toward smaller ids first.

The loop over sorted students is safe because n ≤ 1000, so a linear scan is negligible.

## Worked Examples

### Sample 1

Input students produce totals: 398, 400, 398, 379, 357. We track sorting by (-score, id).

| Step | Student | Total | Key (-total, id) | Sorted order so far |
| --- | --- | --- | --- | --- |
| 1 | 1 | 398 | (-398, 1) |  |
| 2 | 2 | 400 | (-400, 2) |  |
| 3 | 3 | 398 | (-398, 3) |  |
| 4 | 4 | 379 | (-379, 4) |  |
| 5 | 5 | 357 | (-357, 5) |  |

After sorting, order becomes student 2, then students 1 and 3, then 4, then 5. Student 1 is in second position, so the output is 2.

This trace shows how equal totals are resolved purely by id ordering inside the sorted structure.

### Sample 2

Totals are 369, 240, 310, 300, 300, 0.

| Step | Student | Total | Key (-total, id) | Sorted order so far |
| --- | --- | --- | --- | --- |
| 1 | 1 | 369 | (-369, 1) |  |
| 2 | 2 | 240 | (-240, 2) |  |
| 3 | 3 | 310 | (-310, 3) |  |
| 4 | 4 | 300 | (-300, 4) |  |
| 5 | 5 | 300 | (-300, 5) |  |
| 6 | 6 | 0 | (0, 6) |  |

Sorted order starts with student 1, since 369 is strictly largest. Thus Thomas is first.

This confirms that when no one exceeds Thomas’s score, his rank is 1 regardless of other distributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting n students dominates all work |
| Space | O(n) | storing list of student tuples |

The constraints n ≤ 1000 make this comfortably fast. Even in the worst case, sorting 1000 elements is trivial, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    try:
        main()
    except SystemExit:
        pass
    return sys.stdout.getvalue().strip()

# provided samples
assert run("5\n100 98 100 100\n100 100 100 100\n100 100 99 99\n90 99 90 100\n100 98 60 99\n") == "2"
assert run("6\n100 80 90 99\n60 60 60 60\n90 60 100 60\n60 100 60 80\n100 100 0 100\n0 0 0 0\n") == "1"

# all equal
assert run("3\n10 10 10 10\n10 10 10 10\n10 10 10 10\n") == "1"

# Thomas already lowest
assert run("3\n0 0 0 0\n100 100 100 100\n50 50 50 50\n") == "3"

# maximum tie around Thomas
assert run("4\n10 10 10 10\n10 10 10 10\n10 10 10 10\n10 10 10 10\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal scores | 1 | tie-breaking by id places Thomas first |
| Thomas lowest | 3 | correct rank when others dominate |
| uniform max tie | 1 | stable handling of full equality |

## Edge Cases

One important case is when all students have identical total scores. In this situation, sorting relies entirely on id ordering. Since student 1 has the smallest id, the sorted order begins with Thomas, and the algorithm correctly returns rank 1.

Another case is when Thomas has the lowest possible score, such as all zeros while others have maximum scores. The sorting places him at the end because every other student has a higher key (-score is more negative), so his rank becomes n, which is consistent with expectations.

A final subtle case is when multiple students share Thomas’s score but none exceed it. Sorting ensures Thomas appears before all of them due to id ordering, so his rank is still 1 even though many ties exist.
