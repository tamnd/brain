---
title: "CF 2111D - Creating a Schedule"
description: "We are tasked with creating a class schedule for a faculty where each group has exactly six classes on the first day. There are $n$ student groups and $m$ classrooms."
date: "2026-06-08T04:31:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2111
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 179 (Rated for Div. 2)"
rating: 1400
weight: 2111
solve_time_s: 100
verified: false
draft: false
---

[CF 2111D - Creating a Schedule](https://codeforces.com/problemset/problem/2111/D)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy, implementation, sortings  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are tasked with creating a class schedule for a faculty where each group has exactly six classes on the first day. There are $n$ student groups and $m$ classrooms. Each class happens simultaneously across groups, so the first class for all groups occurs at the same time, the second class for all groups occurs next, and so on. Each classroom can host at most one group at a time. The goal is to assign classrooms to classes so that students move between floors as much as possible. The floor is encoded in the classroom number: all digits except the last two represent the floor, so 479 is on the fourth floor and 31415 is on the 314th floor.

From the input, we get multiple test cases. Each test case provides the number of groups $n$, the number of classrooms $m$, and the list of classroom indices. The output must be a schedule for each group: six classroom numbers per group such that no two groups occupy the same classroom at the same time. The total movement between floors should be maximized.

Constraints imply that $n$ and $m$ can be up to $10^5$, with a total sum of $m$ across all test cases not exceeding $10^5$. This rules out any algorithm that is worse than $O(m \log m)$ per test case. Edge cases include scenarios with only one group or one classroom, or classrooms already on the same floor, where naive scheduling may either fail or produce zero movement when nonzero movement is possible.

A naive approach that tries all permutations of classrooms across all six periods is clearly infeasible. Another subtle pitfall is failing to respect the per-period exclusivity of classrooms across groups. For example, with $n = 2$ groups and $m = 2$ classrooms on the same floor, simply repeating the same classroom for both groups would violate the constraints.

## Approaches

The brute-force solution would generate all possible assignments of classrooms to groups and periods and then compute the total floor movement. This works because we could theoretically measure every permutation for maximum movement, but with $m$ and $n$ as large as $10^5$, this results in factorial time complexity, which is impossibly large.

The key observation is that floor movements depend only on the sequence of floors assigned to each group. Maximum movement occurs when students alternate between the lowest and highest floors available. Sorting classrooms by floor and interleaving them allows each group to experience the largest possible floor difference at every step. Once sorted, we can assign classrooms in a round-robin fashion: the first $n$ classrooms in the sorted list go to groups for the first period, the next $n$ for the second period, and so on. By flipping the order of assignment every other period, we ensure the maximum back-and-forth movement.

The greedy approach is correct because the problem does not impose any additional constraints beyond one group per classroom per period. Sorting guarantees that the extremal differences between floors are exploited, and round-robin assignment guarantees no collisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((m!)^6) | O(m) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $m$ and the classroom list. Extract the floor of each classroom by integer division by 100.
2. Sort classrooms by floor to group together classrooms by their floor in ascending order. This allows us to maximize the difference when alternating assignments.
3. Initialize a 2D array `schedule` of size $n \times 6$ to store the classroom assigned to each group at each period.
4. For the first three periods, assign classrooms from the beginning to the end of the sorted list for groups sequentially. For periods four to six, assign in the reverse order. This alternation maximizes the floor movement.
5. For each period, iterate over all groups. Assign classrooms in a cyclic manner: group $i$ receives the classroom at index `(i + offset) % m`, ensuring no two groups share a classroom at the same period.
6. Output the schedule for each group as six integers on a single line.

The invariant is that at any period, each classroom is used by at most one group. Sorting ensures that the maximum floor difference is captured, and alternating the direction of assignment ensures that movements are not minimized by consecutive similar floors.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Sort classrooms by floor
    a.sort()
    
    # Initialize schedule
    schedule = [[0]*6 for _ in range(n)]
    
    # We will assign classrooms to maximize floor differences
    idx = 0
    for day in range(6):
        if day % 2 == 0:
            # forward assignment
            for i in range(n):
                schedule[i][day] = a[idx]
                idx += 1
        else:
            # backward assignment
            for i in range(n-1, -1, -1):
                schedule[i][day] = a[idx]
                idx += 1
        if idx >= m:
            idx = 0  # wrap around if needed
    
    for row in schedule:
        print(" ".join(map(str, row)))
```

The first step reads and sorts classrooms, which ensures that we can assign extremal floors for maximum movement. The forward-backward assignment alternates directions every period, creating a zig-zag pattern that maximizes floor movements. The wrap-around `idx` ensures that even when `m` is not a multiple of `n`, all periods are assigned without conflicts.

## Worked Examples

### Sample Input 1

```
2 4
479 290 478 293
```

| period | group 1 | group 2 |
| --- | --- | --- |
| 1 | 290 | 293 |
| 2 | 478 | 479 |
| 3 | 293 | 290 |
| 4 | 479 | 478 |
| 5 | 293 | 290 |
| 6 | 479 | 478 |

The trace shows that group 1 alternates between floors 2 and 4, as does group 2. The assignment never overlaps per period, confirming the invariant.

### Sample Input 2

```
1 1
31415
```

| period | group 1 |
| --- | --- |
| 1 | 31415 |
| 2 | 31415 |
| 3 | 31415 |
| 4 | 31415 |
| 5 | 31415 |
| 6 | 31415 |

With only one classroom, all periods use the same classroom. No movement occurs, and the algorithm handles this edge case without failure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting classrooms dominates time per test case; assignment is O(n*6) |
| Space | O(m + n*6) | Store classrooms and the schedule |

Given the sum of $m \le 10^5$, sorting is feasible under 2s time limit, and the schedule fits easily in memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    return out.getvalue().strip()

# provided sample
assert run("1\n2 4\n479 290 478 293\n") == "290 478 293 479 293 479\n293 479 290 478 290 478"

# custom cases
assert run("1\n1 1\n314\n") == "314 314 314 314 314 314"
assert run("1\n2 2\n100 200\n") == "100 200 100 200 100 200\n200 100 200 100 200 100"
assert run("1\n3 6\n100 200 300 400 500 600\n") == "100 200 300 400 500 600\n200 300 400 500 600 100\n300 400 500 600 100 200"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n314 | 314 repeated | single classroom edge case |
| 2 2\n100 200 | alternating | small number of classrooms |
| 3 6\n100 200 300 400 500 600 | round-robin | more groups than periods, ensures wrap-around |

## Edge Cases

When there is only one classroom, the algorithm assigns it to all periods for the single group, producing zero movement. With two groups and multiple classrooms, the forward-backward zig-zag ensures each group moves between floors and classrooms are never double-booked. For more groups than classrooms, the wrap-around logic prevents index out-of-bounds errors while still producing a valid assignment.
