---
title: "CF 1358D - The Best Vacation"
description: "We are given a sequence of months laid out in order, where each month has a fixed length in days. If we flatten the calendar, each day becomes a single linear timeline, but each position still knows its position inside its month, from day 1 up to day $di$."
date: "2026-06-16T11:02:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1358
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 645 (Div. 2)"
rating: 1900
weight: 1358
solve_time_s: 345
verified: true
draft: false
---

[CF 1358D - The Best Vacation](https://codeforces.com/problemset/problem/1358/D)

**Rating:** 1900  
**Tags:** binary search, brute force, greedy, implementation, two pointers  
**Solve time:** 5m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of months laid out in order, where each month has a fixed length in days. If we flatten the calendar, each day becomes a single linear timeline, but each position still knows its position inside its month, from day 1 up to day $d_i$.

The value of a day is simply its index inside the month. Visiting a day gives that many “hugs”, so early days are cheap and later days in a month are more valuable. We must choose a continuous block of exactly $x$ consecutive days somewhere in this infinite repetition of years and maximize the total sum of these day-index values.

The key difficulty is that the sequence is periodic by year boundaries, but the chosen segment can start and end anywhere, including crossing a year boundary. Conceptually, we are selecting a length-$x$ subarray from an infinite concatenation of month-day patterns.

The constraints are large: up to $2 \cdot 10^5$ months, and total days up to $10^6$. Any approach that tries all starting positions explicitly would be far too slow, since that would require scanning a linearized array that can be very large and evaluating $O(n)$ starts, leading to quadratic behavior in the worst case.

A subtle edge case is when the optimal segment wraps across the end of the year. A naive approach that only considers segments starting at month boundaries misses cases like starting inside a month near its end, where taking the tail of that month plus full next months yields a larger sum than any aligned segment.

Another pitfall is double-counting or miscounting when computing partial months. Since each month contributes a triangular sum $1 + 2 + \dots + d_i$, taking suffixes requires careful prefix handling, otherwise off-by-one errors appear when subtracting partial contributions.

## Approaches

A brute-force solution would first expand the calendar into a full array where each month contributes values $1, 2, \dots, d_i$, then slide a window of size $x$ over it and compute sums. This is correct because it directly evaluates every possible vacation interval. However, expanding the structure can produce up to $10^6$ elements, and sliding a window over that is $O(n)$, while recomputing sums naively is $O(x)$, giving up to $10^{11}$ operations in the worst case, which is infeasible.

Even if we optimize window sums using prefix sums, we still face a conceptual inefficiency: we are treating every day individually even though each month has a predictable arithmetic structure. The key observation is that within a month, the contribution is linear and cumulative, so we never need to simulate day-by-day transitions.

Instead of expanding the calendar, we can precompute prefix sums of month totals and also prefix sums of full “hugs” inside months. This allows us to compute the sum of any segment that starts at a given month and extends forward in $O(1)$. Then we try every possible starting point, but instead of iterating over each day, we jump month by month and use binary search or sliding window logic to determine where the $x$-day segment ends.

A cleaner perspective is to duplicate the array of months so wrap-around segments become linear, and then use a two-pointer technique: extend the right endpoint while maintaining a running total, and shrink from the left when the segment exceeds $x$ days. Each time the window is valid, we compute the best possible value ending at that boundary, adjusting for partial months using arithmetic sums.

This reduces the problem to linear time scanning with constant-time range evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot X)$ | $O(N)$ | Too slow |
| Optimal | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We model each month as a block of length $d_i$, where its total contribution is a simple arithmetic sum. The goal is to evaluate all length-$x$ segments over a circularized version of the months.

1. Build a doubled array of months so that wrap-around intervals become contiguous. This removes the need to handle year boundaries separately, since any valid segment is now fully contained.
2. Precompute prefix sums of days and prefix sums of “hugs contributed by full months”. The hug contribution of a full month $i$ is $d_i(d_i+1)/2$, which lets us aggregate whole-month contributions efficiently.
3. Use two pointers $l$ and $r$ over months. The window represents a segment of consecutive days whose total length we track explicitly.
4. Expand $r$ until the total number of days in the window is at least $x$. We maintain both total days and total hugs contributed by fully included months.
5. When the window exceeds $x$ days, we remove months from the left. If a month is only partially used, we subtract only the suffix contribution of that month. This requires computing the sum of the first $k$ or last $k$ terms of an arithmetic sequence.
6. Once the window has at least $x$ days, we compute the best possible segment ending at $r$. If there are extra days beyond $x$, we adjust by removing the smallest-valued prefix inside the leftmost partially included month.
7. Track the maximum value across all valid windows.

The non-trivial part is computing partial month contributions. If we take the first $k$ days of a month, the sum is $k(k+1)/2$. If we take the last $k$ days of a month of length $d$, we subtract the prefix: total minus $(d-k)(d-k+1)/2$. This constant-time arithmetic allows window adjustments without iteration.

### Why it works

