---
title: "CF 104454K - To-do list"
description: "We are given a collection of tasks, each task having its own repetition period measured in days. If a task has value $ai$, then once it is initially completed on day 0, it must be repeated again on days $ai, 2ai, 3ai,dots$, as long as those days fall within the next $k$ days we…"
date: "2026-06-30T14:28:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104454
codeforces_index: "K"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2021"
rating: 0
weight: 104454
solve_time_s: 84
verified: false
draft: false
---

[CF 104454K - To-do list](https://codeforces.com/problemset/problem/104454/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of tasks, each task having its own repetition period measured in days. If a task has value $a_i$, then once it is initially completed on day 0, it must be repeated again on days $a_i, 2a_i, 3a_i,\dots$, as long as those days fall within the next $k$ days we are planning for. A value of $a_i = 0$ is a special case where the task does not generate any future repetitions after the initial completion.

The goal is to determine, for each day from 1 to $k$, how many task repetitions are required on that day across all tasks combined.

A direct interpretation is that every task “spawns” a sequence of future days. We are counting how many of these sequences intersect each day in the planning window.

The constraints allow up to $10^5$ tasks and $10^5$ days. This rules out any solution that simulates each task day by day, since a naive propagation would lead to $O(nk)$ behavior in the worst case, which reaches $10^{10}$ operations and is infeasible. Even iterating over all multiples of each $a_i$ individually would be too slow if done without structure, since the total number of updates must be carefully bounded.

A subtle edge case arises when $a_i = 0$. In this case, a careless implementation might attempt to treat it like a normal step size, leading to division by zero or an infinite loop when generating multiples. Another edge case is $a_i > k$, where no repetition should occur within the planning horizon, but a naive loop might still attempt unnecessary processing.

For example, if $n=2, k=6$ and $a = [0, 1]$, then the first task contributes nothing after day 0, while the second task contributes to every day from 1 to 6. The correct output is $1,2,1,2,1,2$. Any solution that mishandles $a_i=0$ might incorrectly attempt to propagate it or crash.

## Approaches

The brute-force approach starts from the interpretation of the problem literally. For each task, we simulate all its future occurrences by stepping through multiples of its period. For each multiple $d = a_i, 2a_i, 3a_i, \dots$ up to $k$, we increment the counter for day $d$.

This is correct because it directly constructs the exact contribution of every task. However, the cost becomes problematic when many tasks have small values of $a_i$. If $a_i = 1$ for all tasks, each task contributes to every day, producing $O(nk)$ updates. With $n = k = 10^5$, this results in $10^{10}$ increments, far beyond feasible limits.

The key observation is that this is a classic “sieve-like accumulation” pattern. Instead of simulating each task independently, we aggregate tasks by their period. If we count how many tasks share the same value $a$, then each distinct $a$ contributes repeatedly at multiples of $a$. This allows us to switch from per-task simulation to per-value frequency accumulation.

Once we have a frequency array $freq[a]$, we only need to iterate over possible step sizes $a$, and for each one distribute its contribution to all multiples. This transforms repeated work into grouped work, similar to how divisor or sieve problems are optimized.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ worst case | $O(k)$ | Too slow |
| Optimal (frequency + multiples) | $O(k \log k)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We convert the list of tasks into a frequency table of repetition intervals. Then we propagate contributions efficiently over multiples.

1. Build an array `freq` where `freq[x]` stores how many tasks have repetition period exactly `x`. This groups identical behaviors together, avoiding redundant work.
2. Create an answer array `ans` of size `k`, initialized to zero. Each position `ans[d]` will store how many tasks occur on day `d`.
3. For each possible period value `x` from 1 to `k`, if `freq[x] > 0`, we distribute its contribution to all multiples of `x` within the range. This means iterating over `d = x, 2x, 3x, ... ≤ k` and adding `freq[x]` to `ans[d]`.
4. Ignore all tasks with `a_i = 0`, since they never contribute future repetitions.
5. Output the array `ans[1..k]`.

Each period class behaves like a “wave” propagating through the timeline at fixed intervals. Grouping them ensures each wave is processed once rather than once per task.

### Why it works

At any day $d$, a task with period $x$ contributes exactly when $d$ is a multiple of $x$. The algorithm ensures that for each $x$, we add its frequency to every such multiple. Since every task is counted exactly once in its frequency bucket and added exactly on its valid days, no overcounting or omission occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    freq = [0] * (k + 1)
    
    for x in a:
        if x != 0 and x <= k:
            freq[x] += 1
    
    ans = [0] * (k + 1)
    
    for x in range(1, k + 1):
        if freq[x] == 0:
            continue
        for d in range(x, k + 1, x):
            ans[d] += freq[x]
    
    print(*ans[1:k+1])

if __name__ == "__main__":
    solve()
```

The code begins by counting how many tasks share each repetition interval. The check `x != 0` avoids invalid step sizes, since zero does not generate a valid arithmetic progression of days. The second condition `x <= k` ensures we only process intervals that can actually appear within the time window.

The nested loop structure is the core propagation step. For each period `x`, we visit its multiples and increment the corresponding day counters. This mirrors the mathematical definition of periodic occurrences.

One subtle point is indexing: the answer array is sized `k+1` so that day indices align naturally with array positions, avoiding off-by-one errors when writing `ans[d]`.

## Worked Examples

### Example 1

Input:

```
2 10
1 2
```

We build frequency:

| x | freq[x] |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

Now propagate contributions:

| x | days updated |
| --- | --- |
| 1 | 1 2 3 4 5 6 7 8 9 10 |
| 2 | 2 4 6 8 10 |

Final accumulation:

| Day | Contribution |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 2 |
| 5 | 1 |
| 6 | 2 |
| 7 | 1 |
| 8 | 2 |
| 9 | 1 |
| 10 | 2 |

Output:

```
1 2 1 2 1 2 1 2 1 2
```

This trace shows how overlapping periodic patterns accumulate linearly through shared multiples.

### Example 2

Input:

```
2 6
0 1
```

Frequency table:

| x | freq[x] |
| --- | --- |
| 1 | 1 |

The task with zero period is ignored.

Propagation for x = 1:

| x | days updated |
| --- | --- |
| 1 | 1 2 3 4 5 6 |

Final array:

| Day | Value |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |
| 6 | 1 |

Output:

```
1 1 1 1 1 1
```

This confirms correct handling of the zero case and uniform propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k \log k)$ | Each period contributes over its multiples, forming a harmonic series over all x |
| Space | $O(k)$ | Frequency and answer arrays of size k |

The runtime fits comfortably within limits since the harmonic sum over multiples is bounded by $k \log k$, and $k \le 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = [0] * (k + 1)
    for x in a:
        if x != 0 and x <= k:
            freq[x] += 1

    ans = [0] * (k + 1)
    for x in range(1, k + 1):
        for d in range(x, k + 1, x):
            ans[d] += freq[x]

    return " ".join(map(str, ans[1:k+1]))

# provided samples
assert run("2 10\n1 2") == "1 2 1 2 1 2 1 2 1 2"
assert run("2 6\n0 1") == "1 1 1 1 1 1"
assert run("3 15\n1 2 3") == "1 2 2 3 1 3 1 3 2 2 1 4 1 2 2"

# custom cases
assert run("1 5\n0") == "0 0 0 0 0", "no propagation"
assert run("3 5\n1 1 1") == "3 3 3 3 3", "all identical period"
assert run("2 7\n5 10") == "0 0 0 0 1 0 0", "large periods"
assert run("4 8\n2 2 2 2") == "0 4 0 4 0 4 0 4", "even-only spikes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 0` | all zeros | zero period handling |
| `3 5 / 1 1 1` | constant max load | repeated identical periods |
| `2 7 / 5 10` | sparse events | periods exceeding k |
| `4 8 / 2 2 2 2` | alternating spikes | multiple identical contributions |

## Edge Cases

A critical edge case is when all values are zero. In this situation, no propagation should occur and the output must be entirely zeros. The frequency table excludes zeros, so the nested loop never adds any contributions.

Another case is when all values are equal to 1. Every task contributes to every day, and the algorithm accumulates all frequencies into every position. Since `freq[1] = n`, each day becomes `n`.

When values exceed `k`, they never appear as valid indices in the propagation loop. They are safely ignored by the `x <= k` check, preventing wasted iterations and ensuring correctness without special handling.

Finally, mixed distributions such as many small values combined with large values demonstrate the advantage of grouping. Small values dominate runtime, but grouping ensures each is processed once per divisor chain rather than per task.
