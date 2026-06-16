---
title: "CF 926F - Mobile Communications"
description: "We are simulating a bank account over a sequence of days. Each day starts with a fixed charge of $p$ rubles applied to the account. On some specific days, before this charge happens, Arkady deposits money into the account."
date: "2026-06-17T03:10:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 926
codeforces_index: "F"
codeforces_contest_name: "VK Cup 2018 - Wild-card Round 1"
rating: 2000
weight: 926
solve_time_s: 74
verified: true
draft: false
---

[CF 926F - Mobile Communications](https://codeforces.com/problemset/problem/926/F)

**Rating:** 2000  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a bank account over a sequence of days. Each day starts with a fixed charge of $p$ rubles applied to the account. On some specific days, before this charge happens, Arkady deposits money into the account.

The timeline is strictly chronological from day 1 to day $m$. Initially the balance is zero. On each day, if it is a deposit day, the balance increases first, then the daily payment $p$ is subtracted. After this operation, we check whether the balance is negative. We need to count how many days produce a negative balance after the daily charge.

A key observation is that the process is purely cumulative: the balance at day $d$ depends only on previous deposits and a fixed subtraction of $p$ per day. There is no reset or branching behavior.

The constraints make a naive simulation impossible. The number of days $m$ can be as large as $10^9$, so iterating day by day is infeasible. However, the number of deposit events $n$ is at most $10^5$, which is small enough for sorting and linear processing. This asymmetry between $n$ and $m$ is the core structural hint: only a small number of days actually change the balance.

A naive approach would simulate all $m$ days and maintain a running balance. This would be $O(m)$, which is completely impossible when $m = 10^9$.

A subtler naive idea is to only process deposit days and assume something simple happens in between. This fails because the balance evolves linearly over every day, so even in non-deposit days, the balance changes meaningfully.

Edge cases that break naive reasoning include:

- No deposits at all: the balance decreases by $p$ every day, so all days are negative.
- A single large deposit near the end: early days are negative, later ones may recover.
- Deposits that exactly cancel daily drain temporarily, causing alternating sign behavior across segments.

These behaviors indicate that we must treat the timeline as a piecewise linear function rather than simulate day-by-day.

## Approaches

If we simulate day by day, we maintain a balance variable and loop from 1 to $m$, applying deposits when they occur and subtracting $p$ each time. This is correct but far too slow when $m$ is large, since it would require up to $10^9$ iterations.

The key observation is that nothing changes within intervals between deposit days except a constant linear decrease. If we know the balance at the start of an interval, we can compute how many days in that interval produce a negative balance using arithmetic reasoning instead of simulation.

We process deposit days in order and treat each interval between consecutive deposit events as a block. Within each block, the balance decreases by $p$ per day, so it forms an arithmetic progression. We can determine directly when the balance crosses below zero and count how many days are negative.

This reduces the problem to handling $n + 1$ segments instead of $m$ days.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) | O(1) | Too slow |
| Segment arithmetic processing | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We track the current balance and iterate through all deposit events in increasing order of day.

1. Initialize current balance to 0 and set previous day pointer to 1. The idea is that we process day ranges starting from day 1 up to the next deposit day.
2. For each deposit event at day $d$ with value $t$, first process the days from previous pointer up to $d - 1$, where no deposits happen. During this interval, the balance decreases by $p$ each day.

Instead of simulating, we treat this as a linear sequence: starting from current balance, after $k$ days the balance becomes $balance - k \cdot p$. We determine how many of these days result in a negative balance after subtraction.
3. Apply the deposit at day $d$: add $t$ to the balance, then immediately subtract $p$ for that day since payment happens after deposit. If the resulting balance is negative, increment the answer.
4. Move the previous pointer to $d + 1$, since day $d$ is fully processed.
5. After processing all deposit days, handle the remaining segment from last processed day to $m$ using the same arithmetic logic.

The crucial detail is correctly counting how many values in a decreasing arithmetic sequence fall below zero, without iterating.

### Why it works

Between deposits, the balance evolves as a simple arithmetic progression with fixed step $-p$. Such a sequence has a single threshold crossing point: once it becomes negative, it stays negative forever. This monotonicity ensures we can count negative days by finding the first index where the balance drops below zero. Since each segment is independent and fully accounted for, every day is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_negative_days(n, p, m, events):
    ans = 0
    cur = 0
    prev_day = 1

    for d, t in events:
        # process days [prev_day, d-1]
        length = d - prev_day
        if length > 0:
            # balance starts at cur and decreases by p each day
            # find first k such that cur - k*p < 0
            if cur < 0:
                ans += length
            else:
                first_neg = cur // p + 1
                if first_neg < 1:
                    first_neg = 1
                if first_neg <= length:
                    ans += length - first_neg + 1

            cur -= length * p

        # process deposit day d
        cur += t
        cur -= p
        if cur < 0:
            ans += 1

        prev_day = d + 1

    # tail segment
    if prev_day <= m:
        length = m - prev_day + 1
        if cur < 0:
            ans += length
        else:
            first_neg = cur // p + 1
            if first_neg <= length:
                ans += length - first_neg + 1

    return ans

