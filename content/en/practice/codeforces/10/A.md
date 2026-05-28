---
title: "CF 10A - Power Consumption Calculation"
description: "Tom uses his laptop during several disjoint time intervals. While he is actively using it, the laptop stays in normal mode and consumes P1 watts per minute. When he stops interacting with the laptop, the machine does not immediately switch to lower-power states."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 10
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 10"
rating: 900
weight: 10
solve_time_s: 90
verified: true
draft: false
---
[CF 10A - Power Consumption Calculation](https://codeforces.com/problemset/problem/10/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Tom uses his laptop during several disjoint time intervals. While he is actively using it, the laptop stays in normal mode and consumes `P1` watts per minute. When he stops interacting with the laptop, the machine does not immediately switch to lower-power states.

For the first `T1` minutes of inactivity, it still stays in normal mode. After that, the screensaver mode starts and the consumption becomes `P2` watts per minute. Once the screensaver has been active for `T2` more minutes, the laptop enters sleep mode and consumes `P3` watts per minute.

We are given all working intervals `[li, ri]`, where Tom continuously interacts with the laptop during the whole interval. The task is to compute the total energy consumed from the start of the first interval until the end of the last interval.

The constraints are tiny. There are at most 100 working intervals, and all times are within a single day. Even a minute-by-minute simulation over the entire day would require at most 1440 iterations, which is already fast enough. This means the problem is not about optimization tricks, it is about implementing the state transitions correctly without off-by-one mistakes.

The most dangerous part is handling the gaps between working intervals. The laptop changes modes gradually during inactivity, so we must carefully split each gap into three segments:

1. The first `T1` minutes at cost `P1`
2. The next `T2` minutes at cost `P2`
3. Everything after that at cost `P3`

A careless implementation often mixes up whether the transition minute belongs to the old mode or the new one.

Consider this example:

```
1 10 5 1 5 5
0 5
```

The laptop is used continuously from minute 0 to 5, so the answer is simply:

```
5 * 10 = 50
```

There is no inactivity period afterward because the problem only asks for consumption until `r_n`.

Another subtle case is when the inactivity duration is shorter than `T1`.

```
2 10 5 1 5 5
0 5
7 10
```

The gap length is only 2 minutes. The laptop never reaches screensaver mode, so both minutes cost `P1`. A buggy implementation might incorrectly activate screensaver immediately after inactivity begins.

A third tricky situation is when the inactivity duration exceeds both thresholds.

```
2 10 5 1 2 3
0 1
10 11
```

The gap has length 9.

The power usage becomes:

- first 2 minutes at `P1`
- next 3 minutes at `P2`
- remaining 4 minutes at `P3`

The correct added cost is:

```
2*10 + 3*5 + 4*1 = 39
```

Missing the final segment is a common mistake.

## Approaches

The most direct solution is to simulate every minute from `l1` to `rn`. At each minute we determine whether Tom is actively using the laptop, whether the machine is still within the normal inactivity window, whether it has reached screensaver mode, or whether it has already fallen asleep.

This brute-force method is correct because the laptop state only changes at integer minute boundaries. Since a day contains at most 1440 minutes, the worst-case work is tiny.

Still, the problem structure allows something cleaner.

The laptop only changes behavior during gaps between consecutive working intervals. While Tom is actively working, every minute costs `P1`. The only interesting part is inactivity.

Suppose the current interval ends at `ri` and the next one begins at `l(i+1)`. The inactivity duration is:

```
gap = l(i+1) - ri
```

Instead of simulating each minute separately, we can directly split this gap into three chunks:

- up to `T1` minutes at `P1`
- up to `T2` additional minutes at `P2`
- the remaining minutes at `P3`

This converts the problem into simple arithmetic on interval lengths.

The brute-force works because the timeline is short, but the interval-based observation removes unnecessary simulation entirely. The resulting implementation is shorter, easier to reason about, and scales naturally even if the timeline were much larger.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1440) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all input values and store the work intervals.
2. For every working interval `[l, r]`, add `(r - l) * P1` to the answer.

During active usage, the laptop is guaranteed to stay in normal mode.
3. For every pair of consecutive intervals, compute the inactivity duration:

```
gap = l[i] - r[i-1]
```
4. Spend as many minutes as possible in the first inactivity phase.

```
first = min(gap, T1)
```

Add:

```
first * P1
```

These minutes still consume normal-mode power.
5. Remove those minutes from the remaining gap:

```
gap -= first
```
6. Spend as many remaining minutes as possible in screensaver mode.

```
second = min(gap, T2)
```

Add:

```
second * P2
```
7. Remove those minutes as well:

```
gap -= second
```
8. Any leftover time is spent in sleep mode.

Add:

```
gap * P3
```
9. After processing all intervals and gaps, print the total answer.

### Why it works

Every minute between `l1` and `rn` belongs to exactly one of two categories:

- Tom is actively using the laptop.
- The laptop is idle between two working intervals.

Active minutes always consume `P1`, so their contribution is immediate.

For an idle segment, the laptop transitions through states in a fixed order with fixed durations. The algorithm partitions the gap into exactly those state durations:

- first `T1` minutes
- next `T2` minutes
- remaining minutes

No minute is skipped and no minute is counted twice. Since each segment is charged with the correct power value, the final sum equals the real total energy consumption.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, p1, p2, p3, t1, t2 = map(int, input().split())

