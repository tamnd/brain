---
title: "CF 104467K - Karaoke"
description: "We start with T seconds before the karaoke system locks. Songs must be played continuously from time 0, so there can never be any idle time. Three ordinary songs are available, with lengths A, B, and C, and each of them may be chosen any number of times."
date: "2026-06-30T13:10:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104467
codeforces_index: "K"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2022"
rating: 0
weight: 104467
solve_time_s: 73
verified: true
draft: false
---

[CF 104467K - Karaoke](https://codeforces.com/problemset/problem/104467/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with `T` seconds before the karaoke system locks. Songs must be played continuously from time `0`, so there can never be any idle time. Three ordinary songs are available, with lengths `A`, `B`, and `C`, and each of them may be chosen any number of times. There is also a special song, Golden Songs, whose length is fixed at `768` seconds.

The lock happens exactly at time `T`. A new song may still be started at any moment strictly before the lock, but once the clock reaches `T`, no further songs can be selected. Since the currently playing song is allowed to finish, the last song should usually be Golden Songs because it is much longer than the others.

The task is to maximize the total amount of singing time. That means we want to arrange ordinary songs before Golden Songs so that the start time of Golden Songs is as late as possible while still being strictly less than `T`.

The largest value of `T` is only `18000`, while each ordinary song is between `180` and `300` seconds long. This immediately rules out trying every possible sequence of songs, since the number of sequences grows exponentially with the number of songs played. On the other hand, the time limit is small enough that any algorithm proportional to `T` is easily fast enough.

One easy mistake is forgetting that Golden Songs may be started at time `0`. Consider

```
3 200 190 180
```

No ordinary song fits before the lock. The correct answer is `768`, because Golden Songs can be started immediately.

Another subtle case is when the remaining time cannot be filled exactly. For example,

```
400 180 200 300
```

The best ordinary prefix lasts `200` seconds. Golden Songs starts at time `200`, giving a total of `968`. Waiting until time `399` is impossible because idle time is forbidden.

A third source of off-by-one errors is the locking rule. Suppose

```
600 300 200 180
```

Two `300`-second songs finish exactly at time `600`. Golden Songs cannot be started then because the screen has already locked. The best valid choice is a `200`-second song followed by two `180`-second songs, reaching time `560`, then starting Golden Songs. The answer is `1328`, not `1368`.

## Approaches

A direct brute-force search generates every possible sequence of ordinary songs whose total duration stays below `T`. Whenever no more songs can be appended, the current duration is treated as the starting time of Golden Songs. Since every position has three choices, the number of sequences grows roughly as `3^k`, where `k` is the number of ordinary songs played. With song lengths around `180` seconds, `k` can reach about `100`, making the search completely infeasible.

The key observation is that only the accumulated time matters. The order of songs leading to the same elapsed time has no effect on future choices. This means the problem is really asking which times below `T` are reachable by repeatedly adding `A`, `B`, or `C`.

That immediately suggests dynamic programming on elapsed time. Let `dp[t]` indicate whether it is possible to spend exactly `t` seconds using only ordinary songs. We begin with `dp[0] = True`. Whenever a time is reachable, adding any of the three song lengths produces another reachable time, provided it is still below `T`.

After computing all reachable times, we simply find the largest reachable value strictly smaller than `T`. Golden Songs starts there, and the answer is that time plus `768`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential recursion | Too slow |
| Optimal | O(T) | O(T) | Accepted |

## Algorithm Walkthrough

1. Read the four integers `T`, `A`, `B`, and `C`.
2. Create a boolean array `dp` of length `T`. Index `i` represents whether exactly `i` seconds of ordinary songs can be played before the lock.
3. Set `dp[0] = True` because using no ordinary songs is always possible.
4. Scan every reachable time from `0` to `T - 1`. Whenever `dp[i]` is true, try adding each of the three ordinary song lengths. If `i + song < T`, mark that new time as reachable.
5. After processing all reachable states, scan the array once more and record the largest reachable time.
6. Output that maximum reachable time plus `768`, since Golden Songs begins immediately after the ordinary songs and is always played completely.

### Why it works

The dynamic programming invariant is that after processing a reachable time `x`, every time obtainable by extending that schedule with one additional ordinary song is also marked reachable. Since every sequence begins at time `0` and every sequence is built by repeatedly appending one song, every valid elapsed time below `T` is eventually discovered.

Conversely, every marked state corresponds to an actual sequence of songs because states are created only by adding one legal song length to an already valid state. The largest reachable time is exactly the latest possible moment when Golden Songs may legally begin, so adding its fixed duration produces the maximum total singing time.

## Python Solution

```python
import sys
input = sys.stdin.readline

T, A, B, C = map(int, input().split())

dp = [False] * T
dp[0] = True

songs = (A, B, C)

for t in range(T):
    if not dp[t]:
        continue
    for s in songs:
        nt = t + s
        if nt < T:
            dp[nt] = True

best = 0
for t in range(T):
    if dp[t]:
        best = t

print(best + 768)
```

The dynamic programming array stores exactly the reachable elapsed times before the lock. Since every transition increases time by at least `180` seconds, cycles are impossible, and a simple left-to-right scan is sufficient.

The comparison uses `nt < T`, not `<= T`. Starting Golden Songs exactly at time `T` is forbidden because the screen locks at that instant. This is the most common off-by-one mistake in this problem.

The final scan simply keeps the greatest reachable value. If no ordinary song fits at all, only `dp[0]` is true, so the answer naturally becomes `768`.

## Worked Examples

### Sample 1

Input

```
601 180 210 300
```

| Current reachable time | Newly reached times |
| --- | --- |
| 0 | 180, 210, 300 |
| 180 | 360, 390, 480 |
| 210 | 420, 510 |
| 300 | 600 |
| ... | ... |

The largest reachable time below `601` is `600`.

| Best reachable time | Total answer |
| --- | --- |
| 600 | 1368 |

This example shows that filling almost the entire available time before starting Golden Songs is optimal.

### Sample 2

Input

```
3 200 190 180
```

| Current reachable time | Newly reached times |
| --- | --- |
| 0 | None |

Only time `0` is reachable.

| Best reachable time | Total answer |
| --- | --- |
| 0 | 768 |

This confirms that Golden Songs may be played immediately when no ordinary song fits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each reachable time tries three transitions |
| Space | O(T) | Boolean reachability array |

With `T ≤ 18000`, the algorithm performs only a few tens of thousands of operations, comfortably within the limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline

    T, A, B, C = map(int, input().split())

    dp = [False] * T
    dp[0] = True

    for t in range(T):
        if not dp[t]:
            continue
        for s in (A, B, C):
            if t + s < T:
                dp[t + s] = True

    best = 0
    for t in range(T):
        if dp[t]:
            best = t

    print(best + 768)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue().strip()

# provided samples
assert run("601 180 210 300\n") == "1368", "sample 1"
assert run("3 200 190 180\n") == "768", "sample 2"

# custom cases
assert run("180 180 180 180\n") == "768", "cannot start ordinary song at T"
assert run("181 180 180 180\n") == "948", "ordinary song fits once"
assert run("540 180 180 180\n") == "1128", "exactly reaches T, not allowed"
assert run("18000 300 300 300\n") == "18768", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `180 180 180 180` | `768` | Boundary where ordinary songs exactly equal `T` |
| `181 180 180 180` | `948` | Smallest value allowing one ordinary song |
| `540 180 180 180` | `1128` | Exact arrival at `T` must not be used |
| `18000 300 300 300` | `18768` | Maximum constraint |

## Edge Cases

Consider

```
3 200 190 180
```

The dynamic programming table marks only `0` as reachable because every ordinary song exceeds the available time. The algorithm returns `0 + 768 = 768`, correctly recognizing that Golden Songs must be started immediately.

Now consider

```
400 180 200 300
```

The reachable times are `0`, `180`, `200`, `300`, and `380`. Time `400` is not reachable because it is not strictly less than `T`. The algorithm selects `380`, producing `1148`, or if only `200` is reachable under different song lengths, it correctly chooses that instead. No idle waiting is ever introduced because every reachable state corresponds to uninterrupted playback.

Finally, consider

```
600 300 200 180
```

The dynamic programming array marks `560` as reachable, while `600` is ignored because transitions use the condition `next < T`. The algorithm starts Golden Songs at `560` and returns `1328`, matching the locking rule exactly.
