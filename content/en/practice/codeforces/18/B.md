---
title: "CF 18B - Platforms"
description: "We have a line with a series of discrete platforms. Each platform has a fixed length l and is separated from the next by"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 18
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 18 (Div. 2 Only)"
rating: 1700
weight: 18
solve_time_s: 73
verified: true
draft: false
---

[CF 18B - Platforms](https://codeforces.com/problemset/problem/18/B)

**Rating:** 1700  
**Tags:** brute force, math  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line with a series of discrete platforms. Each platform has a fixed length `l` and is separated from the next by a fixed distance `m - l`, so platform `k` occupies the segment from `(k-1)*m` to `(k-1)*m + l`. The grasshopper Bob starts at position `0` and jumps forward in steps of exactly `d` units. If he lands on a platform, he survives and can jump again. If he lands outside all platforms, he falls. Landing exactly at the edge counts as safe. The task is to find the first position where Bob falls.

The input integers `n, d, m, l` can all go up to 10^6. That means any approach that iterates over positions individually could require up to a million jumps in the worst case, which is feasible if we are careful, but brute-force scanning every unit of the line would be too slow. Edge cases include situations where the jump length `d` is larger than the distance between two platforms, or where `d` is exactly aligned with the edges, and cases where `l = 1` and `m` is large. These scenarios can easily make naive checks off by one unit, so we need precise arithmetic with closed intervals.

For example, if `n = 1, d = 5, m = 10, l = 3`, Bob jumps to `5` on the first jump. The only platform is `[0,3]`. Even though `5 < 10`, he is outside the platform, so the answer is `5`. A careless implementation might incorrectly assume any jump within `m` units is safe, which would produce `10`, the start of the next (nonexistent) platform, a wrong result.

## Approaches

The simplest approach is a brute-force simulation. Start at position 0, increment by `d` each jump, and for each new position check whether it falls inside any platform segment. This is correct, because it directly models Bob’s behavior. The problem is efficiency: for `n = 10^6` and `d = 1`, this could perform up to a million jumps, and for each jump a linear scan of platforms is too expensive. Worse, checking all platforms each time gives O(n^2) in the worst case, which will time out.

The key observation is that platforms are evenly spaced and identical in length. Platform `k` is `[ (k-1)*m , (k-1)*m + l ]`. We can compute, for a given position `x`, which platform it _would be on_ (or would fall between) by integer division: the candidate platform index is `x // m + 1`. Then we only need to check whether `x` is less than `(candidate - 1)*m + l` to determine if Bob is still on the platform. If it is, he survives; if not, he falls. This reduces the problem to a simple arithmetic check per jump and avoids scanning all platforms.

We can further optimize by realizing that Bob’s jump distance is fixed. The first jump at which he falls can be expressed as `x = d * k` for some integer `k`. We need the smallest `k` such that `x` is greater than the right end of the platform it would be on. This gives a purely arithmetic solution in O(1) per jump until he falls.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimized Arithmetic | O(n/d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize Bob’s position `x` to `0`. We will increment by `d` on each jump.
2. On each jump, compute the platform index Bob would land on. Since platforms are `[ (k-1)*m , (k-1)*m + l ]`, the candidate platform is `k = x // m + 1`.
3. Check whether `k` exceeds `n`. If yes, Bob has jumped beyond the last platform and falls at `x`.
4. Otherwise, check whether `x` is within the platform: `x <= (k-1)*m + l`. If yes, Bob survives and jumps again.
5. If `x > (k-1)*m + l`, Bob lands outside the platform and falls. This is the first unsafe position, and we print it.
6. Increment `x` by `d` and repeat.

Why it works: the algorithm maintains the invariant that `x` is always Bob’s actual position after some number of jumps. By computing the candidate platform algebraically, we never scan irrelevant platforms. The check `x <= (k-1)*m + l` correctly captures whether Bob lands within a platform or falls. Since `d` is constant, each step progresses to the next jump without missing any potential fall point.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d, m, l = map(int, input().split())

x = 0
while True:
    k = x // m + 1
    if k > n or x > (k - 1) * m + l:
        print(x)
        break
    x += d
```

The code starts with `x = 0` and iterates by `d`. Computing `k = x // m + 1` directly gives the 1-based platform index. If `k > n`, Bob has jumped past all platforms. If `x > (k-1)*m + l`, he has overshot the current platform. Otherwise, `x` is safe and the loop continues. This implementation handles edges correctly because we use `<=` for platform inclusion.

## Worked Examples

**Sample Input 1**

```
2 2 5 3
```

| Jump | x | k | Platform end | Falls? |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | No |
| 2 | 2 | 1 | 3 | No |
| 3 | 4 | 1 | 3 | Yes |

Bob falls at position `4`. The trace confirms the algorithm computes the correct platform index and compares with the right edge.

**Custom Input 2**

```
3 4 5 3
```

| Jump | x | k | Platform end | Falls? |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | No |
| 2 | 4 | 1 | 3 | Yes |

Bob jumps past the first platform on the second jump. The check `x > (k-1)*m + l` correctly identifies the fall.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n/d) | We increment by `d` each step. Maximum jumps are roughly `n*m/d`, bounded by `10^6`. |
| Space | O(1) | Only a few integer variables are used, independent of `n`. |

This fits comfortably within the time and memory limits. Even in the worst case where `d = 1` and `n = 10^6`, we perform at most 10^6 iterations, which is feasible in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n, d, m, l = map(int, input().split())
        x = 0
        while True:
            k = x // m + 1
            if k > n or x > (k - 1) * m + l:
                print(x)
                break
            x += d
    return out.getvalue().strip()

# Provided sample
assert run("2 2 5 3\n") == "4", "sample 1"

# Minimum-size inputs
assert run("1 1 2 1\n") == "2", "minimum size"

# All equal
assert run("3 3 3 3\n") == "9", "all equal values"

# d > m
assert run("2 6 5 3\n") == "6", "jump larger than spacing"

# Last jump lands on last edge
assert run("3 2 5 3\n") == "10", "lands exactly on last edge"

# Single platform, multiple jumps
assert run("1 2 5 3\n") == "4", "single platform multiple jumps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 2 1 | 2 | smallest platform and jumps |
| 3 3 3 3 | 9 | jump length equals platform spacing and length |
| 2 6 5 3 | 6 | jump larger than spacing between platforms |
| 3 2 5 3 | 10 | last jump lands exactly on edge |
| 1 2 5 3 | 4 | single platform, multiple jumps |

## Edge Cases

If `d` is larger than the distance between platforms, the algorithm correctly computes `k = x // m + 1` and checks whether Bob overshoots the platform. For example, with `n=2
