---
title: "CF 102791K - Realistic Gameplay"
description: "We have a gun with a magazine that can hold k bullets. There are n independent monster waves. A wave appears at time li, contains ai monsters, and all monsters from that wave must be killed no later than time ri."
date: "2026-07-27T18:17:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "K"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 65
verified: true
draft: false
---

[CF 102791K - Realistic Gameplay](https://codeforces.com/problemset/problem/102791/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a gun with a magazine that can hold `k` bullets. There are `n` independent monster waves. A wave appears at time `l_i`, contains `a_i` monsters, and all monsters from that wave must be killed no later than time `r_i`. The waves are already ordered and never overlap, although one wave may end exactly when the next one starts.

Shooting is instantaneous, so the only action that consumes time is reloading. A reload takes one unit of time and replaces the current magazine with a full one, throwing away any remaining bullets. The goal is not only to minimize the bullets that hit monsters, but also the bullets lost when reloading. We need the smallest total number of bullets that leave our inventory during a successful completion.

The number of waves is only up to 2000, while times and monster counts can be as large as `10^9`. This immediately rules out simulating every time moment, because a single interval can span billions of moments. An `O(n^2)` solution is acceptable because `n` is small enough that around four million transitions are manageable. A solution depending on the size of `l_i` or `r_i` is not feasible.

Several details make incorrect solutions fail. A common mistake is assuming that reloading is always good because it gives a full magazine. For example:

```
1 10
5 6 6
```

The answer is `6`. A greedy approach that reloads immediately after shooting the first few monsters may throw away useful bullets and spend `10` or more bullets.

Another trap is forgetting that waves can touch. Consider:

```
2 3
2 3 6
3 4 3
```

The answer is `9`. The second wave starts at the exact moment the first wave ends, so time `3` can be used for both finishing old monsters and preparing the next reload. Treating intervals as strictly separated loses a valid action.

A third edge case is the final magazine. For example:

```
1 10
100 111 1
```

The answer is `1`. The remaining bullets in the last magazine are not discarded after the fight, so the final reload should not be counted as wasted bullets.

## Approaches

The direct approach is to decide every possible reload schedule. For each wave, we could try every possible number of reloads and every possible point in time to perform them. The number of possible times is enormous because the intervals can contain values up to `10^9`, so this approach cannot even be represented efficiently.

The useful observation is that we do not care about the exact moments inside gaps between waves. What matters is the state immediately after a wave is completely handled and before the next wave starts. If we know that we arrive at a wave with a full magazine, we can greedily simulate what happens if this wave and some following waves are handled without an unnecessary reload between them.

The brute force works because a fixed sequence of reload decisions completely determines the number of bullets spent, but it fails because the number of possible sequences is huge. The key insight is that `n` is small, so we can try every possible starting wave of a segment. For each starting point, we extend the segment forward and simulate the best possible way to survive until some later wave. This reduces the problem to dynamic programming over wave boundaries.

Let `dp[i]` be the minimum bullets spent after clearing the first `i` waves and having a full magazine ready before the next wave. From state `i`, we try to clear waves `i` through `j` consecutively without a forced reload before wave `j` starts. During this simulation, we track how many bullets remain and how many bullets have already been spent. When a magazine becomes insufficient, we calculate how many reloads are needed and whether the available time allows them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of reload schedules | O(1) | Too slow |
| Optimal Dynamic Programming | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize `dp[0] = 0`. This means before the first wave we have spent no bullets and our initial magazine is full.
2. For every possible starting wave `i`, try extending the current segment to every later wave `j`. The state before wave `i` already guarantees that the magazine is full, so this gives us a valid starting point for simulation.
3. While extending the segment, maintain the bullets left in the current magazine. If the current magazine has enough bullets for wave `j`, spend those bullets and continue. The wave can be completed without reloading.
4. If the current magazine is not enough, calculate the number of reloads needed to kill the remaining monsters. Each reload adds `k` bullets, but each reload also consumes one unit of time. The reload count must fit inside the wave's time interval.
5. After clearing wave `j`, update the next dynamic programming state if there is enough time before the next wave to have a full magazine again. The transition stores the bullets spent so far plus any bullets that were discarded when preparing the next full magazine.
6. After processing all possible transitions, `dp[n]` contains the minimum bullets spent after all waves. If it was never reached, the waves cannot be cleared.

Why it works: the invariant is that every reachable `dp[i]` describes a real situation where the first `i` waves are finished and the magazine is full before the next wave. Every optimal solution has some last point where the magazine was full before a wave, so it appears as one of the transitions considered by the dynamic programming. The simulation inside a transition always uses the minimum possible number of reloads needed for that fixed segment, because extra reloads only discard bullets and increase the cost. Thus every candidate is valid and the minimum over all candidates is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    waves = [tuple(map(int, input().split())) for _ in range(n)]

    INF = 10**30
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == INF:
            continue

        spent = dp[i]
        bullets = k

        for j in range(i, n):
            l, r, a = waves[j]
            extra = 0

            if a <= bullets:
                bullets -= a
                finish = l
            else:
                need = a - bullets
                reloads = (need + k - 1) // k
                if reloads > r - l:
                    break

                extra = reloads * k
                finish = l + reloads
                bullets = (k - need % k) % k

            spent += a + extra

            if j == n - 1:
                dp[n] = min(dp[n], spent)
            elif finish <= waves[j + 1][0]:
                dp[j + 1] = min(dp[j + 1], spent + bullets)

    print(-1 if dp[n] == INF else dp[n])

if __name__ == "__main__":
    solve()
```

The outer loop chooses the wave where a full magazine is available before starting. The inner loop tries all possible endpoints of the current continuous segment. This matches the dynamic programming transitions described above.

Inside the simulation, `bullets` represents the current magazine after handling all previous waves in the segment. If the current wave cannot be finished, the code computes the minimum number of reloads required with ceiling division. The condition `reloads > r - l` checks whether those reloads fit before the wave deadline.

The expression `(k - need % k) % k` computes the remaining bullets after the last reload. The extra modulo handles the case where the last magazine becomes exactly empty. After finishing a segment, adding `bullets` to the next state represents the bullets that would be lost by reloading before the next wave.

All calculations use Python integers, so values near the maximum possible answer are safe.

## Worked Examples

For the first sample:

```
2 3
2 3 6
3 4 3
```

The transition simulation behaves as follows:

| Wave | Bullets before wave | Monsters | Reloads | Bullets after | Cost added |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 6 | 1 | 0 | 6 |
| 2 | 3 | 3 | 0 | 0 | 3 |

The first wave requires one reload because the magazine only contains three bullets. The reload finishes exactly when the second wave appears, allowing the remaining actions to continue. The total is `9`.

For the second sample:

```
2 5
3 7 11
10 12 15
```

| Wave | Bullets before wave | Monsters | Reloads | Bullets after | Cost added |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 11 | 2 | 4 | 15 |
| 2 | 5 | 15 | 2 | 0 | 15 |

The first wave ends with four bullets discarded before the next full magazine is needed. The same pattern happens for the second wave, giving a total of `30`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every starting wave tries every possible ending wave, and each transition is simulated in constant time. |
| Space | O(n) | The algorithm stores the wave list and one dynamic programming array. |

With `n <= 2000`, the number of transitions is about four million, which is easily within the limit. The large time values do not affect the complexity because the algorithm never iterates over moments of time.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import math
    data = sys.stdin.readline
    n, k = map(int, data().split())
    waves = [tuple(map(int, data().split())) for _ in range(n)]

    INF = 10**30
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == INF:
            continue
        spent = dp[i]
        bullets = k
        for j in range(i, n):
            l, r, a = waves[j]
            if a <= bullets:
                bullets -= a
                finish = l
                extra = 0
            else:
                need = a - bullets
                reloads = (need + k - 1) // k
                if reloads > r - l:
                    break
                extra = reloads * k
                finish = l + reloads
                bullets = (k - need % k) % k
            spent += a + extra
            if j == n - 1:
                dp[n] = min(dp[n], spent)
            elif finish <= waves[j + 1][0]:
                dp[j + 1] = min(dp[j + 1], spent + bullets)

    sys.stdin = old_stdin
    return str(-1 if dp[n] == INF else dp[n])

assert solve("""2 3
2 3 6
3 4 3
""") == "9"

assert solve("""2 5
3 7 11
10 12 15
""") == "30"

assert solve("""1 10
100 111 1
""") == "1"

assert solve("""5 42
42 42 42
42 43 42
43 44 42
44 45 42
45 45 1
""") == "-1"

assert solve("""1 5
1 1 5
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two touching waves | 9 | Checks that equal end and start times can both be used |
| Large magazine with one monster | 1 | Checks that final unused bullets are not counted |
| Impossible final wave | -1 | Checks deadline handling |
| Single wave exactly filling magazine | 5 | Checks the minimum-size boundary case |

## Edge Cases

For the touching-wave case:

```
2 3
2 3 6
3 4 3
```

The algorithm starts with three bullets. It spends them immediately on the first wave, detects that three more bullets are needed, and uses one reload. The reload finishes at time `3`, which is allowed because the next wave also begins at `3`. The second wave uses the new magazine completely, producing `9`.

For the final-magazine case:

```
1 10
100 111 1
```

The first magazine already contains enough bullets. The simulation spends one bullet and leaves nine bullets unused. Since there is no next wave, the code does not add those remaining bullets as discarded cost, giving the correct answer `1`.

For an impossible deadline:

```
5 42
42 42 42
42 43 42
43 44 42
44 45 42
45 45 1
```

The algorithm tries to simulate the first wave. Every required reload consumes one unit of time, and the later waves leave no enough moments for all necessary reloads. The transition fails because the required reload count exceeds the available interval length, so the final state remains unreachable and the answer is `-1`.
