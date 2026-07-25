---
title: "CF 102861A - Sticker Album"
description: "The album has N empty slots, and every packet contributes a random number of stickers. A packet can contain any integer amount between A and B, with every value having the same probability."
date: "2026-07-25T14:00:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "A"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 45
verified: true
draft: false
---

[CF 102861A - Sticker Album](https://codeforces.com/problemset/problem/102861/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The album has `N` empty slots, and every packet contributes a random number of stickers. A packet can contain any integer amount between `A` and `B`, with every value having the same probability. The goal is not to simulate one collection process, but to compute the average number of packets needed until the accumulated stickers reach at least `N`.

The input values describe the target number of stickers and the smallest and largest possible packet sizes. The output is a floating point value representing the expected number of packets required.

The constraint `N <= 10^6` is the main difficulty. A solution that tries every possible collection history is impossible because the number of histories grows exponentially. Even a dynamic programming solution that performs a transition over every possible packet size for every state would need around `N * (B - A + 1)` operations, which can reach `10^12` when both values are large. The solution must process each state in close to constant time.

There are several cases where a direct formula can fail. The first is when packets can contain zero stickers. For example, with input `1 0 1`, a packet gives either zero or one sticker. The expected answer is `2.0`, because the first packet succeeds with probability one half, and the number of attempts follows a geometric distribution. A formula that divides by the average packet size would fail because the average is not enough information when zero progress is possible.

Another edge case is when every packet has the same size. For input `30 3 3`, every packet gives exactly three stickers, so the answer is `10.0`. Treating the range as if it contained multiple equally likely values would introduce an incorrect division by the range length.

A final boundary case appears when the minimum packet size already finishes small states. For input `5 5 10`, one packet always completes the album, so the answer is `1.0`. A recurrence that accidentally includes impossible previous states can produce values larger than one.

## Approaches

A straightforward dynamic programming solution defines `dp[x]` as the expected number of packets needed when `x` stickers are still missing. If a packet contains `k` stickers, the remaining amount becomes `max(0, x-k)`. The recurrence is

`dp[x] = 1 + average(dp[max(0, x-k)])`

over all possible packet sizes.

This approach is correct because every state only depends on smaller remaining amounts. The problem is the transition. For every `x`, checking every value from `A` to `B` can require up to one million operations. With one million states, this becomes about `10^12` operations in the worst case, which is far beyond the limit.

The key observation is that the transition uses a consecutive range of previous states. When `A > 0`, the values `dp[x-B]` through `dp[x-A]` are the only non-zero contributions. When `A = 0`, the transition also contains `dp[x]` itself because a zero sticker packet leaves the state unchanged. In that case, the recurrence can be rearranged algebraically so the current value is still computed in constant time.

Maintaining prefix sums of the dynamic programming values lets us retrieve any consecutive range sum in constant time. The original quadratic transition becomes a linear scan from `1` to `N`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N(B - A + 1)) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` where `dp[x]` stores the expected number of packets needed to collect `x` more stickers. Also maintain `pref[x]`, the prefix sum of all `dp` values up to `x`.
2. Process the states from `1` to `N`. We always solve smaller missing amounts first, which means every value needed by the recurrence is already known.
3. If `A > 0`, handle the normal recurrence. The possible previous states form the interval from `max(0, x-B)` to `x-A`. Use the prefix sums to get the sum of this interval and compute:

`dp[x] = 1 + interval_sum / (B-A+1)`

The `1` represents buying the next packet, and the average represents the expected remaining work after that packet.
4. If `A = 0`, isolate the current state from the recurrence. The zero sticker packet contributes `dp[x]` itself, so the equation becomes:

`dp[x] = (B+1 + sum(dp[j]) for j in [max(0,x-B), x-1]) / B`

This avoids circular dependency and allows the same forward iteration.
5. After computing each `dp[x]`, update its prefix sum so future states can query ranges immediately.

Why it works: The dynamic programming state exactly represents the expected remaining number of packets for each possible amount of missing stickers. The recurrence follows directly from conditioning on the first packet purchased. Prefix sums only change how the needed average is calculated, not the mathematical value of the recurrence. The special handling of `A = 0` removes the only case where the current state depends on itself, so every state is computed from already finalized values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, A, B = map(int, input().split())

    dp = [0.0] * (N + 1)
    pref = [0.0] * (N + 1)

    count = B - A + 1

    for x in range(1, N + 1):
        if A == 0:
            left = max(0, x - B)
            if left == 0:
                previous_sum = pref[x - 1]
            else:
                previous_sum = pref[x - 1] - pref[left - 1]
            dp[x] = (B + 1 + previous_sum) / B
        else:
            left = max(0, x - B)
            right = x - A
            if right >= left:
                interval_sum = pref[right]
                if left > 0:
                    interval_sum -= pref[left - 1]
            else:
                interval_sum = 0.0
            dp[x] = 1.0 + interval_sum / count

        pref[x] = pref[x - 1] + dp[x]

    print("{:.10f}".format(dp[N]))

if __name__ == "__main__":
    solve()
```

