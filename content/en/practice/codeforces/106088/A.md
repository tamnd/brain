---
title: "CF 106088A - \u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0441\u0435\u0440\u0438\u0430\u043b\u0430"
description: "We have a sequence of episodes with durations t1, t2, ..., tn. Kolya watches them in order and spends exactly m units of time per day, except possibly on the final day when the series may end before he reaches m."
date: "2026-06-19T21:51:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106088
codeforces_index: "A"
codeforces_contest_name: "\u0412\u0443\u0437\u043e\u0432\u0441\u043a\u043e-\u0430\u043a\u0430\u0434\u0435\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 2025, \u0432\u0442\u043e\u0440\u043e\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106088
solve_time_s: 50
verified: true
draft: false
---

[CF 106088A - \u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0441\u0435\u0440\u0438\u0430\u043b\u0430](https://codeforces.com/problemset/problem/106088/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of episodes with durations `t1, t2, ..., tn`. Kolya watches them in order and spends exactly `m` units of time per day, except possibly on the final day when the series may end before he reaches `m`.

A day is called successful if the viewing session of length exactly `m` ends at the precise end of some episode. If the session ends in the middle of an episode, the day is not successful. The last day is special: if fewer than `m` units of viewing remain, that day is not counted even if the series finishes exactly at the end of an episode.

The input gives the episode durations and the daily viewing limit. We must count how many successful days occur.

The key observation is that viewing progress depends only on total watched time. After one full day Kolya has watched `m` units, after two full days `2m`, after three full days `3m`, and so on. A day is successful exactly when one of these cumulative watched times coincides with the end of an episode.

The constraints are small in terms of `n`, only up to 1000, but episode lengths and `m` can reach `10^9`. This immediately rules out any simulation that advances one unit of time at a time. We need an approach based on cumulative sums rather than individual time units.

A subtle point is the treatment of the final partial day. Suppose the total duration of all episodes is `S`. Full viewing days correspond only to times `m, 2m, 3m, ...` that are strictly within the process of watching. If an episode ends at time `S` and `S` is not reached after a full day of length `m`, it must not be counted.

Consider:

```
1 5
3
```

The entire series lasts only 3 units. Kolya watches it in a single partial day. The correct answer is `0`, not `1`.

Another easy mistake is counting episode endings that happen during a day rather than exactly at the day's boundary.

Example:

```
2 3
1 2
```

The first episode ends after 1 unit, but the first day ends after 3 units. The correct answer is `1` because the day boundary at time 3 coincides with the end of episode 2. Counting every episode ending would be wrong.

A third edge case occurs when the total duration is an exact multiple of `m`.

Example:

```
2 2
1 3
```

Total duration is 4. There are two full days. Day 1 ends at time 2, which is in the middle of episode 2. Day 2 ends at time 4, exactly at the series end and also at an episode end. The answer is `1`.

The final full day still counts because Kolya watched exactly `m` units on that day.

## Approaches

A brute-force way to think about the problem is to simulate Kolya's viewing day by day. For each day we would determine where he stops, possibly moving through several episodes. Since `n` is only 1000, even repeatedly advancing through episodes is acceptable. We could maintain the current episode and position inside it and simulate every day until the series ends.

The brute-force simulation is correct because it follows the viewing process exactly. The issue is that it is unnecessarily complicated. The actual state of the process is determined entirely by total watched time.

The crucial observation is that episode endings occur at cumulative sums of episode durations. If we define

```
pref[i] = t1 + t2 + ... + ti
```

then episode `i` ends exactly at time `pref[i]`.

A successful day occurs when the end of a full viewing day coincides with an episode ending. Full viewing days end at times

```
m, 2m, 3m, ...
```

up to the total series duration.

So we simply need to count episode-ending times that are multiples of `m`.

There is one more condition. The last partial day does not count. An episode ending at time `pref[i]` contributes only if it is reached at the end of a full day. That means `pref[i]` must be divisible by `m`.

Nothing else matters. We do not need to simulate pauses or episode transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + number of days) | O(1) | Accepted but unnecessarily complex |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Initialize a running cumulative duration `prefix = 0`.
3. Initialize the answer `ans = 0`.
4. Process the episodes in order.
5. Add the current episode duration to `prefix`.
6. Check whether `prefix % m == 0`.

If the cumulative duration is divisible by `m`, then the end of this episode coincides with the end of some full viewing day.
7. If the condition holds, increment `ans`.
8. After all episodes are processed, output `ans`.

