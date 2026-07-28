---
title: "CF 102739G - \u041f\u043b\u0430\u043d \u0414"
description: "We have n independent subtasks that must be completed during m consecutive days. Each subtask has an allowed time interval: it can be done on any day from si to fi."
date: "2026-07-29T01:09:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102739
codeforces_index: "G"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2020.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102739
solve_time_s: 61
verified: true
draft: false
---

[CF 102739G - \u041f\u043b\u0430\u043d \u0414](https://codeforces.com/problemset/problem/102739/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` independent subtasks that must be completed during `m` consecutive days. Each subtask has an allowed time interval: it can be done on any day from `s_i` to `f_i`. A subtask takes exactly one day unit, meaning several subtasks may be done on the same day, but we want that daily number to be as small as possible.

The goal is to find a schedule where every subtask is assigned to one valid day and the maximum number of subtasks assigned to any single day is minimized. The output is this minimum possible maximum load, followed by one valid distribution of subtasks among the days.

The limits allow up to `300000` subtasks and `300000` days. An approach that checks many possible assignments is impossible because the search space grows exponentially. Even a simulation that tries every subtask on every possible day would require around `n * m`, which is about `9 * 10^10` operations in the largest case. We need a solution close to `O((n + m) log n)` or `O((n + m) log^2 n)`.

The main difficulty is not only deciding whether a certain maximum daily load is possible, but also constructing the actual schedule. A correct solution must handle intervals that overlap heavily, days with no available tasks, and tasks that have only one possible day.

Consider a single task:

```
1 1
```

with one day available. The answer is `1`, because the only task must be done on day one. A solution that initializes the answer from the average load `ceil(n / m)` but forgets impossible concentrated intervals can fail on such cases.

Another example is:

```
3 3
1 1
1 1
1 3
```

The correct answer is `2`. The first two tasks must both be placed on day one, so a maximum load of one is impossible. A careless greedy method that only looks at the total number of tasks per day without considering deadlines can incorrectly claim that one task per day is enough.

A final edge case is:

```
2 5
2 2
5 5
```

The answer is `1`. Days three and four have no work, but that does not matter. Every task only needs one valid day. Implementations that accidentally require every day to receive a task would reject a valid schedule.

## Approaches

The most direct approach is to try to build the schedule while guessing the maximum allowed number of subtasks per day.

Suppose we know the answer is at most `x`. We can test whether this is possible by sweeping through the days from left to right. Every subtask whose starting day has arrived becomes available. Among all available subtasks, we should always choose those with the earliest finishing days. This is the standard earliest deadline greedy rule. If a task expires soon, postponing it is dangerous because later tasks may still have more flexibility.

For a fixed `x`, this greedy check is correct because whenever a schedule exists, moving a chosen task with the smallest deadline to the current day cannot make future days harder. We are using the most urgent tasks first, so no task is unnecessarily lost.

However, testing one value of `x` is not enough. We need the smallest valid value. The answer is monotonic: if a capacity of `x` works, then any larger capacity also works. This allows binary search over the answer.

The brute force version would try every possible capacity and rebuild schedules repeatedly. Trying all capacities up to `n` would be too slow because each feasibility check costs `O((n + m) log n)`, giving about `O(n(n + m) log n)` operations.

The key observation is that the feasibility predicate is monotonic. Binary search reduces the number of checks to about `log n`, and the greedy sweep constructs the schedule during the final successful check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n + m) log n) | O(n + m) | Too slow |
| Optimal | O((n + m) log n log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Store every subtask by its starting day. During a sweep, this allows us to quickly discover which subtasks become available on the current day.
2. Binary search the smallest possible daily capacity `x`. The lower bound is `1`, and the upper bound is `n`, because doing every subtask on one day is always an upper limit if the intervals allow it.
3. For each candidate capacity `x`, perform a left-to-right sweep over all days. Add all subtasks with `s_i` equal to the current day into a min-heap ordered by `f_i`.
4. While the current day still has unused capacity, repeatedly remove the task with the smallest finishing day from the heap and assign it to the current day.
5. If the heap contains a task whose finishing day is smaller than the current day, the candidate capacity is impossible. That task has already missed every possible day.
6. After all days are processed, check whether every task was assigned. If yes, the candidate capacity works and we continue searching for a smaller answer. Otherwise, we increase the capacity.
7. After binary search finds the minimum capacity, run the greedy construction one final time with that capacity and print the resulting assignment.

Why it works:

The invariant during the greedy sweep is that every task currently in the heap is waiting for one of the current or future days. Choosing the smallest deadline first keeps the most restrictive tasks from being delayed. If this greedy process fails, it means some task had no remaining valid position, so no schedule with the tested capacity can exist. If it succeeds, every task has been assigned while respecting both its interval and the daily limit. Binary search then finds the smallest capacity for which this invariant can be maintained.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

n, m = map(int, input().split())
by_start = [[] for _ in range(m + 2)]

for i in range(1, n + 1):
    s, f = map(int, input().split())
    by_start[s].append((f, i))

def check(cap, need_plan=False):
    heap = []
    ans = [[] for _ in range(m + 1)]
    done = 0

    for day in range(1, m + 1):
        for item in by_start[day]:
            heapq.heappush(heap, item)

        if heap and heap[0][0] < day:
            return None

        take = min(cap, len(heap))
        for _ in range(take):
            f, idx = heapq.heappop(heap)
            if need_plan:
                ans[day].append(idx)
            done += 1

        if heap and heap[0][0] < day:
            return None

    if done != n:
        return None

    if need_plan:
        return ans
    return True

lo, hi = 1, n
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):
        hi = mid
    else:
        lo = mid + 1

