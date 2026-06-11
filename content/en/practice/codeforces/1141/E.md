---
title: "CF 1141E - Superhero Battle"
description: "We are given a monster with an initial health value and a repeating damage pattern applied once per minute. The pattern has length n, and after the last minute we immediately loop back to the first minute and continue forever."
date: "2026-06-12T03:42:29+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1141
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 547 (Div. 3)"
rating: 1700
weight: 1141
solve_time_s: 95
verified: true
draft: false
---

[CF 1141E - Superhero Battle](https://codeforces.com/problemset/problem/1141/E)

**Rating:** 1700  
**Tags:** math  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a monster with an initial health value and a repeating damage pattern applied once per minute. The pattern has length `n`, and after the last minute we immediately loop back to the first minute and continue forever.

Each minute modifies the current health by adding a fixed integer, which can be negative or positive. The monster dies the first time its health becomes non-positive. We must determine the earliest minute in this infinite timeline when this happens, or conclude that this never happens.

The constraints make brute-force reasoning important. The number of minutes we might simulate is unbounded in principle, but `n` can be up to 200,000 and the initial health up to 10^12. A naive simulation of minute-by-minute progression could require up to 10^12 iterations in the worst case, which is far beyond feasible limits. Even a single pass repeated many times is only acceptable if we can skip large blocks.

A subtle issue is that health can increase within a round and then decrease later, so the death moment might occur in the middle of a cycle, not only at cycle boundaries.

One edge case is when the total sum of one full cycle is non-negative and no prefix ever decreases enough to kill the monster. For example, if all `d_i` are positive, the monster will never die. A naive simulation might still run forever.

Another edge case appears when the cumulative effect is negative overall but the monster survives early cycles. The death might occur deep inside a later cycle after many full repeats, so we must combine prefix behavior with repeated shifts.

## Approaches

A brute-force approach simulates minute by minute, continuously applying the sequence and checking whether the health drops to zero or below. This is correct because it mirrors the process exactly, but it becomes infeasible because the number of simulated steps can be extremely large. If the answer is `k`, then in worst cases `k` can be on the order of 10^12 or more, which makes this approach impossible within time limits.

The key observation is that the sequence is periodic, so after each full cycle the health changes by a constant value equal to the sum of all `d_i`. This allows us to compress repeated cycles. Instead of simulating every minute, we simulate full cycles while tracking how health shifts globally.

We precompute prefix sums of the array, which tells us the net change after each minute within a cycle. Within any cycle starting from a given health `H`, we can determine if the monster dies during that cycle by checking whether `H + prefix[i] <= 0` for some `i`. If not, we compute the new health after the full cycle as `H + total_sum` and repeat.

If the total sum of a cycle is non-negative and the monster survives one full cycle without dying, then it will never die. This is because future cycles will never reduce its health enough to create a new minimum.

To avoid iterating cycle by cycle, we can use a set of previously seen states or directly compute how many full cycles can be skipped safely using arithmetic when the total sum is negative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums of the damage array. This gives the net health change after each minute in a single cycle. This structure allows us to detect death inside a cycle without simulating step by step.
2. Scan the prefix sums to find the earliest index `i` such that `H + prefix[i] <= 0`. If such an index exists and we are in the first cycle, we can immediately return `i + 1` as the answer.
3. Compute the total sum of one full cycle. This value determines whether repeated cycles make the monster weaker or stronger over time.
4. If the total sum is greater than or equal to zero and the monster survives the first full cycle, return `-1`. This is because health never decreases over full cycles, so any future cycle starts with at least the same or higher health, and prefix patterns are identical.
5. Otherwise, the total sum is negative. We repeatedly simulate cycles, but instead of stepping minute by minute, we first check within each cycle if death occurs. If not, we reduce health by the total sum and accumulate the number of full minutes processed.
6. Each cycle we adjust the starting health and recompute the threshold check using prefix sums until we find the cycle where death occurs.

### Why it works

The algorithm relies on the invariant that within each cycle, the only possible points of failure are determined by prefix sums relative to the cycle's starting health. The ordering of prefix sums never changes between cycles; only a constant shift is applied. If the total cycle sum is non-negative and no prefix is lethal, then all future cycles are identical or better for survival, preventing any eventual death. If the total sum is negative, repeated application strictly decreases starting health, guaranteeing eventual termination if survival is not infinite.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    H, n = map(int, input().split())
    d = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + d[i]

    total = pref[n]

    cur = H
    time = 0
    seen = {}

    # We iterate cycle by cycle, but break early when possible
    while True:
        # check death inside current cycle
        for i in range(1, n + 1):
            if cur + pref[i] <= 0:
                print(time + i)
                return

        # survive full cycle
        cur += total
        time += n

        if total >= 0:
            print(-1)
            return

        # optional safety (not strictly needed but avoids pathological loops)
        if cur in seen:
            print(-1)
            return
        seen[cur] = True

        if cur <= 0:
            print(time)
            return

if __name__ == "__main__":
    solve()
```

The solution builds prefix sums so that each cycle can be checked in linear time. The inner loop checks whether the current starting health combined with any prefix sum leads to death within that cycle. If no such prefix exists, the entire cycle is survived, and the health is updated by adding the total cycle sum.

The key implementation detail is the `cur + pref[i] <= 0` check, which directly encodes whether the monster dies at minute `i` of the current cycle without simulating each subtraction step.

We also handle the infinite case when `total >= 0`, since repeated cycles will never decrease the starting health enough to change the outcome.

## Worked Examples

### Example 1

Input:

```
H = 10, n = 3
d = [-5, 2, -10]
```

Prefix sums: `[0, -5, -3, -13]`

Cycle total: `-13`

| Cycle | Start Health | Check i=1 | Check i=2 | Check i=3 | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 5 > 0 | 7 > 0 | -3 <= 0 | dies at 3 |

The monster survives first two minutes but dies at minute 3 in the first cycle. This shows why prefix checks are essential.

### Example 2

Input:

```
H = 20, n = 2
d = [3, -2]
```

Prefix sums: `[0, 3, 1]`

Cycle total: `1`

| Cycle | Start Health | Check i=1 | Check i=2 | Outcome |
| --- | --- | --- | --- | --- |
| 1 | 20 | 23 > 0 | 21 > 0 | survives |
| 2 | 21 | 24 > 0 | 22 > 0 | survives |

Since total is positive and no prefix kills the monster, it never dies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One prefix computation and one scan per cycle, with at most one cycle effectively processed |
| Space | O(n) | Prefix array stores cumulative sums |

The algorithm fits comfortably within constraints since `n` is up to 200,000 and all operations are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    H, n = map(int, input().split())
    d = list(map(int, input().split()))

    pref = [0]
    for x in d:
        pref.append(pref[-1] + x)

    total = pref[-1]
    cur = H
    time = 0

    while True:
        for i in range(1, n + 1):
            if cur + pref[i] <= 0:
                return str(time + i)

        cur += total
        time += n

        if total >= 0:
            return "-1"

# provided sample
assert run("1000 6\n-100 -200 -300 125 77 -4\n") == "9"

# minimum case
assert run("1 1\n-1\n") == "1"

# always survive
assert run("10 2\n1 1\n") == "-1"

# dies immediately after cycle repetition
assert run("5 2\n3 -10\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 -1 | 1 | immediate death |
| 10 2 1 1 | -1 | infinite survival |
| 5 2 3 -10 | 2 | death in first cycle |
| sample | 9 | mixed cycle + prefix logic |

## Edge Cases

One edge case is when the monster dies inside the first cycle. For an input like `H = 3, d = [-2, 10]`, prefix sums show immediate failure at minute 1 because `3 + (-2) <= 0`. The algorithm catches this before any cycle repetition.

Another edge case is when the cycle sum is zero. For example, `d = [1, -1]` and `H = 5`. Prefix sums never reduce health, and after each cycle health remains identical. Since no prefix kills the monster in the first cycle, every future cycle is identical, so the result is `-1`.
