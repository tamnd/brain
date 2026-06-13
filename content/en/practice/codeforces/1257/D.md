---
title: "CF 1257D - Yet Another Monster Killing Problem"
description: "We are given a sequence of monsters that must be defeated strictly from left to right. Each monster has a required strength threshold, and none can be skipped or reordered. We also have a pool of heroes."
date: "2026-06-13T22:41:23+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1257
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 76 (Rated for Div. 2)"
rating: 1700
weight: 1257
solve_time_s: 215
verified: true
draft: false
---

[CF 1257D - Yet Another Monster Killing Problem](https://codeforces.com/problemset/problem/1257/D)

**Rating:** 1700  
**Tags:** binary search, data structures, dp, greedy, sortings, two pointers  
**Solve time:** 3m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of monsters that must be defeated strictly from left to right. Each monster has a required strength threshold, and none can be skipped or reordered. We also have a pool of heroes. Each hero has a fighting power, which determines whether they can survive a monster encounter, and an endurance, which caps how many monsters they can defeat in a single day.

The process unfolds in days. On each day we pick exactly one hero. That hero starts fighting from the first undefeated monster. If at any point a monster has strictly greater power than the hero, the hero immediately fails and the day ends without progress beyond that monster. Otherwise, the hero can defeat monsters one by one until either their endurance is exhausted or there are no monsters left.

The task is to minimize the number of days needed to defeat the entire sequence, or determine that it is impossible.

The constraints force us away from naive simulation. With up to 2×10^5 monsters and heroes per test, and up to 10^5 tests, any solution that restarts scanning monsters per day or tries all hero choices greedily per position will exceed time limits. We need an approach closer to O((n + m) log n) or O((n + m) log m).

A subtle difficulty comes from the interaction between endurance and power. A hero who can defeat a large segment might still be useless if a single strong monster blocks them early. Conversely, a weaker hero with high endurance may be better if assigned at the right prefix.

Edge cases that break naive greedy ideas include situations like a very strong monster appearing late, for example monsters `[1, 1, 1, 100, 1]`. A greedy strategy that always uses the strongest available hero might waste them early, but a slightly weaker hero with sufficient endurance might be optimal for early segments.

Another failure case appears when no hero can pass a single monster. For instance, if a monster has power 10 but all heroes have power 9 or less, the answer is immediately impossible regardless of endurance.

Finally, a misleading case occurs when endurance is large but power is small. Such heroes look strong for long segments but are actually useless if they cannot pass early high peaks.

## Approaches

The brute-force idea is straightforward. For each day, try every hero and simulate how far they can go from the current monster position. Choose the hero that defeats the most monsters. This is correct because it always locally maximizes progress. However, each simulation may scan up to n monsters, and there are up to n steps in total, leading to O(n²) per test in the worst case, which is far too slow.

To improve, we need to avoid repeatedly simulating prefixes. The key observation is that what matters for any prefix of monsters is not the exact sequence of heroes used so far, but only the best possible endurance among heroes that can survive up to a certain strength threshold.

If we fix a prefix ending at position i, then any valid day that covers a segment ending at i must use a hero whose power is at least the maximum monster in that segment, and whose endurance is at least the segment length. This suggests compressing heroes into a structure where for each power threshold we know the best achievable endurance.

We sort heroes by power, then preprocess a prefix maximum over endurance. This lets us answer queries of the form: among all heroes with power ≥ x, what is the maximum endurance available.

Now we simulate greedily over monsters, but instead of trying heroes directly, we continuously extend the current segment while maintaining the maximum monster value seen so far. When we try to extend the segment, we query whether there exists a hero who can handle both the current maximum monster and the segment length. If yes, we extend; otherwise, we finalize the current day and restart.

To make this efficient, we precompute and use a pointer moving over sorted heroes while maintaining best endurance for all eligible power levels. Each extension becomes amortized constant or logarithmic depending on implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(1) | Too slow |
| Sorting + greedy + preprocessing | O(n log n + m log m) | O(m) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Sort monsters are already given in order, so we keep a pointer over them.
2. Sort heroes by power in increasing order. While doing so, we maintain a structure that can tell us, for any minimum required power, the maximum endurance available among heroes meeting that requirement. This is built by scanning heroes from lowest power to highest and maintaining a suffix maximum of endurance.
3. We define a function that, given a required minimum power and required segment length, checks whether any hero can handle both. This is answered by binary searching the first hero with sufficient power, then checking the precomputed maximum endurance from that index onward.
4. We start from the first monster and attempt to build the longest possible segment for one day. We track the maximum monster power in the current segment and its length.
5. At each step, we try to extend the segment by one monster. After extension, we check whether some hero can handle it. If yes, we continue expanding.
6. If no hero can handle the current segment, we finalize the previous segment as one day, and restart from the current monster. We increment the day counter.
7. If at any point a single monster cannot be handled by any hero, we immediately return -1.

The key invariant is that at any moment, we are maintaining the longest prefix starting from the current position that can be cleared in a single day by some valid hero. Every time we fail to extend, it is because no hero exists that satisfies both constraints for the extended segment, which means the previous segment is maximal and must correspond to an optimal day boundary.

This greedy segmentation is safe because any valid solution must also partition the array into contiguous segments, and delaying a cut when impossible to extend does not improve future feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())

    heroes = []
    for _ in range(m):
        p, s = map(int, input().split())
        heroes.append((p, s))

    heroes.sort()

    best = [0] * m
    best[-1] = heroes[-1][1]
    for i in range(m - 2, -1, -1):
        best[i] = max(best[i + 1], heroes[i][1])

    def can(power_req, len_req):
        # find first hero with power >= power_req
        l, r = 0, m
        while l < r:
            mid = (l + r) // 2
            if heroes[mid][0] >= power_req:
                r = mid
            else:
                l = mid + 1
        if l == m:
            return False
        return best[l] >= len_req

    i = 0
    days = 0

    while i < n:
        days += 1
        seg_max = 0
        seg_len = 0

        j = i
        while j < n:
            seg_max = max(seg_max, a[j])
            seg_len += 1

            if not can(seg_max, seg_len):
                break
            j += 1

        if i == j:
            print(-1)
            return

        i = j

    print(days)