Why does this automatically handle the final partial day? Because a partial day never ends at a time that is a multiple of `m`. Only full viewing days correspond to cumulative watched times `k·m`. Thus counting episode endings at multiples of `m` counts exactly the successful days and ignores any final incomplete day.

### Why it works

Let `pref[i]` be the moment when episode `i` finishes.

After `k` full viewing days, Kolya has watched exactly `k·m` units of time. A day is successful precisely when its ending moment coincides with an episode ending. That means there must exist an episode `i` such that

```
pref[i] = k·m
```

for some integer `k`.

This condition is equivalent to

```
pref[i] % m = 0
```

Every successful day corresponds to exactly one episode-ending time divisible by `m`, and every such episode-ending time corresponds to a successful day. The algorithm counts exactly these moments, so the result is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
t = list(map(int, input().split()))

prefix = 0
ans = 0

for x in t:
    prefix += x
    if prefix % m == 0:
        ans += 1

print(ans)
```

The solution maintains the cumulative duration of all episodes processed so far.

Whenever the cumulative duration becomes divisible by `m`, it means the current episode ends exactly at the end of some full viewing day. We increase the answer immediately.

No additional data structures are required. The cumulative sum can become as large as `1000 × 10^9 = 10^12`, which easily fits in Python integers.

A common implementation mistake is trying to reason about individual days and episode positions. The divisibility condition already captures the entire process. Another mistake is worrying about the final partial day. Since only multiples of `m` are counted, incomplete days are automatically excluded.

## Worked Examples

### Sample 1

Input:

```
4 2
1 1 1 1
```

| Episode | Duration | Prefix Sum | Prefix % 2 | Successful Day Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 | 1 |
| 3 | 1 | 3 | 1 | 1 |
| 4 | 1 | 4 | 0 | 2 |

Output:

```
2
```

Episode 2 ends at time 2 and episode 4 ends at time 4. Both moments are exact multiples of the daily viewing time, so both correspond to successful days.

### Sample 2

Input:

```
4 3
1 1 2 1
```

| Episode | Duration | Prefix Sum | Prefix % 3 | Successful Day Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 2 | 0 |
| 3 | 2 | 4 | 1 | 0 |
| 4 | 1 | 5 | 2 | 0 |

Output:

```
0
```

No episode-ending time is divisible by 3. The first day ends in the middle of episode 3, and the remaining viewing time forms a partial final day, which does not count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through all episodes |
| Space | O(1) | Only a few integer variables are stored |

With `n ≤ 1000`, this runs comfortably within the limits. The algorithm performs only simple arithmetic operations and uses constant additional memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    t = list(map(int, input().split()))

    prefix = 0
    ans = 0

    for x in t:
        prefix += x
        if prefix % m == 0:
            ans += 1

    return str(ans)

# provided samples
assert run("4 2\n1 1 1 1\n") == "2", "sample 1"
assert run("4 3\n1 1 2 1\n") == "0", "sample 2"

# minimum size
assert run("1 1\n1\n") == "1", "single episode exactly one full day"

# partial final day
assert run("1 5\n3\n") == "0", "only partial day"

# all equal values
assert run("5 2\n2 2 2 2 2\n") == "5", "every episode end is successful"

# off-by-one style check
assert run("2 2\n1 3\n") == "1", "only final episode end matches"

# large values
assert run("3 1000000000\n1000000000 1000000000 1000000000\n") == "3", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Smallest valid instance |
| `1 5 / 3` | `0` | Partial final day is not counted |
| `5 2 / 2 2 2 2 2` | `5` | Every episode end matches a day boundary |
| `2 2 / 1 3` | `1` | Correct handling when only the final episode qualifies |
| Large `10^9` values | `3` | Large-number arithmetic |

## Edge Cases

Consider the input

```
1 5
3
```

The cumulative episode-ending time is 3. Since `3 % 5 != 0`, the algorithm does not count it and returns `0`. This matches the rule that a final partial day is not successful.

Now consider

```
2 3
1 2
```

The cumulative sums are 1 and 3. Only 3 is divisible by 3, so the answer is `1`.

Trace:

```
prefix = 1 -> not counted
prefix = 3 -> counted
```

The algorithm counts the day boundary, not merely the existence of an episode ending.

Finally, consider

```
2 2
1 3
```

The cumulative sums are 1 and 4.

```
1 % 2 = 1
4 % 2 = 0
```

Only the second episode contributes, producing answer `1`. The first day ends inside episode 2, while the second full day ends exactly when the series finishes. The algorithm captures this distinction automatically through divisibility of cumulative episode-ending times.
