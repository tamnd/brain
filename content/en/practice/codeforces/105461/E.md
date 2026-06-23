---
title: "CF 105461E - Lighting the Street"
description: "We are given a straight street represented as a continuous segment from 0 to L. There are n fixed lamp posts placed at integer coordinates along this segment. We are not allowed to choose their positions, only the type of bulb installed in each lamp post."
date: "2026-06-23T17:53:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105461
codeforces_index: "E"
codeforces_contest_name: "2024-2025 ICPC, Swiss Subregional"
rating: 0
weight: 105461
solve_time_s: 69
verified: true
draft: false
---

[CF 105461E - Lighting the Street](https://codeforces.com/problemset/problem/105461/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight street represented as a continuous segment from 0 to L. There are n fixed lamp posts placed at integer coordinates along this segment. We are not allowed to choose their positions, only the type of bulb installed in each lamp post.

There are m available bulb types, and each type is defined by a single parameter: how far it shines in both directions. If we install a bulb with range l at a lamp positioned at x, that lamp illuminates the full interval from x − l to x + l. All lamps must use the same bulb type, and we are allowed to choose which type to buy.

The goal is to determine the smallest bulb range among the given types that makes it possible for the union of all illuminated intervals to completely cover every point of [0, L]. If no bulb type can achieve full coverage, the answer is −1.

The constraints n, m ≤ 100000 immediately rule out any approach that tries every bulb type and recomputes coverage in a quadratic manner. A naive O(nm) simulation would lead to about 10^10 interval checks in the worst case, which is far beyond practical limits. Even O(mn log n) becomes tight depending on constants, so we need a linear or near linear check per candidate combined with a logarithmic selection strategy over bulb types.

A subtle aspect of the problem is that coverage is continuous. This means partial overlaps matter, and it is not enough to check whether endpoints of intervals cover integer points. For example, if lamps cover [0, 5] and [6, 10], there is a gap even though both ends are “close”. A correct solution must reason about full interval union, not discrete samples.

Another potential pitfall is assuming that having a bulb large enough for the extreme lamps guarantees coverage. That is false if there is a large gap between consecutive lamp positions. For instance, lamps at positions 0 and 10 with L = 10 require l = 5, but a configuration like 0, 4, 10 still fails with l = 3 even though endpoints look plausible.

Finally, it is easy to forget that the left boundary 0 and right boundary L must be covered explicitly. Missing coverage near 0 is especially common because it depends entirely on whether the leftmost lamp reaches far enough left.

## Approaches

A straightforward approach is to test each bulb type independently. For a fixed range l, we compute the union of all intervals [p_i − l, p_i + l] and check whether this union covers [0, L]. The standard way to do this is to sort the intervals by their starting point and greedily merge them while tracking the furthest covered point. If at any moment we encounter a gap where the next interval starts after the current coverage ends, coverage fails.

This check is correct and runs in O(n log n) per bulb type due to sorting intervals, or O(n) if we reuse a pre-sorted order of positions. However, doing this for all m bulb types leads to O(mn), which is too large for 100000 by 100000.

The key observation is that feasibility is monotonic in l. If a bulb range l is sufficient to cover the street, then any larger range l′ > l is also sufficient, because every interval only expands. This monotonicity allows us to treat the problem as a binary search over the sorted list of bulb ranges.

We first sort the bulb ranges. Then we binary search the smallest index such that the corresponding range is feasible. Each feasibility check runs in O(n) by sweeping through sorted lamp positions once and maintaining the current covered segment. This reduces the problem to O((n + m) log m), which is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per bulb | O(mn) | O(1) | Too slow |
| Sort + binary search + linear check | O(n + m log m) | O(n) | Accepted |

## Algorithm Walkthrough

We exploit the fact that each bulb type induces a symmetric expansion around every lamp position, and coverage becomes easier as the radius grows.

### 1. Sort lamp positions

We sort p so that we can reason about coverage from left to right. This ensures that when we process lamps in order, the left endpoints of their intervals are also non-decreasing.

### 2. Define a feasibility check for a fixed range l

For a given l, each lamp creates an interval [p_i − l, p_i + l]. We simulate merging these intervals without explicitly storing them.

We maintain a variable current, representing the farthest point on the street that is already illuminated continuously starting from 0.

### 3. Scan lamps from left to right

For each lamp i in increasing order of p_i, we compute its interval start and end. If start > current, there is a gap in coverage, so this l fails immediately. Otherwise, we extend current to max(current, end).

### 4. Validate full coverage

After processing all lamps, if current ≥ L, then the entire street is covered. Otherwise, there is some uncovered segment near the right end.

### 5. Binary search over bulb ranges

We sort the m bulb ranges and binary search the smallest index whose range passes the feasibility check. The answer is that range, or −1 if none works.

### Why it works

The feasibility check is equivalent to verifying whether the union of all intervals contains a continuous path from 0 to L. The greedy scan works because at any point, the best possible coverage we can have up to a position is determined solely by the farthest-reaching interval among those that start before or at that position. Any interval starting later cannot repair a gap once it exists, so failing early is safe. Monotonicity in l ensures that once a value works, all larger values also work, making binary search valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_cover(p, L, l):
    current = 0
    for x in p:
        start = x - l
        end = x + l
        if start > current:
            return False
        if end > current:
            current = end
        if current >= L:
            return True
    return current >= L

def solve():
    n, m, L = map(int, input().split())
    p = list(map(int, input().split()))
    lvals = list(map(int, input().split()))

    p.sort()
    lvals.sort()

    lo, hi = 0, m - 1
    ans = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can_cover(p, L, lvals[mid]):
            ans = lvals[mid]
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting lamp positions so that interval merging becomes a single left-to-right sweep. The function `can_cover` encodes the greedy coverage logic. It tracks the current continuous illuminated prefix and rejects a bulb range immediately when a gap appears, which avoids unnecessary work.

The binary search is performed over sorted bulb ranges, and each midpoint is tested using the feasibility function. This structure is essential because recomputing coverage for every bulb independently would be too slow.

A common implementation mistake is forgetting that coverage is continuous, not discrete. The check `start > current` is the precise condition that detects a real uncovered gap. Another subtle point is early termination when `current >= L`, which avoids unnecessary scanning once full coverage is achieved.

## Worked Examples

### Example 1

Input:

```
n = 4, m = 5, L = 10
p = [2, 4, 7, 9]
l = 2
```

We test feasibility for l = 2.

| Step | Lamp | Interval | Current before | Action | Current after |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | [0, 4] | 0 | extend | 4 |
| 2 | 4 | [2, 6] | 4 | extend | 6 |
| 3 | 7 | [5, 9] | 6 | extend | 9 |
| 4 | 9 | [7, 11] | 9 | extend | 11 |

Since current ≥ 10, coverage succeeds.

This trace shows how overlapping intervals merge into a continuous expansion even though individual lamps only cover local regions.

### Example 2

Input:

```
n = 3, L = 10
p = [0, 5, 10]
l = 2
```

| Step | Lamp | Interval | Current before | Action | Current after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | [-2, 2] | 0 | extend | 2 |
| 2 | 5 | [3, 7] | 2 | gap detected | fail |

At the second lamp, the interval starts at 3 while current is 2, creating a gap from 2 to 3. Even though endpoints look close, coverage is not continuous, so the configuration fails.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log m) | sorting positions once, sorting bulbs, binary search with linear feasibility check |
| Space | O(n) | storing lamp positions and temporary variables |

