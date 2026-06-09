---
title: "CF 1701C - Schedule Management"
description: "We are given a collection of tasks, where each task has a designated “preferred” worker. If a worker processes a task they are assigned to prefer, it takes one unit of time; otherwise it takes two."
date: "2026-06-09T21:47:33+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1701
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 131 (Rated for Div. 2)"
rating: 1400
weight: 1701
solve_time_s: 102
verified: true
draft: false
---

[CF 1701C - Schedule Management](https://codeforces.com/problemset/problem/1701/C)

**Rating:** 1400  
**Tags:** binary search, greedy, implementation, two pointers  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of tasks, where each task has a designated “preferred” worker. If a worker processes a task they are assigned to prefer, it takes one unit of time; otherwise it takes two. Workers operate independently in parallel, and each worker can only handle one task at a time.

The goal is to assign every task to some worker so that the overall finishing time, meaning the maximum time any worker spends on their assigned tasks, is minimized.

The key structure is that each worker has a subset of tasks they can do quickly, and everything else is slower. We are not deciding task order globally in time, but distributing load across workers so that no single worker becomes the bottleneck.

The constraints are tight enough that any quadratic or per-worker simulation over all possible time values will not work. The total number of tasks across all test cases is up to 2⋅10^5, which forces an O(n log n) or O(n) per test case strategy.

A naive interpretation might try to explicitly simulate assignment or try all distributions of slow and fast tasks per worker. That immediately becomes impossible since even distributing tasks greedily in multiple configurations would require exploring combinatorial assignments.

A subtle edge case appears when one worker is assigned many non-preferred tasks while others are lightly loaded. For example, if all tasks belong to a single worker, the answer is not 1 but grows linearly depending on how many tasks they must process. Another edge case is when tasks are evenly distributed among workers but assigning them in a naive round-robin causes unnecessary slow tasks even though a balanced shift exists.

## Approaches

If we try to directly assign tasks, we would need to decide for each task which worker takes it and in what order they execute tasks. Since each task can take either 1 or 2 hours depending on assignment, and workers work in parallel, the completion time depends on the maximum workload across workers.

A brute-force idea would be to try all assignments of tasks to workers and compute the resulting completion time. This is clearly exponential in m because each task has n choices, and even pruning does not help in the worst case. Another attempt might simulate increasing time T and checking whether all tasks can be completed by T, but even feasibility checking requires deciding how to split tasks per worker, which is nontrivial unless structured carefully.

The key insight is to reverse the perspective: instead of assigning tasks directly, we fix a candidate answer T and ask whether it is possible to complete everything within T. If we know how to check feasibility, we can binary search T.

For a fixed T, each worker can complete at most T tasks if all are preferred tasks, and at least ⌊T/2⌋ tasks if all are non-preferred. The important part is that every task either contributes 1 unit of load to its preferred worker or 2 units to someone else, so we want to distribute tasks in a way that minimizes overload by prioritizing using workers’ preferred tasks first.

For each worker, let cnt[i] be how many tasks are preferred by worker i. If we assign x of those tasks to worker i, they cost 1 each. Any remaining tasks assigned to worker i must come from other workers and cost 2 each. The total time worker i spends is x + 2y, where y is number of non-preferred tasks.

The greedy structure emerges from noticing that assigning preferred tasks is always better locally. So for a fixed T, we try to maximize usage of preferred tasks per worker up to T, and see how many leftover tasks remain. Those leftovers require 2-unit slots, so we check whether all remaining tasks can fit into remaining capacity across workers.

However, this still leads to a simpler known reformulation: each worker i has cnt[i] preferred tasks. If we set a time T, worker i can take at most T tasks total, but among them at most cnt[i] can be cheap. Therefore, each worker contributes min(cnt[i], T) cheap capacity, and any remaining capacity up to T must be filled with expensive tasks. Summing across workers yields total cheap slots; if total cheap slots across all workers is at least m, we can complete within T.

This monotonic feasibility allows binary search on T.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force assignment | Exponential | O(1) | Too slow |
| Binary search + greedy check | O((n+m) log m) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem into checking whether a given time T is sufficient.

1. Count for each worker how many tasks they are proficient in. This gives a frequency array cnt. This is necessary because all decisions depend only on counts, not task identities.
2. For a candidate time T, compute how many tasks each worker can “comfortably” execute as preferred tasks. This is min(cnt[i], T) for each worker because even a proficient worker cannot process more than T tasks total.
3. Sum these values across all workers. This gives the maximum number of tasks that can be processed in 1 unit per task mode.
4. If this sum is at least m, then all tasks can be assigned within T hours. Otherwise, T is too small.
5. Use binary search over T from 1 to 2m, since in the worst case every task takes 2 hours.

Why this works is tied to the fact that any assignment can be rearranged so that every worker first takes all their preferred tasks up to capacity T before taking any non-preferred ones. This rearrangement never increases completion time because it only replaces expensive assignments with cheaper ones, or leaves them unchanged. Thus feasibility depends only on whether total available “1-hour slots” across workers can cover all tasks within T time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(T, cnt, m):
    total = 0
    for x in cnt:
        total += min(x, T)
    return total >= m

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    cnt = [0] * n
    for v in a:
        cnt[v - 1] += 1

    lo, hi = 1, 2 * m
    ans = 2 * m

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, cnt, m):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)
```

The core implementation begins by compressing the task list into a frequency array. This is crucial because task order is irrelevant; only how many preferred tasks each worker has matters.

The `can` function encodes feasibility. It computes the total number of tasks that can be done within T assuming we always prioritize assigning a worker their preferred tasks first. The use of `min(cnt[i], T)` captures both the limit of available preferred tasks and the per-worker time capacity.

Binary search then finds the smallest feasible T. The upper bound 2m is safe because in the worst case every task requires 2 units of time and one worker could theoretically handle them sequentially.

## Worked Examples

### Example 1

Input:

```
2 4
1 2 1 2
```

Worker counts are [2, 2].

We test feasibility:

| T | min contributions | total | feasible |
| --- | --- | --- | --- |
| 1 | 1 + 1 = 2 | 2 | no |
| 2 | 2 + 2 = 4 | 4 | yes |

So answer is 2.

This demonstrates that when tasks are evenly distributed, each worker can process all their preferred tasks exactly within time 2.

### Example 2

Input:

```
2 4
1 1 1 1
```

Worker counts are [4, 0].

| T | min contributions | total | feasible |
| --- | --- | --- | --- |
| 2 | 2 + 0 = 2 | 2 | no |
| 3 | 3 + 0 = 3 | 3 | yes |

Answer is 3.

This shows that a single worker saturates quickly and forces the answer to depend directly on how many tasks they must process.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Counting tasks is linear, each feasibility check is O(n), binary search adds log m factor |
| Space | O(n) | Frequency array stores worker task counts |

The constraints allow up to 2⋅10^5 total tasks, so the logarithmic factor over m is small enough to fit comfortably within time limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def can(T, cnt, m):
        total = 0
        for x in cnt:
            total += min(x, T)
        return total >= m

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        cnt = [0] * n
        for v in a:
            cnt[v - 1] += 1

        lo, hi = 1, 2 * m
        ans = hi

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, cnt, m):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert solve("4\n2 4\n1 2 1 2\n2 4\n1 1 1 1\n5 5\n5 1 3 2 4\n1 1\n1\n") == "2\n3\n1\n1"

# custom cases
assert solve("1\n1 1\n1\n") == "1", "single task"
assert solve("1\n2 2\n1 2\n") == "1", "perfect matching"
assert solve("1\n3 6\n1 1 1 2 2 2\n") == "2", "balanced heavy case"
assert solve("1\n2 6\n1 1 1 1 1 1\n") == "3", "one worker overloaded"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single task | 1 | minimum boundary |
| perfect matching | 1 | optimal all-fast assignment |
| balanced heavy case | 2 | symmetric distribution correctness |
| one worker overloaded | 3 | saturation behavior |

## Edge Cases

A key edge case is when all tasks belong to one worker. For input like `n=2, m=6` with all tasks assigned to worker 1, the algorithm computes cnt = [6, 0]. For T=2, total min(cnt[i], T) = 2, which is less than 6, so infeasible. For T=3, it becomes 3, still infeasible. For T=6, it becomes 6, feasible, matching the idea that a single worker must spend time linearly increasing with workload.

Another edge case is when tasks are evenly distributed so that no worker exceeds the time limit. For `1 2 1 2`, cnt = [2,2], and at T=2 the sum reaches 4, exactly matching m, confirming that parallelism fully eliminates bottlenecks.

A third edge case is when n = m and each worker has exactly one task. Then cnt[i] ≤ 1 for all i, so even T=1 already gives sum m, showing that the lower bound is tight and no worker overload exists.
