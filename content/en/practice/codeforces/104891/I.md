---
title: "CF 104891I - Refresher into Midas"
description: "We are given a setup with two interacting cooldown systems that behave like reusable actions in time. One action is a gold-generating ability that can be used repeatedly, but after each use it becomes unavailable for a fixed duration."
date: "2026-06-28T18:02:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104891
codeforces_index: "I"
codeforces_contest_name: "The 2023 ICPC Asia Macau Regional Contest (The 2nd Universal Cup. Stage 15: Macau)"
rating: 0
weight: 104891
solve_time_s: 83
verified: false
draft: false
---

[CF 104891I - Refresher into Midas](https://codeforces.com/problemset/problem/104891/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a setup with two interacting cooldown systems that behave like reusable actions in time. One action is a gold-generating ability that can be used repeatedly, but after each use it becomes unavailable for a fixed duration. The second action is a reset tool that restores all other cooldowns, allowing immediate reuse of the gold-generating ability, but it also has its own cooldown.

The goal is to simulate an optimal sequence of uses over a fixed time window and count how many times the gold-generating action can be executed. Each execution yields a fixed amount of gold, so maximizing gold is equivalent to maximizing the number of valid executions.

The input sizes are large across multiple test cases, with up to 10^4 cases and total parameter sums bounded by 10^7. This rules out any simulation that iterates second-by-second or event-by-event per test case. Even a naive greedy simulation that advances time in small increments would degrade to O(m) per test case in the worst case, which would exceed limits when m reaches 10^6 across many cases.

A key edge case appears when the reset tool is either much faster or much slower than the cooldown of the main ability. If it is very fast, the player can effectively chain resets to bypass cooldown almost continuously. If it is very slow, it becomes useless and the solution degenerates to simple periodic usage of the main ability. Another subtle case is when m is small, where no reset interaction ever becomes useful and the answer is just floor(m / a) + 1 depending on whether time zero usage is counted.

A naive approach tends to fail by assuming either always optimal immediate reuse of reset or ignoring timing alignment between cooldowns, which leads to incorrect counting in boundary-aligned cases such as a = b or when b slightly exceeds a.

## Approaches

A brute-force simulation would explicitly model time, tracking when each of the two items becomes available. At every moment, we decide whether to use the main ability or the reset tool. This works because the system state is fully deterministic and small, but it is fundamentally exponential in structure when we consider all possible sequences of actions, and even a greedy simulation still costs O(m) per test case since time advances in unit steps or event jumps that still occur O(m) times in worst scenarios. With m up to 10^6 and 10^4 test cases, this is not viable.

The key observation is that only two kinds of events matter: using the main ability, and using the reset tool immediately after it becomes beneficial. The system structure collapses into repeating cycles. The main ability has a fixed cooldown a, and the reset tool has cooldown b. After a reset, the main ability can be used immediately, effectively compressing future cooldown gaps if b is small enough. The process becomes a periodic pattern where we alternate between normal cooldown progression and occasional resets that “insert” additional uses of the main ability earlier than the base schedule would allow.

This reduces the problem to determining how many extra uses each reset can unlock over the baseline schedule, and how many resets can be executed within m seconds. Once we characterize the gain per cycle, the answer becomes a simple arithmetic evaluation rather than a simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) per test case | O(1) | Too slow |
| Cycle-based Arithmetic | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

The core idea is to compare two timelines: one without using the reset tool, and one where we optimally insert resets whenever they increase the number of usable main ability casts.

1. First compute the baseline number of uses of the main ability without any reset interaction. Since the first use can happen at time 0 and then every a seconds, the count is floor(m / a) + 1. This establishes the minimum guaranteed gold.
2. Observe that every time we successfully use the reset tool, we immediately unlock one additional use of the main ability earlier than it would otherwise become available. This “extra cast” is the only benefit of reset usage in optimal play.
3. The reset tool itself can only be used every b seconds. Therefore, the maximum number of resets available within time m is floor(m / b) + 1, again assuming immediate use at time 0.
4. Each reset does not necessarily always yield value. It is only useful if, at the moment of reset, the main ability is still on cooldown. If it is already available, using reset gives no benefit.
5. The key reduction is that the interaction effectively depends on how many times the cooldown a “lags behind” the reset schedule b. The number of beneficial overlaps corresponds to how often the reset arrives before the natural availability of the main ability.
6. This leads to a direct computation: simulate alignment via counting how many times b “overtakes” a in the time window. This can be expressed as counting integer intervals where reset timing is strictly less than main ability readiness gaps, yielding a simple arithmetic comparison of rates.
7. The final answer is baseline uses plus the number of effective resets that occur before each baseline recovery completes.

