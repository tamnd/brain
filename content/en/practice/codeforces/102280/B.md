---
title: "CF 102280B - \u0421\u0443\u043c\u0430\u0441\u0448\u0435\u0434\u0448\u0438\u0435 \u0433\u043e\u043d\u043a\u0438 \u043d\u0430 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0430\u0445"
description: "We have two independent minibuses. During the one-hour interval from 08:00 to 09:00, each minibus reaches the intersection exactly once, and its arrival time is uniformly distributed over the 3600 seconds of the hour. The traffic light starts with green at time 0."
date: "2026-08-13T16:04:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "B"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 99
verified: true
draft: false
---

[CF 102280B - \u0421\u0443\u043c\u0430\u0441\u0448\u0435\u0434\u0448\u0438\u0435 \u0433\u043e\u043d\u043a\u0438 \u043d\u0430 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0430\u0445](https://codeforces.com/problemset/problem/102280/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two independent minibuses. During the one-hour interval from 08:00 to 09:00, each minibus reaches the intersection exactly once, and its arrival time is uniformly distributed over the 3600 seconds of the hour.

The traffic light starts with green at time 0. Green lasts `g` seconds, red lasts `r` seconds, and this pattern repeats. A dangerous race starts exactly when both minibuses arrive while the light is red and, more specifically, both are waiting during the same red phase. If they arrive during different red phases, they do not meet and no race occurs.

The input contains `g` and `r`, both between 1 and 3600. The output is the probability that the two arrival times belong to the same red interval.

The upper bound of 3600 is small enough that even a few thousand operations are trivial. However, the most useful solution does not need to simulate every second or every pair of arrival times. The periodic structure lets us reduce the entire probability calculation to a constant number of arithmetic operations. Since the required error is only `10^-6`, ordinary double-precision floating point is more than sufficient.

The main edge cases come from the fact that the one-hour observation interval does not necessarily end at the end of a traffic-light cycle. For example, with `g = 3600` and `r = 1`, the whole hour is green, so the answer is exactly `0`. A careless formula that assumes at least one complete red phase inside the hour would incorrectly add a red interval.

Another boundary case is `g = 3000`, `r = 1000`. The first cycle lasts 4000 seconds. During our 3600-second observation window, the light is green for the first 3000 seconds and red for only the final 600 seconds. The correct probability is

`600^2 / 3600^2 = 1 / 36 ≈ 0.0277777778`.

A solution that always adds a complete red interval of length `r` for the final cycle would use `1000^2` instead of `600^2` and produce the wrong answer.

The smallest possible input is `g = 1`, `r = 1`. There are 1800 complete cycles in the hour, and every red interval has length 1. The probability is

`1800 / 3600^2 = 1 / 7200 ≈ 0.000138888889`.

This case is useful because it checks both the cycle count and the fact that the answer can be very small.

## Approaches

A direct approach can divide the hour into 3600 one-second intervals and inspect every ordered pair of arrival seconds. There are `3600 * 3600 = 12,960,000` pairs in the worst case. For each pair we can determine whether the two seconds belong to the same red phase. This is conceptually correct because the traffic-light state is constant inside every open one-second interval, and the exact boundaries have probability zero for continuously distributed arrival times. However, nearly thirteen million pair checks are unnecessary and are a poor fit for the original 0.5 second limit.

The brute-force idea works because we are ultimately measuring an area in the square of possible arrival times. Let the first arrival be `x` and the second be `y`. Since both are uniform over 3600 seconds, every point `(x, y)` in the square `[0, 3600] × [0, 3600]` has uniform probability density. A race happens when `x` and `y` lie inside the same red interval.

This observation gives the key simplification. Suppose one red interval has length `L`. Both arrival times must independently fall inside that interval, so the corresponding region in the `(x, y)` plane is a square with side `L` and area `L²`. Different red intervals produce disjoint squares. Consequently, if the red intervals inside the hour have lengths `L1, L2, ...`, the total favorable area is

`L1² + L2² + ...`.

The total area of all possible pairs is `3600²`, so the answer is

`(L1² + L2² + ...) / 3600²`.

All complete traffic-light cycles contain exactly one red interval of length `r`. If the hour contains `q` complete cycles, they contribute `q * r²`. There can also be one incomplete cycle at the end. Let `rem` be the number of seconds remaining after the complete cycles. The first `g` seconds of that remainder are green. Only `max(0, rem - g)` seconds can belong to red, so the incomplete cycle contributes the square of that length.

Thus the whole calculation becomes constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3600²) | O(1) | Too slow for the tight limit |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Set the observation length to `T = 3600` seconds and the traffic-light cycle length to `cycle = g + r`. Dividing `T` by `cycle` gives the number `q` of complete cycles contained entirely inside the hour.
2. Compute `rem = T % cycle`. This is the length of the incomplete cycle at the end of the hour. If `rem <= g`, that entire remainder is green, so it contributes nothing to the race probability.
3. If `rem > g`, the part after the first `g` seconds of the incomplete cycle is red. Its length is `rem - g`. This red segment contributes `(rem - g)²` to the favorable area.
4. Each of the `q` complete cycles contains a red interval of length `r`. Together they contribute `q * r²`.
5. Add the complete and partial contributions and divide by `T²`. The numerator is the area of all arrival-time pairs that cause a race, while the denominator is the area of all possible arrival-time pairs.
6. Print the resulting floating-point value with enough digits to satisfy the required `10^-6` error tolerance.

