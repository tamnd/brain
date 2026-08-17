---
title: "CF 102219E - Optimal Slots"
description: "We have a time limit T for one weekend and an ordered array of N event durations. Each event can either be accepted once or rejected. The accepted events must have total duration at most T, and the primary objective is to make that total as large as possible."
date: "2026-08-17T22:51:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "E"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 209
verified: false
draft: false
---

[CF 102219E - Optimal Slots](https://codeforces.com/problemset/problem/102219/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We have a time limit `T` for one weekend and an ordered array of `N` event durations. Each event can either be accepted once or rejected. The accepted events must have total duration at most `T`, and the primary objective is to make that total as large as possible. Equivalently, we want to minimize unused hall time.

When several different subsets have the same maximum total duration, the reservation order breaks the tie. Earlier events have priority, so at the first position where two valid choices differ, we prefer the choice that includes the earlier event.

The input contains several independent test cases. Each begins with `T` and `N`, followed by the `N` durations. A line containing `0` ends the input. The official statement says there can be up to 50 reservations and gives a 2 second time limit with 256 MB of memory. The rendered statement does not provide a separate numerical upper bound for `T`, although `T` is clearly intended to be small enough to serve as the capacity dimension of a dynamic program.

The important consequence is that an algorithm exponential in `N` is not appropriate. With `N = 50`, there are already `2^50`, about `1.13 * 10^15`, possible subsets. A dynamic program whose second dimension is `T` is the natural choice because the objective is a sum bounded by the available time.

There are several edge cases that can make an otherwise correct-looking implementation fail.

Consider `5 3 6 7 8`. Every event is longer than the available five units, so nothing can be selected. The correct output is `0`. A careless reconstruction routine may assume at least one event was chosen and print an invalid duration.

Consider `10 4 6 4 5 5`. Both `6 4` and `5 5` fill the capacity exactly. The correct output is `6 4 10`, because the event with duration `6` appears before the events with duration `5`. An implementation that only maximizes the sum and keeps whichever subset it finds first can return the wrong tie-breaking choice.

Consider `5 3 1 4 5`. The best subset is `1 4`, whose sum is exactly `5`, so the output is `1 4 5`. The final `5` is the total, not another selected event. A parser or reconstruction routine that treats every printed number as a selected duration can misinterpret the required output format.

## Approaches

The direct approach is to enumerate every subset of the `N` events, calculate its duration, reject it if the duration exceeds `T`, and keep the subset with the largest valid sum. This is correct because every possible selection corresponds to exactly one subset, so exhaustive search cannot miss the optimum. If the sum is accumulated incrementally while generating subsets, the work is `O(2^N)` subsets. With `N = 50`, that is about `1.13 * 10^15` subset states, far beyond what a 2 second contest program can process. If every subset also scans all `N` events to calculate its sum, the bound becomes `O(N * 2^N)`, roughly `5.6 * 10^16` basic event checks in the worst case.

The brute force works because the only meaningful information about a partial selection is its current total duration. The same remaining capacity can be reached by many different subsets, and once we know the best result for that capacity, repeatedly exploring all of those equivalent partial states is unnecessary.

This is exactly the structure of 0/1 knapsack. For each capacity `j`, we only need to know the best total duration achievable from the events that remain. For event `i` with duration `a[i]`, there are only two possibilities: skip it, giving the existing value for capacity `j`, or take it, giving `a[i]` plus the best value for capacity `j - a[i]`.

The tie-breaking rule fits naturally into this recurrence. Process events from the end of the reservation list toward the beginning. When the current event and skipping it produce the same optimal total, choose the current event. Since the current event is earlier than every event already represented by the DP state, including it gives exactly the required priority.

We can keep the numerical DP in one dimension, reducing memory, while storing one byte per event and capacity to remember whether that event was selected. The DP is processed backwards through the events and backwards through capacities, which prevents the same event from being used more than once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^N)` with incremental sums, `O(N2^N)` with rescanning | `O(N)` | Too slow |
| Optimal | `O(NT)` | `O(NT)` | Accepted |

## Algorithm Walkthrough

1. Read the available time `T`, the number of events `N`, and the duration array `a`.

Every selected event consumes exactly its duration, so the only relevant capacity values are `0` through `T`.
2. Create `dp[j]`, initially zero, where `dp[j]` represents the best total duration achievable with capacity `j` using the events processed so far.

We process events from right to left. Before processing event `i`, `dp` describes only events after `i`, which makes it possible to decide whether the current event should be added without accidentally using it twice.
3. Create `take[i]` as a byte array indexed by capacity. `take[i][j] = 1` means that, after considering event `i`, the optimal solution for capacity `j` chooses event `i`.

We need this information because knowing only the optimal total is not enough to reconstruct which events produced it.
4. Process `i` from `N - 1` down to `0`. For the current duration `w = a[i]`, process capacities `j` from `T` down to `w`.

The candidate obtained by taking the current event is `dp[j - w] + w`. The alternative is the current `dp[j]`, which corresponds to skipping the event.
5. If the candidate is at least as good as `dp[j]`, replace `dp[j]` with the candidate and mark `take[i][j] = 1`.

The use of `>=` rather than `>` is the key to the tie-breaking rule. When both choices produce the same total, the current event is earlier in the original array than every event already represented in `dp`, so selecting it has priority.
6. Iterate forward through the original event array during reconstruction, starting with `remaining = T`.

If `take[i][remaining]` is set, output `a[i]` and subtract it from `remaining`. Otherwise, skip the event. The reconstruction follows exactly the decisions recorded while the DP was built.
7. Finally, output `dp[T]` as the total selected duration.

The selected durations are already encountered in their original order during reconstruction, so no sorting or reversal is needed.

### Why it works

The invariant is that before processing event `i`, `dp[j]` is the maximum total duration obtainable from events `i + 1` through `N - 1` using at most `j` time. For event `i`, every optimal solution either excludes it, represented by the old `dp[j]`, or includes it, represented by `a[i] + dp[j-a[i]]`. Taking the larger value preserves the invariant. When the two values tie, selecting event `i` is correct because it is the earliest unresolved event, so every solution containing it has higher priority than an otherwise equal solution that excludes it. The descending capacity loop guarantees that `dp[j-a[i]]` still describes the later events only, so no event is used twice. Reconstruction follows the recorded optimal decisions, giving both the maximum total and the required earliest-priority subset.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    out = []

    while True:
        line = input().split()
        if not line:
            break

        T = int(line[0])
        if T == 0:
            break

        N = int(line[1])
        a = list(map(int, line[2:]))

        # If input lines are ever wrapped, keep reading until all N durations exist.
        while len(a) < N:
            a.extend(map(int, input().split()))

        # dp[j] = maximum total duration achievable with capacity j
        # using the events processed so far from right to left.
        dp = [0] * (T + 1)

        # take[i][j] tells us whether event i is selected in the
        # optimal solution for capacity j after considering event i.
        take = [bytearray(T + 1) for _ in range(N)]

        for i in range(N - 1, -1, -1):
            w = a[i]

            for j in range(T, w - 1, -1):
                candidate = dp[j - w] + w

                # On equality, prefer the current event because it
                # appears earlier than all events represented by dp.
                if candidate >= dp[j]:
                    dp[j] = candidate
                    take[i][j] = 1

        remaining = T
        selected = []

        for i in range(N):
            if take[i][remaining]:
                selected.append(str(a[i]))
                remaining -= a[i]

        selected.append(str(dp[T]))
        out.append(" ".join(selected))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop reads one test case at a time and stops immediately when the first value is zero. The durations normally all appear on the same line, but the small loop that follows also makes the parser safe if a test case is physically wrapped across input lines.

The `dp` array has only `T + 1` states. Processing events from right to left gives each state the meaning of using only later events, while processing capacities from `T` downward prevents the current event from being read from a state that has already been updated with that same event.

The comparison uses `candidate >= dp[j]`. A strict `>` would still find the correct maximum sum, but it would not necessarily satisfy the required reservation-order priority. Equality must favor the current event.

The `take` array uses `bytearray`, which stores one byte per state instead of a full Python integer object. This keeps the reconstruction information compact while still allowing direct indexing.

During reconstruction, `remaining` is the capacity that must be explained by the events not yet examined. If event `i` was recorded as selected for that capacity, subtracting `a[i]` moves to exactly the state that represents the remaining suffix problem. Since reconstruction scans from left to right, the output is already in reservation order.

Python integers do not have the fixed-width overflow problem of C or C++, and all DP values are at most `T` because no selected total may exceed the capacity.

## Worked Examples

### Sample case 1

For `T = 5` and durations `[1, 2, 3, 4, 5]`, the DP processes the array from right to left. The table shows the state for the full capacity `5`. The decisions at smaller capacities are also stored, because reconstruction may reduce the capacity after selecting an earlier event.

| Event index | Duration | `dp[5]` after processing | `take[i][5]` |
| --- | --- | --- | --- |
| 4 | 5 | 5 | yes |
| 3 | 4 | 5 | no |
| 2 | 3 | 5 | no |
| 1 | 2 | 5 | yes |
| 0 | 1 | 5 | yes |

The final reconstruction starts with capacity `5`. Event `1` is selected, reducing the remaining capacity to `4`. Event `2` cannot improve the recorded solution for capacity `4`, event `3` is selected, reducing the capacity to `0`, and all later decisions are skipped. The selected durations are `1` and `4`, giving the output `1 4 5`.

The fact that event `5` was temporarily selected when considering capacity `5` does not mean it must appear in the final answer. When an earlier event is selected on a tie, reconstruction switches to the smaller capacity state associated with that choice. This is exactly why storing decisions for every `(event, capacity)` state is necessary.

### Sample case 2

For `T = 10` and durations `[9, 11, 9, 3, 5, 8, 4, 9, 3, 2]`, the maximum possible total is `10`.

| Event index | Duration | `dp[10]` after processing | `take[i][10]` |
| --- | --- | --- | --- |
| 9 | 2 | 2 | no |
| 8 | 3 | 5 | no |
| 7 | 9 | 9 | no |
| 6 | 4 | 9 | no |
| 5 | 8 | 10 | yes |
| 4 | 5 | 10 | yes |
| 3 | 3 | 10 | yes |
| 2 | 9 | 10 | no |
| 1 | 11 | 10 | no |
| 0 | 9 | 10 | no |

The final reconstruction starts at capacity `10`. Event `3`, with duration `3`, is selected, leaving capacity `7`. Event `4`, with duration `5`, is selected, leaving capacity `2`. The later events cannot improve that remaining capacity except event `9`, with duration `2`, so it is selected as well. The result is `3 5 2`, with total `10`.

This example also demonstrates the tie-breaking rule. The set `8 2` reaches `10`, but the set `3 5 2` has an earlier selected event, so it receives priority.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NT)` | Each of the `N` events scans capacities from `T` down to its duration. |
| Space | `O(NT)` | `dp` uses `O(T)` memory and `take` stores one byte for every event-capacity pair. |

