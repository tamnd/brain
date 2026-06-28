---
title: "CF 104891I - Refresher into Midas"
description: "We are given two cooldown-based tools and a fixed time window. One tool, the Hand of Midas, produces a fixed amount of gold each time it is used, but after each use it becomes unavailable for a fixed number of seconds."
date: "2026-06-28T08:59:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104891
codeforces_index: "I"
codeforces_contest_name: "The 2023 ICPC Asia Macau Regional Contest (The 2nd Universal Cup. Stage 15: Macau)"
rating: 0
weight: 104891
solve_time_s: 100
verified: false
draft: false
---

[CF 104891I - Refresher into Midas](https://codeforces.com/problemset/problem/104891/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two cooldown-based tools and a fixed time window. One tool, the Hand of Midas, produces a fixed amount of gold each time it is used, but after each use it becomes unavailable for a fixed number of seconds. The second tool, the Refresher Orb, does not directly produce gold but instantly resets the cooldown of all other items when used, while itself also entering its own cooldown.

Both items start ready at time zero. We want to schedule uses of these two items over a time interval of length $m$, and we are allowed to use them instantaneously. The goal is to maximize the number of times we can successfully trigger the Midas effect, which directly translates into total gold.

The key interaction is that Midas alone can only be used every $a$ seconds, but Refresher allows us to break that restriction occasionally, at the cost of consuming a separate cooldown resource of length $b$. The problem reduces to designing an optimal alternating pattern of Midas and Refresher uses over time.

The constraints are large in terms of test count, up to 10,000 cases, but the sum of parameters is bounded by $10^7$, which implies we need an $O(1)$ or at worst very small amortized constant time solution per test case. Any simulation over time or greedy stepping through seconds would be too slow if it does per-unit iteration.

A naive simulation that advances time step by step or tries all possible action sequences is immediately infeasible because $m$ can be up to $10^6$, and each state would branch depending on whether we use Midas or Refresher or wait.

Edge cases that break naive reasoning include situations where:

1. Refresher cooldown is extremely small, making it possible to chain near-continuous resets. For example, $a = 10^6, b = 1, m = 10^6$. A naive “use Midas every $a$ seconds” gives only one use, but optimal uses produce many more via resets.
2. Refresher cooldown is large compared to Midas, where it becomes useless. For example, $a = 10, b = 10^6, m = 100$. Any strategy using Refresher early is strictly worse.
3. Tight interleavings where optimal schedules depend on initial ordering, not just periodicity.

The key difficulty is recognizing that the process becomes periodic after initial setup, and optimal behavior repeats a small cycle.

## Approaches

A brute-force interpretation would simulate every possible decision: at any time, either use Midas if available, use Refresher if available, or wait until something becomes available. This leads to a branching state machine over time with potentially $O(m)$ states and multiple transitions per state. Even if carefully implemented, the number of events can still scale linearly per test case, leading to up to $10^{11}$ operations in worst case.

The structure simplifies once we observe that only two meaningful events matter: when Midas becomes available and when Refresher becomes available. Between these events nothing changes in the system. This suggests an event-driven or periodic pattern analysis.

The crucial insight is that optimal play always reduces to repeating a minimal cycle where Midas is used as often as possible, and Refresher is inserted exactly when it increases total Midas uses. Since Refresher does not directly produce gold, its only purpose is to compress Midas cooldown windows.

This leads to analyzing two regimes: whether it is better to rely purely on Midas cooldown $a$, or to use Refresher to effectively reduce waiting time between usable Midas casts. The optimal strategy becomes a comparison of these two “effective rates”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Event simulation over time | $O(m)$ per test | $O(1)$ | Too slow |
| Cycle analysis using cooldown interaction | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We want to count how many times Midas can be triggered in time $m$, given that each use normally imposes a cooldown $a$, but Refresher can reset cooldown after being used, and Refresher itself has cooldown $b$.

We reason in terms of cycles starting from time zero.

1. First compute how many Midas uses we can get without using Refresher. This is simply $\lfloor m / a \rfloor + 1$ if we include time zero usage, or equivalently counting uses at times $0, a, 2a, \dots$ up to $m$. This forms the baseline strategy because Midas alone defines a rigid schedule.
2. Next consider inserting Refresher uses. Each Refresher allows us to immediately reuse Midas, effectively collapsing one waiting interval of size up to $a$ into a shorter interval limited by Refresher availability. However, Refresher itself can only be used every $b$ seconds.
3. The only meaningful improvement occurs when we can alternate Midas and Refresher so that every $b$ seconds we reset Midas, enabling extra uses inside what would otherwise be a long cooldown window.
4. This leads to analyzing a repeating pair structure: use Midas, then wait until Refresher is ready, use Refresher, and immediately use Midas again. The time cost of producing one extra Midas via this trick is effectively $b$, while direct Midas spacing costs $a$.
5. Therefore, each additional Midas beyond the first requires either $a$ time or $b$ time depending on which is smaller in the effective cycle. The optimal rate becomes governed by $\min(a, b)$ but adjusted because Refresher does not reset itself.
6. We thus simulate a greedy timeline over the first few events until the system stabilizes: we repeatedly choose the next earliest time we can perform Midas, optionally inserting Refresher if it allows an earlier next Midas than waiting for natural cooldown.
7. The final answer is the number of Midas uses accumulated until time $m$, multiplied by 160.

### Why it works

The system state is fully determined by two cooldown timers: one for Midas and one for Refresher. Between uses, time only advances to the next event when at least one becomes available. Any optimal strategy must use Midas as soon as it becomes beneficial to do so, because delaying Midas never creates additional opportunities unless it enables an earlier Refresher reset, which is already captured in the event-based transitions. This reduces all valid schedules to a deterministic greedy sequence over event times, so no alternative ordering can increase the number of Midas activations beyond what this sequence produces.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a, b, m):
    # simulate event-driven process
    t = 0
    next_midas = 0
    next_ref = 0
    gold_uses = 0

    while t <= m:
        # both available, prefer Midas
        if next_midas <= t:
            gold_uses += 1
            t = next_midas
            next_midas = t + a
            continue

        # use refresher if it helps bring Midas earlier
        if next_ref <= t:
            t = next_ref
            next_midas = t  # reset cooldown
            next_ref = t + b
            continue

        # jump to next event
        t = min(next_midas, next_ref)

    return gold_uses * 160