The array `dp` stores the answer for every smaller target, while `pref` stores cumulative sums so a range of states can be retrieved without looping. The prefix sum update happens immediately after calculating a state because later states depend on all previous values.

The branch for `A == 0` is necessary because the ordinary recurrence contains the unknown value `dp[x]`. After moving that term to the left side, the denominator becomes `B`, not `B+1`. Missing this algebraic adjustment is the most common implementation error.

For `A > 0`, `right = x - A` is the largest previous state that can remain after receiving the smallest packet. The lower bound uses `max(0, x-B)` because receiving a large packet can finish the album completely, which corresponds to `dp[0] = 0`.

Python floating point values are sufficient because the required error tolerance is `10^-5`.

## Worked Examples

For input `40 0 2`, the zero packet case is used.

| x | Previous sum used | dp[x] |
| --- | --- | --- |
| 1 | dp[0] = 0 | 1.50000 |
| 2 | dp[0] + dp[1] = 1.50000 | 2.25000 |
| 3 | dp[1] + dp[2] = 3.75000 | 3.37500 |
| 40 | dp[38] + dp[39] | 40.33333 |

The trace shows how zero sticker packets increase the expectation. The recurrence cannot simply use the average packet size because failed packets still consume attempts.

For input `100 1 10`, every packet makes positive progress, so the normal transition is used.

| x | Range of previous states | dp[x] |
| --- | --- | --- |
| 1 | empty | 1.00000 |
| 2 | dp[1] | 1.10000 |
| 3 | dp[1] to dp[2] | 1.21000 |
| 100 | dp[90] to dp[99] | 18.72727 |

The trace demonstrates that only a sliding interval of previous values is needed. Prefix sums allow that interval to be queried instantly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each sticker count is processed once and every transition uses prefix sums. |
| Space | O(N) | The algorithm stores one value and one prefix sum for every possible remaining sticker count. |

The maximum of one million states is practical for a linear algorithm. The memory usage is also linear and fits comfortably because only two arrays of floating point values are stored.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    N, A, B = map(int, sys.stdin.readline().split())

    dp = [0.0] * (N + 1)
    pref = [0.0] * (N + 1)

    for x in range(1, N + 1):
        if A == 0:
            left = max(0, x - B)
            s = pref[x - 1]
            if left > 0:
                s -= pref[left - 1]
            dp[x] = (B + 1 + s) / B
        else:
            left = max(0, x - B)
            right = x - A
            s = 0.0
            if right >= left:
                s = pref[right]
                if left > 0:
                    s -= pref[left - 1]
            dp[x] = 1 + s / (B - A + 1)
        pref[x] = pref[x - 1] + dp[x]

    sys.stdin = old_stdin
    return "{:.5f}".format(dp[N])

assert abs(float(solve_data("40 0 2")) - 40.33333) < 1e-5
assert abs(float(solve_data("100 1 10")) - 18.72727) < 1e-5
assert abs(float(solve_data("30 3 3")) - 10.0) < 1e-5
assert abs(float(solve_data("314 5 8")) - 48.74556) < 1e-5

assert abs(float(solve_data("1 1 1")) - 1.0) < 1e-5
assert abs(float(solve_data("1 0 1")) - 2.0) < 1e-5
assert abs(float(solve_data("5 5 10")) - 1.0) < 1e-5
assert abs(float(solve_data("1000000 1000000 1000000")) - 1.0) < 1e-5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1.00000` | Minimum target with deterministic packets |
| `1 0 1` | `2.00000` | Zero-sized packets and self-dependent recurrence |
| `5 5 10` | `1.00000` | Minimum packet already finishes the album |
| `1000000 1000000 1000000` | `1.00000` | Maximum-size deterministic boundary case |

## Edge Cases

For `1 0 1`, the algorithm enters the zero minimum branch. The previous sum is only `dp[0]`, which is zero, so `dp[1] = (1 + 1 + 0) / 1 = 2`. This matches the expected number of attempts until the first successful one-sticker packet.

For `30 3 3`, every transition has only one possible packet size. The interval contains exactly the state three positions behind the current state, so the values become `dp[3] = 1`, `dp[6] = 2`, and finally `dp[30] = 10`. The deterministic behavior is preserved.

For `5 5 10`, all packet sizes are enough to finish immediately. For every state from `1` to `5`, the transition range is empty, leaving `dp[x] = 1`. The final answer is correctly one packet.

For `1000000 1000000 1000000`, the algorithm does not attempt to allocate a transition table or loop through packet sizes. It performs one million constant-time updates and returns `1.0`, which demonstrates why the linear approach is necessary.

I can also adapt the editorial to a shorter Codeforces-style format if you want a version closer to what would appear in an official contest analysis.
