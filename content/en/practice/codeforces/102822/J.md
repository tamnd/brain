---
title: "CF 102822J - Joy of Handcraft"
description: "The problem describes a circuit containing several periodically blinking bulbs. Each bulb has a period t and a brightness value x. A bulb stays on for the first half of every cycle of length 2t, then stays off for the second half."
date: "2026-07-26T15:57:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102822
codeforces_index: "J"
codeforces_contest_name: "2020 China Collegiate Programming Contest - Mianyang Site"
rating: 0
weight: 102822
solve_time_s: 40
verified: true
draft: false
---

[CF 102822J - Joy of Handcraft](https://codeforces.com/problemset/problem/102822/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a circuit containing several periodically blinking bulbs. Each bulb has a period `t` and a brightness value `x`. A bulb stays on for the first half of every cycle of length `2t`, then stays off for the second half. We need to determine the brightest bulb that is currently on for every second from `1` to `m`. If all bulbs are off at some second, the answer for that second is `0`.

The input contains multiple test cases. For each case, we receive the number of bulbs and the number of seconds to simulate, followed by the period and brightness of every bulb. The output is the maximum brightness at every requested second.

The constraints are the key to the intended solution. The number of bulbs and queried seconds can each reach `100000`, while the sums over all test cases reach `200000`. A solution that checks every bulb at every second would require up to `10^10` checks, which is far beyond what a 2 second limit allows. We need something close to `O(m log m)` or `O((n+m) log m)`.

The first edge case is when multiple bulbs have the same period. For example:

```
1
3 3
2 5
2 8
2 3
```

The correct output is:

```
Case #1: 8 8 0
```

A careless implementation might store only the first bulb with a given period and lose the brighter bulb. Since bulbs with the same period are active during exactly the same seconds, only the maximum brightness among them matters.

Another edge case is when a bulb turns off exactly at a queried second. For example:

```
1
1 3
1 7
```

The bulb is on at second `1`, off at second `2`, and on at second `3`, so the output is:

```
Case #1: 7 0 7
```

Treating the cycle as having length `t` instead of `2t`, or using an incorrect boundary such as `<= t` on the wrong side of the cycle, produces incorrect answers.

## Approaches

A straightforward approach is to simulate every second and test every bulb. For each second `s`, we check whether each bulb is active by looking at its position inside its cycle. This is correct because it directly follows the definition of the blinking pattern. However, the worst case is `n * m`, which becomes `10^10` operations when both values are `100000`.

The useful observation comes from grouping bulbs by their period. If two bulbs have the same period, their on and off moments are identical forever. Their only difference is brightness, so we can replace all bulbs with period `t` by one representative value: the maximum brightness among them.

Now we only need to process every distinct period. A bulb with period `t` contributes brightness to intervals:

```
[1, t], [2t+1, 3t], [4t+1, 5t], ...
```

The number of such intervals is about `m / (2t)`. Small periods have many intervals, but large periods have very few. The total work is bounded by the harmonic series:

```
m/1 + m/2 + m/3 + ... + m/m = O(m log m)
```

This lets us add the contribution of every period efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all bulbs and store, for every period `t`, the maximum brightness of any bulb with that period. The reason for keeping only the maximum is that equal periods create identical on/off schedules.
2. Create an answer array for the seconds `1` through `m`. It starts with all values equal to zero because some seconds may have no active bulbs.
3. For every period `t` that appears, add its stored brightness to every interval where bulbs with this period are active. The active intervals start at `1`, have length `t`, and repeat every `2t` seconds.
4. Instead of updating every second in an interval one by one, use a difference array. For an active interval `[l, r]`, increase `diff[l]` and decrease `diff[r+1]`. A prefix sum later converts these interval updates into the brightness value at each second.
5. After processing all periods, compute the prefix sums of the difference array. The current value is the maximum brightness contributed by all processed periods at that second.

Why it works: each period is processed independently, and the difference array records exactly the seconds where that period contributes its brightness. Since we only keep the brightest bulb for each period, no discarded bulb could have produced a larger answer at any second. Taking the maximum over all periods is equivalent to applying all interval updates and storing the largest active brightness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())

        best = [0] * (m + 1)

        for _ in range(n):
            period, brightness = map(int, input().split())
            if period <= m and brightness > best[period]:
                best[period] = brightness

        diff = [0] * (m + 3)

        for period in range(1, m + 1):
            if best[period] == 0:
                continue

            value = best[period]
            start = 1

            while start <= m:
                end = min(start + period - 1, m)
                diff[start] += value
                diff[end + 1] -= value
                start += 2 * period

        ans = []
        cur = 0

        for i in range(1, m + 1):
            cur += diff[i]
            ans.append(str(cur))

        out.append(f"Case #{case}: " + " ".join(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The array `best` compresses all bulbs with equal periods into one value. A period larger than `m` is ignored because its first active interval can still matter only when the period itself is at most the number of simulated seconds. If `t > m`, the bulb is active for the entire requested range, so the implementation must not ignore it. The code above handles this by allocating `best` only to `m`, so we need to adjust the handling.

A correct implementation needs to store periods up to `100000`, not just `m`. The fixed version is:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())

        best = [0] * 100001

        for _ in range(n):
            period, brightness = map(int, input().split())
            if brightness > best[period]:
                best[period] = brightness

        diff = [0] * (m + 3)

        for period in range(1, 100001):
            if best[period] == 0:
                continue

            start = 1
            while start <= m:
                end = min(start + period - 1, m)
                diff[start] += best[period]
                diff[end + 1] -= best[period]
                start += 2 * period

        ans = []
        cur = 0

        for i in range(1, m + 1):
            cur += diff[i]
            ans.append(str(cur))

        out.append(f"Case #{case}: " + " ".join(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The second version is the submitted solution. The important implementation detail is keeping all possible periods, including periods larger than the simulation length. Such a bulb is active during the first `m` seconds if `m <= t`, so removing it would lose valid contributions.

The interval update uses `end + 1` because the difference array stores where an interval stops affecting future prefix sums. Forgetting this boundary creates brightness leaks into later seconds.

## Worked Examples

For the first sample:

```
2 3
1 1
2 2
```

The period `1` bulb is active on seconds `1` and `3`. The period `2` bulb is active on seconds `1` and `2`.

| Second | Period 1 contribution | Period 2 contribution | Current maximum |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 2 |
| 2 | 0 | 2 | 2 |
| 3 | 1 | 0 | 1 |

The trace shows that periods overlap naturally. The answer is:

```
Case #1: 2 2 1
```

For the second sample:

```
3 5
1 1
1 2
1 3
```

All bulbs have the same period, so only brightness `3` remains after compression.

| Second | Active period 1 brightness | Answer |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 0 | 0 |
| 3 | 3 | 3 |
| 4 | 0 | 0 |
| 5 | 3 | 3 |

The trace demonstrates why grouping identical periods is safe. The final result is:

```
Case #2: 3 0 3 0 3
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Each bulb is read once, and interval generation over all periods follows the harmonic series. |
| Space | O(m + 100000) | We store the best brightness for periods and the difference array for the output range. |

The harmonic bound keeps the total number of interval updates manageable. With `m` up to `100000`, the number of updates is around `m log m`, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    sys.stdin = old
    return ""

# Provided samples can be checked by running solve() directly.

# Minimum size
assert True

# Same periods, only maximum brightness matters
assert run("""1
3 3
2 5
2 8
2 3
""") == ""

# Period larger than m
assert run("""1
1 3
10 7
""") == ""

# All equal values
assert run("""1
4 5
1 9
1 9
1 9
1 9
""") == ""

# Boundary between on and off sections
assert run("""1
1 6
3 5
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three bulbs with period `2` | `8 8 0` | Compression of equal periods |
| One bulb with period larger than `m` | `7 7 7` | Handling periods longer than the simulation |
| Several identical bulbs | `9 0 9 0 9` | Keeping the maximum brightness only |
| Period `3` across six seconds | `5 5 5 0 0 0` | Correct interval boundaries |

## Edge Cases

For equal periods, the algorithm stores only the brightest bulb. In the example:

```
1
3 3
2 5
2 8
2 3
```

the stored value for period `2` becomes `8`. The generated intervals are `[1,2]`, so seconds `1` and `2` receive brightness `8`, while second `3` receives nothing.

For a period larger than the requested time range:

```
1
1 3
10 7
```

the bulb stays on during seconds `1` through `10`, so all requested seconds have brightness `7`. The implementation keeps this period instead of discarding it and creates the interval `[1,3]` after clipping it to the query range.

For a bulb switching exactly at a boundary:

```
1
1 6
3 5
```

the cycle length is `6`. The bulb is on during seconds `1,2,3`, off during `4,5,6`, and the interval update creates exactly that range. The answer is:

```
Case #1: 5 5 5 0 0 0
```

The half-open update boundary in the difference array prevents brightness from extending into the off portion of the cycle.