plan = check(lo, True)

out = [str(lo)]
for day in range(1, m + 1):
    out.append(str(len(plan[day])) + (" " + " ".join(map(str, plan[day])) if plan[day] else ""))

print("\n".join(out))
```

The array `by_start` groups tasks by the first day when they may appear. This avoids scanning all tasks on every day.

The heap stores available tasks ordered by their finishing day. Python compares tuples lexicographically, so `(finish, index)` automatically gives the earliest deadline first while also keeping task numbers available for output.

The function `check` is used both for binary search and for producing the final answer. During binary search it only needs to know whether a capacity works, while the final call records the chosen task numbers.

The deadline check before and after taking tasks prevents a missed task from surviving into a later day. The second check is useful because after assigning the current day's tasks, the next smallest deadline may still already be invalid.

No large integer arithmetic is needed because all counters are at most `300000`.

## Worked Examples

Consider this input:

```
3 3
1 1
1 1
1 3
```

The binary search eventually tests capacity `2`.

| Day | Available tasks | Heap after adding | Assigned today |
| --- | --- | --- | --- |
| 1 | 1, 2, 3 | 1, 1, 3 | 1, 2 |
| 2 | none | 3 | 3 |
| 3 | none | empty | none |

The first two tasks force the capacity to be at least two. The greedy choice handles them immediately because their deadlines are the smallest.

For another example:

```
2 5
2 2
5 5
```

The capacity `1` is tested.

| Day | Available tasks | Heap | Assigned |
| --- | --- | --- | --- |
| 1 | none | empty | none |
| 2 | task 1 | task 1 | task 1 |
| 3 | none | empty | none |
| 4 | none | empty | none |
| 5 | task 2 | task 2 | task 2 |

The trace shows that empty days are allowed. The only requirement is that every task receives a valid day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n log n) | Each binary search iteration performs one heap sweep, and there are O(log n) iterations. |
| Space | O(n + m) | The task buckets, heap, and final schedule all store at most linear information. |

The maximum input size is `300000`, so the algorithm only performs a logarithmic number of linear heap sweeps. This fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io

def solve(data):
    old = sys.stdin
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    by_start = [[] for _ in range(m + 2)]

    for i in range(1, n + 1):
        s, f = map(int, input().split())
        by_start[s].append((f, i))

    import heapq

    def check(cap, plan=False):
        heap = []
        ans = [[] for _ in range(m + 1)]
        cnt = 0

        for day in range(1, m + 1):
            for x in by_start[day]:
                heapq.heappush(heap, x)

            if heap and heap[0][0] < day:
                return None

            for _ in range(min(cap, len(heap))):
                f, idx = heapq.heappop(heap)
                if plan:
                    ans[day].append(idx)
                cnt += 1

        if cnt != n:
            return None
        return ans if plan else True

    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1

    res = check(lo, True)
    out = [str(lo)]
    for i in range(1, m + 1):
        out.append(str(len(res[i])) + (" " + " ".join(map(str, res[i])) if res[i] else ""))

    sys.stdin = old
    return "\n".join(out)

assert solve("""3 3
1 1
1 1
1 3
""").splitlines()[0] == "2"

assert solve("""2 5
2 2
5 5
""").splitlines()[0] == "1"

assert solve("""1 1
1 1
""").splitlines()[0] == "1"

assert solve("""5 5
1 5
1 5
1 5
1 5
1 5
""").splitlines()[0] == "1"

assert solve("""4 4
1 2
1 2
3 4
3 4
""").splitlines()[0] == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three tasks with two fixed to one day | 2 | Forced overlap and deadline handling |
| Two isolated single-day tasks | 1 | Empty days and sparse intervals |
| One task on one day | 1 | Minimum-size case |
| Five identical full-range tasks | 1 | Flexible intervals |
| Two groups of disjoint intervals | 1 | Correct handling of independent ranges |

## Edge Cases

For:

```
1 1
1 1
```

the heap receives the only task on day one and assigns it immediately. Binary search cannot reduce the capacity below one, so the answer is correct.

For:

```
3 3
1 1
1 1
1 3
```

the capacity one check fails. On day one, the greedy algorithm must place one of the two tasks ending on day one, but another task with the same deadline remains. When day two begins, that remaining task is already expired. Capacity two succeeds because both urgent tasks are handled immediately.

For:

```
2 5
2 2
5 5
```

the algorithm leaves days one, three, and four empty. The heap only contains tasks on their allowed days, so no invalid assignment is attempted.

For intervals that cover every day, such as:

```
5 5
1 5
1 5
1 5
1 5
1 5
```

the greedy algorithm can spread tasks across different days. This demonstrates why the answer depends on interval restrictions rather than simply the number of tasks.

I can also adapt this editorial into a shorter Codeforces-style version focused on the core idea and proof if you want.