### Why it works

For every red interval of length `L`, a race occurs precisely when both independent arrival times fall inside that same interval. In the two-dimensional space of arrival-time pairs, those possibilities form a square of area `L²`. Squares belonging to different red intervals are disjoint, so their areas can be added. The algorithm calculates exactly the lengths of every red interval intersecting the one-hour window, including the possibly truncated final interval. Dividing their squared lengths by the total area `3600²` therefore gives exactly the desired probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = 3600

def solve():
    g, r = map(int, input().split())

    cycle = g + r
    full_cycles = T // cycle
    rem = T % cycle

    favorable = full_cycles * r * r

    partial_red = max(0, rem - g)
    favorable += partial_red * partial_red

    answer = favorable / (T * T)
    print(f"{answer:.12f}")

if __name__ == "__main__":
    solve()
```

The first three integer calculations determine how the hour is divided into complete and incomplete traffic-light cycles. Since `g` and `r` are integers and at most 3600, there is no danger of integer overflow in Python, and the same arithmetic is also safe in standard 64-bit integer implementations.

The expression `max(0, rem - g)` handles the final partial cycle. If the remainder ends during green, `rem - g` is negative, but there is no red interval to count. Clamping it to zero avoids accidentally adding a positive square.

The multiplication by `r * r` happens before converting to floating point. This keeps the geometric calculation exact until the final division. The final answer is printed with 12 digits after the decimal point, giving considerably more precision than the required `10^-6`.

The traffic-light boundary itself does not need special treatment. A single exact time, such as the instant at which green changes to red, has probability zero under a continuous uniform distribution, so whether that endpoint is assigned to one phase or the other cannot change the answer.

## Worked Examples

### Sample 1

For `g = 1800` and `r = 1800`, one complete cycle lasts exactly 3600 seconds. The entire hour consists of one green interval followed by one red interval.

| Variable | Value |
| --- | --- |
| `T` | 3600 |
| `cycle` | 3600 |
| `full_cycles` | 1 |
| `rem` | 0 |
| `partial_red` | 0 |
| `favorable` | 3,240,000 |
| `answer` | 0.25 |

The only red interval has length 1800, so the favorable area is `1800² = 3,240,000`. The total arrival-time area is `3600² = 12,960,000`, giving `3,240,000 / 12,960,000 = 0.25`.

### Sample 2

For `g = 2700` and `r = 3600`, one complete cycle lasts 6300 seconds, which is longer than the entire hour. There are no complete cycles. The hour ends 3600 seconds into the first cycle, after 2700 seconds of green, leaving 900 seconds of red.

| Variable | Value |
| --- | --- |
| `T` | 3600 |
| `cycle` | 6300 |
| `full_cycles` | 0 |
| `rem` | 3600 |
| `partial_red` | 900 |
| `favorable` | 810,000 |
| `answer` | 0.0625 |

The favorable area is `900² = 810,000`. Dividing by `3600²` gives `0.0625`.

These traces demonstrate why the partial cycle must be handled separately. In the first sample there is exactly one complete cycle and no remainder. In the second sample there is no complete cycle at all, yet the final part of the hour contains a substantial red interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed. |
| Space | O(1) | Only a few integer and floating-point variables are stored. |

The constraints allow `g` and `r` to be as large as 3600, but the algorithm does not depend on their magnitude. It performs the same constant amount of work for every input, so it comfortably fits the 0.5 second time limit and uses negligible memory compared with the 64 MB limit.

## Test Cases

```python
import sys
import io

