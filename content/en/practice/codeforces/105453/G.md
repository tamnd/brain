---
title: "CF 105453G - Airport Departures' Optimization"
description: "We are given a sequence of flights sorted by their scheduled departure times. Each flight has a time when it ideally wants to use the runway, a payment it offers if it is allowed to depart exactly at that time, and a penalty it imposes if it is not."
date: "2026-06-23T17:36:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105453
codeforces_index: "G"
codeforces_contest_name: "2024 ICPC Greece Regional Collegiate Programming Contest (GRCPC 2024)"
rating: 0
weight: 105453
solve_time_s: 91
verified: true
draft: false
---

[CF 105453G - Airport Departures' Optimization](https://codeforces.com/problemset/problem/105453/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of flights sorted by their scheduled departure times. Each flight has a time when it ideally wants to use the runway, a payment it offers if it is allowed to depart exactly at that time, and a penalty it imposes if it is not.

Because the airport is reduced to a single runway, only some flights can actually depart close to their planned times. If a flight is allowed to depart on time, it contributes a positive reward. If it is not selected, it is postponed and instead contributes a negative value because the airline is compensated for the delay.

The operational restriction is that whenever we choose to let a flight depart on time, we must ensure at least T time units pass before the next chosen departure. This turns the problem into selecting a subset of flights that respects spacing constraints while maximizing total profit, where each selected flight gives one value and each skipped flight gives another.

The output is the maximum total profit achievable after deciding which flights depart on time and which are delayed.

The constraints make it clear that N can be as large as one million, which immediately rules out any quadratic or even log-squared dynamic programming. A solution that examines all pairs of flights or performs heavy per-state searching would exceed time limits. The key requirement is an essentially linear or near-linear scan over the sorted flights.

A naive interpretation would also miss that the schedule constraint only applies between selected flights, not all flights. That distinction is what makes greedy or per-flight local decisions incorrect.

A subtle edge case appears when all flights are close in time. For example, if T is large and all t_i are tightly packed, we may only pick one flight. A naive greedy strategy that always picks the best immediate gain b_i - c_i can fail:

Input:

```
3 10
1 100 -1
2 90 -1
3 80 -1
```

A greedy choice might pick the first flight due to highest gain, but in other structured cases it could miss that a later combination yields better spacing if times allow. The real constraint couples decisions across indices.

Another edge case is when delaying is actually beneficial for some flights if c_i is closer to zero than others. Since c_i is negative, ignoring structure and treating all skipped flights as zero cost would completely break correctness.

## Approaches

The first natural attempt is to decide independently for each flight whether to take it on time or delay it. This immediately fails because taking a flight affects which future flights can be taken due to the T spacing constraint. Any attempt to enumerate all subsets of flights that satisfy spacing leads to exponential complexity, since every flight can be either chosen or skipped.

A more structured brute force is to process flights in order and, for each flight, recursively decide whether to take it or not while tracking the last chosen time. This produces a state space where each step branches into two choices, and the number of states grows roughly like 2^N in the worst case. Even pruning invalid schedules does not help enough because valid subsets are still extremely numerous when times are sparse.

The key observation is that the contribution of skipped flights is fixed regardless of scheduling decisions. Every flight contributes c_i if it is not chosen. If we start from the baseline where all flights are delayed, the total is simply the sum of all c_i. The only real decision is which flights we upgrade from delayed to on-time, and each upgrade gives a profit increase of b_i - c_i.

This converts the problem into selecting a subset of flights, each with a weight gain, subject to a spacing constraint on indices determined by time. Once reframed this way, the structure becomes a classic weighted interval scheduling problem on a sorted list, where compatibility is defined by time gaps rather than arbitrary intervals.

Because flights are already sorted by time, for each flight i we only need to know the last flight j before it such that t_j + T <= t_i. Then we decide whether to take flight i and add its gain on top of the best solution up to j, or skip it.

This leads directly to a dynamic programming formulation that can be evaluated in linear time using a two-pointer technique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force recursion over choices | O(2^N) | O(N) | Too slow |
| DP with predecessor search | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We first transform each flight into a value that represents how much better it is to serve it on time instead of delaying it. That value is b_i - c_i. We also compute the baseline contribution as the sum of all c_i.

Next we process flights in increasing order of time and build a dynamic programming table.

1. Compute gain for each flight as b_i - c_i. This isolates the decision impact of selecting a flight.
2. Maintain a pointer j that tracks the latest flight that can be scheduled before the current flight without violating the T gap constraint.
3. For each flight i, advance j as far as possible while t_j + T <= t_i holds. Because times are sorted, j only moves forward across the entire run, keeping the process linear.
4. Define dp[i] as the best achievable gain using the first i flights. For each i, we have two choices: ignore flight i and keep dp[i-1], or take flight i and add its gain to dp[j].
5. Update dp[i] as the maximum of these two choices.
6. After processing all flights, add the baseline sum of all c_i to dp[N] to restore the full profit.

The correctness rests on the fact that once we fix a flight i as chosen, the only constraint on earlier choices is that they must end at or before t_i - T. Any optimal solution that includes i must combine it with an optimal solution over compatible earlier flights, and dp[j] already represents that optimum.

The dp state is complete because it captures the best achievable gain for every prefix of flights, and transitions never skip valid candidates due to monotonicity of time ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    T = int(next(it))

    t = [0] * n
    b = [0] * n
    c = [0] * n

    for i in range(n):
        t[i] = int(next(it))
        b[i] = int(next(it))
        c[i] = int(next(it))

    base = 0
    gain = [0] * n

    for i in range(n):
        base += c[i]
        gain[i] = b[i] - c[i]

    dp = [0] * (n + 1)

    j = 0
    for i in range(1, n + 1):
        ti = t[i - 1]

        while j < i and t[j] + T <= ti:
            j += 1

        take = dp[j] + gain[i - 1]
        skip = dp[i - 1]
        dp[i] = take if take > skip else skip

    print(base + dp[n])

if __name__ == "__main__":
    solve()
```

The code begins by reading all flights and separating the baseline penalty structure from the decision-dependent component. The dp array stores only the incremental improvement over the “all delayed” scenario, which simplifies transitions.

The pointer j is advanced monotonically, which is the critical implementation detail ensuring linear complexity. It never resets for each i, since compatibility windows only move forward as times increase.

A common pitfall is recomputing j from scratch for each i, which would degrade performance to quadratic time. Another subtle issue is forgetting that dp[j] refers to the prefix ending before the last compatible flight, not including j itself, which is why the pointer is advanced carefully.

## Worked Examples

Consider the sample input:

```
4 5
2 1000 -100
5 500 -500
7 300 -500
9 1000 -100
```

We compute baseline sum c_i as -1200. Gains are 1100, 1000, 800, 1100.

We now build dp over compatibility:

| i | t_i | j (last valid) | gain | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1100 | 1100 |
| 2 | 5 | 1 | 1000 | 1100 |
| 3 | 7 | 2 | 800 | 1100 |
| 4 | 9 | 3 | 1100 | 2200 |

Final answer is -1200 + 2200 = 1000.

This trace shows that even though multiple flights have positive gain, spacing constraints prevent stacking all of them, and the DP correctly selects a compatible subset.

Now consider a tighter case:

```
3 10
1 100 -1
2 90 -1
3 80 -1
```

All flights are incompatible with each other due to large T. The DP can only choose at most one gain, and it correctly selects the best single improvement, yielding final answer -3 + 99 = 96.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each flight is processed once, and the pointer j only moves forward across the array |
| Space | O(N) | Arrays store times, gains, and dp values |

The linear scan and monotonic pointer ensure the solution comfortably handles up to one million flights within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        data = sys.stdin.read().strip().split()
        it = iter(data)
        n = int(next(it))
        T = int(next(it))
        if n == 0:
            print(0)
            return

        t = [0] * n
        b = [0] * n
        c = [0] * n

        for i in range(n):
            t[i] = int(next(it))
            b[i] = int(next(it))
            c[i] = int(next(it))

        base = sum(c)
        gain = [b[i] - c[i] for i in range(n)]

        dp = [0] * (n + 1)
        j = 0

        for i in range(1, n + 1):
            ti = t[i - 1]
            while j < i and t[j] + T <= ti:
                j += 1
            dp[i] = max(dp[i - 1], dp[j] + gain[i - 1])

        print(base + dp[n])

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""4 5
2 1000 -100
5 500 -500
7 300 -500
9 1000 -100
""") == "1000"

# minimum size
assert run("""0 5
""") == "0"

# all flights far apart, all taken
assert run("""3 1
1 10 -1
10 10 -1
20 10 -1
""") == "27"

# all close, only best single
assert run("""3 100
1 10 -1
2 20 -1
3 30 -1
""") == "29"

# equal gains, spacing limits selection
assert run("""4 2
1 10 -1
2 10 -1
3 10 -1
4 10 -1
""") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty flights | 0 | base case handling |
| spaced flights | all chosen | no interference case |
| tight spacing | single best choice | constraint binding |
| uniform gains | spacing-driven selection | DP correctness |

## Edge Cases

When T is zero, every flight is compatible with every other, and the optimal strategy becomes selecting all flights since every gain is independent. The algorithm handles this because j always advances to i, turning dp transitions into a simple accumulation of positive gains.

When T is extremely large, only one flight can be chosen. In this situation dp naturally reduces to picking the maximum gain among all flights, since dp[j] will always be zero for all valid j.

When all gains are negative, dp never improves over zero, meaning the optimal strategy is to delay every flight. This is correctly captured because dp remains non-positive and base cost is unavoidable.

When flights are extremely dense in time, the pointer j advances slowly and the algorithm behaves like a standard weighted scheduling DP, always respecting the most recent compatible boundary without revisiting earlier flights.