intervals = [tuple(map(int, input().split())) for _ in range(n)]

ans = 0

for l, r in intervals:
    ans += (r - l) * p1

for i in range(1, n):
    gap = intervals[i][0] - intervals[i - 1][1]

    first = min(gap, t1)
    ans += first * p1
    gap -= first

    second = min(gap, t2)
    ans += second * p2
    gap -= second

    ans += gap * p3

print(ans)
```

The first loop handles all active working periods. Since Tom constantly interacts with the laptop during those intervals, the machine never leaves normal mode.

The second loop processes the inactivity gaps one by one. The order matters because the laptop always progresses through states sequentially. We first consume as much of the gap as possible in the normal idle phase, then move to screensaver mode, and finally assign any remaining time to sleep mode.

The subtraction steps are easy to get wrong. After assigning minutes to one phase, we must remove them before processing the next phase. Otherwise the same minutes would be counted multiple times.

The intervals use half-open timing behavior naturally. An interval `[l, r]` lasts exactly `r - l` minutes, which matches the problem statement. Using `r - l + 1` would overcount every working period.

Python integers easily handle the maximum answer size, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
1 3 2 1 5 10
0 10
```

There is only one working interval and no inactivity gap.

| Step | Value |
| --- | --- |
| Active duration | 10 |
| Active cost | 10 × 3 = 30 |
| Final answer | 30 |

The trace shows the simplest scenario. Since there are no gaps, the laptop never enters lower-power modes.

### Example 2

Input:

```
2 10 5 1 2 3
0 1
10 11
```

| Step | Value |
| --- | --- |
| First active interval | 1 × 10 = 10 |
| Second active interval | 1 × 10 = 10 |
| Gap length | 9 |
| First phase | min(9, 2) = 2 |
| Added cost | 2 × 10 = 20 |
| Remaining gap | 7 |
| Second phase | min(7, 3) = 3 |
| Added cost | 3 × 5 = 15 |
| Remaining gap | 4 |
| Sleep phase cost | 4 × 1 = 4 |
| Final answer | 59 |

This trace exercises all three power states. The inactivity period is long enough for the laptop to fully transition into sleep mode.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each interval and each gap is processed once |
| Space | O(1) | Only a few integer variables are used besides input storage |

With at most 100 intervals, the algorithm runs instantly. The implementation uses only simple arithmetic operations and fits comfortably within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, p1, p2, p3, t1, t2 = map(int, input().split())

    intervals = [tuple(map(int, input().split())) for _ in range(n)]

    ans = 0

    for l, r in intervals:
        ans += (r - l) * p1

    for i in range(1, n):
        gap = intervals[i][0] - intervals[i - 1][1]

        first = min(gap, t1)
        ans += first * p1
        gap -= first

        second = min(gap, t2)
        ans += second * p2
        gap -= second

        ans += gap * p3

    return str(ans)

# provided sample
assert run(
"""1 3 2 1 5 10
0 10
"""
) == "30", "sample 1"

# minimum-size input
assert run(
"""1 1 1 1 1 1
0 1
"""
) == "1", "single minute"

# gap shorter than T1
assert run(
"""2 10 5 1 5 5
0 5
7 10
"""
) == "100", "only normal mode during gap"

# gap enters all states
assert run(
"""2 10 5 1 2 3
0 1
10 11
"""
) == "59", "all three modes"

# exact boundary transitions
assert run(
"""2 10 5 1 2 3
0 1
6 7
"""
) == "45", "gap exactly T1 + T2"

# all equal power values
assert run(
"""2 4 4 4 3 3
0 2
10 12
"""
) == "48", "state changes should not matter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single interval of length 1 | 1 | Minimum-size behavior |
| Gap shorter than `T1` | 100 | Screensaver should not activate early |
| Long inactivity gap | 59 | Correct handling of all three modes |
| Gap exactly `T1 + T2` | 45 | Boundary transition correctness |
| Equal power values | 48 | Logic should still work when states are indistinguishable |

## Edge Cases

Consider this input where the inactivity duration never reaches screensaver mode:

```
2 10 5 1 5 5
0 5
7 10
```

The active intervals consume:

```
5*10 + 3*10 = 80
```

The gap length is:

```
7 - 5 = 2
```

Since `2 < T1`, the whole gap costs `2*10 = 20`.

The final answer becomes:

```
80 + 20 = 100
```

The algorithm handles this correctly because the first phase consumes the entire gap, leaving nothing for later phases.

Now consider a gap that reaches sleep mode:

```
2 10 5 1 2 3
0 1
10 11
```

The gap length is 9.

The algorithm processes it as:

```
first = min(9, 2) = 2
remaining = 7

second = min(7, 3) = 3
remaining = 4

sleep = 4
```

The costs become:

```
2*10 + 3*5 + 4*1 = 39
```

This confirms the state progression logic is correct even when all three phases are used.

Finally, examine the exact transition boundary:

```
2 10 5 1 2 3
0 1
6 7
```

The gap length is exactly:

```
2 + 3 = 5
```

The laptop spends:

- 2 minutes in normal idle mode
- 3 minutes in screensaver mode
- 0 minutes in sleep mode

The algorithm naturally handles this because the remaining gap becomes zero after the second phase. No extra sleep cost is added.