T = 3600

def solve():
    g, r = map(int, input().split())

    cycle = g + r
    full_cycles = T // cycle
    rem = T % cycle

    favorable = full_cycles * r * r

    partial_red = max(0, rem - g)
    favorable += partial_red * partial_red

    answer = favorable / (T * T)
    print(f"{answer:.12f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def assert_close(inp: str, expected: float, message: str):
    actual = float(run(inp))
    assert abs(actual - expected) <= 1e-12, message

# Provided samples
assert_close("1800 1800\n", 0.25, "sample 1")
assert_close("2700 3600\n", 0.0625, "sample 2")

# Minimum-size input
assert_close("1 1\n", 1 / 7200, "minimum values")

# Maximum-size input
assert_close("3600 3600\n", 0.0, "maximum values")

# Final partial cycle ends exactly at the green/red boundary
assert_close("3600 1\n", 0.0, "no red time inside the hour")

# Only 600 seconds of the final red interval are visible
assert_close("3000 1000\n", 600 * 600 / (3600 * 3600), "partial red interval")

# Many complete cycles, with no partial red interval
assert_close("1000 2000\n", 2000 * 2000 / (3600 * 3600), "complete red interval")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0.000138888889` | Minimum values and many complete cycles |
| `3600 3600` | `0.000000000000` | Maximum values and an hour containing only green |
| `3600 1` | `0.000000000000` | Boundary where the observation ends exactly as green ends |
| `3000 1000` | `0.027777777778` | A partially visible red interval |
| `1000 2000` | `0.308641975309` | Complete cycles followed by a green-only remainder |

## Edge Cases

For `1 1`, the cycle length is 2, so `3600 // 2 = 1800` complete cycles and `rem = 0`. Every red interval has length 1, giving favorable area `1800 * 1² = 1800`. The result is `1800 / 12,960,000 = 0.000138888889`. The algorithm never needs to iterate over those 1800 cycles.

For `3600 3600`, the cycle length is 7200, so there are zero complete cycles and `rem = 3600`. Since the remainder is exactly the green duration, `partial_red = max(0, 3600 - 3600) = 0`. The answer is zero. This catches implementations that accidentally treat the endpoint of green as a positive-length red interval.

For `3600 1`, the cycle length is 3601. Again there are zero complete cycles, and the 3600-second observation ends exactly one second before the first red phase would begin. The partial red length is `max(0, 3600 - 3600) = 0`, so the answer is zero.

For `3000 1000`, the cycle length is 4000. The hour contains the first 3000 seconds of green and then 600 seconds of red. Thus `full_cycles = 0`, `rem = 3600`, and `partial_red = 600`. The favorable area is `600² = 360,000`, producing `360,000 / 12,960,000 = 0.027777777778`. This is the main off-by-one style case because the visible red interval is shorter than the configured red duration.

For `1000 2000`, the cycle length is 3000. The hour contains one complete cycle and a 600-second remainder. That remainder is still inside the next green phase, so it contributes nothing. The only favorable region comes from the complete red interval of length 2000, giving `2000² / 3600² = 0.308641975309`. This verifies that a remainder should not be counted merely because it exists, only its part after the green phase matters.
