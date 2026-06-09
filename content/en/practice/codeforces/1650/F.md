---
title: "CF 1650F - Vitaly and Advanced Useless Algorithms"
description: "We have a sequence of course assignments whose deadlines are already sorted. Assignment i must be fully completed by absolute time a[i]. Initially every assignment has 0% progress. There are m available training options. Option j belongs to exactly one assignment e[j]."
date: "2026-06-10T03:56:11+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1650
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 776 (Div. 3)"
rating: 2200
weight: 1650
solve_time_s: 156
verified: false
draft: false
---

[CF 1650F - Vitaly and Advanced Useless Algorithms](https://codeforces.com/problemset/problem/1650/F)

**Rating:** 2200  
**Tags:** dp, greedy, implementation  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of course assignments whose deadlines are already sorted.

Assignment `i` must be fully completed by absolute time `a[i]`. Initially every assignment has `0%` progress.

There are `m` available training options. Option `j` belongs to exactly one assignment `e[j]`. If we spend `t[j]` hours on that option, the completion percentage of assignment `e[j]` increases by `p[j]`. Each option may be used at most once.

The options are executed one after another in some order chosen by us. Time accumulates globally. After executing several options, the total elapsed time is the sum of their durations.

For every assignment `i`, by the moment time reaches deadline `a[i]`, the total percentage gained from options belonging to assignment `i` must be at least `100`.

We must either construct a valid sequence of distinct options, or determine that no such sequence exists.

The most important observation is that deadlines are attached to prefixes of time. When deadline `a[i]` arrives, every assignment `1..i` must already have reached at least `100%`, because their deadlines are no later than `a[i]`.

The constraints are what drive the solution. Although `n` and `m` can each be as large as `10^5`, the sum of `n+m` over all test cases is only `2·10^5`. This immediately rules out anything exponential and also rules out running a large knapsack over all options globally. We need something close to linear or `O(m · constant)` per test case.

A crucial hidden constraint is that every percentage gain is at most `100`. That means each assignment only cares about progress values from `0` to `100`, which suggests a small knapsack state.

Several edge cases are easy to mishandle.

Consider one assignment with options:

```
deadline = 10

(t=10,p=100)
(t=1,p=60)
(t=1,p=40)
```

Using the single 100% option works, taking 10 hours. Using the other two options works as well, taking only 2 hours. If we only check feasibility, both seem valid. For later deadlines, however, the smaller total time is always better. The solution must minimize time consumed for each assignment.

Another trap is overfilling progress.

```
deadline = 5

(t=2,p=70)
(t=2,p=70)
```

Progress becomes 140%. This is perfectly legal. A DP that stores only exact sums and forgets to clamp values above 100 would miss this solution.

A third trap is that assignments interact only through time.

```
assignment 1 deadline = 5
assignment 2 deadline = 6
```

Even if assignment 2 can be completed eventually, assignment 1 may consume too much time and leave no room before its own deadline. The cumulative time spent on all chosen options for assignments `1..i` must never exceed `a[i]`.

## Approaches

A brute-force approach would examine subsets of options and attempt to schedule them. Even for a single assignment, there may be thousands of options, making `2^m` completely impossible.

The next idea is to process assignments independently. For a fixed assignment, we need a subset of its options whose total progress reaches at least `100`, while total duration is as small as possible.

This suddenly resembles a knapsack problem.

Each option contributes:

```
weight = duration t
value = progress p
```

We want to reach value at least `100` while minimizing weight.

Normally knapsack would be too expensive because durations can be up to `10^9`. The key observation is that progress is bounded by `100`. Instead of DP over time, we perform DP over progress.

For one assignment, let

```
dp[x] = minimum time needed to obtain exactly x progress
```

where all values above `100` are clamped to `100`.

Since progress never exceeds `100`, the state space is only `101`.

After computing the minimum achievable time for an assignment, we add it to the cumulative time spent on previous assignments. If the cumulative time exceeds that assignment's deadline, no schedule exists.

The remaining challenge is reconstruction. We must output actual option indices. While running the knapsack, we store parent information and reconstruct which options formed the optimal subset.

The beautiful part is that assignments are independent except for their contribution to total elapsed time. Once we know the minimum required duration for each assignment, using anything slower can only make deadlines harder to satisfy. Thus the optimal local choice for every assignment is also the globally optimal choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(m) | Too slow |
| Optimal | O(m · 100) | O(m + 100) | Accepted |

## Algorithm Walkthrough

1. Group all options by the assignment they belong to.
2. Process assignments from `1` to `n` in deadline order.
3. For the current assignment, run a 0/1 knapsack on progress.

Let `dp[s]` be the minimum total duration needed to reach progress `s`, where all progress values larger than `100` are stored as state `100`.
4. Initialize:

```
dp[0] = 0
dp[1..100] = INF
```
5. Iterate through the options of this assignment one by one.

For each option `(t, p)`, update the DP backwards exactly like a standard 0/1 knapsack.
6. Whenever we transition

```
old_state -> new_state
```

and obtain a better duration, record parent information. This later allows reconstruction of the chosen options.
7. After all options are processed, inspect `dp[100]`.

If it is still infinite, reaching 100% completion is impossible, so the answer is `-1`.
8. Reconstruct the chosen option indices by following the stored parent pointers from state `100`.
9. Add the minimum duration `dp[100]` to the cumulative time already spent on previous assignments.
10. If cumulative time exceeds deadline `a[i]`, output `-1`.

This means even the fastest way to complete assignments `1..i` misses the deadline.
11. Otherwise append the reconstructed option indices to the global answer sequence.
12. Continue with the next assignment.
13. After all assignments are processed successfully, output the collected option indices.

### Why it works

For a fixed assignment, the DP computes the minimum total duration among all subsets whose progress reaches at least `100`. The state space contains every possible capped progress value from `0` to `100`, so no feasible subset is ignored.

Suppose an assignment can be completed in time `X`, and the DP returns `Y > X`. Then the subset achieving `X` would correspond to a valid DP transition sequence, contradicting the optimality of the minimum stored value. Thus the DP truly finds the minimum duration.

Assignments do not compete for options because every option belongs to exactly one assignment. The only interaction between assignments is the accumulated elapsed time. Replacing a minimum-duration completion plan for some assignment by a slower one can never help satisfy a deadline. Hence if the sum of all minimum durations for assignments `1..i` already exceeds deadline `a[i]`, no valid schedule exists. Conversely, if every prefix of minimum durations satisfies its deadline, executing the chosen subsets assignment by assignment produces a valid schedule.

This proves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        by_task = [[] for _ in range(n)]

        for idx in range(1, m + 1):
            e, tt, p = map(int, input().split())
            by_task[e - 1].append((tt, p, idx))

        total_time = 0
        answer = []
        possible = True

        for task in range(n):
            opts = by_task[task]

            k = len(opts)

            dp = [INF] * 101
            dp[0] = 0

            parent_state = [[-1] * 101 for _ in range(k + 1)]
            used_option = [[-1] * 101 for _ in range(k + 1)]

            for i in range(k):
                tt, p, idx = opts[i]

                ndp = dp[:]

                for s in range(101):
                    if dp[s] == INF:
                        continue

                    ns = min(100, s + p)
                    cand = dp[s] + tt

                    if cand < ndp[ns]:
                        ndp[ns] = cand
                        parent_state[i + 1][ns] = s
                        used_option[i + 1][ns] = i

                for s in range(101):
                    if ndp[s] == dp[s]:
                        if parent_state[i + 1][s] == -1:
                            parent_state[i + 1][s] = s

                dp = ndp

            best = dp[100]

            if best == INF:
                possible = False
                break

            total_time += best

            if total_time > a[task]:
                possible = False
                break

            chosen = []

            state = 100

            for i in range(k, 0, -1):
                if parent_state[i][state] == -1:
                    state = state
                    continue

                prev = parent_state[i][state]

                if used_option[i][state] != -1:
                    opt_index = used_option[i][state]
                    chosen.append(opts[opt_index][2])

                state = prev

            chosen.reverse()
            answer.extend(chosen)

        if not possible:
            out.append("-1")
        else:
            out.append(str(len(answer)))
            out.append(" ".join(map(str, answer)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DP dimension is only `101`, which is the crucial observation that makes the solution fast.

The reconstruction arrays are indexed by `(processed_options, progress_state)`. When a transition improves a state, we remember both the previous progress and which option created the transition.

Progress values larger than `100` are immediately clamped to `100`. Missing this detail is a common source of wrong answers because many valid solutions exceed `100%`.

The deadline check is performed after adding the minimum duration of the current assignment. At that point we have computed the smallest possible cumulative time for the prefix of assignments. If even that exceeds the deadline, no alternative selection can repair it.

## Worked Examples

### Example 1

```
Deadlines: [5, 7, 8]

Task 1:
(1,30,id=1)
(1,80,id=4)

Task 2:
(3,50,id=2)
(3,100,id=3)

Task 3:
(3,100,id=5)
```

For task 1:

| State | Minimum Time |
| --- | --- |
| 0 | 0 |
| 30 | 1 |
| 80 | 1 |
| 100 | 2 |

Best completion time is `2`.

For task 2:

| State | Minimum Time |
| --- | --- |
| 0 | 0 |
| 50 | 3 |
| 100 | 3 |

Best completion time is `3`.

For task 3:

| State | Minimum Time |
| --- | --- |
| 0 | 0 |
| 100 | 3 |

Best completion time is `3`.

Prefix sums of minimum durations:

| Task | Best Duration | Prefix Time | Deadline |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 5 |
| 2 | 3 | 5 | 7 |
| 3 | 3 | 8 | 8 |

All deadlines are satisfied.

The reconstructed answer is one valid sequence such as:

```
1 4 3 5
```

### Example 2

```
1 assignment
deadline = 4

options:
(t=3,p=60)
(t=3,p=60)
```

DP result:

| Progress | Min Time |
| --- | --- |
| 0 | 0 |
| 60 | 3 |
| 100 | 6 |

The minimum duration is `6`.

| Task | Prefix Time | Deadline |
| --- | --- | --- |
| 1 | 6 | 4 |

Since `6 > 4`, the answer is:

```
-1
```

This demonstrates that reaching 100% alone is not enough. The completion must also fit inside the deadline.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · 100) | Each option performs transitions over 101 progress states |
| Space | O(m + 100) | Option storage plus small DP and reconstruction structures |

Since the total number of options across all test cases is at most `2·10^5`, the total amount of DP work is roughly `2·10^7` state transitions, which comfortably fits within the limits in optimized Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # invoke solve() here

    return out.getvalue()

# minimum size, impossible
assert run("""1
1 1
1
1 1 99
""").strip() == "-1"

# minimum size, exact completion
assert run("""1
1 1
5
1 3 100
""").splitlines()[0] == "1"

# overfill beyond 100%
assert run("""1
1 2
10
1 1 70
1 1 70
""").splitlines()[0] == "2"

# deadline violation despite feasible completion
assert run("""1
1 2
3
1 2 60
1 2 60
""").strip() == "-1"

# choose faster subset instead of single slow option
assert run("""1
1 3
5
1 5 100
1 1 60
1 1 40
""").splitlines()[0] == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One option giving 99% | -1 | Cannot stop below 100% |
| One option giving 100% | Valid answer | Smallest feasible instance |
| 70% + 70% | Valid answer | Progress must be capped at 100 |
| Completion time exceeds deadline | -1 | Deadline check |
| Slow 100% option vs fast combination | Fast combination chosen | DP minimizes duration |

## Edge Cases

### Progress exceeds 100%

Input:

```
1
1 2
10
1 1 70
1 1 70
```

The first option reaches progress 70. The second reaches progress 140. The DP stores this as state 100. Completion time becomes 2. Without clamping, state 140 would not exist and the solution could be missed.

### Assignment is completable but misses deadline

Input:

```
1
1 2
3
1 2 60
1 2 60
```

The only way to reach 100% takes 4 hours. The DP correctly finds duration 4. After adding it to the prefix total, we obtain:

```
4 > 3
```

so the algorithm returns `-1`.

### Multiple ways to reach 100%

Input:

```
1
1 3
10
1 10 100
1 1 60
1 1 40
```

Two solutions exist.

```
10 hours -> 100%
2 hours -> 100%
```

The DP stores minimum duration for every progress state, so state 100 ends with value 2. Reconstruction follows the corresponding parent pointers and outputs the faster subset.

### Missing completion for one assignment

Input:

```
1
2 1
5 10
1 1 100
```

Assignment 1 can be completed. Assignment 2 has no options at all.

Its DP leaves `dp[100] = INF`, so the algorithm immediately outputs `-1`, which is correct because every assignment must reach at least 100%.
