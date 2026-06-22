---
title: "CF 105575E - \u5b89\u6392\u65f6\u95f4"
description: "We are given a schedule planning problem. There are several people, and each person provides one or more time intervals during which they are available. The goal is to determine a single moment in time when the maximum number of people are simultaneously available."
date: "2026-06-22T20:39:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "E"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 48
verified: true
draft: false
---

[CF 105575E - \u5b89\u6392\u65f6\u95f4](https://codeforces.com/problemset/problem/105575/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a schedule planning problem. There are several people, and each person provides one or more time intervals during which they are available. The goal is to determine a single moment in time when the maximum number of people are simultaneously available. After finding that best moment, we also report how many people are not available at that moment.

More concretely, time is discretized into integer positions from 1 to m. Each person contributes several closed intervals, and every interval indicates that the person is available for all time points inside it. A person is considered available at a time point if at least one of their intervals covers it, but in this problem formulation each interval is directly treated as contributing availability over its range, so we effectively count how many interval-coverages overlap at each time.

The output requires two things: the time point where the number of available people is maximized, and the number of people who are not available at that time.

The constraints imply that n can be large and each person may have multiple intervals, so a naive approach that checks every time point against every interval quickly becomes too slow. If we assume up to 10^5 time points and many intervals, a direct simulation leads to roughly O(n · m) behavior in the worst case, which is not feasible within typical limits.

A more subtle issue appears with boundary handling. Intervals are inclusive, so if an interval ends at r, we must ensure it contributes to time r but not to r + 1. A naive prefix implementation that forgets this off-by-one detail will incorrectly shift counts forward.

A simple edge case shows this clearly. Suppose m = 5 and a single interval is [2, 3]. At time 3, the person should still be counted. If we mistakenly decrement at position 3 instead of 4, we would lose coverage at time 3 and undercount.

## Approaches

The brute-force idea is straightforward: for every time point from 1 to m, check every interval from every person and count how many intervals include that time. This is correct because it directly simulates the definition of availability. However, if there are up to n people and each has p intervals, and m time points, this becomes O(m · total_intervals), which can degrade to about 10^10 operations in worst cases.

The key observation is that we do not actually need to recompute coverage independently for every time point. Each interval contributes a continuous block of +1 coverage. Instead of applying this contribution repeatedly over every time inside the interval, we can encode its effect using a difference array: increment at l and decrement at r + 1. After processing all intervals, a prefix sum reconstructs the number of active intervals at each time.

This transforms the problem from repeatedly adding ranges into a single linear sweep. Once we have the coverage at every time point, we can scan once to find the maximum position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m · total intervals) | O(1) | Too slow |
| Difference Array + Prefix Sum | O(m + total intervals) | O(m) | Accepted |

## Algorithm Walkthrough

We use a difference array over the time axis.

1. Create an array `diff` of size m + 2 initialized to zero. This array will store how interval contributions start and stop. We use m + 2 to safely handle the r + 1 index without bounds issues.
2. For every person, read their intervals. For each interval [l, r], increment `diff[l]` by 1 and decrement `diff[r + 1]` by 1. This encodes that the interval contributes +1 starting at l and stops contributing after r.
3. After processing all intervals, compute the prefix sum over `diff` to obtain `cnt[i]`, the number of intervals covering time i. Each position accumulates all active interval contributions that include it.
4. Traverse all time points from 1 to m and track the index where `cnt[i]` is maximized. This represents the time when the largest number of intervals overlap.
5. Output the best time and the number of people not available at that time, computed as n minus the maximum coverage value.

### Why it works

Each interval [l, r] can be viewed as adding +1 to every position in a contiguous segment. The difference array encodes this segment update exactly once per interval, and the prefix sum reconstructs the exact accumulated value at each point. Because addition is linear and independent across intervals, the final prefix sum is equivalent to applying all interval contributions explicitly. The maximum over reconstructed values is therefore the true global maximum overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    diff = [0] * (m + 2)

    for _ in range(n):
        p = int(input())
        for _ in range(p):
            l, r = map(int, input().split())
            diff[l] += 1
            if r + 1 <= m:
                diff[r + 1] -= 1

    best_time = 1
    best_val = -1
    cur = 0

    for i in range(1, m + 1):
        cur += diff[i]
        if cur > best_val:
            best_val = cur
            best_time = i

    print(best_time, n - best_val)