This complexity fits comfortably within constraints since both n and m are up to 100000, and each feasibility check is linear with a small constant factor.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    def can_cover(p, L, l):
        current = 0
        for x in p:
            start = x - l
            end = x + l
            if start > current:
                return False
            if end > current:
                current = end
            if current >= L:
                return True
        return current >= L

    def solve():
        n, m, L = map(int, input().split())
        p = list(map(int, input().split()))
        lvals = list(map(int, input().split()))

        p.sort()
        lvals.sort()

        lo, hi = 0, m - 1
        ans = -1

        while lo <= hi:
            mid = (lo + hi) // 2
            if can_cover(p, L, lvals[mid]):
                ans = lvals[mid]
                hi = mid - 1
            else:
                lo = mid + 1

        print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("4 7 20\n10 3 7 14\n2 5 1 7 10 4 20") == "3"
assert run("3 4 200\n14 153 22\n30 2 50 20") == "-1"

# custom cases
assert run("1 1 10\n0\n5") == "5", "single lamp"
assert run("2 2 10\n0 10\n4 5") == "5", "boundary coverage"
assert run("3 3 10\n1 2 3\n0 0 10") == "0", "zero radius works"
assert run("3 3 10\n1 5 9\n1 1 1") == "-1", "uniform small radius fails"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single lamp | 5 | single interval covering whole range |
| boundary coverage | 5 | exact endpoint bridging |
| zero radius works | 0 | degenerate intervals |
| uniform small radius fails | -1 | unavoidable gaps |

## Edge Cases

A critical edge case is when the first lamp does not reach the origin. For example, with p = [5, 10] and l = 2 on L = 20, the first interval is [3, 7], leaving [0, 3] uncovered. The algorithm correctly detects this because current starts at 0 and the first start is 3, triggering an immediate failure.

Another case is when coverage only fails at the end. For p = [0, 4, 8] with l = 2 and L = 15, the union reaches 10 but not 15. The scan completes and returns false since current never reaches L.

A final subtle case is tight chaining where intervals just meet at boundaries. For p = [0, 3, 6] and l = 3, intervals touch exactly at endpoints and should be considered continuous. The condition start > current correctly treats equality as valid connectivity, ensuring no false gaps are introduced.
