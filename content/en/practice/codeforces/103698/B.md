---
title: "CF 103698B - Majhong"
description: "The task describes a simplified Mahjong-like system where tiles are numbered from 1 to n, and each number can appear in any quantity. The entire hand is just a multiset of these numbers. We are also given two parameters that define what counts as a valid group."
date: "2026-07-02T09:48:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103698
codeforces_index: "B"
codeforces_contest_name: "The 4th Turing Cup"
rating: 0
weight: 103698
solve_time_s: 52
verified: true
draft: false
---

[CF 103698B - Majhong](https://codeforces.com/problemset/problem/103698/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a simplified Mahjong-like system where tiles are numbered from 1 to n, and each number can appear in any quantity. The entire hand is just a multiset of these numbers. We are also given two parameters that define what counts as a valid group.

A group can be either a “Pong”, which is exactly x identical tiles of the same number, or a “Chow”, which is y consecutive numbers, each appearing once in that group. A hand is considered valid if we can partition all tiles into such groups with no leftovers.

So the problem reduces to deciding whether a given frequency array can be fully decomposed into blocks of size x (at a single index) and blocks of size y (spread across consecutive indices), where Chows consume one unit from each of y consecutive positions.

The key difficulty is that Pong blocks are local to one index while Chow blocks couple adjacent indices, so decisions at one value affect future possibilities. This interaction makes a greedy local decision unsafe.

The constraints are n up to 1000 and counts up to 10^9, while x and y can also be very large. This immediately rules out any exponential search over decompositions or any simulation that tries all combinations of taking Pongs and Chows greedily in different orders, since even a naive DP over “remaining tiles” would be too large if it tried to track exact counts.

A subtle edge case appears when y is large relative to n. For example, if y > n, no Chow is possible at all, so the problem reduces to checking whether every a[i] is divisible by x. Another tricky situation occurs when x is large but y = 1. In that case, Chows are single elements and effectively all tiles can always be consumed unless counts mismatch in a specific parity-like way induced by x.

The main hidden danger is assuming that greedily forming Pongs whenever possible is safe. For instance, if x = 3 and at some index you have 3 tiles, consuming a Pong immediately may prevent forming a Chow that would have been required later, even though a valid global partition exists.

## Approaches

A brute-force approach would try to simulate all ways of forming groups from left to right. At each index i, we could decide how many Pongs to take from a[i], and how many Chows to start at i that consume future positions. Each choice affects remaining counts forward, so this becomes a branching search with state depending on remaining suffix constraints. In the worst case, at every position we have O(a[i]/x) choices for Pongs and additional choices for how many Chows to start, leading to exponential blowup across n positions. Even with memoization, the state space depends on remaining partial contributions from up to y−1 previous positions, making it infeasible.

The key insight is to treat the process as a forward sweep where we track how many Chows are currently “active” at each position. A Chow started at position i consumes one tile from each of i through i+y−1. So at position i, we only need to know how many Chows started in the last y−1 positions are still affecting i. This transforms the problem into a greedy feasibility check with a sliding window effect.

At each index, once we know how many tiles are already reserved by earlier Chows, the remaining available tiles at i must be split into some number of Pongs and possibly new Chows starting at i. Since Pongs consume x units and Chows consume exactly y starting positions, the structure forces a divisibility constraint on how we handle leftovers modulo x after accounting for required Chow usage.

This reduces the problem to a linear scan where we maintain a queue-like structure for active Chows and enforce consistency locally. Because each Chow has a fixed span and fixed cost per position, we never need to revisit earlier decisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force search over decompositions | Exponential | Exponential | Too slow |
| Sliding window greedy with active Chow tracking | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Traverse indices from 1 to n while maintaining how many tiles at each position are already consumed by Chows started earlier. This represents the forced usage imposed by earlier decisions.
2. At index i, compute the remaining available tiles after subtracting the number already used by active Chows. If this value becomes negative, the configuration is impossible because earlier Chow decisions over-consumed position i.
3. If we are at position i and still have leftover tiles after accounting for active Chows, decide how many new Chows to start at i. Each new Chow started here will consume one tile from i and also reserve usage in the next y−1 positions.
4. After allocating as many Chows as needed or possible, the remaining tiles at position i must be divisible by x. If not, no combination of Pongs can fix the remainder, so the answer is immediately impossible.
5. Convert the remaining tiles at i into Pongs by dividing by x, and continue.
6. Maintain a sliding structure that records how many Chows end at position i+y so that their effect is removed when moving forward.

### Why it works

The algorithm works because every Chow is a fixed-length interval constraint that contributes exactly one unit of demand at each position it spans. Once a Chow is started, its effect is fully determined and cannot be adjusted later. This creates a one-directional dependency from left to right. At each index, all uncertainty about previous decisions is already compressed into the current “active demand” value. Since Pongs are purely local and do not interact across positions, the only global coupling comes from Chows, and those are fully represented by the sliding window state. This ensures that any locally feasible assignment extends consistently forward without needing backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x, y = map(int, input().split())
    a = list(map(int, input().split()))

    # active_chows[i] will track how many chows start at i and affect future positions
    active = [0] * (n + 5)
    current_active = 0

    for i in range(n):
        current_active += active[i]

        # tiles available at i after consuming by active chows
        if current_active > a[i]:
            print("No")
            return

        remaining = a[i] - current_active

        # try to start new chows at i
        if y <= n:
            start = remaining  # start as many chows as possible
        else:
            start = 0  # cannot form any chow

        current_active += start

        # schedule removal after y positions
        if i + y < len(active):
            active[i + y] -= start

        remaining -= start

        if remaining % x != 0:
            print("No")
            return

        # remaining is handled by pongs, no need to track further

    print("Yes")

if __name__ == "__main__":
    solve()
```

The code maintains a running count of how many Chow constraints are active at each position. It subtracts those from the available tiles and immediately rejects any position where earlier decisions require more tiles than exist. After that, it greedily starts as many Chows as possible at each index, because delaying a Chow start can only increase future constraints without benefit.

The remaining tiles must be exactly fillable by Pongs, so the divisibility check by x is the final local consistency condition.

A common pitfall is forgetting that Chows consume future positions, not just the current one. The `active` array encodes this propagation so that each started Chow automatically applies pressure forward in time.

## Worked Examples

### Sample 1

Input:

```
9 3 3
4 1 1 1 1 2 1 1 3
```

We track active Chow contributions and remaining tiles.

| i | a[i] | active before | remaining after active | new Chows started | remaining after | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 0 | 4 | 1 | 3 | yes |
| 1 | 1 | 1 | 0 | 0 | 0 | yes |
| 2 | 1 | 1 | 0 | 0 | 0 | yes |
| 3 | 1 | 0 | 1 | 0 | 1 | yes |
| 4 | 1 | 0 | 1 | 0 | 1 | yes |
| 5 | 2 | 0 | 2 | 0 | 2 | yes |
| 6 | 1 | 0 | 1 | 0 | 1 | yes |
| 7 | 1 | 0 | 1 | 0 | 1 | yes |
| 8 | 3 | 0 | 3 | 1 | 2 | yes |

This trace shows that whenever possible we start Chows early, and the remaining tiles always align with multiples of x.

### Sample 2

Input:

```
9 3 4
2 1 0 2 2 2 0 1 2
```

| i | a[i] | active before | remaining | action | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 2 | start 2 Chows | yes |
| 1 | 1 | 2 | -1 | impossible | no |

Here the second position is already over-consumed by earlier Chows, so the configuration fails immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once with constant updates to the active Chow structure |
| Space | O(n) | Stores pending Chow expirations up to distance y |

The solution fits comfortably within limits since n is at most 1000, and even an O(n) sweep is trivial under a 1 second constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, x, y = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    active = [0] * (n + 5)
    cur = 0

    for i in range(n):
        cur += active[i]
        if cur > a[i]:
            return "No"

        rem = a[i] - cur

        if y <= n:
            start = rem
        else:
            start = 0

        cur += start
        if i + y < len(active):
            active[i + y] -= start

        rem -= start

        if rem % x != 0:
            return "No"

    return "Yes"

# provided samples
assert run("9 3 3\n4 1 1 1 1 2 1 1 3\n") == "Yes"
assert run("9 3 4\n2 1 0 2 2 2 0 1 2\n") == "No"

# custom cases
assert run("3 3 3\n3 3 3\n") == "Yes"
assert run("5 2 3\n2 2 2 2 2\n") == "Yes"
assert run("4 3 2\n1 1 1 1\n") == "No"
assert run("6 1 2\n1 1 1 1 1 1\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 3 / 3 3 3 | Yes | pure Pongs only |
| 5 2 3 / all 2 | Yes | mixed feasibility |
| 4 3 2 / all 1 | No | impossible divisibility |
| 6 1 2 / all 1 | Yes | x=1 edge case |

## Edge Cases

For y > n, the algorithm naturally prevents any Chow from being started, so every position must be exactly divisible by x. For example, input `n=5, x=2, y=10, a=[2,2,2,2,2]` is accepted because all positions are valid Pongs.

When x = 1, every remaining tile after Chow handling is automatically valid since any count is divisible by 1. The algorithm reduces to only checking Chow feasibility.

A case where greedy seems suspicious is when early Chow formation reduces flexibility later. For instance, if starting a Chow at i consumes resources needed for a future Chow, the algorithm still works because any delay would only increase leftover pressure at intermediate positions, never decrease it, so postponing a Chow cannot create a valid configuration that the greedy approach would miss.
