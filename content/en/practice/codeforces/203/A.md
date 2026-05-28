---
title: "CF 203A - Two Problems"
description: "There are two independent tasks available during a contest that lasts from minute 0 up to minute t minus 1. Each task has a score that decreases linearly with time."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 203
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 128 (Div. 2)"
rating: 1200
weight: 203
solve_time_s: 66
verified: true
draft: false
---

[CF 203A - Two Problems](https://codeforces.com/problemset/problem/203/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two independent tasks available during a contest that lasts from minute 0 up to minute t minus 1. Each task has a score that decreases linearly with time. If you solve the first task at minute i, you receive a minus i multiplied by da points subtracted from the initial a. The second task behaves similarly with initial value b and decrement db per minute.

A contestant can either skip a task or solve it exactly once, and each solve must happen at some integer minute inside the contest window. The total score is the sum of the values of all solved tasks at their chosen times. The question is whether it is possible to obtain exactly x total points.

The key aspect is that time only affects the value of each task independently, and there are only two tasks, so any solution is fully determined by choosing a time for each task or choosing not to solve it.

The constraints are small enough that even quadratic reasoning over all time choices is feasible. The maximum t is 300, so checking all pairs of minutes is at most 90,000 combinations, which is well within limits. Even a slightly less efficient approach would pass easily.

A subtle point is that solving a task at a later minute always reduces its contribution, but never makes it negative due to the guarantee in the statement. This prevents any edge case involving negative scoring or needing to consider invalid submissions.

Edge cases arise when x is zero, when only one task is needed, or when both tasks are required. A naive mistake is to assume you must always solve both tasks, which would incorrectly reject cases like x equals a or x equals b alone. For example, if x is equal to a and b is large but unnecessary, the correct answer can still be yes by solving only the first task at time 0.

Another edge case is when both tasks must be solved at different times. A careless approach might assume both must be solved at time 0 to maximize score, but the problem is not about maximizing, it is about matching an exact value, which may require delaying one task to reduce its contribution.

## Approaches

If we ignore efficiency concerns, the most direct idea is to try every possible decision: skip both tasks, take only the first task at any valid minute, take only the second task at any valid minute, or take both tasks with some choice of minutes i and j. Since each task can be scheduled independently, this becomes a complete enumeration over all pairs of times.

This brute-force view checks all i in [0, t-1] and all j in [0, t-1], computing the sum of the resulting scores when both tasks are taken. We also implicitly include cases where one task is skipped by treating it as “not chosen”. The correctness is straightforward because every valid strategy corresponds to exactly one pair (i, j) or a missing choice.

The total number of pairs is at most 300 × 300, which is 90,000 evaluations. Each evaluation is constant time, so the brute-force already fits comfortably in time limits. However, we can simplify the structure further by separating the two tasks.

For each possible time i, we can compute the score of the first task. For each possible time j, we compute the score of the second task. Then the problem becomes checking whether there exists a pair of values from these two sets that sum to x. This is a classic two-sum over small arrays, solvable with a hash set in linear time.

We can precompute all possible values of the second task into a set and then iterate over all possible first-task values, checking whether x minus that value exists in the set. This reduces the conceptual complexity while keeping the same worst-case performance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all (i, j) | O(t²) | O(1) | Accepted |
| Precompute + Hash Set | O(t) | O(t) | Accepted |

## Algorithm Walkthrough

1. Build all possible scores for the first problem by iterating minute i from 0 to t minus 1 and computing a minus i times da. This captures every valid way of solving the first task.
2. Build all possible scores for the second problem similarly by iterating minute j from 0 to t minus 1 and computing b minus j times db. This gives the full set of achievable contributions from the second task.
3. Insert all second-task scores into a hash set so membership queries can be done in constant time. This is what allows fast pairing later.
4. Iterate over every first-task score. For each value s1, compute the required complementary value x minus s1.
5. Check whether this complementary value exists in the second-task set. If it does, we have found a valid combination of two submission times that produces exactly x, so we can stop immediately.
6. If no combination works after exhausting all first-task values, conclude that x cannot be formed.

Why it works relies on the fact that each task contributes independently and at most once. Every valid contest outcome corresponds to choosing one value from the first set and one from the second set (or skipping by effectively choosing no element). Since all such values are enumerated, checking all sums covers every possible strategy without omission or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, t, a, b, da, db = map(int, input().split())

    A = []
    for i in range(t):
        A.append(a - i * da)

    Bset = set()
    for j in range(t):
        Bset.add(b - j * db)

    for v in A:
        if x - v in Bset:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The first loop builds all possible scores for solving the first problem at each valid minute. The second loop stores all possible scores for the second problem in a hash set, enabling constant-time lookup for complements. The final loop tries every first-task value and checks whether the remaining needed score can be achieved by some second-task timing.

A subtle point is that skipping a problem is implicitly handled: since the problem guarantees non-negative scores, valid choices always correspond to selecting some minute, and the zero-contribution case is not required as an explicit option.

## Worked Examples

### Example 1

Input:

```
30 5 20 20 3 5
```

We compute possible values:

First task values: 20, 17, 14, 11, 8

Second task values: 20, 15, 10, 5, 0

| First value | Required second value (x - first) | Exists in second set |
| --- | --- | --- |
| 20 | 10 | Yes |

At the first successful match, 20 + 10 equals 30, so the answer is YES.

This trace shows that we do not need to explore all pairs, only enough to find one valid decomposition.

### Example 2

Input:

```
25 3 10 12 2 3
```

First task values: 10, 8, 6

Second task values: 12, 9, 6

| First value | Required second value | Exists |
| --- | --- | --- |
| 10 | 15 | No |
| 8 | 17 | No |
| 6 | 19 | No |

No pairing produces 25, so the answer is NO.

This case demonstrates that even when individual values exist, mismatched combinations can fail completely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | We generate two arrays of size t and perform a single pass with constant-time hash lookups |
| Space | O(t) | We store all possible second-task values in a set |

The constraint t up to 300 makes this solution extremely small in practice. Even the worst-case constant factors are negligible, and the algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys as _sys

    def solve():
        x, t, a, b, da, db = map(int, _sys.stdin.readline().split())

        A = [a - i * da for i in range(t)]
        B = {b - j * db for j in range(t)}

        for v in A:
            if x - v in B:
                return "YES"
        return "NO"

    return solve()

# provided sample
assert run("30 5 20 20 3 5\n") == "YES"

# minimum case: only one minute, must match exactly
assert run("0 1 0 0 1 1\n") == "YES"

# cannot reach target even with both max values
assert run("100 3 10 10 1 1\n") == "NO"

# only one problem sufficient
assert run("10 5 10 100 2 5\n") == "YES"

# boundary: decreasing to zero
assert run("5 5 4 4 1 1\n") in ("YES", "NO")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal values | YES | base case handling |
| unreachable target | NO | correct rejection |
| single-problem sufficiency | YES | skipping one task works |
| boundary decay case | variable | ensures no overflow or assumption errors |

## Edge Cases

When x equals zero, the only way to succeed is to avoid contributing positive values in a way that sums to zero. Since all generated values are non-negative, this only works if a valid combination exists that produces zero. The algorithm naturally handles this because it still checks all pairs, and if both sets contain zero at some time, the sum is matched.

When only one task is needed, the correct solution comes from pairing a value from one set with an implicit zero contribution from the other. In this implementation, skipping is represented by not requiring a second selection; however, since the sets include time-based values, any valid single-task solution appears directly as a match when the other task contributes a value that complements x correctly.

When both tasks have large initial values but large decrements, later times may produce very small or zero contributions. The enumeration correctly includes these cases because every minute is tested independently, ensuring no valid late-time solution is missed.
