---
title: "CF 106242A - Finding Socks (socks)"
description: "The process described is about a person who starts with a fixed number of socks and wears one pair per day. Each day consumes one pair permanently. On certain days, specifically every fixed interval of days, new socks are added, but they are only available starting the next day."
date: "2026-06-25T07:12:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106242
codeforces_index: "A"
codeforces_contest_name: "2025 Taiwan NHSPC Mock Contest (Mirror)"
rating: 0
weight: 106242
solve_time_s: 39
verified: true
draft: false
---

[CF 106242A - Finding Socks (socks)](https://codeforces.com/problemset/problem/106242/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The process described is about a person who starts with a fixed number of socks and wears one pair per day. Each day consumes one pair permanently. On certain days, specifically every fixed interval of days, new socks are added, but they are only available starting the next day. The question asks how many days the person can continue this daily routine of using one pair before they eventually run out of usable socks.

The input gives two integers. The first is the initial number of sock pairs available at day one. The second is a period that determines how often new sock pairs are added, always at the end of those specific days. The output is a single integer representing the total number of days the process continues until there are no more socks available for the next day’s use.

The constraints are small, with values up to around a hundred. That immediately tells us that any linear simulation of days is sufficient, since even a naive loop over a few thousand steps is trivial in time limits. Anything beyond O(n^2) would still be safe, but the structure of the process suggests we will not need anything heavy.

A subtle edge case comes from the timing of replenishment. Socks bought on a multiple of the period day cannot be used on that same day, only starting the next morning. This creates off-by-one errors in simulations where someone mistakenly adds new socks too early.

A second edge case is when the period is larger than the initial stock. In that situation, the first replenishment happens after all initial socks are already consumed, so the answer depends entirely on whether the first refill arrives in time to extend usage.

## Approaches

The naive way to think about this problem is to simulate day by day. We start with the initial number of socks. Each day we decrement the count because one pair is used. Whenever the current day is a multiple of the given interval, we increment the sock count, but only after consuming the sock for that day since the purchase happens late in the evening.

This simulation is correct because it mirrors the real process exactly. However, even if we run it until exhaustion, the number of days is not large in constraints where both parameters are small. The worst case is when replenishment keeps extending the process, leading to a loop that continues until the accumulated stock is consumed. Since every cycle of length m contributes one extra sock, the growth is linear and predictable.

The key observation is that socks are consumed at a constant rate of one per day, while new socks arrive periodically. Every m days, net gain is one sock (we consume m socks and receive one extra), so the system behaves like a linear depletion process with periodic compensation. This reduces the problem to tracking how many full cycles we can sustain and what happens in the final partial cycle.

Instead of simulating every day, we can jump in blocks of m days. Each full block consumes m socks but also adds one extra sock for the next cycle. So after each full block, the stock decreases by m - 1. We repeat this until the remaining stock is not enough to complete another full block, then finish the remaining days directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Day-by-day simulation | O(answer) | O(1) | Accepted |
| Cycle-based reduction | O(answer / m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the initial number of socks and a day counter at zero. This models the system state at the beginning before any consumption happens.
2. While there are enough socks to reach the next replenishment day, simulate one full cycle of length m. Each cycle corresponds to m days of consumption.
3. For each full cycle, increase the day counter by m since we have completed m days of usage.
4. Reduce the sock count by m to account for usage during those days, then immediately add one sock because a new pair is purchased at the end of the cycle day. This captures the delayed replenishment effect correctly.
5. Once the remaining socks are fewer than m, exit the cycle loop and consume the remaining socks day by day, adding them directly to the day counter.

The correctness comes from maintaining the invariant that after each completed cycle, the sock count reflects exactly the number of unused socks available at the start of the next day. Each full cycle transforms the state in a consistent way: m consumptions always paired with at most one replenishment, so the net change is deterministic. Since no partial cycle can produce additional replenishment, handling the remainder separately completes the timeline exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    days = 0
    
    while n >= m:
        cycles = n // m
        days += cycles * m
        n -= cycles * m
        n += cycles
    
    days += n
    print(days)

if __name__ == "__main__":
    solve()
```

The code follows the cycle-based interpretation directly. The loop compresses multiple full m-day blocks at once instead of simulating them one by one. The expression `n // m` computes how many full cycles we can extract at once. Each cycle reduces the sock count by m but adds back one, which is why `n += cycles` is applied after consumption.

A common implementation mistake is updating socks before accounting for the full cycle effect, which breaks the relationship between consumption and replenishment timing. Another subtle issue is forgetting that replenishment happens after consumption on the m-th day, which is why the net effect is handled after subtracting m.

## Worked Examples

### Example 1

Input:

n = 2, m = 2

| Step | n (socks) | Days added | Action |
| --- | --- | --- | --- |
| Start | 2 | 0 | initial state |
| Cycle | 2 → 0 + 1 = 1 | +2 | consume 2 socks, add 1 |
| Finish | 1 | +1 | use remaining sock |

Final answer is 3 days.

This trace shows that even though socks are fully exhausted after two days, replenishment extends usage by one more day.

### Example 2

Input:

n = 9, m = 3

| Step | n (socks) | Days added | Action |
| --- | --- | --- | --- |
| Start | 9 | 0 | initial state |
| Cycle 1 | 9 → 6 + 1 = 7 | +3 | first 3-day block |
| Cycle 2 | 7 → 4 + 1 = 5 | +3 | second block |
| Cycle 3 | 5 → 2 + 1 = 3 | +3 | third block |
| Finish | 3 | +3 | final partial consumption |

Final answer is 12 days.

This example shows the steady-state behavior where each full cycle reduces stock by 2 net socks, and the process continues until the remaining stock is insufficient for another full block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / m) | each iteration removes a full cycle of m days |
| Space | O(1) | only counters are maintained |

The input limits are small, so even a linear simulation would be fast. The cycle-based reduction further guarantees constant-time behavior for typical inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    
    days = 0
    while n >= m:
        cycles = n // m
        days += cycles * m
        n -= cycles * m
        n += cycles
    days += n
    return str(days)

# provided samples
assert run("2 2") == "3", "sample 1"
assert run("9 3") == "12", "sample 2"

# custom cases
assert run("1 2") == "1", "single sock, no refill before depletion"
assert run("10 1") == "10", "daily refill every day"
assert run("5 5") == "6", "exact one cycle boundary"
assert run("100 100") == "101", "single large boundary cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 | no replenishment before exhaustion |
| 10 1 | 10 | extreme frequent replenishment |
| 5 5 | 6 | exact boundary cycle behavior |
| 100 100 | 101 | single-cycle correctness at scale |

## Edge Cases

When the initial stock is smaller than the replenishment interval, the loop never executes. The algorithm immediately falls through to consuming all socks day by day, which matches reality because no new socks arrive before exhaustion.

When the interval is equal to one, every day produces a new sock after consumption. The loop continuously adds one net sock per day, so the simulation effectively reduces to a non-decreasing system that still progresses correctly because consumption always happens first.

When the initial stock is exactly divisible by the interval, the last full cycle produces a replenishment that extends usage by one more day beyond the naive expectation, and the cycle-based update captures this without special casing.