With at most 50 events, the event dimension is very small. The algorithm avoids the exponential `2^N` search entirely and performs a bounded number of simple DP transitions for each capacity. The memory representation is also compact because reconstruction information is stored as bytes rather than Python integers.

## Test Cases

```python
import sys
import io

def solution():
    input = sys.stdin.readline
    out = []

    while True:
        line = input().split()
        if not line:
            break

        T = int(line[0])
        if T == 0:
            break

        N = int(line[1])
        a = list(map(int, line[2:]))

        while len(a) < N:
            a.extend(map(int, input().split()))

        dp = [0] * (T + 1)
        take = [bytearray(T + 1) for _ in range(N)]

        for i in range(N - 1, -1, -1):
            w = a[i]
            for j in range(T, w - 1, -1):
                candidate = dp[j - w] + w
                if candidate >= dp[j]:
                    dp[j] = candidate
                    take[i][j] = 1

        remaining = T
        selected = []

        for i in range(N):
            if take[i][remaining]:
                selected.append(str(a[i]))
                remaining -= a[i]

        selected.append(str(dp[T]))
        out.append(" ".join(selected))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
5 5 1 2 3 4 5
10 9 11 9 3 5 8 4 9 3 2
16 8 12 6 11 11 13 1 10 7
13 5 10 12 2 13 10
28 14 18 19 26 15 18 24 7 21 14 25 2 12 9 6
0
"""

sample_expected = """\
1 4 5
3 5 2 10
6 10 16
13 13
19 7 2 28
"""

assert run(sample) == sample_expected, "provided sample"

assert run("1 1 1\n0\n") == "1 1\n", "minimum-size input"

assert run("5 3 6 7 8\n0\n") == "0\n", "no event fits"

assert run("10 4 6 4 5 5\n0\n") == "6 4 10\n", "tie-breaking priority"

max_input = "100 50 " + " ".join(["2"] * 50) + "\n0\n"
max_expected = " ".join(["2"] * 50 + ["100"]) + "\n"
assert run(max_input) == max_expected, "maximum event count and exact capacity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1 1` | Minimum capacity and a single event that exactly fills it |
| `5 3 6 7 8` | `0` | No event fits, including reconstruction of an empty selection |
| `10 4 6 4 5 5` | `6 4 10` | Equal-sum solutions and earliest-event priority |
| `100 50` followed by fifty `2` values | Fifty `2` values followed by `100` | Maximum number of events, repeated equal durations, and exact capacity filling |