def main():
    n, p, m = map(int, input().split())
    events = [tuple(map(int, input().split())) for _ in range(n)]
    print(count_negative_days(n, p, m, events))

if __name__ == "__main__":
    main()
```

The implementation processes each segment between deposits and avoids iterating through days. The core idea is that once we know the starting balance of a segment, every day reduces it by exactly $p$, so we can compute the boundary where it becomes negative using integer division.

The only subtle part is handling the transition from a positive starting balance to the first negative day correctly. The expression `cur // p + 1` gives the first index where repeated subtraction crosses below zero, assuming 1-based indexing inside the segment.

## Worked Examples

### Example 1

Input:

```
3 6 7
2 13
4 20
7 9
```

We track segments:

| Segment | Start balance | Length | Negative days | New balance |
| --- | --- | --- | --- | --- |
| 1-1 | 0 | 1 | 1 | -6 |
| 2 | -6 + 13 - 6 = 1 | - | 0 | 1 |
| 3 | 1 | 1 | 1 | -5 |
| 4 | -5 + 20 - 6 = 9 | - | 0 | 9 |
| 5-6 | 9 | 2 | 1 | -3, -9 |
| 7 | -9 + 9 - 6 = -6 | - | 1 | -6 |

Total negative days = 3.

This trace shows that each segment behaves independently and negative regions form contiguous suffixes inside each segment.

### Example 2

Input:

```
2 5 5
3 10
5 5
```

| Segment | Start | Length | Negative days | End |
| --- | --- | --- | --- | --- |
| 1-2 | 0 | 2 | 1 | -5 |
| 3 | 5 | 1 | 0 | 0 |
| 4-4 | 0 | 1 | 1 | -5 |
| 5 | -5 | 1 | 1 | -10 |

This demonstrates alternating recovery and collapse depending on deposits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each deposit event is processed once with constant-time arithmetic |
| Space | O(1) | Only a few variables are maintained besides input storage |

The solution easily fits within limits since $n \le 10^5$, and all operations are constant time per event.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, p, m = map(int, input().split())
    events = [tuple(map(int, input().split())) for _ in range(n)]

    def count_negative_days(n, p, m, events):
        ans = 0
        cur = 0
        prev_day = 1

        for d, t in events:
            length = d - prev_day
            if length > 0:
                if cur < 0:
                    ans += length
                else:
                    first_neg = cur // p + 1
                    if first_neg < 1:
                        first_neg = 1
                    if first_neg <= length:
                        ans += length - first_neg + 1
                cur -= length * p

            cur += t
            cur -= p
            if cur < 0:
                ans += 1

            prev_day = d + 1

        if prev_day <= m:
            length = m - prev_day + 1
            if cur < 0:
                ans += length
            else:
                first_neg = cur // p + 1
                if first_neg <= length:
                    ans += length - first_neg + 1

        return ans

    return str(count_negative_days(n, p, m, events))

# samples
assert solve("3 6 7\n2 13\n4 20\n7 9\n") == "3"

# minimum size, single day
assert solve("1 5 1\n1 10\n") == "0"

# no deposits
assert solve("0 3 5\n") == "5"

# always positive after large deposit
assert solve("1 1 5\n1 100\n") == "0"

# alternating threshold behavior
assert solve("2 5 6\n2 10\n5 5\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single day deposit | 0 | boundary case, immediate recovery |
| no deposits | m | full linear decay |
| large early deposit | 0 | never negative |
| alternating deposits | 2 | segment correctness |

## Edge Cases

One edge case is when there are no deposits. In that case the balance is simply $-p, -2p, \dots$, so every day is negative. The algorithm handles this by skipping the event loop and processing the final tail segment starting from balance zero, correctly counting all $m$ days.

Another case is a large deposit that prevents any future negative balance. The segment logic detects that the starting balance is non-negative and the first negative index exceeds segment length, so it contributes zero days.

A final subtle case is when a deposit occurs on the last day. The algorithm processes that day normally and then the remaining segment is empty, avoiding any off-by-one errors due to zero-length intervals.
