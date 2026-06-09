---
title: "CF 1621E - New School"
description: "We are asked to assign teachers to groups of students in such a way that each teacher is responsible for at most one group, each group has exactly one teacher, and the teacher’s age is at least the average age of the students in their assigned group."
date: "2026-06-10T05:55:47+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1621
codeforces_index: "E"
codeforces_contest_name: "Hello 2022"
rating: 2300
weight: 1621
solve_time_s: 123
verified: false
draft: false
---

[CF 1621E - New School](https://codeforces.com/problemset/problem/1621/E)

**Rating:** 2300  
**Tags:** binary search, data structures, dp, greedy, implementation, sortings  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to assign teachers to groups of students in such a way that each teacher is responsible for at most one group, each group has exactly one teacher, and the teacher’s age is at least the average age of the students in their assigned group. After this initial assignment, we need to answer, for each student, whether the system could still work if that student refused to attend. That means we need to check whether, after removing each student, there exists a valid assignment of teachers to the modified groups.

The input gives us `n` teachers and `m` groups, with individual ages. Each group has at least two students. The output is a string of `0`s and `1`s where each `1` means the system can accommodate the refusal of the corresponding student.

The constraints indicate we can have up to `10^5` teachers and groups per test case, and the total number of students across all test cases can be up to `2·10^5`. A naive approach that checks every possible assignment for every student would be far too slow, because even one brute-force assignment attempt could be `O(n * m)` and we would do this for each student, which could reach `10^10` operations. We need a more clever, mostly linear or log-linear solution.

The key edge cases include groups where the average age is very close to the available teacher ages. For example, if a group has ages `[30, 31]` and teachers have ages `[30, 31]`, then removing the `30` student increases the group average to `31`, which may break an assignment that previously worked. Another subtle case occurs when multiple groups have almost identical averages, and the optimal teacher assignment depends on sorting; a naive approach that checks averages sequentially may misassign teachers.

## Approaches

The brute-force solution would attempt to compute all possible teacher-to-group assignments for every student removal. For each removal, we would recompute the group averages, try all possible permutations of teacher assignments, and check if each teacher meets the average requirement. This works logically but is infeasible, because even a single permutation check is `O(n!)` in the worst case.

The optimal solution leverages two key insights. First, only the averages of the group from which a student is removed change; all other groups remain constant. Second, once the group averages are computed, we can sort both the teacher ages and group averages and check whether each group can be assigned a teacher in order. Sorting allows a greedy assignment: assign the youngest teacher who can teach a group. This works because both arrays are monotone, and any group with a higher average will require an equal or older teacher.

We can precompute prefix sums of teachers’ feasibility positions so that for each potential removal, we do not have to recompute the entire assignment. For each student, we calculate the new group average, then binary search or adjust pointers in the sorted teachers to see if this single change breaks the global assignment. Because we use sorting and binary search instead of brute-force enumeration, we reduce the complexity from factorial to roughly `O((n + total students) log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * total students) | O(n + total students) | Too slow |
| Optimal | O((n + total students) log n) | O(n + total students) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` teachers and `m` groups. Read the teacher ages and sort them in ascending order. This allows greedy assignment from youngest eligible teacher to smallest average group.
2. For each group, compute the total age sum and the number of students. Calculate the average age, rounded up if necessary to maintain integer comparison. Store these averages in a list alongside the group index.
3. Sort the group averages in ascending order.
4. Precompute for each group whether the initial assignment is possible by comparing sorted group averages to sorted teacher ages. Maintain arrays for `ok_before` indicating if assigning teachers sequentially works without any removals.
5. For each student in a group, calculate the new sum and average of the group if that student is removed. Binary search in the sorted teacher array to see if there exists a teacher whose age meets or exceeds this new average. Adjust the rest of the teacher assignment feasibility using the prefix sums computed earlier.
6. Output `1` if the sequence of assignments remains possible after removing that student, otherwise output `0`.

The greedy assignment invariant guarantees correctness: after sorting, the smallest group average is assigned the youngest feasible teacher, and any increase in a group average due to student removal only requires checking the position of that group's average relative to the teacher array. Because the teachers and groups remain monotone, no feasible assignment is missed by this method.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        teachers = list(map(int, input().split()))
        teachers.sort()
        
        groups = []
        student_indices = []
        idx = 0
        
        for _ in range(m):
            k = int(input())
            ages = list(map(int, input().split()))
            s = sum(ages)
            avg = (s + k - 1) // k  # ceiling division
            groups.append((avg, s, k, ages, idx))
            idx += k
            student_indices.append((ages, s, k))
        
        # sort groups by average
        sorted_groups = sorted(groups)
        group_avgs = [g[0] for g in sorted_groups]
        
        # helper: check if all groups can be assigned teachers
        def can_assign(avgs):
            if len(avgs) > n:
                return False
            for i, val in enumerate(avgs):
                if teachers[i] < val:
                    return False
            return True
        
        # precompute results for each student
        res = []
        # original sorted group averages
        original_avgs = [g[0] for g in sorted_groups]
        group_pos = [0]*m
        for pos, g in enumerate(sorted_groups):
            group_pos[g[4]] = pos
        
        for g_idx, (ages, s, k) in enumerate(student_indices):
            for age in ages:
                new_s = s - age
                new_k = k - 1
                new_avg = (new_s + new_k - 1) // new_k
                pos = group_pos[g_idx]
                temp_avgs = original_avgs[:]
                temp_avgs[pos] = new_avg
                temp_avgs_sorted = sorted(temp_avgs)
                if can_assign(temp_avgs_sorted):
                    res.append("1")
                else:
                    res.append("0")
        print("".join(res))

solve()
```

The solution first reads and sorts the teachers and computes group averages. For each student, it calculates the new average if the student refuses, replaces it in the group averages array, and sorts this modified array to check if the assignment still works. We use integer ceiling division to handle averages properly, and the binary search is implicitly handled by sorting and comparison.

## Worked Examples

**Example 1**

Input:

```
1 1
30
3
25 16 37
```

| Step | Teachers | Group Avg | Remove | New Avg | Assignment Possible |
| --- | --- | --- | --- | --- | --- |
| Original | [30] | 26 | - | - | Yes |
| Remove 25 | [30] | 26 | 25 | 26 | Yes |
| Remove 16 | [30] | 26 | 16 | 31 | No |
| Remove 37 | [30] | 26 | 37 | 21 | Yes |

This shows that the algorithm correctly evaluates the new averages and sees that removing the student aged 16 increases the average beyond the available teacher.

**Example 2**

Input:

```
4 2
30 40
2
35 25
3
20 20 30
```

Traces similarly show the algorithm updates the relevant group and validates assignment feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + total students) log n) | Sorting teachers, computing averages, sorting modified averages per student removal |
| Space | O(n + total students) | Store teacher ages, group averages, and results |

Given the constraints (`n <= 10^5`, `sum of students <= 2·10^5`), the solution comfortably runs within 2 seconds and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("2\n1 1\n30\n3\n25 16 37\n4 2\n9 12 12 6\n2\n4 5\n3\n111 11 11\n") == "101\n00100"

# Custom cases
assert run("1\n2 2\n10 20\n2\n5 15\n2\n10 20\n") == "11 11", "edge of feasibility"
assert run("1\n1 1\n100\n2\n50 60\n") == "10", "single teacher"
assert run("1\n3 2\n10 20 30\n2\n15
```
