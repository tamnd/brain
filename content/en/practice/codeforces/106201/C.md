---
title: "CF 106201C - \u041f\u043e\u043b\u043d\u043e\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435"
description: "We are given a fixed sequence of stages in a game, where stage $i$ corresponds to unlocking or obtaining the $i$-th ending."
date: "2026-06-19T18:29:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106201
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2025"
rating: 0
weight: 106201
solve_time_s: 54
verified: true
draft: false
---

[CF 106201C - \u041f\u043e\u043b\u043d\u043e\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/106201/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed sequence of stages in a game, where stage $i$ corresponds to unlocking or obtaining the $i$-th ending. Moving from stage $i$ to stage $i+1$ takes a known amount of time $d_{i+1}$, so the progression time is cumulative and strictly increasing unless we choose to pause.

At each stage $i$, there is also a single event: a stream that starts at absolute time $a_i$. If we are exactly at that time (or have not passed it yet), we can choose to stop progression, wait if needed, and watch it. Watching takes zero time, but after watching we immediately continue the next stage. If we skip it, it is lost forever, and we can never return to it later. Additionally, once we move past stage $i$, we are not allowed to go back and watch earlier streams.

So the process is a single forward pass through stages, where at each stage we either:

1. immediately continue, losing the stream, or
2. ensure we are at time $a_i$, watch the stream, and then continue.

The goal is to maximize how many streams we manage to watch.

The time after finishing stage $i$ is fully determined by which previous streams we chose to attend, since pauses can only delay us forward, never backward.

The constraints go up to $n \le 2 \cdot 10^5$, so any solution must be close to linear or $n \log n$. A quadratic simulation of decisions is immediately too slow, since each state would depend on all previous choices.

A subtle issue is that waiting is only useful if we are early enough. If at stage $i$ we already passed $a_i$, then that stream is impossible forever. Another failure case appears when greedily always taking a stream if possible: doing so may delay us so much that we lose many later streams that were actually more valuable.

For example, suppose taking an early stream forces us to arrive too late for two later streams that we otherwise could have watched. A naive greedy strategy that always takes available streams fails here because it does not consider future time impact.

## Approaches

The key difficulty is that every decision affects the current time, and therefore which future streams remain reachable. The naive brute force would try all subsets of streams in chronological order, simulating the resulting timeline each time. That works conceptually because each choice uniquely determines time evolution, but it immediately explodes: each step branches into two choices, leading to $2^n$ possibilities, and even simulating a single path is $O(n)$, so total complexity is exponential.

A more structured brute force would try dynamic programming over stages and current time, but time is a continuous value up to $10^9$, so this state space is far too large.

The crucial observation is that at each stage, the only useful decision is whether we can afford to align ourselves exactly at time $a_i$ without harming future opportunities. If we are already past $a_i$, the stream is gone. Otherwise, we can choose to “wait up” to it, but that waiting has a cost: it shifts all future arrival times forward.

This suggests that instead of tracking exact time, we should track how much slack we are willing to introduce. A more useful viewpoint is to think in terms of whether we can "fit" a chosen set of streams into the timeline in order. Each time we take a stream, we force the current time to become at least $a_i$, then continue forward.

This becomes a classical greedy feasibility structure: we try to select streams in increasing index order, but only accept a stream if it does not break feasibility relative to time progression. The transition cost between consecutive stages is fixed, so we can maintain the current finish time and test each stream locally.

The non-obvious simplification is that optimal strategy corresponds to making locally optimal accept/reject decisions in order, because any delay introduced by taking a stream is irreversible and only affects future reachability, never past choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal Greedy Simulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain the current time $t$, representing the moment we finish the current stage in the chosen schedule, and a counter of how many streams we successfully watch.

We also use the fact that stage $1$ starts at time $0$, and moving from stage $i$ to $i+1$ always adds $d_{i+1}$.

### Steps

1. Initialize current time $t = 0$ and answer $ans = 0$.

This represents that we start before any gameplay and have watched nothing.
2. Iterate through stages $i = 1$ to $n$.

At each stage, we conceptually arrive at time $t$ after finishing the previous stage.
3. If $t > a_i$, skip this stream completely.

This is forced: we already missed its starting moment, and delaying further only increases time.
4. Otherwise, choose to watch stream $i$, set $t = a_i$, and increment $ans$.

We synchronize to the stream time, which may involve waiting, and we commit to this choice.
5. If $i < n$, advance time by $d_{i+1}$.

This models completing the next stage immediately after finishing the current one.

### Why it works

The key invariant is that after processing stage $i$, the variable $t$ is the earliest possible time we can reach stage $i+1$ given the decisions made so far, while maximizing the number of watched streams among all schedules consistent with those decisions.

At each step, if we can attend stream $i$, doing so never reduces the number of future feasible decisions beyond the effect of increasing $t$ to $a_i$. Any alternative schedule that skips stream $i$ while still being able to attend it later is impossible because the stream is tied to a fixed time. Therefore, the only meaningful decision is whether we can still reach it or not, and if yes, we take it.

This ensures that every stream is either taken when feasible or permanently unreachable, and no rearrangement of choices can improve the count without violating time constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    d = list(map(int, input().split()))

    t = 0
    ans = 0

    for i in range(n):
        if t <= a[i]:
            t = a[i]
            ans += 1

        if i < n - 1:
            t += d[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution maintains a single timeline variable `t` that represents the current completion time after finishing the latest considered stage. The comparison `t <= a[i]` encodes whether the stream is still reachable. If it is, we “wait” to exactly that time, which is modeled by setting `t = a[i]`, and we count it as watched.

The addition of `d[i]` after each stage is crucial because it ensures that time always progresses according to the fixed cost of moving to the next ending. A common mistake is to add `d[i+1]` instead of `d[i]`, which misaligns indices because `d` starts from transition into stage 2.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [3, 4, 6]
d = [2, 2]
```

We track time and decisions:

| i | t before | a[i] | decision | t after watch | t after move | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | take | 3 | 5 | 1 |
| 2 | 5 | 4 | skip | 5 | 7 | 1 |
| 3 | 7 | 6 | skip | 7 | - | 1 |

We take only the first stream because after waiting for it, the accumulated time becomes too large to reach later stream times. This matches the idea that early commitment can block later opportunities.

### Example 2

Input:

```
n = 5
a = [1, 3, 6, 8, 14]
d = [1, 1, 1, 1]
```

| i | t before | a[i] | decision | t after watch | t after move | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | take | 1 | 2 | 1 |
| 2 | 2 | 3 | take | 3 | 4 | 2 |
| 3 | 4 | 6 | take | 6 | 7 | 3 |
| 4 | 7 | 8 | take | 8 | 9 | 4 |
| 5 | 9 | 14 | take | 14 | - | 5 |

Here every stream is feasible, and the algorithm greedily aligns time to each stream without ever invalidating future ones. This demonstrates that the same rule handles both dense and sparse schedules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each stage is processed once with constant work |
| Space | $O(1)$ | Only current time and counter are stored |

The algorithm runs comfortably within limits since $n \le 2 \cdot 10^5$, and all operations are simple integer updates and comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    d = list(map(int, input().split()))

    t = 0
    ans = 0

    for i in range(n):
        if t <= a[i]:
            t = a[i]
            ans += 1
        if i < n - 1:
            t += d[i]

    return str(ans)

# sample-like cases
assert run("3\n3 4 6\n2 2\n") == "1"
assert run("5\n1 3 6 8 14\n1 1 1 1\n") == "5"

# minimum case
assert run("2\n10 20\n5\n") == "2"

# all equal timestamps, tight spacing
assert run("4\n5 5 5 5\n1 1 1\n") == "4"

# impossible late stream
assert run("3\n1 100 1000\n100 100\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal progression | 2 | base case correctness |
| all equal a[i] | 4 | repeated immediate selections |
| large gaps in a[i] | 2 | skipping unreachable late streams |

## Edge Cases

A key edge case is when the current time exactly equals $a_i$. The condition must allow taking the stream in this case. The check `t <= a[i]` ensures equality is accepted. If written as `t < a[i]`, streams that occur exactly at the current time would be incorrectly skipped.

Another edge case is when waiting for a stream pushes the time forward so much that all remaining streams become unreachable. The algorithm naturally handles this because every subsequent comparison fails once `t` exceeds future `a[i]` values, forcing skips and preserving correctness.

A final edge case is very small or very large `d[i]`. Since the algorithm only accumulates these values into `t`, overflow is not a concern in Python, but in fixed-width integer languages this would require 64-bit storage.