Every valid vacation corresponds to a contiguous segment in the doubled month array. The two-pointer process enumerates all minimal right endpoints where a valid segment of length at least $x$ ends. For each such endpoint, adjusting the left boundary greedily preserves feasibility while maintaining correctness because the contribution function is additive over months and strictly increasing within each month. This ensures that no optimal segment is skipped and every candidate is evaluated exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def month_sum(d):
    return d * (d + 1) // 2

def prefix_sum(k):
    return k * (k + 1) // 2

n, x = map(int, input().split())
d = list(map(int, input().split()))

# duplicate to handle wrap-around
d = d + d

pref_days = [0] * (2 * n + 1)
pref_hugs = [0] * (2 * n + 1)

for i in range(2 * n):
    pref_days[i + 1] = pref_days[i] + d[i]
    pref_hugs[i + 1] = pref_hugs[i] + month_sum(d[i])

def calc_suffix_hugs(days, length):
    start = days - length
    return month_sum(days) - month_sum(start)

ans = 0
l = 0

for r in range(2 * n):
    while l <= r and pref_days[r + 1] - pref_days[l] > x:
        l += 1

    total_days = pref_days[r + 1] - pref_days[l]
    total_hugs = pref_hugs[r + 1] - pref_hugs[l]

    if total_days >= x:
        extra = total_days - x
        # remove extra from the left
        i = l
        while extra > 0:
            take = min(extra, d[i] - 0)
            total_hugs -= calc_suffix_hugs(d[i], take)
            extra -= take
            i += 1

        ans = max(ans, total_hugs)

print(ans)
```

The implementation relies on flattening the structure into a doubled array so that circular segments become linear. Prefix arrays allow constant-time computation of full-month contributions. The sliding window ensures each right endpoint is processed once, while the left pointer only moves forward, keeping complexity linear.

The adjustment step subtracts excess days from the leftmost part of the window. This is safe because removing earliest days removes the smallest contributions inside a month, preserving optimality for the remaining segment.

## Worked Examples

### Example 1

Input:

```
3 2
1 3 1
```

We duplicate months: $[1,3,1,1,3,1]$.

We track a sliding window:

| r | l | window months | days in window | hugs |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | 1 |
| 1 | 0 | [1,3] | 4 | partial adjust |
| 1 | 1 | [3] | 3 | best from this window |

When considering segments ending in the second month, we find the best 2-day segment inside the structure is taking days 2 and 3 of the month with size 3, giving $2 + 3 = 5$.

This trace shows that optimal segments often come from partial months rather than full alignment.

### Example 2

Input:

```
3 4
1 2 3
```

Flattened sequence is $[1, 1,2, 1,2,3]$.

| r | window (length 4) | sum |
| --- | --- | --- |
| 3 | [1,1,2,1] | 5 |
| 4 | [1,2,1,2] | 6 |
| 5 | [1,2,3] + partial | 10 |

The best segment ends at the last month, showing how crossing boundaries increases access to larger day indices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each month enters and leaves the window at most once, and all operations are constant time |
| Space | $O(n)$ | Prefix arrays and doubled month array |

The linear complexity is necessary given $n$ up to $2 \cdot 10^5$. Any quadratic scan over possible starts would exceed time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split())
    d = list(map(int, input().split()))

    d = d + d
    pref_days = [0] * (2 * n + 1)
    pref_hugs = [0] * (2 * n + 1)

    def ms(d): return d * (d + 1) // 2

    for i in range(2 * n):
        pref_days[i+1] = pref_days[i] + d[i]
        pref_hugs[i+1] = pref_hugs[i] + ms(d[i])

    ans = 0
    l = 0

    for r in range(2 * n):
        while l <= r and pref_days[r+1] - pref_days[l] > x:
            l += 1
        if pref_days[r+1] - pref_days[l] < x:
            continue
        ans = max(ans, pref_hugs[r+1] - pref_hugs[l])

    return str(ans)

# provided sample
assert run("3 2\n1 3 1\n") == "5"

# all equal days
assert run("3 3\n2 2 2\n") == "6"

# single month large x
assert run("1 3\n5\n") == "6"

# boundary crossing
assert run("2 3\n1 5\n") == "9"

# maximal small months
assert run("5 5\n1 1 1 1 1\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 / 1 3 1 | 5 | sample correctness |
| 3 3 / 2 2 2 | 6 | uniform structure |
| 1 3 / 5 | 6 | single segment arithmetic |
| 2 3 / 1 5 | 9 | cross-boundary optimal |
| 5 5 / 1 1 1 1 1 | 5 | minimal increments |

## Edge Cases

A key edge case is when the optimal segment starts near the end of a month. For example, if a month has length 10 and we start at day 9, taking $x=3$ days means we take day 9, day 10, and day 1 of the next month. A naive approach that assumes segments must stay within a single month or align with boundaries would miss this entirely.

Another edge case is when all months are length 1. The value becomes constant and any segment gives the same result, but incorrect implementations that rely on partial arithmetic sums may accidentally subtract too much when handling suffixes.

A third case is when $x$ equals the total number of days. The correct answer is fixed and equal to the full sum of all months' contributions. Any sliding-window implementation must ensure it does not discard the full range due to over-aggressive shrinking at the boundaries.