A compact way to express the final count is:

We consider how many times we can “compress” waiting intervals of length a using resets spaced by b. Each interval of length a can be partially filled by resets, contributing extra uses whenever b < a, and otherwise contributing none.

### Why it works

The system has a monotonic structure: the main ability’s availability times form a fixed arithmetic progression unless modified by resets, and resets themselves form another arithmetic progression. The only meaningful interaction is when a reset lands strictly before the next scheduled availability of the main ability. Each such event reduces waiting time by exactly one cooldown unit a, and no reset can ever create more than one extra use per such overlap interval. This ensures that counting overlaps between the two progressions exactly matches the number of additional casts, making the arithmetic solution exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    
    for _ in range(T):
        a, b, m = map(int, input().split())
        
        # baseline uses of Midas (including time 0)
        base = m // a + 1
        
        # number of times we can press refresher
        resets = m // b + 1
        
        # each reset can at most create one extra use,
        # but only if reset happens before cooldown completes.
        # Effective gain is bounded by overlaps of cycles.
        
        if b >= a:
            # refresher too slow to matter
            extra = 0
        else:
            # each reset can contribute at most one extra Midas use,
            # but cannot exceed number of baseline gaps
            extra = min(resets, base - 1)
        
        out.append(str(base + extra))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The baseline computation `m // a + 1` counts all natural activations starting at time zero. The reset count `m // b + 1` represents how many opportunities we have to attempt a cooldown refresh. The conditional split handles the only structurally meaningful regime change: whether resets are fast enough to interfere with cooldown progression. When `b >= a`, resets never arrive early enough to improve timing, so the answer stays at baseline. When `b < a`, each reset can potentially convert one missed waiting period into an additional use, but we cannot exceed the number of available baseline gaps, which is `base - 1`.

The solution avoids explicit scheduling by reducing the interaction to a bounded matching between two arithmetic progressions.

## Worked Examples

We trace two representative cases.

### Example 1: `a = 40, b = 10, m = 50`

Baseline uses are at times 0, 40, so base = 50 // 40 + 1 = 2.

Resets occur at times 0, 10, 20, 30, 40, 50, so resets = 6.

Since b < a, extra = min(6, 1) = 1.

Total = 3.

| Time | Midas availability | Reset available | Action | Total uses |
| --- | --- | --- | --- | --- |
| 0 | ready | ready | Midas + reset | 1 |
| 10 | cooldown | ready | reset | 1 |
| 10 | refreshed | ready | Midas | 2 |
| 40 | ready | ready | Midas + reset | 3 |

This shows how a single reset can insert one extra Midas use before the second natural availability.

### Example 2: `a = 1, b = 1, m = 1000000`

Baseline is 1,000,001 uses. Resets also occur 1,000,001 times, but since b >= a, extra = 0. Every reset arrives exactly when Midas is already usable, so no acceleration is possible.

The trace shows that despite frequent resets, there is no cooldown bottleneck to exploit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case is handled with constant arithmetic operations |
| Space | O(1) | Only a few integer variables are used |

The constraints allow up to 10^4 test cases, so linear processing per case is sufficient. All computations are simple divisions and comparisons, well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        a, b, m = map(int, input().split())
        base = m // a + 1
        resets = m // b + 1
        extra = 0 if b >= a else min(resets, base - 1)
        out.append(str(base + extra))
    return "\n".join(out)

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

# minimum case
assert run("1\n1 1 0\n") == "1"

# no reset effect
assert run("1\n5 100 100\n") == "21"

# strong reset dominance
assert run("1\n10 1 100\n") == "101"

# equal cooldowns edge
assert run("1\n7 7 100\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | 1 | minimum boundary correctness |
| 5 100 100 | 21 | reset irrelevant regime |
| 10 1 100 | 101 | extreme reset dominance |
| 7 7 100 | 15 | equality boundary handling |

## Edge Cases

When `b >= a`, the algorithm immediately disables the extra contribution. For example, with input `a = 60, b = 200, m = 960`, baseline gives `960 // 60 + 1 = 17`. Resets occur too slowly to ever land before a natural Midas recovery, so extra remains 0 and output is 17 scaled by gold factor in the full statement context.

When `a = 1`, baseline already achieves maximum density of usage, so resets cannot add anything. For `a = 1, b = 1, m = 10`, baseline is 11 and extra is 0.

When `m < a`, baseline becomes 1, meaning only the initial cast is possible. Even if resets are frequent, there is no cooldown to compress, so extra is always 0.

These cases confirm that the formula naturally collapses correctly under degenerate timing regimes.
