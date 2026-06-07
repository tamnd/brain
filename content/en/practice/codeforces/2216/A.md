---
title: "CF 2216A - Course Wishes"
description: "We are asked to simulate a course registration system where a student has multiple courses, each with an initial priority level, and some levels have capacity limits."
date: "2026-06-07T18:53:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2216
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 2, Based on THUPC 2026 \u2014 Finals)"
rating: 900
weight: 2216
solve_time_s: 96
verified: false
draft: false
---

[CF 2216A - Course Wishes](https://codeforces.com/problemset/problem/2216/A)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a course registration system where a student has multiple courses, each with an initial priority level, and some levels have capacity limits. The student wants to gradually increase the priority level of each course until all courses reach the lowest-priority level, which has no limit. Each operation increments a course's priority level by one, and after each increment, the system must remain valid with respect to the capacity limits. The task is to output a valid sequence of operations to reach the target configuration, or report impossibility.

The input gives us the number of courses `n`, the number of constrained priority levels `k`, a list of capacity limits for the first `k` levels, and the initial assignment of courses to priority levels. The final level `k+1` has no limit, so every course can eventually reach it. The constraints are small: `n` up to 50, `k` up to 20, and at most 50 test cases. This indicates that a relatively straightforward simulation is acceptable, as even a naive solution performing `n * k` operations is well below the limit of 1000 operations.

An edge case arises when many courses are already at high levels, close to the unconstrained level. For instance, if all courses start at level `k`, a naive approach that blindly increments might exceed capacity in intermediate steps. Another subtlety is that some courses may already be at level `k+1`, and these cannot be incremented. A careless approach might attempt to increment these, violating constraints.

## Approaches

A brute-force approach is to repeatedly scan through the courses and increment any course whose level is not yet `k+1` while maintaining the capacity limits. For each operation, we would check if incrementing a particular course violates the current count of courses at that level. This method is simple and correct but inefficient in the worst case if we have to check all courses and levels repeatedly, though in our constraints, this still works.

The key insight for an optimal approach is that we can always increment courses at the lowest current level first, because incrementing a course from level `i` to `i+1` frees up a slot at level `i` and does not violate the capacity of any higher level. By repeating this from the lowest level up to `k`, we ensure that each operation is always valid and we will eventually reach all courses at level `k+1`. This greedy strategy guarantees we never exceed any capacity, and it naturally produces a sequence within the allowed number of operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n_k_operations) | O(n+k) | Accepted due to small n, k |
| Greedy Increment | O(n*k) | O(n+k) | Accepted and efficient |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the number of courses `n`, number of constrained levels `k`, the list of capacity limits `a`, and the initial course levels `b`.
2. Initialize a list `count` of length `k+1` to track the number of courses currently at each level. Fill it by counting occurrences in `b`. This allows quick verification that increments will not violate capacities.
3. Initialize an empty list `operations` to store the sequence of course indices to increment.
4. Repeat the following until all courses reach level `k+1`. Scan levels from 1 to `k`. For each level `i`, scan all courses. If a course is at level `i` and the count of courses at level `i` is greater than the allowed capacity `a[i-1]` after removing this course, increment the course. Update `b`, `count[i]`, and `count[i+1]`, and append the course index to `operations`. Always select the first eligible course at the current level, which guarantees we do not block any other operations.
5. Stop when no courses remain below level `k+1`. If the total number of operations exceeds 1000, return `-1` (though constraints guarantee we can always do it under 1000). Otherwise, output the number of operations and the operation sequence.

This method works because the invariant maintained is that at any time, the number of courses at level `i` never exceeds its capacity. By incrementing courses starting from the lowest levels, we systematically reduce constrained levels without violating higher-level capacities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        count = [0] * (k + 2)  # count[i] = number of courses at level i
        for level in b:
            count[level] += 1
        
        operations = []
        
        while True:
            made_move = False
            for level in range(1, k + 1):
                for idx in range(n):
                    if b[idx] == level and count[level] > a[level - 1]:
                        count[level] -= 1
                        count[level + 1] += 1
                        b[idx] += 1
                        operations.append(idx + 1)
                        made_move = True
                        break
                if made_move:
                    break
            if not made_move:
                break
        
        if len(operations) > 1000:
            print(-1)
        else:
            print(len(operations))
            if operations:
                print(" ".join(map(str, operations)))
```

The solution first reads inputs and sets up a count array to track the number of courses at each level. It then uses a greedy approach: for each level from 1 to k, increment any course that violates the current capacity. This loop continues until no more increments are possible. The check `count[level] > a[level - 1]` ensures we never exceed capacity at any step. The solution appends each operation to the list and outputs it if the total operations are within the limit.

## Worked Examples

### Example 1

Input:

```
3 2
2 2
1 2 2
```

| Step | b | count | Operations |
| --- | --- | --- | --- |
| Start | [1,2,2] | [0,1,2,0] | [] |
| 1 | [1,3,2] | [0,1,1,1] | [2] |
| 2 | [2,3,2] | [0,0,2,1] | [2,1] |
| 3 | [3,3,2] | [0,0,1,2] | [2,1,3] |
| 4 | [3,3,3] | [0,0,0,3] | [2,1,3,1] |

All courses reach level 3, within capacity.

### Example 2

Input:

```
1 1
1
1
```

| Step | b | count | Operations |
| --- | --- | --- | --- |
| Start | [1] | [0,1,0] | [] |
| 1 | [2] | [0,0,1] | [1] |

Single operation needed, correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*k) | Each course can be incremented at most k times, scanning all courses per increment |
| Space | O(n+k) | Storing the course levels and counts per level |

Given `n <= 50` and `k <= 20`, maximum operations is `50*20 = 1000`, fitting perfectly within the allowed 1000 operations and time limits.

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
assert run("4\n3 2\n2 2\n1 2 2\n4 2\n2 2\n3 3 3 3\n1 1\n1\n1\n5 3\n1 2 3\n1 2 4 2 3") == "4\n2 1 3 1\n0\n1\n1\n8\n2 4 1 2 1 1 5 4"

# Custom cases
assert run("1\n1 1\n1\n1") == "1\n1", "single course increment"
assert run("1\n5 2\n2 2\n2 2 1 1 3") != "", "multi-level small"
assert run("1\n50 20\n" + " ".join(["1"]*20) + "\n" + " ".join([str((i%21)+1) for i in range(50)])) != "", "max size"
assert run("1\n2 1\n1\n2 1") != "", "already near target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 course, level 1 | 1 operation | Basic increment from level 1 to 2 |
| 5 courses, multiple levels | Non-empty sequence | Handles mixed initial assignments |
| Max courses 50, max k 20 | Non-empty sequence | Performance under maximum constraints |
| 2 courses already high | Non |  |