t = int(input())
for _ in range(t):
    solve()
```

The code first sorts heroes by power, then builds a suffix maximum array over endurance so that feasibility queries become fast. The `can` function checks whether any hero can handle a segment with given maximum monster power and length by binary searching the first eligible hero and then checking the best endurance available from that point onward.

The main loop greedily builds each day’s segment. If even a single monster cannot be started, the answer is impossible. Otherwise, each segment is extended as far as possible under feasibility constraints.

A subtle implementation detail is that we always recompute segment maximum incrementally. This avoids rescanning previous monsters. Another subtlety is the suffix maximum array: without it, checking endurance would require linear scanning and would break performance.

## Worked Examples

### Example 1

Input:

```
6
2 3 11 14 1 8
2
3 2
100 1
```

We sort heroes: `(3,2), (100,1)` and build suffix max endurance `[2,1]`.

We start day 1 from monster 2.

| Step | Segment Max | Segment Length | Can? | Action |
| --- | --- | --- | --- | --- |
| start | 2 | 1 | yes | extend |
| 3 | 3 | 2 | yes | extend |
| 11 | 11 | 3 | no | cut |

Day 1 ends at first 2 monsters.

Day 2 starts at 11.

| Step | Segment Max | Segment Length | Can? | Action |
| --- | --- | --- | --- | --- |
| 11 | 11 | 1 | yes | extend |
| 14 | 14 | 2 | no | cut |

Day 2 ends at 11.

Continuing similarly yields total days = 5.

This shows that segmentation depends heavily on when a hero’s endurance becomes the limiting factor rather than just power.

### Example 2

Input:

```
5
3 5 100 2 3
2
30 5
90 1
```

Hero preprocessing gives `(30,5), (90,1)`.

We start:

| Step | Segment Max | Length | Can? | Action |
| --- | --- | --- | --- | --- |
| 3 | 3 | 1 | yes | extend |
| 5 | 5 | 2 | yes | extend |
| 100 | 100 | 3 | no | cut |

Then at monster 100:

| Step | Segment Max | Length | Can? | Action |
| --- | --- | --- | --- | --- |
| 100 | 100 | 1 | no | impossible |

Since no hero can handle 100, the process stops and answer is -1.

This confirms the correctness of the feasibility check: a single unreachable monster makes the entire test impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m + m log m) | sorting heroes plus binary search per extension step |
| Space | O(m) | suffix maximum array over heroes |

The complexity fits within constraints because total n and m over all test cases is bounded by 2×10^5, making the overall work roughly O(N log N), well within 2 seconds in Python with efficient I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    return stdout.getvalue()

# NOTE: placeholder; actual function integration needed in real setup

# provided samples
# assert run(...) == ...

# edge: single monster, single strong hero
# edge: impossible case
# edge: many small segments
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single monster + strong hero | 1 | base feasibility |
| monster too strong | -1 | impossibility detection |
| alternating small segments | small number | greedy segmentation correctness |

## Edge Cases

A critical edge case is when the strongest monster appears early. The algorithm handles it by failing the segment extension immediately and forcing a cut before that monster, ensuring no invalid hero assignment continues.

Another edge case is when heroes exist with high endurance but insufficient power. The preprocessing ensures they are never incorrectly considered for high-power segments, because the binary search enforces the power constraint before endurance is checked.

A final edge case is a single hero with both high power and large endurance. In that case, the algorithm will extend the entire array in one segment, since feasibility remains true at every prefix, and the segment is never cut prematurely.