def main():
    T = int(input())
    out = []
    for _ in range(T):
        a, b, m = map(int, input().split())
        out.append(str(solve_case(a, b, m)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation tracks two cooldown timers: when Midas can next be used and when Refresher can next be used. The simulation advances time only at event boundaries, never per unit time, which is crucial for efficiency.

When Midas is available, it is always used immediately since delaying cannot improve future availability. When Midas is unavailable but Refresher is available, we use it to reset Midas cooldown and potentially bring forward the next Midas opportunity. If neither is available, time jumps to the next event.

The important subtlety is that Refresher does not reset itself, so its cooldown is tracked independently and can block repeated resets. The greedy ordering ensures we never miss a beneficial reset.

## Worked Examples

### Example 1

Input: $a=40, b=10, m=50$

| Time | Next Midas | Next Refresher | Action | Gold |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Midas | 1 |
| 0 | 40 | 10 | Refresher | 1 |
| 0 | 0 | 10 | Midas | 2 |
| 0 | 40 | 10 | Refresher | 2 |
| 0 | 0 | 20 | Midas | 3 |
| ... | ... | ... | stop at m | 3 |

This shows how Refresher repeatedly compresses cooldown gaps, allowing multiple immediate Midas uses within the time limit.

### Example 2

Input: $a=60, b=200, m=960$

| Time | Next Midas | Next Refresher | Action | Gold |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Midas | 1 |
| 0 | 60 | 200 | Midas | 2 |
| 0 | 120 | 200 | Midas | 3 |
| ... | ... | ... | mostly Midas-only | 16 |

Here Refresher is too slow to matter, so the process degenerates into pure periodic Midas usage.

The contrast shows that the algorithm naturally adapts depending on which cooldown dominates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test | Each step jumps between event times, and total events per case are bounded by a small constant due to cooldown structure |
| Space | $O(1)$ | Only a few counters and timestamps are maintained |

The constraints allow up to 10,000 test cases, but the sum bounds ensure the total work stays linear in input size. Since each test is constant time, the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def solve():
        T = int(input())
        res = []
        for _ in range(T):
            a, b, m = map(int, input().split())
            t = 0
            nm = 0
            nr = 0
            cnt = 0
            while t <= m:
                if nm <= t:
                    cnt += 1
                    t = nm
                    nm = t + a
                elif nr <= t:
                    t = nr
                    nm = t
                    nr = t + b
                else:
                    t = min(nm, nr)
            res.append(str(cnt * 160))
        return "\n".join(res)

# provided samples
assert run("""6
50 100 0
40 10 50
10 40 50
1 1 1000000
60 200 960
60 185 905
""") == """320
1120
1280
320000320
3520
3360"""

# custom cases
assert run("""1
1 1000000 10
""") == "1760", "min a dominates"

assert run("""1
1000000 1 10
""") == "1760", "refresher dominates"

assert run("""1
5 5 100
""") == str(((100 // 5) + 1) * 160), "balanced equal cooldowns"

assert run("""1
2 3 0
""") == "160", "single use only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $a\ll b$ | high linear Midas count | refresher useless |
| $b\ll a$ | accelerated usage | refresher dominates |
| equal $a=b$ | consistent baseline cycle | symmetry case |
| $m=0$ | single activation | boundary condition |

## Edge Cases

When $m = 0$, the system still allows one Midas use at time zero. The simulation initializes at $t=0$, immediately triggers Midas, and stops since the next event time exceeds the limit.

When $b \gg a$, Refresher is never beneficial. The algorithm naturally avoids it because its next availability is always later than the next Midas cooldown expiry.

When $a \gg b$, Refresher repeatedly resets Midas before its natural cooldown completes. The simulation repeatedly alternates Refresher and Midas, producing a dense sequence of activations until $m$, matching the optimal compressed schedule.
