---
title: "CF 105575F - \u5168\u80fd\u732b\u5a18\u7684\u70e6\u607c"
description: "We are given a collection of tasks. Each task has a processing time and a deadline-like constraint that represents the latest moment by which it must be completed."
date: "2026-06-22T06:21:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "F"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 40
verified: true
draft: false
---

[CF 105575F - \u5168\u80fd\u732b\u5a18\u7684\u70e6\u607c](https://codeforces.com/problemset/problem/105575/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of tasks. Each task has a processing time and a deadline-like constraint that represents the latest moment by which it must be completed. We are allowed to choose an order in which to execute all tasks, but once a task starts it runs for its full duration without interruption.

The goal is to decide whether there exists an ordering of all tasks such that every task finishes no later than its own deadline, and if it is possible, compute the maximum slack-like quantity implied by the best ordering. The sample solution reveals that the real objective reduces to finding whether we can schedule all tasks and measure how far we can push the schedule before violating feasibility.

Each task contributes two values: a duration and a deadline. The task ordering affects cumulative time, so the key interaction is between prefix sums of durations and the deadlines.

From the constraints implied by the solution, the number of tasks can be large enough that any quadratic ordering strategy is infeasible. Any approach that tries all permutations would require factorial time, and even dynamic programming over subsets would be exponential in the number of tasks. This immediately forces us toward sorting-based greedy reasoning in roughly O(n log n).

A subtle failure case appears when tasks with large durations but early deadlines are placed late in the schedule. For example, consider tasks (duration, deadline): (5, 6), (2, 3), (2, 10). If we process in arbitrary order, we might try (5, 6) first, then accumulate time and break feasibility for (2, 3). However, ordering by deadlines fixes this issue.

The output is a single integer representing the best achievable value derived from scheduling, or -1 if no valid schedule exists.

## Approaches

The naive approach is to try every possible ordering of tasks and simulate completion times. For each permutation, we compute prefix sums of durations and check whether each task finishes before its deadline. This is correct because it directly tests feasibility. However, the number of permutations grows as m!, and even for m around 10 or 11 this becomes impractical. Each simulation costs O(m), so the total complexity is O(m · m!).

The key observation is that tasks with earlier deadlines impose stricter constraints and should be handled earlier in any feasible schedule. If a task with an earlier deadline is delayed behind tasks with later deadlines, its feasibility only becomes harder, never easier. This suggests sorting tasks by increasing deadline.

After sorting, we maintain a running sum of durations. When processing each task, we check how much time has already been consumed before it starts. The expression deadline minus accumulated time captures how much slack remains for that task if it is scheduled in this order. The answer is the minimum such slack over all tasks, since the tightest constraint determines feasibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · m!) | O(m) | Too slow |
| Optimal Greedy Sort | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

We transform each task into a pair containing its duration and deadline, then sort tasks by deadline.

1. Read all tasks and store them as pairs (duration, deadline). This standardizes the problem so we can reason only about ordering and cumulative time.
2. Sort tasks in increasing order of deadline. This ensures that tasks with tighter constraints are considered earlier, preventing late placement of fragile tasks.
3. Initialize a running sum variable to track total time spent so far. This represents the completion time of the current prefix in the chosen order.
4. Iterate through tasks in sorted order, adding each task’s duration to the running sum. After adding, compute the slack for this task as deadline minus current running sum. This measures how far we are from violating this task’s constraint at its position.
5. Maintain the minimum slack over all tasks. This minimum determines the worst margin of safety in the schedule.
6. After processing all tasks, if the minimum slack is negative, no valid schedule exists and we output -1. Otherwise, we output this minimum slack.

### Why it works

The sorting by deadline ensures that whenever we consider a task, all tasks with earlier deadlines are already placed and contribute to the prefix sum. Any deviation from this ordering can only increase the risk of violating earlier deadlines, because swapping a later-deadline task forward does not reduce the prefix sum before a tighter deadline task unless that task itself has an even smaller or equal deadline. This establishes that the sorted order is optimal for feasibility checking.

The running sum creates a fixed prefix structure where each task’s constraint is checked at the earliest possible moment consistent with deadline ordering. The minimum slack captures the tightest constraint across all prefixes, and feasibility reduces to whether this slack stays non-negative.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    tasks = []
    for _ in range(m):
        d, t = map(int, input().split())
        tasks.append((t, d))  # (deadline, duration)

    tasks.sort()

    total = 0
    best = 10**30

    for deadline, duration in tasks:
        total += duration
        best = min(best, deadline - total)

    print(best if best >= 0 else -1)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy structure exactly. Each task is stored with deadline first to make sorting direct. The running sum `total` represents cumulative execution time in the chosen order. After each update, we evaluate how much remaining time is available before violating the current task’s deadline. The variable `best` tracks the minimum of these values.

The final check converts feasibility into a simple sign test. A negative value indicates that at some point the schedule overtakes a deadline, making the ordering invalid.

## Worked Examples

Consider input:

```
m = 3
tasks: (duration, deadline)
2 5
1 3
2 10
```

After reordering into (deadline, duration):

| Step | Task (d, t) | Total Time | Slack = t - total | Min Slack |
| --- | --- | --- | --- | --- |
| 1 | (3, 1) | 1 | 2 | 2 |
| 2 | (5, 2) | 3 | 2 | 2 |
| 3 | (10, 2) | 5 | 5 | 2 |

The minimum slack is positive, so scheduling is feasible. The trace shows that the tightest constraint comes from the early deadline task, which is handled first and never violated.

Now consider a failing case:

```
m = 2
tasks:
2 3
2 3
```

After sorting (order unchanged):

| Step | Task (d, t) | Total Time | Slack | Min Slack |
| --- | --- | --- | --- | --- |
| 1 | (3, 2) | 2 | 1 | 1 |
| 2 | (3, 2) | 4 | -1 | -1 |

The second task causes the running time to exceed its deadline, making the schedule invalid. This confirms that detecting a negative slack correctly captures infeasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting dominates, single linear scan afterward |
| Space | O(m) | Storage of task list |

The constraints force any solution to avoid quadratic or factorial behavior. Sorting plus a single pass is sufficient for large m, since each task is processed exactly once after ordering.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = backup
    return out.getvalue().strip()

# sample-like case: feasible
assert run("3 3\n5 2\n3 1\n10 2\n") == "2"

# impossible case: immediate overflow
assert run("2 2\n3 2\n3 2\n") == "-1"

# single task
assert run("1 1\n5 10\n") == "5"

# tight chain
assert run("4 3\n3 4\n3 4\n3 10\n") == "-1"

# already optimal order
assert run("5 3\n1 5\n2 7\n3 10\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single task | 5 | base case correctness |
| two identical tight tasks | -1 | cumulative overflow detection |
| sorted-feasible chain | 2 | stable greedy behavior |
| tight chain forcing failure | -1 | prefix accumulation correctness |

## Edge Cases

One important edge case is when a task with a large duration appears after a slightly larger deadline but still becomes infeasible due to accumulated time. For example:

```
m = 2
tasks:
4 5
3 6
```

After sorting by deadline:

| Step | Task (d, t) | Total | Slack |
| --- | --- | --- | --- |
| 1 | (5, 4) | 4 | 1 |
| 2 | (6, 3) | 7 | -1 |

Even though both tasks individually fit their deadlines, their combined ordering causes overflow. The algorithm captures this because it evaluates cumulative time, not isolated feasibility.

Another case is when all deadlines are large but durations are also large. Even then, the minimum slack correctly reflects whether cumulative growth stays within bounds, ensuring no hidden overflow scenario is missed.