if __name__ == "__main__":
    solve()
```

The code directly mirrors the difference array idea. The `diff` array records only boundary effects of intervals. The variable `cur` maintains the running prefix sum, which is the actual number of active intervals at each time. The comparison step updates the best time whenever a higher overlap is found. The final subtraction `n - best_val` converts maximum participation into the number of absent people.

A subtle implementation detail is the condition `if r + 1 <= m`. Since we only care about time up to m, any decrement beyond that range is irrelevant, but keeping the array safe avoids accidental out-of-bounds writes.

## Worked Examples

### Example 1

Input:

```
3 5
1
1 2
1
2 4
1
3 5
```

We process differences:

| Interval | diff changes |
| --- | --- |
| [1,2] | +1 at 1, -1 at 3 |
| [2,4] | +1 at 2, -1 at 5 |
| [3,5] | +1 at 3, -1 at 6 |

Prefix accumulation:

| i | diff[i] | cur |
| --- | --- | --- |
| 1 | +1 | 1 |
| 2 | +1 | 2 |
| 3 | 0 | 2 |
| 4 | 0 | 2 |
| 5 | -1 | 1 |

Maximum is 2 at times 2-4, earliest is 2.

Output:

```
2 1
```

This shows that overlapping intervals are correctly accumulated even when they come from different people.

### Example 2

Input:

```
2 4
2
1 2
3 4
1
2 3
```

| Interval | diff changes |
| --- | --- |
| [1,2] | +1 at 1, -1 at 3 |
| [3,4] | +1 at 3, -1 at 5 |
| [2,3] | +1 at 2, -1 at 4 |

Prefix:

| i | cur |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |

Maximum is 2 at times 2 and 3, so we pick 2.

Output:

```
2 0
```

This demonstrates correct handling of overlapping boundaries where multiple intervals intersect exactly at endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + total intervals) | Each interval is processed once, and a single linear scan over time is performed |
| Space | O(m) | Difference array and prefix accumulation over the time range |

The algorithm fits comfortably within constraints because both the number of intervals and the time range are processed in linear time, avoiding any nested iteration between them.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    diff = [0] * (m + 2)

    for _ in range(n):
        p = int(input())
        for _ in range(p):
            l, r = map(int, input().split())
            diff[l] += 1
            diff[r + 1] -= 1

    best_time = 1
    best_val = -1
    cur = 0

    for i in range(1, m + 1):
        cur += diff[i]
        if cur > best_val:
            best_val = cur
            best_time = i

    return f"{best_time} {n - best_val}\n"

# provided sample-like case
assert run("3 5\n1\n1 2\n1\n2 4\n1\n3 5\n") == "2 1\n"

# minimum size
assert run("1 1\n1\n1 1\n") == "1 0\n"

# non-overlapping intervals
assert run("2 5\n1\n1 1\n1\n5 5\n") == "1 1\n"

# full overlap
assert run("3 3\n1\n1 3\n1\n1 3\n1\n1 3\n") == "1 0\n"

# boundary test
assert run("2 4\n1\n1 2\n1\n2 3\n") == "2 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single interval | 1 0 | smallest boundary case |
| disjoint intervals | 1 1 | correctness when no overlap |
| full overlap | 1 0 | maximum stacking behavior |
| boundary touching intervals | 2 0 | correct handling of r+1 transitions |

## Edge Cases

One important edge case is when all intervals end exactly at m. In that case, the decrement at r + 1 must not affect valid indices. The code safely ignores r + 1 when it exceeds m, so the final prefix still reflects full coverage until the end.

Another case is when intervals only touch at endpoints. For example [1,2] and [2,3] must both contribute at time 2. The difference array correctly keeps both active at i = 2 because the decrement for the first interval happens at 3, not 2. This preserves overlap at the boundary exactly as required.

A final edge case is when every interval is disjoint. The algorithm will still compute correct counts because each segment contributes independently and never interferes with others, and the maximum naturally becomes 1 at any covered point.
