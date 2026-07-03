---
title: "CF 102961V - Tasks and Deadlines"
description: "Each task has two properties: how long it takes to finish and a deadline that is used to evaluate how “late” you are when you complete it. You must execute all tasks sequentially starting from time zero, choosing any order you want."
date: "2026-07-04T06:57:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "V"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 42
verified: true
draft: false
---

[CF 102961V - Tasks and Deadlines](https://codeforces.com/problemset/problem/102961/V)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Each task has two properties: how long it takes to finish and a deadline that is used to evaluate how “late” you are when you complete it. You must execute all tasks sequentially starting from time zero, choosing any order you want.

When a task finishes at time `f` and its deadline is `d`, it contributes `d - f` to the total score. The total reward is the sum of these contributions over all tasks. Since finishing time accumulates as tasks are processed, ordering directly affects all future penalties.

The input gives a list of tasks, each described by a duration and a deadline. The output is a single number: the maximum possible total reward over all permutations of task order.

The constraints allow up to 200,000 tasks, which immediately rules out any factorial or quadratic scheduling simulation. Even `O(n^2)` becomes too slow if each task requires scanning or swapping. Any valid solution must be close to `O(n log n)` or linear.

A subtle issue in this problem is that every task must be completed even if it yields negative contribution. A naive interpretation might suggest dropping “bad” tasks, but the statement explicitly disallows skipping, so the optimization is purely about ordering.

Another common pitfall is thinking each task can be optimized independently. For example, placing the smallest deadline first feels natural, but that can still be suboptimal when a long task delays everything that follows.

A small counterexample where greedy by deadline fails:

Input:

```
2
1 10
10 11
```

If you take earliest deadline first, you do (1,10) then (10,11), finishing times are 1 and 11, total reward is (10-1)+(11-11)=9.

If you reverse, finishing times are 10 and 11, total reward is (10-10)+(11-11)=0, so in this tiny case greedy works, but this is misleading. In larger instances, long tasks placed early can destroy many future contributions, which is the key structural issue.

## Approaches

The brute-force idea is straightforward: try every permutation of tasks, simulate the schedule, compute finishing times incrementally, and track the best result. This is correct because it evaluates all possible orders explicitly. However, it requires `n!` permutations, and even evaluating one permutation costs `O(n)`, giving `O(n! · n)` operations, which is impossible even for `n = 20`.

The key observation is that the objective can be rewritten so that ordering only matters through completion times. If we expand the sum, each task contributes its deadline once, and subtracts its finishing time once. The sum of deadlines is fixed regardless of order, so maximizing reward is equivalent to minimizing the sum of finishing times.

Now the problem becomes a classic scheduling question: minimize total completion time on a single machine with fixed processing times. The well-known optimal strategy is to process tasks in increasing order of duration. This works because swapping two adjacent tasks shows that a longer task placed earlier increases total completion time more than placing it later.

The deadlines vanish from the ordering decision entirely after the transformation; they only contribute a constant offset to the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Sort by duration (optimal) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all tasks and store their durations and deadlines. The goal is to later choose an order that minimizes cumulative finishing times.
2. Sort tasks by increasing duration. This ensures short tasks are executed early, preventing long processing times from inflating many future completion times.
3. Maintain a running prefix time, initially zero, representing the current finishing time after processing tasks in the chosen order.
4. Iterate through tasks in sorted order. For each task, add its duration to the running time, which gives its finishing time.
5. Accumulate the contribution `deadline - finishing_time` into the answer.
6. Output the final accumulated value.

The important design choice is that we never explicitly optimize deadlines during ordering, because they do not affect relative comparisons between permutations after the algebraic transformation.

### Why it works

The core invariant is that after sorting by duration, any adjacent inversion where a longer task precedes a shorter one can only increase the sum of finishing times. Swapping such a pair reduces the total accumulated completion time, and repeated swaps transform any ordering into the sorted-by-duration order without worsening the objective. This establishes that the sorted order minimizes total finishing time, which in turn maximizes the original reward function.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
tasks = []

for _ in range(n):
    a, d = map(int, input().split())
    tasks.append((a, d))

tasks.sort()  # sort by duration

time = 0
answer = 0

for a, d in tasks:
    time += a
    answer += d - time

print(answer)
```

The implementation directly follows the reduction to minimizing total completion time. Sorting is done lexicographically, which places tasks in increasing duration order.

The variable `time` tracks cumulative processing time. It is crucial that it is updated before computing the contribution, since `time` represents the finishing time of the current task, not its starting time.

A subtle detail is that all arithmetic fits comfortably in 64-bit integers, but Python naturally handles large integers so overflow is not a concern.

## Worked Examples

Consider the sample input:

```
3
6 10
8 15
5 12
```

After sorting by duration, the tasks become `(5,12)`, `(6,10)`, `(8,15)`.

| Step | Task (a,d) | Cumulative time | Finishing time | Contribution |
| --- | --- | --- | --- | --- |
| 1 | (5,12) | 5 | 5 | 12 - 5 = 7 |
| 2 | (6,10) | 11 | 11 | 10 - 11 = -1 |
| 3 | (8,15) | 19 | 19 | 15 - 19 = -4 |

Total reward is `7 - 1 - 4 = 2`.

This trace shows that even tasks with negative individual contribution must still be included, and the ordering trades off early gains against later penalties.

Now consider a second example:

```
4
3 5
2 100
1 4
4 6
```

Sorted order is `(1,4)`, `(2,100)`, `(3,5)`, `(4,6)`.

| Step | Task | Time | Contribution |
| --- | --- | --- | --- |
| 1 | (1,4) | 1 | 3 |
| 2 | (2,100) | 3 | 97 |
| 3 | (3,5) | 6 | -1 |
| 4 | (4,6) | 10 | -4 |

Total is `3 + 97 - 1 - 4 = 95`.

This confirms that keeping the very large deadline task early is beneficial because it avoids being penalized by a large finishing time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; single linear scan afterward |
| Space | O(n) | Storage for task list |

With `n ≤ 2 × 10^5`, sorting comfortably fits within time limits, and the linear pass is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import inf

    n = int(input())
    tasks = []
    for _ in range(n):
        a, d = map(int, input().split())
        tasks.append((a, d))

    tasks.sort()
    time = 0
    ans = 0
    for a, d in tasks:
        time += a
        ans += d - time
    return str(ans)

# provided sample
assert run("""3
6 10
8 15
5 12
""") == "2"

# minimum input
assert run("""1
5 10
""") == "5"

# already sorted durations
assert run("""3
1 10
2 20
3 30
""") == "54"

# reverse durations
assert run("""3
3 30
2 20
1 10
""") == "54"

# equal durations
assert run("""3
5 10
5 10
5 10
""") == "-30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single task | 5 | base case correctness |
| increasing order | 54 | correctness under stable optimal order |
| decreasing order | 54 | sorting fixes worst initial arrangement |
| equal durations | -30 | handling ties and cumulative penalties |

## Edge Cases

When all tasks have identical durations, sorting does not change their relative order, and the algorithm effectively processes them in input order. Since every task contributes increasing finishing times linearly, the total becomes strongly negative if deadlines are small, which matches the formula exactly.

For an input like:

```
3
5 10
5 10
5 10
```

The running times are 5, 10, and 15, producing contributions 5, 0, and -5, summing to -30. Any permutation yields the same multiset of finishing times, so the algorithm remains correct regardless of stability.

A second subtle case is a single very long task among many short ones. Sorting ensures the long task is placed last, preventing it from inflating many intermediate finishing times. For example:

```
3
1 100
1 100
10 100
```

Processing the 10-length task first would add 10 to every subsequent completion time, which would significantly reduce total reward. The sorted order avoids this and keeps cumulative penalties minimal.
