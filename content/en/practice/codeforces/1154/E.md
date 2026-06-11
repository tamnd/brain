---
title: "CF 1154E - Two Teams"
description: "We are given a row of n students, each with a distinct programming skill ranging from 1 to n. Two coaches take turns picking students to form their teams. On a coach's turn, they select the student with the highest skill remaining in the row."
date: "2026-06-12T02:49:32+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1154
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 552 (Div. 3)"
rating: 1800
weight: 1154
solve_time_s: 118
verified: true
draft: false
---

[CF 1154E - Two Teams](https://codeforces.com/problemset/problem/1154/E)

**Rating:** 1800  
**Tags:** data structures, implementation, sortings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of `n` students, each with a distinct programming skill ranging from 1 to `n`. Two coaches take turns picking students to form their teams. On a coach's turn, they select the student with the highest skill remaining in the row. Then, in addition to that student, they also take up to `k` students to the left and `k` students to the right, as long as these students have not already been chosen. All selected students leave the row and join the current coach's team. The process alternates until no students remain.

The input provides `n` and `k`, followed by an array of `n` integers representing the skills of the students in order. The output must indicate, for each student in the original row, which team they join: `1` for the first coach and `2` for the second coach.

Given the constraints, `n` can be up to 200,000. A naive approach that repeatedly scans for the maximum skill in the current row could take O(n²) time, which is far too slow. We must use a data structure that allows us to quickly find the current maximum and efficiently remove consecutive ranges of students. An edge case arises when the maximum is near the boundaries of the row; here, the range of `k` students to the left or right may extend beyond the row, and the algorithm must handle this gracefully. A careless implementation might try to access indices outside the array bounds.

For example, with `n = 5`, `k = 2`, and skills `[2, 4, 5, 3, 1]`, the first coach chooses `5` and takes all students (positions 1 to 5), leaving the second coach with no students. A naive method that does not correctly handle ranges at the edges could produce incorrect team assignments.

## Approaches

The brute-force approach is straightforward: on each turn, scan the current array to find the maximum skill, determine the indices of the students to take based on `k`, mark them as belonging to the current coach, remove them from the array, and repeat. While this works logically, scanning the array to find the maximum at each turn can require up to `n + (n-1) + ... + 1 = O(n²)` comparisons, which is unacceptable for `n` up to 2 × 10⁵.

The key insight is that the skills are distinct integers from 1 to `n`. This allows us to process students in order of decreasing skill rather than scanning repeatedly. If we maintain a sorted set of indices of students who are still in the row, we can, for each skill from `n` down to 1, check whether the student has already been assigned. If not, we assign them and their `k` closest neighbors on each side using the sorted set to efficiently find adjacent indices. This reduces the number of operations to O(n log n) because each insert/remove in a balanced tree structure (or a sorted set) takes log n time, and each student is processed exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `team` of length `n` with all zeros. This array will store the team assignment of each student. A zero indicates the student has not yet been assigned.
2. Construct a list of `(skill, index)` pairs and sort it in descending order of skill. This allows processing students from the highest skill to the lowest.
3. Maintain a `SortedSet` or a `TreeSet` of indices representing students still in the row. This allows efficient finding of consecutive neighbors.
4. Set a variable `current_team = 1` to track which coach's turn it is.
5. Iterate over the sorted list of students. For each `(skill, idx)`:

- If `team[idx]` is already non-zero, skip this student.
- Otherwise, assign `team[idx] = current_team`.
- Using the sorted set, identify up to `k` neighbors to the left and right. Assign them the same `current_team` value and remove all assigned indices from the sorted set.
6. After processing each highest skill, flip `current_team` to alternate coaches.
7. Continue until all students are assigned a team.

Why it works: At each step, we always pick the highest unassigned skill, just like the rules dictate. Assigning up to `k` neighbors on each side exactly models the coaches' choice. Since we never reassign a student, and each student is eventually processed in decreasing order, the resulting `team` array is guaranteed to respect the problem rules.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left, bisect_right, insort

class SortedSet:
    def __init__(self, data=None):
        self.data = sorted(data) if data else []

    def __contains__(self, x):
        i = bisect_left(self.data, x)
        return i < len(self.data) and self.data[i] == x

    def add(self, x):
        i = bisect_left(self.data, x)
        if i == len(self.data) or self.data[i] != x:
            self.data.insert(i, x)

    def discard(self, x):
        i = bisect_left(self.data, x)
        if i < len(self.data) and self.data[i] == x:
            self.data.pop(i)

    def index_left(self, x):
        i = bisect_left(self.data, x)
        return i

    def index_right(self, x):
        i = bisect_right(self.data, x)
        return i

    def get_left_neighbors(self, idx, k):
        i = bisect_left(self.data, idx)
        left = self.data[max(0, i - k):i]
        return left

    def get_right_neighbors(self, idx, k):
        i = bisect_right(self.data, idx)
        right = self.data[i:i + k]
        return right

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    team = [0] * n
    sorted_indices = SortedSet(range(n))
    skills = sorted([(val, idx) for idx, val in enumerate(a)], reverse=True)
    current_team = 1

    for val, idx in skills:
        if team[idx] != 0:
            continue
        to_assign = [idx]
        to_assign += sorted_indices.get_left_neighbors(idx, k)
        to_assign += sorted_indices.get_right_neighbors(idx, k)
        for i in to_assign:
            team[i] = current_team
            sorted_indices.discard(i)
        current_team = 3 - current_team  # switch team

    print("".join(map(str, team)))

if __name__ == "__main__":
    main()
```

The `SortedSet` class is a utility for maintaining remaining student indices and finding neighbors efficiently. The `get_left_neighbors` and `get_right_neighbors` functions retrieve up to `k` neighbors on each side. Switching `current_team` is done by `3 - current_team` to alternate between 1 and 2. The final `team` array directly represents the required output string.

## Worked Examples

### Sample 1

Input: `5 2`, skills `[2, 4, 5, 3, 1]`.

| Iteration | Current Team | Max Skill | Assigned Indices | Remaining SortedSet | Team Array |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | [2,0,1,3,4] | [] | [1,1,1,1,1] |

All students are taken in the first move. The final output is `11111`. This shows the algorithm handles full-range selection correctly.

### Sample 2

Input: `5 1`, skills `[1, 3, 5, 4, 2]`.

| Iteration | Current Team | Max Skill | Assigned Indices | Remaining SortedSet | Team Array |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | [2,1,3] | [0,4] | [0,1,1,1,0] |
| 2 | 2 | 4 | [0,4] | [] | [2,1,1,1,2] |

This confirms neighbor selection respects the boundaries and alternating turns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting takes O(n log n), and each insert/discard in the sorted set is O(log n) per student. |
| Space | O(n) | Storing team assignments and sorted indices of size n. |

With n ≤ 2 × 10⁵, the algorithm runs comfortably within 2 seconds and uses less than 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    input_backup = builtins.input
    builtins.input = lambda: sys.stdin.readline()
    from contextlib import redirect_stdout
    output = io.StringIO()
    with redirect_stdout(output):
        main()
    builtins.input = input_backup
    return output.getvalue().strip()

# Provided samples
assert run("5 2\n2 4 5
```
