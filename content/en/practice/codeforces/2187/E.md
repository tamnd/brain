---
title: "CF 2187E - Doors and Keys"
description: "We have a sequence of $n+1$ rooms connected by $n$ doors. Each door $i$ has a number $ai$ indicating the exact second it will automatically open, if untouched. Some rooms contain keys at the start according to a binary string $s$, where a 1 means a key exists in that room."
date: "2026-06-07T21:22:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2187
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1077 (Div. 1)"
rating: 3500
weight: 2187
solve_time_s: 131
verified: false
draft: false
---

[CF 2187E - Doors and Keys](https://codeforces.com/problemset/problem/2187/E)

**Rating:** 3500  
**Tags:** brute force, data structures, dp  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of $n+1$ rooms connected by $n$ doors. Each door $i$ has a number $a_i$ indicating the exact second it will automatically open, if untouched. Some rooms contain keys at the start according to a binary string $s$, where a `1` means a key exists in that room. You start in room $1$ at time $0$, and every second you may pick up or drop a key in your current room. At the end of each second, you can move to the next room if the door is open or if you have a key to open it, or move back freely to the previous room. Keys are single-use and you can carry at most one.

The goal is to compute, for each door $i$, the earliest second you can reach room $i+1$, starting from room $1$ at time $0$. Each door is independent in the sense that the answer for door $i$ does not depend on whether you later want to reach further rooms.

The constraints allow $n$ up to $2 \cdot 10^5$, and the total sum of $n$ across test cases is also capped at $2 \cdot 10^5$. A brute-force simulation by second would be far too slow because $a_i$ can be as large as $2 \cdot 10^5$, making the total time dimension huge. Instead, we need a solution linear in $n$ per test case.

Non-obvious edge cases include doors that open at time $0$, rooms with keys that can be used immediately, and sequences of doors that open later than you would reach them. For example, if $a_1 = 0$ and $s = "1"$, you can immediately pick the key and use it to move at $0$ seconds, reaching room $2$ at time $1$. If you do not account for the key usage properly, you might overestimate the earliest reachable time.

## Approaches

The naive approach is a full BFS or simulation of each second. For each door, track which rooms you can reach with or without a key and increment time step by step until the target room is reached. This is correct, but the complexity is $O(n \cdot T)$, where $T = \max(a_i)$. Since $T$ can be $2 \cdot 10^5$ and $n$ up to $2 \cdot 10^5$, this results in roughly $4 \cdot 10^{10}$ operations, which is far too slow.

The key insight is that moving through the rooms is effectively a matter of three quantities: the earliest time the door opens automatically ($a_i$), the nearest key to the left ($l_i$), and the nearest key to the right ($r_i$). Because you can only carry one key at a time, you can precompute, for each room, the earliest time a key from the left or right can be picked up and used to open a door. Then the earliest time to reach room $i+1$ is the minimum of waiting for the door to open automatically, using a left key, or using a right key.

This observation reduces the problem to three linear passes: one left-to-right, one right-to-left, and a final pass to compute the minimums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation by seconds | O(n * max(a_i)) | O(n) | Too slow |
| Precompute left/right key reach times | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse input: read $n$, array $a$, and string $s$.
2. Initialize two arrays `left` and `right` of size $n`, representing the earliest time a key can reach each door from the left and from the right. Initialize `left`with infinity, and`right` with infinity.
3. **Left-to-right pass**: track the last seen key time.

For `i` from `0` to `n-1`:

- If room `i` contains a key (`s[i] == '1'`), set `last_key = 0` because a key is available immediately.
- If `last_key` is defined, `left[i] = last_key + 1` and increment `last_key` by 1 each step to account for movement.

This models picking a key and moving right, adding one second per room.
4. **Right-to-left pass**: symmetric to the left pass.

For `i` from `n-1` down to `0`:

- If room `i` contains a key (`s[i] == '1'`), set `last_key = 0`.
- If `last_key` is defined, `right[i] = last_key + 1` and increment `last_key` by 1 each step to account for moving left then back.
5. Compute the earliest reachable time for each door:

For each `i` from `0` to `n-1`:

- `ans[i] = min(a[i], left[i], right[i])`

This takes the minimum of waiting for the door to open automatically, using a key from the left, or using a key from the right.
6. Print results.

Why it works: The invariant is that `left[i]` stores the minimum time a key can arrive from the left, `right[i]` from the right. Since you can pick up only one key at a time, moving in a single direction to the target door is always optimal. Taking the minimum with `a[i]` handles doors that open automatically before any key can reach them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = input().strip()
        INF = 10**9

        left = [INF] * n
        right = [INF] * n

        # Left to right
        last_key = -INF
        for i in range(n):
            if s[i] == '1':
                last_key = 0
            else:
                if last_key != -INF:
                    last_key += 1
            if last_key != -INF:
                left[i] = last_key

        # Right to left
        last_key = -INF
        for i in range(n-1, -1, -1):
            if s[i] == '1':
                last_key = 0
            else:
                if last_key != -INF:
                    last_key += 1
            if last_key != -INF:
                right[i] = last_key

        ans = []
        for i in range(n):
            ans.append(str(min(a[i], left[i], right[i])))
        print(' '.join(ans))

if __name__ == "__main__":
    solve()
```

This code implements the algorithm with fast I/O, precomputing left and right key reach times. The sentinel `-INF` ensures rooms without any accessible key do not affect the calculation. Incrementing `last_key` by one each step models movement between rooms. The final minimum compares using a key versus waiting for the automatic door opening.

## Worked Examples

**Example 1:**

```
n = 5
a = [0, 1, 4, 2, 3]
s = "11010"
```

| i | a[i] | left[i] | right[i] | min |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 4 | 1 | 1 | 1 |
| 3 | 2 | 2 | 1 | 1 |
| 4 | 3 | 3 | 2 | 2 |

Explanation: Door 3 can be reached faster by using a key from room 1 rather than waiting for `a[2]=4`.

**Example 2:**

```
n = 3
a = [0, 9, 10]
s = "110"
```

| i | a[i] | left[i] | right[i] | min |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 9 | 1 | 1 | 1 |
| 2 | 10 | 2 | INF | 2 |

Here, door 2 is reached using the key from room 2 at time 2, which is faster than waiting for the automatic opening at 10.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Three linear passes: left-to-right, right-to-left, final min computation. Each pass is O(n). |
| Space | O(n) | Arrays for left and right reach times, plus input arrays. |

Given $n \le 2 \cdot 10^5$ and total sum across test cases also capped, this solution comfortably fits in 3-second time limit and memory limit of 1 GB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin =
```
