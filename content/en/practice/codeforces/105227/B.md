---
title: "CF 105227B - Let's Watch Football"
description: "We are given a video of length c seconds. Each second of watching requires consuming a units of data, while the internet connection can download b units of data per second continuously."
date: "2026-06-24T16:26:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105227
codeforces_index: "B"
codeforces_contest_name: "CPG Training Contest - 1"
rating: 0
weight: 105227
solve_time_s: 66
verified: true
draft: false
---

[CF 105227B - Let's Watch Football](https://codeforces.com/problemset/problem/105227/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a video of length `c` seconds. Each second of watching requires consuming `a` units of data, while the internet connection can download `b` units of data per second continuously.

If we start watching too early, playback may stall because at some point the video will demand more data than has been downloaded so far. However, downloading continues even while watching, so the buffer can be partially refilled during playback.

The goal is to choose an integer waiting time `t` before starting the video so that once playback begins, it can proceed continuously until the end, never exceeding the available downloaded data at any moment. We want the smallest such `t`.

The key quantity is not just total data, but a running balance between what has been downloaded and what has been consumed by watching. At time `t0`, the downloaded amount is `b * t0`. After starting playback at time `t`, the watched portion is `t0 - t`, requiring `a * (t0 - t)` data. The condition becomes:

`b * t0 ≥ a * (t0 - t)` for all `t0` in `[t, t + c]`.

The constraints are small, with `a, b, c ≤ 1000`, so even a simulation over possible waiting times is feasible, but a direct continuous-time check would still be unnecessarily complex. The real structure is linear, so we expect a direct formula.

A subtle edge case arises when the connection is very fast relative to consumption. For example, if `b ≥ a`, then streaming is always safe and waiting is unnecessary. Another edge case is when `b` is only slightly smaller than `a`, where a naive “compare total needed vs total downloaded” approach fails because it ignores intermediate buffer depletion.

## Approaches

A brute-force idea is to try each possible waiting time `t`, simulate the playback second by second, and check whether the buffer ever becomes negative. For each candidate `t`, we would track downloaded data and consumed data over `c` seconds. This works because the state evolves deterministically, but it is too slow in the worst case: up to `O(c^2)` operations if we test all `t` and simulate `c` steps each time.

The key observation is that the constraint `b * t0 ≥ a * (t0 - t)` is linear in `t0`, so if it holds at the worst point, it holds everywhere. The worst point occurs at the end of playback, when `t0 = t + c`. If we ensure the inequality at that point, earlier moments automatically satisfy it because both sides grow linearly and the slope of consumption is higher than download.

So we only need to enforce:

`b * (t + c) ≥ a * c`

Expanding gives:

`b * t + b * c ≥ a * c`

So:

`b * t ≥ c * (a - b)`

Since `a > b`, the right-hand side is positive, and we can solve directly:

`t ≥ ceil(c * (a - b) / b)`

We take the smallest integer satisfying this.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(c^2) | O(1) | Too slow |
| Mathematical derivation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We derive the minimum waiting time by enforcing that the buffer never becomes insufficient even at the worst moment of playback.

1. Compute the net deficit rate per second during playback as `a - b`. This is how much more data is consumed than replenished while watching.
2. Compute the total deficit accumulated over the full video duration `c`, which is `c * (a - b)`. This represents how much buffer must be preloaded before starting playback.
3. Observe that waiting `t` seconds produces `b * t` units of buffer.
4. Require that preloaded buffer is enough to cover the full deficit: `b * t ≥ c * (a - b)`.
5. Solve for `t` using integer division with ceiling: `t = (c * (a - b) + b - 1) // b`.
6. Output `t`.

The reason we focus on total deficit rather than per-second tracking is that both download and consumption evolve linearly. Once the total buffer at the start is sufficient to cover the net loss over time, intermediate points cannot violate the constraint because the system evolves with constant rates.

### Why it works

During playback, the buffer changes at a constant rate of `b - a`, which is negative since `a > b`. The buffer is therefore minimized at the final moment of playback. Ensuring that the buffer is non-negative at the end guarantees it never becomes negative earlier. This reduces a continuous feasibility condition over an interval into a single inequality at one endpoint.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, c = map(int, input().split())
    
    deficit = c * (a - b)
    
    if deficit <= 0:
        print(0)
        return
    
    t = (deficit + b - 1) // b
    print(t)

if __name__ == "__main__":
    solve()
```

The code computes the total extra data required for watching the full video and then determines how many seconds of downloading are needed to accumulate that amount. The expression `(deficit + b - 1) // b` is a standard ceiling division to ensure we do not underestimate the waiting time.

A common pitfall is forgetting that integer division must round up, since waiting slightly less than required leads to failure near the end of playback.

## Worked Examples

### Sample 1

Input:

```
4 1 1
```

We compute deficit per second as `4 - 1 = 3`, total deficit `3 * 1 = 3`.

| Step | Deficit | Buffer per second | Required t |
| --- | --- | --- | --- |
| Compute | 3 | 1 | ceil(3 / 1) |

So `t = 3`.

This shows that even though only one second of video exists, the download is too slow to start immediately.

### Sample 2

Input:

```
10 3 2
```

Deficit per second is `7`, total deficit is `14`.

| Step | Deficit | Buffer per second | Required t |
| --- | --- | --- | --- |
| Compute | 14 | 3 | ceil(14 / 3) |

So `t = 5`.

This demonstrates a case where waiting slightly less (4 seconds) would still allow starting playback, but the buffer would fail later, because total accumulated deficit is not fully covered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The solution easily fits within constraints since all computations are constant time and use only integer arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    
    output = io.StringIO()
    sys.stdout = output
    
    def solve():
        a, b, c = map(int, input().split())
        deficit = c * (a - b)
        if deficit <= 0:
            print(0)
            return
        print((deficit + b - 1) // b)

    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("4 1 1") == "3", "sample 1"
assert run("10 3 2") == "5", "sample 2"
assert run("13 12 1") == "1", "sample 3"

# custom cases
assert run("2 1 10") == "10", "slow net large duration"
assert run("5 4 1000") == "1000", "small deficit long video"
assert run("100 99 1") == "1", "almost equal rates"
assert run("10 1 1") == "9", "high deficit single second"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 10 | 10 | long video with small deficit per second |
| 5 4 1000 | 1000 | large duration with minimal net loss |
| 100 99 1 | 1 | near-balanced rates |
| 10 1 1 | 9 | extreme imbalance forcing large wait |

## Edge Cases

One edge case occurs when `b` is very close to `a`. For input `a = 100, b = 99, c = 1`, the deficit is `1`, so waiting `1` second gives exactly enough buffer. The algorithm computes `ceil(1 / 99) = 1`, matching the requirement.

Another edge case is when the video is long but imbalance is small, such as `a = 5, b = 4, c = 1000`. The total deficit becomes `1000`, and each second of waiting contributes only `4`, so the result is `250`. The ceiling division handles this precisely without simulation.

A final edge case is when `c = 1`. Then the condition reduces to ensuring enough buffer for a single second, and the formula becomes `ceil((a - b) / b)`, which correctly matches the intuition that only the first second of playback matters.
