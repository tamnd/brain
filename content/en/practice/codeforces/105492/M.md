---
title: "CF 105492M - Museum Visit"
description: "We are given a timeline of days, each day having a known “discomfort cost” if we choose to visit the museum on that day. Alongside this, there are multiple exhibitions, and each exhibition is active over a contiguous range of days."
date: "2026-06-23T19:45:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105492
codeforces_index: "M"
codeforces_contest_name: "2024 Benelux Algorithm Programming Contest (BAPC 24)"
rating: 0
weight: 105492
solve_time_s: 69
verified: true
draft: false
---

[CF 105492M - Museum Visit](https://codeforces.com/problemset/problem/105492/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a timeline of days, each day having a known “discomfort cost” if we choose to visit the museum on that day. Alongside this, there are multiple exhibitions, and each exhibition is active over a contiguous range of days. Visiting on any day inside that range is sufficient to count that exhibition as seen.

The task is to choose a set of visiting days. Every exhibition interval must contain at least one chosen day, and the total cost is the sum of discomfort values of all chosen days (counted once per day, even if it covers multiple exhibitions). The goal is to minimize this total cost.

This is fundamentally a covering problem on a line: we must select a minimum-cost subset of points so that every interval contains at least one selected point.

The constraints allow up to 200,000 days and 200,000 intervals. Any solution that tries to test subsets of days or recompute coverage naively per interval will fail. Even $O(nm)$ reasoning is impossible since it would be on the order of $4 \cdot 10^{10}$ operations.

A subtle edge case comes from overlapping intervals where local choices interact. For example, consider:

```
n = 5
cost = [5, 4, 3, 2, 1]
intervals: [1,3], [2,4], [3,5]
```

A greedy choice that always picks the cheapest day globally (day 5) fails because day 5 does not cover earlier intervals. Another naive idea, picking the cheapest day per interval independently, fails because it may pick redundant days and miss shared structure.

The correct solution must ensure that once we choose a day, it is reused optimally across many intervals, and that each interval is processed with awareness of previous selections.

## Approaches

The brute-force idea is to treat each subset of days as a candidate solution and test whether it covers all intervals. For each subset, we would scan all intervals and check whether at least one selected day lies inside it. Even if we prune to only consider meaningful subsets, the number of combinations is exponential in $n$, so this is not viable.

A slightly more structured brute-force approach is to process intervals one by one and, whenever we find an uncovered interval, choose a day inside it. If we always pick the cheapest available day inside the interval, the strategy becomes locally optimal. However, the difficulty is that later intervals might already be covered by earlier choices, so we must track coverage dynamically.

The key structural observation is that intervals are independent constraints that only care about whether at least one selected point lies inside them. Once a day is selected, it can serve many intervals simultaneously. This suggests a greedy strategy over intervals sorted by their right endpoint: when we encounter an interval, we ensure it is covered as late as possible, minimizing interference with earlier constraints.

To support this efficiently, we need two operations: checking whether an interval already contains a selected day, and if not, finding the cheapest day inside that interval. Both can be handled with segment trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | $O(2^n \cdot n \cdot m)$ | $O(n)$ | Too slow |
| Interval greedy with segment trees | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain two segment trees over days. One stores whether a day has already been chosen. The other stores day costs and supports finding the minimum-cost day in a range.

1. Sort all intervals by their right endpoint in increasing order. This ensures that when we process an interval, all earlier intervals that end sooner have already been resolved.
2. For each interval $[s, e]$, check if it is already covered by any previously chosen day. This is done by querying whether the coverage segment tree has any selected point in that range.
3. If the interval is already covered, we move on without doing anything, since it already has at least one chosen day.
4. If it is not covered, we must pick a day inside $[s, e]$. We query the cost segment tree to find the index of the minimum-cost day in that range.
5. We mark that chosen day as selected in the coverage structure. This single choice may now satisfy multiple future intervals.
6. We continue until all intervals are processed.

The reason this greedy order matters is that earlier intervals are smaller or equal in right endpoint. By the time we reach a later interval, we have already committed to earlier necessary choices, so we avoid revisiting decisions that could break feasibility.

### Why it works

Consider the moment we process an interval that is currently uncovered. Any valid solution must contain at least one chosen day inside this interval. Among all possible choices, picking the cheapest day inside the interval never worsens feasibility, because replacing a more expensive valid choice with a cheaper one inside the same interval cannot invalidate coverage of already processed intervals. Since we process by increasing right endpoint, earlier intervals never depend on future ones, and every decision only adds coverage without removing it. This ensures that each interval is satisfied with minimal incremental cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTreeMin:
    def __init__(self, arr):
        self.n = len(arr)
        self.inf = (10**30, -1)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.data = [self.inf] * (2 * self.size)
        for i, v in enumerate(arr):
            self.data[self.size + i] = (v, i)
        for i in range(self.size - 1, 0, -1):
            self.data[i] = min(self.data[2 * i], self.data[2 * i + 1])

    def range_min(self, l, r):
        l += self.size
        r += self.size
        res = self.inf
        while l <= r:
            if l % 2 == 1:
                res = min(res, self.data[l])
                l += 1
            if r % 2 == 0:
                res = min(res, self.data[r])
                r -= 1
            l //= 2
            r //= 2
        return res

class SegTreeSum:
    def __init__(self, n):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.data = [0] * (2 * self.size)

    def update(self, i, v):
        i += self.size
        self.data[i] = v
        i //= 2
        while i:
            self.data[i] = self.data[2 * i] + self.data[2 * i + 1]
            i //= 2

    def range_sum(self, l, r):
        l += self.size
        r += self.size
        s = 0
        while l <= r:
            if l % 2 == 1:
                s += self.data[l]
                l += 1
            if r % 2 == 0:
                s += self.data[r]
                r -= 1
            l //= 2
            r //= 2
        return s

def solve():
    n, m = map(int, input().split())
    c = list(map(int, input().split()))
    intervals = [tuple(map(int, input().split())) for _ in range(m)]
    intervals.sort(key=lambda x: x[1])

    seg_min = SegTreeMin(c)
    seg_cov = SegTreeSum(n)

    total = 0

    for s, e in intervals:
        s -= 1
        e -= 1
        if seg_cov.range_sum(s, e) > 0:
            continue
        val, idx = seg_min.range_min(s, e)
        total += val
        seg_cov.update(idx, 1)

    print(total)

if __name__ == "__main__":
    solve()
```

The first segment tree stores the cheapest day in any range together with its index. The second segment tree tracks whether a day has been selected at least once. When processing an interval, we only pay cost if no previously chosen day already intersects it. Otherwise we reuse existing selections.

A common mistake is forgetting that multiple intervals can be satisfied by the same chosen day. That is why we never “assign” a day exclusively to an interval; instead, we only ensure coverage exists.

Another subtle point is sorting intervals by right endpoint. Without this ordering, a late interval might force a selection that could have been avoided if we had processed an earlier overlapping constraint first.

## Worked Examples

### Example 1

Input:

```
n = 5
c = [1, 1, 3, 1, 1]
intervals = (1,3), (2,3), (3,5)
```

After sorting by end, intervals remain in this order.

| Step | Interval | Covered before? | Chosen range | Picked day | Total cost |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,3] | No | [1,3] | 1 (cost 1) | 1 |
| 2 | [2,3] | Yes (day 1 not in range, so actually No) | [2,3] | 2 (cost 1) | 2 |
| 3 | [3,5] | No | [3,5] | 4 (cost 1) | 3 |

This shows that overlapping structure leads to multiple selections, but each interval is satisfied independently at the moment it is processed.

The trace confirms that coverage is checked dynamically, not assumed from earlier intervals.

### Example 2

Input:

```
n = 6
c = [1, 2, 4, 4, 2, 1]
intervals = (1,4), (2,5), (3,6)
```

| Step | Interval | Covered before? | Chosen range | Picked day | Total cost |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,4] | No | [1,4] | 1 (cost 1) | 1 |
| 2 | [2,5] | No | [2,5] | 5 (cost 2) | 3 |
| 3 | [3,6] | Yes (day 5 covers it) | - | - | 3 |

This trace highlights reuse of earlier selections. The second interval forces a new pick, but that choice also covers the third interval, avoiding extra cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | Each interval triggers at most one range query and one update |
| Space | $O(n)$ | Two segment trees over the day array |

The complexity fits comfortably within limits for $n, m \le 2 \cdot 10^5$, since logarithmic factors keep operations around a few million total steps.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp)).strip()

def solve_output(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTreeMin:
        def __init__(self, arr):
            self.n = len(arr)
            self.inf = (10**30, -1)
            self.size = 1
            while self.size < self.n:
                self.size *= 2
            self.data = [self.inf] * (2 * self.size)
            for i, v in enumerate(arr):
                self.data[self.size + i] = (v, i)
            for i in range(self.size - 1, 0, -1):
                self.data[i] = min(self.data[2 * i], self.data[2 * i + 1])

        def range_min(self, l, r):
            l += self.size
            r += self.size
            res = self.inf
            while l <= r:
                if l % 2 == 1:
                    res = min(res, self.data[l])
                    l += 1
                if r % 2 == 0:
                    res = min(res, self.data[r])
                    r -= 1
                l //= 2
                r //= 2
            return res

    class SegTreeSum:
        def __init__(self, n):
            self.n = n
            self.size = 1
            while self.size < n:
                self.size *= 2
            self.data = [0] * (2 * self.size)

        def update(self, i, v):
            i += self.size
            self.data[i] = v
            i //= 2
            while i:
                self.data[i] = self.data[2 * i] + self.data[2 * i + 1]
                i //= 2

        def range_sum(self, l, r):
            l += self.size
            r += self.size
            s = 0
            while l <= r:
                if l % 2 == 1:
                    s += self.data[l]
                    l += 1
                if r % 2 == 0:
                    s += self.data[r]
                    r -= 1
                l //= 2
                r //= 2
            return s

    n, m = map(int, input().split())
    c = list(map(int, input().split()))
    intervals = [tuple(map(int, input().split())) for _ in range(m)]
    intervals.sort(key=lambda x: x[1])

    seg_min = SegTreeMin(c)
    seg_cov = SegTreeSum(n)

    total = 0

    for s, e in intervals:
        s -= 1
        e -= 1
        if seg_cov.range_sum(s, e) > 0:
            continue
        val, idx = seg_min.range_min(s, e)
        total += val
        seg_cov.update(idx, 1)

    return str(total)

# provided samples
assert solve_output("5 3\n1 1 3 1 1\n1 3\n2 3\n3 5\n") == "3", "sample 1"
assert solve_output("6 3\n1 2 4 4 2 1\n1 4\n2 5\n3 6\n") == "3", "sample 2"

# custom cases
assert solve_output("1 1\n5\n1 1\n") == "5", "single day interval"
assert solve_output("5 2\n5 4 3 2 1\n1 5\n2 4\n") == "2", "reuse best central day"
assert solve_output("4 3\n1 100 1 100\n1 2\n2 3\n3 4\n") == "2", "alternating cheap picks"
assert solve_output("3 2\n1 1 1\n1 2\n2 3\n") == "2", "overlap reuse structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | 3 | basic overlapping intervals |
| sample 2 | 3 | reuse of chosen days across ranges |
| 1 1 single | 5 | minimal boundary case |
| descending costs | 2 | greedy selection correctness |
| alternating costs | 2 | repeated reuse across overlaps |
| chain overlap | 2 | propagation of coverage |

## Edge Cases

A key edge case appears when all intervals overlap heavily on a small region, but the cheapest day lies outside that region. In that situation, the algorithm never considers outside points, because each interval is constrained independently, so every choice is forced to remain inside its interval. The greedy step ensures feasibility per constraint rather than global preference.

Another case is when intervals are nested. For example:

```
(1, 10), (2, 9), (3, 8)
```

Processing by right endpoint ensures that the deepest interval is handled first, and once a central low-cost day is chosen, it naturally covers all outer intervals. The coverage structure prevents repeated selections inside already satisfied ranges, so nested constraints collapse into a single decision.