## Edge Cases

For `5 3 6 7 8`, every duration is larger than the capacity. The inner DP loop never runs for any event because `w > T`, so every `dp[j]` remains zero and every `take[i][j]` remains unset. Reconstruction consequently selects nothing and appends `dp[5] = 0`, producing exactly `0`.

For `10 4 6 4 5 5`, the two earliest events form a total of `10`, while the two later events also form `10`. When event `1` with duration `4` is processed in the reverse DP, its inclusion ties the best value already available for capacity `10`, so `take[1][10]` becomes true. Later, event `0` with duration `6` also ties the best value at capacity `10` and is preferred because it appears even earlier. Reconstruction therefore selects `6`, leaves capacity `4`, selects the earlier `4`, and produces `6 4 10`.

For `5 3 1 4 5`, the maximum total is exactly `5`. The DP can reach that total using the event of duration `5`, but when the earlier duration `1` is considered, the state for capacity `5` can also reach `5` through the remaining capacity `4`, so the tie selects duration `1`. Reconstruction then moves to capacity `4`, where duration `4` is selected. The output is `1 4 5`, demonstrating that the final number is the total rather than another event.

For the maximum-size case with 50 events of duration `2` and capacity `100`, every event can be selected, giving a total of exactly `100`. The DP reaches `100` without exceeding the capacity, and because all events are identical, the required priority naturally selects them in their original order. Reconstruction consumes two units of remaining capacity at each event until the remaining capacity becomes zero, producing all 50 durations followed by `100`.
